SSSD 2.4.2 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

-  Default value of 'user' config option was fixed into accordance with man page, i.e. default is 'root'
-  Example systemd service configs now makes use of CapabilityBoundingSet option as a security hardening measure.

New features
~~~~~~~~~~~~

-  ``pam_sss_gss`` now support authentication indicators to further harden the authentication

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

-  Added ``pam_gssapi_indicators_map`` to configure authentication indicators requirements

Tickets Fixed
-------------

-  `#5385 <https://github.com/SSSD/sssd/issues/5385>`_ - Fedora rawhide mock build is broken
-  `#5406 <https://github.com/SSSD/sssd/issues/5406>`_ - sssd-kcm starts successfully for non existent socket_path
-  `#5482 <https://github.com/SSSD/sssd/issues/5482>`_ - Add support to verify authentication indicators in pam_sss_gss
-  `#5499 <https://github.com/SSSD/sssd/issues/5499>`_ - [pam_sss] AD users cannot login to IPA clients

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.4.1..2.4.2

    Alexander Bokovoy (1):
        5ce7ced26  pam_sss_gss: support authentication indicators

    Alexey Tikhonov (6):
        d547a2dc1  BUILD: fixes gpo_child linking issue
        b1f4dc82a  SPEC: don't hard require python3-sssdconfig in a meta package
        a53c214b7  spec file: don't enable implicit files domain on RHEL
        9aaa0e51d  systemd configs: limit process capabilities
        ee9dbea1e  monitor: fixed default value of 'user' config option
        fd7ce7b3d  systemd configs: add CAP_DAC_OVERRIDE in case certain case

    Pavel Březina (7):
        4c47f1daf  scripts: change release tag from sssd-x_y_z to x.y.z
        db51ce55f  Update version in version.m4 to track the next release
        b100efbfa  sudo: do not search by low usn value to improve performance
        75343ff57  ldap: fix modifytimestamp debugging leftovers
        135d843f6  spec: remove setuid bit from child helpers if sssd user is root
        50e3221da  responder: fix warning in activate_unix_sockets
        709bfc4a0  pot: update pot files

    Stanislav Levin (1):
        5c9143e9a  pam_sss: Don't fail on deskprofiles phase for AD users

    ikerexxe (1):
        f890fc4b5  RESPONDER: check that configured sockets match
