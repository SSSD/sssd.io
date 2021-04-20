SSSD 1.13.0 Release Notes
=========================

Highlights
----------

-  Support for separate prompts when using two-factor authentication was added
-  Added support for one-way trusts between an IPA and Active Directory environment. Please note that this SSSD functionality depends on IPA code that will be released in the IPA 4.2 version
-  The fast memory cache now also supports the initgroups operation.
-  The PAM responder is now capable of caching authentication for configurable period, which might reduce server load in cases where accounts authenticate very frequently. Please refer to the ``cached_auth_timeout`` option in the ``sssd.conf`` manual page.
-  The Active Directory provider has changed the default value of the ``ad_gpo_access_control`` option from ``permissive`` to ``enforcing``. As a consequence, the GPO access control now affects all clients that set ``access_provider`` to ``ad``. In order to restore the previous behaviour, set ``ad_gpo_access_control`` to ``permissive`` or use a different ``access_provider`` type.
-  Group Policy objects defined in a different AD domain that the computer object is defined in are now supported.
-  Credential caching and Offline authentication are also available when using two-factor authentication
-  Many enhancements to the InfoPipe D-Bus API. Notably, the SSSD users and groups are now exposed as first-class objects. The users and groups can also be marked as cached and would subsequently show up in the Introspection output
-  The DBus interface is now also able to look up User objects by certificate. This is a first part of work that will eventually allow smart-card authentication in SSSD.
-  The LDAP cleanup task is now disabled by default, unless enumeration is enabled. Please refer to the ``ldap_purge_cache_timeout`` option in case your environment requires the cleanup task
-  The Python bindings are now built for both Python2 and Python3
-  The LDAP bind timeout, StartTLS timeout and password change timeout are now configurable using the ``ldap_opt_timeout`` option

Packaging Changes
-----------------

-  A new directory ``/var/lib/sss/keytabs`` is present and owned by the ``sssd-ipa`` subpackage. The SSSD stores keytabs for one-way trust relationships in this directory. Downstreams should make sure that the directory is only readable to the user who runs the SSSD service.
-  Several packaging changes are present in this release to support the Python3 bindings, notably new ``python-sss`` and ``python-sss-murmur`` subpackages are introduced in upstream RPM packaging
-  All python bindings now have a Python3 and a Python2 version in the upstream RPM packaging scheme
-  The OpenSSL development library such as ``openssl-devel`` on RHEL/Fedora or Debian/Ubuntu ``libssl-dev`` is now required to support certificate operations
-  A new internal library ``libsss_cert.so`` is present in this release.
-  The fast initgroups memcache is represented by a new file ``/var/lib/sss/mc/initgroups``

Documentation Changes
---------------------

-  The ``ad_gpo_access_control`` option default has changed from ``permissive`` to ``enforcing``
-  The default value of ``ldap_purge_cache_timeout`` changed to 0, thus effectivelly disabling the cleanup task.
-  A new option ``cache_credentials_minimal_first_factor_length`` was added. This option sets constraints on the password length if One-Time passwords are used and credentials are to be cached. Please see the ``sssd.conf(5)`` man page for more details
-  The cached authentication is controlled by new option ``cached_auth_timeout``. By default the cached authentication is disabled.

Tickets Fixed
-------------

