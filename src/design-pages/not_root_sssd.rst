Running SSSD as a non-root user
===============================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2370 <https://pagure.io/SSSD/sssd/issue/2370>`__

Problem statement
-----------------

Currently, all SSSD processes run as the root user. However, if one of
the processes was compromised, this might lead to compromising the whole
system, especially if additional measures like SELinux were not enabled.
It would improve security if instead SSSD was running as its own private
user, This design page summarizes what would be needed to run sssd as a
non-privileged user and all the cases that currently require a root
user.

Use case
--------

This is a general use-case, following the principle of least privilege.
The processes should not run as root unless they really need the root
privileges.

Important note
--------------
The text below describes initial design. The sssd-2.10 release introduces major
improvements and changes in this area. For more details, please refer to the
`SSSD 2.10.0-beta1 <https://sssd.io/release-notes/sssd-2.10.0-beta1.html#general-information>`__
and `SSSD 2.10.0-beta2 <https://sssd.io/release-notes/sssd-2.10.0-beta2.html#packaging-changes>`__
Release Notes.

Implementation details
----------------------

At a higher level, the changes would amount to:

-  A new system user would be created. This user must be added in
   sssd.spec during the ``%pre`` section.
-  Files that were used by sssd and previously owned by root should now
   be owned as the sssd user. This includes the LDB databases.
-  Responders and back ends would drop privileges and become the sssd
   user as soon as possible, ideally as the first action after startup.
-  Short-lived processes that are spawned by ``sssd_be`` but might still
   require elevated privileges would be setuid root.

The changes to individual binaries and files are described in more
detail below. After the changes are implemented, the code that runs as
root will be reduced to the monitor process and the setuid helpers.

A new system user
-----------------

The sssd will run as a new system user called simply ``sssd``. We do not
need to have the UID fixed across systems as no files owned by SSSD are
shared among different systems. The user will be simply added during the
``%pre`` phase: ::

    %pre
    getent group sssd >/dev/null || groupadd -r sssd
    getent passwd sssd >/dev/null || useradd -r -g sssd -d / -s /sbin/nologin -c "User for sssd" sssd

As it's common practice for system users, the shell will be
``/sbin/nologin`` so the user cannot log in into the system.

Configuration options
~~~~~~~~~~~~~~~~~~~~~

To be on the safe side, sssd will allow configuring the user to run as.
This option will also allow root, to allow users to keep the old
behaviour around in case they hit a bug with the unprivileged process.
As a first step, we will include these options, but leave the default as
'root'. When we're certain the non-root sssd works for most users as a
non-privileged user, we will switch the default to the sssd user.

Dropping privileges of the SSSD processes
-----------------------------------------

The goal is for the "worker" processes (that is, both responders and
providers) to drop the root privileges as soon as possible - typically
right after startup, or alternatively after completing any work that
requires root privileges such as opening a file. Because the processes
might have to keep the root privileges after startup, the monitor
process would still be running as root.

Monitor (sssd)
~~~~~~~~~~~~~~

The monitor process would keep running as root. This is in order to be
able to fork and exec processes that are initially privileged without
making them all setuid. As a future enhancement, the process management
functionality of the monitor will be delegated to systemd (see ticket
`#2243 <https://pagure.io/SSSD/sssd/issue/2243>`__).

Responders
~~~~~~~~~~

The responder processes are by nature 'readers' that mostly read data
from cache and request cache updates from the back end processes.

NSS responder
^^^^^^^^^^^^^

The NSS responder can drop privileges after startup. The files that the
NSS responder reads (sysdb, confdb, NSS pipe) and writes (memory cache,
debug logs, NSS pipe) will be owned by the sssd user.

PAM responder
^^^^^^^^^^^^^

The PAM responder can drop privileges after startup. The files that the
PAM responder reads (sysdb, confdb, PAM public pipe) and writes (debug
logs, PAM pipe) will be owned by the sssd user.

In order to keep the privileged pipe only owned by the root user, we
would open the pipe prior to becoming user and pass the file descriptor.

