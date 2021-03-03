Troubleshooting Fleet Commander Integration
===========================================

This document consists in a few common issues faced while playing with Fleet
Commander integration and how to debug and solve those.

It's important to understand that the role played by SSSD in this integration
is **only** on the client side and that for general issues related to Fleet
Commander you should always refer, in the first place, to:
https://fleet-commander.org/documentation.html

Also, refer to the following design page in case you'd like to have a better
understanding of the feature itself:
https://docs.pagure.org/SSSD.sssd/design_pages/fleet_commander_integration.html


Common misconfigurations:
-------------------------

For any error seen in Fleet Commander's Cockpit plugin, please, add
``log_level = debug`` to ``/etc/xdg/fleet-commander-admin.conf`` under
``[admin]`` section and use ``journalctl`` to check for the error messages.


Can't initialize Fleet Commander
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``Error during service connection. Check system logs for details.``


.. code:: ini

    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: Traceback (most recent call last):
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: File "/usr/lib64/python2.7/runpy.py", line 162, in _run_module_as_main
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: "__main__", fname, loader, pkg_name)
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: File "/usr/lib64/python2.7/runpy.py", line 72, in _run_code
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: exec code in run_globals
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: File "/usr/share/fleet-commander-admin/python/fleetcommander/fcdbus.py", line 881, in <module>
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: svc = FleetCommanderDbusService(config)
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: File "/usr/share/fleet-commander-admin/python/fleetcommander/fcdbus.py", line 196, in __init__
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: os.makedirs(self.state_dir)
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: File "/usr/lib64/python2.7/os.py", line 150, in makedirs
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: makedirs(head, mode)
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: File "/usr/lib64/python2.7/os.py", line 150, in makedirs
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: makedirs(head, mode)
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: File "/usr/lib64/python2.7/os.py", line 150, in makedirs
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: makedirs(head, mode)
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: File "/usr/lib64/python2.7/os.py", line 157, in makedirs
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: mkdir(name, mode)
    Aug 21 08:44:07 master.ipa.fc org.freedesktop.FleetCommander[23521]: OSError: [Errno 13] Permission denied: '/home/admin'


In case this error is seen, you have installed ipa-server without ``--mkhomedir`` option.

To solve the issue, please. do:

.. code:: ini

    # For Fedora 28+
    # authselect select sssd with-mkhomedir

    # For older systems which still rely on authconfig
    # authconfig --enablemkhomedir --update


And log into the system with the admin user in order to have its home directory
created:

.. code:: ini

    # ssh -l admin localhost

And now click in ``Retry connection``

NOTE: A patch to give a better debug message for this issue has already been
proposed: https://github.com/fleet-commander/fc-admin/pull/195


Error connecting to IPA server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``Error connecting to IPA server. Check system logs for details.``

.. code:: ini

    Aug 21 09:11:33 master.ipa.fc org.freedesktop.FleetCommander[23521]: FC: [DEBUG] Started session checking
    Aug 21 09:11:33 master.ipa.fc org.freedesktop.FleetCommander[23521]: FC: [DEBUG] Connecting to IPA server
    Aug 21 09:11:34 master.ipa.fc org.freedesktop.FleetCommander[23521]: ipa: INFO: trying https://master.ipa.fc/ipa/session/json
    Aug 21 09:11:34 master.ipa.fc org.freedesktop.FleetCommander[23521]: ipa: INFO: [try 1]: Forwarding 'ping/1' to json server 'https://master.ipa.fc/ipa/session/json'
    Aug 21 09:11:34 master.ipa.fc [22135]: GSSAPI client step 1
    Aug 21 09:11:34 master.ipa.fc [22135]: GSSAPI client step 1
    Aug 21 09:11:34 master.ipa.fc ns-slapd[22623]: GSSAPI server step 1
    Aug 21 09:11:34 master.ipa.fc [22135]: GSSAPI client step 1
    Aug 21 09:11:34 master.ipa.fc org.freedesktop.FleetCommander[23521]: FC: [DEBUG] FreeIPAConnector: Starting sanity check
    Aug 21 09:11:34 master.ipa.fc org.freedesktop.FleetCommander[23521]: FC: [ERROR] FreeIPAConnector: Error connecting to FreeIPA: freeipa-desktop-profile is not installed in FreeIPA server
    Aug 21 09:11:34 master.ipa.fc org.freedesktop.FleetCommander[23521]: FC: [DEBUG] IPA server connection failed: freeipa-desktop-profile is not installed in FreeIPA server
    Aug 21 09:11:34 master.ipa.fc org.freedesktop.FleetCommander[23521]: FC: [DEBUG] Last call time: 1534835493.38
    Aug 21 09:11:34 master.ipa.fc org.freedesktop.FleetCommander[23521]: FC: [DEBUG] Checking running sessions. Time passed: 1.32938504219


