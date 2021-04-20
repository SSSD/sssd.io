SSSD 1.16.0 Release Notes
=========================

Highlights
----------

Security fixes
~~~~~~~~~~~~~~

-  This release fixes CVE-2017-12173: Unsanitized input when searching in local cache database. SSSD stores its cached data in an LDAP like local database file using ``libldb.`` To lookup cached data LDAP search filters like ``(objectClass=user)(name=user_name)`` are used. However, in ``sysdb_search_user_by_upn_res()``, the input was not sanitized and allowed to manipulate the search filter for cache lookups. This would allow a logged in user to discover the password hash of a different user.

New Features
~~~~~~~~~~~~

-  SSSD now supports session recording configuration through ``tlog``. This feature enables recording of everything specific users see or type during their sessions on a text terminal. For more information, see the ``sssd-session-recording(5)`` manual page.
-  SSSD can act as a client agent to deliver `Fleet Commander <https://wiki.gnome.org/Projects/FleetCommander>`_ policies defined on an IPA server. Fleet Commander provides a configuration management interface that is controlled centrally and that covers desktop, applications and network configuration.
-  Several new `systemtap <https://sourceware.org/systemtap/>`_ probes were added into various locations in SSSD code to assist in troubleshooting and analyzing performance related issues. Please see the ``sssd-systemtap(5)`` manual page for more information.
-  A new LDAP provide access control mechanism that allows to restrict access based on PAM's rhost data field was added. For more details, please consult the ``sssd-ldap(5)`` manual page, in particular the options ``ldap_user_authorized_rhost`` and the ``rhost`` value of ``ldap_access_filter``.

Performance enhancements
~~~~~~~~~~~~~~~~~~~~~~~~

-  Several attributes in the SSSD cache that are quite often used during cache searches were not indexed. This release adds the missing indices, which improves SSSD performance in large environments.

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  The SSSD libwbclient implementation adjusted its behaviour in order to be compatible with Winbind's return value of wbcAuthenticateUserEx(). This enables the SSSD libwbclient library to work with Samba-4.6 or newer.
-  SSSD's plugin for MIT Kerberos to send the PAC to the PAC responder did not protect the communication with the PAC responder with a mutex. This was causing multi-threaded applications that process the Kerberos PAC to miss a reply from SSSD and then were blocked until the default client timeout of 300 seconds passed. This release adds the mutex, which fixes the PAC responder usage in multi-threaded environments.
-  Previously, SSSD used to refresh several expired sudo rules by combining them into a long LDAP filter. This was ineffective, because the LDAP server had to process the query, but at that point, the client was quite often querying most or all of the sudo rules anyway. In this version, when the number of sudo rules to be refreshed exceeds the value of a new option ``sudo_threshold``, all sudo rules are fetched instead.
-  A bug in the sudo integration that prevented the rules from matching if the user name referenced in that rule was overriden with ``sss_override`` or IPA ID views was fixed
-  When SSSD is configured with ``id_provider=ad``, then a Kerberos configuration is created that instructs libkrb5 to use TCP for communication with the AD DC by default. This would save switching from UDP to TCP, which happens almost every time with the ``ad`` provider due to the PAC attached to the Kerberos ticket.

Packaging Changes
-----------------

-  The ``sss_debuglevel`` and ``sss_cache`` utilities were superseded by ``sssctl`` commands ``sssctl debug-level`` and ``sssctl cache-expire``, respectively. While this change is backwards-compatible in the sense that the old commands continue to work, it is recommended to switch to the ``sssctl`` command which will in future encompass all SSSD administration tasks.
-  Two new manpages, ``sssd-session-recording(5)`` and ``sssd-systemtap(5)`` were added.
-  A new systemtap example script, which is packaged by default at ``/usr/share/sssd/systemtap/dp_request.stp`` was added.
-  A new directory called ``deskprofile`` under the SSSD state directory (typically ``/var/lib/sss/``) was added. SSSD downloads the Fleet Commander profiles into this directory.

Documentation Changes
---------------------

