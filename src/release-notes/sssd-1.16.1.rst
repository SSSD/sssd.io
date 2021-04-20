SSSD 1.16.1 Release Notes
=========================

Highlights
----------

New Features
~~~~~~~~~~~~

-  A new option ``auto_private_groups`` was added. If this option is enabled, SSSD will automatically create user private groups based on user's UID number. The GID number is ignored in this case. Please see <../../design_pages/auto_private_groups.mdfor more details on the feature.
-  The SSSD smart card integration now supports a special type of PAM conversation implemented by GDM which allows the user to select the appropriate smrt card certificate in GDM. Please refer to <../../design_pages/smartcard_multiple_certificates.mdfor more details about this feature.
-  A new API for accessing user and group information was added. This API is similar to the tradiional Name Service Switch API, but allows the consumer to talk to SSSD directly as well as to fine-tune the query with e.g. how cache should be evaluated. Please see <../../design_pages/enhanced_nss_api.mdfor more information on the new API.
-  The ``sssctl`` command line tool gained a new command ``access-report``, which can generate who can access the client machine. Currently only generating the report on an IPA client based on HBAC rules is supported. Please see <../../design_pages/attestation_report.mdfor more information about this new feature.
-  The ``hostid`` provider was moved from the IPA specific code to the generic LDAP code. This allows SSH host keys to be access by the generic LDAP provider as well. See the ``ldap_host_*`` options in the ``sssd-ldap`` manual page for more details.
-  Setting the ``memcache_timeout`` option to 0 disabled creating the memory cache files altogether. This can be useful in cases there is a bug in the memory cache that needs working around.

Performance enhancements
~~~~~~~~~~~~~~~~~~~~~~~~

