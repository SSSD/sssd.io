SSSD 2.4.1 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

-  ``SYSLOG_IDENTIFIER`` was renamed to ``SSSD_PRG_NAME`` in journald output, to avoid issues with PID parsing in rsyslog (BSD-style forwarder) output.

New features
~~~~~~~~~~~~

-  New PAM module ``pam_sss_gss`` for authentication using GSSAPI
-  ``case_sensitive=Preserving`` can now be set for trusted domains with AD provider
-  ``case_sensitive=Preserving`` can now be set for trusted domains with IPA provider. However, the option needs to be set to ``Preserving`` on both client and the server for it to take effect.
-  ``case_sensitive`` option can be now inherited by subdomains
-  ``case_sensitive`` can be now set separately for each subdomain in ``[domain/parent/subdomain]`` section
-  ``krb5_use_subdomain_realm=True`` can now be used when sub-domain user principal names have upnSuffixes which are not known in the parent domain. SSSD will try to send the Kerberos request directly to a KDC of the sub-domain.

Important fixes
~~~~~~~~~~~~~~~

-  krb5_child uses proper umask for DIR type ccaches
-  Memory leak in the simple access provider
-  KCM performance has improved dramatically for cases where large amount of credentials are stored in the ccache.

Packaging changes
~~~~~~~~~~~~~~~~~

-  Added ``pam_sss_gss.so`` PAM module and ``pam_sss_gss.8`` manual page

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

-  New default value of ``debug_level`` is 0x0070
-  Added ``pam_gssapi_check_upn`` to enforce authentication only with principal that can be associated with target user.
-  Added ``pam_gssapi_services`` to list PAM services that can authenticate using GSSAPI

Tickets Fixed
-------------

