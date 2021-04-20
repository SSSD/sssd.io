SSSD 2.3.0 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

-  SSSD can now handle ``hosts`` and ``networks`` nsswitch databases (see ``resolve_provider`` option)
-  By default, authentication request only refresh user's initgroups if it is expired or there is not active user's session (see ``pam_initgroups_scheme`` option)
-  OpenSSL is used as default crypto provider, NSS is deprecated
-  Active Directory provider now defaults to GSS-SPNEGO SASL mechanism (see ``ldap_sasl_mech`` option)
-  Active Directory provider can now be configured to use only ``ldaps`` port (see ``ad_use_ldaps`` option)
-  SSSD now accepts host entries from GPO's security filter
-  Format of debug messages has changed to be shorter and better sortable
-  New debug level (``0x10000``) was added for low level ldb messages only (see ``sssd.conf`` man page)

Packaging changes
~~~~~~~~~~~~~~~~~

-  New configure option ``--enable-gss-spnego-for-zero-maxssf``

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

-  Default value of ``ldap_sasl_mech`` has changed to ``GSS-SPNEGO`` for AD provider
-  Return code of ``pam_sss.so`` are documented in ``pam_sss`` manpage
-  Added option ``ad_update_samba_machine_account_password``
-  Added option ``ad_use_ldaps``
-  Added option ``ldap_iphost_object_class``
-  Added option ``ldap_iphost_name``
-  Added option ``ldap_iphost_number``
-  Added option ``ldap_ipnetwork_object_class``
-  Added option ``ldap_ipnetwork_name``
-  Added option ``ldap_ipnetwork_number``
-  Added option ``ldap_iphost_search_base``
-  Added option ``ldap_ipnetwork_search_base``
-  Added option ``ldap_connection_expire_offset``
-  Added option ``ldap_sasl_maxssf``
-  Added option ``pam_initgroups_scheme``
-  Added option ``entry_cache_resolver_timeout``
-  Added option ``entry_cache_computer_timeout``
-  Added option ``resolver_provider``
-  Added option ``proxy_resolver_lib_name``
-  Minor text improvements

Tickets Fixed
-------------

