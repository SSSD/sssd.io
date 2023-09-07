SSSD 2.9.2 Release Notes
========================

Highlights
----------

SSSD 2.9 branch is now in long-term maintenance (LTM) phase.

General information
~~~~~~~~~~~~~~~~~~~

* ``libkrb5-1.21`` can now be used to build PAC plugin.
* ``sssctl cert-show`` and ``cert-show cert-eval-rule`` can now be run as non-root
  user.

Important fixes
~~~~~~~~~~~~~~~

* SSSD does no longer crash if PIN is introduced but the tactile trigger isn't
  pressed during passkey authentication.
* SSSD can now recover if memory-cache files under ``/var/lib/sss/mc`` where
  truncated while SSSD is running.
* Chaining of identical D-Bus requests that run in parallel to avoid multiple
  backend queries works again.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* New option ``local_auth_policy`` is added to control which offline
  authentication methods will be enabled by SSSD. This option is relevant for
  authentication methods which have online, and offline capability such as
  passkey, and smartcard authentication. The default value ``match`` sets the
  offline methods to their corresponding online value. This enables offline
  authentication when online kerberos pre-authentication such as PKINIT, or
  passkey is supported by the backend, note that online methods will still be
  attempted first. Option value ``only`` can be used to disable online
  authentication entirely, or the value ``enable:method`` to explicitly enable
  specific authentication methods, e.g. ``enable:passkey``.

Tickets Fixed
-------------

