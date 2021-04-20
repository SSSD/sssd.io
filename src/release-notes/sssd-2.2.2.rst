SSSD 2.2.2 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

None

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  Removing domain from ad_enabled_domain was not reflected in SSSD's cache. This has been fixed.
-  Because of a race condition SSSD could crash during shutdown. The race condition was fixed.
-  Fixed a bug that limited number of external groups fetched by SSSD to 2000.
-  pam_sss now properly creates gnome keyring during login.
-  SSSD with KCM could wrongly pick older ccache instead of the latest one after login. This was fixed.

Packaging Changes
-----------------

None

Documentation Changes
---------------------

None

Tickets Fixed
-------------

-  `#4912 <https://github.com/SSSD/sssd/issues/4912>`_ - MAN: Document that PAM stack contains the systemd-user service in the account phase in recent distributions
-  `#4980 <https://github.com/SSSD/sssd/issues/4980>`_ - Removing domain from ad_enabled_domains is not reflected in cache
-  `#5026 <https://github.com/SSSD/sssd/issues/5026>`_ - Paging not enabled when fetching external groups, limits the number of external groups to 2000
-  `#5031 <https://github.com/SSSD/sssd/issues/5031>`_ - sssd-kcm: type confusion on KDC offset
-  `#5035 <https://github.com/SSSD/sssd/issues/5035>`_ - pam_sss with smartcard auth does not create gnome keyring
-  `#5036 <https://github.com/SSSD/sssd/issues/5036>`_ - pam_sss: empty smart card pin registers as authentication attempt
-  `#5037 <https://github.com/SSSD/sssd/issues/5037>`_ - pam_sss should reset PAM_USER based on use_fully_qualified_names option in sssd.conf
-  `#4968 <https://github.com/SSSD/sssd/issues/4968>`_ - sudo: do not update last usn when updating expired rules
-  `#5033 <https://github.com/SSSD/sssd/issues/5033>`_ - IFP: GetUserAttr does not search by UPN
-  `#5042 <https://github.com/SSSD/sssd/issues/5042>`_ - Integration tests use python2 unconditionally

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-2_2_1..sssd-2_2_2

    Jakub Hrozek (6):
        820151f38  MAN: Document that PAM stack contains the systemd-user service in the account phase in RHEL-8
        c2e24df43  IPA: Allow paging when fetching external groups
        c580c76a2  KCM: Use int32_t type conversion in DEBUG message for int32_t variable
        6b0570022  KCM: Add a forgotten return
        f5f7f26a3  KCM: Allow modifications of ccache's principal
        0216bfe2c  KCM: Fill empty cache, do not initialize a new one

    Lukas Slebodnik (18):
        078ed8db6  BUILD: Add macro for checking python3 modules
        b262a7b87  BUILD: Fix typo of detecting python module for intgcheck
        e7d1c1529  BUILD: Move checking of python2 modules for intgcheck
        87e97bb0b  BUILD: Add macro for checking pytest for intgcheck
        b0ad68609  BUILD: Change value of variable HAVE_PYTHON2/3_BINDINGS
        4378d949d  BUILD: Move python checks for intgcheck to macro
        05aad0303  INTG: Do hot hardcode version of python/pytest in intgcheck
        0e1346b93  BUILD: Prefer python3 for intgcheck
        5dc86be06  intg: Install python3 dependencies for intgcheck on new distros
        d625308c9  pyhbac: Fix warning Wdiscarded-qualifiers
        0610618bb  test_pam_responder: Fix unicore error
        f10530b3d  SSSDConfig: Add minimal test for parse method
        be3588bd0  SSSDConfig: Fix SyntaxWarning "is not" with a literal
        bce896fe6  TESTS: Add minimal test for pysss encrypt
        618014f44  pysss: Fix DeprecationWarning PY_SSIZE_T_CLEAN
        a946d1341  pysss_murmur: Fix DeprecationWarning PY_SSIZE_T_CLEAN
        f3529bed3  test_pam_responder: Fix DeprecationWarning invalid escape sequence
        629416d8a  testlib: Fix SyntaxWarning "is" with a literal

    Michal Židek (2):
        4bc342276  Bumping the version to track the 2.2.2 development
        f52eadd33  Update the translations for the 2.2.2 release

    Pavel Březina (12):
        815957cd1  ad: remove subdomain that has been disabled through ad_enabled_domains from sysdb
        7a03e9989  sysdb: add sysdb_domain_set_enabled()
        6882bc5f5  ad: set enabled=false attribute for subdomains that no longer exists
        d278704d8  sysdb: read and interpret domain's enabled attribute
        c7e6530d6  sysdb: add sysdb_list_subdomains()
        d0bdaabbc  ad: remove all subdomains if only master domain is enabled
        b3c354218  ad: make ad_enabled_domains case insensitive
        8e1f6734a  ci: use python2 version of pytest
        498a230e5  ci: pep8 was renamed to pycodestyle in Fedora 31
        7129979bf  ci: remove left overs from previous rebase
        f9b589a47  sudo: do not update last usn value on rules refresh
        18611d70e  ifp: let cache_req parse input name so it can fallback to upn search

    Sumit Bose (5):
        e989620bd  pam: keep pin on the PAM stack for forward_pass
        6e759010a  pam: do not accept empty PIN
        945970088  pam: user PAM return codes where expected
        5dccf76af  pam: set PAM_USER properly with allow_missing_name
        e7b7edea4  Revert "SERVER: Receving SIGSEGV process on shutdown"

    Tomas Halman (3):
        f19f8e6b9  SERVER: Receving SIGSEGV process on shutdown
        7fcd0a70d  BE: Invalid oprator used in condition
        a9669683d  SERVER: Receving SIGSEGV process on shutdown
