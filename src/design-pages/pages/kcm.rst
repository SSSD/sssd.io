.. highlight:: none

KCM server for SSSD
===================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/2887


Problem statement
-----------------
Over time, both ``libkrb5`` and SSSD used different credential cache types
to store Kerberos credentials - going from a simple file-based storage
(``FILE:``) to a directory (``DIR:``) and most recently a kernel-keyring based
cache (``KEYRING:``).

Each of these caches has its own set of advantages and disadvantages. The
``FILE`` ccache is very widely supported, but does not support multiple
primary caches. The ``DIR`` cache does, but creating and managing the
directories including proper access control can be tricky. The ``KEYRING``
cache is not well suited for cases where multiple semi-isolated environments
might share the same kernel. Managing credential caches' lifetime is not
well solved in neither of these cache types automatically, only with the
help of a daemon like SSSD.

With KCM, the Kerberos caches are not stored in a "passive" store, but
managed by a daemon. In this setup, the Kerberos library (typically used
through an application, like for example, ``kinit``) is a *KCM client*
and the daemon is being referred to as a *KCM server*.

Having the Kerberos credential caches managed by a daemon has several
advantages:

 * the daemon is stateful and can perform tasks like Kerberos credential
   cache renewals or reaping old ccaches. Some tasks, like renewals are
   possible already with SSSD, but only for tickets that SSSD itself acquired
   (typically via a login through ``pam_sss.so``) and tracks. Tickets acquired
   otherwise, most notably though kinit wouldn't be tracked and renewed.
 * since the process runs in userspace, it is subject
   to UID namespacing, `unlike the kernel keyring
   <http://www.projectatomic.io/blog/2014/09/yet-another-reason-containers-don-t-contain-kernel-keyrings>`_
 * unlike the kernel keyring-based cache, which is entirely dependant on
   UIDs of the caller and in a containerized environment is shared between
   all containers, the KCM server's entry point is a UNIX socket which can
   be bind-mounted to only some containers

At the moment, only the Heimdal implementation of Kerberos contains a KCM
server. This design page describes adding a KCM server to SSSD as a new
SSSD service called ``sssd_kcm``.

External links:
---------------
 * `MIT wiki KCM documentation <http://k5wiki.kerberos.org/wiki/Projects/KCM_client>`_
 * `Heimdal upstream KCM documentation <https://www.h5l.org/manual/HEAD/info/heimdal/Credential-cache-server-_002d-KCM.html>`_
 * `Heimdal KCM man page <http://www.unix.com/man-page/All/8/kcm/>`_


Use cases
---------
The primary use-cases for the next SSSD upstream releases are related to
containers. In particular:

 * A sysadmin needs to deploy applications in containers without worrying
   about applications clobbering each other's credential caches in a kernel
   keyring as keyrings are not namespaced
 * An Administrator wants to initialize and ccache centrally and then
   have the ccache available in all relevant containerized applications,
   so that applications do not have deal with Kerberos authentication or
   have access to keytab separately

Having the KCM service might also enable us to solve tickets such as:
 * `RFE To delete kerberos tickets once the user logs out <https://pagure.io/SSSD/sssd/issue/2551>`_
 * `RFE Expand kerberos ticket renewal <https://pagure.io/SSSD/sssd/issue/1723>`_
 * `RFE Add a general-purpose D-Bus responder for ticket monitoring <https://pagure.io/SSSD/sssd/issue/1497>`_
 * `KCM: Implement a shim layer to format FILE-based credentials from KCM credential cache <https://pagure.io/SSSD/sssd/issue/3348>`_

Overview of the solution
------------------------
A new SSSD responder is added as part of this feature. While it's of course
possible to create a completely standalone daemon that would implement a
KCM server, doing so in the context of SSSD has some advantages, notably:

 * We can reuse a lot of code to set up and configure the server, or parse
   Kerberos related data
 * SSSD already has a D-Bus API that could publish information about
   Kerberos tickets and for example emit signals that a graphical application
   can consume
 * SSSD ships with a "secrets responder" to store data at rest. It makes
   sense to leverage this component to store Kerberos ccaches persistently

