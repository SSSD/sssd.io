SSSD 2.8.0 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* The new D-Bus function ``ListByAttr()`` allows the caller to look for users that have an attribute with a certain value. For performance reasons, it is recommended that the attribute is indexed both on the remote server and on the local cache. The sssctl tool now provides the cache-index command to help you manage indexes on the local cache.

New features
~~~~~~~~~~~~

* Introduced the dbus function ``org.freedesktop.sssd.infopipe.Users.ListByAttr(attr, value, limit)`` listing up to limit users matching the filter ``attr=value``.
* sssctl is now able to create, list and delete indexes on the local caches. Indexes are useful for the new D-Bus ``ListByAttr()`` function.
* sssctl is now able to read and set each component's debug level independently.

Important fixes
~~~~~~~~~~~~~~~

* `domains` option in `[sssd]` section can now be completely omitted if domains are enabled via `domains/enabled` option

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* New option ``core_dumpable`` to manage ``PR_SET_DUMPABLE`` flag of SSSD processes. Enabled by default.
* New option ``ldap_enumeration_refresh_offset`` to set the maximum period deviation between enumeration updates. Defaults to 30 seconds.
* New option ``subdomain_refresh_interval_offset`` to set the maximum period deviation when refreshing the subdomain list.
* New option ``dyndns_refresh_interval_offset`` to set the maximum period deviation when updating the client's DNS entry. Defaults to 0.
* New option ``refresh_expired_interval_offset`` to set the maximum period deviation when refreshing expired entries in background.
* New option ``ldap_purge_cache_offset`` to set the maximum time deviation between cache cleanups. Defaults to 0.
* Option ``ad_machine_account_password_renewal_opts`` now accepts an optional third part as the maximum deviation in the provided period (first part) and initial delay (second part). If the period and initial delay are provided but not the offset, the offset is assumed to be 0. If no part is provided, the default is 86400:750:300.
* override_homedir now recognizes the %h template which is replaced by the original home directory retrieved from the identity provider, but in lower case.

Tickets Fixed
-------------