InfoPipe responder
^^^^^^^^^^^^^^^^^^

The InfoPipe responder can drop privileges after startup. The files that
the InfoPipe responder reads (sysdb, confdb) and writes (debug logs, PAM
pipe) will be owned by the sssd user.

Contrary to other responders, the InfoPipe responder doesn't have a
public pipe. The InfoPipe responder also binds to the system bus, we
must also convert the bus policy file to allow the sssd user to bind to
the bus.

Currently there is also functionality to modify sssd.conf from the
InfoPipe. During the feature design review, it was suggested that a
configuration interface doesn't belong to the InfoPipe code at all and
should be moved to a separate helper. Until that is done, the InfoPipe
responder must keep running as root. The work on splitting the InfoPipe
is tracked by
`https://pagure.io/SSSD/sssd/issue/2395 <https://pagure.io/SSSD/sssd/issue/2395>`__

Autofs, SUDO and SSH responders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Autofs, SUDO and SSH responders only read from the sysdb, confdb and
their respective UNIX public pipes. These responders also only write to
the debug logs and the public pipe, all of which would be owned by the
sssd user. This means the Autofs, SUDO and SSH responders can drop
privileges right after startup.

Providers
~~~~~~~~~

The providers are dynamically loadable libraries that are loaded by the
``sssd_be`` process. After startup, the sssd\_be process dlopens the
provider library and dlsyms the handlers. During sssd operation, the
``sssd_be`` process mostly unpacks requests arriving on the SBUS and
calls the provider-specific handlers.

Several areas of the initialization still require elevated privileges:

-  Checking for principals in the keytab
-  Checking for user TGTs to be renewed

Therefore, the initialization is still performed with root privileges
and sssd\_be drops to a non-root user post initialization. See the
"Future Enhancements" section for ideas on reducing the code that runs
as root during initialization even further.

Short-lived processes
~~~~~~~~~~~~~~~~~~~~~

The purpose of the short-lived processes is to avoid blocking calls by
performing an otherwise blocking action in a completely separate
process.

ldap\_child
^^^^^^^^^^^

The ldap\_child subprocess primes the credential cache used to establish
GSSAPI-encrypted connection. In order to do so, the ldap\_child process
needs to be able to read the keytab, which is readable by root only.
Therefore, the ldap\_child process is setuid root, with permissions set
to 4750 to make sure only the sssd user can run the ldap\_child process.
As soon as the credentials are obtained, the ldap\_child drops
privileges and continues running as the sssd user -- hence also the
resulting ccache is owned by the sssd user.

krb5\_child
^^^^^^^^^^^

The user krb5\_child runs as depends on how the SSSD back end is set up.
In the simplest case, where neither validation nor FAST are used, the
krb5\_child can drop privileges to the user who is logging in after
startup and runs unprivileged except for the initialization part.

In case either validation or FAST are used, part of the krb5\_child runs
as root. Once the resulting ccache is validated using the keytab, the
krb5\_child process drops privileges to the user who is logging in.

See the "Future Enhancements section" for discussion of using the MEMORY
ccache to reduce the time krb5\_child runs as root.

proxy\_child
^^^^^^^^^^^^

In general, we can't make assumptions on what the PAM module we wrap
using the proxy backend requires, so at least the part of proxy child
that runs the PAM conversation should run as root. During development,
we should consider splitting the proxy\_child into a small setuid helper
that would still run privileged and only wrap the PAM module and the
rest of the proxy\_child that would run unprivileged.

gpo\_child
^^^^^^^^^^

The gpo\_child process connects to a SMB share, downloads a GPO policy
file and stores it locally, by default in ``/var/lib/sss/gpo_cache``.
The gpo\_child authenticates to the SMB share using Kerberos; the
ccache, as created by ldap\_child is already accessible to the sssd
user. Since that directory would be owned by the sssd user, the
gpo\_child could run unprivileged.

ssh helpers
^^^^^^^^^^^

