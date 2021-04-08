.. highlight:: none

Systemd Activatable Responders
==============================

Related ticket(s):
------------------
  * https://pagure.io/SSSD/sssd/issue/2243
  * https://pagure.io/SSSD/sssd/issue/3129
  * https://pagure.io/SSSD/sssd/issue/3245

Problem statement
-----------------
SSSD has some responders which don't have to be running all the time, but could
be ``socket-activated`` or ``dbus-activated`` instead on platforms where it's
supported. That's the case, for instance, for the ``IFP``, ``SSH`` and ``Sudo``
responders.

Making these responders socket-activated or dbus-activated would provide a
better user experience, as these services could be started on-demand when a
client needs them and exit after a period of inactivity.

Currently, the Administrator has to explicitly list all the services that might
be potentially needed in the ``services`` line of ``[sssd]`` section and those
processes will be running all the time.

Use cases
---------
 * sssctl: As more and more features had been added depending on the ``IFP``
   responder being activated, leaving this responder to be started on-demand
   instead of having the admins explicitly setting them up is desired;

 * KCM: The KCM responder is only seldom needed, when libkrb5 needs to access
   the credentials store. At the same time, the KCM responder must be running
   if Kerberos credentials cache defaults to KCM. Socket-activating this
   responder would solve both of the cases;

 * AutoFS: The AutoFS responder is typically needed only when a shared
   directory is about to be mounted.

Overview of the solution
------------------------
The solution agreed on the mailing list is to add a new unit file for each one
of the responders. Once a responder is started, it will communicated to the
monitor in order to let the monitor know that it's up and then the monitor will
take care of registering the responder, which basically consists in marking the
service as started, increasing the services' counter, getting the responders'
configuration and finally adding the responder to the services' list. A
configurable idle timeout will be implemented the responders, in order to
shut the process down in case it becomes idle.

Implementation details
----------------------
In order to achieve our goal we will need some small modifications in the
responders' common code to make those ready for socket-activation, add a
systemd unit file for each of the responders, add a new binary file to ensure
that the Administrator won't mix up those two methods of starting services
(for the very same service) and finally do some changes in the
monitor code for managing the socket-activated service.

The change in the responders' common code is quite trivial and goes towards
calling ``activate_unix_sockets()`` function instead of ``set_unix_socket()``.
The important part around this change is to avoid the responders' file
descriptors to be set as -1 in all cases as it would cause the socket to be
unreachable in case the Administrator decides to move back from using the
socket-activated services to the default way.

