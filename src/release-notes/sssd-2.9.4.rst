SSSD 2.9.4 Release Notes
========================

Highlights
----------

Important fixes
~~~~~~~~~~~~~~~

* Fixes a crash when PAM passkey processing incorrectly handles non-passkey data.
* A workaround was implemented to handle gracefully misbehaving applications that destroy internal state of SSSD client librarires. A particular example of such application is described in https://github.com/TigerVNC/tigervnc/issues/1709.
* An error when rotating KCM's logs was fixed. When KCM's logs were rotated by logrotate, KCM would still use the old file (renamed sssd_kcm.log.1). Only after KCM was restarted (either manually or automatically) the new log file would be used. This problem is now solved and KCM uses the new file immediately.
* Fixed group membership handling when members are coming from  different forest domains and using ldap token groups is prohibited.
* Files provider was erroneously taking into consideration `local_auth_policy` config option, thus breaking smartcard authentication of local user in setups that didn't explicitly specify this option. This is now fixed.

Tickets Fixed
-------------

* `#5708 <https://github.com/SSSD/sssd/issues/5708>`__ - SSSD incorrectly works with AD GPO during user login
* `#6790 <https://github.com/SSSD/sssd/issues/6790>`__ - gpo_child process terminates with SIGSEGV.
* `#6986 <https://github.com/SSSD/sssd/issues/6986>`__ - The ``sss_nss_mc_destroy_ctx()`` function will close the TCP socket of the daemon process
* `#7014 <https://github.com/SSSD/sssd/issues/7014>`__ - Reduce the amount of memory allocated by KCM and avoid zeroing it when not necessary
* `#7061 <https://github.com/SSSD/sssd/issues/7061>`__ - sssd_pam segfaults during password-based SSH-login
* `#7072 <https://github.com/SSSD/sssd/issues/7072>`__ - sssd_kcm "leaks" around 86MiB of memory per day
* `#7084 <https://github.com/SSSD/sssd/issues/7084>`__ - Invalid handling groups from child domain
* `#7094 <https://github.com/SSSD/sssd/issues/7094>`__ - Incorrect IdM product name in man sssd.conf


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.3..2.9.4

    Alejandro López (9):
        469ddcbf6  LOGROTATE: logrotate should also signal sssd_kcm
        8c8323451  KCM: Replace a hard-coded constant by a macro
        855d04656  KCM: Fixed a wrong check
        14e7d7c03  KCM: Remove unused cc_be_type from struct kcm_ccdb
        3e740a256  KCM: When freeing the client, check that it is not NULL.
        a5c96e290  KCM: sss_iobuf_init_empty() shall not zero memory
        78d0a97de  KCM: Reduce the amount of memory allocated for the packages
        60fde9d55  KCM: Do not zero memory when not need.
        46f4161e8  KCM: Fix a memory "leak"

    Alexey Tikhonov (9):
        f394acee8  SPEC: 'sssd-proxy' requires 'libsss_certmap.so'
        4b4564c38  UTIL: use proper specifier for 'DEBUG_CHAIN_ID_FMT_*'
        1e2af0d15  Don't provide 'uint64_t' as POPT_ARG_LONG.
        6959dc6aa  DP: reduce log level in case a responder asks for unknown domain
        f6faf1231  LOGS: added missing new line
        160738ee8  SSS_CLIENT: MC: in case mem-cache file validation fails,
        a186224d6  SSS_CLIENT: check if mem-cache fd was hijacked
        abb146e14  SSS_CLIENT: check if reponder socket was hijacked
        98d8bedd1  DEBUG: added missing new line

    Andre Boscatto (1):
        033f3db09  man: fix wrong product name

    Dan Lavu (3):
        b536e4b3b  tests: consolidation, refactoring and organizing, renaming of some tests
        cb64d47b2  tests: updating poor assertion in dyndns
        1c5a11fc2  tests: adding background refresh tests to the new framework

    Iker Pedrosa (4):
        ba7b99383  CI: clean configure.sh
        31617400e  CI: clean distro.sh
        52acc3940  CI: clean deps.sh
        776f6e198  CI: upload cwrap logs

    Jakub Vavra (8):
        fd414aae8  Tests: Add a test for bz1900973 kcm delete expired tickets
        e44ad3242  Tests: Add a test for kcm log rotation SSSD-5687
        1cffe5bca  Tests: Fix tokengroups tests.
        9f406d427  Tests: Retry realm join as it is flaky on multiarch setups
        cbd479d76  Tests: Change path to keytabs to reflect whole domain in them
        0ae923834  Tests: Add importance and ticket to multihost
        854edfb00  Tests: Revert change of retun type of realm_join
        5a2256cba  Tests: Add a plugin for a per-test logging

    Justin Stephenson (5):
        f4908728f  passkey: Add krb5 preauthentication prompt support
        4d01e11d4  passkey: Skip processing non-passkey mapping data
        02c183204  Passkey: Fix coverity memory overrun error
        f5e3bb391  Passkey: Fix coverity RESOURCE_LEAK
        51f90318b  Passkey: Fix valgrind error and missing free

    Madhuri Upadhye (2):
        a8928a9ad  tests: add passkey tests for authentication failures
        80d5a34fe  Tests: Add passkey test cases for following scenario

    Patrik Rosecky (6):
        c5d045788  Tests: converted alltests/test_default_debug_level
        2bc72a2b7  Tests: alltests/test_autoprivategroup.py converted to system/test_auto_private_groups.py
        66bd91d50  Tests: alltests/test_ldap_extra_attrs.py converted to system/tests/test_schema.py
        8a78c75ab  Tests: multihost/test_sssctl_analyzer.py converted to system/test_sssctl_analyze.py
        852b9e0c5  Tests: alltests/test_config_validation converted
        bd9cf6f4d  Tests: alltests/test_offline.py converted

    Pavel Březina (7):
        35bcb91b6  ad: do not print backtrace if SSSD domain name is not the same as DNS name
        eabeb3a73  ad: do not print backtrace if SOM is missing in GPO
        d02874beb  tests: adapt to new firewall API
        8bf25b6cd  scripts: sign tarball with sssd project key
        5c224730a  scripts: create checksum file for release tarball
        eecd41831  pot: update pot files
        02d3f214b  Release sssd-2.9.4

    Sumit Bose (8):
        ff520020c  ci: make valgrind suppression more relaxed for test_ipa_subdomains_server
        e03921e4b  nssidmap: fix sss_nss_getgrouplist_timeout() with empty secondary group list
        9a6ff9e7b  pam: fix Smartcard auth with files provider
        be5399c15  sssctl: do not require root for user-checks
        936b82816  LDAP: make groups_by_user_send/recv public
        09dcc73ed  ad: gpo evalute host groups
        dda0f2e0b  sysdb: remove sysdb_computer.[ch]
        f5ce7c1da  sdap: add set_non_posix parameter

    Tomas Halman (2):
        a33931562  Handle child-domain group membership
        05de56d0c  GPO evaluation of primary group

    aborah (1):
        c054fc007  Tests: Fix ipa test for gating.