-  `#1939 <https://github.com/SSSD/sssd/issues/1939>`_ sssd should pass -d to nsupdate when running with high log level
-  `#2543 <https://github.com/SSSD/sssd/issues/2543>`_ Make the LDAP bind operation timeout configurable
-  `#3192 <https://github.com/SSSD/sssd/issues/3192>`_ [RFE] Expose listing calls over D-BUS
-  `#3266 <https://github.com/SSSD/sssd/issues/3266>`_ nsupdate stderr is not captured
-  `#3278 <https://github.com/SSSD/sssd/issues/3278>`_ The cleanup task has no DEBUG statements
-  `#3368 <https://github.com/SSSD/sssd/issues/3368>`_ SBUS: Flush the UID cache when we receive NameOwnerChanged
-  `#3380 <https://github.com/SSSD/sssd/issues/3380>`_ [RFE] Implement object caching on the bus
-  `#3381 <https://github.com/SSSD/sssd/issues/3381>`_ IFP: support multiple interfaces for object
-  `#3582 <https://github.com/SSSD/sssd/issues/3582>`_ SSSD does not update Dynamic DNS records if the IPA domain differs from machine hostname's domain
-  `#3611 <https://github.com/SSSD/sssd/issues/3611>`_ In ipa-ad trust, with 'default_domain_suffix' set to AD domain, IPA user are not able to log unless use_fully_qualified_names is set
-  `#3616 <https://github.com/SSSD/sssd/issues/3616>`_ SSSD should be able to build python2 and python3 bindings in a one build
-  `#3624 <https://github.com/SSSD/sssd/issues/3624>`_ [RFE] Homedir is always overwritten with subdomain_homedir value in server mode
-  `#3634 <https://github.com/SSSD/sssd/issues/3634>`_ Does sssd-ad use the most suitable attribute for group name?
-  `#3637 <https://github.com/SSSD/sssd/issues/3637>`_ Add a way to lookup users based on CAC identity certificates
-  `#3644 <https://github.com/SSSD/sssd/issues/3644>`_ Make SSSD's HBAC validation more permissive if deny rules are not used
-  `#3650 <https://github.com/SSSD/sssd/issues/3650>`_ [bug] sssd always appends default_domain_suffix when checking for host keys
-  `#3659 <https://github.com/SSSD/sssd/issues/3659>`_ Man sssd-ad(5) lists Group Policy Management Editor naming for some policies but not for all
-  `#3661 <https://github.com/SSSD/sssd/issues/3661>`_ id_provider=proxy with auth_provider=ldap does not work reliably
-  `#3666 <https://github.com/SSSD/sssd/issues/3666>`_ Sudo responder does not respect filter_users and filter_groups
-  `#3668 <https://github.com/SSSD/sssd/issues/3668>`_ Disable the cleanup task by default
-  `#3677 <https://github.com/SSSD/sssd/issues/3677>`_ RFE: Fetch keytabs for one-way trusts in IPA subdomain code
-  `#3679 <https://github.com/SSSD/sssd/issues/3679>`_ RFE: Change ad_id_ctx instantiation in the IPA subdomain code to support one-way trusts
-  `#3686 <https://github.com/SSSD/sssd/issues/3686>`_ [RFE] Support GPOs from different domain controllers
-  `#3702 <https://github.com/SSSD/sssd/issues/3702>`_ RFE: Change AD GPO default to enforcing
-  `#3707 <https://github.com/SSSD/sssd/issues/3707>`_ sssd with ldap backend throws error domain log
-  `#2849 <https://github.com/SSSD/sssd/issues/2849>`_ [RFE] authenticate against cache in SSSD
-  `#3059 <https://github.com/SSSD/sssd/issues/3059>`_ [RFE] Python 3 support
-  `#3527 <https://github.com/SSSD/sssd/issues/3527>`_ [RFE] The fast memory cache should cache initgroups
-  `#3631 <https://github.com/SSSD/sssd/issues/3631>`_ SSSD doesn't re-read resolv.conf if the file doesn't exist during boot
-  `#3682 <https://github.com/SSSD/sssd/issues/3682>`_ Add a IS_DEFAULT_VIEW macro
-  `#3742 <https://github.com/SSSD/sssd/issues/3742>`_ Kerberos-based providers other than krb5 do not queue requests

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_12_3..sssd-1_13_0

    Adam Tkac (1):
        2a25713af  Option filter_users had no effect for retrieving sudo rules

    Aron Parsons (2):
        c520f40d1  IPA: fix segfault in ipa_s2n_exop
        4df706219  autofs: fix 'Cannot allocate memory' with FQDNs

    Bohuslav Kabrda (1):
        341a00311  Python3 support in SSSD

    Daniel Hjorth (1):
        2b20ff2e3  LDAP: unlink ccname_file_dummy if there is an error

    Jakub Hrozek (127):
        5c14f85f2  Updating the version to the 1.12.4 release
        fc2cc91a5  GPO: Ignore ENOENT result from sysdb_gpo_get_gpo_result_setting()
        ee8dccf5f  TESTS: Cover sysdb_gpo.c with unit tests
        ba68d2bd1  MAN: Fix a typo
        bb7ddd2be  GPO: Set libsmb debugging to stderr
        16cb0969f  UTIL: Allow dup-ing child pipe to a different FD
        f00a61b60  GPO: Don't use stdout for output in gpo_child
        ccff8e759  GPO: Extract server hostname after connecting
        4f4d35e14  SYSDB: Reduce code duplication in sysdb_gpo.c
        9b2cd4e5e  krb5_child: Return ERR_NETWORK_IO on KRB5_KDCREP_SKEW
        dc7d8ab0f  UTIL: Make two child_common.c functions static
        44703b84f  TESTS: Cover child_common.c with unit tests
        752227a75  LDAP: Use child_io_destructor instead of child_cleanup in a custom desctructor
        0e8a48e38  UTIL: Remove child_cleanup
        f3d91181d  UTIL: Unify the fd_nonblocking implementation
        858e750c3  Open the PAC socket from krb5_child before dropping root
        51d65c4ad  BUILD: Include python-test.py in the tarball
        b2c5e98de  IPA: Use attr's dom for users, too
        486f0d522  SELINUX: Call setuid(0)/setgid(0) to also set the real IDs to root
        8f78b6442  SELINUX: Set and reset umask when caling set_seuser from deamon code
        108db0e3b  LDAP: Add UUID when saving incomplete groups
        b2c3722b9  IPA: Resolve IPA user groups' overrideDN in non-default view
        4d7fe714f  LDAP: Rename the _res output parameter to avoid clashing with libresolv in tests
        bf54fbed1  RESOLV: Add an internal function to read TTL from a DNS packet
        5594736ea  RESOLV: Remove obsolete in-tree implementation of SRV and TXT parsing
        842fe49b8  resolv: Fix a typo
        b0f46a301  SELINUX: Check the return value of setuid and setgid
        2fec5f131  GPO: Better debugging for gpo_child's mkdir
        eb85a718f  LDAP: Add better DEBUG messages to the cleanup task
        5a56c7c6e  LDAP: Handle ENOENT better in the cleanup task
        bdc2aced1  PAM: print the pam status as string, too
        eafbc66c2  resolv: Use the same default timeout for SRV queries as previously
        8df69bbc5  FO: Use SRV TTL in fail over code
        01f78f755  selinux: Delete existing user mapping on empty default
        429d51ec3  KRB5: More debugging for create_ccache()
        cecee447d  build: Only run cmocka tests if cmocka 1.0 or newer is available
        0aad066ba  RPM: BuildRequire libcmocka >= 1.0
        4e5e846de  tests: convert all unit tests to cmocka 1.0 or later
        9cc2223e0  tests: ncache_hit must be an int to test UPNs
        84a4c4fcc  tests: Add a getpwnam-by-UPN test
        ff19b24a9  NSS: Handle ENOENT when doing initgroups by UPN
        aa648535f  Add unit tests for initgroups
        3e6dac8e1  selinux: Handle setup with empty default and no configured rules
        b123a618d  SDAP: Make simple bind timeout configurable
        f0072e2b1  SDAP: Make password change timeout configurable with ldap_opt_timeout
        7a62712d6  SDAP: Make StartTLS bind configurable with ldap_opt_timeout
        331de115a  SDAP: Decorate the sdap_op functions with DEBUG messages
        e2405de14  tests: Use cmocka-1.0+ API in test_sysdb_utils
        9797aa590  Resolv: re-read SRV query every time if its TTL is 0
        1243e093f  IPA: Use custom error codes when validating HBAC rules
        64d8e2df8  IPA: Drop useless sysdb parameter
        c41ae115b  IPA: Only treat malformed HBAC rules as fatal if deny rules are enabled
        fdfe33975  IPA: Deprecate the ipa_hbac_treat_deny_as option
        6dff95bdf  IPA: Remove the ipa_hbac_treat_deny_as option
        86bbaa25f  MAN: Clarify debug_level a bit
        eeecc48d2  SSH: Ignore the default_domain_suffix
        450c2b78f  LDAP: Set sdap handle as explicitly connected in LDAP auth
        e11b9f85b  tests: Revert strcmp condition
        d338bb46b  ncache: Fix sss_ncache_reset_permanent
        1aa492ce8  ncache: Silence critical error from filter_users when default_domain_suffix is set
        0d19785f9  ncache: Add sss_ncache_reset_repopulate_permanent
        0528fdec1  responders: reset ncache after domains are discovered during startup
        da3fcbec4  NSS: Reset negcache after checking domains
        ab11b2573  MAN: Clarify how are GPO mappings called in GPO editor
        843a66170  UTIL: Add a simple function to get the fd of debug_file
        cdff114a0  dyndns: Log nsupdate stderr with a high debug level
        00f58d221  nsupdate: Append -d/-D to nsupdate with a high debug level
        aa00d67b2  selinux: Disconnect before closing the handle
        748b38a79  selinux: Begin and end the transaction on the same nesting level
        1e0fa55fb  selinux: Only call semanage if the context actually changes
        6fa190d63  subdom: Remove unused function get_flat_name_from_subdomain_name
        ce6f3b6b2  sysdb: Add cache_expire to the default sysdb_search_object_by_str_attr set
        6a074a591  nss: Use negcache for getbysid requests
        bbd6f73bb  tests: Add NSS responder tests for bysid requests
        589a8760b  SELINUX: Avoid disconnecting disconnected handle
        f1f585456  LDAP: return after tevent_req_error
        601d193fe  LDAP: disable the cleanup task by default
        5c2f80ef0  MAN: refresh_expired_interval also supports users and groups
        ee44aac95  Download complete groups if ignore_group_members is set with tokengroups
        d9296ba01  DP: Set extra_value to NULL for enum requests
        40bc389bc  Skip enumeration requests in IPA and AD providers as well
        a010c6fc2  TESTS: Use the right testcase
        4f97aaa2f  TESTS: Add test for get_next_domain
        e7e61c777  LDAP: Do not print verbose DEBUG messages from providers that don't set UUID
        1711cbfd2  confdb: Add new option subdomain_inherit
        b3d110fbc  DP: Add a function to inherit DP options, if set
        12089241f  SDAP: Add sdap_copy_map_entry
        01c049cee  UTIL: Inherit ignore_group_members
        9b162bf39  subdomains: Inherit cleanup period and tokengroup settings from parent domain
        ea224c381  SYSDB: Store trust direction for subdomains
        50936fc72  UTIL/SYSDB: Move new_subdomain() to sysdb_subdomains.c and make it private
        526a15438  TESTS: Add a test for sysdb_subdomains.c
        9af86b9c9  SYSDB: Add realm to sysdb_master_domain_add_info
        b50baee36  SYSDB: Add a forest root attribute to sss_domain_info
        ad9ca94d0  IPA: Add ipa_subdomains_handler_get_{start,cont} wrappers
        5a5f1e105  IPA: Check master domain record before subdomain records
        9b7762729  IPA: Fold ipa_subdom_enumerates into ipa_subdom_store
        c3243e321  IPA: Also update master domain when initializing subdom handler
        27e89b692  IPA: Move server-mode functions to a separate module
        89ddc9ed4  IPA: Split two functions to new module ipa_subdomains_utils.c
        05d935cc9  IPA: Include ipaNTTrustDirection in the attribute set for trusted domains
        10bf907b6  IPA: Read forest name for trusted forest roots as well
        298e22fc9  IPA: Make constructing an IPA server mode context async
        b1a822a16  TESTS: Split off keytab creation into a common module
        d43c9d18f  TESTS: Add a common mock_be_ctx function
        28600ab8d  TESTS: Add a common function to set up sdap_id_ctx
        78fb1789e  TESTS: Move krb5_try_kdcip to nested group test
        f4025ea81  TESTS: Add unit test for the subdomain_server.c module
        64ea4127f  IPA: Fetch keytab for 1way trusts
        44ba57358  AD: Rename ad_set_ad_id_options to ad_set_sdap_options
        51b5e1475  AD: Rename ad_create_default_options to ad_create_2way_trust_options
        933314e53  AD: Split off ad_create_default_options
        de2bad8ae  IPA/AD: Set up AD domain in ad_create_2way_trust_options
        0c37b025b  IPA: Do not set AD_KRB5_REALM twice
        30dd3f3e0  AD: Add ad_create_1way_trust_options
        d2c552edd  IPA: Utility function for setting up one-way trust context
        3b9f34f65  LDAP: Do not set keytab through environment variable
        7abec79ff  LDAP: Consolidate SDAP_SASL_REALM/SDAP_KRB5_REALM behaviour
        a5bb51844  CONFIG: Add SSS_STATEDIR as VARDIR/lib/sss
        dbfc407ee  BUILD: Store keytabs in /var/lib/sss/keytabs
        be5cc3c01  Updating the translations for the 1.13 Alpha release
        7d4b8fe68  Updating the version.m4 file for the 1.13 Beta release
        eca74a955  tests: Reduce duplication with new function test_ev_done
        01ec08efd  KRB5: Add and use krb5_auth_queue_send to queue requests by default
        7e798b94c  PAM: Only cache first-factor
        531661c7b  Updating the translations for the 1.13.0 release
        9e0a2ea88  Updating the version for the 1.13.0 release

    John Dickerson (1):
        dcaf21465  MAN: Amend the description of ignore_group_members

    Lukas Slebodnik (97):
        565eb6fa4  logrotate: Fix warning file size changed while zipping
        ecf9e7a87  MAN: Remove indentation in element programlistening
        e2d36e6f7  Fix warning: for loop has empty body
        2d5cdfef3  Bump version to track 1.13 development
        ead4e0a2e  SPEC: Use libnl3 for epel6
        b3b618985  MAKE: Don't include autoconf generated file to tarball
        33889b2ad  PROXY: Fix use after free
        3cd7275c3  pysss: Fix double free
        be73b2632  TESTS: Mock return value of sdap_get_generic_recv
        2c7a47b6e  test_nested_groups: Additional unit tests
        5085d263f  Fix warning: equality comparison with extraneous parentheses
        373946b54  MONITOR: Fix double free
        1ac368d09  SSSDConfig: Remove unused exception name
        a71004c11  SSSDConfig: Port missing parts to python3
        e80583227  Remove strict requirements of python2
        deeadf40d  CONFIGURE: Do not use macro AC_PROG_MKDIR_P twice
        fa0a9bad8  RESPONDERS: Warn to syslog about colliding objects
        35808a6c8  LDAP: Conditional jump depends on uninitialised value
        4e0404ca1  BUILD: Remove unused libraries for pysss.so
        36458f305  BUILD: Remove unused variables
        d6c3de740  BUILD: Remove detection of type Py_ssize_t
        9eabaad5e  UTIL: Remove python wrapper sss_python_set_new
        887edd6b7  UTIL: Remove python wrapper sss_python_set_add
        a63b368a0  UTIL: Remove python wrapper sss_python_set_check
        03e9d9d6c  UTIL: Remove compatibility macro PyModule_AddIntMacro
        e4796d5ed  UTIL: Remove python wrapper sss_python_unicode_from_string
        dc4c30bae  BUILD: Use python-config for detection *FLAGS
        de0b510a1  SPEC: Use new convention for python packages
        4706958e7  SPEC: Move python bindings to separate packages
        4a5a18f48  BUILD: Add possibility to build python{2,3} bindings
        183727125  TESTS: Run python tests with all supported python versions
        b6840554b  SPEC: Replace python_ macros with python2_
        889706cbc  SPEC: Build python3 bindings on available platforms
        192583f96  BUILD: Uninstall also symbolic links to python bindings
        d88694443  Remove unused argument from be_nsupdate_create_fwd_msg
        cfb6e8c83  IPA: Remove unused argument from ipa_id_get_group_uuids
        cac22be9e  Remove useless assignment to function parameter
        76faa8557  PAC: Fix memory leak
        04d138472  Log reason in debug message why ldb_modify failed
        e239b5bed  sbus_codegen: Port to python3
        0df2970fe  ipa_selinux: Fix warning may be used uninitialized
        8981779c8  responder_cache: Fix warning may be used uninitialized
        87f8bee53  Add missing new lines to debug messages
        95e98d7f6  debug-tests: Fix test with new line in debug message
        999c87114  memberof: Do not create request with 0 attribute values
        077f8c9ca  BUILD: Add missing header file to tarball
        50afd8b1d  pam_client: fix casting to const pointer
        2233216c6  test_expire: Use right assertion macro for standard functions
        33e54a998  test_ldap_auth: Use right assertion for integer comparison
        2b84054e2  test_resolv_fake: Fix alignment warning
        3b894003c  PAC: Remove unused function
        818c55be4  GPO: Check return value of ad_gpo_store_policy_settings
        41f13bb04  KRB5: Unify prototype and definition
        d51bc5f43  CLIENT: Clear errno with enabled sss-default-nss-plugin
        2f84032c2  util-tests: Initialize boolean variable to default value
        148623c86  SPEC: Drop workaround for old libtool
        f66f53572  SPEC: Drop workarounds for old rpmbuild
        2674eeb15  SPEC: Remove unused option
        98d45a51d  SPEC: Few cosmetic changes
        5d864e7a9  SDAP: Do not set gid 0 twice
        bad2fc813  SDAP: Extract filtering AD group to function
        b9fbeb75e  SDAP: Filter ad groups in initgroups
        cf0be3395  simple_access-tests: Simplify assertion
        4a73eb4c8  sysdb-tests: Add missing assertions
        4ea6bc6de  sysdb-tests: test return value before output arguments
        adb148603  ad_opts: Use different default attribute for group name
        827dd3424  BUILD: Write hints about optional python bindings
        03e5f1528  GPO: Do not ignore missing attrs for GPOs
        582f6b1d1  sss_nss_idmap-tests: Use different prepared buffers for big endian
        21687d1d5  SDAP: Fix id mapping with disabled subdomains
        56552c518  SPEC: Fix cyclic dependencies between sssd-{krb5,}-common
        2ec676521  sss_client: Fix mixed enums
        b4b2115bb  LDAP: Remove dead assignment
        75e4a7753  negcache: Soften condition for expired entries
        390de028b  test_nss_srv: Use right function for storing time_t
        fd6052832  nss: Do not ignore default vaue of SYSDB_INITGR_EXPIRE
        d0cc678d2  SDAP: Set initgroups expire attribute at the end
        dca741129  SDAP: Remove unnecessary argument from sdap_save_user
        0a111b876  sss_client: Fix warning "_" redefined
        62b201548  SSSDConfigTest: Use unique temporary directory
        1370bccca  PROXY: proxy_child should work in non-root mode
        df233bce9  PROXY: Do not register signal with SA_SIGINFO
        7a4e3e291  util-tests: Add validation of internal error messages
        176244cb1  SDAP: Check return value before using output arguments
        56e88cd5f  SDAP: Log failure from sysdb_handle_original_uuid
        9d69c0508  test_ipa_subdomains_server: Run clean-up after success
        f2bba721d  IFP: Fix warnings with enabled optimisation
        9fc96a4a2  SDAP: Remove user from cache for missing user in LDAP
        9aa384d5b  test_ipa_subdom_server: Add missing assert
        323943605  test_ipa_subdomains_server: Fix build with --coverage
        ebf6735dd  nss: Store entries in responder to initgr mmap cache
        6d292632a  mmap_cache: Invalidate entry in right memory cache
        7c83c2317  nss: Invalidate entry in initgr mmap cache
        88e68607e  sss_client: Use initgr mmap cache in client code
        b08bcc387  sss_cache: Clear also initgroups fast cache
        0ed6114c6  sss_client: Use unique lock for memory cache
        537e27787  sss_client: Re-check memcache after acquiring the lock

    Michal Zidek (4):
        804df4040  Use FQDN if default domain was set
        9619e0ae8  MAN: default_domain_suffix with use_fully_qualified_names.
        7c6922107  DEBUG: Add missing strings for error messages
        7650ded4f  test: Check ERR_LAST

    Michal Židek (3):
        9ac2a33f4  views: Add is_default_view helper function
        66615eee7  MONITOR: Poll for resolv.conf if not available during boot
        0469c14ca  MONITOR: Do not report missing file as fatal in monitor_config_file

    Nikolai Kondrashov (3):
        9c5e4ae08  BUILD: Add AM_PYTHON2_MODULE macro
        9d453f1e8  Add integration tests
        fd3b0d823  BUILD: Fix variable substitution in cwrap.m4

    Pavel Březina (62):
        ce6ba48c5  spec: sifp requires sssd-dbus
        dbb990fb2  tests: refactor create_dom_test_ctx()
        acc1c0c07  tests: add create_multidom_test_ctx()
        629a188ec  tests: add test_multidom_suite_cleanup()
        cb4742876  tests: remove code duplication in single domain cleanup
        360a4be42  responders: new interface for cache request
        96faa5ca7  responders: enable views in cache request
        faae3d55e  IFP: use new cache interface
        fd52e9e51  server-tests: use strtouint32 instead strtol
        9fa95168d  sbus: add new iface via sbus_conn_register_iface()
        d87e960c1  sbus: move iface and object path code to separate file
        894f09f14  sbus: use 'path/*' to represent a D-Bus fallback
        46ee93131  sbus: support multiple interfaces on single path
        71c9027d4  sbus: add object path to sbus request
        21e05273e  sbus: add sbus_opath_hash_lookup_supported()
        80d0bd382  sbus: support org.freedesktop.DBus.Introspectable
        b742179ac  sbus: support org.freedesktop.DBus.Properties
        66277b211  sbus: unify naming of handler data variable
        3a8f6b575  sbus: move common opath functions from ifp to sbus code
        ca6dd8e7a  sbus: add sbus_opath_get_object_name()
        c66420cb2  ifp: fix potential memory leak in check_and_get_component_from_path()
        df4e1db5d  sbus: use hard coded getters instead of generated
        16cf65323  sbus: remove unused 'reply as' functions
        772199031  IFP: move interface definitions from ifpsrv.c into separate file
        beeef7f62  IFP: unify generated interfaces names
        4e5d19f65  sbus codegen: do not prefix getters with iface name
        62ebed858  IFP: simplify object path constant names
        e3a7f7ee0  sbus: add constant to represent subtree
        b0d3164ca  be_refresh: refresh all domains in backend
        a849d848d  sdap_handle_acct_req_send: remove be_req
        ab0eda362  be_refresh: refactor netgroups refresh
        17531a398  be_refresh: add sdap_refresh_init
        e77d6366f  be_refresh: support users
        61c8d13e5  be_refresh: support groups
        26d6ed2f1  be_refresh: get rid of callback pointers
        12a000c8c  sysdb: use sysdb_user/group_dn
        54ed1b121  cache_req tests: rename test_user to test_user_by_name
        bbc34d5a6  cache_req tests: define user name constant
        665bc06b1  cache_req: preparations for different input type
        3a5ea8100  cache_req: add support for user by uid
        641d684ee  cache_req: add support for group by name
        4458dbab0  cache_req: remove default branch from switches
        71965bb18  cache_req: add support for group by id
        282203aa6  cmocka: include mock_parse_inp in header file
        e87b2a6e9  cache_req: parse input name if needed
        997864d49  cache_req: return ERR_INTERNAL if more than one entry is found
        725bb2a99  enumeration: fix talloc context
        c526cd124  sudo: sanitize filter values
        364b3572b  sbus: provide custom error names
        10a28f461  sbus: add sbus_opath_decompose[_exact]
        ac7442234  sbus: add a{sas} get invoker
        c747b0c87  IFP: add org.freedesktop.sssd.infopipe.Users
        a1e4113a5  IFP: add org.freedesktop.sssd.infopipe.Users.User
        132e477d6  IFP: add org.freedesktop.sssd.infopipe.Groups
        8fe171bf5  IFP: add org.freedesktop.sssd.infopipe.Groups.Group
        4b8f260c9  IFP: deprecate GetUserAttr
        d3c82d017  IFP: Implement org.freedesktop.sssd.infopipe.Cache[.Object]
        c5184e9ee  SBUS: Use default GetAll invoker if none is set
        f7adbb15d  SBUS: Add support for <node /> in introspection
        2b7ef8508  IFP: Export nodes
        ae7247551  sbus: add support for incoming signals
        d4aa04972  sbus: listen to NameOwnerChanged

    Pavel Reichl (44):
        b49c6abe1  GPO: add systemd-user to gpo default permit list
        702176303  MAN: dyndns_iface supports only one interface
        9a15eb105  MAN: add dots as valid character in domain names
        b22e0da9e  AD: add new option ad_site
        e438fbf10  AD: support for AD site override
        ab5f9b58a  MAN: amend sss_ssh_authorizedkeys
        b07a3b729  add missing '\n' in debug messages
        a61d6d01a  PAM: do not reject abruptly
        e039f1aef  PAM: new option pam_account_expired_message
        f3c2dc1f9  PAM: warn all services about account expiration
        c5290f217  PAM: check return value of confdb_get_string
        18e24f20a  PROXY: add missing space in debug message
        cabc05118  BUILD: fix chmake not to generate warning
        c820e6db2  SDAP: log expired accounts at lower severity level
        cdaa29d2c  SDAP: refactor pwexpire policy
        c9b0071bf  SDAP: enable change phase of pw expire policy check
        5a5c5cdeb  UTIL: convert GeneralizedTime to unix time
        13ec767e6  SDAP: Lock out ssh keys when account naturally expires
        79ee5fbac  SDAP: fix minor neglect in is_account_locked()
        6ccda8691  ldap_child: fix coverity warning
        33b8bf140  MAN: libkrb5 and SSSD use different expansions
        131da4d9f  IPA: set EINVAL if dn can't be linearized
        2bb92b969  KRB5: add debug hint
        ef9ca5848  LDAP: remove unused code
        50b8a36b0  TESTS: test expiration
        0ec41ab7d  ldap: refactor check_pwexpire_kerberos to use util func
        08f83281c  ldap: refactor nds_check_expired to use util func
        871f34083  LDAP: fix a typo in debug message
        c2cb78c26  Fix a few typos in comments
        1426ee875  MAN: Update ppolicy description
        82a958e65  simple-access-provider: make user grp res more robust
        6170f00ee  sbus: sbus_opath_hash_add_iface free tmp talloc ctx
        9696ce0c9  krb5: remove field run_as_user
        108a49f0e  LDAP: warn about lockout option being deprecated
        cc98e19b4  localauth plugin: fix coverity warning
        aa8a8318a  krb5: new option krb5_map_user
        bee7549be  dyndns: remove dupl declaration of ipa_dyndns_update
        366c3020c  dyndns: don't pass zone directive to nsupdate
        dd40f54ba  dyndns: ipa_dyndns.h missed declaration of used data
        3683195b2  krb: remove duplicit decl. of write_krb5info_file
        979e8d8d6  IPA: Don't override homedir with subdomain_homedir
        32cc237aa  sysdb: new attribute lastOnlineAuthWithCurrentToken
        0aa18cc0b  PAM: authenticate agains cache
        6aff93510  Minor code improvements

    Rob Crittenden (1):
        0e4d3214d  Add user_attributes to ifp section of API schema

    Stephen Gallagher (8):
        d9079aa05  AD: Clean up ad_access_gpo
        e2bd4f8a4  AD: Always get domain-specific ID connection
        475d986b5  AD GPO: Always look up GPOs from machine domain
        c9db9d3e3  LDAP: Support returning referral information
        31bafc0d6  AD GPO: Support processing referrals
        772464c84  AD GPO: Change default to "enforcing"
        a0b95be79  Add Vagrant configuration for SSSD
        b08b6a994  GPO: Fix incorrect strerror on GPO access denial

    Sumit Bose (71):
        d32b165fa  IPA: add get_be_acct_req_for_user_name()
        765d9075b  IPA: resolve ghost members if a non-default view is applied
        fbcdc0872  sysdb: fix group members with overridden names
        eab17959d  IPA: ipa_resolve_user_list_send() take care of overrides
        d8ceb1940  IPA: do not look up overrides on client with default view
        2fc12875f  IPA: make version check more precise
        e6046d23b  IPA: add missing break
        942ebb62c  IPA: process_members() optionally return missing members list
        f1f22df95  IPA: rename ipa_s2n_get_groups_send() to ipa_s2n_get_fqlist_send()
        3cd287313  IPA: resolve missing members
        62d919aea  IPA: set SYSDB_INITGR_EXPIRE for RESP_USER_GROUPLIST
        576ad6371  krb5: fix entry order in MEMORY keytab
        5f4d896ec  nss: make fill_orig() multi-value aware
        a4d64002b  nss: refactor fill_orig()
        7543052f5  nss: Add original DN and memberOf to origbyname request
        ba818cc39  views: fix GID overrride for mpg domains
        dd5ebcde0  IPA: properly handle mixed-case trusted domains
        d6ddc3557  nss: fix SID lookups
        fc2146c10  sysdb: remove ghosts in all sub-domains as well
        63748c69a  IPA: resolve IPA group-memberships for AD users
        60f11e2fa  IPA: process_members() add ghosts only once
        9ad346318  ipa_s2n_save_objects: properly handle fully-qualified group names
        561ed2fd0  AD: use GC for SID requests as well
        866ab4502  fill_id() fix LE/BE issue with wrong data type
        cc0f9a541  ldap_child: initialized ccname_file_dummy
        7bbf9d1d0  PAM: use the logon_name as the key for the PAM initgr cache
        10da5ea89  pam_initgr_check_timeout: add debug output
        3e9712c2f  ipa: do not treat missing sub-domain users as error
        7ee9ac324  ipa: make sure extdom expo data is available
        d81d8d3dc  LDAP/AD: do not resolve group members during tokenGroups request
        8be0cf3ee  IPA idviews: check if view name is set
        abb093b4a  IPA: make sure output variable is set
        1d9302962  sdap: properly handle binary objectGuid attribute
        4cfab2330  GPO: error out instead of leaving array element uninitialized
        2ab9a4538  IPA: do not try to save override data for the default view
        625cff0b0  IPA: use sysdb_attrs_add_string_safe to add group member
        605dc7fcc  IPA: check ghosts in groups found by uuid as well
        f70a1adbf  IPA: allow initgroups by SID for AD users
        e87badc0f  IPA: do initgroups if extdom exop supports it
        cffe3135f  IPA: update initgr expire timestamp conditionally
        145578006  IPA: enhance ipa_initgr_get_overrides_send()
        2263c6dd1  IPA: search for overrides during initgroups in sever mode
        3fe2e555e  IPA: do not add domain name unconditionally
        35b178d02  NSS: check for overrides before calling backend
        0f9c28eb5  IPA: allow initgroups by UUID for FreeIPA users
        80b5dbe12  Add leak check and command line option to test_authtok
        bc052ea17  utils: add sss_authtok_[gs]et_2fa
        ea98a7af0  pam: handle 2FA authentication token in the responder
        fb045f6e5  Add pre-auth request
        4b1b2e60d  krb5-child: add preauth and split 2fa token support
        deb28a893  IPA: create preauth indicator file at startup
        e5698314b  pam_sss: add pre-auth and 2fa support
        932c3e22e  Add cache_credentials_minimal_first_factor_length config option
        55b7fdd83  sysdb: add sysdb_cache_password_ex()
        c5ae04b2d  krb5: save hash of the first authentication factor to the cache
        2d0e76581  krb5: try delayed online authentication only for single factor auth
        219f5b698  2FA offline auth
        bf6c3f07d  pam_sss: move message encoding into separate file
        ea422c706  PAM: add PAM responder unit test
        305267064  SDAP: use DN to update entry
        a50b229c8  IPA: do not fail if view name lookup failed on older versions
        1270ffe9f  libwbclient-sssd: update interface to version 0.12
        d0b7e5fcf  ldap: use proper sysdb name in groups_by_user_done()
        070bb5153  adding ldap_user_auth_type where missing
        e22e04517  LDAP: add ldap_user_certificate option
        bf01e8179  certs: add PEM/DER conversion utilities
        7d8b7d82f  sysdb: add sysdb_search_user_by_cert() and sysdb_search_object_by_cert()
        caacea0db  LDAP/IPA: add user lookup by certificate
        8d4dedea1  ncache: add calls for certificate based searches
        a99845006  utils: add get_last_x_chars()
        827a016a0  IFP: add FindByCertificate method for User objects
