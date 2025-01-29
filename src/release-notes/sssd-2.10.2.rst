SSSD 2.10.2 Release Notes
=========================

Highlights
----------

This release fixes a number of minor issues in the spec and services files,
affecting mainly rpm-ostree based systems.

Important fixes
~~~~~~~~~~~~~~~

* If the ssh responder is not running, ``sss_ssh_knownhosts`` will not fail (but
  it will not return the keys).

* A wrong path to a pid file in SSSD logrotate configuration snippet was
  corrected.

* SSSD is now capable of handling multiple services associated with the same
  port.

* ``sssd_pam``, being a privileged binary, now clears the environment and
  doesn't allow configuration of the ``PR_SET_DUMPABLE`` flag as a precaution.


Tickets Fixed
-------------

* `#7746 <https://github.com/SSSD/sssd/issues/7746>`__ - krb5_child couldn't parse pkcs11 objects if token label contains semicolon
* `#7781 <https://github.com/SSSD/sssd/issues/7781>`__ - New ``chown`` likely not working as expected.



Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.10.1..2.10.2

    Alejandro López (1):
        4880e00a5  SSH: sss_ssh_knownhost must succeed if the responder is stopped

    Alexey Tikhonov (13):
        00aadc78e  UTILS: reduce log level if `sss_krb5_touch_config()` fails
        be612e6a4  SPEC: conf files are owned by 'root:sssd'
        97629f36b  SYSTEMD SERVICE: use "--no-dereference" for 'chown'
        fa26915e6  SYSTEMD: traverse 'sssdconfdir' symlink while chown-ing
        a0ab704c9  SYSTEMD: fix missing 'g+x' on /etc/sssd and subdirs
        12bd58515  LOGROTATE: fix path to pid file
        6d63a0514  PAM: don't set PR_SET_DUMPABLE
        5b4f48e7c  SELINUX_CHILD: fail immediately if set-id fails
        00074501d  SELINUX_CHILD: 'ret' argument of `prepare_response()` is always 0
        033d8c452  SELINUX: get rid of response as it was redundant and
        6fc4cc3ee  Clear env of privileged 'sssd_pam' as a security hardening measure.
        a1dba9c9e  Don't clear 'sssd_pam' env when built for intg-tests
        e8bba7e02  certmap: remove stray export declaration

    Dan Lavu (3):
        5bac96bc4  tests: moved ad specific authentication test and created test_ad.py
        7fa059116  tests: adding override_homedir test
        3d432188b  tests: test_kcm.py fixing confusing error message

    Dominika Borges (1):
        4529ed413  doc: improve description of ldap_disable_range_retrieval

    Evgeny Sinelnikov (1):
        da8d010c1  cert util: add support build with OpenSSL older than 3.0

    Iker Pedrosa (2):
        44ff5c8d3  tests: add feature presence automation
        c44bcb78c  tests: improve feature presence automation

    Justin Stephenson (5):
        bd7f41895  DEBUG: lower missing passkey data debug level
        f7258c4c8  tests: have analyzer request child parse child log
        ab95df5f9  ci: Remove internal covscan workflow
        31160a38a  ci: Add workflow for 'coverity' label in PRs
        4bcfeba9a  CI: Fix coverity label multiline conditional

    Krzesimir Nowak (1):
        8bac60ad3  Assume that callbacks are not broken in OpenLDAP when cross-compiling

    Pavel Březina (2):
        caa4be407  po: update pot files
        9a5c416c9  Release sssd-2.10.2

    SATOH Fumiyasu (1):
        33e3a2e12  SPEC: sssd.conf file is owned by 'root:sssd' and mode is 0640

    Samuel Cabrero (5):
        143dd27ee  CACHE_REQ: always return the first result in service by port lookups
        cb03f09c3  SYSDB: Use temporary memory context to allocate the results
        ea4b933b8  SYSDB: Allow multiple services associated to the same port
        a84e2f49b  INTG-TESTS: Add Tests for service by name and by port lookups
        961742cbd  IFP: Restrict destination

    Sumit Bose (1):
        8d7fecd26  krb5_child: ignore Smartcard identifiers with a ':'

    aborah-sudo (5):
        dd5a1a276  Tests: Fix the permission of snippet file
        2efbaa4d2  Tests: SSSD fails to store users if any of the requested attribute is empty
        cf2733b9c  Tests: Fix python black formation error
        bdeae923c  Tests: ldap search base does not fully limit the Netgroup search base
        ae2e2e90d  Tests: Test trasformation for netgroup with generic provider

    fossdd (1):
        6098cfcdc  Fix missing include sys/types.h