The KCM responder is socket-activated. It should be possible to use the
responder without SSSD being configured, although this feature depends on
the platform - in general this would only be possible with distributions that
enable the files provider. On older distributions (such as RHEL-7), an SSSD
domain must be enabled in order for SSSD to even generate the configuration.

The identity of the ccache owner is read from the client socket connection.
However, because in containerized environments, the same ID can often
identify multiple apps, it is important to also track the SELinux label
as part of the client identity. This would prevent two containers running with
the same ID but different SELinux label to access each other's credentials.


Differences between sssd-kcm and Heimdal KCM
--------------------------------------------
Heimdal treats the root user special in the sense that listing all ccaches
as root lists everyone's ccaches. With ``sssd-kcm``, this is not implemented.


Implementation details
----------------------
The KCM responder implements the same subset of the KCM protocol the MIT
client libraries implement. Contrary to Heimdal's KCM server that just
stores the credential caches in memory, the SSSD KCM server would store
the ccaches in the secrets database through the sssd-secret's responder
`public rest API <https://jhrozek.fedorapeople.org/sssd/1.14.2/man/sssd-secrets.5.html>`_.

For testing, an in-memory ccache storage, similar to Heimdal's was also
implemented, although this in-memory back end is not documented and should
not be used in production. If the persistent storage in sssd-secrets (which
is the default) is used, the KCM responder is allowed to idle-terminate.

For user credentials the KCM Server uses a secrets responder URI
in the form of ``http://localhost/kcm/persistent/$uid`` where ``$uid``
is the user ID of the user whose credentials are being saved. In order to
impersonate different users, the KCM responder runs as a trusted user
(defined as ``KCM_PEER_UID``, defaulting to root) and only this trusted
user can access the ``/kcm`` hive in the sssd-secrets responder.

The peer identity consists of an UID/GID tuple that is read from the
client socket using ``getsockopt(SO_PEERCRED)`` and SELinux label using
``SELINUX_getpeercon()``. To evaluate whether the MCS category the peer
is running with can access the ccache potentially created with a different
category, we'll call ``selinux_check_access()``.

Since from the point of view of the KCM responder, the operations on the
Kerberos caches should be seemingly atomic, but often the operations
might require several round-trips to the secrets storage, all operations
towards the KCM responder by a single UID are serialized.

Internally in the secrets responder, the ccaches are stored at a new
top-level anchor ``cn=kcm``. The secret responder's quotas on secrets
also apply separately to the ``cn=kcm`` tree; separately here means
that it is allowed to store ``max_secrets`` secrets and at the same
time ``max_secrets`` credential caches. There is a `separate ticket
<https://pagure.io/SSSD/sssd/issue/3363>`_ to make the quotas per-UID.

Currently, when the quota is reached we just fail. We should consider
recovering more gracefully, such as by removing the oldest service
(non-TGT) tickets.