-  `#1025 <https://github.com/SSSD/sssd/issues/1025>`_ - Man pages don't mention that ``use_fully_qualified_names==true`` for trusted domain
-  `#1032 <https://github.com/SSSD/sssd/issues/1032>`_ - Wrong debug level in calc_flat_name()?
-  `#1038 <https://github.com/SSSD/sssd/issues/1038>`_ - ``sssd.api.conf`` and ``sssd.api.d`` should belong to ``python-sssdconfig`` package
-  `#2404 <https://github.com/SSSD/sssd/issues/2404>`_ - Fill missing config options in SSSDConfig.py
-  `#4356 <https://github.com/SSSD/sssd/issues/4356>`_ - GPO Security Filtering and Access Control are not Compliant with MS-ADTS
-  `#4489 <https://github.com/SSSD/sssd/issues/4489>`_ - TESTS: make intgcheck is not always passing in the internal CI (enumeration tests)
-  `#4541 <https://github.com/SSSD/sssd/issues/4541>`_ - Disable host wildcards in sudoHost attribute (ldap_sudo_include_regexp=false)
-  `#4651 <https://github.com/SSSD/sssd/issues/4651>`_ - Randomize ldap_connection_expire_timeout either by default or w/ a configure option
-  `#4691 <https://github.com/SSSD/sssd/issues/4691>`_ - Provide a list of pam_status return codes used by the pam_sss.so module in the module man file
-  `#4730 <https://github.com/SSSD/sssd/issues/4730>`_ - subdomain lookup fails when certmaprule contains DN
-  `#4978 <https://github.com/SSSD/sssd/issues/4978>`_ - [RFE] SSSD should use GSS-SPNEGO instead of GSSAPI when talking to AD
-  `#5010 <https://github.com/SSSD/sssd/issues/5010>`_ - MAN page: sssd-ipa: confusing text
-  `#5029 <https://github.com/SSSD/sssd/issues/5029>`_ - override_gid not working for subdomains
-  `#5052 <https://github.com/SSSD/sssd/issues/5052>`_ - server/be: SIGTERM handling is incorrect
-  `#5053 <https://github.com/SSSD/sssd/issues/5053>`_ - Watchdog implementation or usage is incorrect
-  `#5062 <https://github.com/SSSD/sssd/issues/5062>`_ - initgroups for already logged in users should not cause long delays
-  `#5079 <https://github.com/SSSD/sssd/issues/5079>`_ - sssd requires timed sudoers ldap entries to be specified up to the seconds
-  `#5082 <https://github.com/SSSD/sssd/issues/5082>`_ - [RFE]: use certificate matching rule when generating SSH key from a certificate
-  `#5085 <https://github.com/SSSD/sssd/issues/5085>`_ - Impossible to enforce GID on the AD's "domain users" group in the IPA-AD trust setup
-  `#5087 <https://github.com/SSSD/sssd/issues/5087>`_ - pcscd rejecting sssd ldap_child as unauthorized
-  `#5088 <https://github.com/SSSD/sssd/issues/5088>`_ - [Doc]Provide explanation on escape character for match rules sss-certmap
-  `#5090 <https://github.com/SSSD/sssd/issues/5090>`_ - sssctl config-check command does not give proper error messages with line numbers
-  `#5092 <https://github.com/SSSD/sssd/issues/5092>`_ - Force LDAPS over 636 with AD Provider
-  `#5094 <https://github.com/SSSD/sssd/issues/5094>`_ - Unreadable GPOs should not be logged as a critical failure
-  `#5096 <https://github.com/SSSD/sssd/issues/5096>`_ - util/sss_ptr_hash.c: potential double free in ``sss_ptr_hash_delete_cb()``
-  `#5100 <https://github.com/SSSD/sssd/issues/5100>`_ - sssd_be frequent crash
-  `#5105 <https://github.com/SSSD/sssd/issues/5105>`_ - Build error with python3.8-config --ldflags
-  `#5106 <https://github.com/SSSD/sssd/issues/5106>`_ - Expecting appropriate error message when new password length is less than 8 characters when ldap_pwmodify_mode = ldap_modify in sssd.conf
-  `#5114 <https://github.com/SSSD/sssd/issues/5114>`_ - p11_child should have an option to skip C_WaitForSlotEvent if the PKCS#11 module does not implement it properly
-  `#5116 <https://github.com/SSSD/sssd/issues/5116>`_ - sssctl config-check reports errors when auto_private_groups is disabled/enabled in child domains
-  `#5124 <https://github.com/SSSD/sssd/issues/5124>`_ - "off-by-one error" in watchdog implementation
-  `#5126 <https://github.com/SSSD/sssd/issues/5126>`_ - sbus: wrong handling of certain fails in sbus_dbus_connect_address()
-  `#5128 <https://github.com/SSSD/sssd/issues/5128>`_ - SSSD doesn't honour the customized ID view created in IPA
-  `#5129 <https://github.com/SSSD/sssd/issues/5129>`_ - id_provider = proxy proxy_lib_name = files returns \* in password field, breaking PAM authentication
-  `#5132 <https://github.com/SSSD/sssd/issues/5132>`_ - background refresh task does not refresh updated netgroup entries
-  `#5133 <https://github.com/SSSD/sssd/issues/5133>`_ - Odd lastUpdate attribute if SSSD is started without sssd.conf
-  `#5136 <https://github.com/SSSD/sssd/issues/5136>`_ - ad and ipa backends should require proper version of ``samba-client-libs``
-  `#5139 <https://github.com/SSSD/sssd/issues/5139>`_ - pam_sss reports PAM_CRED_ERR when providing wrong password for an existing IPA user, but this error's description is misleading
-  `#5160 <https://github.com/SSSD/sssd/issues/5160>`_ - Multiples Kerberos ticket on RHEL 7.7 after lock and unlock screen

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-2_2_3..sssd-2_3_0

    Alex Rodin (5):
        192eadaaf  Update pam_sss.8.xml
        2014d8f52  Update __init__.py.in
        9483bf410  SSSDConfig: Update of config options
        a4219bbcc  SSSDConfig: New SSSDOptions class
        db6f6b6dd  MAN: use_fully_qualified_names description updated

    Alexey Tikhonov (26):
        1d4a7ffdc  providers/krb5: got rid of unused code
        e41e9b37e  data_provider_be: got rid of duplicating SIGTERM handler
        3f52de891  util/server: improved debug at shutdown
        2c13d8bd0  util/watchdog: fixed watchdog implementation
        26e33b198  util/sss_ptr_hash: fixed double free in sss_ptr_hash_delete_cb()
        faa5dbf6f  sbus_server: stylistic rename
        adc7730a4  sss_ptr_hash: don't keep empty sss_ptr_hash_delete_data
        d0eb88089  sss_ptr_hash: sss_ptr_hash_delete fix/optimization
        8cc2ce4e9  sss_ptr_hash: removed redundant check
        4bc0c2c78  sss_ptr_hash: fixed memory leak
        0bb128925  sss_ptr_hash: internal refactoring
        88b23bf50  TESTS: added sss_ptr_hash unit test
        653df698a  Watchdog: fixes "off-by-one" error
        863f71acb  sssd.spec.in: added missing Requires
        fa9ab9584  PAM: fixed wrong debug message
        903fe0fa9  MAN: fixed description of pam_cert_db_path
        9b120fe09  SPEC: added explicit `samba-client-libs` dependency
        8b2c4ad07  config: switch to OpenSSL as default crypto backend
        5379fddb1  SPEC: 'sssd.api.*' should belong `python-sssdconfig`
        b43546232  TESTS: NSS db setup is only required in NSS based build
        f2ac087da  SBUS: do not return invalid connection pointer
        bf8536a0b  Fixed unsafe usage of strncpy()
        7b2537515  DEBUG: changed timestamp output format
        b5604d072  DEBUG: introduce new SSSDBG_TRACE_LDB level
        00e7b1ada  DEBUG: changed "debug_prg_name" format
        65369f293  WATCHDOG: log process termination to the journal

    Andreas Hasenack (1):
        4dbfaae43  Fix another build failure with python 3.8

    Andrew Gunnerson (1):
        1cdd43140  ad: Add support for passing --add-samba-data to adcli

    David Mulder (5):
        d1f8ec8a9  SSSD should accept host entries from GPO's security filter
        8aa2f9edc  Test the host sid checking
        d6f0b432a  Remove sssd Security Filtering host comment from man
        a2e7f6875  Create a computer_timeout for caching GPO security filter
        5c8f7960f  Resolve computer lookup failure when sam!=cn

    Fabiano Fidêncio (1):
        3477f2c28  INTG: Increase the sleep() time so the changes are reflected on SSSD

    Joakim Tjernlund (1):
        494b838db  Update OpenRC init.d script

    Lars Francke (1):
        5019d2166  ldap: set ldap_group_name to sAMAccountName for ad schema

    Lukas Slebodnik (8):
        007d5b79b  BE_REFRESH: Do not try to refresh domains from other backends
        b47edd9fe  SSS_INI: Fix syntax error in sss_ini_add_snippets
        3bdce86b4  PROXY: Fix warning-format-overflow directive argument is null
        d7ddcc56e  test_nss_srv: Suppress Conditional jump or move depends on uninitialised value
        c3b98b2b6  CONFIGURE: Fix detection of samba version for idmap plugin
        a483bfa67  CONFIGURE: Fix detection of attribute fallthrough
        399ee9d1a  BUILD: Accept krb5 1.18 for building the PAC plugin
        d028df036  CI: Drop usage of unnecessary copr repo for mock

    MIZUTA Takeshi (4):
        a18a6f008  util/server: Fix the timing to close() the PID file
        50cc1963f  Remove redundant header file inclusion
        ceea56be3  monitor: Fix check process about multiple starts of sssd when pidfile remains
        9ccf78dbd  man: fix typos - correct manpage reference - correct wrong word - capitalize the first letter

    Michal Židek (5):
        a706ea8e0  Update version in version.m4 to track the next release.
        b11907c65  Bump the version.
        fe9eeb51b  nss: Collision with external nss symbol
        7fbc7e3ff  sssd.spec: Add recommended packages
        e698d53e0  spec: Do not overwrite /etc/pam.d/sssd-shadowutils

    Noel Power (2):
        1fdd8fa2f  Use ndr_pull_steal_switch_value for modern samba versions
        c031adde4  ad_gpo_ndr.c: refresh ndr_ methods from samba-4.12

    Pavel Březina (19):
        03bc96247  nss: use real primary gid if the value is overriden
        97c96fd06  ci: add rhel7
        63c38d613  ci: set sssd-ci notification to pending state when job is started
        c861a3909  ci: archive ci-mock-result
        116b144bc  tests: fix race condition in enumeration tests
        d3d72b907  ci: add CentOS 7
        5b87af6f5  sss_sockets: pass pointer instead of integer
        bfa02b0b0  ci: keep system list outside repository
        feaf88914  ci: remove old dependency repository
        e4c6ebf67  sdap: provide error message when password change fail in ldap_modify mode
        d4bf66261  sbus: commit complete generated code
        ae5a2cdcc  proxy: set pwfield to x for files library
        c7d328ea9  proxy: do not fail if proxy_resolver_lib_name is not set
        23c2d376b  be: add BE_REQ_HOST to be_req2str
        41220021d  dp: free methods if target is not configured
        1b84c3a1f  sysdb: check if the id override belongs to requested domain
        ee56fbca3  p11_child: fix initializer error
        69de78d82  Move from Pagure to Github
        ed64f142f  Update the translations for the 2.3.0 release

    Paweł Poławski (6):
        58a67cd38  sysdb_sudo: Enable LDAP time format compatibility
        9188aa17d  GPO: Duplicated error message for unreadable GPO
        b432b2c4c  LDAP: Netgroups refresh in background task
        704d9f1d3  SYSDB: Cache selector as enum
        4c93aa76d  DOMAIN: Downgrade log message type
        035271b72  MAN: refresh_expired_interval description updated

    Petr Vaněk (1):
        6ab9ac3ff  configure: prefer python3 if available

    REIM THOMAS (5):
        f5cb0e160  GPO: Grant access if DACL is not present
        8527ed113  GPO: Support group policy file main folders with upper case name
        866d588ae  GPO: Close group policy file after copying
        5435e0a66  GPO: Group policy access evaluation not in line with [MS-ADTS]
        a32f94f5c  GPO: Improve logging of GPO security filtering

    Samuel Cabrero (69):
        8d333499a  AD: Improve host SID retrieval
        2143c7276  AD: use getaddrinfo with AI_CANONNAME to find the FQDN
        12bd3f96c  STAP: Add missing session data provider target
        d263fa9d6  UTIL: Add a function to canonicalize IP addresses
        860c45706  SYSDB: Add sysdb functions for hosts entries
        622849279  SYSDB: Add index for hostAddress attribute
        99ce11710  SBUS: Add new resolver target interface
        d76d818cb  DP: Add a new filter type, filter by address
        469891df6  RESPONDER: Add sss_dp_resolver_get_send
        1cb209556  CACHE_REQ: Rename cache req host by name name plugin used by SSH
        dafdd066e  CACHE_REQ: Add a data field to store network addresses
        6e66e3217  CACHE_REQ: Implement ip_host_by_addr and ip_host_by_name plugins
        e931f27df  NSS: Add client support for hosts (non-enumeration)
        55cfacfe3  NSS: Add gethostbyname and gethostbyaddr support to the NSS responder
        014cd3a54  TESTS: Add gethostbyname and gethostbyaddr NSS responder tests
        2c317ce9f  DP: Implement resolver target handler
        6f6900374  CONFDB: Add new options for resolver provider
        d6d03aafc  CONFDB: Add a new resolver_timeout to timeout cached resolver entries
        b523fb6a0  UTIL: Allow to specify mandatory and optional symbols when loading nss libs
        0ec8bd578  PROXY: Create a module context to store id and auth contexts
        688e6a6b5  PROXY: Load resolver NSS library
        b1fe85eb0  PROXY: Register resolver hosts handler method
        be7919789  PROXY: Handle resolver hosts by name requests
        bbb7a45df  PROXY: Store results from NSS library call into the cache
        00bc78971  SYSDB: Extend sysdb_store_host() to accept extra attributes
        29c583b64  PROXY: Handle resolver hosts by address requests
        5672d2beb  LDAP: Initialize resolver provider
        1402f1004  AD: Initialize resolver provider
        a61c6d61c  LDAP: Initialize ldap_iphost_\* options
        6a7775263  LDAP: Document new ldap_iphost_\* options
        0498591ea  AD: Initialize ldap_iphost_\* options
        b8fba0166  LDAP: Prepare for iphost lookups
        29b27395f  LDAP: Add support for iphost lookups (no enumeration)
        bbcd849a4  NSS: Add client support for [set|get|end]hostent()
        11cc32e48  SYSDB: Add support for enumerating hosts
        8b96109ff  CACHE_REQ: Add support for enumerating hosts
        8a51bc0df  LDAP: Setup resolver enumeration tasks
        82b808d93  LDAP: Add support for iphost enumeration
        2be80a00c  AD: Setup resolver enumeration tasks
        10d9346af  AD: Add support for iphost enumeration
        ae6d042cb  LDAP: Implement iphost cleanup for expired cache entries
        45dbaddde  AD: Implement iphost cleanup for expired cache entries
        e980b0f6a  PROXY: Add support for iphost enumeration
        8a66d6e5a  TESTS: Add LDAP resolver target integration tests
        233d30a50  SYSDB: Add sysdb functions for ipnetwork entries
        b37a13db5  SYSDB: Add index for ipNetworkNumber attribute
        c01c1c34a  CACHE_REQ: Implement ip_network_by_name and ip_network_by_addr plugins
        9c96d570e  NSS: Add client support for networks (non-enumeration)
        e88aac3b1  NSS: Add getnetbyname and getnetbyaddr support to the NSS responder
        0ae366573  TESTS: Add getnetbyname and getnetbyaddr NSS responder tests
        5dfced3cf  DP: Handle IP network requests in resolver target
        be1e6c12d  PROXY: Load networks symbols
        5e92783f8  PROXY: Handle resolver IP network by name requests
        0b88ce5d5  PROXY: Handle resolver IP network by address requests
        fe9f0ecf2  SYSDB: Add functions to store IP networks from providers
        92e8c1e88  PROXY: Store IP network results from NSS library in the cache
        93de591c9  LDAP: Initialize ldap_ipnetwork_\* options
        4ab99ef1b  LDAP: Document new ldap_ipnetwork_\* options
        407d766d6  AD: Initialize new ldap_ipnetwork_\* options
        3533697f0  LDAP: Prepare for ipnetwork lookups (no enumeration)
        0e5303ba6  LDAP: Add support for ipnetwork lookups (no enumeration)
        29adb1089  NSS: Add client support for [set|get|end]netent()
        cad60f636  SYSDB: Add support for enumerating ipnetworks
        5e75d695a  CACHE_REQ: Add support for enumerating ip networks
        ab2cd9ca5  LDAP: Add support for ipnetworks enumeration
        f70695730  LDAP: Implement ipnetwork cleanup for expired cache entries
        08b774e43  PROXY: Add support for ipnetwork enumeration
        ebe944ba9  TESTS: Add LDAP resolver IP networks tests
        090d804c8  Drop obsolete SUSE spec file

    Simo Sorce (3):
        7aa96458f  Add TCP level timeout to LDAP services
        b57287123  cache_req: introduce cache_behavior enumeration
        d2424bfb7  pam: Use cache for users with existing session

    Stephen Gallagher (1):
        bc56b10ae  Fix build failure against samba 4.12.0rc1

    Sumit Bose (23):
        580d61884  ldap_child: do not try PKINIT
        21cb9fb28  certmap: mention special regex characters in man page
        090cf77a0  ad: allow booleans for ad_inherit_opts_if_needed()
        341ba49b0  ad: add ad_use_ldaps
        78649907b  ldap: add new option ldap_sasl_maxssf
        24387e19f  ad: set min and max ssf for ldaps
        f9b3c0d10  ssh: do not mix different certificate lists
        849d495ea  ssh: add 'no_rules' and 'all_rules' to ssh_use_certificate_matching_rules
        7b647338a  p11_child: check if card is present in wait_for_card()
        37780b895  PAM client: only require UID 0 for private socket
        6f7f15691  ssh: fix matching rules default
        0003eda98  ipa: add missing new-line in debug message
        27a3c0cf3  sysdb: sanitize certmap rule name before using it in DN
        dab522c09  confdb: use proper timestamp if sssd.conf is missing
        a7099b72f  sudo: fix ldap_sudo_include_regexp default
        ac7248e83  ad: use GSSAPI with LDAPS
        dc21609f1  ad: change SASL mech default to GSS-SPNEGO
        95c8667a5  ad: make GSS-SPNEGO maxssf=0 workaround configurable
        11435b106  krb5: do not cache ccache or password during preauth
        b66f0e448  pam: add option pam_initgroups_scheme
        68aa68e8d  pam: use pam_initgroups_scheme
        74f0a451b  cache_req: no refresh with CACHE_REQ_BYPASS_PROVIDER
        272efe495  pam: make sure initgr cache is not created twice

    Thorsten Scherf (2):
        2dc82a242  Fix sssd-ldap man page
        b19b25e13  add reference to sss_obfuscate man page

    Tomas Halman (3):
        bd201746f  sdap: Add randomness to ldap connection timeout
        b62665184  INI: sssctl config-check command error messages
        626c9c2f4  SYSDB: override_gid not working for subdomains

    Yuri Chornoivan (1):
        7578bdea9  sssctl: fix typo in user message

    ikerexxe (3):
        746d4ff34  config: allowed auto_private_groups in child domains
        80b9285b3  man: in sssd-ipa clarified trusted domains section
        49b9ca158  ipa_auth and krb5_auth: when providing wrong password return PAM_AUTH_ERR