In case this error is seen, you have to install ``freeipa-desktop-profile`` plugin.

To solve the issue, please, do:

.. code:: ini

    # For Fedora
    # dnf install freeipa-desktop-profile

    # For EL
    # yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    # yum install freeipa-desktop-profile


And now click in ``Retry connection``

In case the problem still persists, please, do:

.. code:: ini

    # su -l admin

    Then on ipa console, check if the admin user has access to the api commands

    [admin@master ~]$ ipa console
    (Custom IPA interactive Python console)
    >>> 'deskprofileconfig_show' in api.Command
    False


In this case, the user's cache must be wiped out and it can be done either by:
 * Adding ``force_schema_check = True`` to ``/etc/ipa/fleetcommander.conf``
   file under the ``[global]`` section or;
 * By just calling ``rm -rf ~/.cache/ipa/`` as the admin user.

Once it's done, check, again, if the admin user has access to the api commands:

.. code:: ini

    [admin@master ~]$ ipa console
    (Custom IPA interactive Python console)
    >>> 'deskprofileconfig_show' in api.Command
    True


And now, again, click in ``Retry connection``

NOTE: A patch to prevent this issue has already been merged:
https://github.com/abbra/freeipa-desktop-profile/pull/9


Error getting domain list
~~~~~~~~~~~~~~~~~~~~~~~~~

This error may happen when trying to connect to a Live Session.

.. code:: ini

    Aug 21 12:46:41 master.ipa.fc sshd[7846]: pam_unix(sshd:session): session opened for user user by (uid=0)
    Aug 21 12:46:41 master.ipa.fc sshd[7852]: Received disconnect from 192.168.0.114 port 52348:11: disconnected by user
    Aug 21 12:46:41 master.ipa.fc sshd[7852]: Disconnected from 192.168.0.114 port 52348
    Aug 21 12:46:41 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [DEBUG] Getting domain try 2: Error connecting to host: Error executing remote command: bash: virsh: command not found
    Aug 21 12:46:41 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [ERROR] Error retrieving domains Error connecting to host: Error executing remote command: bash: virsh: command not found
    Aug 21 12:46:41 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [DEBUG] Last call time: 1534848400.52
    Aug 21 12:46:41 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [DEBUG] Checking running sessions. Time passed: 0.843245983124
    Aug 21 12:46:41 master.ipa.fc sshd[7846]: pam_unix(sshd:session): session closed for user user


As said in the debu logs, ``virsh`` is not present in the machine. In order to
solve this, please, do:

.. code:: ini

    # For Fedora
    # dnf install libvirt-client

    # For EL
    # yum install libvirt-client


And add the user to be used to the libvirt groups by doing:

.. code:: ini

    # usermod --append --groups libvirt <user>


After following the instructions, please, retry to use the Live Session.


Error starting session
~~~~~~~~~~~~~~~~~~~~~~

This error may happen when connecting to the VM to be used for the Live
Session.

.. code:: ini

    Aug 21 12:55:30 master.ipa.fc libvirtd[8345]: 2018-08-21 10:55:30.602+0000: 8349: error : qemuProcessStartValidateVideo:4692 : unsupported configuration: this QEMU does not support 'virtio' video device
    Aug 21 12:55:30 master.ipa.fc org.freedesktop.FleetCommander[3802]: libvirt: QEMU Driver error : unsupported configuration: this QEMU does not support 'virtio' video device
    Aug 21 12:55:30 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [ERROR] unsupported configuration: this QEMU does not support 'virtio' video device
    Aug 21 12:55:30 master.ipa.fc sshd[9449]: Received disconnect from 192.168.0.114 port 52946:11: disconnected by user
    Aug 21 12:55:30 master.ipa.fc sshd[9449]: Disconnected from 192.168.0.114 port 52946
    Aug 21 12:55:30 master.ipa.fc sshd[9443]: pam_unix(sshd:session): session closed for user user
    Aug 21 12:55:30 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [DEBUG] Last call time: 1534848929.73
    Aug 21 12:55:30 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [DEBUG] Checking running sessions. Time passed: 19.4876799583
    Aug 21 12:55:30 master.ipa.fc systemd-logind[796]: Removed session 93.


