SSSD 2.9.8 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* After startup SSSD already creates a Kerberos configuration snippet typically in /var/lib/sss/pubconf/krb5.include.d/localauth_plugin if the AD or IPA providers are used. This enables SSSD's localauth plugin. Starting with this release the an2ln plugin is disabled in the configuration snippet as well. If this file or its content are included in the Kerberos configuration it will fix CVE-2025-11561.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* An option `ipa_enable_dns_sites`, that never worked due to missing server side implementation, was removed.
* The default value of session_provider option was changed to none (i.e. disabled) no matter what id_provider used. Previously session_provider was enabled by default for id_provider = ipa case. The primary tool it was intended to support, “Fleet Commander,” has become obsolete.
* The option `ipa_subid_ranges_search_base` was deprecated in favor of `ldap_subid_ranges_search_base`.

Tickets Fixed
-------------

* `#7274 <https://github.com/SSSD/sssd/issues/7274>`__ - Clarify root permissions for KCM
* `#7606 <https://github.com/SSSD/sssd/issues/7606>`__ - Deprecated code used in 'sss_client/pam_sss.c'
* `#7921 <https://github.com/SSSD/sssd/issues/7921>`__ - AD user in external group is not cleared when expiring the cache
* `#7967 <https://github.com/SSSD/sssd/issues/7967>`__ - sssd client nss coredump
* `#7968 <https://github.com/SSSD/sssd/issues/7968>`__ - cache_credentials = true not working in sssd master
* `#7981 <https://github.com/SSSD/sssd/issues/7981>`__ - invalid memcache_delete_entry  errors  cause   in excess of 150 MB of /var/log/sssd/sss_nss.log entries per day.
* `#8021 <https://github.com/SSSD/sssd/issues/8021>`__ - potentially dangerous id mapping between local and domain users
* `#8022 <https://github.com/SSSD/sssd/issues/8022>`__ - sssd-idp is available but not functional on Fedora 42
* `#8030 <https://github.com/SSSD/sssd/issues/8030>`__ - Support subuid with generic LDAP provider
* `#8059 <https://github.com/SSSD/sssd/issues/8059>`__ - IPA idoverride and auto private groups - behavior change with the copr repo @sssd/nightly
* `#8062 <https://github.com/SSSD/sssd/issues/8062>`__ - Drop Fedora 40 from sssd-2-9 ci testing
* `#8089 <https://github.com/SSSD/sssd/issues/8089>`__ - Including innapropriate IPv6 addresses in dyndns_update
* `#8108 <https://github.com/SSSD/sssd/issues/8108>`__ - After I log in offline with a cached password hash, sssd stays offline forever because my account requires MFA
* `#8194 <https://github.com/SSSD/sssd/issues/8194>`__ - sss_nss: hang when looking up a group with stale cache entry and a LDAP provider
* `#8300 <https://github.com/SSSD/sssd/issues/8300>`__ - SSSD checks PAC from MIT Kerberos and fails

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.7..2.9.8

    Alejandro López (1):
        5a8d15a57  MAN: Make disable_netlink in `man sssd.conf` conditional

    Alexey Tikhonov (34):
        db774e4ed  CI: drop "missingInclude" from cppcheck
        677fb30a4  MAN: remove mention of a 'local domain'.
        9f6a8f7df  UTIL: add a helper to print libldap diagnostics
        f84aa6311  LDAP: debug fail of ldap_set_option(LDAP_OPT_X_SASL_NOCANON)
        95af0a155  Replaces usage of 'sss_ldap_get_diagnostic_msg()'
        547719a60  UTILS: removed ununsed 'sss_ldap_get_diagnostic_msg()`
        be42c950c  RESPONDER: skip mem-cache invalidation
        f730a9287  'gemini-code-assist' config
        5f1015ca9  SSS_CLIENT:MC: simplify logic and
        3934c081a  KCM: corrected debug messages
        e6c4125ca  KCM: verbosity
        aabe28762  KCM: don't trigger backtrace if 'uuid_by_name' fails
        9bbe3dc8f  CLIENT: fix thread unsafe access to autofs struct.
        ef5949701  gpo_child: don't include 'util/signal.c'
        87c9ad335  RESOLV: supress deprecation warnings
        b530fa6f0  CLIENT:PAM: replace deprecated `_pam_overwrite`
        1c4c6b508  SPEC: require reasonably up to date 'libldb' version
        759560c2f  CONTRIB:fedconfig: enable '--with-subid'
        cf6e764a5  MAN: fix missing `with_subid` condition
        1c78f630c  SUBID:IPA: correct OC
        f55e29845  SUBID: deprecate `ipa_subid_ranges_search_base`
        93b7daf02  LDAP: add subid ranges support
        301d51533  SUBID: don't require search bases to be set in advance
        aa0d46c52  man: document subid LDAP attributes
        db5eaf4b3  DEBUG: lower debug level of several messages
        3d4ec50ad  SUBID: resolve owner DN instead of guessing
        42d2e2123  SUBID: sanitize range owner dn
        6d41e9277  SUBID: trusted subdomains aren't currently supported
        8fa2233fc  Add 'libsubid-dev' to deps list on Debian
        35519ca11  CONFIG: disable 'session_provider' by default
        f6d671524  IPA: remove 'ipa_enable_dns_sites' option
        1e858ce73  KCM: root can't access arbitrary KCM cache
        d669556cd  SBUS: increase SBUS_MESSAGE_TIMEOUT to 5 mins
        9c25275a7  RESPONDER: fixed an issue with 'client_idle_timer'

    André Boscatto (2):
        4a3157b5c  TESTS: Add tests to cover access control access_filter (AD/LDAP)
        e1979acfb  tests: Adding nested group test case for simple access control

    Dan Lavu (6):
        5f8be1180  adding pytest markers to help keep track of transformation status
        0d7f66e0c  tests: skipping simple access control tests that have been rewritten.
        1ac53a124  tests: test_access_control_simple, adding missing import
        e3b460e21  tests: improving sss_override to adhere to new guidelines
        5d6303c66  fixing and making automatic kcm renewal test more foriving
        4805f73ea  Replacing provider conditionals with set_server method

    Gleb Popov (1):
        7c8fd5d20  util-tests.c: Properly bring back the value of TZ

    Iker Pedrosa (11):
        6c234b66c  CI: target sssd-2-9 branch in workflows
        ea6e7e545  CI: install dependencies
        d365dfcc8  CI: remove FreeBSD as they don't rely on sssd-2-9
        47fd8f670  sssd-badversion.conf: fix pre-commit issue
        8c7ee5ed2  CI: only run sssd-2-9 branch in centos-9
        39f9f5686  packit: only run upstream jobs for centos-9
        f8a640a37  Makefile: fix installation issue
        f47394f06  CI: stop running intgcheck
        c2efd27a5  CI: disable coverity in maintenance branches
        979b561f4  ci: fix dependabot.yml schema validation
        4c6c0102c  Responder: fix passkey auth when user-verification is off

    Jakub Vávra (8):
        39275ea02  Tests: Add missing markers for ticket plugin
        6987f7166  Tests: Move test_sssctl__analyze_without_root_privileges from gating
        0fcc2d2b5  Tests: Make multihost custom-log more resilient.
        f0c10efce  Tests: Update polarion team name
        a0e901f90  Tests: Update keytab rotation tests.
        276a86c7e  Tests: Drop failing ported test_idmap
        0122693f5  Tests: Skip tests unstable on other architectures.
        4f733b678  Tests: Add umockdev and virtsmarcard as test dependencies

    Justin Stephenson (34):
        480772b4d  UTIL: Add string_ends_with utility function
        deafbfcde  CONFDB: Store domain ID override templates
        17c10b9a5  SYSDB: Support ID override templates
        bbe9200ff  IPA: Support ID override templates
        df75d3b1b  tests: Stabilize analyze child logs
        7190b0141  tests: test_sssctl__analyze_child_logs handle timing issue
        0af1b6711  ci: Workaround pylibssh Failed to open session
        ccb03da73  ci: Install libssh-dev
        6d595cd48  sysdb: Execute override code even if no templates exist
        2245f841b  tests: update test_sudo network utilities
        e7179006e  ipa: additional IPA hosts/hostgroups debugging
        6907308fd  ci: constraints - pin to branch for pylibssh workaround
        b49ceceaa  ipa: Handle auto private group lookup with login override
        61bbbf42d  tests: auto private group lookup with login override
        84e11b0a8  ci: Remove intgcheck on debian-latest
        ae0b5b574  ci: Update python version to latest minor version
        22f3a532e  CI: Add dependabot to get updates of github actions
        acdb5ab85  ci: get changed script handle run for master push (non-PR)
        2879ab6fb  ci: Override shell builtin bash options for get-changed script
        200dc3df8  ci: remove pylibssh workaround
        7c2edd8dc  man: Clarify the user_attributes option
        b6fae86bf  SYSDB: Add sysdb_add_bool()
        fa661fb24  SYSDB: Dont store gid 0 for non-posix groups
        456782d06  SDAP: Remove sdap_store_group_with_gid()
        89f9b05b5  authtok: Set Kerberos passkey PIN to NULL when UV is false
        edf77b8f9  passkey: Remove SYSDB_PASSKEY_USER_VERIFICATION
        3554b52a6  pam: Skip passkey_local() in Kerberos auth flow
        f42378971  pam: Remove PAM_PASSKEY_VERIFICATION_OMIT mode
        ef635ba9e  ipa: Fix typo in trust type conditional
        9e7eb46c2  ipa: improve unknown trust type error return
        a4b350d65  util: Add string_begins_with() helper
        10456f22b  simple: Resolve group names in SID format
        7f46f04fe  tests: Update sssctl config-check tests
        cf07d7971  tests: python black 26.1.0 style changes

    Madhuri Upadhye (3):
        dd6b19bc7  tests: Add netgroup tests for incomplete triples and complex hierarchy
        80ac52de8  tests: Remove hardcoded domain and fix type errors in netgroup tests
        613961816  tests: Add netgroup offline and nested hierarchy

    Pavel Březina (25):
        185f98b01  SSSDConfig: allow last section to be empty
        e879f1d6b  ci: add pre-commit configuration
        886e371c1  ci: add python-system-tests as requirement to the result job
        6177c7a06  whitespace: fix issues found by pre-commit
        def3d3986  dependapot: add ci prefix to commit messages
        50d9cf2d1  scripts: add support for beta and rc versions
        bf40deaf9  version: replace dash with tilda
        c629eefa9  scripts: switch back to dash for pre-releases
        6d1f02a3e  ci: add automation for creating new release
        41e189490  ci: move build to standalone workflow
        7e9310abb  ci: only run changed tests for test only changes
        9f58f9cd5  ci: use parallel build
        a87fd31bf  ci: add packit configuration
        160cd2b54  packit: get version from version.m4 for upstream builds
        04a26e419  ci: remove custom copr builds
        adc612d47  ci: automatically add Reviewed-by trailer when Accepted label is set
        8dc0f6f01  ci: add autobackport workflow
        eb86ceb37  ci: remove final result job
        56bf331e5  ci: remove result job from analyze-target
        c061a8cbd  ci: remove result job from static-code-analysis
        1c333b690  ci: run long jobs only if Accepted label is not set
        d7af71e03  intg: remove ent_test.py
        56d9b114d  sbus: defer notification callbacks
        eb7a2bce7  cache_req: allow cache_first mode only if there is more than one domain
        6196567f6  tests: filter_groups by name and lookup by id with expired cache

    Samuel Cabrero (1):
        a4f007427  SSSCTL: config-check: do not return an error if snippets directory does not exists

    Scott Poore (2):
        27be9f993  CI: drop Fedora-40 from testing since it is EOL
        c595694a0  intg: remove test_session_recording.py

    Sumit Bose (27):
        37f6f1aa6  sysdb: add sysdb_get_direct_parents_ex()
        844cefe14  ipa: improve handling of external group memberships
        be42436c2  authtok: add IS_PW_OR_ST_AUTHTOK()
        6d3e61523  krb5: offline with SSS_AUTHTOK_TYPE_PAM_STACKED
        3892ad212  ci: add missing intgcheck artifacts
        de347b27f  ipa: improve handling of external group memberships
        46f7101c2  tests: test removal of external group membership
        e5224f0cb  krb5: disable Kerberos localauth an2ln plugin for AD/IPA
        56ba233e3  ipa: filter DNs for ipa_add_trusted_memberships_send()
        47361fdba  tests: add test_pac_responder.py
        a945132b7  intg: remove test_pac_responder.py
        74e18a9a7  utils: add new error code ERR_CHECK_NEXT_AUTH_TYPE
        ad46eee77  krb5_child: use ERR_CHECK_NEXT_AUTH_TYPE instead of EAGAIN
        cacbfbe08  krb5_child: clarify EAGAIN returned by krb5_get_init_creds_password()
        85af57c0d  ipa: check for empty trusts in ipa_get_trust_type()
        0fdf61789  tests: add pysss_nss_idmap system test
        74911bc38  intg: remove test_pysss_nss_idmap.py
        02108cb74  spec: clarify description of sssd-idp package
        3a8ef7353  pac: fix issue with pac_check=no_check
        91d564baa  test: check is an2ln plugin is disabled or not
        95119fff1  ipa s2n: do not try to update user-private-group
        294a62dc6  tests: check user lookup after view change
        7f1f2a45e  sysdb: add sysdb_search_user_by_upn_with_view_res()
        bf1ffa638  cache_req: use sysdb_search_user_by_upn_with_view_res()
        947c7aab7  sysdb:: remove sysdb_getpwupn()
        f5f4591a3  tests: lookup user with overrides with email
        47163860b  sysdb: do not treat missing id-override as an error

    Tomas Halman (7):
        9604b4e25  tests: Remove obsolete sssctl tests
        7adbc1f7d  tests: migrate sssctl tests to new framework
        d94ae7694  Filter IPv6 addresses not suitable for DNS updates
        cdb0167bb  test: check temporary address exclusion
        de54d140c  IPA: Fail with short names
        b0a6c302d  IPA: remove re-declaration of `ipa_trusted_subdom_init`
        33b6082d1  IPA: remove CONFDB_DEFAULT_FULL_NAME_FORMAT_INTERNAL

    Yuri Chornoivan (3):
        8f16354f2  Fix typo in sssd-ldap.5.xml
        23f925e0c  Fix typos in sss-certmap.5.xml
        2f8cf986e  Update sss-certmap.5.xml

    dependabot[bot] (7):
        60e395d00  build(deps): bump actions/setup-python from 5 to 6
        9ec94ed7d  build(deps): bump vapier/coverity-scan-action from 1.7.0 to 1.8.0
        d16491c1b  build(deps): bump actions/checkout from 4 to 5
        2f78ba468  build(deps): bump github/codeql-action from 3 to 4
        fe78007d7  build(deps): bump actions/upload-artifact from 4 to 5
        15258e9f2  ci: bump actions/checkout from 4 to 6
        f8198bce2  ci: bump actions/upload-artifact from 5 to 6

    krishnavema (1):
        3d54bafc4  tests: adding user su smartcard login test

    shridhargadekar (3):
        0a2651611  Test: HBAC affecting AD-users ipa-group membership
        f9c30efb4  Tests:cache_credentials = true not working for 2-9
        b357459cc  Tests: ADuser external group cache update
