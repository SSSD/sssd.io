SSSD 2.13.0 Release Notes
=========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

- Security fix for CVE-2026-6245: out-of-bounds read in PAM passkey responder
- During the processing of the ``pam_sss_gss`` request SSSD will read the SID from
  the PAC of the Kerberos ticket and might add authentication indicators based
  on the value of the new option ``pam_gssapi_indicators_apply``. The primary use
  case is to handle SIDs added by Active Directory’s Authentication Mechanism
  Assurance (AMA).
- Active Directory’s Foreign Security Principals (FSP) are now properly detected
  and ignored when reading nested group members. The
  ``ldap_ignore_unreadable_references`` option is only needed to ignore member
  objects which are really not accessible.
- A number of cache performance optimizations for large deployments.

New features
~~~~~~~~~~~~

- Tokens acquired from the IdP are now stored in the domain cache, and are
  automatically refreshed if the new option ``idp_auto_refresh`` is enabled.
- ``idp_type`` option allows ``entra_idp`` url to be specified if user is using a
  different Microsoft Entra endpoint.
- KDE Plasma Login Manager support.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

- New option ``avoid_by_id_lookups`` to tell the SSSD responders to use a lookup
  by name instead of by id where possible
- New options to customize the OAuth2 prompting behavior: ``interactive`` and
  ``interactive_prompt``.

Packaging changes
~~~~~~~~~~~~~~~~~

- New ``./configure`` option ``--enable-sensitive-logs`` to enable logging of
  sensitive data (like, for example, IdP tokens). Recommended for debug builds
  only.

Tickets Fixed
-------------