From the first line of the log message: "this QEMU does not support 'virtio'
video device". However, 'virtio' is not stricitly needed in this case.

A quick dirty hack that could be applied till
https://github.com/fleet-commander/fc-admin/pull/194 lands in your distro is:

.. code:: ini

    # Edit /usr/share/fleet-commander-admin/python/fleetcommander/libvirtcontroller.py
    # Search for the following lines:

    ...
        video = devs.find('video')
        model = video.find('model')
        if model is not None:
            video.remove(model)
        model = ET.SubElement(video, 'model')
        model.set('heads', '1')
        model.set('primary', 'yes')
        model.set('type', 'virtio')
    ...

    # And change 'virtio' to 'qxl'


NOTE: This problem has only been seen when using CentOS7 as a host machine.


SSSD troubleshooting
--------------------

All the issues that would point to SSSD should come from the following
question:

* Why the profile was not applied to my machine?

And those are the steps you should take in order to figure out the answer:

* Check that your user and machine are part of the users, groups, hosts and
  hostgroups the profile should be applied to. If not, then it's not a bug;

* Check if ``/var/lib/sss/deskprofile/<domain>/<username>/<profile>`` has
  been created. If yes, you're dealing with a problem with the communication
  between SSSD and fleet-commander-client; otherwise, you have a problem with
  the profile being fetched/stored by SSSD.

In order to cover the troubleshooting of both sessions, the first thing to do
is to set a the domain's debug level to ``0x0040``, like:

.. code:: ini

   [domain/ipa.fc]
   ...
   debug_level = 0x0040
   ...


After the domain's debug level has been increased, SSSD has to be restarted
(``systemctl restart sssd``) and a new attempt to log into the system with the
user can be done.

Then, as part of ``/var/log/sssd/sssd_<domain>.log``, messages containing
``deskprofile`` must be searched.

In case of communication problem between SSSD and fleet-commander-client, a
message like this will be seen:

.. code:: ini

    (Wed Aug 22 11:02:07 2018) [sssd[be[ipa.fc]]] [ipa_pam_session_handler_notify_deskprofile_client_done] Error sending sbus message ...
    (Wed Aug 22 11:02:07 2018) [sssd[be[ipa.fc]]] [ipa_pam_session_handler_save_deskprofile_rules]  ipa_pam_session_handler_notify_deskprofile_client() failed ...

For the cases where the profiles haven't been fetched/stored, messages like
thoses will be seen:

.. code:: ini

    (Wed Aug 22 11:02:04 2018) [sssd[be[ipa.fc]]] [ipa_pam_session_handler_done] Unable to fetch Desktop Profile rules ...

    (Wed Aug 22 11:02:07 2018) [sssd[be[ipa.fc]]] [ipa_pam_session_handler_save_deskprofile_rules] Could not retrieve Desktop Profile rules from the cache
    ...

    (Wed Aug 22 11:02:07 2018) [sssd[be[ipa.fc]]] [ipa_pam_session_handler_save_deskprofile_rules] Failed to save a Desktop Profile Rule to disk ...
    ...


In case anything like those is seen, please, contact open a SSSD bug on
`https://pagure.io/SSSD/sssd/issues`__ with a descriptive name, like:
"Fleet Commander: failed to fetch Desktop Profile rules" and add the
following logs:

* journalctl messages from Fleet Commander

* http's error_log messages with after adding ``[global]\ndebug=True`` to the
  IPA's config file and restarting httpd;

* full logs from SSSD's domain (please, sanitize them before attaching to the
  issue);

Also, a quite nice explanation of the issue is appreciated, something like:

"I have a desktop profile set for this user, which is part of those groups
and works from this host, which is part of this hostgroup.
Here's the info about the user:
...

When the user tries to log into the machine I expect **this** to happen,
however the behaviour I can see is **that**.
..."

Asking for help
---------------

If you did not have any luck with debugging the issue yourself you
can reach us through either:

* `sssd-users <https://fedorahosted.org/mailman/listinfo/sssd-users>`__ mailing list

* `#sssd channel on freenode.net <irc://irc.freenode.net/sssd>`__ IRC.

* `#fleet-commander channel on freenode.net <irc://irc.freenode.net/sssd>`__ IRC.

It would be great if you can also provide all the information that you
have found so far to speed things up. Such as the ones pointed above.