* `#4646 <https://github.com/SSSD/sssd/issues/4646>`__ - Make sure periodical tasks use randomization
* `#4728 <https://github.com/SSSD/sssd/issues/4728>`__ - Invalidating initgroups memory cache by a single name does not work
* `#4930 <https://github.com/SSSD/sssd/issues/4930>`__ - [Security] Improve plain text password handling in code
* `#5120 <https://github.com/SSSD/sssd/issues/5120>`__ - Consider replacing the ``nss_`` prefix for SSSD internal functions and structures to avoid conflicts with external nss library
* `#5696 <https://github.com/SSSD/sssd/issues/5696>`__ - Set _SSS_LOOPS conditionally at monitor startup
* `#6019 <https://github.com/SSSD/sssd/issues/6019>`__ - Need a means to report current debug level settings
* `#6020 <https://github.com/SSSD/sssd/issues/6020>`__ - [RFE] provide dbus method to find users by attr
* `#6146 <https://github.com/SSSD/sssd/issues/6146>`__ - oidc_child issues found in FreeIPA idp testing
* `#6210 <https://github.com/SSSD/sssd/issues/6210>`__ - RFE: Add an option to sssd config to convert home directories to lowercase (or add a new template for the ``override_homedir`` option)
* `#6220 <https://github.com/SSSD/sssd/issues/6220>`__ - [RFE] SSSD does not support  to change the user’s password when option ldap_pwd_policy equals to shadow in sssd.conf file
* `#6285 <https://github.com/SSSD/sssd/issues/6285>`__ - Refresh the well-know SID table
* `#6306 <https://github.com/SSSD/sssd/issues/6306>`__ - does not support MIT krb5 1.20
* `#6331 <https://github.com/SSSD/sssd/issues/6331>`__ - Freeipa nightly test failure when calling sssctl domain-status ipa.test -o
* `#6342 <https://github.com/SSSD/sssd/issues/6342>`__ - [D-Bus] ListByName() and ListByDomainAndname() return an empty list when used on the "files" provider
* `#6352 <https://github.com/SSSD/sssd/issues/6352>`__ - Use negative cache better and domain checks for lookup by SIDs
* `#6354 <https://github.com/SSSD/sssd/issues/6354>`__ - SUDO: Timezone issues with sudoNotBefore and sudoNotAfter
* `#6355 <https://github.com/SSSD/sssd/issues/6355>`__ - Cannot SSH with AD user to ipa-client (`krb5_validate` and `pac_check` settings conflict)

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.7.0..2.8.0

    Alejandro López (21):
        886ff516c  sssctl: free one malloc-allocated variable.
        97cffab3e  sss_tools: More flexible sss_tool_popt_ex()
        a809db922  sbus: Getter for the debug_level property
        e82135eb5  sbus: Setter for the debug_level property.
        e7974472e  sssctl: Get and set per-component debug-level
        34528ef2e  NSS: Replace the ``nss_`` prefix for SSSD internal functions
        fc3797ab7  NSS: Removed the unused function sss_nss_setnetgrent_recv()
        d415f354c  NSS: Removed the unused function sss_nss_protocol_fill_name_list()
        9cddeb8ba  Config: Add the %h template for the 'override_homedir' option
        7b34401b1  AD: Fixed a wrong index.
        35c35de42  PTasks: Make sure periodical tasks use randomization
        e40b9e929  Monitor: Set _SSS_LOOPS conditionally at monitor startup
        c2ae062d1  Tests: make test_kcm_renewals immune to LC_TIME
        73ba58a82  Responders: Remove unused argument
        5e032bbd9  sssctl: Fix malformed localizable string
        f4f28ac03  sssctl: Add an argument's missing description
        3618b2957  Tests: Minor improvement to the Multihost RST files
        830296c20  SIDs: Update the well-known SID tables
        f418e940c  D-Bus: Do not use timestamp optimization on "files" provider.
        3e5251bf2  sssctl: Management of indexes on cache DBs.
        acfe3b292  DBUS: Add ListByAttr(attr, filter, limit)

    Alexey Tikhonov (33):
        a2517ef85  SDAP: got rid of unused function argument
        4b8d781fa  SDAP: got rid of unsused state member
        cabc6cee7  SDAP: sdap_get_generic_send(): fix mem leak
        386c6d3ea  SPEC: drop sssd-ipa dependency on sssd-idp
        7b1033d10  sssctl: fixed log message
        a90ef949e  SDAP: sdap_nested_group_deref_direct_process(): store 'state->members' in a hash table to reduce computational complexity during "new member" check.
        1e142041e  TESTS: new case to test ad_gpo_parse_ini_file()
        37d2a1842  GPO: make ad_gpo_parse_ini_file() to accept full path
        1ed59fb6e  PAM P11: fixed mistype in a log message
        f1195229e  PAM P11: fixed minor mem-leak
        5433961b9  PAM: user feedback when login fails due to blocked PIN
        94352a9fb  New option for system hardening.
        27f35f029  CLIENT: use thread local storage for socket to avoid the need for a lock.
        ffec99930  SSS_CLIENT: mem-cache: fixed missing error code
        ef26371ab  SSS_CLIENT: got rid of code duplication
        43c6bf31c  TESTS: test_memory_cache: execute NSS functions in teardown to force sss_client libs to realize mem-cache files were deleted
        98f2f9f58  confdb: supress false positive warning: src/confdb/confdb.c:260:10: warning[-Wanalyzer-use-of-uninitialized-value]: use of uninitialized value 'secdn'
        ad7d1de9d  NSS MC: deleted misleading comment
        1690ae1ca  NSS MS: trivial simplification
        7abc9cfaf  NSS: MC: no need to convert name to output format.
        cceb136f2  NSS: fix initgroups store key (one of)
        810d92209  NSS: mem-cache: don't update domains other than the one where an entry was found.
        473752e26  RESPONDER: fixed condition in responder_idle_handler()
        0f3a761ed  CLIENT:MC: store context mutex outside of context as it should survive context destruction / re-initialization
        c6226c298  Makefile: remove unneeded dependency
        b98bcf28c  DB: upgrades aren't errors
        9aff9c531  CFG: domain ranges overlap requires attention
        68042d72a  RESPONDER: add missing \n
        579cc0b26  CLIENT:MC: -1 is more appropriate initial value for fd
        4ac93d9c5  CLIENT:MC: pointer to the context mutex shouldn't be touched
        1a6f67c92  CLIENT: fix client fd leak
        69fd828c1  CLIENT: fix thread unsafe acces to get*ent structs.
        d07dee78f  UTILS: change of log level isn't an error

    Anton Bobrov (1):
        0198f64ce  SUDO: Fix timezone issues with sudoNotBefore and sudoNotAfter

    Anuj Borah (11):
        da1d8eb4e  Tests: Fix ns_account test with sleep time
        72a403e92  Tests: Fix sss_analyzer tests
        e254ba8fc  Tests: Enabling ssctl_ldap test cases
        91969611f  Tests: Fix ns_account test with clear_sssd_cache
        bb4e054cf  Tests: port proxy_provider/misc
        fdc89c740  Tests: Add automation for bz 2056035
        19e474527  Tests: sssd runs out of proxy child slots and doesn't clear the counter for Active requests
        06d007fc9  Tests: avoid interlocking among threads that use `libsss_nss_idmap` API
        0a9e0c11a  Tests: Fix test_avoid_interlocking_among_threads
        cec7e8b7a  Tests: Fix test cases for signoff CI
        2dc5bc1b3  Tests: port proxy_provider/netgroup

    Dan Lavu (1):
        3f7ccfbd7  TEST: Fixing multidomain testcase bz2077893

    David Mulder (1):
        d4a1b71bd  Fix sdap_access_host No matching host rule found

    Iker Pedrosa (11):
        ecc8aa714  CI: update flake8 action reference
        e83e10652  p11_child: enable more than one CRL PEM file
        dfadb7da4  ad: prepend GPO_CACHE_PATH in caller function
        678146348  CI: flake8 move target to pull_request_target
        5c3d60907  CI: update actions version
        242fb3f9e  Revert "CI: flake8 move target to pull_request_target"
        2156e3780  CI: update python dependencies to version 3
        a8fc21c29  CI: build debian without python 2 bindings
        f25ab6d73  Fix E226 reported by flake8
        ba628d184  version.m4: update version to 2.8.0
        b96077c5d  sssctl: fix memory management with new POPT

    Jakub Vavra (25):
        50a6f23d7  Tests: Set FIPS:AD-SUPPORT crypto-policy for AD integration
        fd90c0d61  Tests: Fix/finish Sasl authid tests, minor tweak to hostname test.
        b207d1de9  Fix some flake 8 violations
        a7faea3e2  Tests: Add a test for bz2026799 bz2070138
        89191dd13  Tests: Extend test to cover bz2098615.
        f03768e52  Tests: Add oddjob fixture to enable working homes in basic tests.
        5f31118e9  Tests: Update auth_from_client to allow both short and full user names.
        24d35a161  Tests: remove python paramiko library from tests.
        6c16b4bf4  Tests: Remove SSHClient from ipa/conftest.py
        d38461b1e  Tests: Remove paramiko/SSHClient from utils.py.
        a163a63e0  Tests: Code review fixes for paramiko removal.
        f9d365863  Tests: Add pexpect to requirements.
        fb712c62f  Tests: Fix issue in the test test_0002_ad_parameters_junk_domain.
        d0b01cf2e  Tests: Rewrite autofs_ad_schema from direct ldap access to powershell.
        e8004792f  Tests: Modify sambaTools to lazy initialize ldap AD connection.
        8a17029a2  Tests: Add a fixture add_etc_host_records for Testcifs to solve name resolution issue.
        6e8701a61  Tests: Re-implement reset_machine_password using powershell instead of direct ldap access.
        d6743c33d  Tests: Update failure message for nismap manipulation.
        ccc878609  Tests: Fix rid computation for windows 2012.
        4360fb3d3  Tests: Extend info functions to handle line breaks.
        b3150506f  Tests: Modify ad schema tests for compatibility with windows 2012.
        6fe83c771  Tests: Skip TestBugzillaAutomation::test_0016_forceLDAPS on Windows 2012
        77f22429b  Tests: Port AD Login Attributes suite from bash.
        6f7f7237d  Tests: Refactor code to reduce number of called commands via ssh.
        3c9935449  Tests: Add ADOperation methods for sudorules, update fixture sudorules

    Justin Stephenson (14):
        3d8622031  Analyzer: Fix escaping raw fstring
        96a1dce80  CACHE_REQ: Fix hybrid lookup log spamming
        5e9d72f23  Fix new pycodestyle E275 requirement
        4e1ce1c12  SSSCTL: Allow analyzer to work without SSSD setup
        46b53b231  Tests: Add missing URI for device restriction
        b4aa4f126  CI: pycodestyle fixes evident on centos8 stream
        ad4b3aa95  RESPONDER: Fix client ID tracking
        5ef7435f2  Analyzer: support parallel requests parsing
        794fd130e  MAN: Add note about AD Group types
        6bf93c27c  CI: Remove pep8 from contrib/ci/run
        a915531fa  CI: Remove make check from contrib/ci/run
        ad49db495  CI: Remove make distcheck from contrib/ci/run
        b274f359a  CI: Remove coverage builds from contrib/ci/run
        a2417753d  MAN: Remove duplicate dns options

    Madhuri Upadhye (7):
        8edb287af  Tests: ipa: Add automation of BZ1859751
        ba5d4708b  Tests: Document: Document to run the tests using multihost config.
        a6566e1c5  Tests: Document: Setup python virtual environment to run pytest.
        f7c509801  Test: ipa: remove useless fixture call
        db05816a0  common: Install krb5-pkinit package
        556649de7  Tests: alltests/test_services.py: Port the failing test cases in pytest
        72246c97a  Tests: ipa: Add krb5-pkinit package to install

    Paul Donohue (9):
        0acb80a70  LDAP: Add an idle connection timeout
        baab4dbc8  Minor formatting and typo fixes (no functional changes)
        5f05aa695  LDAP: Reduce idle timer reschedule frequency
        3cb870475  Add ldap_connection_idle_timeout to subdomain_inherit
        e46295f8d  LDAP: Allow group rename with non-identical attributes
        4ded61f8e  LDAP: Document interaction between ldap_connection_expire_timeout and ldap_opt_timeout
        74be536fa  AD: Ignore option inherit failure
        6e3d2d768  Split dp_option_inherit() into two functions
        068c9980e  Add LDAP timeout support to subdomain_inherit

    Pavel Březina (32):
        dff9ba783  ci: switch to write-file-action
        460d02d12  ci: disable Jenkins jobs
        1eec0aae2  ci: enable ci for sssd-2-7
        950a77d5b  ci: fix syntax for flake8 job
        0a8d8f9e9  ci: enable copr builds for CentOS Stream 8
        2b6349c3f  ci: fix syntax error in copr build
        4b8438593  configure: fix libkrad detection
        e4d75912a  cert: fix assignment discards _const_ qualifier from pointer target type
        ef014b8b2  ci: allow deprecated functions during build
        d550b5f60  man: add idp indicator
        9aad30711  pam_sss_gss: KRB5CCNAME may be NULL
        8270d4c98  readme: add status badges
        7126f664a  po: translate sssd_krb5_localauth_plugin.8.xml
        1a7b53ac2  pot: update pot files
        686786c65  sbus: ensure single new line at end of file
        d1aa1ab64  sbus: apply changes in codegen
        ab49bfd7e  tests: fix pep8 issues
        24de04dde  ci: switch to debian-latest
        dc0eec59f  ci: upload test-suite.log as an artifact
        9a33cb824  intgcheck: mark files provider tests as flaky
        003b94fb3  confdb: allow empty sssd/domains option
        0ae94c162  confdb: consider enabled option when expanding app domains
        c5933066e  confdb: log to syslog when no domains are configured
        fbdc213bf  tests: add domains enabled tests
        12d4b679d  pot: update translations
        c5dab4bcc  pot: update translations
        b5fbb2837  tests: fix missing new line at the eof: src/tests/multihost/requirements.txt
        7e286aff3  ci: fix copr builds
        c4a26ebe3  pot: update translations
        4937c08a3  intg: fix test_rename_incomplete_group_rdn_changed
        8e23ec892  ci: add final result to workflows
        59cd19706  pot: update translations

    Sergio Durigan Junior (1):
        d91a814c3  Initialize UID/GID when using popt in "main" functions

    Shridhar Gadekar (4):
        0c35ed53a  Tests:port rfc2307 username begin with a space
        27f481182  Test: Minor trival testcase doc-string changes of rfc2307
        b7c78b5cd  Tests: 2FA prompting setting
        41cc08642  Test: better default for IPA/AD re_expression

    Steeve Goveas (17):
        3f177aa37  TEST: Fix docstrings for successful polarion import
        b9094ee68  TEST: Update default debug levels expected in logs
        624ad523a  TEST: Add missing markers in pytest.ini
        45411d844  TEST: Implement time logging for the LDAP queries
        a45d58c56  TEST: Add test for memcache SID
        686b1c8ce  TEST: Update and sort ad pytest.ini
        abce8dbeb  TEST: Install iproute-tc for tc
        bff0a4a6a  TEST: Fix the indentation in doctrings
        e89d7e442  TEST: Update to search the start string for hostname
        952959525  TEST: Modify test to compare backtrace for same error
        d0fad4998  update the sequence number of tests
        e100afc37  TEST: sssctl analyze --logdir does not need sssd running
        2230107da  TEST: Remove duplicate 'SSS_PAM_AUTHENTICATE'
        a1f1398f6  TEST: Add new marker tier1_4
        c533d0901  TEST: Add status field in docstrings
        c7f959911  TEST: Add README.rst as index.rst is not rendered
        14f1bcdb1  Tests: Add doc for docstrings for test files and cases

    Sumit Bose (30):
        2591f8d75  spec: mention oidc_child in description
        bd0854316  sdap: move some functions from sysdb to sdap
        3af930e5b  sdap: rename functions copied from sysdb
        e88559fa8  sdap: replace sysdb_attrs_primary_name() with sdap_get_primary_name()
        e587572b4  sdap: move sysdb_attrs_primary_name() into sdap_get_primary_name()
        bb4e93015  sdap: make sdap_get_primary_name() aware of multi-valued RDNs
        dd1f4902b  sdap: removed unused dom parameter from sdap_get_primary_name()
        952b9bd71  sdap: add tests for sdap_get_primary_name
        97eabb7ed  proxy: lower child count even if there is an error
        67270a088  proxy: finish request if proxy_child is terminated
        4af071af6  data_provider: add dp_client_cancel_timeout()
        4950bc00b  proxy: remove DP client timeout handler
        71b14474b  ad: add fallback in ad_domain_info_send()
        2d52fffdb  ad: make new PAC buffers available
        e57ab1ea5  tests: add PAC upn_dns_info test
        a28f8a337  krb5: add krb5_check_pac option
        6970cb1bf  pac: apply new pac check options
        30dbecaa9  ad: enable the PAC responder implicitly for AD provider
        9c12e962e  monitor: add implicit_pac_responder option.
        4c7f730b8  localauth: improve localauth add man page
        55e93cf1c  pac: relax default for pac_check option
        9656516b9  names: only check sub-domains for regex match
        00e5f3306  conf: make libjose and libcurl required for oidc_child
        ce8174787  ldap: allow password changes with shadow pwd policy
        abd8966a0  BUILD: Accept krb5 1.20 for building the PAC plugin
        12d5c6344  oidc_child: escape scopes
        a4d4617ef  oidc_child: use client secret if available to get device code
        5ed767076  oidc_child: increase wait interval by 5s if 'slow_down' is returned
        1a475e0c5  oidc_child: add --client-secret-stdin option
        f4dffaeae  krb5: respect krb5_validate for PAC checks

    Timotej Lazar (1):
        c104e250e  Analyzer: Only import sssd.source_* when needed

    Tomas Halman (4):
        1859523d5  SPEC: python egg info format change
        9d2d6c079  make: clean python new files
        70d5460b0  CACHE: implement ncache_add_fn for ncache SID
        5ea1ed27f  CACHE: implement *get_domain* for SID lookup

    Weblate (7):
        b24fd01b2  po: update translations
        8c0c59496  po: update translations
        8096abc51  Added translation using Weblate (Georgian)
        97b706ea6  po: update translations
        124cc3f11  po: update translations
        a6ed0ad76  po: update translations
        58adcbcf8  po: update translations

    Yuri Chornoivan (1):
        8ff6dee14  Fix minor typo

    aborah-sudo (2):
        1ed3baa2c  Tests: Fix multidomain tests
        35a4ebf03  Tests: Fix failure of SSSD pam module accepts usernames with leading spaces

    roy214 (3):
        f68d4e848  COMPONENT: /src/util/server.c
        17c3a1242  COMPONENT: sdap_handle_id_collision_for_incomplete_groups
        3c6bfc2d4  COMPONENT: domain_info_utils.c