* `#6951 <https://github.com/SSSD/sssd/issues/6951>`__ - NSS enumerated passwd/group truncated output and performance regression since >=2.8.0
* `#7668 <https://github.com/SSSD/sssd/issues/7668>`__ - Google LDAP does not allow filtering by uidNumber by default causing SSSD cache refreshes to fail
* `#8330 <https://github.com/SSSD/sssd/issues/8330>`__ - SSSD IdP (Entra ID): listing group members does not work
* `#8441 <https://github.com/SSSD/sssd/issues/8441>`__ - Failed to resolve indirect group-members of nested non-POSIX group
* `#8446 <https://github.com/SSSD/sssd/issues/8446>`__ - oidc/entra hardcoded to graph.microsoft.com in 4 places
* `#8490 <https://github.com/SSSD/sssd/issues/8490>`__ - Add KDE Plasma Login Manager to ad_gpo_map_interactive and update man page
* `#8514 <https://github.com/SSSD/sssd/issues/8514>`__ - Release tarball contains src/tests/tests
* `#8531 <https://github.com/SSSD/sssd/issues/8531>`__ - backtrace when not providing `krb5_kpasswd` but `krb5_server`
* `#8555 <https://github.com/SSSD/sssd/issues/8555>`__ - KRB5:`do_keytab_copy()`: don't `faccessat()` for types other than 'FILE:'
* `#8616 <https://github.com/SSSD/sssd/issues/8616>`__ - Regression in IPA nightly tests: test_idp.py fails

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.12.0..2.13.0

    Alejandro López (9):
        b89f9b626  SYSDB: Remove unused function
        5b5d1ffd6  NSS: Reduce a possibly extremely long log message
        e91c10a64  NSS: Fix wrong condition invalidating an optimization
        70e78f105  TESTS: Improve test_sysdb_enumpwent_filter
        5284ea6c3  NSS: Some optimizations.
        670db53b1  NSS: Be coherent when using a lastUpdate filter
        55e3a308e  NSS: Fix the logged function name
        11a15c250  NSS: Fix sysdb_enumpwent_filter()
        0a739f855  NSS: Better handle ERR_NO_TS in sysdb_enumpwent_filter()

    Alexey Tikhonov (46):
        e73250b1e  SPEC: since Fedora 44 Samba provides dedicated 'samba-ndr-libs' package
        ee081e11f  SBUS: increase SBUS_MESSAGE_TIMEOUT to 5 mins
        7762901c3  RESPONDER: fixed an issue with 'client_idle_timer'
        35e32b77d  UTILS: comment fixed
        743b8d33f  Makefile: 'libsss_child' doesn't need to be part of 'libsss_util'
        704f36333  Makefile: don't link against 'KEYUTILS_LIBS'
        25dcf242d  UTILS: get rid of 'selinux.c'
        2112b6eb0  Makefile: removed some duplicates
        8d376e8cf  Makefile: `libsss_crypt` doesn't need `libdhash`
        f95f64f52  CONFIG: allow 'ldap_subuid_*' attrs
        498974b84  RESPONDER: fix `responder_set_fd_limit()`
        a7fb84376  PO: remove stray </arg> from translation
        af5fbd52e  PO: add missing <placeholder ...> tag
        29a8731d2  Fix libini_config related includes.
        ee42c35db  INI: get rid of useless macros
        ade61ef1b  INI: use proper deallocators
        003c591a3  CHILD HELPERS: use less severe debug level
        09e283e22  SDAP: use `DEBUG_CONDITIONAL` in hot path
        9a2cf2122  UTIL: `sss_tc_utf8_str_tolower()` optimization
        a5b77e429  UTIL: `sss_create_internal_fqname()` optimization (caching)
        2de37515b  UTIL: fix discarded-qualifiers warning in domain_to_basedn()
        5548493c7  SDAP: fix discarded-qualifiers warning in are_sids_from_same_dom()
        ef104b784  SDAP: fix discarded-qualifiers warnings in sdap_parse_range()
        086a52e5d  SDAP: fix discarded-qualifiers warning in split_extra_attr()
        0f21660da  AD: fix discarded-qualifiers warnings in ad_access filter parsing
        24de2bc0a  CERTMAP: fix discarded-qualifiers warnings in sss_certmap.c
        68edad94b  KRB5: fix discarded-qualifiers warning in compare_principal_realm()
        9e517f84b  Makefile: add missing 'CMOCKA_CFLAGS'
        39db12dc3  BUILD: supress 'deprecated-declarations' error for cmocka tests
        54c634033  BUILD: fix _POSIX_C_SOURCE redefinition with Python 3.14 and glibc 2.41+
        f91c7bbc3  sdap: eliminate O(N^2) loop in `sdap_add_incomplete_groups()`
        8c1e20b23  LDAP: free tmp var within the loop
        c1eced627  memberOf plugin: redundant comparison removed
        7a7480e84  memberOf plugin: swap instead of a shift
        704c31dbc  memberOf plugin: avoid `ldb_dn_compare()` in `mbof_add_operation()`
        74e7bc658  KRB5: fix mem leak in `authenticate_stored_users()`
        5b85b647e  UTIL: fix mem leak if `get_active_uid()` fails
        feca02838  SDAP: reduce logger load in the hot path
        87c7bce15  SDAP: use DEBUG_CONDITIONAL in the hot paths
        8631c02e0  KRB5: log level adjusted
        2dcdca2f9  memberOf plugin: avoid `ldb_dn_compare()` in `mbof_append_addop()`
        05706145e  memberOf plugin: avoid `ldb_dn_compare()` in `mbof_append_muop`
        06692d50a  memberOf plugin: use hash table for value dedup in `mbof_append_muop()`
        0100b1c35  KCM: fix use-after-free in `kcm_read_options()`
        a809b9236  Add missing include
        3b0b16e96  PAM/PASSKEY: avoid unnecessary memcpy

    Christopher Byrne (1):
        dc6970c2a  src/sss_client/common.c: Use getpwnam_r to avoid clobbering struct passwd

    Dan Lavu (7):
        ab7a7f438  removing netgroup intg test
        0458e6556  updating subid test case to test provider_ldap config
        b4e88e833  adding sss_ssh_knownhosts test case
        77fc6ff1d  updated kcm flaky test
        428e61304  Reworked memcache tests * parametrized test cases * added colliding hash test case * remove poor test scenarios
        7d9bdd508  removing intg memcache tests
        6726f5a8a  removing unstable topologies from memecache tests

    Ezri Zhu (1):
        3bd74d9b3  oidc_child: parameterize entra_idp url

    Gleb Popov (14):
        f2a4ce27d  FreeBSD CI: Switch to FreeBSD 15
        46fb30abd  FreeBSD CI: Enable testing and run the build with -j
        165f51129  FreeBSD CI: Remove the timezone patch for FreeBSD 14 and add another one
        af8ef967a  Use portable shebangs in tests scripts
        308bacbd2  Skip whitespace and double semicolon tests on FreeBSD
        26350606a  FreeBSD CI: Add some more deps and make configure flags match what our port does
        d78f89cde  test_responder_common.c: Use correct value to check against
        e4eb8bdc0  test_pam_srv: Use more random UIDs/GIDs for the test
        308af8f21  platform.m4: Fix case when we have to source /etc/os-release
        c6dc4d7af  FreeBSD CI: Pass correct paths to adcli and realm programs
        404d166a6  sdap_select_principal_from_keytab_sync: waitpid() synchronously
        b970e7fac  Print a bit more information in the debugging output of resolv_is_address() and get_client_cred()
        64ee91fa5  getsockopt: Pass correct option level value on FreeBSD
        ba4353fdd  dp_target_id.c: Fix typo "lenght" -> "length"

    Hosted Weblate (1):
        9c836671c  po: update translations

    Iker Pedrosa (2):
        dd3cd958d  krb5_child: fix enterprise principal parsing in keep-alive sessions
        03b744103  ci: install and load kernel module for passkey testing

    Jakub Vávra (2):
        07401d626  Test: Update misc ipa tests to work correctly on stig
        0c956d95c  Tests: Housekeeping and Clean Sweep of Sevice/Logging suite

    Justin Stephenson (2):
        96829a000  tests: python black 26.1.0 style changes
        d87b96f11  ci: Skip GPG checks when installing rawhide sssd rpms

    Madhuri Upadhye (2):
        2cdaaa47a  Fix test_sudo__case_sensitive_false: use /bin/ls and /bin/cat instead of less/more
        80e648257  tests: port LDAP+Kerberos tests to pytest

    Neal Gompa (1):
        5df3bfff9  Add support for Plasma Login Manager as a supported PAM service

    Nikola Forró (2):
        f9697d4ff  Use macro rather than shell expansion for string processing in spec file
        caa0ec228  Add a default for %samba_package_version

    Ondrej Valousek (6):
        d77096434  Simplify direct nested group processing
        b3a9b8198  Parser update, cleanup
        f13a88ca5  Tests fix: mock users/groups with objectclasses and expected RFC2307 attrs
        461722a39  Bugfix (handle unreadable references) that intg check discovered
        ccfc33a9a  sdap: restrict list of requested attributes
        96d38232f  Honor ldap filters

    Paul Adelsbach (1):
        d0beceaa1  pam: gate PAC indicator code on BUILD_SAMBA

    Pavel Březina (10):
        6afffacf2  Update version in version.m4 to track the next release
        7d8e3c333  scripts: fetch branch before checkout in release script
        4e89caeb9  errors: add ERR_SERVER_FAILURE
        cc42932ac  sdap: remove be context from sdap_cli_connect code
        3b7dc8c73  contrib: removed unused test-suite
        f260623f9  dist: clean up and fix ditribution tarball
        cb1ef376a  scripts: add fixed-issues.sh script
        27aac3a29  scripts: add generate-release-notes.py script
        033a81bef  scripts: add generate-full-release-notes.sh script
        c8257a3ef  ci: automatically generate release notes

    Paymon MARANDI (2):
        3d2752679  krb5: improve reporting failure on reading keytab
        95d847670  krb5: make sure keytab is a FILE before checking for access

    Scott Poore (4):
        f8c281cfe  Tests: Add GDM Smartcard tests
        d78e32678  Tests: gdm passkey fixes for timing issues in c10s
        7f78c93f1  Tests: rename and update test_gdm to xidp
        17390fd25  Test: combine gdm tests into one file

    Striker Leggette (2):
        58cc4d226  Fix spelling in AD provider code comments
        35019632b  More trivial spelling/grammatical fixes. No functional code was harmed in the changing of these files.

    Sumit Bose (25):
        4ca8bb655  pam_sss: change PAM message type for PIN locked
        bc3ad168e  krb5: check for PIN locked in error message
        bcd9998f0  man: add details about 'an2ln'
        ad173e057  sdap: do not require GID for non-POSIX group
        3766e5188  sdap: add sdap_get_and_multi_parse_generic_send()
        d028661e1  sdap: use sdap_get_and_multi_parse_generic_send
        c6f941d62  sdap: remove extra parsing
        e27b791b5  ad: add basic foreign security principal sdap map
        b97dbe536  sdap: avoid second parsing of objectclasses
        d8b53a88d  tests: add a test with a FSP group member
        92ffd72c1  sdap: new type SDAP_NESTED_GROUP_DN_IGNORE
        251aca943  sdap: add struct sdap_reply_with_type
        59bc5d628  sdap: add struct sdap_attr_map_info_ex
        6e87db116  sdap: re-add IPA shortcut for nested members
        3a33ae01e  sdap: initialize attribute list only once
        527d67072  sdap: initialize base filter only once
        fc779c4d9  sdap: change increment style for reply array
        639814e6b  tests: remove wrong and misleading assigment
        10d509a84  conf: add avoid_by_id_lookups domain option
        c767b8ea0  cache_req: switch from ID to name lookup
        a3b2b4f15  idp: do not update cache timeout if member is added
        3f9c415ab  ad: move ad_get_sids_from_pac() to ad_pac_common.c
        22de4fd2d  pam: add pam_gssapi_indicators_apply option
        1f680edad  pam: apply SIDs from PAC to authentication indicators
        9926e7ef9  oidc_child: add new option return-tokens

    Timo Eisenmann (20):
        0fc52802f  Add OAuth2 prompting config
        870619c42  sss_client: deduplicate string copying in pc_list_from_response
        a50a9529d  Add test for OAuth2 prompting config
        1233fc7d6  config: add missing rules for idp options
        6a3295280  oidc_child: get refresh_token for later
        371148d7c  oidc_child: store tokens in cache
        ede49c2c2  oidc_child: add --refresh-access-token flag
        9525cccb4  idp: automatically refresh tokens
        2e887f12c  idp: add option to automatically refresh tokens
        1f57c2b11  idp: delete non-replaced tokens from cache
        aadae62db  idp: construct pam_data with timer
        a3c506dd9  oidc_child: url-encode post data items
        0f08795fd  oidc_child: free json objects properly
        c9ca1900e  oidc_child: add macros for token names
        fe5d548d7  idp: pass sss_domain_info to create_refresh_token_timer
        c3f6388f8  idp: fix idp_id_scope Entra example
        3f65f58b2  oidc_child: initialize curl only once
        f9ee090e7  fix typos
        ec440c04c  fix gcc warning
        a32aab401  add config option to enable logging sensitive data

    Xu Raoqing (1):
        550b08cab  pam: fix out-of-bounds read in pam_passkey_child_read_data

    aborah-sudo (4):
        8b0071c64  Tests: Handle SELinux in proxy provider tests
        157194618  tests: reorganize infopipe tests by interface
        a6d0f0cf4  Tests: Fix ipa multihost test_authentication_indicators
        abee6e7ca  Tests: Add integration tests validating SSSD socket

    dependabot[bot] (2):
        7328fbdb8  ci: bump actions/upload-artifact from 6 to 7
        23a23cd29  ci: bump crazy-max/ghaction-import-gpg from 6.3.0 to 7.0.0

    squiddim (1):
        b4336056d  systemd: relaunch sssd after unclean exit

    sssd-bot (2):
        9faae339d  pot: update pot files
        d1329f902  Release sssd-2.13.0

