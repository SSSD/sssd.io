SSSD 1.13.2 Release Notes
=========================

Highlights
----------

-  This is primarily a bugfix release, with minor features added to the local overrides feature
-  The ``sss_override`` tool gained new ``user-show``, ``user-find``, ``group-show`` and ``group-find`` commands
-  The PAM responder was crashing if PAM_USER was set to an empty string. This bug was fixed
-  The ``sssd_be`` process could crash when looking up groups in setups with IPA-AD trusts that use POSIX attributes but do not replicate them to the Global Catalog
-  A socket leak in case SSSD couldn't establish a connection to an LDAP server was fixed
-  SSSD's memory cache now behaves better when used by long-running applications such as system daemons and the administrator invalidates the cache
-  The SSSDConfig Python API no longer throws an exception when config_file_version is missing
-  The InfoPipe D-Bus interface is able to retrieve user groups correctly if the user is a member of non-POSIX groups like ipausers as well
-  Lookups by certificate now work correctly in multi-domain environment
-  The lookup of POSIX attributes after startup was relaxed to only check attribute presence, not validity. The POSIX check was also made less verbose.
-  A bug when looking up a subdomain user by UPN users was fixed

Packaging Changes
-----------------

-  The memory cache for initgroups results was previously not packaged. This bug was fixed.
-  Python 2/3 packaging in the RPM specfile was improved

Tickets Fixed
-------------