The SSH helpers already run non-privileged. ``sss_ssh_knownhostsproxy``
runs as the user who initiated the SSH session.
``sss_ssh_authorizedkeys`` runs as the user specified with the
AuthorizedKeysCommandUser directive in sshd\_config.

Command line tools
~~~~~~~~~~~~~~~~~~

There are two general kinds of command line tools we ship with the SSSD
- tools that manage accounts in the local backend and SSSD management
tools. All tools check if they are executed by root currently. I think
this check makes sense and should stay because all the tool are intended
for administrative purposes only.

Some of the tools can be changed to drop privileges. However, the attach
surface of these tools is small, so changing them is not a priority.
This effort is rather tracked in the Future Enhancements.

Local back end tools
^^^^^^^^^^^^^^^^^^^^

The tools either write (sss\_useradd, userdel, usermod, sss\_groupadd,
groupdel,
groupmod) or read  (sss\_groupshow) the sssd.ldb file.
But additionally, these tools also set the SELinux context of the user.
Since there is no capability to call semanage, setting the context still
requires root privileges.

sss\_seed and sss\_cache
^^^^^^^^^^^^^^^^^^^^^^^^

These two tools function similarly to the local backend management
tools, except they manipulate the domain cache. The cache is also owned
and writable by the sssd user, so would be safe to drop privileges here,
too.

sss\_debuglevel
^^^^^^^^^^^^^^^

The sss\_debuglevel tool changes the debug level of sssd on the fly. The
tool writes new debug level values to the confdb (owned by sssd) and
touches sssd.conf (ownership tbd). The tool can drop privileges to sssd
after startup.

sss\_obfuscate
^^^^^^^^^^^^^^

The sss\_obfuscate tool is written in Python and manipulates the
sssd.conf file by obfuscating the input and using it as a value of the
``ldap_default_authtok`` configuration option. For dropping privileges
of the sss\_obfuscate tool, we can use the python bindings of libcap-ng.
Again, making this tool non-privileged is not a priority.

External resources currently requiring root access
--------------------------------------------------

This part of the design page summarizes which external resources,
typically file system objects currently require SSSD to have elevated
privileges.

For filesystem objects, we can either change their owner to the sssd
local user, add an ACL or open them as the privileged process and pass
the file descriptor.

SSSD configuration file
~~~~~~~~~~~~~~~~~~~~~~~

-  Filesystem path: ``/etc/sssd/sssd.conf``
-  Current owner and permissions: root.root 0600
-  Read by: The monitor process
-  Written to by: The InfoPipe responder and users of the configAPI,
   such as sss\_obfuscate or authconfig
-  *Change: Currently the permissions will stay the same as the monitor
   process and the InfoPipe still run as root*

Debug logs
~~~~~~~~~~

