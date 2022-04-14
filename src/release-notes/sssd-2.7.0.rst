SSSD 2.7.0 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

* Added a new krb5 plugin ``idp`` and a new binary ``oidc_child`` which performs
  **OAuth2** authentication against FreeIPA. This, however, can not be tested
  yet because this feature is still under development on the FreeIPA server
  side. Nevertheless, we have decided to include this in the release in order to
  enable the functionality on the clients immediately when the FreeIPA project
  delivers this feature without the need to update the clients.

General information
~~~~~~~~~~~~~~~~~~~

* Better default for IPA/AD re_expression. Tunning for group names containing '@' is no longer needed.
* A warning is added in the logs if an LDAP operation needs more than 80% of the configured timeout.
* A new debug level is added to show statistical and performance data. Currently the duration of a backend request and of single LDAP operations are recorded if debug_level is set to 9 or the bit 0x20000 is set.
* Added support for anonymous PKINIT to get FAST credentials
* We have many warnings and errors from static analyzers

Important fixes
~~~~~~~~~~~~~~~

* SSSD now correctly falls back to UPN search if the user was not found even with `cache_first = true`.

Packaging changes
~~~~~~~~~~~~~~~~~

* Added new configure option ``--with-oidc-child`` and ``--without-oidc-child`` to control build of ``oidc_child`` (enabled by default).
* Added new package ``sssd-idp`` that contains the ``oidc_child`` and krb5 ``idp`` plugin, this package is required by ``sssd-ipa``.

Tickets Fixed
-------------