-  `#3218 <https://github.com/SSSD/sssd/issues/3218>`_ warn if memcache_timeout is greater than entry_cache_timeout
-  `#3535 <https://github.com/SSSD/sssd/issues/3535>`_ Check chown_debug_file() usage
-  `#3714 <https://github.com/SSSD/sssd/issues/3714>`_ Consider also disabled domains when link_forest_roots() is called
-  `#3738 <https://github.com/SSSD/sssd/issues/3738>`_ extend PAM responder unit test
-  `#3747 <https://github.com/SSSD/sssd/issues/3747>`_ Contribute and DevelTips are duplicate
-  `#3767 <https://github.com/SSSD/sssd/issues/3767>`_ Long living applicantion can use removed memory cache.
-  `#3771 <https://github.com/SSSD/sssd/issues/3771>`_ responder_cache_req-tests failed
-  `#3777 <https://github.com/SSSD/sssd/issues/3777>`_ sss_override: add find and show commands
-  `#3800 <https://github.com/SSSD/sssd/issues/3800>`_ sbus_codegen_tests leaves a process running
-  `#3820 <https://github.com/SSSD/sssd/issues/3820>`_ Review and update wiki pages for 1.13.2
-  `#3827 <https://github.com/SSSD/sssd/issues/3827>`_ Create a wiki page that lists security-sensitive options
-  `#3833 <https://github.com/SSSD/sssd/issues/3833>`_ SSSD is not closing sockets properly
-  `#3841 <https://github.com/SSSD/sssd/issues/3841>`_ Relax POSIX check
-  `#3843 <https://github.com/SSSD/sssd/issues/3843>`_ sss_override segfaults when accidentally adding --help flag to some commands
-  `#3845 <https://github.com/SSSD/sssd/issues/3845>`_ Size limit exceeded too loud during POSIX check
-  `#3848 <https://github.com/SSSD/sssd/issues/3848>`_ CI: configure script failed on CentOS {6,7}
-  `#3851 <https://github.com/SSSD/sssd/issues/3851>`_ sssd_be crashed
-  `#3852 <https://github.com/SSSD/sssd/issues/3852>`_ PAM responder crashed if user was not set
-  `#3855 <https://github.com/SSSD/sssd/issues/3855>`_ avoid symlinks witih python modules
-  `#3860 <https://github.com/SSSD/sssd/issues/3860>`_ CI: test_ipa_subdomains_server failed on rhel6 + --coverage (FAIL: test_ipa_subdom_server)
-  `#3867 <https://github.com/SSSD/sssd/issues/3867>`_ sss_override: memory violation
-  `#3868 <https://github.com/SSSD/sssd/issues/3868>`_ bug in UPN lookups for subdomain users
-  `#3874 <https://github.com/SSSD/sssd/issues/3874>`_ local overrides: don't contact server with overriden name/id
-  `#3878 <https://github.com/SSSD/sssd/issues/3878>`_ REGRESSION: ipa-client-automout failed
-  `#3902 <https://github.com/SSSD/sssd/issues/3902>`_ sssd crashes if non-UTF-8 locale is used
-  `#3904 <https://github.com/SSSD/sssd/issues/3904>`_ IFP: ifp_users_user_get_groups doesn't handle non-POSIX groups


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_13_1..sssd-1_13_2

    Dan Lavu (1):
        7f6f615e8  sss_override: Add restart requirements to man page

    Jakub Hrozek (10):
        6491a24eb  Bump the version for the 1.13.2 development
        15a4b34cc  AD: Provide common connection list construction functions
        f1742784d  AD: Consolidate connection list construction on ad_common.c
        e9ccb2a7e  tests: Fix compilation warning
        4f8ed159b  tools: Don't shadow 'exit'
        39cfcfc26  IFP: Skip non-POSIX groups properly
        b51ed15a7  DP: Drop dp_pam_err_to_string
        518c003f3  DP: Check callback messages for valid UTF-8
        620b2adf7  sbus: Check string arguments for valid UTF-8 strings
        185200440  Updating translations for the 1.13.2 release

    Lukas Slebodnik (33):
        09365a02c  CI: Fix configure script arguments for CentOS
        cf37196dc  CI: Don't depend on user input with apt-get
        900638409  CI: Add missing dependency for debian
        cccbf6f5b  CI: Run integration tests on debian testing
        a164c1fa7  BUILD: Link just libsss_crypto with crypto libraries
        2dcf0c023  BUILD: Link crypto_tests with existing library
        77f801a32  BUILD: Remove unused variable TEST_MOCK_OBJ
        19181db61  BUILD: Avoid symlinks with python modules
        69612bc5d  SSSDConfigTest: Try load saved config
        b1c676761  SSSDConfigTest: Test real config without config_file_version
        36f92c5a7  intg_tests: Fix PEP8 warnings
        3dd118ee8  BUILD: Accept krb5 1.14 for building the PAC plugin
        807df8db5  BUILD: Fix detection of pthread with strict CFLAGS
        85046f9e1  BUILD: Fix doc directory for sss_simpleifp
        db2fdba6f  LDAP: Fix leak of file descriptors
        1c231bad0  CI: Workaroung for code coverage with old gcc
        9dffda361  cache_req: Fix warning -Wshadow
        6eb4f6e8d  SBUS: Fix warnings -Wshadow
        8539951ec  TESTS: Fix warnings -Wshadow
        d68024ffd  INIT: Drop syslog.target from service file
        0ff0d8604  sbus_codegen_tests: Suppress warning Wmaybe-uninitialized
        1779ef8bb  DP_PTASK: Fix warning may be used uninitialized
        d3d82089f  UTIL: Fix memory leak in switch_creds
        4a7dbc19e  TESTS: Initialize leak check
        cd60cf669  TESTS: Check return value of check_leaks_pop
        157a050cc  TESTS: Make check_leaks static function
        1c0c6e910  TESTS: Add warning for unused result of leak check functions
        01c888be3  sss_client: Fix underflow of active_threads
        e360fa6e9  sssd_client: Do not use removed memory cache
        87af3a1e5  test_memory_cache: Test removing mc without invalidation
        c54c09744  Revert "intg: Invalidate memory cache before removing files"
        fd311cdf3  CONFIGURE: Bump AM_GNU_GETTEXT_VERSION
        782ea07cd  test_sysdb_subdomains: Do not use assignment in assertions

    Michal Židek (7):
        a2363aa59  SSSDConfig: Do not raise exception if config_file_version is missing
        0c38ebe30  spec: Missing initgroups mmap file
        2a385185e  util: Update get_next_domain's interface
        4a3153e8b  tests: Add get_next_domain_flags test
        d78a21bb5  sysdb: Include disabled domains in link_forest_roots
        3dc864a93  sysdb: Use get_next_domain instead of dom->next
        5b8f64fea  Refactor some conditions

    Nikolai Kondrashov (13):
        6a29264e8  CI: Update reason blocking move to DNF
        4ed2835d7  CI: Exclude whitespace_test from Valgrind checks
        b4a390bc2  intg: Get base DN from LDAP connection object
        0257cd959  intg: Add support for specifying all user attrs
        d11def4bd  intg: Split LDAP test fixtures for flexibility
        0b29ccaee  intg: Reduce sssd.conf duplication in test_ldap.py
        cfb069fcf  intg: Fix RFC2307bis group member creation
        e6aa16d7b  intg: Do not use non-existent pre-increment
        38a66876d  CI: Do not skip tests not checked with Valgrind
        86be90e1e  CI: Handle dashes in valgrind-condense
        7e365b932  intg: Fix all PEP8 issues
        d15c3b220  CI: Enforce coverage make check failures
        3ab0400da  intg: Add more LDAP tests

    Pavel Březina (23):
        4d5e7e548  sss tools: improve option handling
        72745686b  sbus codegen tests: free ctx
        ae3896a12  cache_req: provide extra flag for oob request
        f04ead531  cache_req: add support for UPN
        44415c5a8  cache_req tests: reduce code duplication
        6bb2a0133  cache_req: remove raw_name and do not touch orig_name
        f3ea9ea32  sss_override: fix comment describing format
        d4a746b6a  sss_override: explicitly set ret = EOK
        81b92281b  sss_override: steal msgs string to objs
        2a5c268f6  nss: send original name and id with local views if possible
        6e3fa0324  sudo: search with view even if user is found
        329ea3541  sudo: send original name and id with local views if possible
        fc47b2026  sss_tools: always show common and help options
        94b98c264  sss_override: fix exporting multiple domains
        c85bfee21  sss_override: add user-find
        649075396  sss_override: add group-find
        81f29b0c7  sss_override: add user-show
        e573320d8  sss_override: add group-show
        21ad6bc0e  sss_override: do not free ldb_dn in get_object_dn()
        5b2b68b09  sss_override: use more generic help text
        db5a92be1  sss_tools: do not allow unexpected free argument
        ac7b15dac  BE: Add IFP to known clients
        a4b0ae112  AD: remove annoying debug message

    Pavel Reichl (12):
        1e8721947  AD: add debug messages for netlogon get info
        3fb1ee96f  confdb: warn if memcache_timeout > than entry_cache
        cc04876ec  SDAP: Relax POSIX check
        fed99d90d  SDAP: optional warning - sizelimit exceeded in POSIX check
        99ac13e26  SDAP: allow_paging in sdap_get_generic_ext_send()
        a46599bab  SDAP: change type of attrsonly in sdap_get_generic_ext_state
        86ec0fdda  SDAP: pass params in sdap_get_and_parse_generic_send
        5a84d0692  sss_override: amend man page - overrides do not stack
        59d20aab8  sss_override: Removed overrides might be in memcache
        b0bdc28de  pam-srv-tests: split pam_test_setup() so it can be reused
        f0c4ca6e3  pam-srv-tests: Add UT for cached 'online' auth.
        07c230554  intg: Add test for user and group local overrides

    Petr Cech (9):
        6e2822b15  DEBUG: Preventing chown_debug_file if journald on
        73519a952  TEST: Add test_user_by_recent_filter_valid
        b6dd72c59  TEST: Refactor of test_responder_cache_req.c
        3d135f299  TEST: Refactor of test_responder_cache_req.c
        b87363f82  TEST: Add common function are_values_in_array()
        a6c3dba7e  TEST: Add test_users_by_recent_filter_valid
        56c7cb868  TEST: Add test_group_by_recent_filter_valid
        f4c7c9268  TEST: Refactor of test_responder_cache_req.c
        87a8f263e  TEST: Add test_groups_by_recent_filter_valid

    Stephen Gallagher (2):
        51ee1fb07  LDAP: Inform about small range size
        6f6622cfe  Monitor: Show service pings at debug level 8

    Sumit Bose (5):
        ba9d5c045  PAM: only allow missing user name for certificate authentication
        055248cf2  fix ldb_search usage
        f2c3994c6  fix upn cache_req for sub-domain users
        b1b0abe62  nss: fix UPN lookups for sub-domain users
        ad259029b  cache_req: check all domains for lookups by certificate
