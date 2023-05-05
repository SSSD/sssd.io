SSSD 2.9.0 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* ``sss_simpleifp`` library is deprecated and might be removed in further releases. Those who are interested to keep using it awhile should configure its build explicitly using ``--with-libsifp`` ``./configure`` option.
* "Files provider" (i.e. ``id_provider = files``) is deprecated and might be removed in further releases. Those who are interested to keep using it awhile should configure its build explicitly using ``--with-files-provider`` ``./configure`` option. Or consider using "Proxy provider" with ``proxy_lib_name = files`` instead.
* Previously deprecated ``--enable-files-domain`` configure option, which was used to manage default value of the ``enable_files_domain`` config option, is now removed.
* Long time unused '--enable-all-experimental-features' configure option was removed.
* SSSD will no longer warn about changed defaults when using ``ldap_schema = rfc2307`` and default autofs mapping. This warning was introduced in 1.14 to loudly warn about different default values.

New features
~~~~~~~~~~~~

* New passkey functionality, which will allow the use of FIDO2 compliant devices to authenticate a centrally managed user locally. Moreover, in the case of a FreeIPA user, it can also issue a Kerberos ticket automatically with upcoming FreeIPA version 4.11.
* Add support for ldapi:// URLs to allow connections to local LDAP servers
* NSS IDMAP has two new methods: ``getsidbyusername`` and ``getsidbygroupname``

Note: support for passkey is in its initial phase and the authentication policy will be adjusted in future versions.

Packaging changes for passkey
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Include passkey subpackage and dependency for libfido2.

Configuration changes for passkey
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* New options to enable and tune passkey behavior: ``pam_passkey_auth``, ``ldap_user_passkey``, ``passkey_verification``, ``passkey_child_timeout``, ``interactive``, ``interactive_prompt``, ``touch`` and ``touch_prompt``.
* ``--with-passkey`` is a new configuration option to enable building passkey authentication.


Important fixes
~~~~~~~~~~~~~~~

* A regression when running sss_cache when no SSSD domain is enabled would produce a syslog critical message was fixed.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* Default value of ``cache_first`` option was changed to ``true`` in case SSSD is built without ``files provider``.
* ipa_access_order parameter introduced. It behaves much like ldap_access_order but affects IPA domains (id_provider = ipa) and accepts limited values. Please see sssd-ipa(5) for more information.

Tickets Fixed
-------------

* `#5390 <https://github.com/SSSD/sssd/issues/5390>`__ - sssd failing to register dynamic DNS addresses against an AD server due to unnecessary DNS search
* `#6383 <https://github.com/SSSD/sssd/issues/6383>`__ - sssd is not waiting for network-online.target
* `#6403 <https://github.com/SSSD/sssd/issues/6403>`__ - Add new Active Directory related certificate mapping templates
* `#6404 <https://github.com/SSSD/sssd/issues/6404>`__ - [RFE] Add digest mapping feature from pam_pkcs11 in SSSD
* `#6451 <https://github.com/SSSD/sssd/issues/6451>`__ - UPN check cannot be disabled explicitly but requires krb5_validate = false' as a work-around
* `#6479 <https://github.com/SSSD/sssd/issues/6479>`__ - Smart Card auth does not work with p11_uri (with-smartcard-required)