-  The ``ldap_user_certificate`` option has changed its default value in the LDAP provider from "not set" to ``userCertificate;binary``.
-  The ``ldap_access_filter`` option has a new allowed value ``rhost`` to support access control based on the PAM rhost value. The attribute that SSSD reads during the rhost access control can be configured using the new option ``ldap_user_authorized_rhost``.
-  The thresholds after which the IPA and LDAP sudo providers will refresh all sudo rules instead of only the expired ones can be tuned using the ``sudo_threshold`` option.
-  A new provider handler, ``session_provider`` was added. At the moment, only two handlers, ``ipa`` and ``none`` are supported. The IPA session handler is used to fetch the Fleet Commander profiles from an IPA server.
-  The interval after which the IPA session provider will check for new FleetCommander profiles can be configured using the new ``ipa_deskprofile_request_interval`` option.

Tickets Fixed
-------------

-  `#4575 <https://github.com/SSSD/sssd/issues/4575>`_ - CVE-2017-12173: Unsanitized input when searching in local cache database
-  `#4557 <https://github.com/SSSD/sssd/issues/4557>`_ - dbus-1.11.18 caused hangs in cwrap integration tests
-  `#4544 <https://github.com/SSSD/sssd/issues/4544>`_ - sssd_client: add mutex protected call to the PAC responder
-  `#4537 <https://github.com/SSSD/sssd/issues/4537>`_ - sssd incorrectly checks 'try_inotify' thinking it is the wrong section
-  `#4534 <https://github.com/SSSD/sssd/issues/4534>`_ - Issues with certificate mapping rules
-  `#4527 <https://github.com/SSSD/sssd/issues/4527>`_ - Accessing IdM kerberos ticket fails while id mapping is applied
-  `#4517 <https://github.com/SSSD/sssd/issues/4517>`_ - pysss_nss_idmap: py3 constants defined as strings or bytes
-  `#4511 <https://github.com/SSSD/sssd/issues/4511>`_ - getsidbyid does not work with 1.15.3
-  `#4507 <https://github.com/SSSD/sssd/issues/4507>`_ - ERROR at setup of test_kcm_sec_init_list_destroy
-  `#4485 <https://github.com/SSSD/sssd/issues/4485>`_ - Allow fallback from krb5_aname_to_localname to other krb5 plugins
-  `#4487 <https://github.com/SSSD/sssd/issues/4487>`_ - unable to access cifs share using sssd-libwbclient
-  `#4514 <https://github.com/SSSD/sssd/issues/4514>`_ - SUDO doesn't work for IPA users on IPA clients after applying ID Views for them in IPA server
-  `#4504 <https://github.com/SSSD/sssd/issues/4504>`_ - sudo: fall back to the full refresh after reaching a certain threshold
-  `#4499 <https://github.com/SSSD/sssd/issues/4499>`_ - Failures on test_idle_timeout()
-  `#4498 <https://github.com/SSSD/sssd/issues/4498>`_ - sysdb index improvements - missing ghost attribute indexing, unneeded objectclass index etc..
-  `#4393 <https://github.com/SSSD/sssd/issues/4393>`_ - secrets: Per UID secrets quota
-  `#4533 <https://github.com/SSSD/sssd/issues/4533>`_ - Long search filters are created during IPA sudo command + command group retrieval
-  `#4525 <https://github.com/SSSD/sssd/issues/4525>`_ - Change the ldap_user_certificate to userCertificate;binary for the generic LDAP provider as well
-  `#4508 <https://github.com/SSSD/sssd/issues/4508>`_ - Fleet Commander: Add a timeout to avoid contacting the DP too often in case there was no profile fetched in the last login
-  `#4486 <https://github.com/SSSD/sssd/issues/4486>`_ - id root triggers an LDAP lookup
-  `#4348 <https://github.com/SSSD/sssd/issues/4348>`_ - infopipe: org.freedesktop.sssd.infopipe.Groups.Group doesn't show users
-  `#4341 <https://github.com/SSSD/sssd/issues/4341>`_ - SELinux: Use libselinux's getseuserbyname to get the correct seuser
-  `#4340 <https://github.com/SSSD/sssd/issues/4340>`_ - RFE: Log to syslog when sssd cannot contact servers, goes offline
-  `#4339 <https://github.com/SSSD/sssd/issues/4339>`_ - infopipe: List\* with limit = 0 returns 0 results
-  `#4338 <https://github.com/SSSD/sssd/issues/4338>`_ - infopipe: crash when filter doesn't contain '*'
-  `#4287 <https://github.com/SSSD/sssd/issues/4287>`_ - Set udp_preference_limit=0 by sssd-ad using a krb5 snippet
-  `#4036 <https://github.com/SSSD/sssd/issues/4036>`_ - RFE: Deliver FleetCommander URL endpoint from an IPA server
-  `#3934 <https://github.com/SSSD/sssd/issues/3934>`_ - [RFE] Conditionally wrap user terminal with tlog
-  `#4539 <https://github.com/SSSD/sssd/issues/4539>`_ - MAN: Document that full_name_format must be set if the output of trusted domains user resolution should be shortnames only
-  `#4477 <https://github.com/SSSD/sssd/issues/4477>`_ - Unnecessary second log event causing much spam to syslog
-  `#4444 <https://github.com/SSSD/sssd/issues/4444>`_ - MAN: document that attribute 'provider' is not allowed in section 'secrets'
-  `#4426 <https://github.com/SSSD/sssd/issues/4426>`_ - Improve description of 'trusted domain section' in sssd.conf's man page
-  `#4094 <https://github.com/SSSD/sssd/issues/4094>`_ - Add systemtap probes into the top-level data provider requests
-  `#3850 <https://github.com/SSSD/sssd/issues/3850>`_ - CI doesn't work with DNF
-  `#3343 <https://github.com/SSSD/sssd/issues/3343>`_ - Print a warning when enumeration is requrested but disabled
-  `#2940 <https://github.com/SSSD/sssd/issues/2940>`_ - Move header files consumed by both server and client to special folder
-  `#4543 <https://github.com/SSSD/sssd/issues/4543>`_ - Prevent "TypeError: must be type, not classobj"
-  `#4180 <https://github.com/SSSD/sssd/issues/4180>`_ - sssctl: get and set debug level
-  `#4090 <https://github.com/SSSD/sssd/issues/4090>`_ - Merge existing command line tools into sssctl


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_15_3..sssd-1_16_0

    Alexey Kamenskiy (1):
        f34a8330c  LDAP: Add support for rhost access control

    AmitKumar (6):
        3996e3910  Moving headers used by both server and client to special folder
        7aac90a35  ldap_child: Removing duplicate log message
        781d231a1  MAN: Improve description of 'trusted domain section' in sssd.conf's man page
        fdefac9c4  MAN: Improve ipa_hostname description
        efa0a019f  IPA: check if IPA hostname is fully qualified
        c33fa3306  Print a warning when enumeration is requested but disabled

    Fabiano Fidêncio (57):
        9d9039677  CACHE_REQ: Fix warning may be used uninitialized
        1b3425d8c  INTG: Add --with-session-recording=/bin/false to intgcheck's configure
        5d855b5d5  IFP: Change ifp_list_ctx_remaining_capacity() return type
        b0b9222f7  IFP: Don't pre-allocate the amount of entries requested
        8a26d32bc  IPA_ACCESS: Remove not used attribute
        9a18f78f3  IPA: Make ipa_hbac_sysdb_save() more generic
        21909d3b6  IPA: Leave only HBAC specific defines in ipa_hbac_private.h
        e17e37cd0  IPA_ACCESS: Make hbac_get_cache_rules() more generic
        d2a0b4a6a  IPA_ACCESS: Make ipa_purge_hbac() more generic
        0f6234564  IPA_RULES_COMMON: Introduce ipa_common_save_rules()
        ee164913f  IPA_RULES_COMMON: Introduce ipa_common_get_hostgroupname()
        18d898d9c  IPA_ACCESS: Make use of struct ipa_common_entries
        7c1d13935  IPA_COMMON: Introduce ipa_get_host_attrs()
        5b93634c7  UTIL: move {files,selinux}.c under util directory
        6f466e0a3  UTIL: Add sss_create_dir()
        f982039c7  DESKPROFILE: Introduce the new IPA session provider
        b054e7d8c  HBAC: Fix tevent hierarchy in ipa_hbac_rule_info_send()
        9d98e98ab  HBAC: Document ipa_hbac_rule_info_next()'s behaviour
        c9e104f17  HBAC: Remove a cosmetic extra space from an if clause
        dd6a4fb9a  HBAC: Improve readability of ipa_hbac_rule_info_send()
        4b37ee7d3  HBAC: Enforce coding style on ipa_hbac_rule_info_send()
        684a13e8d  HBAC: Enforce coding style ipa_hbac_rule_info_recv()
        85a93ca67  HBAC: Add a debug message in case ipa_hbac_rule_info_next() fails
        85517b576  HBAC: Not having rules should not be logged as error
        4a3117020  DESKPROFILE: Add ipa_deskprofile_request_interval
        b54d79cf3  NEGCACHE: Add some comments about each step of sss_ncache_prepopulate()
        1e7b7da3a  NEGCACHE: Always add "root" to the negative cache
        e54764d62  TEST_NEGCACHE: Test that "root" is always added to ncache
        9908bdc97  NEGCACHE: Descend to all subdomains when adding user/groups
        8888d7a46  CACHE_REQ: Don't error out when searching by id = 0
        431c7508e  NSS: Don't error out when deleting an entry which has id = 0 from the memcache
        3ad33ca77  NEGCACHE: Add root's uid/gid to ncache
        b4b3d0642  TEST_NEGCACHE: Ensure root's uid and gid are always added to ncache
        b4195db08  CONFDB: Set a default value for subdomain_refresh_interval in case an invalid value is set
        362b8a94c  SDAP: Add a debug message to explain why a backend was marked offline
        5a117d360  SDAP: Don't call be_mark_offline() because sdap_id_conn_data_set_expire_timer() failed
        9375eae59  PYTHON: Define constants as bytes instead of strings
        e5c42c263  SYSDB: Add sysdb_search_by_orig_dn()
        9a44e7830  TESTS: Add tests for sysdb_search_{users,groups}_by_orig_dn()
        a5e9d34fd  IPA: Use sysdb_search_*_by_orig_dn() _hbac_users.c
        4c508463b  SDAP: Use sysdb_search_*_by_orig_dn() in sdap_async_nested_groups.c
        e3d9ce0ac  SDAP: Use sysdb_search_*_by_orig_dn() in sdap_async_groups.c
        59db26782  IPA: Use sysdb_search_*_by_orig_dn() in _subdomains_ext_group.c
        3ec6f2902  MAN: Add a note about the output of all commands when using domain_resolution_order
        58a9b4f0b  RESOLV: Fix "-Werror=null-dereference" caught by GCC
        f194bd0fa  SIFP: Fix "-Wjump-misses-init" caught by GCC
        0e6248c60  NSS: Fix "-Wold-style-definition" caught by GCC
        1a9cdc6ba  TESTS: Fix "-Werror=null-dereference" caught by GCC
        76ff0b1dd  TOOLS: Fix "-Wstack-protector" caught by GCC
        47863dee6  SSSCTL: Fix "-Wshadow" warning caught by GCC
        1ef1056e7  SSSCTL: Fix "-Wunitialized" caught by GCC
        3cb4592e2  SSSCTL: Use get_ prefix for the sssctl_attr_fn functions
        01f852fcb  TESTS: Fix "-Wshadow" caught by GCC
        d8d49ae91  RESPONDER: Fix "-Wold-style-definition" caught by GCC
        82464078c  PAM: Avoid overwriting pam_status in _lookup_by_cert_done()
        60ec0db01  DP: Fix the output type used in dp_req_recv_ptr()
        1185cbce8  DP: Log to syslog whether it's online or offline

    Jakub Hrozek (29):
        3b9460869  Updating the version for the 1.15.4 release
        47f73fbf3  MAN: Don't tell the user to autostart sssd-kcm.service; it's socket-enabled
        137e105ac  TESTS: Add wrappers to request a user or a group by ID
        5883b99fa  TESTS: Add files provider tests that request a user and group by ID
        6c3841099  TESTS: Add regression tests to try if resolving root and ID 0 fails as expected
        9787bc589  CONFDB: Do not crash with an invalid domain_type or case_sensitive value
        45e322191  IPA: Only attempt migration for the joined domain
        2d40ce078  SECRETS: Remove unused declarations
        9ef185255  SECRETS: Do not link with c-ares
        7a162ca3e  SECRETS: Store quotas in a per-hive configuration structure
        4db56d8c9  SECRETS: Read the quotas for cn=secrets from [secrets/secrets] configuration subsection
        392f48c03  SECRETS: Rename local_db_req.basedn to local_db_req.req_dn
        197da1639  SECRETS: Use separate quotas for /kcm and /secrets hives
        0558f270b  TESTS: Test that ccaches can be stored after max_secrets is reached for regular non-ccache secrets
        6b3bab516  SECRETS: Add a new option to control per-UID limits
        109ed7ca1  SECRETS: Support 0 as unlimited for the quotas
        4d1e380fe  TESTS: Relax the assert in test_idle_timeout
        cd2b8fd42  IPA: Reword the DEBUG message about SRV resolution on IDM masters
        a309525cc  IPA: Only generate kdcinfo files on clients
        3bcf6b17a  MAN: Improve failover documentation by explaining the timeout better
        e8bad995f  MAN: Document that the secrets provider can only be specified in a per-client section
        280f69cf2  TESTS: Use NULL for pointer, not 0
        dee665060  SUDO: Use initgr_with_views when looking up a sudo user
        7f68de6c2  KCM: Do not leak newly created ccache in case the name is malformed
        3e4fe6cc5  KCM: Use the right memory context
        613a832d5  KCM: Add some forgotten NULL checks
        381bc154e  GPO: Don't use freed LDAPURLDesc if domain for AD DC cannot be found
        9a839b298  Updating the translation for the 1.16.0 release
        2de0072db  Updating the version for the 1.16.0 release

    Justin Stephenson (8):
        cfe87ca0c  SELINUX: Use getseuserbyname to get IPA seuser
        d46d59e78  DP: Add Generic DP Request Probes
        1182dd93a  CONTRIB: Add DP Request analysis script
        f199c7491  MAN: Add sssd-systemtap man page
        d2c614143  SSSCTL: Move sss_debuglevel to sssctl debug-level
        da19eaea9  SSSCTL: Replace sss_debuglevel with shell wrapper
        f74408e37  SSSCTL: Add cache-expire command
        bc854800c  IPA: Add threshold for sudo searches

    Lukas Slebodnik (31):
        7ecf21b35  SPEC: Use language file for sssd-kcm
        eec0b39ed  SHARED: Return warning back about minimal header files
        a24e735d3  intg: Disable add_remove tests
        08cb2a344  SPEC: require http-parser only on rhel7.4
        dc5da7411  intg: Increase startup timeouts for kcm and secrets
        725d04cd2  libwbclient: Change return code for wbcAuthenticateUserEx
        aede6a1f4  libwbclient: Fix warning statement with no effect
        fa0d29fe3  SPEC: rhel8 will have python3 as well
        8302d6da8  SPEC: Fix unowned directory
        22abbb479  certmap: Suppress warning Wmissing-braces
        2e72ababb  cache_req: Look for name attribute also in nss_cmd_getsidbyid
        f5d440000  SPEC: Update owner and mode for /var/lib/sss/deskprofile
        51c4da6e4  CI: Use dnf 2.0 for installation of packages in fedora
        53f74f542  Revert "PYTHON: Define constants as bytes instead of strings"
        cc4d6435e  pysss_nss_idmap: return same type as it is in module constants
        e7fd33642  pysss_nss_idmap: Fix typos in python documentation
        895584001  CONFIG: Fix schema for try_inotify
        c20a9efbf  SPEC: Fix detecting of minor release
        39e300314  Fix warning declaration of 'index' shadows a global declaration
        82c36227e  intg: Fix execution with dbus-1.11.18
        90cbf7bc0  TOOLS: Log redirection info for sss_debuglevel to stderr
        401514216  TOOLS: Print Better usage for sssctl debug-level
        37b108ec4  TOOLS: Hide option --debug in sssctl
        035bed97b  intg: Fix pep8 warnings in config.py template
        a3bed9df5  intg: Let python paths be configurable
        948c1a4d4  intg: prevent "TypeError: must be type, not classobj"
        d82741b1a  intg: Prefer locally built python modules
        ebbd9a2b5  ds_openldap: Extract functionality to protected methods
        36df33cd4  intg: Create FakeAD class based on openldap
        da7a3c347  intg: Add sanity tests for pysss_nss_idmap
        6ef14c5c9  Revert "IPA: Only generate kdcinfo files on clients"

    Marlena Marlenowska (1):
        0526dde7f  IDMAP: Prevent colision for explicitly defined slice.

    Nikolai Kondrashov (16):
        cb89693cf  CACHE_REQ: Propagate num_results to cache_req_state
        c31065ecc  NSS: Move shell options to common responder
        9759333b3  NSS: Move nss_get_shell_override to responder utils
        555f43b49  CONFIG: Add session_recording section
        d802eba25  BUILD: Support configuring session recording shell
        99b96048b  UTIL: Add session recording conf management module
        29dd45610  RESPONDER: Add session recording conf loading
        5ea60d18d  DP: Add session recording conf loading
        90fb7d3e6  SYSDB: Add sessionRecording attribute macro
        bac0c0df3  DP: Load override_space into be_ctx
        24b3a7b91  DP: Overlay sessionRecording attribute on initgr
        382a972a8  CACHE_REQ: Pull sessionRecording attrs from initgr
        836dae913  NSS: Substitute session recording shell
        49d24ba63  PAM: Export original shell to tlog-rec-session
        53a4219e2  INTG: Add session recording tests
        27c30eb5f  MAN: Describe session recording configuration

    Pavel Březina (4):
        200787df7  DP: Update viewname for all providers
        a5f300adf  sudo: add a threshold option to reduce size of rules refresh filter
        ed7767aa1  IFP: fix typo in option name in man pages
        1024dbcba  IFP: parse ping arguments in codegen

    Petr Čech (4):
        d84e841ed  IFP: Do not fail when a GHOST group is not found
        6bd6571df  UTIL: Set udp_preference_limit=0 in krb5 snippet
        5fe1e8ba9  IFP: Filter with * in infopipe group methods
        3c31ce392  IFP: Fix of limit = 0 (unlimited result)

    Sumit Bose (15):
        d1b2a3394  libwbclient-sssd: update interface to version 0.14
        3f94a979e  localauth plugin: change return code of sss_an2ln
        b4e45531b  tests: add unit tests for krb5 localauth plugin
        0475a98d3  IPA: format fixes
        a20fb9cbd  certmap: add OpenSSL implementation
        f00591a46  ipa: make sure view name is initialized at startup
        f5a8cd60c  certmap: make sure eku_oid_list is always allocated
        f2e70ec74  IPA: fix handling of certmap_ctx
        9acdf51bf  sysdb: add missing indices
        11a030ac6  IDMAP: add a unit test
        1f331476e  sssd_client: add mutex protected call to the PAC responder
        ce68b4ff2  BUILD: Accept krb5 1.16 for building the PAC plugin
        1f2662c8f  sysdb: sanitize search filter input
        c2dec0dc7  IPA: sanitize name in override search filter
        28f9c2051  sss_client: refactor internal timeout handling

    Yuri Chornoivan (3):
        77e5c3fc2  Fix minor typos
        1afc79695  Fix minor typos
        ba2fb2c7b  Fix minor typos in docs

    amitkuma (2):
        d1d6f3a7f  ldap: Change ldap_user_certificate to userCertificate;binary
        b07852825  python: Changing class declaration from old to new-style type
