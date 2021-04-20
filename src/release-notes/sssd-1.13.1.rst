SSSD 1.13.1 Release Notes
=========================

Highlights
----------

-  Initial support for Smart Card authentication was added. The feature can be activated with the new ``pam_cert_auth`` option
-  The PAM prompting was enhanced so that when Two-Factor Authentication is used, both factors (password and token) can be entered separately on separate prompts. At the same time, only the long-term password is cached, so offline access would still work using the long term password
-  A new command line tool ``sss_override`` is present in this release. The tools allows to override attributes on the SSSD side. It's helpful in environment where e.g. some hosts need to have a different view of POSIX attributes than others. Please note that the overrides are stored in the cache as well, so removing the cache will also remove the overrides
-  New methods were added to the SSSD D-Bus interface. Notably support for looking up a user by certificate and looking up multiple users using a wildcard was added. Please see the interface introspection or the design pages for full details
-  Several enhancements to the dynamic DNS update code. Notably, clients that update multiple interfaces work better with this release
-  This release supports authenticating againt a KDC proxy
-  The fail over code was enhanced so that if a trusted domain is not reachable, only that domain will be marked as inactive but the backed would stay in online mode
-  Several fixes to the GPO access control code are present

Packaging Changes
-----------------

-  The Smart Card authentication feature requires a helper process ``p11_child`` that needs to be marked as setgid if SSSD needs to be able to. Please note the ``p11_child`` requires the NSS crypto library at the moment
-  The ``sss_override`` tool was added along with its own manpage
-  The upstream RPM can now build on RHEL/CentOS 6.7

Documentation Changes
---------------------

-  The ``config_file_version`` configuration option now defaults to 2. As an effect, this option doesn't have to be set anymore unless the config file format is changed again by SSSD upstream
-  It is now possible to specify a comma-separated list of interfaces in the ``dyndns_iface`` option
-  The InfoPipe responder and the LDAP provider gained a new option ``wildcard_lookup`` that specifies an upper limit on the number of entries that can be returned with a wildcard lookup
-  A new option ``dyndns_server`` was added. This option allows to attempt a fallback DNS update against a specific DNS server. Please note this option only works as a fallback, the first attempt will always be performed against autodiscovered servers.
-  The PAM responder gained a new option ``ca_db`` that allows the storage of trusted CA certificates to be specified
-  The time the ``p11_child`` is allowed to operate can be specified using a new option ``p11_child_timeout``

Tickets Fixed
-------------