Since the secrets responder is a key-value store at heart, but the ccaches
can be addressed by both name and UID, the key of the secrets store (the
secret's name) is a concatenation of the ccache's name and UUID. The value
(the secret) is a JSON object in the following format::

 {
     version: number
     kdc_offset: number
     principal : {
         "type": "number",
         "realm": "string",
         "components": [ "elem1", "elem2", ...]
     }

     creds : [
         {
            "uuid": <data>,
            "payload": <data>,
         }
         {
            ...
         }
         ...
     ]
 }

All the credentials are stored in the per-UID secrets container under a
container named ``ccaches``. This container is crated when a ccache is
initialized by a KCM client. There is also a secret named ``default``
which contains (as secrets value) the UUID of the default ccache, if any.

Note that the credentials themselves are not unpacked. We rather just store
exactly the same blob that the KCM client sends us. If we will support
renewals in a future version, we might need to parse the credentials as well.

Configuration changes
---------------------
The SSSD KCM responder would use the same common options like other SSSD
services such as idle timeout or debug level.

There is also an option named ``socket_path`` that lets the admin select
the UNIX socket the KCM service listens on. See the ``sssd-kcm(8)`` man
page for more details.

Packaging changes
-----------------
The KCM responder is be packaged in its own subpackage called
``sssd-kcm``. This subpackage will not be installed by default, in other
words it would not be required by the sssd meta-package, but a user will
have to install this subpackage manually. Except for the KCM responder,
the systemd socket and service file and documentation, the package
will also contain a krb5.conf snippet that enables the ``KCM`` ccache type,
so switching to the new credentials cache should be as easy as installing
the package.


How To Test
-----------
First, the KCM responder must be installed. On Fedora/RHEL, this is done
by installing the ``sssd-kcm`` subpackage.

In order for the admin to start using the KCM service, the sssd-kcm socket
must be enabled and started and the sssd-kcm service must be enabled::

 # systemctl enable sssd-kcm.socket
 # systemctl start sssd-kcm.socket
 # systemctl enable sssd-kcm.service

Please note that starting the KCM socket auto-starts the sssd-secrets
socket so that the persistent secrets storage is available.

Then, set the ``KCM`` credential type as the default for the
system. The ``sssd-kcm`` subpackage ships with a snippet file
``/etc/krb5.conf.d/kcm_default_ccache`` where it's enough to just uncomment
the following two lines::

  [libdefaults]
  default_ccache_name = KCM:

Of course, the same modification can be done directly in
``/etc/krb5.conf``. Downstreams may choose to change this include file to
enable the KCM cache directly so that just installing the ``sssd-kcm``
package with its snippet enables the KCM credential type.

After that, all common operations like ``kinit``, ``kdestroy``, ``kswitch``
or login through ``pam_sss`` should just work and store their credentials in
the KCM server. Any existing tests for other collection-aware credential
caches should work the same way. The ``KRB5CCNAME`` variable is in the form of::

    KCM:$NAME:$CACHE_ID

The ``$NAME`` represents the collection and is typically the UID of the
client. Only root is allowed to create arbitrarily named credential
caches. Please note that the names are normally selected by libkrb5,
but even attempting to do something like::

     KRB5CCNAME=KCM:foobar kinit

must not work unless done as root. The ``$CACHE_ID`` is just an identifier
of the cache in the collection. An example list of a KCM collection with
two ccache look like this::

    $ klist -A
    Ticket cache: KCM:10327:75404
    Default principal: tuser2@IPA.TEST

    Valid starting       Expires              Service principal
    04/04/2017 19:12:32  04/05/2017 19:12:29  krbtgt/IPA.TEST@IPA.TEST

    Ticket cache: KCM:10327
    Default principal: tuser1@IPA.TEST

    Valid starting       Expires              Service principal
    04/04/2017 19:12:26  04/05/2017 19:12:24  krbtgt/IPA.TEST@IPA.TEST


The KCM server implements per-UID credential cache ownership and access
control. Therefore accessing other user's credential caches as an
unprivileged user should not work::

     $ KRB5CCNAME=KCM:10327 klist

However, root can access anyone's ccache, so doing the above as root should
allow to list arbitrary user's ccaches.

Restarting the KCM server or rebooting the machine must persist the tickets
as they are stored in sssd-secrets' on-disk storage.

The next section illustrates several use-cases related to containers
step-by-step.

Use-case: separating ccaches of root users in containers, SSSD is running on the host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this scenario, SSSD is running on the host and an application is running
in a container. However, the application in a container runs as root and
we want to keep its credential caches separate from the credential caches
on the host. On the other hand we want to share the kerberos credentials
between the containers.

#. Make sure the ``sssd-kcm`` package is installed and the services and sockets enabled

#. Create a directory that will contain the KCM daemon socket::

    host # mkdir /var/run/kcm

#. Configure sssd-kcm to spawn the KCM socket there. Add the following to
   ``/etc/sssd/sssd.conf`` on the host::

    [kcm]
    socket_path = /var/run/kcm/kcm.sock

#. Restart sssd on the host to pick up the changes::

    host # systemctl restart sssd.service

#. Tune the systemd ``sssd-kcm`` socket to ensure systemd will listen on
   the same socket KCM listens on::

    host # mkdir /etc/systemd/system/sssd-kcm.socket.d
    host # cat /etc/systemd/system/sssd-kcm.socket.d/socket_override.conf
    [Socket]
    ListenStream=
    ListenStream=/var/run/kcm/kcm.sock

#. Re-read the unit file and verify the ``sssd-kcm.socket`` unit file is
   listening to the right socket::

    host # systemctl daemon-reload
    host # systemctl restart sssd-kcm.socket
    host # systemctl status sssd-kcm.socket
    host # systemctl cat sssd-kcm.socket

#. In order for the root user in the container to be represented as a
   different UID to the host, we need to create a subordinate UID and GID
   ranges that the ID from the containers will be mapped to. This range
   takes a required argument, which must correspond to a user that exists in
   ``/etc/passwd`` (although domain users `will be supported starting with
   docker 1.13 <https://github.com/docker/docker/pull/27599>`_). The
   subordinate ranges are created in ``/etc/subuid`` and
   ``/etc/subgid`` on the host. Please refer to the `docker documentation
   <https://success.docker.com/Datacenter/Apply/Introduction_to_User_Namespaces_in_Docker_Engine>`_
   for more details on Docker user namespaces. For example::

    host # useradd kcmtest
    host # grep kcmtest /etc/subgid
    kcmtest:50000:65536
    host # grep kcmtest /etc/subuid
    kcmtest:50000:65536

#. Configure the docker daemon to use this subordinate ID namespace by
   changing this line in ``/etc/sysconfig/docker``::

    OPTIONS='--selinux-enabled --log-driver=journald --userns-remap=kcmtest'

#. Restart the docker service. Please note that docker stores the images
   under a per-user-namespace directory, so you'll need to pull the images
   again::

    host # systemctl restart docker.service

#. Start a container, bind-mounting the ``/var/run/kcm`` directory from
   the host to make the KCM socket accessible::

    host # docker run -t -i -h=kcmtest1 -v=/var/run/kcm:/var/run/kcm fedora /bin/bash

#. Configure the container's Kerberos config file to use ``KCM:`` as the
   credential cache. Edit ``/etc/krb5.conf`` in the container::

    [libdefaults]
    default_realm = IPA.TEST
    dns_lookup_realm = true
    dns_lookup_kdc = true
    rdns = false
    default_ccache_name = KCM:
    kcm_socket = /var/run/kcm/kcm.sock

    [realms]
    IPA.TEST = {
        pkinit_anchors = FILE:/etc/ipa/ca.crt
        kdc = unidirect.ipa.test
    }

#. Acquire Kerberos credentials for the ``admin`` IPA user. Note that
   despite the user's UID value in the container is 0, the UID is translated
   to 50000 on the host, which is what the KCM server then uses to store the
   credentials at::

    [root@kcmtest1 /]# id
    uid=0(root) gid=0(root) groups=0(root)

    [root@kcmtest1 /]# kinit admin
    Password for admin@IPA.TEST: 

    [root@kcmtest1 /]# klist 
    Ticket cache: KCM:50000
    Default principal: admin@IPA.TEST

    Valid starting     Expires            Service principal
    11/25/16 15:29:38  11/26/16 15:29:37  krbtgt/IPA.TEST@IPA.TEST

#. Start another container, bind-mounting the `/var/run/kcm` directory
   from the host to make the KCM socket accessible::

    host # docker run -t -i -h=kcmtest2 -v=/var/run/kcm:/var/run/kcm fedora /bin/bash

#. Configure ``krb5.conf`` in the same manner and run klist (without
   kinit!) in the container. Note we can access the same ccache the first
   container acquired::

    [root@kcmtest2 /]# klist 
    Ticket cache: KCM:50000
    Default principal: admin@IPA.TEST

    Valid starting     Expires            Service principal
    11/25/16 15:29:38  11/26/16 15:29:37  krbtgt/IPA.TEST@IPA.TEST