* `#5080 <https://github.com/SSSD/sssd/issues/5080>`__ - [RFE] - Show password expiration warning when IdM users login with SSH keys
* `#5390 <https://github.com/SSSD/sssd/issues/5390>`__ - sssd failing to register dynamic DNS addresses against an AD server due to unnecessary DNS search
* `#6228 <https://github.com/SSSD/sssd/issues/6228>`__ - Enable passkey authentication in a centralized environment
* `#6324 <https://github.com/SSSD/sssd/issues/6324>`__ - coredump occurs when I restart sssd-ifp.service with sssd.service is inactive
* `#6357 <https://github.com/SSSD/sssd/issues/6357>`__ - KCM erroneously changes primary cache when renewing credentials
* `#6360 <https://github.com/SSSD/sssd/issues/6360>`__ - [D-Bus] ListByName() returns several times the same entry
* `#6361 <https://github.com/SSSD/sssd/issues/6361>`__ - [D-Bus] ListByName() fails when not using wildcards
* `#6383 <https://github.com/SSSD/sssd/issues/6383>`__ - sssd is not waiting for network-online.target
* `#6387 <https://github.com/SSSD/sssd/issues/6387>`__ - Fatal errors in log during Anaconda installation: "CRIT sss_cache:No domains configured, fatal error!"
* `#6398 <https://github.com/SSSD/sssd/issues/6398>`__ - [D-Bus] Groups.ListByName() and Groups.ListByDomainAndName() not working
* `#6403 <https://github.com/SSSD/sssd/issues/6403>`__ - Add new Active Directory related certificate mapping templates
* `#6404 <https://github.com/SSSD/sssd/issues/6404>`__ - [RFE] Add digest mapping feature from pam_pkcs11 in SSSD
* `#6451 <https://github.com/SSSD/sssd/issues/6451>`__ - UPN check cannot be disabled explicitly but requires krb5_validate = false' as a work-around
* `#6465 <https://github.com/SSSD/sssd/issues/6465>`__ - SBUS:A core dump occurs when ``dbus_server_get_address()``
* `#6477 <https://github.com/SSSD/sssd/issues/6477>`__ - changing password with ldap_password_policy = shadow does not take effect immediately
* `#6479 <https://github.com/SSSD/sssd/issues/6479>`__ - Smart Card auth does not work with p11_uri (with-smartcard-required)
* `#6487 <https://github.com/SSSD/sssd/issues/6487>`__ - implicit declaration of function ``fgetpwent`` in test_negcache_2.c
* `#6505 <https://github.com/SSSD/sssd/issues/6505>`__ - SSS_CLIENT: general library destructor should cancel thread-at-exit destructors
* `#6531 <https://github.com/SSSD/sssd/issues/6531>`__ - FAST/OTP with Anonymous PKINIT - oddly requires a keytab to exist (can be a bogus keytab)
* `#6544 <https://github.com/SSSD/sssd/issues/6544>`__ - AD: Nested group processing can fail or return invalid members (security issue)
* `#6548 <https://github.com/SSSD/sssd/issues/6548>`__ - sssd-ipa
* `#6551 <https://github.com/SSSD/sssd/issues/6551>`__ - passkey_child cannot be used to register passkey due to too strict permissions
* `#6558 <https://github.com/SSSD/sssd/issues/6558>`__ - enabling passkey authentication breaks idp support
* `#6565 <https://github.com/SSSD/sssd/issues/6565>`__ -  Improvement: sss_client: add 'getsidbyusername()' and 'getsidbygroupname()' and corresponding python bindings
* `#6588 <https://github.com/SSSD/sssd/issues/6588>`__ - Integration Tests：The ``sssd_hosts`` module is missing in release tarball
* `#6592 <https://github.com/SSSD/sssd/issues/6592>`__ - pid wrapping caused sss_cli_check_socket to close the file descriptor opened by the process
* `#6600 <https://github.com/SSSD/sssd/issues/6600>`__ - [sssd] Auth fails if client cannot speak to forest root domain (ldap_sasl_interactive_bind_s failed)
* `#6610 <https://github.com/SSSD/sssd/issues/6610>`__ - BUILD: Clear compilation alarms.
* `#6612 <https://github.com/SSSD/sssd/issues/6612>`__ - MIT Kerberos confusion over password expiry
* `#6617 <https://github.com/SSSD/sssd/issues/6617>`__ - filter_groups doesn't filter GID from 'id' output: AD + 'ldap_id_mapping = True' corner case
* `#6626 <https://github.com/SSSD/sssd/issues/6626>`__ - Unable to lookup AD user from child domain (or "make filtering of the domains more configurable")
* `#6635 <https://github.com/SSSD/sssd/issues/6635>`__ - sss allows extraneous @ characters prefixed to username


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.8.0..2.9.0

    Alejandro López (36):
        2070000a3  CACHE_REQ: Do not use timestamp optimization on "files" provider.
        214540e72  Cache: String has to be duplicated instead of copied
        719c92533  CACHE_REQ: Initialize domain with NULL
        8f7c35eae  CACHE_REQ: Do not return duplicated values.
        a97962826  TESTS: Correct ListByAttr()'s test
        569dca5f2  CACHE_REQ: Consider the domain when looking names in the cache
        09895561a  TESTS: New test for D-Bus' ListByName()
        c3453e4e8  CACHE_REQ: Use a const struct in cache_req_data_create()
        36e5479b2  BUILD: Fix some warnings thrown while building
        34d55884c  BACKEND: Reload resolv.conf after initialization
        0da99b73e  SDAP: Fixed header file
        11dab864e  PAM: Localize some forgotten words.
        475052a29  LDAP: Moved and renamed set_access_rules()
        ae74a9d1f  IPA: Add password expiration warning when using ssh keys
        be84d6ee8  PAM: Warn that the password has expired when using ssh keys
        ede02a201  MAN: Cosmetic changes to sssd-ldap.5
        cfd71fec6  MONITOR: Move the file monitoring code to util.
        d4e574475  TESTS: Add a test for file-watch
        e1c0af26e  MAN PAGES: Make try_inotify dependent on HAVE_INOTIFY.
        fadd8eb6c  BACKEND: Move resolv.conf watching to the backends
        2e3fa180d  D-BUS: Remove resInit() method from sssd.services
        c97d92754  FILE WATCH: Get rid of parent_ctx
        729c1fc2d  FILE WATCH: Simplify watching on missing files.
        fe67123cc  CONFIG-CHECK: Extracted code checking 'inherit_from'
        1911ad64f  CONFIG-CHECK: Function always returns EOK
        255d9f6e8  CHECK-CONFIG: id_provider is now mandatory
        f604d033f  TESTS: Test mandatory id_provider
        f283248ff  CONFIG-CHECK: inherit_from is not a typo
        55e27a423  KCM: Switch default caches only when there is no current default.
        cfc591d65  SDAP: Include struct ldb_dn in struct sdap_search_base
        84e7dbc9b  SDAP: Ignore the cn=views entries in nested groups
        9e9d5825d  Tests: Test that cn=views is ignored.
        54aabca0b  UTIL: Introduicing SPRItime
        3463caa82  COVERITY: Remove several Y2K38_SAFETY warnings
        3b65d7be5  COVERITY: Resolve a WRITE_CONST_FIELD warning
        c3d6cc9a3  AD: Do not use the shortcut when filter_groups is set.

    Alexander Bokovoy (2):
        9724f871a  passkey: only accept the client realm as relaying party ID
        d0a6bf606  passkey: implement realm check for the passkey challenge

    Alexey Tikhonov (48):
        a5403f789  IPA: "trusted user not found" isn't an error
        8a2fd06b2  CFG RULES: allow 'fallback_to_nss' option
        71466a8db  SYSDB: pre-existence of MPG group in the cache isn't an error
        3e02de933  UTILS: socket connect: added missing new line and adjusted log level to more appropriate
        25eae1c08  SYSDB: use `sss_strerror()` to handle `ERR_GID_DUPLICATED`
        93ed5e58e  UTILS: got rid of deprecated `inet_netof()` to please 'rpminspect'.
        6ef3aade0  TOOLS: don't export internal helpers
        7af46ba0e  TOOLS: fixed handling of init error
        99791400b  SSSCTL: don't require 'root' for "analyze" cmd
        d4d9aa654  SSSCTL: don't require 'root' for "passkey-exec" cmd
        e4dd11f2c  SYSDB: pre-existence of MPG group in the cache isn't an error
        8b09c9387  Translations: add missing `tools/sssctl/sssctl_cert.c` and macros
        714ababe8  BUILD: deprecate `--enable-files-domain` build option
        293264509  SBUS: don't call `dbus_server_get_address(NULL)`
        4e600d9b9  Added a number of missing new lines.
        b631c3174  MAN: mention `attributes` in 'see also'
        08ccd23fb  SSS_CLIENT: delete key in lib destructor
        501e05f46  BUILD: remove `--enable-files-domain` build option
        6b048a6a1  INTG TESTS: make `get_call_output()` respect `check` arg for Python < 3.7
        6ffd46d11  MAN: remove "experimental" notice off LDAP access control based on NDS attributes.
        aa5c0c9c0  BUILD: remove long time unused '--enable-all-experimental-features'
        0b8638d8d  SSS_CLIENT: fix error codes returned by common read/write/check helpers.
        ef93284b5  SSS_CLIENT: if poll() returns POLLNVAL then socket is alredy closed (or wasn't open) so it shouldn't be closed again. Otherwise there is a risk to close "foreign" socket opened in another thread.
        bf3f73ea0  PAM_SSS: close(sss_cli_sd) should also be protected with mutex. Otherwise a thread calling pam_end() can close socket mid pam transaction in another thread.
        4e6540052  PAM: removed outdated comment
        c55bb3976  Use `is_files_provider()` helper where possible.
        8e75bb611  RESPONDERS: get rid of `NEED_CHECK_PROVIDER` helper
        d4f7ed69d  MONITOR: fix `socket_activated` flag initialization
        9f8e71152  MAN: describe security risk of `cache_credentials`
        2ce24d38d  UTILS: missing domain in `sss_parse_name()` input isn't SSSDBG_CONF_SETTINGS
        f5787878e  NSS: empty result of `..._group_by_origgid()` isn't an error
        e5fba8f97  TESTS: fix compilation issue with musl libc
        7356881cd  SDAP: removed leftovers after 65bd6bf05d75c843e525f8bf89e9b75b02a2bfb7
        a9bc94f0e  INTG-TESTS: add missing files to Makefile.am
        067cc5cce  BUILD: make "files provider" build configurable
        978ef1794  UTILS: force inline `is_files_provider()`
        c53390a83  DP: warn loudly if config uses 'files' when support wasn't built
        8962eaca5  INTG-TESTS: enable '--with-files-provider'
        132fb4016  Deprecate 'sss_simpleifp' library.
        c586b9a28  RESPONDERS: delete obsolete 'responder_sbus.h'
        437dbe9e1  MONITOR: currently only 'ifp' doesn't support running as non-root
        e2106c946  SUDO: fix mistype
        5159992d7  RESPONDER: use safe helper
        64424963a  UTILS: sanitize `cli_creds_get_*` macro
        ae691f0b4  NSS: change default value of 'cache_first' to 'true'
        ddec8ae2d  SPEC: obsolete libsss_simpleifp
        9bf55bf9a  MONITOR: disable 'user' config option in case --with-sssd-user=root
        8b94af6ef  MONITOR: validate value of 'user' option.

    Cole Robinson (1):
        340691fae  MAN: Fix option typo on sssd-kcm.8

    Dan Lavu (4):
        419b9b8f6  Adding Ported DynDNS Testcases
        7caf2da3c  Fixing dyndns tests
        53c8e8f07  Removing unnecessary restart unnecessary restart
        9aece27dd  Adding ptr zone creation to class setup

    David Härdeman (1):
        96a0e9fbe  LDAP: Handle MIT LDAP KDB password expiry

    Florence Blanc-Renaud (1):
        718afc297  Passkey: flush stdout

    Gioele Barabucci (1):
        47f82a418  Makefile: Install dbus policy in /usr, not /etc

    HelloCarry (1):
        42594c375  fix sysvol_gpt_version may be used uninitialized

    Iker Pedrosa (23):
        7a1976c94  fido2: register key with helper process
        9a2548ea0  fido2: make the build conditional
        f800471e2  sssd.supp: suppress leak errors
        8bdcc0287  passkey: change fido2 to passkey
        f24b6daa9  passkey: replace erroneous description
        28124cfbd  passkey: print PEM formatted public key
        ab6910ae0  passkey: verify assertion
        2b0a8f275  passkey: public key in PEM format
        6b0d175f8  passkey: input PIN via stdin
        336b1facd  ci: fix codeql
        723872f3e  CI: remove flake8 action
        927fa8433  passkey: register discoverable credentials
        62654e254  passkey: user id for discoverable credentials
        bd02f6378  passkey: fix uninitialized variable
        30daa0ccd  spec: update to include passkey
        92d1b4699  passkey: move select authenticator
        bccdc2af2  passkey: obtain assertion data
        f77ec4f50  passkey: verify assertion data
        8218634df  passkey: replace printf by PRINT
        dae5367b6  test: cast to `char *` assert_string_equal() args
        a41810bdf  CI: store CodeQL configuration artifacts
        f97cd4d4f  passkey: don't print User ID
        619ecbbc6  test: add conditional build for passkey functions

    Jakub Vavra (26):
        a21c66625  Tests: Add a test for bz1964121 override homedir to lowercase
        a7759ab30  Tests: Add the missing admisc pytest marker.
        bce2b0c80  Tests: Wait a bit before collection log in test_0015_ad_parameters_ad_hostname_machine.
        d7e7efe93  Tests: Fix E126 in test_adparameters_ported.py
        14748ff98  Tests: Update fixture using adcli to handle password from stdin.
        fc3fad982  Tests: Fix automount OU removal from AD.
        153b1c913  Tests: Add mark tier1_4 so pytest is not throwing warnings.
        c4ea28511  Tests: Move some less important scenarios from tier 1 to tier 2.
        067c550cf  Tests: Test for bz2144491 UPN mismatch
        708a924a1  Tests: Changes to the version handling and fixture create_testdir.
        32a8b9538  Tests: Optimize winhost properties
        fc4f0399b  Tests: Fix incorrect distro parsing in qe_class on Fedora.
        97e040f98  Tests: Set cryptopolicy for master for AD fips tests.
        9145544fd  Tests: Add a remedy for a missing multihost_dir.
        1c55f0d4c  Tests: Refactor join ad.
        80d28babb  Tests: Make sure that session_multihost.ad is always available.
        f46fe473c  Tests: Skip test_0002_ad_parameters_junk_domain on multiarch
        9e061fc06  Tests: Remove keytab on realm leave.
        bc5de6868  Tests: Add a timeout to realm join for AD, modify realm leave.
        255c01a1c  Tests: Fix error in cifs tests.
        325fc8e13  Tests: Improve stability of tests in TestADParamsPorted, remove un-needed backups.
        30e0b472a  Tests: Add tests for BZ1765354
        9329c09dc  Tests: Fix pytest markers to remove warnings.
        04cc2f73c  Tests: Install libsss_simpleifp conditionally based on release.
        d735fb1e4  Tests: Ignore chattr result on resolv.conf
        ed2510d91  Tests: Add test for bz1913839 gid of filtered group gid still present in id

    Justin Stephenson (32):
        5b27a353a  Fido2 child: Add missing options
        ab89455be  CI: Build srpm fix for illegal version tag '-'
        6d87af5ef  SSSCTL: Add passkey exec command
        ee0d73a2c  SSSCTL: Use wrapper function for analyze
        4c678cbb4  Analyzer: Optimize list verbose output
        bfa8d50c4  Analyzer: Ensure parsed id contains digit
        2f99cd31b  SSSCTL: Add debug option to help message
        4a6eb258c  CI: Update core github actions
        4138b0a73  MAN: ldap_group_name enhancement with nested groups
        fb5a300b4  passkey: Add configuration options
        fbbe9ba3f  authtok: Add Passkey type
        57152761b  Add new option ldap_user_passkey
        3f24aa71f  Extend IPA config search
        ec6774930  Add DNS Domain name to struct sss_domain_info
        ea9bcab65  IPA Retrieve passkey configuration
        b92ff263c  PAM: Call the passkey helper binary
        7f8fe3994  Support Passkey prompting config
        64f98463a  Tests: Passkey (Pre)auth
        938676a37  Tests: Passkey prompting config
        64aa2672e  PAM: Add destructor for passkey pin
        5a22aefbc  PAM: Covscan NULL check for cache req result domain
        50a3a1911  Passkey: Use correct User verification comparison
        745379bc4  SSSCTL: Switch passkey-exec to passkey-register
        cdfe2c515  Authtok: Support SSS_AUTHTOK_TYPE_PASSKEY{_REPLY}
        5de070f94  pam_sss: Add passkey kerberos preauth support
        7c34742c4  krb5_child: Add passkey kerberos preauth support
        c76ba343b  PAM: Passkey kerberos preauth support
        9869e4875  krb5_child: Increase child buffer and chunk size
        88f4d3cf7  Passkey: Add util function to prefix passkey data
        1032ca21d  MAN: Clarify user_verification will be overwritten
        bb21171b7  Passkey: Changes to debug_libfido2 option
        5744bad7d  Tests: Amend PAM Preauth tests

    Luke Dickinson (1):
        d48669405  Remove the need for a keytab when using fast with anonymous pkinit

    MCJ Vasseur (1):
        02bdef7d7  Fix typo (pasword -> password)

    Madhuri Upadhye (3):
        81eb0606d  Tests: Minor fixes for alltests
        576a1c19a  Tests: Automation of bug, bz2100789, which test id_provider parameter from domain section
        c200fc019  Test: Test nested group in view based search

    Pavel Březina (35):
        6a2de710b  Update version in version.m4 to track the next release
        b38fdc818  confdb: avoid syslog message when no domains are enabled
        4da861368  monitor: read all enabled domains in add_implicit_services
        64c22dd1c  sss_cache: use ERR_NO_DOMAIN_ENABLED instead of ENOENT
        df55b1f16  confdb: chande debug level when no domain are found in confdb_get_domains
        103a48887  autofs: do not yield warning on default configuratoin
        62458d490  ci: enable ci for sssd-2-8 branch
        c526acbae  ci: switch to actions/checkout@v3
        770bf7bf3  ci: use GITHUB_OUTPUT instead of set-output
        b2d193b93  ci: switch to actions/upload-artifact@v3
        a22af6f00  pot: update translations
        f5c0e7b39  ci: make /dev/shm writable
        ae614c17b  ci: install correct python development package
        c6053c431  pot: update pot files
        f43d8c9a0  ci: increase timeout for covscan
        7e8b97c14  ldap: update shadow last change in sysdb as well
        c0b394ab2  sudo: skip smart refresh if it happens inside full refresh
        59d2f945e  fix missing new line in sss_iface.c and docstrings.rst
        f44e58642  tests: fix all flake8 issues
        bd803bf6b  nssidmap: add getsidbyusername and getsidbygroupname
        712377ea5  tests: add system tests using pytest-mh framework
        ce81f017f  tests: include requirements.txt in system tests documentation requirements
        df7a5c33a  tests: build systen tests documentation in readthedocs
        62cb54dc2  tests: make pytest-ldap aware of TLS options
        ad68d71c3  passkey: add Kerberos plugins
        2a16c2563  idp: switch to common API for radius-style plugin
        a5efc5e63  tests: fix type errors due to type enhancements in jc
        3d0fcca3c  tests: avoid list() and dict() as default parameter value
        a825b28b1  passkey: fix copyrights and comments in krb plugin
        e794bfdea  ci: prepend pr copr build with high version number
        c3a0b5f07  tests: split system test framework into standalone repository
        559f29ffb  tests: load fixtures from sssd-test-framework
        52c3d6c2d  tests: create data directory in system tests
        e91b5d4ad  man: put sssd_user_name.include to builddir
        6c184c476  pot: update pot files

    Sargun Narula (6):
        2bd0c249b  Tests: Ported Bash-krb-access-provider to pytest
        61f1b8937  Tests: Ported Bash-krb-fast-principal to pytest
        61d6030b1  Added entry for krb_access_provider in readme.rst
        9fd8da284  Fixed domainname value in krb_ldap_connection
        821455c7c  Tests: Ported cache_performance testing cases to pytest
        6d659e29e  Fixed docstring minor changes

    SargunNarula (1):
        34f1c222c  Reused sssdTools Instance

    Shridhar Gadekar (14):
        a05719fab  Tests: Porting the AD-Access-control test-suite to pytest
        92347d98f  Tests: GSSAPI ssh login failing due to a missing directive
        955192b12  Tests: gssapi ssh login minor fix
        607723063  Tests: Use negative cache better for lookup by SIDs
        664a436e9  Test: gssapi test fix
        24a536638  Tests: port bash idmap testcase to pytest
        ddd85f95d  Tests: change tier of dyndns tests
        2fa80dbd2  Dropping idmap
        42842c16a  TESTS: bz2110091 sssd starting offline after reboot
        8cda19e28  Tests: bz2128840 automation
        4e9c2fdbe  TESTS: clean up group delete fix
        d249154c0  Test: porting of failing rfc2307bis testcase
        a75557b73  Test: porting bash range_retrieval to pytest
        265f6e028  Tests: sss allows extraneous @ characters prefixed to username

    Steeve Goveas (1):
        790e7a779  Tests: Cannot SSH with AD user to ipa-client with invalid keytab

    Sumit Bose (23):
        91789449b  PAC: allow to disable UPN check
        b3d7a4f6d  ipa: do not add guessed principal to the cache
        51b11db8b  pac: relax default check
        3f8bc8720  certmap: add support for serial number
        10d977a36  certamp: add support for subject key id
        9e1b711b2  certmap: add support for SID extension
        f293507d9  certmap: fix for SAN URI
        c4085c9a7  certmap: add bin_to_hex() helper function
        11483f1ec  sssctl: add cert-eval-rule sub-command
        3676a4fba  certmap: add get_digest_list() and get_hash()
        0a9061073  certmap: dump new attributes in sss_cert_dump_content()
        1303c6241  certmap: add LDAPU1 mapping rules
        4ac53fb5e  certmap: add tests for new attributes and LDAPU1 rules
        882f560e6  certmap: add LDAPU1 rules to man page
        b0bdf712e  certmap: Add documentation for some internal functions
        aac303e84  p11: fix size of argument array
        7fb89ab01  passkey: do not copy more than received
        6ba0187e1  certmap: fix to handle ediPartyName
        ced32c44e  certmap: Handle type change of x400Address
        ebc1e460e  krb5: add joined/parent domain to [domain_realm]
        def571ba4  krb5: make sure realm is known when writing domain_realms
        9358a74d3  ad: skip filtering if ad_enabled_domains is set
        1bf475140  tests: fix typo in ldapi test

    Timotej Lazar (1):
        e623fac7e  tests: use echo instead of /bin/echo in Makefile

    Tomas Halman (4):
        2fda8e7b7  RESOLV: Configuration option for DNS search
        087845363  cfg_rules.ini update
        526aea3e8  util: Improve re_expression defaults
        b78b508b1  responder: regexp cleanup

    Weblate (4):
        ba5439c0f  po: update translations
        80690213f  po: update translations
        7c5dd8783  po: update translations
        ede8c1392  po: update translations

    aborah (15):
        76c7fa463  Tests: make corresponding tests capture SSSD logs
        a5176f4d9  Tests: SSSD: `sssctl analyze` command shouldn't require 'root' privileged
        5021d2394  Tests: Fix minor error in root privilage test
        7a68ed1f6  Tests: Fix ipa tests wrong ipa_client_ip
        13d420ca7  Tests: Fix test test_0017_filesldap
        3dfc82a05  Tests: Fix subidranges test
        66687d8c2  Tests: Port bz785908 and bz785898
        173d0867f  Tests: Port Thread issue can cause the application to not get any identity information bz847043
        97c671e4a  Tests: Port automount bash tests to pytest
        cc0545b4e  Tests: Port Bash Password Policy to pytest
        c6db359fa  Tests: Fix restore work for ipa test
        b3c681a7b  Tests: Port bash inmemory_cache test suit to pytest
        9c17615a7  Tests: don't fail if chattr file doesn't exist
        08711256a  Tests: Add missing package
        eb4941541  Tests: Add support for ldapi:// URLs

    aborah-sudo (6):
        6c0ae779f  Tests: port proxy_provider/rfc2307
        dab19a4d6  Tests: Removing tests from gating pipe line
        7c907a7c9  Tests: Removing tests from gating pipe line
        285f17031  Tests: fix test_bz1368467
        ad0a8c6a3  Tests: fix test_sssctl_local.py::Testsssctl::test_0002_bz1599207
        4a658e6cc  Tests: port proxy_provider/rfc2307bis

    answer9030 (2):
        0e25f0d19  Fixed pid wrapping in sss_cli_check_socket
        5c363bfbf  Fixed the problem of calling getpid() and lstat() twice in sss_cli_check_socket()

    bluikko (1):
        5c83deb5d  src/util/domain_info_utils.c: fix typo

    minfrin (6):
        9f2d8d691  Add support for ldapi:// URLs.
        f22134181  Align sockaddr_storage to sockaddr for updated API.
        91b701232  Ensure we touch sockaddr_len in the success case only.
        4ccd5b9ac  Do not set SO_KEEPALIVE on AF_UNIX.
        2d54cf5eb  Rename sdap_get_server_ip_str() to sdap_get_server_peer_str()
        e004595ae  Don't force TLS on if we're a unix domain socket.