* `#5198 <https://github.com/SSSD/sssd/issues/5198>`__ - monatomically should have been monotonically
* `#6733 <https://github.com/SSSD/sssd/issues/6733>`__ - New covscan errors in 'passkey' code
* `#6802 <https://github.com/SSSD/sssd/issues/6802>`__ - sss_certmap_test fail in v2.9.1 on Arch Linux
* `#6803 <https://github.com/SSSD/sssd/issues/6803>`__ - [sssd] SSSD enters failed state after heavy load in the system
* `#6889 <https://github.com/SSSD/sssd/issues/6889>`__ - Crash in ``pam_passkey_auth_done``
* `#6911 <https://github.com/SSSD/sssd/issues/6911>`__ - SBUS chaining is broken for getAccountInfo and other internal D-Bus calls

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.1..2.9.2

    Alexey Tikhonov (20):
        4e7cfe17e  BUILD: Accept krb5 1.21 for building the PAC plugin
        e6fbd1cb4  SPEC: sync with Fedora spec file
        9c9a8dee2  MAN: only mention 'files' provider if its support is built
        e19570ef6  KRB5: avoid another attempt to free 'cc' in 'done:' section if first attempt failed.
        e124370f5  KRB5: use proper function to deallocate mem
        f745621e8  KRB5: avoid FORWARD_NULL
        b9fa1af6e  KRB5: fix memory leak
        2ed6aa8d4  KRB5: fix memory leak
        afbf087d1  KRB5: avoid RESOURCE_LEAK
        996affcf6  KRB5: fixed RESOURCE_LEAK
        4d1283676  LDAP: fixed RESOURCE_LEAK
        f7f9f6e5f  LDAP: fixed leak of `kprinc`
        50e2fd242  UTILS: fixed USE_AFTER_FREE
        d479b28d5  UTILS: swap order of seteuid()/setegid()
        358e6d182  SBUS: warn loudly if bus denies access
        1c417bafc  IFP: add a comment to 'org.freedesktop.sssd.infopipe.service' to avoid potential confusion
        3d22dcad7  PROXY: missing `proxy_resolver_lib_name` isn't an error
        78fba725c  Fix compilation warning ``` ../src/responder/pam/pamsrv_cmd.c: In function ‘pam_reply’: ../src/responder/pam/pamsrv_cmd.c:1188:10: warning: unused variable ‘pk_preauth_done’ [-Wunused-variable] 1188 | bool pk_preauth_done = false; ``` in case SSSD is built without 'passkey' support.
        cb86a5ce9  DP: ENOTSUP isn't a fatal failure for target c-tor
        d935fa6bc  UTILS: include name of the file that failed perform_checks() in the debug log

    Andre Boscatto (1):
        7fbb9a0d4  mans: fix typo in ldap_idmap_autorid_compat

    Dan Lavu (1):
        ee8f50f27  TESTS: Porting sss_override test suite

    François Cami (1):
        4b2dbc2da  Fix typo: found => find

    Iker Pedrosa (4):
        5bd218b44  test: basic tests for ldap_user_extra_attrs
        8c1b5c472  man: clarify passkey PIN prompt
        f79ce5348  passkey: fix two covscan issues
        aba98a49b  passkey: rename function

    Justin Stephenson (12):
        b8b75abeb  Change "non_kerberos" to "local" authentication
        5b575fcb6  Add local auth policy
        16f12efd9  PAM: Fail empty password in passkey fallback
        e57b8e775  Passkey: Warning display for fallback
        ccbeb647c  Makefile: Respect `BUILD_PASSKEY` conditional
        1508225a3  pam: Conditionalize passkey code
        f72763ab9  ipa: Add `BUILD_PASSKEY` conditional for passkey codepath
        d0359db13  pam: Remove unneeded passkey verification call
        19b43cc06  CI: Add Fedora 40+ to install CI scripts
        0919c9217  Proxy: Avoid ldb_modify failed error
        e71a35392  Passkey: Add child timeout handler
        2a3a132c6  Passkey: Conditional fixes

    Madhuri Upadhye (4):
        89ff25496  Tests: Minor fix in test_adtrust
        752e0026f  Test: Check case-insensitive while checking with group lookup for a overrideuser
        e26215d66  Tests: Package download
        e8bd99ef9  Tests: Add package for IPA tests

    Patrik Rosecky (6):
        c26b6b5ad  Tests: converted multihost/test_config.py
        9cecdc1bd  Tests: convert intg/test_memory_cache.py to system tests
        fe6be47d9  tests: multihost/basic/sssctl_config_check.py converted
        be42e37b4  Tests: converted intg/test_memory_cache to test_id
        833528496  tests: converted multihost/basic/test_ldap.py
        e2cb4d555  Tests: sssctl_config_check: test for incorrectly set value

    Pavel Březina (16):
        84e0aac45  ci: move to new centos8 buildroot repository url
        2f4a3fa89  ci: run workflows on sssd-2-9
        fd80b421c  tests: add pytest-importance plugin to system tests
        bb46f3176  tests: add pytest-output plugin to system tests
        b9d3ad106  tests: add requirements to system tests
        cc99fdd83  tests: drop tier from system tests
        df727cbb3  tests: fix doctring in test_config__add_remove_section
        71876d6c8  ci: generate polarion xmls from system tests
        13373ea3c  ci: run system test in collect only mode first
        3734714f8  tests: fix doctring in test_memory_cache__invalidate_group_after_stop
        0b5d3abd8  readme: remove github actions badges
        9c4ac1bdd  mc: recover from invalid memory cache size
        45ed619e3  sss_iface: do not add cli_id to chain key
        c84689d7c  pot: update pot files
        a62efb76e  tests: include passkey test code only if passkey is built
        644cd599f  Release sssd-2.9.2

    Shridhar Gadekar (1):
        b8ff5f1c9  Test: gating sssd after crash

    Sumit Bose (5):
        f16e57083  watchdog: add arm_watchdog() and disarm_watchdog() calls
        27987c791  sbus: arm watchdog for sbus_connect_init_send()
        15d7d34b2  sssct: allow cert-show and cert-eval-rule as non-root
        11afa7a6e  certmap: fix partial string comparison
        aedef959a  test: fix linking issue

    Weblate (1):
        9d6ab77c2  po: update translations

    aborah (11):
        a87139894  Tests: Fix alltest tier1_3 tests with new ssh module
        7eef9162d  Tests: Fix IPA tire1_2 tests
        e57414475  Tests: Update test_ldap_password_policy.py::test_maxage as per the new sssd change
        140692c1d  Tests: Fix test_0002_bz1928648 with new ssh module
        a1e773df0  Tests: Update tier1 test cases with new ssh module
        ddfc5e52b  Tests: Backport of https://github.com/SSSD/sssd/pull/6818
        7a6358294  Tests: Fix test_0008_1636002
        d8c18e114  Tests: Fix test_maxage
        65abf0579  Tests: Fix KCM::test_client_timeout
        0b9bc877b  Tests: Update sssh module for tier 1_3, 1_4 and 2
        473e2b4c0  Tests: Add sleep time to test_bz785908

    wangcheng (1):
        d08af4bd6  IPA: Change sysdb_attrs_add_val to sysdb_attrs_add_val_safe in debug output
