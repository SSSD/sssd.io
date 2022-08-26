SSSD 2.7.4 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

*  * Lock-free client support will be only built if libc provides ``pthread_key_create()`` and ``pthread_once()``. For glibc this means version 2.34+

Tickets Fixed
-------------

* `#6298 <https://github.com/SSSD/sssd/issues/6298>`__ - sssctl analyze --logdir option requires sssd to be running
* `#6307 <https://github.com/SSSD/sssd/issues/6307>`__ - Incorrect request ID tracking from responder to backend

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.7.3..2.7.4

    Alejandro López (1):
        7f5adf718  Tests: Minor improvement to the Multihost RST files

    Alexey Tikhonov (5):
        03142f8de  CLIENT:MC: store context mutex outside of context as it should survive context destruction / re-initialization
        4e9e83210  Makefile: remove unneeded dependency
        0eae08620  CLIENT:MC: -1 is more appropriate initial value for fd
        d386e94ef  CLIENT:MC: pointer to the context mutex shouldn't be touched
        1b2e4760c  CLIENT: fix client fd leak

    Anuj Borah (3):
        d928192e0  Tests: avoid interlocking among threads that use `libsss_nss_idmap` API
        e56ca5402  Tests: Fix test_avoid_interlocking_among_threads
        173e67553  Tests: Fix test cases for signoff CI

    Jakub Vavra (16):
        0f0fd4d50  Tests: Add oddjob fixture to enable working homes in basic tests.
        863cfda6c  Tests: Update auth_from_client to allow both short and full user names.
        705f01ffb  Tests: remove python paramiko library from tests.
        26521890f  Tests: Remove SSHClient from ipa/conftest.py
        6dde7e62f  Tests: Remove paramiko/SSHClient from utils.py.
        c6c0186e1  Tests: Code review fixes for paramiko removal.
        4cc8d794a  Tests: Add pexpect to requirements.
        98dd014c3  Tests: Fix issue in the test test_0002_ad_parameters_junk_domain.
        38a2423dc  Tests: Rewrite autofs_ad_schema from direct ldap access to powershell.
        b2f5f373f  Tests: Modify sambaTools to lazy initialize ldap AD connection.
        576e15e39  Tests: Add a fixture add_etc_host_records for Testcifs to solve name resolution issue.
        b4eef0543  Tests: Re-implement reset_machine_password using powershell instead of direct ldap access.
        06c9230e8  Tests: Update failure message for nismap manipulation.
        4b82be81b  Tests: Fix rid computation for windows 2012.
        2328fc769  Tests: Extend info functions to handle line breaks.
        1da8c80be  Tests: Modify ad schema tests for compatibility with windows 2012.

    Justin Stephenson (7):
        f90205831  Analyzer: Fix escaping raw fstring
        49eb87184  CACHE_REQ: Fix hybrid lookup log spamming
        4a46d62cc  Fix new pycodestyle E275 requirement
        f8704cc24  SSSCTL: Allow analyzer to work without SSSD setup
        6c6b09692  CI: pycodestyle fixes evident on centos8 stream
        e6d450d4f  RESPONDER: Fix client ID tracking
        d22ea2df6  Analyzer: support parallel requests parsing

    Madhuri Upadhye (2):
        c90a1f61c  common: Install krb5-pkinit package
        6ac200c80  Tests: alltests/test_services.py: Port the failing test cases in pytest

    Pavel Březina (5):
        582e66c1c  tests: fix missing new line at the eof: src/tests/multihost/requirements.txt
        610b47110  ci: fix syntax error in copr build
        9ca7d6bab  ci: fix copr builds
        c8b2a764f  pot: update translations
        fd06791ee  Release sssd-2.7.4

    Steeve Goveas (2):
        1944b18c5  TEST: Modify test to compare backtrace for same error
        7985fc3ba  update the sequence number of tests

    Weblate (1):
        3abcd18d1  po: update translations