- `#3768 <https://github.com/SSSD/sssd/issues/3768>`__ - Add a memcache for SID-by-id lookups
- `#4138 <https://github.com/SSSD/sssd/issues/4138>`__ - SSSD cant parse GPO if AD server have Russain language
- `#4893 <https://github.com/SSSD/sssd/issues/4893>`__ - If parsing an entry fails, the whole back end goes offline
- `#5380 <https://github.com/SSSD/sssd/issues/5380>`__ - refactor confdb_get_domain_internal()
- `#5753 <https://github.com/SSSD/sssd/issues/5753>`__ - Restart=on-failure without a limit is holding boot forever
- `#5848 <https://github.com/SSSD/sssd/issues/5848>`__ - Consistency in defaults between OpenSSH and SSSD
- `#5961 <https://github.com/SSSD/sssd/issues/5961>`__ -  [RFE] Allow SSSD to use anonymous pkinit for FAST
- `#5967 <https://github.com/SSSD/sssd/issues/5967>`__ -  [RFE] Implement time logging for the LDAP queries and warning of high queries time
- `#5968 <https://github.com/SSSD/sssd/issues/5968>`__ - backtrace in responder for error "Could not get account info"
- `#5998 <https://github.com/SSSD/sssd/issues/5998>`__ - ``ldap_default_authtok_type = obfuscated_password`` option set in domain with ``id_provider = ad`` causes issues.
- `#6022 <https://github.com/SSSD/sssd/issues/6022>`__ - SSSD update prompts for smartcard pin twice
- `#6023 <https://github.com/SSSD/sssd/issues/6023>`__ - sssd does not enforce smartcard auth for kde screen locker
- `#6042 <https://github.com/SSSD/sssd/issues/6042>`__ - Add user and group version of sss_nss_getorigbyname()
- `#6055 <https://github.com/SSSD/sssd/issues/6055>`__ - Unable to lookup AD user if the AD group contains '@' symbol
- `#6059 <https://github.com/SSSD/sssd/issues/6059>`__ - Usage of ```cache_first = true``` seems to break "User by UPN" plugin
- `#6063 <https://github.com/SSSD/sssd/issues/6063>`__ - Use right sdap_domain in ad_domain_info_send
- `#6081 <https://github.com/SSSD/sssd/issues/6081>`__ - 2FA prompting setting ineffective
- `#6088 <https://github.com/SSSD/sssd/issues/6088>`__ - idp preauth: handle multiple State messages from ipa-otpd
- `#6107 <https://github.com/SSSD/sssd/issues/6107>`__ - SSSD fails to start if 'sssd user' isn't resolvable by ``libnss_files.so``

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.6.3..2.7.0

    Alejandro López (3):
        5cf46fc8c  COMMIT TEMPLATE: Fixed two typos
        8a9458df7  confdb: refactor confdb_get_domain_internal()
        a049ac715  systemd: only relaunch after crashes and do not retry forever

    Alexander Bokovoy (1):
        63e6365cb  krb5: switch to Proxy-State in idp plugin reply

    Alexey Sheplyakov (1):
        81d67a592  ad: gpo: ignore GPO if SecEdit/GptTmpl.inf is missing

    Alexey Tikhonov (24):
        2054f9908  TESTS: fixed use-after-free
        c2e2036ae  UTILS: removed unused file helpers
        7f6c2755e  debug: suppress backtrace for backend errors
        fa47bd1dd  CACHE_REQ: removed unused code
        5f9445432  SIMPLE: reduce severity level of debug message in case primary group is missing in the domain cache
        5cdb7e2c4  Test: fix wrong messages
        25faf9839  AD/IPA: ignore 'ldap_default_authtok_type' conf setting
        f1573e51c  UTILS: reduce debug level in case well_known_sid_to_name() fails
        b963aa3c7  SDAP: sdap_nested_group_hash_insert(): don't create key copy - hash_enter() takes care of this.
        d241b5529  GPO: ignore non-ascii symbols in values in GPT.INI
        60c30a3fd  UTILS: fixes CWE-394
        37f900577  Revert "usertools: force local user for sssd process user"
        3c6218aa9  Revert "man: sssd.conf and sssd-ifp clarify user option"
        720c39a13  SID mem-cache: config, init, man page
        2a160adb0  mem-cache: fix error in the comment
        d5e4753ef  SID mem-cache: data structure and store function
        f869c6947  NSS: SID: debug message in case of collision: - fixed mistype (users -> groups) - added SIDs of colliding entries
        a87dfd624  NSS: SID: reduced code duplication
        25426f6a5  NSS: mem-cache: const correctness
        aec620f62  NSS: SID: store results in mem-cache
        483d26e9f  SSS_CLIENT: sss_get_ex() should be static
        24770866f  SSS_CLIENT: NSS: SID: mem-cache support for sid-by-id and id-by-sid lookups
        8cee413b7  NSS: SID: don't try to deduce object type based on request type
        b2be59f1d  SSS_CLIENT: NSS: SID: improved sss_nss_mc_get_sid_by_id()

    Anuj Borah (7):
        c0f767c55  Tests: Fix test_pass_krb5cname_to_pam test
        7f4e04ba3  Tests: Port the old ns_account_lock.sh script to pytest
        bf9deea19  Tests: Add 389-ds package to client machine
        556f42e10  Tests: Regressions 8.5 - alltests-tier3
        aa054c223  Tests: Install nss-pam-ldapd package for alltests-tier2
        d1bce130f  Tests: Porting of proxy provider test suits to pytest
        a84797cb0  Tests: Fix FileNotFoundError for environment_setup

    Dhairya Parmar (1):
        d082681a0  TEST: Current value of ssh_hash_known_hosts causes error in the default configuration in FIPS mode

    Iker Pedrosa (46):
        121576a45  util: fix rawhide compilation problem
        27e2a0f44  CI: enable CodeQL analysis
        bcfb1cb15  CI: split dependencies for Ubuntu
        d53bb2be4  sbus: Multiplication result converted to larger type
        923c94b43  Duplicate include guard
        5ea0c927c  Array offset used before range check
        949768190  Potentially uninitialized local variable
        c30356d07  Inconsistent nullness check
        f36deb3e3  tests: Remove unused format_interactive_conf()
        dd5f23383  tests: Remove unused gethostbyaddr_r()
        90ad1ea46  tests: Unreachable code
        9bd821b6f  Comparison result is always the same
        b9783436d  ad: Empty branch of conditional
        36920a04c  Commented-out code
        f04ca9b29  Implicit string concatenation in a list
        439b9fc65  CI: change pycodestyle max line length
        bab44e928  Tests: fix missing name (F821)
        94e5466e6  Tests: fix indentation(E12*) and whitespace(E20*)
        b3244e39d  Tests: fix missing whitespace after ',' (E231)
        e81f89916  Tests: fix unexpected spaces around '/' (E251)
        5be30ac0c  Tests: remove 12 years old TODOs
        6bbfd1b6c  Tests: fix ambiguous variable (E741)
        58605202b  Tests: fix shadowed variable (F402)
        fe46bd3bd  Tests: fix f-strings usage (F541)
        56b375200  Tests: fix comparison symbols (F632)
        899a7df9b  Tests: fix indentation issues (E111 and E117)
        294debcd1  Tests: fix end semicolon (E703)
        0534fd3e9  Tests: fix incorrect comparison with "==" (E711)
        089123bd9  Tests: fix bare 'except' (E722)
        d377d1daf  Tests: fix continuation line under-indented (E128)
        2f742fc95  Tests: fix star imports (F403 and F405)
        634c91b0f  Tests: fix imported but unused modules (F401)
        8cdfd3d29  Tests: fix blank lines (E302 and E303)
        4f303da4b  Tests: fix blank line at end of file (W391)
        838669d9c  Tests: fix line too long (E501)
        3f8493f94  Tests: fix missing name (F821)
        c71d83b86  Tests: fix missing whitespace after ',' (E231)
        b8f4c1710  Tests: block comment should start with '# ' (E265)
        ad1f64e4e  Tests: fix unused variable (F841)
        fd19512a5  ccpcheck: fix issues
        1abda8381  CI: enable cppcheck analysis
        67b129235  CI: enable flake8 analysis
        3c39d007e  Tests: remove unused module (F401)
        73bd21b37  SSSDConfig: fix indentation for bracket (E124)
        30831cc3b  GDB: rename duplicated function (F811)
        42d3e28ce  CI: disable result comment for cppcheck

    Jakub Vavra (9):
        23286d27e  Tests: Update/fix AD parameters tests ported from bash
        7e41098e5  Tests: Add a test for bz1859315 - sssd does not use kerberos port that is set.
        10a14594c  Tests: [SSSD-3579]: Update test_0018_bz1734040 for RHEL 9.
        bd6f6671f  Tests: Use lazy initialization for ad_conn property of AD.
        eb85382c9  Tests: Update ADOperations methods to use powershell.
        6845db5ad  Tests: Add sleep before collecting logs in flaky ad parameters tests.
        2ec518724  Tests: Update KeytabRotation tests in AD tier 2
        81936d436  Tests: Reduce sleeps before collecting logs in AD parameters tests.
        63ab01f38  Tests: Port ad-schema test suite from bash.

    Jean-Baptiste Denis (1):
        91e8c4fb1  Increase listen backlog

    Justin Stephenson (11):
        c41cc16ca  CI: Remove unused travis CI related files
        616e69f6c  make_srpm: Add option to specify package version
        21a91ce21  CI: Add internal covscan workflow to Jenkins
        0a9c00c37  Add external covscan workflow
        961e320d3  CI: Update apt cache
        abc41d0b0  CONTRIB: Switch distro.sh to use /etc/os-release
        59484ef04  CONTRIB: Add shadow and unused-variable to SSS_WARNINGS
        098c3fcf6  CONTRIB: Update rpm-spec-builddeps to python3 shebang
        a0f454aa0  CONTRIB: Add install dependencies option to contrib/ci/run
        94254dd7a  CI: Install dependencies with contrib/ci/run
        81450b9a4  CI: Add warnings enabled build and make check

    Madhuri Upadhye (1):
        6d105980a  Tests: ipa: Minor fix while add users in groups in windows bash shell script.

    Pavel Březina (40):
        ad8f0d350  BUILD.txt: fix invalid link
        6df690524  ci: move languages parameter to codeql init
        b21542987  ci: build pull requests in copr
        0d7ae85f3  sifp: fix coverity issue
        709e9cc9a  authtok: add SSS_AUTHTOK_TYPE_OAUTH2
        292bde667  pam: add new SSS_CHILD_KEEP_ALIVE pam item
        7d688556b  pam: add new SSS_PAM_OAUTH2_INFO pam item
        8ca8fcf01  conf: add libjansson dependency
        673149420  make: define RUNDIR
        68a8a2d71  krb5: add idp preauth plugins
        3a2add67f  krb5: support to exchange multiple messages with the same child
        5f9e5c2e0  krb5: terminate child if it fails to setup
        689bb4f8b  krb5: exchange messages with krb5_child with exact length
        dcd7133e1  krb5: add support for idp:oauth2 responder question
        8cba6b4b4  krb5: fix memory hierarchy in krb5_child unpack_buffer()
        95495e7b4  krb5: add keep alive timeout for krb5_child
        918d493c3  pam: add oauth2 url+pin prompt
        74ef76b88  ci: avoid concurrent runs
        e8b22f2d6  ci: allow to run coverity scan on demand
        71cd2822c  cache_req: fallback to UPN even with cache_first = true
        8b95efa2d  intg: do not run valgrind on infopipe tests
        ee752f8e2  intg: make kcm renewal test user independent
        52e53926c  ci: make sure that $USER is available
        5def61fb9  ci: disable mock build in contrib/ci/run
        df44fc203  ci: make intgcheck work on CentOS Stream and RHEL 9
        4ea511c65  ci: include acl package in basic multihost tests
        562a4507b  ci: run intgcheck and multihost tests
        22bbb7a04  ci: fix concurrency group for copr
        6a51ffee3  ci: add working-directory to build-sssd-srpm
        4396cd4be  ci: integrate covscan into github actions
        872bbbcc3  ci: fix concurrency group in analyze-target workflow
        0fbabd4a1  ci: switch to next-actions
        c321fa5f3  ci: switch to next-actions/print-logs
        f853a8683  krb5: switch to Proxy-State in idp plugin
        74cb09ea2  krb5: idp method is only supported if FAST channel is available
        2980f1144  ci: use correct checkout path for covscan
        0c568e94d  ci: disable fedora-review for copr pr builds
        66f60aada  contrib: add sssd public key
        f9901d5ad  pot: update pot files
        f48eddc3b  Release sssd-2.7.0

    Samuel Cabrero (4):
        b67caf27b  Tests: Use group1_dom1-19661 in test_pysss_nss_idmap.py
        941418f43  SDAP: Add 'ldap_ignore_unreadable_references' parameter
        5c7fb41f3  SDAP: Honor ldap_ignore_unreadable_references parameter
        57d6af2f2  Tests: Add a test for the ldap_ignore_unreadable_references parameter

    Shridhar Gadekar (2):
        95b17d156  Tests: sssctl analyze capture tevent chain ID logic in logs
        38636ffaf  minor change in testcase description

    Steeve Goveas (4):
        0eb8564c3  Tests: Add tests for poor man's backtrace
        1b24149ee  TEST: Enable files domain, fix flake8 issues, improve test code
        6edbb6cdd  Tests: prefix 'session_' to avoid failure
        e538db29b  Tests: CRB repo name has changed in IDM CI

    Sumit Bose (26):
        fa2d7a492  TEST: fix long line pep8 error
        d1ad68fab  krb5_child: move FAST TGT request into a function
        58ab4137c  krb5_child: add fast-use-anonymous-pkinit option
        7e839befe  krb5: add krb5_fast_use_anonymous_pkinit option
        775150b58  debug: add new dubug level SSSDBG_PERF_STAT
        2fb5cbfa6  util: add time measurement helpers
        3b7955306  sdap: record time needed for a sdap operation
        3063a73c0  dp: adding log message with spend time
        23e64beee  sdap: split out function to get the server IP as string
        5dc34b753  sdap_op: add strings member for extra statistical information
        a9b4ae62a  ldap: add info string for statistics
        e2082c03a  ipa: add info string for statistics
        b3646c663  sdap: warn if request needs 80% of timeout
        15f66efcc  sdap: make struct sdap_op private
        5494f7ffe  sdap: add sdap_get_server_ip_str_safe()
        9c5632dfa  nss: add sss_nss_getorigbyusername and sss_nss_getorigbygroupname
        027e89b44  test: suppress memory leak in _dl_find_object_update
        3baf161eb  integration tests: switch OpenLDAP from hdb to mdb
        51e922971  ad: use right sdap_domain in ad_domain_info_send
        d8d25758a  pam: fix section parsing issue
        34829d3bc  tests: add utilities for cmocka based unit tests
        5c5a6b89e  tests: allow to run single pam-srv-tests tests
        731b3e668  pam: add more checks for require_cert_auth
        4d2277f8c  pam: better SC fallback message
        878737c8e  oidc_child: add initial implementation of oidc_child
        cc811edf5  oidc_child: make build configurable

    Tomas Halman (5):
        00940cd1b  systemtap: Hard-coded path instead of @libdir@
        3935e89c1  ci: discard old builds
        0c0705e30  usertools: better default for IPA/AD re_expression
        c159f5299  usertools: move default re_expression definition
        dde276e25  TESTS: New tests for IPA/AD re_expression default

    Weblate (1):
        e09ac40a2  po: update translations