-  `#1588 <https://github.com/SSSD/sssd/issues/1588>`_ [RFE] Support for smart cards
-  `#2739 <https://github.com/SSSD/sssd/issues/2739>`_ sssd: incorrect checks on length values during packet decoding
-  `#2968 <https://github.com/SSSD/sssd/issues/2968>`_ [RFE] Start the dynamic DNS update after the SSSD has been setup for the first time
-  `#3036 <https://github.com/SSSD/sssd/issues/3036>`_ Complain loudly if backend doesn't start due to missing or invalid keytab
-  `#3317 <https://github.com/SSSD/sssd/issues/3317>`_ nested netgroups do not work in IPA provider
-  `#3325 <https://github.com/SSSD/sssd/issues/3325>`_ test dyndns failed.
-  `#3377 <https://github.com/SSSD/sssd/issues/3377>`_ Investigate using the krb5 responder for driving the PAM conversation with OTPs
-  `#3505 <https://github.com/SSSD/sssd/issues/3505>`_ Pass error messages via the extdom plugin
-  `#3537 <https://github.com/SSSD/sssd/issues/3537>`_ [RFE]Allow sssd to add a new option that would specify which server to update DNS with
-  `#3591 <https://github.com/SSSD/sssd/issues/3591>`_ RFE: Support multiple interfaces with the dyndns_iface option
-  `#3595 <https://github.com/SSSD/sssd/issues/3595>`_ RFE: Add support for wildcard-based cache updates
-  `#3600 <https://github.com/SSSD/sssd/issues/3600>`_ Add dualstack and multihomed support
-  `#3603 <https://github.com/SSSD/sssd/issues/3603>`_ Too much logging
-  `#3620 <https://github.com/SSSD/sssd/issues/3620>`_ TRACKER: Support one-way trusts for IPA
-  `#3622 <https://github.com/SSSD/sssd/issues/3622>`_ Re-check memcache after acquiring the lock in the client code
-  `#3625 <https://github.com/SSSD/sssd/issues/3625>`_ RFE: Support client-side overrides
-  `#3638 <https://github.com/SSSD/sssd/issues/3638>`_ Add index for 'objectSIDString' and maybe to other cache attributes
-  `#3678 <https://github.com/SSSD/sssd/issues/3678>`_ RFE: Don't mark the main domain as offline if SSSD can't connect to a subdomain
-  `#3680 <https://github.com/SSSD/sssd/issues/3680>`_ RFE: Detect re-established trusts in the IPA subdomain code
-  `#3693 <https://github.com/SSSD/sssd/issues/3693>`_ KDC proxy not working with SSSD krb5_use_kdcinfo enabled
-  `#3717 <https://github.com/SSSD/sssd/issues/3717>`_ Group members are not turned into ghost entries when the user is purged from the SSSD cache
-  `#3723 <https://github.com/SSSD/sssd/issues/3723>`_ sudoOrder not honored as expected
-  `#3729 <https://github.com/SSSD/sssd/issues/3729>`_ Default to config_file_version=2
-  `#3732 <https://github.com/SSSD/sssd/issues/3732>`_ GPO: PAM system error returned for PAM_ACCT_MGMT and offline mode
-  `#3733 <https://github.com/SSSD/sssd/issues/3733>`_ GPO: Access denied due to using wrong sam_account_name
-  `#3740 <https://github.com/SSSD/sssd/issues/3740>`_ SSSDConfig: wrong return type returned on python3
-  `#3741 <https://github.com/SSSD/sssd/issues/3741>`_ krb5_child should always consider online state to allow use of MS-KKDC proxy
-  `#3749 <https://github.com/SSSD/sssd/issues/3749>`_ Logging messages from user point of view
-  `#3752 <https://github.com/SSSD/sssd/issues/3752>`_ [RFE] Provide interface for SSH to fetch user certificate
-  `#3753 <https://github.com/SSSD/sssd/issues/3753>`_ Initgroups memory cache does not work with fq names
-  `#3757 <https://github.com/SSSD/sssd/issues/3757>`_ Initgroups mmap cache needs update after db changes
-  `#3758 <https://github.com/SSSD/sssd/issues/3758>`_ well-known SID check is broken for NetBIOS prefixes
-  `#3759 <https://github.com/SSSD/sssd/issues/3759>`_ SSSD keytab validation check expects root ownership
-  `#3760 <https://github.com/SSSD/sssd/issues/3760>`_ IPA: returned unknown dp error code with disabled migration mode
-  `#3763 <https://github.com/SSSD/sssd/issues/3763>`_ Missing config options in gentoo init script
-  `#3764 <https://github.com/SSSD/sssd/issues/3764>`_ Could not resolve AD user from root domain
-  `#3765 <https://github.com/SSSD/sssd/issues/3765>`_ getgrgid for user's UID on a trust client prevents getpw\*
-  `#3766 <https://github.com/SSSD/sssd/issues/3766>`_ If AD site detection fails, not even ad_site override skipped
-  `#3770 <https://github.com/SSSD/sssd/issues/3770>`_ Do not send SSS_OTP if both factors were entered separately
-  `#3772 <https://github.com/SSSD/sssd/issues/3772>`_ searching SID by ID always checks all domains
-  `#3774 <https://github.com/SSSD/sssd/issues/3774>`_ Don't use deprecated libraries (libsystemd-\*)
-  `#3778 <https://github.com/SSSD/sssd/issues/3778>`_ sss_override: add import and export commands
-  `#3779 <https://github.com/SSSD/sssd/issues/3779>`_ Cannot build rpms from upstream spec file on rawhide
-  `#3783 <https://github.com/SSSD/sssd/issues/3783>`_ When certificate is added via user-add-cert, it cannot be looked up via org.freedesktop.sssd.infopipe.Users.FindByCertificate
-  `#3784 <https://github.com/SSSD/sssd/issues/3784>`_ memory cache can work intermittently
-  `#3785 <https://github.com/SSSD/sssd/issues/3785>`_ cleanup_groups should sanitize dn of groups
-  `#3787 <https://github.com/SSSD/sssd/issues/3787>`_ the PAM srv test often fails on RHEL-7
-  `#3789 <https://github.com/SSSD/sssd/issues/3789>`_ test_memory_cache failed in invalidation cache before stop
-  `#3790 <https://github.com/SSSD/sssd/issues/3790>`_ Fix crash in nss responder
-  `#3795 <https://github.com/SSSD/sssd/issues/3795>`_ Clear environment and set restrictive umask in p11_child
-  `#3798 <https://github.com/SSSD/sssd/issues/3798>`_ sss_override does not work correctly when 'use_fully_qualified_names = True'
-  `#3799 <https://github.com/SSSD/sssd/issues/3799>`_ sss_override contains an extra parameter --debug but is not listed in the man page or in the arguments help
-  `#3803 <https://github.com/SSSD/sssd/issues/3803>`_ [RFE] sssd: better feedback form constraint password change
-  `#3809 <https://github.com/SSSD/sssd/issues/3809>`_ Test 'test_id_cleanup_exp_group' failed
-  `#3813 <https://github.com/SSSD/sssd/issues/3813>`_ sssd cannot resolve user names containing backslash with ldap provider
-  `#3814 <https://github.com/SSSD/sssd/issues/3814>`_ Make p11_child timeout configurable
-  `#3818 <https://github.com/SSSD/sssd/issues/3818>`_ Fix memory leak in GPO
-  `#3823 <https://github.com/SSSD/sssd/issues/3823>`_ sss_override : The local override user is not found
-  `#3824 <https://github.com/SSSD/sssd/issues/3824>`_ REGRESSION: Dyndns soes not update reverse DNS records
-  `#3831 <https://github.com/SSSD/sssd/issues/3831>`_ sss_override --name doesn't work with RFC2307 and ghost users
-  `#3840 <https://github.com/SSSD/sssd/issues/3840>`_ unit tests do not link correctly on Debian
-  `#3844 <https://github.com/SSSD/sssd/issues/3844>`_ Memory leak / possible DoS with krb auth.

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_13_0..sssd-1_13_1

    Jakub Hrozek (52):
        585ea4eb0  Updating the version for 1.13.1 development
        429f8454a  tests: Move N_ELEMENTS definition to tests/common.h
        696c17580  SYSDB: Add functions to look up multiple entries including name and custom filter
        cdc44abdf  DP: Add DP_WILDCARD and SSS_DP_WILDCARD_USER/SSS_DP_WILDCARD_GROUP
        fd04b25ea  cache_req: Extend cache_req with wildcard lookups
        fa7921c82  UTIL: Add sss_filter_sanitize_ex
        2922461ea  LDAP: Fetch users and groups using wildcards
        f4e643ed7  LDAP: Add sdap_get_and_parse_generic_send
        5b2ca5cc0  LDAP: Use sdap_get_and_parse_generic_/_recv
        1f2fc55ec  LDAP: Add sdap_lookup_type enum
        b9e74a747  LDAP: Add the wildcard_limit option
        bdf32fbb3  IFP: Add wildcard requests
        f6a71ab5f  Use NSCD path in execl()
        61015cf52  KRB5: Use the right domain for case-sensitive flag
        146e024b3  IPA: Better debugging
        698601256  UTIL: Lower debug level in perform_checks()
        6ed964cf2  IPA: Handle sssd-owned keytabs when running as root
        6fe057efb  IPA: Remove MPG groups if getgrgid was called before getpw()
        32445affe  LDAP: use ldb_binary_encode when printing attribute values
        619e21ed9  IPA: Change the default of ldap_user_certificate to userCertificate;binary
        d95bcfe23  UTIL: Provide a common interface to safely create temporary files
        db5f9ab3f  IPA: Always re-fetch the keytab from the IPA server
        8145ab51b  DYNDNS: Add a new option dyndns_server
        13f30f69e  p11child: set restrictive umask and clear environment
        f5db13d44  KRB5: Use sss_unique file in krb5_child
        df07d54f8  KRB5: Use sss_unique_file when creating kdcinfo files
        51ae9cb4e  LDAP: Use sss_unique_filename in ldap_child
        84493af37  SSH: Use sss_unique_file_ex to create the known hosts file
        e61b0e41c  SYSDB: Index the objectSIDString attribute
        6c2a29a91  sbus: Initialize errno if constructing message fails and add debug messages
        9118a539a  sbus: Add a special error code for messages sent by the bus itself
        3954cd07d  GPO: Use sss_unique_file and close fd on failure
        63fb08573  SDAP: Remove unused function
        f0815f5df  KRB5: Don't error out reading a minimal krb5.conf
        b5825c74b  UTIL: Convert domain->disabled into tri-state with domain states
        99c5f2f6b  DP: Provide a way to mark subdomain as disabled and auto-enable it later with offline_timeout
        0561d532c  SDAP: Do not set is_offline if ignore_mark_offline is set
        7fc8692d4  AD: Only ignore errors from SDAP lookups if there's another connection to fallback to
        dd0a21738  KRB5: Offline operation with disabled domain
        64d4b1e5f  AD: Do not mark the whole back end as offline if subdomain lookup fails
        ece345a74  AD: Set ignore_mark_offline=false when resolving AD root domain
        201623520  IPA: Do not allow the AD lookup code to set backend as offline in server mode
        2ddacb721  BUILD: link dp tests with LDB directly to fix builds on Debian
        67625b1b4  LDAP: imposing sizelimit=1 for single-entry searches breaks overlapping domains
        cffe3defa  tests: Move named_domain from test_utils to common test code
        cf66c53e4  LDAP: Move sdap_create_search_base from ldap to sdap code
        fb83de069  LDAP: Filter out multiple entries when searching overlapping domains
        4c53f8b74  IPA: Change ipa_server_trust_add_send request to be reusable from ID code
        669ce24f8  FO: Add an API to reset all servers in a single service
        bc58e1cfe  FO: Also reset the server common data in addition to SRV
        42bd89dbe  IPA: Retry fetching keytab if IPA user lookup fails
        261cdde02  Updating translations for the 1.13.1 release

    Lukas Slebodnik (49):
        da17e4c19  KRB5: Return right data provider error code
        890ae77c5  Update few debug messages
        eabc1732e  intg: Invalidate memory cache before removing files
        b0ee27fd9  SPEC: Update spec file for krb5_local_auth_plugin
        2ab9822a7  SSSDConfig: Return correct types in python3
        872aa0d01  intg: Modernize 'except' clauses
        39b31427e  mmap_cache: Rename variables
        225dc6914  mmap_cache: "Override" functions for initgr mmap cache
        ea7839cec  mmap: Invalidate initgroups memory cache after any change
        ba847347c  sss_client: Update integrity check of records in mmap cache
        38b070198  intg_test: Add module for simulation of utility id
        a2c10cf31  intg_test: Add integration test for memory cache
        dda025870  NSS: Initgr memory cache should work with fq names
        cb8c24707  test_memory_cache: Add test for initgroups mc with fq names
        85fe1601d  SPEC: Workaround for build with rpm 4.13
        e693e9c67  KRB5: Do not try to remove missing ccache
        c3baf4d7c  test_memory_cache: Test mmap cache after initgroups
        089db891b  test_memory_cache: Test invalidation with sss_cache
        6c676de3f  krb5_utils-tests: Remove unused variables
        32c6db689  sss_cache: Wait a while for invalidation of mc by nss responder
        137d5dd0d  test_memory_cache: Fix few python issues
        b9901fe3d  NSS: Fix use after free
        90b8e2e47  NSS: Don't ignore backslash in usernames with ldap provider
        03a4bb070  intg_tests: Add regression test for 2163
        1116fbbf0  BUILD: Build libdlopen_test_providers.la as a dynamic library
        802909e59  BUILD: Speed up build of some tests
        af3a627a3  BUILD: Simplify build of simple_access_tests
        447d32b6f  CI: Set env variable for all tabs in screen
        b3074dca3  dyndns-tests: Simulate job in wrapped execv
        d71cd46ed  AUTOMAKE: Disable portability warnings
        50c9d542e  tests: Use unique name for TEST_PATH
        c106bfdf2  tests: Move test_dom_suite_setup to different module
        bee2f31ca  test_ipa_subdomains_server: Use unique dorectory for keytabs
        83788fb29  test_copy_keytab: Create keytabs in unique directory
        295c8e301  test_ad_common: Use unique directory for keytabs
        9c563db82  Revert "LDAP: end on ENOMEM"
        3d8b576bf  Partially revert "LDAP: sanitize group name when used in filter"
        6cb5bad3c  LDAP: Sanitize group dn before using in filter
        2cec08a31  test_ldap_id_cleanup: Fix coding style issues
        75889713a  DYNDNS: Return right error code in case of failure
        71493344f  BUILD: Simplify build of test_data_provider_be
        e3c06950b  BUILD: Remove unused variable CHECK_OBJ
        a801d42c4  BUILD: Do not build libsss_ad_common.la as library
        f3d84d2b6  BUILD: Remove unused variable SSSD_UTIL_OBJ
        d9378e644  CONFIGURE: Remove bashism
        afdc0179a  IFP: Suppress warning from static analyzer
        73ec8fdfd  BUILD: Link test_data_provider_be with -ldl
        40fa5c38d  sysdb-tests: Use valid base64 encoded certificate for search
        f182ede71  test_pam_srv: Run cert test only with NSS

    Michal Židek (13):
        c4fb8f55f  DEBUG: Add new debug category for fail over.
        9da121c08  pam: Incerease p11 child timeout
        06987186f  sdap_async: Use specific errmsg when available
        f02b62138  TESTS: ldap_id_cleanup timeouts
        9f0bffebd  sssd: incorrect checks on length values during packet decoding
        175613be0  CONFDB: Assume config file version 2 if missing
        3b1aa479b  Makefile.am: Add missing AM_CFLAGS
        b0d6d14b5  SYSDB: Add function to expire entry
        4d8f0f92e  cleanup task: Expire all memberof targets when removing user
        95b2c5177  CI: Add regression test for #2676
        60713f738  intg: Fix some PEP 8 violations
        d85be8ad4  PAM: Make p11_child timeout configurable
        ab3c0e05d  tests: Set p11_child_timeout to 30 in tests

    Nikolai Kondrashov (1):
        cbff3fcdc  TESTS: Add trailing whitespace test

    Pavel Březina (18):
        166a622bc  VIEWS TEST: add null-check
        a8d31510d  SYSDB: prepare for LOCAL view
        284937e6b  TOOLS: add common command framework
        b69cb1787  TOOLS: add sss_override for local overrides
        cbbd8ce52  AD: Use ad_site also when site search fails
        ef7de95fc  IFP: use default limit if provided is 0
        52e3ee5c5  sudo: use "higher value wins" when ordering rules
        4285cf181  sss_override: print input name if unable to parse it
        7eba58cfc  sss_override: support domains that require fqname
        a76f63544  TOOLS: add sss_colondb API
        5df5a6b85  sss_override: decompose code better
        23fb01bf6  sss_override: support import and export
        5e2ffb69d  sss_override: document --debug options
        4649f19ea  sss_override: support fqn in override name
        9571c9ba5  views: do not require overrideDN in grous when LOCAL view is set
        d5e26a3ec  views: fix two typos in debug messages
        87e0dcaff  views: allow ghost members for LOCAL view
        8ca1a503c  sss_override: remove -d from manpage

    Pavel Reichl (23):
        aa3fd6fde  DYNDNS: sss_iface_addr_list_get return ENOENT
        038b9ba28  DYNDNS: support mult. interfaces for dyndns_iface opt
        0a26e92fb  DYNDNS: special value '*' for dyndns_iface option
        1112e8449  TESTS: dyndns tests support AAAA addresses
        b0a8ed519  DYNDNS: support for dualstack
        4f68747b1  TESTS: fix compiler warnings
        4b1a46396  SDAP: rename SDAP_CACHE_PURGE_TIMEOUT
        afa6ac75f  IPA: Improve messages about failures
        7c3cc1ee2  DYNDNS: Don't use server cmd in nsupdate by default
        e4d6e9cca  DYNDNS: remove redundant talloc_steal()
        4f2a07c42  DYNDNS: remove zone command
        76604931b  DYNDNS: rename field of sdap_dyndns_update_state
        b42bf6c0c  DYNDNS: remove code duplication
        6fd530614  TESTS: UT for sss_iface_addr_list_as_str_list()
        e2e334b2f  LDAP: sanitize group name when used in filter
        4772d3f1f  LDAP: minor improvements in ldap id cleanup
        e0f2a7834  TESTS: fix fail in test_id_cleanup_exp_group
        f31a57321  LDAP: end on ENOMEM
        bfa5e3869  AD: send less logs to syslog
        2b490bc94  Remove trailing whitespace
        5dbdcc2c7  GPO: fix memory leak
        eeac17ebb  DDNS: execute nsupdate for single update of PTR rec
        101628a48  AD: inicialize root_domain_attrs field

    Petr Cech (6):
        cebf9d194  BUILD: Repair dependecies on deprecated libraries
        bdf422fde  TESTS: Removing part of responder_cache_req-tests
        11e8f3ecd  UTIL: Function 2string for enum sss_cli_command
        46e362869  UTIL: Fixing Makefile.am for util/sss_cli_cmd.h
        376eaf187  DATA_PROVIDER: BE_REQ as string in log message
        e6595222c  IPA PROVIDER: Resolve nested netgroup membership

    Robin McCorkell (1):
        e6b6719ec  man: List alternative schema defaults for LDAP AutoFS parameters

    Stephen Gallagher (1):
        7c18b65db  AD: Handle cases where no GPOs apply

    Sumit Bose (17):
        b1bea7c3d  test common: sss_dp_get_account_recv() fix assignment
        4f1897ad4  nss_check_name_of_well_known_sid() improve name splitting
        e1aed98d7  negcache: allow domain name for UID and GID
        c2cc00e8d  nss: use negative cache for sid-by-id requests
        b698a04b3  krb5: do not send SSS_OTP if two factors were used
        0d5bb3836  utils: add NSS version of cert utils
        45726939a  Add NSS version of p11_child
        35f3a213e  pack_message_v3: allow empty name
        10703cd55  authok: add support for Smart Card related authtokens
        a8d887323  PAM: add certificate support to PAM (pre-)auth requests
        5242964d2  pam_sss: add sc support
        4de84af23  ssh: generate public keys from certificate
        7bb9ba868  krb5 utils: add sss_krb5_realm_has_proxy()
        05ed6a29c  krb5: do not create kdcinfo file if proxy configuration exists
        67c68b563  krb5: assume online state if KDC proxy is configured
        560b624b3  GPO: use SDAP_SASL_AUTHID as samAccountName
        9a847b5d7  utils: make sss_krb5_get_primary() private

    Thomas Oulevey (1):
        b4c44ebb8  Fix memory leak in sssdpac_verify()

    Tyler Gates (1):
        cbe70d47d  CONTRIB: Gentoo daemon startup options as declared in conf.d/sssd

    Yuri Chornoivan (1):
        f91029dd8  Fix minor typos