-  Filesystem path: ``/var/log/sssd/*.log``
-  Current owner and permissions: root.root 0600
-  Read by: N/A, only externally by admin
-  Written to by: monitor, providers, responders, child processes
-  *New owner and permissions: sssd.sssd 0600*

The configuration database
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Filesystem path: ``/var/lib/sss/db/config.ldb``
-  Current owner and permissions: root.root 0600
-  Read by: responders, providers, monitor, command-line tools
-  Written to by: The monitor process, sssd-ad (a single confdb\_set
   call), sss\_debuglevel, sssd\_ifp
-  *New owner and permissions: sssd.sssd 0600*

The on-disk cache (sysdb)
~~~~~~~~~~~~~~~~~~~~~~~~~

-  Filesystem path: ``/var/lib/sss/db/cache_$domain.ldb``
-  Current owner and permissions: root.root 0600
-  Read by: responders, providers, command-line tools
-  Written to by: sssd\_be, the CLI tools
-  *New owner and permissions: sssd.sssd 0600*

Memory Cache
~~~~~~~~~~~~

-  Filesystem path: ``/var/lib/sss/mc/{passwd,group}``
-  Current owner and permissions: root.root 0644
-  Read by: The SSS NSS module
-  Written to by: The NSS responder
-  *New owner: sssd.sssd permissions will stay the same*

Kerberos keytab
~~~~~~~~~~~~~~~

-  Filesystem path: configurable, ``/etc/krb5.keytab`` by default
-  Current owner and permissions: root.root 0600
-  Read by: LDAP, KRB5, IPA, AD providers, krb5\_child, ldap\_child
-  Written to by: sssd\_be, the CLI tools
-  *Change: No change at the moment. The keytab will be kept readable by
   the root user only*

Kerberos user credential cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Filesystem path: Configurable, only if FILE or DIR based cache is
   used, which is not the default anymore
-  Current owner and permissions: the user who logged in, 0600
-  Read by: KRB5, AD, IPA, krb5\_child, libkrb5 externally
-  Written to by: krb5\_child
-  *Change: No change, the credential cache will still be written as the
   user in question*

Kerberos LDAP credential cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Filesystem path: ``/var/lib/sss/db/ccache_$domain``
-  Current owner and permissions: root.root 0600
-  Read by: AD, IPA and LDAP providers (coded up in LDAP provider tree)
-  Written to by: ldap\_child
-  No change needed since ldap\_child will run as the sssd user in the
   new design
-  *New owner and permissions: sssd.sssd 0600*

Kerberos kdcinfo files
~~~~~~~~~~~~~~~~~~~~~~

-  Filesystem path: ``/var/lib/sss/pubconf/*``
-  Current owner and permissions: root.root. The directory has
   permissions of 0755, the files 0644
-  Read by: libkrb5
-  Written to by: LDAP, KRB5, IPA, AD providers, krb5\_child,
   ldap\_child
-  *New owner and permissions: Both directory and files will be owned by
   sssd.sssd, the permissions will stay the same*

SELinux user mappings
~~~~~~~~~~~~~~~~~~~~~

-  Filesystem path: ``/etc/selinux/targeted/logins``
-  Current owner and permissions: root.root. The directory has
   permissions of 0755, the files 0644
-  Read by: pam\_selinux
-  Written to by: IPA provider
-  *Change: libsemanage will be used to set the labels instead. Since
   setting the label is a privileged operation and sssd\_be runs
   unprivileged, setting the label was moved to a separate child
   process, selinux\_child*

UNIX pipes
~~~~~~~~~~

-  Filesystem path: ``/var/lib/sss/pipes/``
-  Current owner and permissions: root.root. The directory has
   permissions of 0755, the files 0666. There is one pipe per responder.
-  Read by: client modules, all responders except InfoPipe
-  Written to by: client modules, responders
-  *New owner and permissions: Both directory and files will be owned by
   sssd.sssd, the permissions will stay the same*

UNIX PAM private pipe
~~~~~~~~~~~~~~~~~~~~~

-  Filesystem path: ``/var/lib/sss/pipes/private/pam``
-  Current owner and permissions: root.root. The directory has
   permissions of 0700, the files 0600. Only the PAM responder uses the
   private pipe.
-  Read by: PAM responder
-  Written to by: PAM client module
-  *New owner and permissions: The directory will be owned by sssd.sssd,
   the file will stay the same*

Data Provider private pipes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Filesystem path: ``/var/lib/sss/pipes/private/sbus-dp_$domain.$PID``
-  Current owner and permissions: root.root. The directory has
   permissions of 0700, the files 0600.
-  Read by: Responders
-  Written to by: Data Provider
-  *New owner and permissions: Both directory and files will be owned by
   sssd.sssd, the permissions will stay the same*

Kerberos configuration file
---------------------------

-  Filesystem path: ``/etc/krb5.conf``
-  Read by: libkrb5
-  Written to by: The IPA and AD providers "touch" the file in order to
   make libkrb5 re-read it
-  *Change: The file can be opened before dropping privileges and we can
   keep the fd around. Alternatively, the modification can be performed
   with a setuid helper*

Configuration changes
---------------------

There is a new option called ``user`` that allows the administrator to
configure the user sssd runs as. Please note that it makes sense to only
use either root or the user sssd was configured with.

How to test
-----------

Test ordinary SSSD operations. Everything must work as it used to
before. Pay special attention to operations that involve the short-lived
processes, like GSSAPI LDAP provider authentication or Kerberos user
authentication.

Upgrade testing must be performed as well.

Future Enhancements
-------------------

During the design or implementation, we identified several ideas for
improvement. Even though we don't need to implement these now, it makes
sense to keep the description in this design page for future.

Allow the InfoPipe responder to run as sssd user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In 1.12.3, sssd.conf is still owned by root, mostly because there is a
number of programs like authconfig that generate sssd.conf as root.
Moreover, in enterprise setups, the sssd.conf would be pushed to the
client with a tool such as puppet that would still use the same
privileges.

Therefore, even rootless sssd needs to handle sssd.conf owned by root,
at least for the time being. We can even chown the file to sssd user
after startup or move the write-operation in
`InfoPipe? <https://docs.pagure.org/sssd-test2/InfoPipe.html>`__ to a
privileged helper.

-  Tracked by:
   `https://pagure.io/SSSD/sssd/issue/2395 <https://pagure.io/SSSD/sssd/issue/2395>`__

Allow the command line tools to run unprivileged
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some command line tools can be run unprivileged - see the section called
"Command Line Tools". However, changing them is not a priority as they
are short-lived and in general only accept switches, not free-form
input.

-  Tracked by:
   `https://pagure.io/SSSD/sssd/issue/2500 <https://pagure.io/SSSD/sssd/issue/2500>`__

Splitting the back end initialization into privileged and unprivileged part
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It was proposed on the sssd-devel list that the initialization of the
sssd\_be process is split into a privileged and non-privileged function.
The back end would open all providers, call the privileged
initialization functions and then drop privileges. Currently all
initialization is done as root, which is not strictly required in many
setups.

-  Tracked by:
   `https://pagure.io/SSSD/sssd/issue/2504 <https://pagure.io/SSSD/sssd/issue/2504>`__

Using Kerberos MEMORY cache to avoid further restrict running Kerberos helpers as root
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sumit proposed that the keytab is read to a MEMORY type after child
process startup so krb5\_child and ldap\_child can drop root privileges
sooner. There are even some proof-of-concept patches `on sssd-devel
<https://lists.fedorahosted.org/archives/list/sssd-devel@lists.fedorahosted.org/message/XREVGCOZ4OP4VM337M5TUQYHUUPS54HH/>`__

-  Tracked by:
   `https://pagure.io/SSSD/sssd/issue/2503 <https://pagure.io/SSSD/sssd/issue/2503>`__

Using libcap-ng to drop the privileges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once we need to not only drop privileges but also retain some capability
(CAP\_AUDIT comes to mind), we'll need to use something like
`libcap-ng <https://people.redhat.com/sgrubb/libcap-ng/>`__ instead of
handling capabilities ourselves with prctl

The downside is obviously the extra dependency, but libcap-ng has a
small footprint and is already used by packages that are present on
most, if not all, modern GNU/Linux installations, such as dbus.

We would keep the existing code around as a fallback for environments
that don't have the libcap-ngs library available, such as non-Linux
systems or embedded systems. Because the code wouldn't be enabled by
default, it's important to have unit tests for the privilege drop. For
unit testing both options (libcap-ng and our own code),
`uid\_wrapper <http://cwrap.org/uid_wrapper.html>`__ and
`nss\_wrapper <http://cwrap.org/nss_wrapper.html>`__ are the best
choice.

-  Tracked by:
   `https://pagure.io/SSSD/sssd/issue/2482 <https://pagure.io/SSSD/sssd/issue/2482>`__

Merge the ldap\_child and krb5\_child processes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

During design review, it was also proposed to look into merging the
ldap\_child and krb5\_child as the code performs similar tasks The new
krb5\_child would act as an ldap\_child based on a command line option
value.

-  Tracked by:
   `https://pagure.io/SSSD/sssd/issue/2502 <https://pagure.io/SSSD/sssd/issue/2502>`__

Authors
-------

-  Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
-  Simo Sorce <`simo@redhat.com <mailto:simo@redhat.com>`__
