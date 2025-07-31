SSSD 2.11.1 Release Notes
=========================

This is a minor bugfix update.

Tickets Fixed
-------------

* `#7921 <https://github.com/SSSD/sssd/issues/7921>`__ - AD user in external group is not cleared when expiring the cache
* `#7968 <https://github.com/SSSD/sssd/issues/7968>`__ - cache_credentials = true not working in sssd master
* `#8005 <https://github.com/SSSD/sssd/issues/8005>`__ - Socket activation doesn't work for 'sssd_pam'

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.11.0..2.11.1

    Alexey Tikhonov (5):
        e23844357  PAM: keep 'LISTEN_PID' and 'LISTEN_FDS'
        76b160e3e  'gemini-code-assist' config
        4e7ae2422  SPEC: add missing '\'
        f51065918  Make sure previously rotated logs are chown-ed as well.
        30f03098a  spec: don't dereference links while chown-ing in %post

    André Boscatto (1):
        9129d890c  tests: Adding nested group test case for simple access control

    Dan Lavu (3):
        c5eb5b141  adding pytest markers to help keep track of transformation status
        c34e24cc3  tests: skipping simple access control tests that have been rewritten.
        f0e6650d2  removing deprecated pam_ldap pam_krb proxy provider multihost tests

    Jakub Vávra (3):
        963e31606  Tests: Move test_ldap_referrals from gating (tier1)
        7d4affed8  Tests: Add missing markers for ticket plugin
        e013f9599  Tests: Move test_sssctl__analyze_without_root_privileges from gating

    Pavel Březina (23):
        cd54cd0fb  spec: remove old Obsoletes
        0e6e3c275  spec: remove old Provides
        18dbf893d  spec: always build with sssd user
        13d05a9bf  spec: always use sysusers to create the sssd user
        aea12fede  spec: remove build_subid condition as it is always enabled
        2faa4c3f5  spec: always build kcm renewals
        d941f86d7  spec: remove build_passkey as it is always enabled
        d2c8841e2  spec: build idp only on f43+ and rhel10+
        31e9170bc  spec: remove _hardened_build
        32d80c52a  spec: remove ldb_version
        7fa5f5d15  spec: add comment to samba_package_version
        131c97f18  spec: move packages required for p11_child tests together
        fd5e2b32d  spec: remove systemtap-sdt-dtrace version condition
        096a59fdf  spec: use upstream_version variable when producing downstream_version
        60f13397e  spec: use autochangelog
        710f4ff88  spec: target f41+ and rhel10+
        ba905e827  spec: use version_no_tilde
        d06f9b5ff  spec: use correct url for the tarball
        1e1cfc4c2  spec: support gpg verification
        a7b96f0ec  ci: add packit configuration
        5698d6059  ci: remove custom copr builds
        6fd3415e1  pot: update pot files
        ced937c9d  Release sssd-2.11.1

    Sumit Bose (4):
        2ace6155f  sysdb: add sysdb_get_direct_parents_ex()
        63a6f5106  ipa: improve handling of external group memberships
        706a673ae  authtok: add IS_PW_OR_ST_AUTHTOK()
        856d20a37  krb5: offline with SSS_AUTHTOK_TYPE_PAM_STACKED

    Yuri Chornoivan (4):
        e0ca338d2  Fix typo in sssd-ldap.5.xml
        2024de506  Fix typo in sssd-idp.5.xml
        03bff005d  Fix typos in sss-certmap.5.xml
        2c9a3d443  Update sss-certmap.5.xml

    fossdd (1):
        4c3ce6773  sss_prctl: avoid redefinition of prctl_mm_map

    krishnavema (1):
        5757dfdbb  tests: adding user su smartcard login test

    shridhargadekar (1):
        61a5ab6c5  Tests: cache_credentials = true not working
