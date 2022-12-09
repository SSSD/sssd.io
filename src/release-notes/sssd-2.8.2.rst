SSSD 2.8.2 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* SSSD can be configured not to perform a DNS search during DNS name resolution. This behavior is governed by the new dns_resolver_use_search_list. This parameter can be used in the domain section. Default value is true - that means that SSSD follows the system settings.
* ``--enable-files-domain`` configure option is deprecated and will be removed in one of the next versions of SSSD.
* ``sssctl analyze`` tool doesn't require anymore to be run under root.

New features
~~~~~~~~~~~~

* New mapping template for serial number, subject key id, SID, certificate hashes and DN components are added to ``libsss_certmap``.

Tickets Fixed
-------------

* `#5390 <https://github.com/SSSD/sssd/issues/5390>`__ - sssd failing to register dynamic DNS addresses against an AD server due to unnecessary DNS search
* `#6383 <https://github.com/SSSD/sssd/issues/6383>`__ - sssd is not waiting for network-online.target
* `#6403 <https://github.com/SSSD/sssd/issues/6403>`__ - Add new Active Directory related certificate mapping templates
* `#6404 <https://github.com/SSSD/sssd/issues/6404>`__ - [RFE] Add digest mapping feature from pam_pkcs11 in SSSD
* `#6451 <https://github.com/SSSD/sssd/issues/6451>`__ - UPN check cannot be disabled explicitly but requires krb5_validate = false' as a work-around
* `#6479 <https://github.com/SSSD/sssd/issues/6479>`__ - Smart Card auth does not work with p11_uri (with-smartcard-required)

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.8.1..2.8.2

    Alejandro López (1):
        98412a4ec  BACKEND: Reload resolv.conf after initialization

    Alexey Tikhonov (9):
        9258f0bec  UTILS: socket connect: added missing new line and adjusted log level to more appropriate
        2f8859890  UTILS: got rid of deprecated `inet_netof()` to please 'rpminspect'.
        541cd6772  TOOLS: don't export internal helpers
        bb97f89ab  TOOLS: fixed handling of init error
        581617c09  SSSCTL: don't require 'root' for "analyze" cmd
        cd1a94e58  SYSDB: pre-existence of MPG group in the cache isn't an error
        64c990553  Translations: add missing `tools/sssctl/sssctl_cert.c` and macros
        be569b0cb  Updated .pot/.po files
        f17bb003c  BUILD: deprecate `--enable-files-domain` build option

    Cole Robinson (1):
        ece943486  MAN: Fix option typo on sssd-kcm.8

    Dan Lavu (1):
        a8b6be403  Adding Ported DynDNS Testcases

    Elena Mishina (1):
        8290b0e7e  po: update translations

    Iker Pedrosa (1):
        77ef7b256  ci: fix codeql

    Jakub Vavra (6):
        8e82f3d47  Tests: Add a test for bz1964121 override homedir to lowercase
        44717b82b  Tests: Add the missing admisc pytest marker.
        564af88dd  Tests: Wait a bit before collection log in test_0015_ad_parameters_ad_hostname_machine.
        d2b5c789c  Tests: Fix E126 in test_adparameters_ported.py
        e3be45977  Tests: Update fixture using adcli to handle password from stdin.
        765fe3de6  Tests: Fix automount OU removal from AD.

    Justin Stephenson (3):
        7d0c70cc4  Analyzer: Ensure parsed id contains digit
        49b107175  SSSCTL: Add debug option to help message
        0253f7c3f  CI: Update core github actions

    Madhuri Upadhye (1):
        5b7a4b4fe  Tests: Minor fixes for alltests

    Pavel Březina (4):
        dc71321f7  ci: make /dev/shm writable
        8c4da4937  ci: install correct python development package
        37f934f27  pot: update pot files
        796b6daee  Release sssd-2.8.2

    Piotr Drąg (1):
        5bd2aa9b8  po: update translations

    Shridhar Gadekar (3):
        de1d4636c  Tests: gssapi ssh login minor fix
        25deb9e06  Tests: Use negative cache better for lookup by SIDs
        464c78beb  Test: gssapi test fix

    Steeve Goveas (1):
        a34b4f5e8  Tests: Cannot SSH with AD user to ipa-client with invalid keytab

    Sumit Bose (16):
        b00c72d29  PAC: allow to disable UPN check
        a3304cc6b  ipa: do not add guessed principal to the cache
        35a28524e  pac: relax default check
        cca0233ef  certmap: add support for serial number
        a2bca35c7  certamp: add support for subject key id
        47f3408e9  certmap: add support for SID extension
        8d8e3c7c6  certmap: fix for SAN URI
        6ad29f999  certmap: add bin_to_hex() helper function
        9a45e6162  sssctl: add cert-eval-rule sub-command
        3f336da42  certmap: add get_digest_list() and get_hash()
        8a6a874ba  certmap: dump new attributes in sss_cert_dump_content()
        698d56882  certmap: add LDAPU1 mapping rules
        17142068c  certmap: add tests for new attributes and LDAPU1 rules
        925d8a9f1  certmap: add LDAPU1 rules to man page
        12e39a456  certmap: Add documentation for some internal functions
        20037ae53  p11: fix size of argument array

    Temuri Doghonadze (1):
        f1dc6cdde  po: update translations

    Tomas Halman (1):
        99d46b2fa  RESOLV: Configuration option for DNS search

    Weblate (1):
        5d4f9dfd6  po: update translations

    Yuri Chornoivan (1):
        0909e8a15  po: update translations

    aborah-sudo (5):
        a3b30043d  Tests: Removing tests from gating pipe line
        10641ea1f  Tests: Removing tests from gating pipe line
        19fd96f1d  Tests: fix test_bz1368467
        65e944bd5  Tests: fix test_sssctl_local.py::Testsssctl::test_0002_bz1599207
        16c814ade  Tests: port proxy_provider/rfc2307bis

    김인수 (2):
        72eed0349  po: update translations
        0b4679616  po: update translations
