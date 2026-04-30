SSSD 2.9.9 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

- Security fix for CVE-2026-6245: out-of-bounds read in PAM passkey responder
- During the processing of the pam_sss_gss request SSSD will read the SID from
  the PAC of the Kerberos ticket and might add authentication indicators based
  on the value of the new option pam_gssapi_indicators_apply. The primary use
  case is to handle SIDs added by Active Directory’s Authentication Mechanism
  Assurance (AMA).
- Active Directory’s Foreign Security Principals (FSP) are now properly detected
  and ignored when reading nested group members. The
  ``ldap_ignore_unreadable_references`` option is only needed to ignore member
  objects which are really not accessible.
- A number of cache performance optimizations for large deployments.

Tickets Fixed
-------------

* `#6951 <https://github.com/SSSD/sssd/issues/6951>`__ - NSS enumerated passwd/group truncated output and performance regression since >=2.8.0
* `#8441 <https://github.com/SSSD/sssd/issues/8441>`__ - Failed to resolve indirect group-members of nested non-POSIX group
* `#8514 <https://github.com/SSSD/sssd/issues/8514>`__ - Release tarball contains src/tests/tests
* `#8531 <https://github.com/SSSD/sssd/issues/8531>`__ - backtrace when not providing `krb5_kpasswd` but `krb5_server`

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.8..HEAD

    Alejandro López (9):
        77e17ccf5  SYSDB: Remove unused function
        603b2df64  NSS: Reduce a possibly extremely long log message
        6d7129198  NSS: Fix wrong condition invalidating an optimization
        d220bb024  TESTS: Improve test_sysdb_enumpwent_filter
        27ff11b27  NSS: Some optimizations.
        95633bcf8  NSS: Be coherent when using a lastUpdate filter
        e0e5f3dc9  NSS: Fix the logged function name
        cb11e00ce  NSS: Fix sysdb_enumpwent_filter()
        e738a9dbc  NSS: Better handle ERR_NO_TS in sysdb_enumpwent_filter()
    
    Alexey Tikhonov (31):
        b11cdcca8  CONFIG: allow 'ldap_subuid_*' attrs
        4a7245caf  CHILD HELPERS: use less severe debug level if `child_sig_handler()` is called for unknown pid.
        5596fe54a  SDAP: use `DEBUG_CONDITIONAL` in hot path
        d3634ccc9  UTIL: `sss_tc_utf8_str_tolower()` optimization
        8679758d4  UTIL: `sss_create_internal_fqname()` optimization (caching)
        ebdddfff2  UTIL: fix discarded-qualifiers warning in domain_to_basedn()
        02f1b2f9b  SDAP: fix discarded-qualifiers warning in are_sids_from_same_dom()
        6e8095fc8  SDAP: fix discarded-qualifiers warnings in sdap_parse_range()
        f8532758e  SDAP: fix discarded-qualifiers warning in split_extra_attr()
        52e233c0e  AD: fix discarded-qualifiers warnings in ad_access filter parsing
        39ec5a64d  CERTMAP: fix discarded-qualifiers warnings in sss_certmap.c
        1514c28f4  KRB5: fix discarded-qualifiers warning in compare_principal_realm()
        8ca723a24  Makefile: add missing 'CMOCKA_CFLAGS'
        361b5d2c0  BUILD: supress 'deprecated-declarations' error for cmocka tests
        281ee45f8  sdap: eliminate O(N^2) loop in `sdap_add_incomplete_groups()`
        e830df8e5  LDAP: free tmp var within the loop
        a0c67ac80  memberOf plugin: redundant comparison removed
        52c71afbd  memberOf plugin: swap instead of a shift
        999afa264  memberOf plugin: avoid `ldb_dn_compare()` in `mbof_add_operation()`
        8b452b34d  KRB5: fix mem leak in `authenticate_stored_users()`
        7ccc1b726  UTIL: fix mem leak if `get_active_uid()` fails
        4c183fbb8  SDAP: reduce logger load in the hot path
        d294a73e3  SDAP: use DEBUG_CONDITIONAL in the hot paths
        330f84553  KRB5: log level adjusted
        078b3c286  memberOf plugin: avoid `ldb_dn_compare()` in `mbof_append_addop()`
        a22971a75  memberOf plugin: avoid `ldb_dn_compare()` in `mbof_append_muop`
        01b2bd343  memberOf plugin: use hash table for value dedup in `mbof_append_muop()`
        50ae35feb  KCM: fix use-after-free in `kcm_read_options()`
        ca6629582  Add missing include
        93363d268  PAM/PASSKEY: avoid unnecessary memcpy
        392d07849  IPA: memory leak fixed
    
    Dan Lavu (1):
        6f0c48025  adding subid test
    
    Gleb Popov (1):
        7aa2dbee6  dp_target_id.c: Fix typo "lenght" -> "length"
    
    Hosted Weblate (1):
        970f26ea6  Update translation files
    
    Jakub Vávra (2):
        2dfae252b  Test: Update misc ipa tests to work correctly on stig
        dcc3f9a49  Tests: Housekeeping and Clean Sweep of Sevice/Logging suite
    
    Madhuri Upadhye (4):
        76b6a0eac  Fix test_sudo__case_sensitive_false: use /bin/ls and /bin/cat instead of less/more
        66ec8474d  Tests: Add sleep time in multihost test
        df360cd11  tests: mark KCM TGT renewal test as flaky
        f0f9bdf8a  tests: poll for KCM TGT renewal instead of fixed sleep
    
    Nikola Forró (2):
        3242123cd  Use macro rather than shell expansion for string processing in spec file
        16794c257  Add a default for %samba_package_version
    
    Ondrej Valousek (6):
        f8625df4f  Simplify direct nested group processing
        25c89cb4d  Parser update, cleanup
        dd014f5e5  Tests fix: mock users/groups with objectclasses and expected RFC2307 attrs
        a1df7b479  Bugfix (handle unreadable references) that intg check discovered
        b327adda7  sdap: restrict list of requested attributes
        ea29407b5  Honor ldap filters
    
    Paul Adelsbach (1):
        423a309e4  pam: gate PAC indicator code on BUILD_SAMBA
    
    Pavel Březina (6):
        3bd00e4b8  contrib: removed unused test-suite
        cf35a8f86  dist: clean up and fix ditribution tarball
        312357e9c  scripts: add fixed-issues.sh script
        9fd523b8a  scripts: add generate-release-notes.py script
        9125bc8b6  scripts: add generate-full-release-notes.sh script
        58cbbe66b  ci: automatically generate release notes
    
    Striker Leggette (2):
        d61053e50  Fix spelling in AD provider code comments
        2708dfca3  More trivial spelling/grammatical fixes. No functional code was harmed in the changing of these files.
    
    Sumit Bose (19):
        bb225ef11  man: add details about 'an2ln'
        259bdbadd  sdap: do not require GID for non-POSIX group
        ca09a18e0  sdap: add sdap_get_and_multi_parse_generic_send()
        22d411c88  sdap: use sdap_get_and_multi_parse_generic_send
        dca6755e0  sdap: remove extra parsing
        82fd92aca  ad: add basic foreign security principal sdap map
        badd169fd  sdap: avoid second parsing of objectclasses
        5147c7fc7  tests: add a test with a FSP group member
        e6545f702  sdap: new type SDAP_NESTED_GROUP_DN_IGNORE
        1b141d827  sdap: add struct sdap_reply_with_type
        45bc31329  sdap: add struct sdap_attr_map_info_ex
        8f5beeb21  sdap: re-add IPA shortcut for nested members
        d1dd2769e  sdap: initialize attribute list only once
        284469586  sdap: initialize base filter only once
        8fa27a0e2  sdap: change increment style for reply array
        fa4f7ed84  tests: remove wrong and misleading assigment
        1df058515  ad: move ad_get_sids_from_pac() to ad_pac_common.c
        5d36c320c  pam: add pam_gssapi_indicators_apply option
        dc75971c6  pam: apply SIDs from PAC to authentication indicators
    
    Xu Raoqing (1):
        d62cd9393  pam: fix out-of-bounds read in pam_passkey_child_read_data
    
    aborah-sudo (1):
        d412ffa72  tests: reorganize infopipe tests by interface
    
    dependabot[bot] (2):
        5064ed168  ci: bump actions/upload-artifact from 6 to 7
        5c5d64455  ci: bump crazy-max/ghaction-import-gpg from 6.3.0 to 7.0.0
    
    sssd-bot (2):
        becf284ec  pot: update pot files
        6017c6538  Release sssd-2.9.9