-  `#3413 <https://github.com/SSSD/sssd/issues/3413>`_ - autofs: return a connection failure until maps have been fetched
-  `#3730 <https://github.com/SSSD/sssd/issues/3730>`_ - proxy_child hardening
-  `#4590 <https://github.com/SSSD/sssd/issues/4590>`_ - syslog mesages for back ends uses invalid ident tag
-  `#4759 <https://github.com/SSSD/sssd/issues/4759>`_ - sssd krb5_child using wrong domain to authenticate
-  `#4829 <https://github.com/SSSD/sssd/issues/4829>`_ - KCM: Increase the default client idle timeout, consider decreasing the timeout on busy servers
-  `#5121 <https://github.com/SSSD/sssd/issues/5121>`_ - timestamp cache entries are not created if missing
-  `#5238 <https://github.com/SSSD/sssd/issues/5238>`_ - Unexpected behavior and issue with filter_users/filter_groups option
-  `#5250 <https://github.com/SSSD/sssd/issues/5250>`_ - [RFE] RHEL8 sssd: inheritance of the case_sensitive parameter for subdomains.
-  `#5333 <https://github.com/SSSD/sssd/issues/5333>`_ - sssd-kcm does not store TGT with ssh login using GSSAPI
-  `#5349 <https://github.com/SSSD/sssd/issues/5349>`_ - kcm: poor performance with large number of credentials
-  `#5351 <https://github.com/SSSD/sssd/issues/5351>`_ - Do not overwrite LDAP data of local domain when looking up a Global Catalog
-  `#5359 <https://github.com/SSSD/sssd/issues/5359>`_ - SSSD can hang being blocked on TCP operation involving socket opened internally by libldap
-  `#5382 <https://github.com/SSSD/sssd/issues/5382>`_ - User lookups over the InfoPipe responder fail intermittently
-  `#5384 <https://github.com/SSSD/sssd/issues/5384>`_ - sssd syslog/journal logging is now too generic
-  `#5400 <https://github.com/SSSD/sssd/issues/5400>`_ - Can't login with smartcard with multiple certs having same ID value
-  `#5403 <https://github.com/SSSD/sssd/issues/5403>`_ - filter_groups option partially filters the group from 'id' output of the user because gidNumber still appears in 'id' output [RHEL 8]
-  `#5412 <https://github.com/SSSD/sssd/issues/5412>`_ - sssd_be segfaults at be_refresh_get_values_ex() due to NULL ptrs in results of sysdb_search_with_ts_attr()
-  `#5425 <https://github.com/SSSD/sssd/issues/5425>`_ - SBUS: failures during servers startup
-  `#5436 <https://github.com/SSSD/sssd/issues/5436>`_ - krb5_child: "DIR:" ccache directory created with bad mode 0600 due to umask
-  `#5451 <https://github.com/SSSD/sssd/issues/5451>`_ - resolv: resolv_gethostbyname_dns_parse() doesn't properly handle fail of ares_parse_*_reply()
-  `#5456 <https://github.com/SSSD/sssd/issues/5456>`_ - Memory leak in the simple access provider
-  `#5466 <https://github.com/SSSD/sssd/issues/5466>`_ - SBUS: NULL deref in dp_client_handshake_timeout()
-  `#5469 <https://github.com/SSSD/sssd/issues/5469>`_ - sssd unable to lookup certmap rules
-  `#5471 <https://github.com/SSSD/sssd/issues/5471>`_ - [RFE] sss_override: Usage limitations clarification in man page
-  `#5475 <https://github.com/SSSD/sssd/issues/5475>`_ - Do not add '%' to group names already prefixed with '%' in IPA sudo rules
-  `#5488 <https://github.com/SSSD/sssd/issues/5488>`_ - Unexpected (?) side effect of SSSDBG_DEFAULT change

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-2_4_0..2.4.1

    Alexander Bokovoy (1):
        cd48ef507  sudo runas: do not add '%' to external groups in IPA

    Alexey Tikhonov (65):
        f7dba450c  SDAP: set common options for sockets open by libldap
        833034f53  DEBUG: journal_send() was made static
        18233532b  DEBUG: fixes program identifier as seen in syslog
        ff24d1538  SYSDB: merge_res_sysdb_attrs() fixed to avoid NULL ptr in msgs[]
        0e225ff79  KCM: avoid NULL deref
        e350d917e  SYSDB:autofs: cosmetic updates
        df723cb98  SYSDB: wrong debug message corrected
        d8af1db84  SYSDB:sudo: changed debug message to be consistent
        b4acf71d0  SYSDB:iphosts: severity level of few debug messages adjusted
        a73df70ee  SYSDB:ipnetworks: severity level of few debug messages adjusted
        033c31a2a  SYSDB:ops: few debug messages were corrected
        744582419  SYSDB:search: few debug messages were corrected
        f55c95990  SYSDB:selinux: debug message severity level was adjusted
        e731368ed  SYSDB:service: severity level of few debug messages adjusted
        82dc14b02  SYSDB:upgrade: debug message corrected
        daa5454f8  SYSDB:views: few debug message corrections
        fe0530ef9  MONITOR: severity level of few debug messages adjusted
        85d8adc4d  P11_CHILD: severity level of few debug messages adjusted
        d6f6f053d  AD: few debug message corrections
        2f70695a8  DP: few debug message corrections
        667b983aa  IPA: few debug message corrections
        9244820af  KRB5: few debug message corrections
        ff8f44ce2  LDAP: few debug message corrections
        d91409df4  PROXY: few debug message corrections
        fb052a4c9  RESOLV: debug message correction
        018c08acb  AUTOFS: few debug message corrections
        01ba32f25  CACHE_REQ: debug message correction
        058644f2e  RESPONDER: few debug message corrections
        f457a1a69  IFP: few debug message corrections
        f028253ff  NSS: few debug message corrections
        3cbd0465b  PAM: few debug message corrections
        5068655a6  UTIL: few debug message corrections
        ac2285900  PAM: reduce log level in may_do_cert_auth()
        a7b6413d9  UTIL: sss_ldb_error_to_errno() improved
        52dc85540  SYSDB: reduce log level in sysdb_update_members_ex() in case failed attempt to DEL unexisting attribute
        99e44d9db  LDAP: added missed \n in log message
        a419b7e67  SSS_IFACE: corrected misleading return code
        1af89925e  IPA: corrected confusing message
        69aa3e8c4  DP: do not log failure in case provider doesn't support check_online method
        90dae38d7  RESPONDER: reduce log level in sss_parse_inp_done() in case of "Unknown domain" since this might be search by UPN
        6e3b4d745  SBUS: reduced log level in case of unexpected signal
        a7b145b99  LDAP: reduced log level in hosts_get_done()
        26fdc3c8f  CACHE_REQ: reduced log level in cache_req_object_by_name_well_known() Non fqdn input isn't necessarily an error here.
        ed6ec5697  SDAP: reduced log level in case group without members
        29f243fd5  AD: reduced log level in case check_if_pac_is_available() can't find user entry. This is typical situation when, for example, INITGROUPS lookup is executed for uncached user.
        4fe060abb  FILES: reduced debug level in refresh_override_attrs() if case "No overrides, nothing to do"
        644453f8d  LOGS: default log level changed to <= SSSDBG_OP_FAILURE
        0986cf6ce  UTIL: fixed bug in server_setup() that prevented setting debug level to 0 explicitly
        9215cf4e2  CERTMAP: removed stray debug message
        9390af3c2  IPA: reduce log level in apply_subdomain_homedir()
        60b17be9e  SYSDB: changed log level in sysdb_update_members_ex()
        bf873598a  IPA: ignore failed group search in certain cases
        e86599ba0  IPA: changed logging in ipa_get_subdom_acct_send()
        dba7de0db  SYSDB: changed logging in sysdb_get_real_name()
        00e3ac4a4  LDAP: reduce log level in case of fail to store members of missing group (it might be built-in skipped intentionally)
        0db68a1f9  LDAP: sdap_save_grpmem(): log level changed
        bd2f38abe  UTIL: find_domain_by_object_name_ex() changed log level
        d207eaafc  RESOLV: handle fail of ares_parse_*_reply() properly
        bdf461c75  SBUS: do not try to del non existing sender
        c48a4e804  Removed leftovers after PR #5246
        66ef363b1  dhash tables are now created with count=0 whenever no useful size hint available
        0c6924b8d  SBUS: set sbus_name before dp_init_send()
        3986deade  PROXY: child process security hardening
        b6fc7c0e9  Sanitize --domain option to allow safe usage as a part of log file name
        ff0f76561  Makefile: add missing '-fno-lto' to some tests

    Anuj Borah (1):
        39c52817d  TESTS:KCM: Increase client idle timeout to 5 minutes

    Armin Kuster (1):
        b0edc83e3  Provide missing defines which otherwise are available on glibc system headers

    Deepak Das (1):
        6c9f929ad  man: sss_override clarification

    Duncan Eastoe (2):
        4b0bd8455  nss: Use posix_fallocate() to alloc memcache file
        311e22724  nss: remove clear_mc_flag file after clearing caches

    Evgeny Sinelnikov (1):
        5892c3676  krb5: allow to use subdomain realm during authentication

    Justin Stephenson (1):
        3fdfb42b5  krb5: Remove secrets text from drop-in KCM file

    Madhuri Upadhye (6):
        78ef0828d  Test: AD: For sssd crash in ad_get_account_domain_search
        b5264396b  Test: alltests: "enabled" option to domain section
        2b00d5071  Update remove command to delete the snippet files
        014f416d0  Update the title of test case.
        cdad94802  Tests: alltests: "ldap_library_debug_level" option to domain section
        536e8b83a  alltests: password_policy: Removing the log debug messages

    Marco Trevisan (Treviño) (1):
        a06ce2107  test_ca: Look for libsofthsm2 in libdir before falling back to hardcoded paths

    Pavel Březina (64):
        b913ddbd5  Update version in version.m4 to track the next release
        47a316c85  kcm: fix typos in debug messages
        8edcea8c3  kcm: avoid name confusion in GET_CRED_UUID_LIST handlers
        b8f28d9aa  kcm: disable encryption
        74fdaa64b  kcm: avoid multiple debug messages if sss_sec_put fails
        908c15af9  secrets: allow to specify secret's data format
        ed08ba002  secrets: accept binary data instead of string
        b6cc661b9  iobuf: add more iobuf functions
        9b1631def  kcm: add json suffix to existing searialization functions
        e63a15038  kcm: move sec key parser to separate file so it can be shared
        15069a647  kcm: avoid suppression of cppcheck warning
        f17740d83  kcm: add spaces around operators in kcmsrv_ccache_key.c
        194447d35  kcm: use binary format to store ccache instead of json
        241ee30da  kcm: add per-connection data to be shared between requests
        a370553c9  sss_ptr_hash: fix double free for circular dependencies
        c3b314db5  kcm: store credentials list in hash table to avoid cache lookups
        bf127d4f3  secrets: fix may_payload_size exceeded debug message
        9c1b51d05  secrets: default to "plaintext" if "enctype" attr is missing
        39277cdad  secrets: move attrs names to macros
        325de5a5b  secrets: remove base64 enctype
        3f0ba4c2d  cache_req: allow cache_req to return ERR_OFFLINE if all dp request failed
        e50258da7  autofs: return ERR_OFFLINE if we fail to get information from backend and cache is empty
        9098108a7  autofs: translate ERR_OFFLINE to EHOSTDOWN
        34c519a48  autofs: disable fast reply
        8a22d4ad4  autofs: correlate errors for different protocol versions
        075519bce  configure: check for stdatomic.h
        18b98836e  kcm: decode base64 encoded secret on upgrade path
        45f2eb57d  sss_format.h: include config.h
        3b0e48c33  packet: add sss_packet_set_body
        6715b31f2  domain: store hostname and keytab path
        a3e2677f9  cache_req: add helper to call user by upn search
        dcc42015f  pam: fix typo in debug message
        d63172f12  pam: add pam_gssapi_services option
        fffe3169b  pam: add pam_gssapi_check_upn option
        d09aa174b  pam: add pam_sss_gss module for gssapi authentication
        4ea1739d0  pam_sss: fix missing initializer warning
        c0ae6d34f  pamsrv_gssapi: fix implicit conversion warning
        cc173629f  gssapi: default pam_gssapi_services to NULL in domain section
        111b8b4d6  pam_sss_gssapi: fix coverity issues
        2499bd145  cache_req: ignore autofs not configured error
        0eb0281c9  man: add auto_private_groups to subdomain_inherit
        12eb04b2f  subdomains: allow to inherit case_sensitive=Preserving
        f26559504  subdomains: allow to set case_sensitive=Preserving in subdomain section
        f6bb31af5  subdomains: allow to inherit case_sensitive=Preserving for IPA
        944c47e27  man: update case_sensitive documentation to reflect changes for subdomains
        78af35c35  po: add pam_sss_gss to translated man pages
        6add2ef31  pot: update pot files
        d163a120b  spec: synchronize with Fedora 34 spec file
        3e5ff111c  spec: remove unneeded conditionals and unused variables
        8b68aa28d  spec: keep _strict_symbol_defs_build
        eb6a3bacb  spec: enable LTO
        2b1c3c3dd  spec: remove support for NSS
        fcbbf1244  spec: remove --without-python2-bindings
        2970cd639  spec: re-import changes that were not merged in Fedora
        5eb4d5c8e  spec: synchronize with RHEL spec file
        e56ddbedd  spec: use sssd user on RHEL
        38d761466  spec: remove conflicts that no longer make sense
        bf1482c2f  spec: remove unused BuildRequires
        6f47eaca4  spec: remove unused Requires
        5d02f1e8b  spec: sort Requires, BuildRequires and configure for better clarity
        482ab2d8f  spec: comment some requirements
        ea55cd023  spec: fix spelling in package description
        3ee3c4c61  spec: use %autosetup instead of %setup
        78323d44e  configure: libcollection is not required

    Paweł Poławski (2):
        1e9abd508  data_provider_be: Add random offset default
        171b664ec  data_provider_be: MAN page update

    Samuel Cabrero (2):
        4ab47a914  Improve samba version check for ndr_pull_steal_switch_value signature
        6617f3d7d  winbind idmap plugin: Fix struct idmap_domain definition

    Sergio Durigan Junior (1):
        a25256fe2  Only start sssd.service if there's a configuration file present

    Shridhar Gadekar (1):
        fb6edec60  Tests:ad:sudo: support non-posix groups in sudo rules

    Steeve Goveas (13):
        804ae76d6  Move conftest.py to basic dir
        ef4c82bb9  Add alltests code
        73f5699bc  Add ad test code
        3c06709b9  Add ipa test code
        6cc11a9a8  Update sssd testlibs
        4205accc2  Add empty conftest.py and update path to run basic tests
        fe56d5c9e  Fix pep8 issues
        d2d44e9a3  Include data directory
        94a9833b0  Fix errors found during testing
        f404cd3e3  Remove trailing whitespaces
        1a616b590  tests: modify ipa client install for fedora
        f7ccc6799  TEST: Split tier1 tests with new pytest marker
        0f2d31e2e  tests: netstat command not found for test

    Sumit Bose (18):
        81e757b7b  ifp: fix use-after-free
        5f3b9e1d4  AD: do not override LDAP data during GC lookups
        0e1bcf77b  negcache: make sure domain config does not leak into global
        385af99ff  utils: add SSS_GND_SUBDOMAINS flag for get_next_domain()
        0dc81a52e  negcache: make sure short names are added to sub-domains
        fa4b46e7d  negcache: do not use default_domain_suffix
        3b158934c  ifp: fix original fix use-after-free
        c87b2208b  nss: check if groups are filtered during initgroups
        1b9b7f5a6  pam_sss: use unique id for gdm choice list
        8b6be52e9  authtok: add label to Smartcard token
        b8800d3e1  pam_sss: add certificate label to reply to pam_sss
        f633f37e7  add tests multiple certs same id
        19c2c641e  simple: fix memory leak while reloading lists
        6ca29942c  krb5_child: use proper umask for DIR type ccaches
        e7fb88fc6  BUILD: Accept krb5 1.19 for building the PAC plugin
        e07eeea7d  responders: add callback to schedule_get_domains_task()
        cb936e920  pam: refresh certificate maps at the end of initial domains lookup
        2d26c95d7  ssh: restore default debug level

    Tomas Halman (2):
        37761b42f  CACHE: Create timestamp if missing
        62b2b4972  TESTS: Add test for recreating cache timestamp

    Valters Jansons (1):
        01cc26749  DEBUG: Drop custom syslog identifier from journald

    Weblate (1):
        b38701b9e  Update the translations for the 2.4.1 release

    aborah (1):
        b5c5281c5  TESTS:sssd-kcm does not store TGT with ssh login using GSSAPI

    peptekmail (3):
        568bb1a0f  Add rsassapss cert for future checks
        92ed415cd  Add rsassapss cert for future checks
        7f3576ea3  Add rsassapss cert for future checks

    tobias-gruenewald (3):
        e25f87901  Change LDAP group type from int to string
        afa15cb73  Change LDAP group type from int to string
        2786071e4  Change LDAP group type from int to string
