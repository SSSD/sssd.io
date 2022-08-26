SSSD 2.7.3 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

*  All SSSD client libraries (nss, pam, etc) won't serialize requests anymore by
   default, i.e. requests from multiple threads can be executed in parallel. Old
   behavior (serialization) can be enabled by setting environment variable
   "SSS_LOCKFREE" to "NO".

Tickets Fixed
-------------

- `#6153 <https://github.com/SSSD/sssd/issues/6153>`__ - Provide user feedback when login fails due to blocked PIN
- `#6218 <https://github.com/SSSD/sssd/issues/6218>`__ - 2.7.2: build fails

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.7.2..2.7.3

    Alexey Tikhonov (8):
        abc2ae569  PAM P11: fixed mistype in a log message
        aec973314  PAM P11: fixed minor mem-leak
        f0609d82c  PAM: user feedback when login fails due to blocked PIN
        c7918bef5  CLIENT: use thread local storage for socket to avoid the need for a lock.
        455940d93  SSS_CLIENT: mem-cache: fixed missing error code
        ddcf9a06d  SSS_CLIENT: got rid of code duplication
        0a8a5b6c2  TESTS: test_memory_cache: execute NSS functions in teardown to force sss_client libs to realize mem-cache files were deleted
        ab749f02d  confdb: supress false positive warning: src/confdb/confdb.c:260:10: warning[-Wanalyzer-use-of-uninitialized-value]: use of uninitialized value 'secdn'

    Anuj Borah (2):
        a694a2064  Tests: Add automation for bz 2056035
        ff67197ae  Tests: sssd runs out of proxy child slots and doesn't clear the counter for Active requests

    Elena Mishina (1):
        3678f40b4  po: update translations

    Iker Pedrosa (3):
        42e4bbfff  CI: update python dependencies to version 3
        3bf58985a  CI: build debian without python 2 bindings
        289ff0ca2  Fix E226 reported by flake8

    Jakub Vavra (4):
        490b23bef  Tests: Fix/finish Sasl authid tests, minor tweak to hostname test.
        ae400d259  Fix some flake 8 violations
        0b0fdb667  Tests: Add a test for bz2026799 bz2070138
        17c60bb84  Tests: Extend test to cover bz2098615.

    Kemal Oktay Aktoğan (2):
        2b62330c0  po: update translations
        590ff9067  po: update translations

    Pavel Březina (9):
        5d39cd5c5  tests: fix pep8 issues
        b7893b9a5  ci: switch to debian-latest
        7f71eec46  ci: upload test-suite.log as an artifact
        7f30777ea  intgcheck: mark files provider tests as flaky
        446002b9a  sbus: ensure single new line at end of file
        440076ebb  sbus: apply changes in codegen
        1861d4342  pot: update translations
        acfec6130  pot: update translations
        160bbf488  Release sssd-2.7.2

    Piotr Drąg (1):
        e5902e1a4  po: update translations

    Shridhar Gadekar (3):
        8e2b83b52  Test: Minor trival testcase doc-string changes of rfc2307
        754bacec1  Tests: 2FA prompting setting
        a123419e0  Test: better default for IPA/AD re_expression

    Sumit Bose (1):
        0816b64c6  conf: make libjose and libcurl required for oidc_child

    Weblate (1):
        eb3b0fade  Update translation files

    Yuri Chornoivan (2):
        0239ad06c  po: update translations
        8136a60f4  Fix minor typo

    김인수 (2):
        3d16e7419  po: update translations
        fe79c4a0d  po: update translations
