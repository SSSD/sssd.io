SSSD 2.4.0 Release Notes
========================

Highlights
----------

-  ``libnss`` support was dropped, SSSD now supports only ``openssl`` cryptography

New features
~~~~~~~~~~~~

-  Session recording can now exclude specific users or groups when ``scope`` is set to ``all`` (see ``exclude_users`` and ``exclude_groups`` options)
-  Active Directory provider now sends CLDAP pings over UDP protocol to Domain Controllers in parallel to determine site and forest to speed up server discovery

Packaging changes
~~~~~~~~~~~~~~~~~

-  python2 bindings are disable by default, use ``--with-python2-bindings`` to build it

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

-  Default value of ``client_idle_timeout`` changed from 60 to 300 seconds for KCM, this allows more time for user interaction (e.g. during ``kinit``)
-  Added ``exclude_users`` and ``exclude_groups`` option to ``session_recording`` section, this allows to exclude user or groups from session recording when ``scope`` is set to ``all``
-  Added ``ldap_library_debug_level`` option to enable debug messages from ``libldap``
-  Added ``dyndns_auth_ptr`` to set authentication mechanism for PTR DNS records update
-  Added ``ad_allow_remote_domain_local_groups`` to be compatible with other solutions

Tickets Fixed
-------------

-  `#1030 <https://github.com/SSSD/sssd/issues/1030>`_ - Excessive dependencies on ``libsss_certmap``
-  `#1041 <https://github.com/SSSD/sssd/issues/1041>`_ - Deprecate and eventually get rid of support of NSS as a crypto backend
-  `#3743 <https://github.com/SSSD/sssd/issues/3743>`_ - RFE: Improve AD site discovery process
-  `#3987 <https://github.com/SSSD/sssd/issues/3987>`_ - "domains" description in pam_sss(8) is misleading
-  `#4569 <https://github.com/SSSD/sssd/issues/4569>`_ - IFP: org.freedesktop.sssd.infopipe.GetUserGroups does not take SYSDB_PRIMARY_GROUP_GIDNUM into account
-  `#4733 <https://github.com/SSSD/sssd/issues/4733>`_ - Access after free during kcm shutdown with a non-empty queue
-  `#4743 <https://github.com/SSSD/sssd/issues/4743>`_ - [RFE] Add "enabled" option to domain section
-  `#4829 <https://github.com/SSSD/sssd/issues/4829>`_ - KCM: Increase the default client idle timeout, consider decreasing the timeout on busy servers
-  `#4840 <https://github.com/SSSD/sssd/issues/4840>`_ - gpo: use correct base dn
-  `#5002 <https://github.com/SSSD/sssd/issues/5002>`_ - p11_child::do_ocsp() function implementation is not FIPS140 compliant
-  `#5061 <https://github.com/SSSD/sssd/issues/5061>`_ - [RFE] Add a new mode for ad_gpo_implicit_deny
-  `#5089 <https://github.com/SSSD/sssd/issues/5089>`_ - Enable exclusions in the sssd-session-recording configuration
-  `#5097 <https://github.com/SSSD/sssd/issues/5097>`_ - please migrate to the new Fedora translation platform
-  `#5215 <https://github.com/SSSD/sssd/issues/5215>`_ - SSSD uses only TCP/IP stream to send CLDAP request
-  `#5256 <https://github.com/SSSD/sssd/issues/5256>`_ - ``getent networks ip`` is not working
-  `#5259 <https://github.com/SSSD/sssd/issues/5259>`_ - False errors/warnings are logged in sssd.log file after enabling 2FA prompting settings in sssd.conf
-  `#5261 <https://github.com/SSSD/sssd/issues/5261>`_ - Secondary LDAP group go missing from 'id' command on RHEL 7.8 with sssd-1.16.2-37.el7_8.1
-  `#5274 <https://github.com/SSSD/sssd/issues/5274>`_ - dyndns: asym auth for nsupdate
-  `#5278 <https://github.com/SSSD/sssd/issues/5278>`_ - sss-certmap man page change to add clarification for userPrincipalName attribute from AD schema
-  `#5290 <https://github.com/SSSD/sssd/issues/5290>`_ - krb5_child denies ssh users when pki device detected
-  `#5295 <https://github.com/SSSD/sssd/issues/5295>`_ - Crash in ad_get_account_domain_search()
-  `#5314 <https://github.com/SSSD/sssd/issues/5314>`_ - Attribute 'ldap_sasl_realm' is not allowed in section 'domain/example.com'. Check for typos.
-  `#5325 <https://github.com/SSSD/sssd/issues/5325>`_ - correction in sssd.conf man page
-  `#5330 <https://github.com/SSSD/sssd/issues/5330>`_ - automount sssd issue when 2 automount maps have the same key (one un uppercase, one in lowercase)
-  `#5333 <https://github.com/SSSD/sssd/issues/5333>`_ - sssd-kcm does not store TGT with ssh login using GSSAPI
-  `#5338 <https://github.com/SSSD/sssd/issues/5338>`_ - [RFE] sssd-ldap man page modification for parameter "ldap_referrals"
-  `#5346 <https://github.com/SSSD/sssd/issues/5346>`_ - [RfE] Implement a new sssd.conf option to disable the filter for AD domain local groups from trusted domains

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-2_3_1..sssd-2_4_0

    Alexey Tikhonov (27):
        4ad1dfa35  Got rid of unused Transifex settings (".tx")
        70898d98a  Got rid of "zanata.xml" due to migration to Weblate.
        10366b4ee  p11_child: switch default ocsp_dgst to sha1
        266ecc083  Drop support of libnss as a crypto backend
        a2911482a  Get rid of "NSS DB" references.
        83ae34509  CONFDB: fixed compilation warning
        fbc708214  CONFDB: fixed bug in confdb_get_domain_enabled()
        67b3f3717  CLIENT:PAM: fixed missed return check
        245dea6ea  PAM responder: fixed compilation warning
        93bcfd159  KCM: supress false positive cppcheck warnings
        c273a78c3  RESOLV: makes use of sss_rand() helper
        20b8b9555  UTIL: fortify IS_SSSD_ERROR() check
        4c218a55f  LDAP: sdap_parse_entry() optimization
        0c193e827  DP: fixes couple of covscan's complains
        f434fedf3  cmocka based tests: explicitly turn LTO off
        d34eb9633  Makefile.am: get rid of `libsss_nss_idmap_tests`
        5f23f2373  sss_nss_idmap-tests: fixed error in iteration over `test_data`
        62aceaf93  UTIL:utf8: code cleanup
        a0bf4b3d1  UTIL:utf8: moved a couple of helper
        8fa702321  AD: validate `search_bases` in DPM_ACCT_DOMAIN_HANDLER
        edec0ee31  DP:getAccountDomain: add DP_FAST_REPLY support
        1b0167746  Got rid of unused providers/data_provider/dp_pam_data.h
        d1ed68bda  UTILS: adds helper to convert authtok type to str
        038385dd9  krb5_child: fixed few mistypes in debug messages
        445812769  parse_krb5_child_response: adds verbosity
        68497dc1a  krb5_child: adds verbosity
        d1e5d1882  krb5_child: reduce log severity in sss_krb5_prompter

    Anuj Borah (1):
        2f4140fa6  libdirsrv should be modified to be compatible with new DS

    Duncan Eastoe (4):
        b1ef82b6b  data_provider_be: Configurable max offline time
        7807ffd7c  be_ptask: max_backoff may not be reached
        904ff17cc  be_ptask: backoff not applied on first re-schedule
        04ea42208  data_provider_be: Add OFFLINE_TIMEOUT_DEFAULT

    Joakim Tjernlund (1):
        0b069085c  Add dyndns_auth_ptr support

    Jonatan Pålsson (1):
        2b73285ef  build: Don't use AC_CHECK_FILE when building manpages

    Justin Stephenson (11):
        00ae18dc9  KCM: Increase client idle timeout to 5 minutes
        a4af77e08  CONFIG: Add SR exclude_users exclude_groups options
        0049ec855  UTIL: Add support for SR exclude_users exclude_groups
        38df7a3bb  NSS: Rely on sessionRecording attribute
        3a3be1cba  PAM: Rely on sessionRecording attribute
        c51a9f6be  DP: Support SR excludes in initgroups postprocessing
        19602d9a8  CACHE_REQ: Support SR exclude options
        d947ac7af  INTG: Add session recording exclude tests
        733cafd72  MAN: Add SR exclude_users and exclude_groups options
        f126afc98  KCM: Fix GSSAPI delegation for the memory back end
        d39b6580a  KCM: Fix access after free on shutdown

    Luiz Angelo Daros de Luca (2):
        05c06cd66  ldap: add ldap_sasl_realm to cfg_rules.ini
        cf15e9eac  SSSCTL: fix logs-remove when log directory is empty

    Lukas Slebodnik (20):
        bb7d80d21  DLOPEN-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        7e44cfd91  SYSDB-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        a0945dca1  SYSDB-TESTS: Fix format string
        bae2b416e  STRTONUM-TESTS: Fix format string issues
        4954da70b  RESOLV-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        dc598c53e  KRB5-UTILS-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        d46b44f34  KRB5-UTILS-TESTS: Fix format string issues
        692f6b7ed  CHECK-AND-OPEN-TESTS: Fix format string issues
        0b89f5117  REFCOUNT-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        1bb423812  FAIL-OVER-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        a933f60ed  FAIL-OVER-TESTS: Fix format string issues
        6c5374f93  AUTH-TESTS: Fix format string issues
        e2dc5c3b3  IPA-LDAP-OPT-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        0c20b4bdd  CRYPTO-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        2e2703676  UTIL-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        2cb158559  UTIL-TESTS: Fix format string issues
        da64aea71  IPA-HBAC-TESTS: Fix error too few arguments to function ‘_ck_assert_failed’
        cc8962105  SSS-IDMAP-TESTS: Fix format string issues
        c445d1694  RESPONDER-SOCKET-ACCESS-TESTS: Fix format string issues
        d47e442dc  DEBUG-TESTS: Fix warnings format not a string literal and no format arguments

    Niranjan M.R (1):
        f4322cd95  pytest/testlib: Execute pk12util command to create ca.p12

    Pavel Březina (21):
        bb48af24e  Update version in version.m4 to track the next release
        d79f59338  gpo: remove unused variable domain_dn
        a0792b32f  gpo: use correct base dn
        4a84f8e18  dp: fix potential race condition in provider's sbus server
        abd19122d  conf: disable python2 bindings by default
        7fbcaa8fe  be: remove accidental sleep
        414593cca  ldap: add support for cldap and udp connections
        8265674a0  ad: use cldap for site and forrest discover (perform CLDAP ping)
        1889ca60a  ad: connect to the first available server for cldap ping
        fcfd834c9  ad: if all in-site dc are unreachable try off-site controllers
        a62a13ae6  man: fix typo in failover description
        9fdf5cfac  ad: renew site information only when SSSD was previously offline
        f0d650799  tevent: correctly handle req timeout error
        93e35c760  autofs: if more then one entry is found store all of them
        b427e0595  pot: update pot files to allow updated translations
        78f221edc  multihost: move sssd.testlib closer to tests
        974b4e90b  multihost: remove packaging files
        3379dac2e  spec: enable kcm by default
        d7d531413  tests: run TIER-0 multihost tests in PRCI
        ad6944118  git-template: add tags to help with release notes automation
        51db6a23a  Release sssd-2.4.0

    Samuel Cabrero (7):
        430e695a0  PROXY: Fix iphost not found code path in get_host_by_name_internal
        9d350e040  NSS: Fix get ip network by address when address type is AF_UNSPEC
        2c456951a  NSS: Fix _nss_sss_getnetbyaddr_r address byte order
        a590fd98e  PROXY: getnetbyaddr_r expects the net argument in host byte order
        9edc3c49c  TESTS: getnetbyaddr_r expects network in host byte order
        69af6848f  TESTS: Fix resolver test calling getnetbyname instead of getnetbyaddr
        77734063f  TESTS: Extend resolver tests to check getnetbyaddr with AF_UNSPEC

    Simo Sorce (1):
        bc1ce6f0c  krb5_child: Harden credentials validation code

    Steeve Goveas (3):
        20787da9d  use prerealease option in make srpm script
        39c564bec  Add seconds in copr version
        dda652a21  enable files domain in copr builds for testing

    Sumit Bose (16):
        69e1f5fe7  GPO: respect ad_gpo_implicit_deny when evaluation rules
        b50521e46  cache_req: allow to restrict the domains an object is search in
        6ec94790e  tests: add unit-test for cache_req_data_set_requested_domains
        3808c04fb  pam: use requested_domains to restrict cache_req searches
        db170d0a4  intg: krb5 auth and pam_sss domains option test
        35ab0493a  pam_sss: clarify man page entry of domains option
        bca413267  krb5: only try pkinit with Smartcard credentials
        5fb22633d  ldap: add new option ldap_library_debug_level
        50d0d154c  ldap: use member DN to create ghost user hash table
        88631392e  intg: allow member DN to have a different case
        37ba37a42  ad: fix handling of current site and forest in cldap ping
        4f65a8d15  ad: add ad_allow_remote_domain_local_groups
        5c309f52b  cert: move cert_to_ssh_key_send/recv() to ssh responder
        deefae789  sysdb: add sysdb_cert_derb64_to_ldap_filter()
        7fcc8b0e3  cert: move sss_cert_derb64_to_ldap_filter() out of libsss_cert.so
        bb50ad830  build: remove libsss_certmap from dependencies of libsss_cert

    Thorsten Scherf (2):
        b377253b7  MAN: fix 'pam_responsive_filter' option type
        e5bdc0b72  MAN: update 'ldap_referrals' config entry

    Timothée Ravier (1):
        a409ffae9  sss_cache: Do nothing if SYSTEMD_OFFLINE=1

    Tomas Halman (3):
        093061f55  UTIL: DN sanitization
        21b9417e1  UTIL: Use sss_sanitize_dn where we deal with DN
        fe0f1e64e  UTIL: Use sss_sanitize_dn where we deal with DN 2

    Weblate (1):
        c94d91c46  Update the translations for the 2.4.0 release

    ikerexxe (8):
        3bb910503  man: clarify AD certificate rule
        4526858ad  config: allow prompting options in configuration
        838baa837  util/sss_python: change MODINITERROR to dereference module
        c008d899f  python/pysss_nss_idmap: check return from functions
        8b1a8cf93  python/pyhbac: if PyModule* fails decrement references
        03b00f72e  python/pysss: if PyModule* fails decrement references
        49481da2f  IFP: GetUserGroups() returns origPrimaryGroupGidNumber
        5ddabede9  IFP-TESTS: GetUserGroups() returns origPrimaryGroupGidNumber
