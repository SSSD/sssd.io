SSSD 1.15.3 Release Notes
=========================

Highlights
----------

New Features
~~~~~~~~~~~~

-  In a setup where an IPA domain trusts an Active Directory domain, it is now possible to `define the domain resolution order <http://www.freeipa.org/page/Releases/4.5.0#AD_User_Short_Names>`_. Starting with this version, SSSD is able to read and honor the domain resolution order, providing a way to resolve Active Directory users by just their short name. SSSD also supports a new option ``domain_resolution_order`` applicable in the ``[sssd]`` section that allows to configure short names for AD users in setup with ``id_provider=ad`` or in a setup with an older IPA server that doesn't support the ``ipa config-mod --domain-resolution-order`` configuration option. Also, it is now possible to use ``use_fully_qualified_names=False`` in a subdomain configuration, but please note that the user and group output from trusted domains will always be qualified to avoid conflicts.

   -  Design page - `Shortnames in trusted domains <../../design_pages/shortnames.md>`_

-  SSSD ships with a new service called KCM. This service acts as a storage for Kerberos tickets when ``libkrb5`` is configured to use ``KCM:`` in ``krb5.conf``. Compared to other Kerberos credential cache types, KCM is better suited for containerized environments and because the credential caches are managed by a stateful daemon, in future releases will also allow to renew tickets acquired outside SSSD (e.g. with ``kinit``) or provide notifications about ticket changes. This feature is optional and can be disabled by selecting ``--without-kcm`` when configuring the SSSD build.

   -  Design page - `KCM server for SSSD <../../design_pages/kcm.md>`_
   -  \`NOTE\`: There are several known issues in the ``KCM`` responder that will be handled in the next release such as `issues with very large tickets <https://github.com/SSSD/sssd/issues/4413>`_ or `tracking the SELinux label of the peer <https://github.com/SSSD/sssd/issues/4461>`_ or even one `intermittent crash <https://github.com/SSSD/sssd/issues/4481>`_. There are also some differences between how SSSD's KCM server works compared to Heimdal's KCM server such as `visibility of ccaches by root <https://github.com/SSSD/sssd/issues/4405>`_.

-  Support for user and group resolution through the D-Bus interface and authentication and/or authorization through the PAM interface even for setups without UIDs or Windows SIDs present on the LDAP directory side. This enhancement allows SSSD to be used together with `apache modules <https://github.com/adelton/mod_lookup_identity>`_ to provide identities for applications

   -  Design page - `Support for non-POSIX users and groups <../../design_pages/non_posix_support.md>`_

-  SSSD ships a new public library called ``libsss_certmap`` that allows a flexible and configurable way of mapping a certificate to a user identity. This is required e.g. in environments where it is not possible to add the certificate to the LDAP user entry, because the certificates are issued externally or the LDAP schema cannot be modified. Additionally, specific matching rules allow a specific certificate on a smart card to be selected for authentication.

   -  Design page - `Matching and Mapping Certificates <../../design_pages/matching_and_mapping_certificates.md>`_

-  The Kerberos locator plugin can be disabled using an environment variable ``SSSD_KRB5_LOCATOR_DISABLE``. Please refer to the ``sssd_krb5_locator_plugin`` manual page for mode details.
-  The ``sssctl`` command line tool supports a new command ``user-checks`` that enables the administrator to check whether a certain user should be allowed or denied access to a certain PAM service.
-  The ``secrets`` responder now forwards requests to a proxy Custodia back end over a secure channel.

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  The IPA HBAC evaluator no longer relies on ``originalMemberOf`` attributes to construct the list of groups the user is a member of. Maintaining the ``originalMemberOf`` attribute was unreliable and was causing intermittent HBAC issues.
-  A bug where the cleanup operation might erroneously remove cached users during their cache validation in case SSSD was set up with ``enumerate=True`` was fixed.
-  Several bugs related to configuration of trusted domains were fixed, in particular handling of custom LDAP search bases set for trusted domains.
-  Password changes for users from trusted Active Directory domains were fixed

Packaging Changes
-----------------

-  A new KCM responder was added along with a manpage. The upstream reference specfile packages the responder in its own subpackage called ``sssd-kcm`` and a krb5.conf snippet that enables the ``KCM`` credentials cache simply by installing the subpackage
-  The ``libsss_certmap`` library was packaged in a separate package. There is also a ``libsss_certmap-devel`` subpackage in the upstream packaging.

Documentation Changes
---------------------

