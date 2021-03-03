Troubleshooting Fleet Commander
###############################

This document contains common issues of Fleet Commander integration with SSSD.
Please, refer to the `Fleet Commander`_ project documentation for general issues
that are not related to the SSSD project. You can also read the
:doc:`../design-pages/pages/fleet_commander_integration` design page to get a
better understanding of the SSSD role and how the integration works under the
hood.

.. _Fleet Commander: https://fleet-commander.org

Fleet command logging
*********************

To enable verbose Fleet Commander's debug logs please set:

.. code-block:: ini
    :caption: /etc/xdg/fleet-commander-admin.conf

    [admin]
    log_level = debug

Use ``journalctl`` command to read the logs.

Common issues with Fleet Commander
**********************************

Can not initialize Fleet Commander
----------------------------------

* **Error**: ``Error during service connection. Check system logs for details.``
* **Logs**:

    .. code-block:: text

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

* **Cause**: You have installed ``ipa-server`` without ``--mkhomedir`` option.
* **Solution**:

  #. Enable ``mkhomedir`` PAM module

     .. code-tabs::

         .. fedora-tab::

             authselect enable-feature with-mkhomedir

         .. rhel-tab::

             authselect enable-feature with-mkhomedir

  #. Log into the system with the ``admin`` user in order to have its home
     directory created

     .. code-block:: bash

         ssh -l admin localhost

  #. And now click on ``Retry connection``

Error connecting to IPA server
------------------------------

* **Error**: ``Error connecting to IPA server. Check system logs for details.``
* **Logs**:

    .. code-block:: text

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

* **Cause**: ``freeipa-desktop-profile`` plugin is not installed
* **Solution**:

  #. Install ``freeipa-desktop-profile``

     .. code-tabs::

         .. fedora-tab::

             dnf install freeipa-desktop-profile

         .. rhel-tab::

             yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
             yum install freeipa-desktop-profile

  #. Click on ``Retry connection``

Unable to get the domain list
-----------------------------

* **Error**: ``Error getting domain list``. This error may happen when
  connecting to a Live Session.
* **Logs**:

    .. code-block:: text

        Aug 21 12:46:41 master.ipa.fc sshd[7846]: pam_unix(sshd:session): session opened for user user by (uid=0)
        Aug 21 12:46:41 master.ipa.fc sshd[7852]: Received disconnect from 192.168.0.114 port 52348:11: disconnected by user
        Aug 21 12:46:41 master.ipa.fc sshd[7852]: Disconnected from 192.168.0.114 port 52348
        Aug 21 12:46:41 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [DEBUG] Getting domain try 2: Error connecting to host: Error executing remote command: bash: virsh: command not found
        Aug 21 12:46:41 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [ERROR] Error retrieving domains Error connecting to host: Error executing remote command: bash: virsh: command not found
        Aug 21 12:46:41 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [DEBUG] Last call time: 1534848400.52
        Aug 21 12:46:41 master.ipa.fc org.freedesktop.FleetCommander[3802]: FC: [DEBUG] Checking running sessions. Time passed: 0.843245983124
        Aug 21 12:46:41 master.ipa.fc sshd[7846]: pam_unix(sshd:session): session closed for user user

* **Cause**: ``virsh`` is not present on the machine
* **Solution**:

  #. Install ``libvirt-client``

     .. code-tabs::

         .. fedora-tab::

             dnf install libvirt-client

         .. rhel-tab::

             yum install libvirt-client

  #. Add the user to the libvirt group

     .. code-block:: bash

         usermod --append --groups libvirt <user>

  #. Retry the Live Session

Why was the profile not applied to my machine
*********************************************

* Check that the profile applies to your user and machine.
* Check if ``/var/lib/sss/deskprofile/<domain>/<username>/<profile>`` exists. If
  yes, then the problem is between SSSD and ``fleet-commander-client``. If no
  then SSSD was not able to download or store the profile correctly.
* Enable SSSD debugging, restart SSSD and try to log in again to get more
  verbose information:

     .. code-block:: ini

         [domain/<domain>]
         ...
         debug_level = 0x3ff0
         ...

* Read the logs at ``/var/log/sssd/sssd_<domain>.log``

  #. The problem is between SSSD and ``fleet-commander-client``

     .. code-block:: sssd-log

         [ipa_pam_session_handler_notify_deskprofile_client_done] Error sending sbus message ...
         [ipa_pam_session_handler_save_deskprofile_rules] ipa_pam_session_handler_notify_deskprofile_client() failed ...

  #. The profile was not correctly stored

     .. code-block:: sssd-log

         [ipa_pam_session_handler_done] Unable to fetch Desktop Profile rules ...
         [ipa_pam_session_handler_save_deskprofile_rules] Could not retrieve Desktop Profile rules from the cache
         ...
         [ipa_pam_session_handler_save_deskprofile_rules] Failed to save a Desktop Profile Rule to disk ...
         ...

Ask for help
************

If you did not have any luck with debugging the issue yourself you can reach us
through multiple channels, see the :doc:`../community` page for more
information. Please, provide us all the information that you have found in
advance.