The systemd units for the responders will look like:
 * NSS responder: NSS is a really special case as it cannot have be run as
   unprivileged user. It happens because libc does initgroups on pretty much
   any account and initgroups checks all NSS modules in order to be precise,
   causing ``nss_sss`` to trigger the ``NSS responder`` ... so a cycle
   dependency would happen.

   * sssd-nss.service::

        [Unit]
        Description=SSSD NSS Service responder
        Documentation=man:sssd.conf(5)
        After=sssd.service
        BindsTo=sssd.service
        RefuseManualStart=true

        [Install]
        Also=sssd-nss.socket

        [Service]
        ExecStart=@libexecdir@/sssd/sssd_nss --debug-to-files --socket-activated
        Restart=on-failure

   * sssd-nss.socket::

        [Unit]
        Description=SSSD NSS Service responder socket
        Documentation=man:sssd.conf(5)
        After=sssd.service
        BindsTo=sssd.service
        Before=sssd-autofs.socket sssd-pac.socket sssd-pam.socket sssd-ssh.socket sssd-sudo.socket
        DefaultDependencies=no
        Conflicts=shutdown.target

        [Socket]
        ExecStartPre=@libexecdir@/sssd/sssd_check_socket_activated_responders -r nss
        ListenStream=@pipepath@/nss

        [Install]
        WantedBy=sssd.service

 * PAM responder: PAM is a little bit special as it has two sockets associated
   to itself.

   * sssd-pam.service::

        [Unit]
        Description=SSSD PAM Service responder
        Documentation=man:sssd.conf(5)
        After=sssd.service
        BindsTo=sssd.service
        RefuseManualStart=true

        [Install]
        Also=sssd-pam.socket sssd-pam-priv.socket

        [Service]
        ExecStartPre=-/bin/chown @SSSD_USER@:@SSSD_USER@ @logpath@/sssd_pam.log
        ExecStart=@libexecdir@/sssd/sssd_pam --debug-to-files --socket-activated
        Restart=on-failure
        User=@SSSD_USER@
        Group=@SSSD_USER@
        PermissionsStartOnly=true

   * sssd-pam.socket::

        [Unit]
        Description=SSSD PAM Service responder socket
        Documentation=man:sssd.conf(5)
        After=sssd.service
        BindsTo=sssd.service
        BindsTo=sssd-pam-priv.socket
        DefaultDependencies=no
        Conflicts=shutdown.target

        [Socket]
        ExecStartPre=@libexecdir@/sssd/sssd_check_socket_activated_responders -r pam
        ListenStream=@pipepath@/pam
        SocketUser=root
        SocketGroup=root

        [Install]
        WantedBy=sssd.service

   * sssd-pam-private.socket::

        [Unit]
        Description=SSSD PAM Service responder private socket
        Documentation=man:sssd.conf(5)
        After=sssd.service
        BindsTo=sssd.service
        BindsTo=sssd-pam.socket
        DefaultDependencies=no
        Conflicts=shutdown.target

        [Socket]
        ExecStartPre=@libexecdir@/sssd/sssd_check_socket_activated_responders -r pam
        Service=sssd-pam.service
        ListenStream=@pipepath@/private/pam
        SocketUser=root
        SocketGroup=root
        SocketMode=0600

        [Install]
        WantedBy=sssd.service

 * AutoFS, PAC, Ssh and Sudo responders:

   * sssd-@responder@.service::

        [Unit]
        Description=SSSD @responder@ Service responder
        Documentation=man:sssd.conf(5)
        After=sssd.service
        BindsTo=sssd.service
        RefuseManualStart=true

        [Install]
        Also=sssd-@responder@.socket

        [Service]
        ExecStartPre=-/bin/chown @SSSD_USER@:@SSSD_USER@ @logpath@/sssd_autofs.log
        ExecStart=@libexecdir@/sssd/sssd_@responder@ --debug-to-files --socket-activated
        Restart=on-failure
        User=@SSSD_USER@
        Group=@SSSD_USER@
        PermissionsStartOnly=true

   * sssd-@responder@.socket::

        [Unit]
        Description=SSSD @responder@ Service responder socket
        Documentation=man:sssd.conf(5)
        After=sssd.service
        BindsTo=sssd.service
        DefaultDependencies=no
        Conflicts=shutdown.target

        [Socket]
        ExecStartPre=@libexecdir@/sssd/sssd_check_socket_activated_responders -r @responder@
        ListenStream=@pipepath@/@responder@
        SocketUser=@SSSD_USER@
        SocketGroup=@SSSD_USER@

        [Install]
        WantedBy=sssd.service

 * IFP responder: While the other responders are going to be socket-activated,
   IFP will be dbus-activated:

   * sssd-ifp.service::

        [Unit]
        Description=SSSD IFP Service responder
        Documentation=man:sssd-ifp(5)
        After=sssd.service
        BindsTo=sssd.service

        [Service]
        Type=dbus
        BusName=org.freedesktop.sssd.infopipe
        ExecStart=@libexecdir@/sssd/sssd_ifp --uid 0 --gid 0 --debug-to-files --dbus-activated
        Restart=on-failure


The newly added binary does nothing but check in the config files whether the
responder that is about to be activated is also listed in the ``services`` of
the configuration file. In case it's there, the services' socket is not
started, fallbacking to the default way.

And, finally, the code on the monitor side will have to have some adjustments
in order to properly deal with an empty list of services and, also, to register
the service when it is stated.

As just the responders will be socket-activated (for now), the service type
will have to be exposed and passed through sbus when calling the
``RegistrationService`` method and then the monitor will properly do the
services' registration when the method's callback is triggered. As mentioned
before, the registration that has to be done consists in:

 * Marking the service as started;
 * Increasing the services' counter;
 * Getting the services' configuration;
 * Setting the services' restart number;
 * Adding the service to the services' list;

Unregistering a socket-activated responder will also be done by the monitor
when the connection between the service and the monitor is closed.

Configuration changes
---------------------
After this design is implemented, the ``services`` line in ``sssd.conf`` will
become optional for platforms where systemd is present. Note that in order to
keep backward compatibility, if the ``services`` line is present, the services
will behave exactly as they did before these changes.

How To Test
-----------
The easiest way to test is removing the service from sssd.conf's  ``services``
line, enabling the service's socket and trying to use SSSD normally.

See below an example of how to enable NSS and PAM sockets::

    # systemctl enable sssd-nss.socket sssd-pam.socket
    # systemctl start sssd-nss.socket sssd-pam.socket

Using sssctl tool without having the IFP responder set in the ``services`` line
is another way to test.

How To Debug
------------
The easiest way to debug this new feature is taking a look on the responders'
common initialization code and in the monitors' client registration code.

Is worth to mention that disabling the systemd's sockets will prevent the
responders' services to be started.

Authors
-------
Fabiano Fidencio <fidencio@redhat.com>
