SSSD 2.9.3 Release Notes
========================

Highlights
----------

SSSD 2.9 branch is now in long-term maintenance (LTM) phase.

General information
~~~~~~~~~~~~~~~~~~~

* The proxy provider is now able to handle certificate mapping and matching rules and users handled by the proxy provider can be configured for local Smartcard authentication. Besides the mapping rule local Smartcard authentication should be enabled with the 'local_auth_policy' option in the backend and with 'pam_cert_auth' in the PAM responder.

Important fixes
~~~~~~~~~~~~~~~

Passkey doesn't fail when using FreeIPA server-side authentication and require-user-verification=false.

New features
~~~~~~~~~~~~

* When adding a new credential to KCM and the user has already reached their limit, the oldest expired credential will be removed to free some space. If no expired credential is found to be removed, the operation will fail as it happened in the previous versions.

Tickets Fixed
-------------

* `#6667 <https://github.com/SSSD/sssd/issues/6667>`__ - KCM: provide mechanism to purge expired credentials
* `#6681 <https://github.com/SSSD/sssd/issues/6681>`__ - Default hardening - id_provider channel defaults unencrypted with starttls
* `#6920 <https://github.com/SSSD/sssd/issues/6920>`__ - sssd-sudo missing debug statement in its .service file
* `#6942 <https://github.com/SSSD/sssd/issues/6942>`__ - SSSD goes offline during initgroups of trusted user if a group is missing SID
* `#6956 <https://github.com/SSSD/sssd/issues/6956>`__ - Incorrect handling of reverse IPv6 update results in update failure
* `#7009 <https://github.com/SSSD/sssd/issues/7009>`__ - sssd-2.9.2-1.el8 breaks smart card authentication

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.2..2.9.3

    Alejandro López (3):
        c6ea805ee  NSS: Replace notification message by a less scary one
        1fa72109e  KCM: Remove the oldest expired credential if no more space.
        834b53697  KCM: Display in the log the limit as set by the user

    Alexey Tikhonov (4):
        b86d301c1  SUDO service: ${DEBUG_LOGGER} was missed for 'sudo'
        0705145c6  MC: a couple of additions to 'recover from invalid memory cache size' patch
        5e35a695b  configure: use 'LDB_CFLAGS'
        ef5370e96  SSS_CLIENT: replace `__thread` with `pthread_*specific()`

    Dan Lavu (4):
        674ee267c  tests: adding group and importance markers
        aa3616b34  Updating ad_multihost test
        c866b5316  Updating ad_multihost test
        3fd19c802  Adding test case for bz2167728

    Iker Pedrosa (3):
        a31113389  passkey: omit user-verification
        9c4f7281d  man: clarify user credentials for `cache_credentials`
        fa33c997c  CI: build passkey for centos-9

    Jakub Vavra (8):
        f1a11708a  Tests: Print krb5.conf when joining realm.
        cb1c59c7a  Tests: Split package installation to different transactions.
        f117da5a0  Tests: Handle dns with systemd resolved.
        ec8f0269c  tests: Add missing pytest marker config.
        6218b40fb  Tests: Skip tests unstable on other archs and tweak realm join.
        c799b75da  Tests: Fix AD param sasl tests.
        c99f684c7  Tests: adjoin in test_00015_authselect_cannot_validate_its_own_files
        a9498b12b  Tests: Fix autofs cleanups

    Justin Stephenson (5):
        02bd1d7e7  Passkey: Allow kerberos preauth for "false" UV
        5469de2fa  tests: Improve read write pipe child tests
        004796939  util: Realloc buffer size for atomic safe read
        ede391c26  Passkey: Increase conv message size for prompting
        793284ab9  man: Improve LDAP security wording

    Madhuri Upadhye (1):
        df709da52  tests: add passkey tests for sssctl and non-kerberos authentication

    Patrik Rosecky (7):
        0a429107a  tests: convert multihost/basic/test_basic to test_kcm and test_authentication
        583daff7d  Tests: converted alltests/test_pasword_policy.py to tests/test_ldap.py
        b8b2bfaf1  Tests: alltest/test_sssctl_local.py converted to system/tests/sssctl.py
        7a53c7ac7  Tests: multihost/basic/test_files converted
        a9617cff8  Tests:alltests/test_rfc2307.py converted to test_ldap.py
        8d5752f44  Tests: alltests/test_sss_cache.py converted to multihost/test_sssctl.py
        9e7a08a80  TESTS: topology set to KnownTopologyGroup.AnyProvider

    Pavel Březina (7):
        71ca2053b  tests: add sssd_test_framework.markers plugin
        6bba653c6  ci: install latest SSSD code on IPA server
        380eafa5b  intg: return status code for calls requiring it in fake nss module
        e217fa826  ci: get frozen Fedora releases in the matrix
        5a546c84e  ipa: do not go offline if group does not have SID
        d380342b4  pot: update pot files
        ee2e0cd9b  Release sssd-2.9.3

    Scott Poore (1):
        3b939ce9c  Tests: add follow-symlinks to sed for nsswitch

    Sumit Bose (10):
        a4de653f5  ci: remove unused clang-analyzer from dependencies
        7d73571ed  utils: enable talloc null tracking
        42face74e  proxy: add support for certificate mapping rules
        351aab979  intg: add NSS module for nss-wrapper support
        d36491435  intg: replace files with proxy provider in PAM responder test
        25a913eae  confdb: add new option for confdb_certmap_to_sysdb()
        7668ed6eb  intg: use file and proxy provider in PAM responder test
        04b6a22b3  intg: add proxy auth with fallback test
        2bbc87540  ipa: reduce log level of some HBAC log messages
        3da54579e  PAM: fix Smartcard offline authentication

    Tomas Halman (1):
        a48c7445d  dyndns: PTR record updates separately

    Weblate (1):
        2eae8ab44  po: update translations

    aborah (2):
        45fbcd93c  Tests: Enabling proxy_fast_alias shows "ldb_modify failed: [Invalid attribute syntax]" for id lookups.
        7e45b32a3  Tests: Port rootdse test suit to new test framework.

    dependabot[bot] (4):
        9ebaee777  build(deps): bump DamianReeves/write-file-action
        d154f72d0  build(deps): bump actions/checkout from 3 to 4
        66d115cc8  build(deps): bump vapier/coverity-scan-action from 1.2.0 to 1.7.0
        155584ee2  build(deps): bump linuxdeepin/action-cppcheck

    licunlong (1):
        129ceaed8  cli: caculate the wait_time in milliseconds
