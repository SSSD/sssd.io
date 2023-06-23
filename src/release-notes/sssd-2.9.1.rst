SSSD 2.9.1 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

* Passkey: added option to write key mapping data to file.

Important fixes
~~~~~~~~~~~~~~~

* A regression was fixed that prevented autofs lookups to function correctly
  when cache_first is set to True. Since this was set as a new default value in
  sssd-2.9.0, it is considered as a regression.

* A regression where SSSD failed to properly watch for changes in
  '/etc/resolv.conf' when it was a symbolic link or was a relative path, was
  fixed.

Tickets Fixed
-------------

* `#6442 <https://github.com/SSSD/sssd/issues/6442>`__ - PAC errors when no PAC configured
* `#6652 <https://github.com/SSSD/sssd/issues/6652>`__ - IPA: previously cached netgroup member is not remove correctly after it is removed from ipa
* `#6659 <https://github.com/SSSD/sssd/issues/6659>`__ - sssd_be segfault at 0 ip 00007f16b5fcab7e sp 00007fffc1cc0988 error 4 in libc-2.28.so[7f16b5e72000+1bc000]
* `#6718 <https://github.com/SSSD/sssd/issues/6718>`__ - file_watch-tests fail in v2.9.0 on Arch Linux
* `#6720 <https://github.com/SSSD/sssd/issues/6720>`__ - [sssd] User lookup on IPA client fails with 's2n get_fqlist request failed'
* `#6739 <https://github.com/SSSD/sssd/issues/6739>`__ - autofs mounts: Access to non-existent file very slow since 2.9.0
* `#6744 <https://github.com/SSSD/sssd/issues/6744>`__ - sssd-be tends to run out of system resources, hitting the maximum number of open files
* `#6766 <https://github.com/SSSD/sssd/issues/6766>`__ - [RHEL8] sssd : AD user login problem when modify ldap_user_name= name and restricted by GPO Policy
* `#6768 <https://github.com/SSSD/sssd/issues/6768>`__ - [RHEL8] sssd attempts LDAP password modify extended op after BIND failure

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.0..2.9.1

    Alejandro López (12):
        eb43c2400  FILE WATCH: Callback not executed on link or relative path
        0c6f4926e  TESTS: Fix doble slash comments
        58855b712  SYSDB: Make enum sysdb_obj_type public
        3eb4c4a7e  IPA: Use a more specific filter when searching for BE_REQ_USER_AND_GROUP
        6239f50f6  PAM: Fix a possible segmentation fault
        4b0683bda  AD: The shortcut must be used equally on _send() and _done()
        509222428  TEST: Fix pam-srv-tests to correctly treat the test name
        228183bf4  IPA: Do not try to add duplicate values to the LDAP attributes
        42cf3c41c  UTIL: New function string_in_list_size()
        010e61ffa  UTIL: add_strings_lists() becomes add_strings_lists_ex()
        bfc88dc3c  RESPONDER: attr_in_list() is replaced by string_in_list_size()
        355b0c2e8  IPA: Do not duplicate the entry attributes.

    Alexey Tikhonov (3):
        15dd35454  MAN: fix issue with multithread build
        d9749ba1f  RESPONDER: avoid log backtrace in case access denined
        d3c3408e0  SYSDB: in case (ignore_group_members == true) group is actually complete

    Dan Lavu (1):
        33f10c4a5  Updating ad_multihost test

    Elena Mishina (1):
        8d3acd3b9  po: update translations

    Iker Pedrosa (1):
        425d88fa7  passkey: write mapping data to file

    Jakub Vavra (4):
        2466310e8  Tests: Modify expiring/expired password test for RHEL 8.
        0192c1c8f  Tests: Add conditional skip for simple ifp test.
        58a007de8  Tests: Skip test_0016_ad_parameters_ad_hostname_valid on other architectures.
        19fecbf17  Tests: Improve stability of test_0004_bz2110091

    Justin Stephenson (2):
        270f0ba01  Passkey: Adjust IPA passkey config error log level
        16275d9b4  IPA: Log missing IPA config data on default level

    Kemal Oktay Aktoğan (1):
        d37d72f0e  po: update translations

    Ludek Janda (3):
        d95212b26  po: update translations
        4f469c0b5  po: update translations
        c40d183cd  po: update translations

    Madhuri Upadhye (4):
        6d0608180  Tests: Gating fixes for RHEL8.9 and RHEL9.3
        e4e8e3444  Tests: Add package for tc command
        256e013a8  Test: Test search filter specific user override or a specific group override
        301e5b389  Tests: When adding attributes ldap_user_extra_attrs with mail value in sssd.conf the cross-forest query stop working

    Pavel Březina (5):
        640f41588  ipa: correctly remove missing attributes on netgroup update
        5711bb253  cache_req: remove unused field cache_behavior from state
        bc5fe9eb0  cache_req: fix propagation of offline status with cache_first = true
        7f6c10dce  pot: update pot files
        dc8d649bc  Release sssd-2.9.1

    Piotr Drąg (1):
        f0d8f9364  po: update translations

    Shridhar Gadekar (5):
        60806f593  Tests: move unstable default_debug to tier2
        a74d42dfa  Tests: fix default debug level for typo
        74c6fefe1  Tests: move test_access_control.py to tier2
        6125efe1f  Tests: Adding c-ares markers for related tests
        02b158ff7  Test: dropping unstable dyndns tests

    Sumit Bose (6):
        d104c01f1  sysdb: fix string comparison when checking for overrides
        e5dfa2a8c  AD: add missing AD_AT_DOMAIN_NAME for sub-domain search
        4d2cf0b62  krb5: make sure sockets are closed on timeouts
        f63a54c3d  fail_over: protect against a segmentation fault
        895d194f3  ldap: return failure if there are no grace logins left
        5008f0f92  ad: use sAMAccountName to lookup hosts

    Temuri Doghonadze (1):
        a94f39f0c  po: update translations

    Yuri Chornoivan (1):
        abce376ce  po: update translations

    aborah (4):
        de75ff3c4  Tests: Fix gating tests for 9.3
        b9a0b4245  Tests: Netgroups do not honor entry cache nowait percentage
        bb64f2cd2  Tests: Skip test_0001_bz2021196
        05bc18ce9  Tests: Add ssh module that is fast, reliable, accurate

    김인수 (2):
        aa0615948  po: update translations
        8e80798d5  po: update translations