-  ``sssd-kcm`` and ``libsss_certmap`` are documented in their own manual pages.
-  A new option ``domain_resolution_order`` was added. This option allows to specify the lookup order (especially w.r.t. trusted domains) that sssd will follow. Please see the `Shortnames in trusted domains <../../design_pages/shortnames.md>`_ design page. for mode details.
-  New options ``pam_app_services`` and ``domain_type`` were added. These options can be used to only limit certain PAM services to reach certain SSSD domains that should only be exposed to non-OS applications. For more details, refer to the `Support for non-POSIX users and groups <../../design_pages/non_posix_support.md>`_ design page.

..

-  The ``secrets`` responder supports several new options related to TLS setup and handling including ``verify_peer``, ``verify_host``, ``capath``, ``cacert`` and ``cert``. These options are all described in the ``sssd-secrets`` manual page.

Tickets Fixed
-------------

-  `#4451 <https://github.com/SSSD/sssd/issues/4451>`_ - calling nspr_nss_setup/cleanup repeatedly in sss_encrypt SIGABRTs NSS eventually
-  `#4479 <https://github.com/SSSD/sssd/issues/4479>`_ - ad_account_can_shortcut: allow shortcut for unhandled IDs
-  `#4474 <https://github.com/SSSD/sssd/issues/4474>`_ - files provider should not use LOCAL_pam_handler but call the backend
-  `#4462 <https://github.com/SSSD/sssd/issues/4462>`_ - Create a function to copy search bases between sdap_domain structures
-  `#4458 <https://github.com/SSSD/sssd/issues/4458>`_ - Loading enterprise principals doesn't work with a primed cache
-  `#4453 <https://github.com/SSSD/sssd/issues/4453>`_ - IPA client cannot change AD Trusted User password
-  `#4445 <https://github.com/SSSD/sssd/issues/4445>`_ - Segfault in access_provider = krb5 is set in sssd.conf due to an off-by-one error when constructing the child send buffer
-  `#4437 <https://github.com/SSSD/sssd/issues/4437>`_ - python-sssdconfig doesn't parse hexadecimal debug_level, resulting in set_option(): /usr/lib/python2.7/site-packages/SSSDConfig/**init**.py killed by TypeError
-  `#4435 <https://github.com/SSSD/sssd/issues/4435>`_ - Accept changed principal if krb5_canonicalize=True
-  `#4431 <https://github.com/SSSD/sssd/issues/4431>`_ - man: Update option "ipa_server_mode=True" in "man sssd-ipa"
-  `#4430 <https://github.com/SSSD/sssd/issues/4430>`_ - SSSD doesn't handle conflicts between users from trusted domains with the same name when shortname user resolution is enabled
-  `#4425 <https://github.com/SSSD/sssd/issues/4425>`_ - MAN: The timeout option doesn't say after how many heartbeats will the process be killed
-  `#4424 <https://github.com/SSSD/sssd/issues/4424>`_ - ad provider: Child domains always use autodiscovered search bases
-  `#4420 <https://github.com/SSSD/sssd/issues/4420>`_ - sss_nss_getlistbycert() does not return results from multiple domains
-  `#4418 <https://github.com/SSSD/sssd/issues/4418>`_ - sss_override doesn't work with files provider
-  `#4416 <https://github.com/SSSD/sssd/issues/4416>`_ - subdomain_homedir is not present in cfg_rules.ini
-  `#4407 <https://github.com/SSSD/sssd/issues/4407>`_ - domain_to_basedn() function should use SDAP_SEARCH_BASE value from the domain code
-  `#4406 <https://github.com/SSSD/sssd/issues/4406>`_ - sssd-ad man page should clarify that GSSAPI is used
-  `#4404 <https://github.com/SSSD/sssd/issues/4404>`_ - minor typo fix that might have big impact
-  `#4391 <https://github.com/SSSD/sssd/issues/4391>`_ - sssd_be crashes if ad_enabled_domains is selected
-  `#4389 <https://github.com/SSSD/sssd/issues/4389>`_ - Allow to disable krb5 locator plugin selectively
-  `#4388 <https://github.com/SSSD/sssd/issues/4388>`_ - [abrt] [faf] sssd: vfprintf(): /usr/libexec/sssd/sssd_be killed by 11
-  `#4384 <https://github.com/SSSD/sssd/issues/4384>`_ - ifp: Users.FindByCertificate fails when certificate contains data before encapsilation boundary
-  `#4375 <https://github.com/SSSD/sssd/issues/4375>`_ - Include sssd-secrets in SEE ALSO section of sssd.conf man page
-  `#4374 <https://github.com/SSSD/sssd/issues/4374>`_ - Properly fall back to local Smartcard authentication
-  `#4371 <https://github.com/SSSD/sssd/issues/4371>`_ - The option enable_files_domain does not work if sssd is not compiled with --enable-files-domain
-  `#4370 <https://github.com/SSSD/sssd/issues/4370>`_ - sssd failed to start with missing /etc/sssd/sssd.conf if compiled without --enable-files-domain
-  `#4363 <https://github.com/SSSD/sssd/issues/4363>`_ - Issue processing ssh keys from certificates in ssh respoder
-  `#4475 <https://github.com/SSSD/sssd/issues/4475>`_ - Idle nss file descriptors should be closed
-  `#4455 <https://github.com/SSSD/sssd/issues/4455>`_ - getent failed to fetch netgroup information after changing default_domain_suffix to ADdomin in /etc/sssd/sssd.conf
-  `#4386 <https://github.com/SSSD/sssd/issues/4386>`_ - Config file validator doesn't process entries from application domain
-  `#4362 <https://github.com/SSSD/sssd/issues/4362>`_ - Wrong pam return code for user from subdomain with
-  `#4360 <https://github.com/SSSD/sssd/issues/4360>`_ - Wrong principal found with ad provider and long host name
-  `#4448 <https://github.com/SSSD/sssd/issues/4448>`_ - Wrong search base used when SSSD is directly connected to AD child domain
-  `#4433 <https://github.com/SSSD/sssd/issues/4433>`_ - sssd goes offline when renewing expired ticket
-  `#4421 <https://github.com/SSSD/sssd/issues/4421>`_ - LDAP to IPA migration doesn't work in master
-  `#4419 <https://github.com/SSSD/sssd/issues/4419>`_ - org.freedesktop.sssd.infopipe.GetUserGroups does not resolve groups into names with AD
-  `#4410 <https://github.com/SSSD/sssd/issues/4410>`_ - SSSD should use memberOf, not originalMemberOf to evaluate group membership for HBAC rules
-  `#4409 <https://github.com/SSSD/sssd/issues/4409>`_ - Per-subdomain LDAP filter is not applied for subsequent subdomains
-  `#4403 <https://github.com/SSSD/sssd/issues/4403>`_ - Infopipe method ListByCertificate does not return the users with overrides
-  `#4402 <https://github.com/SSSD/sssd/issues/4402>`_ - crash in sssd-kcm due to a race-condition between two concurrent requests
-  `#4399 <https://github.com/SSSD/sssd/issues/4399>`_ - ldap_purge_cache_timeout in RHEL7.3 invalidate most of the entries once the cleanup task kicks in
-  `#4392 <https://github.com/SSSD/sssd/issues/4392>`_ - fiter_users and filter_groups stop working properly in v 1.15
-  `#4381 <https://github.com/SSSD/sssd/issues/4381>`_ - User lookup failure due to search-base handling
-  `#4377 <https://github.com/SSSD/sssd/issues/4377>`_ - gpo_child fails when log is enabled in smb
-  `#4351 <https://github.com/SSSD/sssd/issues/4351>`_ - SSSD in server mode iterates over all domains for group-by-GID requests, causing unnecessary searches
-  `#4343 <https://github.com/SSSD/sssd/issues/4343>`_ - Support delivering non-POSIX users and groups through the IFP and PAM interfaces
-  `#4083 <https://github.com/SSSD/sssd/issues/4083>`_ - [RFE] Use one smartcard and certificate for authentication to distinct logon accounts
-  `#4042 <https://github.com/SSSD/sssd/issues/4042>`_ - [RFE] Short name input format with SSSD for users from all domains when domain autodiscovery is used or when SSSD acts as an IPA client for server with IPA-AD trusts
-  `#3928 <https://github.com/SSSD/sssd/issues/3928>`_ - [RFE] KCM ccache daemon in SSSD
-  `#4446 <https://github.com/SSSD/sssd/issues/4446>`_ - krb5: properly handle 'password expired' information retured by the KDC during PKINIT/Smartcard authentication
-  `#4434 <https://github.com/SSSD/sssd/issues/4434>`_ - IPA: do not lookup IPA users via extdom plugin
-  `#4432 <https://github.com/SSSD/sssd/issues/4432>`_ - Handle certmap errors gracefully during user lookups
-  `#4422 <https://github.com/SSSD/sssd/issues/4422>`_ - Properly support IPA's promptusername config option
-  `#4414 <https://github.com/SSSD/sssd/issues/4414>`_ - Dbus activate InfoPipe does not answer some initial request
-  `#4412 <https://github.com/SSSD/sssd/issues/4412>`_ - Smart card login fails if same cert mapped to IdM user and AD user
-  `#4385 <https://github.com/SSSD/sssd/issues/4385>`_ - application domain requires inherit_from and cannot be used separately
-  `#4358 <https://github.com/SSSD/sssd/issues/4358>`_ - expect sss_ssh_authorizedkeys and sss_ssh_knownhostsproxy manuals to be packaged into sssd-common package
-  `#4330 <https://github.com/SSSD/sssd/issues/4330>`_ - selinux_provider fails in a container if libsemanage is not available
-  `#4301 <https://github.com/SSSD/sssd/issues/4301>`_ - D-Bus GetUserGroups method of sssd is always qualifying all group names
-  `#4273 <https://github.com/SSSD/sssd/issues/4273>`_ - Smartcard authentication with UPN as logon name might fail
-  `#4243 <https://github.com/SSSD/sssd/issues/4243>`_ - [RFE] Read prioritized list of trusted domains for unqualified ID resolution from IDM server
-  `#4225 <https://github.com/SSSD/sssd/issues/4225>`_ - [sssd-secrets] https proxy talks plain http
-  `#4215 <https://github.com/SSSD/sssd/issues/4215>`_ - sssd does not refresh expired cache entries with enumerate=true
-  `#4098 <https://github.com/SSSD/sssd/issues/4098>`_ - sssctl: distinguish between autodiscovered and joined domains
-  `#3981 <https://github.com/SSSD/sssd/issues/3981>`_ - The member link is not removed when the last group's nested member goes away
-  `#3755 <https://github.com/SSSD/sssd/issues/3755>`_ - Add SSSD domain as property to user on D-Bus
-  `#2540 <https://github.com/SSSD/sssd/issues/2540>`_ - sss_ssh_knownhostsproxy prevents connection if the network is unreachable via one IP address
-  `#4361 <https://github.com/SSSD/sssd/issues/4361>`_ - sssctl config-check does not give any error when default configuration file is not present
-  `#4325 <https://github.com/SSSD/sssd/issues/4325>`_ - RFE: Create troubleshooting tool to check authentication, authorization and extended attribute lookup
-  `#4166 <https://github.com/SSSD/sssd/issues/4166>`_ - RFE to add option of check user access in SSSD


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_15_2..sssd-1_15_3

    AmitKumar (2):
        bb1543000  MAN: The timeout option doesn't say after how many heartbeats will the process be killed
        2bd5bb451  MAN: Updating option ipa_server_mode in man sssd-ipa

    David Kupka (1):
        5231ba679  libsss_certmap: Accept certificate with data before header

    Fabiano Fidêncio (40):
        dcc52d9c6  CACHE_REQ: Descend into subdomains on lookups
        a3442e4a2  NSS/TESTS: Improve setup/teardown for subdomains tests
        5856a621a  NSS/TESTS: Include searches for non-fqnames members of a subdomain
        2e85b015d  SYSDB: Add methods to deal with the domain's resolution order
        723d514f6  SYSDB/TESTS: Add tests for the domain's resolution order methods
        3cbf0e7b6  IPA: Get ipaDomainsResolutionOrder from ipaConfig
        17ab121a6  IPA_SUBDOMAINS: Rename _refresh_view() to _refresh_view_name()
        fb81f337b  IPA: Get ipaDomainsResolutionOrder from IPA ID View
        34228050a  DLINKLIST: Add DLIST_FOR_EACH_SAFE macro
        66c8e92eb  CACHE_REQ: Make use of domainResolutionOrder
        1e437af95  UTIL: Expose replace_char() as sss_replace_char()
        163855685  Add domain_resolution_order config option
        a3faad0e4  RESPONDER: Fallback to global domain resolution order in case the view doesn't have this option set
        ed518f61f  NSS/TESTS: Improve non-fqnames tests
        dae798231  CACHE_REQ: Allow configurationless shortname lookups
        f9bac0275  CACHE_REQ_DOMAIN: Add some comments to cache_req_domain_new_list_from_string_list()
        213048fd9  RESPONDER_COMMON: Improve domaiN_resolution_order debug messages
        b78febe4c  CACHE_REQ_DOMAIN: debug the set domain resolution order
        255ea3674  NSS: Fix typo inigroups -> initgroups
        251a3b2b9  LDAP: Remove duplicated debug message
        2644a8ba6  CONTRIB: Force single-thread install to workaround concurrency issues
        df4b24bed  LDAP/AD: Do not fail in case rfc2307bis_nested_groups_recv() returns ENOENT
        f24ee5cca  CACHE_REQ: Add a new cache_req_ncache_filter_fn() plugin function
        180e0b282  CACHE_REQ_RESULT: Introduce cache_req_create_ldb_result_from_msg_list()
        4ef0b19a5  CACHE_REQ: Make use of cache_req_ncache_filter_fn()
        6a1da829e  CACHE_REQ: Avoid using of uninitialized value
        1a89fc33d  CACHE_REQ: Ensure the domains are updated for "filter" related calls
        c8193b160  CACHE_REQ: Simplify _search_ncache_filter()
        4c09cd008  CACHE_REQ_SEARCH: Check for filtered users/groups also on cache_req_send()
        13205258c  INTG_TESTS: Add one more test for filtered out users/groups
        01c6bb9b4  SYSDB: Return ERR_NO_TS when there's no timestamp cache present
        347be58e1  SYSDB: Internally expose sysdb_search_ts_matches()
        8ad57e177  SYSDB: Make the usage of the filter more generic for search_ts_matches()
        9883d1e29  SYSDB_OPS: Mark an entry as expired also in the timestamp cache
        a71f1a655  SYSDB_OPS: Invalidate a cache entry also in the ts_cache
        41708e1e5  SYSDB: Introduce _search_{users,groups}_by_timestamp()
        05e579691  LDAP_ID_CLEANUP: Use sysdb_search_*_by_timestamp()
        865268913  RESPONDER: Use fqnames as output when needed
        fa2fc8a29  DOMAIN: Add sss_domain_info_{get,set}_output_fqnames()
        b294f9f08  INTG/FILES_PROVIDER: Test user and group override

    Jakub Hrozek (70):
        012ee7c3f  Updating the version for the 1.15.3 release
        3a4a88259  UTIL: iobuf: Make input parameter for the readonly operation const
        24889dc5e  UTIL: Fix a typo in the tcurl test tool
        c194e8d7c  UTIL: Add SAFEALIGN_COPY_UINT8_CHECK
        4f511a4c5  UTIL: Add utility macro cli_creds_get_gid()
        5f7f45a64  UTIL: Add type-specific getsetters to sss_iobuf
        1dbf09404  UTIL: krb5 principal (un)marshalling
        b9c563c29  KCM: Initial responder build and packaging
        9dcdbf596  KCM: request parsing and sending a reply
        bea0dc79f  KCM: Implement an internal ccache storage and retrieval API
        70fe6e2bb  KCM: Add a in-memory credential storage
        1ec4198f3  KCM: Implement KCM server operations
        ba89271f5  MAN: Add a manual page for sssd-kcm
        0700118d8  TESTS: Add integration tests for the KCM responder
        8bb2fcbce  SECRETS: Create DB path before the operation itself
        73ce539aa  SECRETS: Return a nicer error message on request with no PUT data
        60612b5fb  SECRETS: Store ccaches in secrets for the KCM responder
        c9db8b8b1  TCURL: Support HTTP POST for creating containers
        cac0db2f8  KCM: Store ccaches in secrets
        35c9dfe9b  KCM: Make the secrets ccache back end configurable, make secrets the default
        2b5518eea  KCM: Queue requests by the same UID
        e89ba9573  KCM: Idle-terminate the responder if the secrets back end is used
        6324eaf1f  CONFDB: Introduce SSSD domain type to distinguish POSIX and application domains
        825e8bf2f  CONFDB: Allow configuring [application] sections as non-POSIX domains
        cee85e8fb  CACHE_REQ: Domain type selection in cache_req
        35f0f5ff9  IFP: Search both POSIX and non-POSIX domains
        b010f24f4  IFP: ListByName: Don't crash when no results are found
        57eeec5d7  PAM: Remove unneeded memory context
        3e789aa0b  PAM: Add application services
        5f7f249f2  SYSDB: Allow storing non-POSIX users
        901396366  SYSDB: Only generate new UID in local domain
        ed0cdfcac  LDAP: save non-POSIX users in application domains
        3e3980617  LDAP: Relax search filters in application domains
        861ab44e8  KRB5: Authenticate users in a non-POSIX domain using a MEMORY ccache
        7d7304988  KCM: Fix off-by-one error in secrets key parsing
        7c074ba2f  Move sized_output_name() and sized_domain_name() into responder common code
        c9a73bb6f  IFP: Use sized_domain_name to format the groups the user is a member of
        ef019268d  IPA: Improve DEBUG message if a group has no ipaNTSecurityIdentifier
        53e9a5aef  LDAP: Allow passing a NULL map to sdap_search_bases_ex_send
        337dd8a87  IPA: Use search bases instead of domain_to_basedn when fetching external groups
        734e73257  CONFDB: Fix standalone application domains
        dfe05f505  AD: Make ad_account_can_shortcut() reusable by SSSD on an IPA server
        7410f735b  KRB5: Advise the user to inspect the krb5_child.log if the child doesn't return a valid response
        fb51bb68e  KCM: Fix the per-client serialization queue
        274489b09  TESTS: Add a test for parallel execution of klist
        3e3034199  IPA: Avoid using uninitialized ret value when skipping entries from the joined domain
        eb404bcdb  IPA: Return from function after marking a request as finished
        c92e49144  HBAC: Do not rely on originalMemberOf, use the sysdb memberof links instead
        89726be5a  test_kcm: Remove commented code
        5d9df623e  TESTS: Fix pep8 errors in test_kcm.py
        af435c498  TESTS: Fix pep8 errors in test_secrets.py
        84ae0c434  TESTS: Fix pep8 errors in test_ts_cache.py
        ed15b405f  RESP: Provide a reusable request to fully resolve incomplete groups
        c59b73626  IFP: Only format the output name to the short version before output
        95acbbb3f  IFP: Resolve group names from GIDs if required
        f772649cb  KRB5: Fix access_provider=krb5
        15a76bb7b  IFP: Fix error handling in ifp_user_get_attr_handle_reply()
        fcfc1450a  IPA: Enable enterprise principals even if there are no changes to subdomains
        fdecdc416  README: Add a hint on how to submit bugs
        509cd7650  README: Add social network links
        75a7bd76a  Fix fedorahosted links in BUILD.txt
        d67a89931  README.md: Point to our releases on pagure
        422217c7e  RESPONDERS: Fix terminating idle connections
        d24335e9b  TESTS: Integration test for idle timeout
        74e2415f0  MAN: Document that client_idle_timeout can't be shorter than 10 seconds
        a6f606117  CRYPTO: Do not call NSS_Shutdown after every operation
        865cbab7d  KRB5: Return invalid credentials internally when attempting to renew an expired TGT
        4b4603fb8  KCM: Fix Description of sssd-kcm.socket
        d2ed40c0e  Remove the locale tag from zanata.xml
        b47fd11a2  Updating translations for the 1.15.3 release

    Justin Stephenson (9):
        a04bef313  IPA: Add s2n request to string function
        cd83aead3  IPA: Enhance debug logging for ipa s2n operations
        0c5f463e9  IPA: Improve s2n debug message for missing ipaNTSecurityIdentifier
        133ee2239  MAN: AD Provider GSSAPI clarification
        e98d085b5  DP: Reduce Data Provider log level noise
        beab60d88  CONFIG: Add subdomain_homedir to config locations
        a3f6d90c3  SSSCTL: Add parent or trusted domain type
        925a14d50  LDAP: Fix nesting level comparison
        6d57cd501  TESTS: Update zero nesting level test

    Lukas Slebodnik (57):
        3c071c4d6  MAN: Mention sssd-secrets in "SEE ALSO" section
        7c67679ba  CONFIGURE: Fix fallback if pkg-config for uuid is missing
        8e785c747  intg: fix configure failure with strict cflags
        f75ba99fc  intg: Remove bashism from intgcheck-prepare
        84fecc2fd  BUILD: Fix compilation of libsss_certmap with libcrypto
        3509bb03e  CONFDB: Fix handling of enable_files_domain
        c6f1bc327  UTIL: Use max 15 characters for AD host UPN
        bf8f11977  SPEC: Drop conditional build for krb5_local_auth_plugin
        363e4c407  README: Update links to mailing lists
        0e8f0c06c  SECRETS: remove unused variable
        b70ec63cc  cache_req: Avoid bool in switch/case
        386a97820  SPEC: Update processing of translation in %install
        ffa05d220  SPEC: Move systemd service sssd-ifp.service to right package
        1b1a89c28  SPEC: Add missing scriptlets for package sssd-dbus
        dd7128871  SPEC: Use correct package for translated sssd-ifp man page
        e821ed507  SPEC: Move man page for sss_rpcidmapd to the right package
        60327984a  SPEC: Use correct package for translated sss_ssh* man pages
        fc57f91b4  SPEC: Use correct package for translated sssctl man pages
        b2175f271  SPEC: Use correct package for translated idmap_sss man pages
        2915214ba  SPEC: Use correct package for translated sss_certmap man pages
        8843feb6f  SPEC: Use correct package for translated sssd-kcm man pages
        8bbe26cfc  SPEC: Move files provider files within package
        fa1cea867  SPEC: Move kcm scriptlets to systemd section
        9055ed29a  SPEC: Call ldconfig in libsss_certmap scriptlets
        1cfbec566  SPEC: Use macro python_provide conditionally
        708f0497d  SPEC: Use %license macro
        2186f88e0  KCM: include missing header file
        e1052a50b  test_ldap.py: Add test for filter_{users,groups}
        87de1e0fb  CONFDB: Use default configuration with missing sssd.conf
        b7ad403d5  UTIL: Drop unused error code ERR_MISSING_CONF
        1732c4028  INTG: Do not use configure time option enable-files-domain
        02bb4f874  BUILD: Link libwbclient with libdl
        d82ffa52d  BUILD: Fix build without ssh
        6df5b3600  SSSDConfig: Handle integer parsing more leniently
        fca26b76f  SSSDConfig: Fix saving of debug_level
        074ded4cd  SECRETS: Fix warning Wpointer-bool-conversion
        8ccc9b7c3  BUILD: Improve error messages for optional dependencies
        5919e884d  VALIDATOR: prevent duplicite report from subdomain sections
        291b6bfd4  test_config_check: Fix few issues
        c62dc2ac0  pam_sss: Fix checking of empty string cert_user
        054900ab4  codegen: Remove util.h from generated files
        24f4426ad  UTIL: Remove few unused headed files
        cf098cbee  UTIL: Remove signal.h from util/util.h
        91141c6ae  UTIL: Remove signal.h from util/util.h
        8890a30f5  UTIL: Remove fcntl.h from util/util.h
        92b2a4023  Remove string{,s}.h
        96e1794db  UTIL: Remove ctype.h from util/util.h
        0f058b315  UTIL: Remove limits.h from util/util.h
        709989b80  Remove unnecessary sys/param.h
        0fba03cab  certmap: Remove unnecessary included files
        c83e265bb  cache_req: Do not use default_domain_suffix with netgroups
        818d01b4a  pam_sss: Fix leaking of memory in case of failures
        223f4ff3c  CI: Do not use valgrind for dummy-child
        7c0402b85  Revert "CI: Use /bin/sh as a CONFIG SHELL"
        934937029  Revert "LDAP: Fix nesting level comparison"
        f3a306cf7  KCM: temporary increase hardcoded buffers
        614545382  KCM: Modify krb5 snippet file kcm_default_ccache

    Michal Židek (20):
        6fb643c75  UTIL: Typo in comment
        e0e038218  UTIL: Introduce subdomain_create_conf_path()
        a63d74f65  SUBDOMAINS: Allow use_fully_qualified_names for subdomains
        78a08d30b  selinux: Do not fail if SELinux is not managed
        955574eeb  config-check: Message when sssd.conf is missing
        4c49edbd8  SDAP: Fix handling of search bases
        21f3d6124  SERVER_MODE: Update sdap lists for each ad_ctx
        b4ca0da4d  AD: Add debug messages
        c4ddb9cca  AD SUBDOMAINS: Fix search bases for child domains
        0ab730850  VALIDATORS: Add subdomain section
        f433e4dc4  VALIDATORS: Remove application section domain
        a6a750d98  VALIDATORS: Escape special regex chars
        537103f29  TESTS: Add unit tests for cfg validation
        88d723396  MAN: Fix typo in trusted domain section
        0bfc49133  VALIDATORS: Change regex for app domains
        39c5aee02  VALIDATORS: Detect inherit_from in normal domain
        283d589b3  TESTS: Add one config-check test case
        b1d340595  GPO: Fix typo in DEBUG message
        630aea130  SDAP: Update parent sdap_list
        386c5f2e1  SDAP: Add sdap_domain_copy_search_bases

    Nikolai Kondrashov (1):
        a012a71f2  NSS: Move output name formatting to utils

    Pavel Březina (22):
        46c99a59c  NSS/TESTS: Fix subdomains attribution
        300b9e921  tcurl: add support for ssl and raw output
        b800a6d09  tcurl test: refactor so new options can be added more easily
        36e49a842  tcurl test: add support for raw output
        886e0f75e  tcurl test: add support for tls settings
        c2ea75da7  tcurl: add support for http basic auth
        d1ed11fc5  tcurl test: allow to set custom headers
        ae6b11229  tcurl test: add support for client certificate
        6698d4051  ci: do not build secrets on rhel6
        793f2573b  build: make curl required by secrets
        df99d709c  secrets: use tcurl in proxy provider
        06744bf5a  secrets: remove http-parser code in proxy provider
        720e1a5b9  secrets: allow to configure certificate check
        af026ea6a  secrets: support HTTP basic authentication with proxy provider
        db826f57b  secrets: fix debug message
        13d720de1  secrets: always add Content-Length header
        18e4fe9d8  sss_iobuf: fix 'read' shadows a global declaration
        dc186bfe9  configure: fix typo
        05c2c3047  responders: do not leak selinux context on clients destruction
        b07bcd8b9  ipa_s2n_get_acct_info_send: provide correct req_input name
        6a611406e  DP: Fix typo
        37d2194cc  IFP: Add domain and domainname attributes to the user

    René Genz (2):
        0a86dede8  minor typo fixes
        352f48323  Use correct spelling of override

    Simo Sorce (3):
        08084b117  ssh tools: The ai structure is not an array,
        5f6232c7e  ssh tools: Fix issues with multiple IP addresses
        244adc327  ssh tools: Split connect and communication phases

    Sumit Bose (53):
        843bc50c0  split_on_separator: move to a separate file
        8b7548f65  util: move string_in_list to util_ext
        db36dca3d  certmap: add new library libsss_certmap
        31a6661ff  certmap: add placeholder for OpenSSL implementation
        3994e8779  sysdb: add sysdb_attrs_copy()
        70c0648f0  sdap_get_users_send(): new argument mapped_attrs
        81c564a06  LDAP: always store the certificate from the request
        b341ee51c  sss_cert_derb64_to_ldap_filter: add sss_certmap support
        49f8ec8e0  sysdb: add certmap related calls
        c44728a02  IPA: add certmap support
        440797cba  nss-idmap: add sss_nss_getlistbycert()
        a0b1bfa76  nss: allow larger buffer for certificate based requests
        bd1fa0ec9  ssh: handle binary keys correctly
        1b5d6b1af  ssh: add support for certificates from non-default views
        1c551b137  krb5: return to responder that pkinit is not available
        415d93196  IPA: add mapped attributes to user from trusted domains
        2cf7becc0  IPA: lookup AD users by certificates on IPA clients
        828437541  IPA: enable AD user lookup by certificate
        7be6624d9  pam_test_client: add service and environment to PAM test client
        435b3678d  pam_test_client: add SSSD getpwnam lookup
        40ff10d73  sss_sifp: update method names
        9be97c9cc  pam_test_client: add InfoPipe user lookup
        4a9160e2b  sssctl: integrate pam_test_client into sssctl
        dbeae4834  i18n: adding sssctl files
        1193f20a8  KRB5_LOCATOR: add env variable to disable plugin
        35186217d  sbus: check connection for NULL before unregister it
        712e5b2e4  utils: add sss_domain_is_forest_root()
        feeabf273  ad: handle forest root not listed in ad_enabled_domains
        2e5fc89ef  overrides: add certificates to mapped attribute
        92d8b072f  PAM: check matching certificates from all domains
        71731d26d  sss_nss_getlistbycert: return results from multiple domains
        870b58a6c  cache_req: use the right negative cache for initgroups by upn
        ec9ac22d6  test: make sure p11_child is build for pam-srv-tests
        29d063505  pam: properly support UPN logon names
        eb7095099  ipa: filter IPA users from extdom lookups by certificate
        ca95807a9  krb5: accept changed principal if krb5_canonicalize=True
        29ee3e094  ldap: handle certmap errors gracefully
        749963195  RESPONDER_COMMON: update certmaps in responders
        89ff140d7  tests: fix test_pam_preauth_cert_no_logon_name()
        a192a1d72  pam_sss: add support for SSS_PAM_CERT_INFO_WITH_HINT
        6073cfc40  add_pam_cert_response: add support for SSS_PAM_CERT_INFO_WITH_HINT
        32474fa2f  PAM: send user name hint response when needed
        ee7e72a65  sysdb: sysdb_get_certmap() allow empty certmap
        b130adaa3  sssctl: show user name used for authentication in user-checks
        a5e134b22  IPA: Fix the PAM error code that auth code expects to start migration
        614057ea8  krb5: disable enterprise principals during password changes
        7e2ec7caa  krb5: use plain principal if password is expired
        2ccfa9502  tests: update expired certificate
        9cca5bff0  files: refresh override attributes after re-read
        0c5b97812  responders: update domain even for local and files provider
        1b3ca692b  PAM: make sure the files provider uses the right auth provider
        c377d4d60  idmap_error_string: add missing descriptions
        a406b52a0  ad_account_can_shortcut: shortcut if ID is unknown

    Ville Skyttä (1):
        00172861b  SSSDConfig: Python 3.6 invalid escape sequence deprecation fix
