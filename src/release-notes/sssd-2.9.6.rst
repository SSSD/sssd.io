SSSD 2.9.6 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* The DoT for dynamic DNS updates is supported now. It requires new version of
  ``nsupdate`` from BIND 9.19+.

* The option ``default_domain_suffix`` is deprecated. Consider using the more
  flexible ``domain_resolution_order`` instead.

Important fixes
~~~~~~~~~~~~~~~

* When the ``DP_OPT_DYNDNS_REFRESH_OFFSET`` enumerator was created, the
  associated ``struct dp_option`` was not. Because these structures are part of
  an array and the enumerator is used as the index, the wrong structure would be
  accessed when trying to use this index. This problem was fixed by creating the
  missing structure.


Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* The ``dyndns_server`` option is extended so it can be in form of URI
  (``dns+tls://1.2.3.4:853#servername``). New set of options
  ``dyndns_dot_cacert``, ``dyndns_dot_cert`` and ``dyndns_dot_key`` allows to
  configure DNS-over-TLS communication.

* Added ``exop_force`` value for configuration option ``ldap_pwmodify_mode``.
  This can be used to force a password change even if no grace logins are left.
  Depending on the configuration of the LDAP server it might be expected that
  the password change will fail.


Tickets Fixed
-------------

* `#5418 <https://github.com/SSSD/sssd/issues/5418>`__ - Problem with transition user's credentials through pam-stack
* `#5861 <https://github.com/SSSD/sssd/issues/5861>`__ - openssl3 deprecated some functions
* `#6922 <https://github.com/SSSD/sssd/issues/6922>`__ - ``CURLOPT_PROTOCOLS`` is deprecated
* `#7007 <https://github.com/SSSD/sssd/issues/7007>`__ - pamstack_oldauthtok is not used during prelim check
* `#7375 <https://github.com/SSSD/sssd/issues/7375>`__ - [RFE] Add option to configure timeout to reconnect to primary servers
* `#7404 <https://github.com/SSSD/sssd/issues/7404>`__ - CRL option soft_crl doesn't check CRL at all, if nextupdate date has passed
* `#7411 <https://github.com/SSSD/sssd/issues/7411>`__ - GPO application fails with more > 1host in security filter
* `#7451 <https://github.com/SSSD/sssd/issues/7451>`__ - sssd is skipping GPO evaluation with auto_private_groups
* `#7456 <https://github.com/SSSD/sssd/issues/7456>`__ - 2FA is being enforced after upgrading 2.9.1->2.9.4
* `#7510 <https://github.com/SSSD/sssd/issues/7510>`__ - No way to configure ``debug_backtrace_enabled`` for ``ldap_/krb_child``
* `#7532 <https://github.com/SSSD/sssd/issues/7532>`__ - EL9/CentOS Stream 9 lost offline smart card authentication
* `#7590 <https://github.com/SSSD/sssd/issues/7590>`__ - GPO access control might fail if ldap_user_name is set
* `#7612 <https://github.com/SSSD/sssd/issues/7612>`__ - sssd does not lookup user gid's at reboot without \*.ldb files
* `#7642 <https://github.com/SSSD/sssd/issues/7642>`__ - AD machine account password renewal via adcli doesn't honor ad_use_ldaps setting
* `#7671 <https://github.com/SSSD/sssd/issues/7671>`__ - Mismatch between input and parsed domain name when default_domain_suffix is set.
* `#7715 <https://github.com/SSSD/sssd/issues/7715>`__ - sssd backend process segfaults when krb5.conf is invalid


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.5..2.9.6

    Alejandro López (2):
        dafe48341  OPTS: Add the option for DP_OPT_DYNDNS_REFRESH_OFFSET
        5411fa745  TESTS: Also test default_dyndns_opts

    Alexey Tikhonov (16):
        abce3bf3a  SSH: sanity check to please coverity
        c0fc941ce  CLIENT:idmap: fix coverity warning
        9992ac67e  CI: remove http-parser dependency
        9af9ca123  DEBUG: added missing newline
        09b23e788  TS_CACHE: never try to upgrade timestamps cache
        13e3d0390  SYSDB: remove index on `dataExpireTimestamp`
        5ef0bc477  sssd.supp: remove outdated entries
        aa29ca7f5  sssd.supp: suppress invalid read in dlopen
        b48f7356f  SPEC: add new systemtap-sdt-dtrace to build deps
        3accd5b4b  CI: capture full 'config.log' from ./configure
        071b93213  Unit tests: use ".invalid" domain name for OCSP responder
        06920b480  DEBUG: add 'debug_backtrace_enable' getter
        344171410  UTILS: simplify / comment a bit better
        c259d46a0  DEBUG: propagate debug_backtrace_enabled to child processes
        d621c2287  MAN: mistypes fixes
        d197da975  CLIENT: don't try to lookup `getservbyport(0, ...)`

    Christopher Byrne (1):
        31a5c70ff  cfg_rules.ini: Add missing ldap_user_passkey entry.

    Dan Lavu (29):
        50d97644e  tests: updating gpo auto private group test case
        c70abfb5c  tests: housekeeping - test_kcm.py
        9debaf53d  tests: fixing gpo test case
        950e52a7a  tests: housekeeping - test_gpo.py
        cc1c0a194  tests: test_autofs.py - adding error messages
        424235675  tests: updating makefile.am to include tests
        c9fc8ca90  tests: fixing auto_private_group test cases
        041a3657f  test: housekeeping - sudo
        5ff80cf34  tests: housekeeping, test_proxy.py
        998d1839b  tests: housekeeping, test_files.py
        5e1a62dd1  tests: housekeeping - test_trusts.py -> test_ipa_trusts.py
        e9a802985  tests: housekeeping - test_cache.py
        b98dab5c9  tests: housekeeping - test_failover.py
        1b6dce3c9  tests: housekeeping, test_ldap.py
        60651df12  tests: housekeeping - schema
        762288309  tests: housekeeping, test_authenticaiton.py
        52a374f4d  tests: housekeeping - identity
        08b3f567b  tests: failover docstrong
        61408c8e4  tests: updating gpo test case to test all auto_private_group values
        5d8b43580  tests: housekeeping - sss_override
        6bb9e7c3e  tests: remove multihost basic tests
        838ee2f83  tests: removing intg/test_confdb.py
        01dea8782  tests: removing intg/test_files_ops.py
        86a5c09e4  tests: improving gpo tests to be run against ad and samba
        5a6093f3e  tests: housekeeping - test_logging.py
        1583e1bfa  tests: rm intg/test_sss_cache.py
        2df6ff98f  tests: adding gpo customer test scenario to use the ldap attribute name
        99c65ad86  tests: backport, removing intg/ts_cache.py
        120383035  tests: adding system/tests/readme.rst as a quick primer

    Dominika Borges (2):
        452b5df33  doc: improve `failover_primary_timeout` option
        77f1374bb  doc: improve ad_access_filter option

    Evgeny Sinelnikov (1):
        710a99397  cert util: add support build with OpenSSL older than 3.0

    Iker Pedrosa (1):
        ee8de7e40  spec: change passkey_child owner

    Jakub Vávra (18):
        717cc6e99  Tests: Update password change expect to work
        f6d45be82  Tests: Add extra output in package_mgmt when operation fails.
        fa89b1d8e  Tests: Move logging settings change to test start
        d76b1e555  Tests: Update ad multiforest and multidomain suites.
        6d6e0f441  Tests: Update code handling journald.conf
        409198e6d  tests: Drop already ported tests from alltest
        1bd7ca82d  tests: Add loading kernel module sch_netem for tc tool
        57b7f8bb6  Tests: Drop tests converted to system from basic to save resources in prci
        55b9a281d  Tests: Handle missing ldap_child.log in AD parameters
        1c92d8acf  tests: Add fallback log directory for custom_log.py
        9ace698a7  tests: change parameters for pytest.mark.flaky to max_runs
        edd4beb23  tests: Update code handling systemd-resolved for F42.
        aa94afc72  tests: Addd sssd.log when sssd does not start.
        1d7a6eba3  tests: Update ldap test to use journal utility.
        5d382b4f3  tests: Unify packages available on client for ipa suites
        5f617f2c9  ci: Remove Fedora 41 and 42 from matrix for sssd-2-9.
        d75b666b8  ci: Exclude fedora-38, fedora-41, fedora-42, fedora-rawhide, c8s and c10s from build of sssd-2-9
        316f911c7  Tests: Update sst to rhel-sst-idm-sssd for polarion.

    Jan Engelhardt (3):
        5de9da1ce  build: unbreak detection for x400Address
        0e537e7f8  build: stop overriding CFLAGS
        eb3720286  build: fix spellos in configure.ac

    Justin Stephenson (2):
        8b35d7066  sdap: Log hint for ignore unreadable references
        811269221  ipa: Check sudo command threshold correctly

    Kaushik Banerjee (4):
        eda5e2e0b  Tests: Restart systemd-journald instead of stop/start
        11db501e0  Tests: Disable journald rate limiting during alltests pytest session
        b8f2b33c0  Tests: Move journald rate disable to common/fixtures.py
        f2ca67cda  man: Use c_rehash instead of deprecated cacertdir_rehash

    Madhuri Upadhye (2):
        ec50198d7  Passkey: Backport of PR-7331
        fdad5eae8  Tests: housekeeping: Description in passkey tests

    Pavel Březina (14):
        d29e40184  ci: explicitly set which topologies are already provisioned
        50a407289  ci: use python 3.11 for system tests
        5310a54d0  ci: do not collect pytest-mh logs in separate file
        638320a8d  ci: disable show-capture in system tests
        2a50bc1a5  ci deps: do not use -- to denote positional arguments anymore
        f78ec84fa  tests: update the tests to work with latest pytest-mh
        ccb0165ca  tests: use podman instead of ssh to speed up in PR CI
        2b551e98c  tests: stabilize test_sudo__refresh_random_offset
        ab5b65a1f  ci: switch back to ssh connections in system tests
        b6d3e2ca8  tests: add topology marker back to test_ldap__password_change_using_ppolicy
        d18684269  tests: avoid skipif in the system tests for feature detection
        722446564  make_srpm: fallback to tar if git archive fails
        28f6e3153  pot: update pot files
        b52a6a7a7  Release sssd-2.9.6

    Pavel Raiskup (1):
        5a6cd13e1  rpm: drop the --remote argument from git-archive call

    Petr Mikhalicin (1):
        39cbb8df4  pam_sss: fix passthrow of old authtok from another pam modules at PAM_PRELIM_CHECK

    Samuel Cabrero (2):
        2f54a0b3f  BUILD: Fix os detection
        bc83ca89d  TOOLS: Adjust sssctl user-checks default PAM service for SUSE

    Scott Poore (1):
        cd40695a0  man: sssd.conf update defaults for certmap maprule

    Sumit Bose (19):
        723a30b45  ad: use right memory context in GPO code
        d234cf5d6  sysdb: do not fail to add non-posix user to MPG domain
        aa3fbe8cb  p11_child: enhance 'soft_crl' option
        ef375cdd6  krb5_child: do not try passwords with OTP
        7e76396a8  pam_sss: add missing optional 2nd factor handling
        70ea95046  man: add details for ad_access_filter
        cdb9d69f4  oidc_child: use CURLOPT_PROTOCOLS_STR if available
        dfcfa5157  cert util: replace deprecated OpenSSL calls
        b4c496856  pam: only set SYSDB_LOCAL_SMARTCARD_AUTH to 'true' but never to 'false'.
        321ca19ae  sdap: allow to provide user_map when looking up group memberships
        2c233636c  ad: use default user_map when looking of host groups for GPO
        e3a3f44c4  ldap: add 'exop_force' value for ldap_pwmodify_mode
        86e610286  tests: add 'expo_force' tests
        9f9ee2dc4  pam_sss: add some missing cleanup calls.
        421dfee3c  subdomains: check when going online
        d456f136a  ssh: do not use default_domain_suffix
        698a751f2  responders: deprecate default_domain_suffix option
        a34098c54  ldap_child: make sure invalid krb5 context is not used
        c6792b7ca  dyndns: collect nsupdate debug output

    Tomas Halman (2):
        069b86f9c  Missing 'dns_update_per_family' option
        255e7a78e  Add DoT support for DNS updates

    aborah (4):
        9c02c72ef  Tests: Fix the test failures for tier-1-pytest-alltests-tier1-2 for non root configuration
        d495be42c  Tests: Fix RHEL10 failures
        3375448be  Tests: Fix ipa tests for RHEL10
        b80036820  Tests: Fix tier2 tests for RHEL10

    aborah-sudo (2):
        e63784bae  Tests: Test transformation of bash-ldap-id-ldap-auth netgroup
        a0dd53c3b  Tests: Reverse the condition and fail

    dependabot[bot] (1):
        97796f66e  build(deps): bump actions/setup-python from 4 to 5

    santeri3700 (1):
        5e6fd2a05  ad: honor ad_use_ldaps setting with ad_machine_pw_renewal

    shridhargadekar (1):
        c595e729e  Tests: automount segfault fix

    spinningTops (1):
        fe6d806c5  Expose flat_name for use in homedir path
