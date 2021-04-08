Socket Activatable Responders
=============================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2243 <https://pagure.io/SSSD/sssd/issue/2243>`__
-  `https://pagure.io/SSSD/sssd/issue/3129 <https://pagure.io/SSSD/sssd/issue/3129>`__
-  `https://pagure.io/SSSD/sssd/issue/3245 <https://pagure.io/SSSD/sssd/issue/3245>`__

Problem statement
~~~~~~~~~~~~~~~~~

SSSD has some responders which don't have to be running all the time,
but could be socket-activated instead in platforms where it's supported.
That's the case, for instance, for the IFP, ssh and sudo responders.
Making these responders socket-activated would provide a better use
experience, as these services could be started on-demand when a client
needs them and exist after a period of inactivity. Currently the admin
has to explicitly list all the services that might potentially be needed
in the ``services`` section and the processes have to be running all the
time.

Use cases
~~~~~~~~~

sssctl
^^^^^^

As more and more features that had been added depending on the IFP
responder, we should make sure that the responder is activated on demand
and the admins doesn't have to activate it manually.

KCM
^^^

The KCM responder is only seldom needed, when libkrb5 needs to access
the credentials store. At the same time, the KCM responder must be
running if the Kerberos credentials cache defaults to ``KCM``.
Socket-activating the responder would solve both of these cases.

autofs
^^^^^^

The autofs responder is typically only needed when a share is about to
be mounted.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

The solution agreed on the mailing list is to add a new unit for each
one of the responders. Once a responder is started, it will communicate
to the monitor in order to let the monitor know that it's up and the
monitor will do the registration of the responder, which basically
consists in marking the service as started, increasing the services'
counter, getting the responder's configuration, adding the responder to
the service's list. A configurable idle timeout will be implemented in
each responder, as part of this task, in order to exit the responder in
case it's not used for a few minutes.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

In order to achieve our goal we will need a small modification in
responders' common code in order to make it ready for socket-activation,
add some systemd units for each of the responders and finally small
changes in the monitor code in order to manage the new activated
service.

The change in the responders' common code is quite trivial, just change
the sss\_process\_init code to call activate\_unix\_sockets() instead of
set\_unix\_socket(). Something like: ::

    -    ret = set_unix_socket(rctx, conn_setup);
    +    ret = activate_unix_sockets(rctx, conn_setup);

The units that have to be added for each responder must look like:

sssd-@responder@.service.in (for services which can be run as
unprivileged user): ::

    [Unit]
    Description=SSSD SSH Service responder
    Documentation=man:sssd.conf(5)
    After=sssd.service
    BindsTo=sssd.service

    [Install]
    Also=sssd-ssh.socket

    [Service]
    ExecStartPre=-/bin/chown @SSSD_USER@:@SSSD_USER@ @logpath@/sssd_ssh.log
    ExecStart=@libexecdir@/sssd/sssd_@responder@ --debug-to-files --socket-activated
    Restart=on-failure
    User=@SSSD_USER@
    Group=@SSSD_USER@
    PermissionsStartOnly=true

sssd-@responder@.service.in (for services which cannot be run as
unprivileged user): ::

    [Unit]
    Description=SSSD NSS Service responder
    Documentation=man:sssd.conf(5)
    After=sssd.service
    BindsTo=sssd.service

    [Install]
    Also=sssd-nss.socket

    [Service]
    ExecStartPre=-/bin/chown root:root @logpath@/sssd_nss.log
    ExecStart=@libexecdir@/sssd/sssd_nss --debug-to-files --socket-activated
    Restart=on-failure

sssd-@responder@.socket.in: ::

    [Unit]
    Description=SSSD NSS Service responder socket
    Documentation=man:sssd.conf(5)
    BindsTo=sssd.service

    [Socket]
    ListenStream=@pipepath@/@responder@
    SocketUser=@SSSD_USER@
    SocketGroup=@SSSD_USER@

    [Install]
    WantedBy=sssd.service

Some responders may have more than one socket, which is the case of PAM,
so another unit will be needed.

sssd-@responder@-priv.socket.in: ::

    [Unit]
    Description=SSSD PAM Service responder private socket
    Documentation=man:sssd.conf(5)
    BindsTo=sssd.service
    BindsTo=sssd-@responder@.socket

    [Socket]
    Service=sssd-@responder@.service
    ListenStream=@pipepath@/private/@responder@
    SocketUser=root
    SocketGroup=root
    SocketMode=0600

    [Install]
    WantedBy=sssd.service

Last but not least, the IFP responder doesn't have a socket. It's going
to be D-Bus activated and some small changes will be required on its
D-Bus service unit (for platforms where systemd is supported). ::

    -Exec=@libexecdir@/sssd/sss_signal
    +ExecStart=@libexecdir@/sssd/sssd_@responder@ --uid 0 --gid 0 --debug-to-files --dbus-activated
    +SystemdService=sssd-ifp.service
    +Restart=on-failure

And, finally, the code in the monitor side will have to have some
adjustments in order to properly deal with an empty list of services
and, also, to register the service when it's started.

As just the responders' will be socket-activated for now, the service
type will have to exposed and passed through sbus when calling the
RegistrationService method and the monitor will have to properly do
the registration of the service when RegistrationService callback is
triggered. As mentioned before, the "registration" that has to be done
from the monitor's side is:

-  Mark the service as started;
-  Increase the services' counter;
-  Get the responders' configuration;
-  Set the service's restart number;
-  Add the service to the services' list.

"Unregistering" a socket-activated service will be done when the
connection between the service and the monitor is closed.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

After this design is implemented, the "services" line in sssd.conf will
become optional for platforms where systemd is present. Note that in
order to keep backward compatibility, if the "services" line is present,
the services will behave exactly as they did before these changes.

How To Test
~~~~~~~~~~~

The easiest way to test is removing the "services" line from sssd.conf
and try to use SSSD normally. Using sssctl tool without having the ifp
responder set in the "services" line is another way to test.

How To Debug
~~~~~~~~~~~~

The easiest way to debug this new feature is taking a look on the
responders' common initialization code and in the monitors' client
registration code. Is worth to mention that disabling the systemd's
services/sockets will prevent the responders' services to be started.

Authors
~~~~~~~

Fabiano Fidêncio <`fidencio@redhat.com <mailto:fidencio@redhat.com>`__>
