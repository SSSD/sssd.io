SSSD 2.9.7 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* When both IPv4 and IPv6 address families are resolvable, but the primary is
  blocked on firewall, SSSD attempts to connect to the server on the secondary
  family.

New features
~~~~~~~~~~~~

* SSSD IPA provider now supports IPA subdomains, not only Active Directory.
  This IPA subdomain support will enable SSSD support of IPA-IPA Trust feature,
  the full usable feature coming in a later FreeIPA release. Trusted domain
  configuration options are specified in the 'sssd-ipa' man page.

Important fixes
~~~~~~~~~~~~~~~

* 'sssd_kcm' memory leak was fixed.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* New 'ldap_read_rootdse' option allows you to specify how SSSD will read RootDSE
  from the LDAP server. Allowed values are "anonymous", "authenticated" and "never"
* Until now dyndns_iface option supported only "*" for all interfaces or exact names. With
  this update it is possible to use shell wildcard patterns (e. g. eth*, eth[01], ...).


Tickets Fixed
-------------

* `#6601 <https://github.com/SSSD/sssd/issues/6601>`__ - smartcard login fails when network disconnected
* `#6665 <https://github.com/SSSD/sssd/issues/6665>`__ - LDAP auth happens after search failure
* `#6910 <https://github.com/SSSD/sssd/issues/6910>`__ - SSSD dyndns_ifname with wildcard
* `#7209 <https://github.com/SSSD/sssd/issues/7209>`__ - Tests: util-tests fails if time zone is not UTC
* `#7746 <https://github.com/SSSD/sssd/issues/7746>`__ - krb5_child couldn't parse pkcs11 objects if token label contains semicolon
* `#7793 <https://github.com/SSSD/sssd/issues/7793>`__ - Disk cache failure with large db sizes
* `#7876 <https://github.com/SSSD/sssd/issues/7876>`__ - Group enumeration does not work if group name contains '#'
* `#7931 <https://github.com/SSSD/sssd/issues/7931>`__ - LDAPU1 Local auth mapping rule error


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.6..2.9.7

    Alexander Bokovoy (1):
        b237fe960  oidc_child: fallback to ID and access tokens when looking up configured user identity

    Alexey Tikhonov (41):
        15e0eef9d  Ignore '--dumpable' argument in 'krb5_child' and 'ldap_child' to avoid leaking host keytab accidentially.
        90a6a1ff9  CERT: mistype fix
        60b1ae48d  certmap: remove stray export declaration
        6aba9a7dd  KCM: fix memory leak
        3bd7461fd  TESTS: fix issue reported by 'black'
        e7c76df8c  KCM: another memory leak fixed
        ed9fe4cb1  CI: update list of target platforms
        addb1a781  SYSDB: don't add group members if 'ignore_group_members == true'
        73f6c4a70  SYSDB: update in sysdb_add_group_member_overrides()
        ccc90e2fb  SYSDB: update in sysdb_add_group_member_overrides()
        f7964c992  SYSDB: update in sysdb_add_group_member_overrides()
        648404964  SYSDB: fix sysdb_add_group_member_overrides()
        638b904c1  SYSDB: update in sysdb_add_group_member_overrides()
        c4100177b  SYSDB: update in sysdb_add_group_member_overrides()
        3477221b9  SYSDB: update in sysdb_add_group_member_overrides()
        02a599530  SYSDB: update in sysdb_add_group_member_overrides()
        668533424  SYSDB: make `sysdb_get_user_members_recursively()` static
        b64d205c0  SYSDB: update in get_user_members_recursively()
        e1eae1cae  SYSDB: update in sysdb_add_group_member_overrides()
        0e479b71b  SYSDB: update in sysdb_add_group_member_overrides()
        8b4b4e334  SYSDB: debug message fixed
        e6216ef4b  SYSDB: update in sysdb_add_group_member_overrides()
        c3b37ab4f  SYSDB: update in get_user_members_recursively()
        03cef2f42  DEBUG: a new helper that skips backtrace
        9a7ecff04  Avoid logging to the backtrace unconditionally in hot paths.
        87d105420  UTIL: sss_parse_internal_fqname() optimization
        0088d4095  UTIL: sss_parse_internal_fqname() optimization
        c44fbb651  UTIL: sized_domain_name() optimization
        3b1d79b92  RESPONDER: sized_output_name() optimization
        84322c3d6  UTIL: sss_output_name() optimization
        23f06186a  RESPONDER: delete sss_resp_create_fqname()
        5698ee0c9  UTIL: remake sss_*replace_space() to inplace version
        7e064f6fe  UTIL: delete sss_fqname()
        50e9b7aa8  UTIL: sss_tc_fqname2() optimization
        cb6350b2f  SPEC: relax Samba version req a bit
        6ab380f5a  DB: skip sysdb_add_group_member_overrides() completely
        bf034fa70  DB: don't provide 'expect_override_dn' to `sysdb_add_group_member_overrides()`
        8cef0a5d9  UTIL: mark non string array properly
        ecaa49c91  IPA: return ENOENT if `ipa_get_config` yields nothing
        9878ac25d  PAM: fixes following issue:
        19bd4c497  Release sssd-2.9.7

    André Boscatto (2):
        cf0d337af  man: Updating sssd-simple(5) man page
        5f37296b4  TESTS: Add access control simple filter tests

    Dan Lavu (5):
        e4e9dc495  tests: test_kcm.py fixing confusing error message
        4381cc510  tests: extending sss_override testcase to assert overridden user group memberships
        139dfc71a  moving ad topology test to it's own file test_ad.py
        e4bd8b987  tests: adding generic password change tests * user is forced to changed password at login * user logins and issues a password change
        2c1cbe850  tests: removed overlapping test scenarios from authentication tests * few scenarios have been removed * ppolicy tests have been made into ppolicy tests only, since normal ldap is covered by the generic provider now * renamed some of the test cases * removed su from a password change test * removed some test cases that are now covered by the new test cases

    Dominika Borges (1):
        de0220070  doc: improve description of ldap_disable_range_retrieval

    Iker Pedrosa (2):
        f068ba004  tests: add feature presence automation
        eafffce6f  tests: improve feature presence automation

    Ivan Korytov (1):
        91fe7678b  tests: Update mock date to postpone timezone related failures

    Jakub Vávra (2):
        5607973de  tests: Update mhc.yaml for relocated /data and /enrollment
        f944b00ca  tests: Move /exports to /var/exports for autofs tests

    Jan Engelhardt (1):
        f34626a5e  sssd: always print path when config object is rejected

    Justin Stephenson (23):
        384f67ed7  DEBUG: lower missing passkey data debug level
        d0d8b0a5e  tests: have analyzer request child parse child log
        2b5168214  ci: Remove internal covscan workflow
        33855f726  ci: Add workflow for 'coverity' label in PRs
        95d198dfd  CI: Fix coverity label multiline conditional
        1bf60984f  ci: Have coverity workflow run against PR code
        dfef948f3  SYSDB: Store IPA trust type
        af30e1f93  Rename struct ipa_ad_server_ctx, and add id_ctx union member
        19e30002b  ipa: Make ipa_service_init() like ad_failover_init()
        a05dc1e2a  ad: Combine 1+2way trust options creation functions
        e34d8d7df  ipa: Make ipa server ad* functions generic
        07f0cdbd3  ipa: Add ipa subdomain provider initialization
        cb53396e0  ipa: Support ipa subdomain account info requests
        e23431014  ipa s2n: Remove check for SYSDB_UPN
        69566f1fa  ipa: Rename ipa_create_ad_1way_trust_ctx()
        f811d944c  Handle missing SID for user private group
        b234d1ea5  ipa s2n: Ignore trusted IPA user private group
        f23428673  AD: Remove unused AD_AT_TRUST_TYPE attribute
        49e3bcb3b  man: IPA subdomain changes to sssd-ipa
        3bc17c672  ipa: Set proper domain basedn for subdomain options
        5c480941f  ci: include build description for covscan
        b24c151d1  ci: Use pull_request_target for conditional
        bbb7b7967  IPA: ipa_get_config_send() was updated

    Krzesimir Nowak (1):
        ee195e776  Assume that callbacks are not broken in OpenLDAP when cross-compiling

    Michael Stone (3):
        a6273e7ff  return here so MINOR_FAILURE isn't auto-promoted to FATAL_FAILURE
        1eee5a4c4  make log line match preceeding function name
        1341a970e  add SSS_AUTHTOK_TYPE_PAM_STACKED

    Pavel Březina (2):
        910575e8a  ci: grab ipa logs from ipa host
        9200ee29a  ci: print duration of each test case

    Samuel Cabrero (1):
        4f9fb5fd3  SYSDB: Use SYSDB_NAME from cached entry when updating users and groups

    Sumit Bose (5):
        2a8349049  krb5_child: ignore Smartcard identifiers with a ':'
        50ebb7441  sdap: include sub-domain memberships in updates
        42805f875  certmap: allow prefix in rule in sssd.conf
        29506a5b7  oidc_child: change verify_token() to decode_token()
        67c6d3fa0  Revert "sdap: include sub-domain memberships in updates"

    Tomas Halman (9):
        5239cdab1  Pattern support for dyndns_iface option
        d9ee62797  man: clarify %o and %h homedir substitution
        1e9205d28  Configure how SSSD should access RootDSE.
        53365dcfd  test: enumeration with # in the group name
        116d6221c  Enumerate object with escaped characters in name
        c1693bbce  failover: Make failover work over IP families
        511003c8b  failover: fix fo_is_ip_address check
        47df70968  tests: Check failover to secondary IP family
        3ae9b5aab  p11_child: Add timeout parameter

    aborah-sudo (1):
        4d2a09eb5  Tests: Add proxy provider test cases for SSSD

    fossdd (1):
        ec174a043  Fix missing include sys/types.h

    shridhargadekar (1):
        001069311  Tests: add importance marker for sssctl analyze