-  Several internal changes to how objects are stored in the cache improve SSSD performance in environments with large number of objects of the same type (e.g. many users, many groups). In particular, several useless indexes were removed and the most common object types no longer use the indexed ``objectClass`` attribute, but use unindexed ``objectCategory`` instead (#3503)
-  In setups with ``id_provider=ad`` that use POSIX attributes which are replicated to the Global Catalog, SSSD uses the Global Catalog to determine which domain should be contacted for a by-ID lookup instead of iterating over all domains. More details about this feature can be found at <../../design_pages/uid_negative_global_catalog.md>

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  A crash in ``sssd_nss`` that might have happened if a list of domains was refreshed while a NSS lookup using this request was fixed (#3551)
-  A potential crash in ``sssd_nss`` during netgroup lookup in case the netgroup object kept in memory was already freed (#3523)
-  Fixed a potential crash of ``sssd_be`` with two concurrent sudo refreshes in case one of them failed (#3562)
-  A memory growth issue in ``sssd_nss`` that occured when an entry was removed from the memory cache was fixed (#3588)
-  Two potential memory growth issues in the ``sssd_be`` process that could have hit configurations with ``id_provider=ad`` were fixed (#3639)
-  The ``selinux_child`` process no longer crashes on a system where SSSD is compiled with SELinux support, but at the same time, the SELinux policy is not even installed on the machine (#3618)
-  The memory cache consistency detection logic was fixed. This would prevent printing false positive memory cache corruption messages (#3571)
-  SSSD now remembers the last successfuly discovered AD site and use this for DNS search to lookup a site and forest during the next lookup. This prevents time outs in case SSSD was discovering the site using the global list of DCs where some of the global DCs might be unreachable. (#3265)
-  SSSD no longer starts the implicit file domain when configured with ``id_provider=proxy`` and ``proxy_lib_name=files``. This bug prevented SSSD from being used in setups that combine identities from UNIX files together with authentication against a remote source unless a files domain was explicitly configured (#3590)
-  The IPA provider can handle switching between different ID views better (#3579)
-  Previously, the IPA provider kept SSH public keys and certificates from an ID view in its cache and returned them even if the public key or certificate was then removed from the override (#3602, #3603)
-  FleetCommander profiles coming from IPA are applied even if they are assigned globally (to ``category: ALL``), previously, only profiles assigned to a host or a hostgroup were applied (#3449)
-  It is now possible to reset an expired password for users with 2FA authentication enabled (#3585)
-  A bug in the AD provider which could have resulted in built-in AD groups being incorrectly cached was fixed (#3610)
-  The SSSD watchdog can now cope better with time drifts (#3285)
-  The ``nss_sss`` NSS module's return codes for invalid cases were fixed
-  A bug in the LDAP provider that prevented setups with id_provider=proxy and auth_provider=ldap with LDAP servers that do not allow anonymous binds from working was fixed (#3451)

Packaging Changes
-----------------

-  The FleetCommander desktop profile path now uses stricter permissions, 751 instead of 755 (#3621)
-  A new option ``--logger`` was added to the ``sssd(8)`` binary. This option obsoletes old options such as ``--debug-to-files``, although the old options are kept for backwards compatibility.
-  The file ``/etc/systemd/system/sssd.service.d/journal.conf`` is not installed anymore In order to change logging to journald, please use the ``--logger`` option. The logger is set using the ``Environment=DEBUG_LOGGER`` directive in the systemd unit files. The default value is ``Environment=DEBUG_LOGGER=--logger=files``

Documentation Changes
---------------------

There are no notable documentation changes such as options changing default values etc in this release.

Tickets Fixed
-------------

-  `#4668 <https://github.com/SSSD/sssd/issues/4668>`_ - Mention in the manpages that Fleet Commander does *not* work when SSSD is running as the unprivileged user
-  `#4660 <https://github.com/SSSD/sssd/issues/4660>`_ - sssd_be consumes more memory on RHEL 7.4 systems.
-  `#4648 <https://github.com/SSSD/sssd/issues/4648>`_ - MAN: Explain how does auto_private_groups affect subdomains
-  `#4642 <https://github.com/SSSD/sssd/issues/4642>`_ - FleetCommander integration must not require capability DAC_OVERRIDE
-  `#4639 <https://github.com/SSSD/sssd/issues/4639>`_ - selinux_child segfaults in a docker container
-  `#4636 <https://github.com/SSSD/sssd/issues/4636>`_ - Requesting an AD user's private group and then the user itself returns an emty homedir
-  `#4634 <https://github.com/SSSD/sssd/issues/4634>`_ - auto_private_groups does not work with trusted domains with direct AD integration
-  `#4632 <https://github.com/SSSD/sssd/issues/4632>`_ - AD provider - AD BUILTIN groups are cached with gidNumber = 0
-  `#4631 <https://github.com/SSSD/sssd/issues/4631>`_ - dbus-send unable to find user by CAC cert
-  `#4626 <https://github.com/SSSD/sssd/issues/4626>`_ - Certificate is not removed from cache when it's removed from the override
-  `#4625 <https://github.com/SSSD/sssd/issues/4625>`_ - SSH public key authentication keeps working after keys are removed from ID view
-  `#4624 <https://github.com/SSSD/sssd/issues/4624>`_ - race condition: sssd_be in a one-way trust accepts request before ipa-getkeytab finishes, marking the sssd offline
-  `#4622 <https://github.com/SSSD/sssd/issues/4622>`_ - getent output is not showing home directory for IPA AD trusted user
-  `#4617 <https://github.com/SSSD/sssd/issues/4617>`_ - sssd used wrong search base with wrong AD server
-  `#4615 <https://github.com/SSSD/sssd/issues/4615>`_ - Write a regression test for false possitive "corrupted" memory cache
-  `#4613 <https://github.com/SSSD/sssd/issues/4613>`_ - proxy to files does not work with implicit_files_domain
-  `#4612 <https://github.com/SSSD/sssd/issues/4612>`_ - sssd_nss consumes more memory until restarted or machine swaps
-  `#4610 <https://github.com/SSSD/sssd/issues/4610>`_ - Give a more detailed debug and system-log message if krb5_init_context() failed
-  `#4609 <https://github.com/SSSD/sssd/issues/4609>`_ - Reset password with two factor authentication fails
-  `#4603 <https://github.com/SSSD/sssd/issues/4603>`_ - SSSD fails to fetch group information after switching IPA client to a non-default view
-  `#4595 <https://github.com/SSSD/sssd/issues/4595>`_ - mmap cache: consistency check might fail if there are hash collisions
-  `#4594 <https://github.com/SSSD/sssd/issues/4594>`_ - The cache-req debug string representation uses a wrong format specifier for by-ID requests
-  `#4593 <https://github.com/SSSD/sssd/issues/4593>`_ - The cache_req code doesn't check the min_id/max_id boundaries for requests by ID
-  `#4588 <https://github.com/SSSD/sssd/issues/4588>`_ - Smartcard authentication fails if SSSD is offline and 'krb5_store_password_if_offline = True'
-  `#4587 <https://github.com/SSSD/sssd/issues/4587>`_ - Some sysdb tests fail because they expect a certain order of entries returned from ldb
-  `#4586 <https://github.com/SSSD/sssd/issues/4586>`_ - Use-after free if more sudo requests run and one of them fails, causing a fail-over to a next server
-  `#4585 <https://github.com/SSSD/sssd/issues/4585>`_ - Improve Smartcard integration if multiple certificates or multiple mapped identities are available
-  `#4577 <https://github.com/SSSD/sssd/issues/4577>`_ - Race condition between refreshing the cr_domain list and a request that is using the list can cause a segfault is sssd_nss
-  `#4573 <https://github.com/SSSD/sssd/issues/4573>`_ - data from ipa returned with id_provider=file
-  `#4571 <https://github.com/SSSD/sssd/issues/4571>`_ - SSSD creates bad override search filter due to AD Trust object with parenthesis
-  `#4565 <https://github.com/SSSD/sssd/issues/4565>`_ - Do not autostart the implicit files domain if sssd configures id_provider=proxy and proxy_target_files
-  `#4555 <https://github.com/SSSD/sssd/issues/4555>`_ - SSSD-kcm/secrets failed to restart during/after upgrade
-  `#4554 <https://github.com/SSSD/sssd/issues/4554>`_ - sssd refuses to start when pidfile is present, but the process is gone
-  `#4549 <https://github.com/SSSD/sssd/issues/4549>`_ - ABRT crash - /usr/libexec/sssd/sssd_nss in setnetgrent_result_timeout
-  `#4529 <https://github.com/SSSD/sssd/issues/4529>`_ - Do not index objectclass, add and index objectcategory instead
-  `#4522 <https://github.com/SSSD/sssd/issues/4522>`_ - [RFE] Add a configuration option to SSSD to disable the memory cache
-  `#4512 <https://github.com/SSSD/sssd/issues/4512>`_ - Improve ``enumerate`` documentation/troubleshooting guide
-  `#4510 <https://github.com/SSSD/sssd/issues/4510>`_ - MAN: Describe the constrains of ipa_server_mode better in the man page
-  `#4494 <https://github.com/SSSD/sssd/issues/4494>`_ - SSSD doesn't use AD global catalog for gidnumber lookup, resulting in unacceptable delay for large forests
-  `#4481 <https://github.com/SSSD/sssd/issues/4481>`_ - sssd-kcm crashes with multiple parallel requests
-  `#4478 <https://github.com/SSSD/sssd/issues/4478>`_ - When sssd is configured with id_provider proxy and auth_provider ldap, login fails if the LDAP server is not allowing anonymous binds.
-  `#4471 <https://github.com/SSSD/sssd/issues/4471>`_ - document information on why SSSD does not use host-based security filtering when processing AD GPOs
-  `#4460 <https://github.com/SSSD/sssd/issues/4460>`_ - SYSLOG_IDENTIFIER is different
-  `#4326 <https://github.com/SSSD/sssd/issues/4326>`_ - Log when SSSD authentication fails because when two IPA accounts share an email address
-  `#4318 <https://github.com/SSSD/sssd/issues/4318>`_ - SSSD needs restart after incorrect clock is corrected with AD
-  `#4298 <https://github.com/SSSD/sssd/issues/4298>`_ - [RFE] sssd should remember DNS sites from first search
-  `#4231 <https://github.com/SSSD/sssd/issues/4231>`_ - Incorrect error code returned from krb5_child for expired/locked user with id_provider AD
-  `#4017 <https://github.com/SSSD/sssd/issues/4017>`_ - sdap code can mark the whole sssd_be offline
-  `#3881 <https://github.com/SSSD/sssd/issues/3881>`_ - [RFE] Produce access control attestation report for IPA domains
-  `#3864 <https://github.com/SSSD/sssd/issues/3864>`_ - Integration tests: Use dbus-daemon in cwrap enviroment for test
-  ``2478](https://github.com/SSSD/sssd/issues/3520) - Provide [sss_nss*()`` API to directly query SSSD instead of nsswitch.conf route
-  `#2914 <https://github.com/SSSD/sssd/issues/2914>`_ - [RFE] Support User Private Groups for main domains, too
-  `#2771 <https://github.com/SSSD/sssd/issues/2771>`_ - Enumerating large number of users makes sssd_be hog the cpu for a long time.


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_16_0..sssd-1_16_1

    Andreas Schneider (1):
        1ef36a878  Avoid double semicolon warnings on older compilers

    Carlos O'Donell (1):
        c096972ff  nss: Fix invalid enum nss_status return values.

    Fabiano Fidêncio (21):
        0f44eefe2  CACHE_REQ: Copy the cr_domain list for each request
        add72860c  LDAP: Bind to the LDAP server also in the auth
        c8396478e  TOOLS: Double quote array expansions in sss_debuglevel
        06c4482c0  TOOLS: Call "exec" for sss_debuglevel
        20d18db36  LDAP: Improve error treatment from sdap_cli_connect() in ldap_auth
        b739b3e76  SYSDB: Remove code causing a covscan warning
        1d88a0591  NSS: Fix covscan warning
        aa8608253  CACHE_REQ: Fix typo: cache_reg -> cache_req
        9be0fce9b  TOOLS: Fix typo: exist -> exists
        6c3d0ed4d  SYSDB: Return EOK in case a non-fatal issue happened
        d0d363124  SYSDB_VIEWS: Remove sshPublicKey attribute when it's not set
        56f015ef6  IPA: Remove sshPublicKey attribute when it's not set
        b72e444bc  DESKPROFILE: Add checks for user and host category
        0fce902c5  DESKPROFILE: Harden the permission of deskprofilepath
        b576b290d  DESKPROFILE: Soften umask for the domain's dir
        2c5b03913  DESKPROFILE: Fix the permissions and soften the umask for user's dir
        07ae0da06  DESKPROFILE: Use seteuid()/setegid() to create the profile
        1a011c4f2  DESKPROFILE: Use seteuid()/setegid() to delete the profile/user's dir
        f0cbe890a  DESKPROFILE: Set the profile permissions to read-only
        1c42c3962  PYSSS_MURMUR: Fix [-Wsign-compare] found by gcc
        5150fbdc4  DESKPROFILE: Document it doesn't work when run as unprivileged user

    Hristo Venev (1):
        60a715a0d  providers: Move hostid from ipa to sdap, v2

    Jakub Hrozek (36):
        dbad9f4e7  Update the version number to track 1.16.1 development
        d72ac2c58  CONFIG: Add a new option auto_private_groups
        8fab9d6fa  CONFDB: Remove the obsolete option magic_private_groups
        cdb74b2cc  SDAP: Allow the mpg flag for the main domain
        057e8af37  LDAP: Turn group request into user request for MPG domains if needed
        ac962e2b2  SYSDB: Prevent users and groups ID collision in MPG domains except for id_provider=local
        6c802b200  TESTS: Add integration tests for the auto_private_groups option
        2c6c3cff2  RESP: Add some missing NULL checks
        3ee8659bc  TOOLS: Add a new sssctl command access-report
        37fdd9dc1  SDAP: Split out utility function sdap_get_object_domain() from sdap_object_in_domain()
        8e93ebb2a  LDAP: Extract the check whether to run a POSIX check to a function
        dacfe7411  LDAP: Only run the POSIX check with a GC connection
        6ae22d9ad  SDAP: Search with a NULL search base when looking up an ID in the Global Catalog
        ba8a92bbd  SDAP: Rename sdap_posix_check to sdap_gc_posix_check
        c0f9f5a0f  DP: Create a new handler function getAccountDomain()
        095844d6b  AD: Implement a real getAccountDomain handler for the AD provider
        95fd82a4d  RESP: Expose DP method getAccountDomain() to responders
        07452697a  NEGCACHE: Add API for setting and checking locate-account-domain requests
        6cd367da6  TESTS: Add tests for the object-by-id cache_req interface
        800b1a275  CACHE_REQ: Export cache_req_search_ncache_add() as cache_req private interface
        2856dac58  CACHE_REQ: Add plugin methods required for the domain-locator request
        0a0b34f5f  CACHE_REQ: Add a private request cache_req_locate_domain()
        a6eb9c4c3  CACHE_REQ: Implement the plugin methods that utilize the domain locator API
        f2a5e29f0  CACHE_REQ: Use the domain-locator request to only search domains where the entry was found
        a72919af8  MAN: Document how the Global Catalog is used currently
        dc49e07a0  IPA: Include SYSDB_OBJECTCATEGORY, not OBJECTCLASS in cache search results
        89ed594e8  MAN: Document that auth and access IPA and AD providers rely on id_provider being set to the same type
        c6a4ef46f  MAN: Improve enumeration documentation
        f651d895b  MAN: Describe the constrains of ipa_server_mode better in the man page
        261a84355  IPA: Delay the first periodic refresh of trusted domains
        29ebf45f9  AD: Inherit the MPG setting from the main domain
        6df34be3e  SYSDB: Fix sysdb_search_by_name() for looking up groups in MPG domains
        50d9424d3  SYSDB: Use sysdb_domain_dn instead of raw ldb_dn_new_fmt
        a8a3fcbf6  SYSDB: Read the ldb_message from loop's index counter when reading subdomain UPNs
        9ac071272  AD: Use the right sdap_domain for the forest root
        7465d6a1e  Update translations for the 1.16.1 release

    Lukas Slebodnik (51):
        90503ff5a  KCM: Fix typo in comments
        0a20e4c03  CI: Ignore source file generated by systemtap
        09e3f0af9  UTIL: Add wrapper function to configure logger
        cb75b275d  Add parameter --logger to daemons
        a7277fecf  SYSTEMD: Replace parameter --debug-to-files with ${DEBUG_LOGGER}
        115145f0f  SYSTEMD: Add environment file to responder service files
        18a47bcc4  UTIL: Hide and deprecate parameter --debug-to-files
        53d1459e9  KCM: Fix restart during/after upgrade
        b495522f3  BUILD: Properly expand variables in sssd-ifp.service
        f4b808c83  SYSTEMD: Clean pid file in corner cases
        a24954cc1  CHILD: Pass information about logger to children
        44bc6e8f4  BUILD: Disable tests with know failures
        700fced06  SPEC: Reduce build time dependencies
        ab224783b  sysdb-test: Fix warning may be used uninitialized
        06e741a9b  responder: Fix talloc hierarchy in sized_output_name
        051e0fc7c  test_responder: Check memory leak in sized_output_name
        c987e5831  confdb: Move detection files to separate function
        30621369b  confdb: Fix starting of implicit files domain
        4928657ce  confdb: Do not start implicit_files with proxy domain
        34e5190f9  test_files_provider: Regression test for implicit_files + proxy
        1f2324abf  SDAP: Fix typo in debug message
        26803ffac  Revert "intg: Disable add_remove tests"
        ffc8c0696  libnfsidmap: Use public plugin header file if available
        44996f2ea  dyndns_tests: Fix unit test with missing features in nsupdate
        20a9c55ad  Remove unnecessary script for upgrading debug_levels
        fb22e59d2  Remove legacy script for upgrading sssd.conf
        7ad9f9c7c  BUILD: Add missing libs found by -Wl,-z,defs
        b61304a9f  BUILD: Fix using of libdlopen_test_providers.so in tests
        4e8d5c163  SYSDB: Decrese debuglevel in sysdb_get_certmap
        d380148b0  KRB5: Pass special flag to krb5_child
        5a7b76bf3  krb5_child: Distinguish between expired & disabled AD user
        1b6965fd0  AD: Suppress warning Wincompatible-pointer-types with sasl callbacks
        35eb23755  pysss: Drop unused parameter
        187f68360  pysss: Suppress warning Wincompatible-pointer-types
        2951a9a84  CRYPTO: Suppress warning Wstringop-truncation
        c53997720  INOTIFY: Fix warning Wstringop-truncation
        fcf6a9f34  SIFP: Suppress warning Wstringop-truncation
        bd5f48540  CLIENT: Fix warning Wstringop-overflow
        41454a64c  pysss_murmur: Allow to have NUL character in python bindings
        8f83feea4  TESTS: Extend code coverage for murmurhash3
        fd17e0925  mmap_cache: Remove unnecessary memchr in client code
        6dc1de978  test_memory_cache: Regression test for #3571
        274ee2952  SPEC: Fix systemd executions/requirements
        65afba536  SPEC: Reduce changes between upstream and downstream
        3b0356f3b  intg: Build with optimisations and debug symbols
        841bcb5e1  intg: Do not prefer builddir in PATH
        52ae4eeba  intg: Install configuration for dbus daemon
        e64696e1f  intg: Install wrapper for getsockopt
        0df79781d  intg: Add sample infopipe test in cwrap env
        2f8d0cc83  IPA: Drop unused ifdef HAVE_SELINUX_LOGIN_DIR
        47362caf4  IPA: Fix typo in debug message in sssm_ipa_selinux_init

    Michal Židek (9):
        878b0d42a  NSS: Move memcache setup to separate function
        ffe29e570  NSS: Specify memcache_timeout=0 semantics
        1becbb7be  MAN: Document memcache_timeout=0 meaning
        6c1661d2f  MAN: GPO Security Filtering limitation
        39d6a3be1  SYSDB: Better debugging for email conflicts
        caae0e53e  TESTS: Order list of entries in some lists
        fe189c1ab  Revert "BUILD: Disable tests with know failures"
        450b472a6  SELINUX: Check if SELinux is managed in selinux_child
        6b9c38df5  util: Add sss_ prefix to some functions

    Niranjan M.R (1):
        ee1e4c0fa  Initial revision of sssd pytest framework

    Pavel Březina (10):
        5c7170c6d  sudo: document background activity
        2ee201dcf  sudo: always use srv_opts from id context
        f54d202db  AD: Remember last site discovered
        e16539779  sysdb: add functions to get/set client site
        fb0431b13  AD: Remember last site discovered in sysdb
        6211a2023  dp: use void * to express empty output argument list
        e737cdfa2  dp: add method to refresh access control rules
        2754a8dcf  ipa: implement method to refresh HBAC rules
        c6cf75233  ifp: add method to refresh access control rules in domain
        be804178d  sssctl: call dbus instead of pam to refresh HBAC rules

    René Genz (12):
        a02a5ed51  Fix minor spelling mistakes
        6ab49aef1  README: Add link to docs repo
        655d723e7  Fix minor spelling mistakes
        4a9c10473  Fix minor spelling mistakes in providers/*
        677a31351  Fix minor spelling mistakes in responder/*
        080e1bfb7  Fix minor spelling mistakes in sss_client/*
        57c5ea882  Fix minor spelling mistakes in tests/cmocka/*
        346d6d8bf  Fix minor spelling mistakes
        49dd8ee28  Fix minor spelling mistakes in tests/*
        8a53449ad  Fix minor spelling mistakes in tests/multihost/*
        b6ece2885  Fix minor spelling mistakes in PY files in tests/python/*
        e10d56ed7  Fix minor spelling mistakes and formatting in tests/python/*

    Sumit Bose (48):
        7449b2365  sss_client: create nss_common.h
        5e6622722  nss-idmap: add nss like calls with timeout and flags
        cf93f7c2f  NSS: add *_EX version of some requests
        ac6b267ff  NSS: add support for SSS_NSS_EX_FLAG_NO_CACHE
        52e675ec4  CACHE_REQ: Add cache_req_data_set_bypass_dp()
        a7d6ca275  nss: make memcache_delete_entry() public
        55f7d8034  NSS: add support for SSS_NSS_EX_FLAG_INVALIDATE_CACHE
        85da8a5e9  NSS/TESTS: add unit tests for *_EX requests
        e54db68cb  nss-idmap: add timeout version of old sss_nss_* calls
        859bddc2b  nss-idmap: allow empty buffer with SSS_NSS_EX_FLAG_INVALIDATE_CACHE
        39fd336e4  p11_child: return multiple certs
        0bdd8800c  PAM: handled multiple certs in the responder
        122830e67  pam_sss: refactoring, use struct cert_auth_info
        0a8024af2  p11_child: use options to select certificate for authentication
        06c230035  pam: add prompt string for certificate authentication
        fd6f4047b  PAM: allow missing logon_name during certificate authentication
        08d1f8c0d  p11_child: add descriptions for error codes to debug messages
        177ab84f0  pam: filter certificates in the responder not in the child
        57cefea83  PAM: add certificate's label to the selection prompt
        f6a1cef87  NSS: Use enum_ctx as memory_context in _setnetgrent_set_timeout()
        438204749  mmap_cache: make checks independent of input size
        0cce3d3ad  sysdb: be_refresh_get_values_ex() remove unused option
        0e238c259  sysdb: do not use objectClass for users and groups
        98195e591  sysdb: do not use LDB_SCOPE_ONELEVEL
        2927da49d  sysdb: remove IDXONE and objectClass from users and groups
        2c1081975  krb5: show error message for krb5_init_context() failures
        b6d3da6cf  UTIL: add find_domain_by_object_name_ex()
        7988988aa  ipa: handle users from different domains in ipa_resolve_user_list_send()
        4671acb94  overrides: fixes for sysdb_invalidate_overrides()
        919b5d760  ipa: check for SYSDB_OVERRIDE_DN in process_members and get_group_dn_list
        f29040342  IPA: use cache searches in get_groups_dns()
        a52226c65  ipa: compare DNs instead of group names in ipa_s2n_save_objects()
        2297cc7d6  p11_child: make sure OCSP checks are done
        bba068c53  nss-idmap: allow NULL result in *_timeout calls
        c221b5fb4  Revert "p11_child: make sure OCSP checks are done"
        787ba9c88  p11_child: properly check results of CERT_VerifyCertificateNow
        510ac1939  ifp: use realloc in ifp_list_ctx_remaining_capacity()
        c36a66b7f  SDAP: skip builtin AD groups in sdap_save_grpmem()
        5b78fff78  sysdb: add userMappedCertificate to the index
        011dc5354  krb5_child: check preauth types if password is expired
        a409fd64a  pam_sss: password change with two factor authentication
        3e32cb2ad  nss-idmap: check timed muted return code
        a87658e53  krb5: call krb5_auth_cache_creds() if a password is available
        0633e97cf  DESKPROFILE: Fix 'Improper use of negative value'
        db52090e3  AD: sdap_get_ad_tokengroups_done() allocate temporary data on state
        e6ad16e05  AD: do not allocate temporary data on long living context
        430038511  ipa: remove SYSDB_USER_CERT from sub-domain users
        5e04cbb8b  ipa: add SYSDB_USER_MAPPED_CERT for certs in idoverrides

    Thorsten Scherf (1):
        d4a6579a9  IPA: Fixed subdomain typo

    Victor Tapia (1):
        ad286a79c  WATCHDOG: Restart providers with SIGUSR2 after time drift

    amitkuma (3):
        d25646c64  cache_req: Correction of cache_req debug string ID format
        2af80640f  cache: Check for max_id/min_id in cache_req
        52ae76737  MAN: Explain how does auto_private_groups affect subdomains