#. root on the host cannot access the same cache by default. An interesting
   property of the KCM protocol is that UID 0 can list all ccaches or all
   other UIDs, though::

    host # klist 
    klist: Matching credential not found


Note - if the container is running as a different user (using the
``USER`` directive specified in the container's ``Dockerfile``), then the
ID the KCM server is contacted with depends on whether ID namespaces
are used. Without the ID namespaces, the host receives the UID of the
container user as-is. If user namespaces are in effect, then the ID of the
container user is translated into the subordinate namespace. For example,
if the namespace above was still in effect, a container user running as
uid=1000 would be translated into user with uid=51000 on the host.


Use-case: separating ccaches of containers from ccaches of the host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this use-case, SSSD is running in one container and keeps track of ccaches
in other containers that are completely separated from the host environment.
The containers must also share the credential caches between one another.

#. Start a container that will run an SSSD instance with the KCM service. We
   name the container ``kcmserver`` and assign a volume called ``/kcmserver``
   to this container::

    host# docker run -t -i --name=kcmserver -h=kcmserver -v=/kcmserver fedora /bin/bash

#. Install and configure sssd in the container. The configuration can be
   pretty minimal, but the important piece is the KCM socket in the Docker
   volume at ``/kcmserver/kcm.socket``. Please note that depending on your
   version, the domain might or might not be required - on Fedora, there is
   an implicit domain starting with F-26. Older versions might need to define
   a domain even if no remote server with users is being used actually::

    kcmserver # yum -y install sssd-kcm
    kcmserver # cat /etc/sssd/sssd.conf
    [sssd]
    domains = local

    [kcm]
    socket_path = /kcmserver/kcm.socket

    [domain/local]
    id_provider = local

#. Tune the systemd ``sssd-kcm`` socket to ensure systemd will listen on
   the same socket KCM listens on::

    host # mkdir /etc/systemd/system/sssd-kcm.socket.d
    host # cat /etc/systemd/system/sssd-kcm.socket.d/socket_override.conf
    [Socket]
    ListenStream=
    ListenStream=/kcmserver/kcm.socket

#. Re-read the unit file and verify the ``sssd-kcm.socket`` unit file is
   listening to the right socket::

    host # systemctl daemon-reload
    host # systemctl restart sssd-kcm.socket
    host # systemctl status sssd-kcm.socket
    host # systemctl cat sssd-kcm.socket


#. Start another container that will represent an application. Make sure
   the container mounts the volume from the ``kcmserver`` instance::

    host # docker run -t -i --name=kcmclient -h=kcmclient --volumes-from=kcmserver fedora /bin/bash

#. Observe that the container mounted the volume and the volume includes
   the KCM server socket::

    kcmclient # ll /kcmserver/kcm.socket 
    srw-rw-rw-. 1 root root 0 Nov 29 16:21 /kcmserver/kcm.socket

#. Configure ``/etc/krb5.conf`` to use ``KCM:`` as the credentials cache
   and point libkrb5 to the KCM socket::

    kcmclient # grep default_ccache_name /etc/krb5.conf
    default_ccache_name = KCM:
    kcmclient # grep kcm_socket /etc/krb5.conf
    kcm_socket = /kcmserver/kcm.socket

#. Acquire Kerberos credentials in the ``kcmclient`` container::

    kcmclient # kinit admin
    Password for admin@IPA.TEST: 
    kcmclient # klist 
        Ticket cache: KCM:0
        Default principal: admin@IPA.TEST

        Valid starting     Expires            Service principal
        11/29/16 16:21:28  11/30/16 16:21:26  krbtgt/IPA.TEST@IPA.TEST

#. Observe that these credentials are not visible to the host::

    host # klist
    klist: Matching credential not found

#. Start another container as another KCM client, configure its ``krb5.conf``
   configuration file in the same manner. As long as this container runs as
   the same UID as the first KCM client, the credentials should be visible
   in this container immediately without having to acquire them::

    kcmclient2 # klist 
        Ticket cache: KCM:0
        Default principal: admin@IPA.TEST

        Valid starting     Expires            Service principal
        11/29/16 16:21:28  11/30/16 16:21:26  krbtgt/IPA.TEST@IPA.TEST


How To Debug
------------

The SSSD KCM server would use the same DEBUG facility as other SSSD
services. In order to debug the client side operations, setting the
``KRB5_TRACE`` variable might come handy.

The KCM protocol response-request can be logged using ``strace``.

The admin might also inspect the SSSD secrets database to see what credential
caches have been stored by the SSSD.

Authors
-------
 * Jakub Hrozek <jhrozek@redhat.com>
 * Simo Sorce <simo@redhat.com>
