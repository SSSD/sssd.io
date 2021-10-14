SSSD 2.6.0 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* Support of legacy json format for ccaches was dropped
* Support of long time deprecated ``secrets`` responder was dropped.
* Support of long time deprecated ``local`` provider was dropped.
* This release drops support of ``--with-unicode-lib`` configure option. ``libunistring`` will be used unconditionally for Unicode processing.
* This release removes pcre1 support. pcre2 is used unconditionally.
* p11_child does not stop at the first empty slot when searching for tokens
* A flaw was found in SSSD, where the sssctl command was vulnerable to shell command injection via the logs-fetch and cache-expire subcommands. This flaw allows an attacker to trick the root user into running a specially crafted sssctl command, such as via sudo, to gain root access. The highest threat from this vulnerability is to confidentiality, integrity, as well as system availability. This patch fixes a flaw by replacing ``system()`` with ``execvp()``.

New features
~~~~~~~~~~~~

* Basic support of user's 'subuid and subgid ranges' for IPA provider and corresponding plugin for shadow-utils were introduced. Limitations: - single subid interval pair (subuid+subgid) per user - idviews aren't supported - only forward lookup (user -> subid ranges) Take a note, this is MVP of experimental feature. Significant changes might be required later, after initial feedback. Corresponding support in shadow-utils was merged upstream, but since there is no upstream release available yet, SSSD feature isn't built by default. Build can be enabled with ``--with-subid`` configure option. Plugin's install path can be configured with ``--with-subid-lib-path=`` (``${libdir}`` by default)

Important fixes
~~~~~~~~~~~~~~~

* KCM now replace the old credential with new one when storing an updated credential that is however already present in the ccache to avoid unnecessary growth of the ccache.
* Improve mpg search filter to be more reliable with id-overrides and the new auto_private_groups options.
* Even if the forest root is disabled for lookups all required internal data is initialized to be able to refresh the list of trusted domains in the forest from a DC of the forest root.
* ccache files are created with the right ownership during offline Smartcard authentication
* AD ping is now sent over ``ldap`` if ``cldap`` support is not available during build. This helps to build SSSD on distributions without ``cldap`` support in ``libldap``.
* CVE-2021-3621

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* New IPA provider's option ``ipa_subid_ranges_search_base`` allows configuration of search base for user's subid ranges. Default: ``cn=subids,%basedn``

Tickets Fixed
-------------

- `#2739 <https://github.com/SSSD/sssd/issues/2739>`_ - sssd: incorrect checks on length values during packet decoding
- `#4904 <https://github.com/SSSD/sssd/issues/4904>`_ - sss_cache prints spurious error messages when invoked from shadow-utils on package install
- `#5121 <https://github.com/SSSD/sssd/issues/5121>`_ - timestamp cache entries are not created if missing
- `#5197 <https://github.com/SSSD/sssd/issues/5197>`_ - Support subid resources in ipa provider
- `#5482 <https://github.com/SSSD/sssd/issues/5482>`_ - Add support to verify authentication indicators in pam_sss_gss
- `#5514 <https://github.com/SSSD/sssd/issues/5514>`_ - [RFE] SSSD logs improvements: clarify which config option applies to each timeout in the logs
- `#5596 <https://github.com/SSSD/sssd/issues/5596>`_ - sss_cache: reset originalModifyTimestamp in timestamp cache as well
- `#5720 <https://github.com/SSSD/sssd/issues/5720>`_ - SSSD requirement for CLDAP support in libldap should be optional
- `#5729 <https://github.com/SSSD/sssd/issues/5729>`_ - kcm fails to start if /var/lib/sss/db is empty
- `#5744 <https://github.com/SSSD/sssd/issues/5744>`_ - Lookup with fully-qualified name does not work with 'cache_first = True'
- `#5767 <https://github.com/SSSD/sssd/issues/5767>`_ - Drop support of glib2 for Unicode processing
- `#5768 <https://github.com/SSSD/sssd/issues/5768>`_ - Drop support of obsolete PCRE1
- `#5770 <https://github.com/SSSD/sssd/issues/5770>`_ - disabled root ad domain causes subdomains to be marked offline
- `#5775 <https://github.com/SSSD/sssd/issues/5775>`_ - kcm: replace old credentials when storing a new one
- `#5785 <https://github.com/SSSD/sssd/issues/5785>`_ - SSSD 2.4.1 - krb5_child creates ccache file owned by root when in offline mode
- `#5790 <https://github.com/SSSD/sssd/issues/5790>`_ - IPA clients fail to resolve override group names.
- `#5824 <https://github.com/SSSD/sssd/issues/5824>`_ - SSSD should use "hidden" temporary file in its krb locator

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.5.2..2.6.0

    Alexey Tikhonov (17):
        f54608822  Basics of 'subid ranges' support for IPA provider.
        365cd676c  NSS: don't treat absent 'CLEAR_MC_FLAG' as an error (This is expected in case of SIGHUP sent for log rotation.)
        7ab83f97e  TOOLS: replace system() with execvp() to avoid execution of user supplied command
        bd2ccbf69  file utils: reduce log level in remove_tree_with_ctx() Users of this function are responsible to decide if fail is critical.
        c037432c3  BUILD: get rid of PCRE support
        6acb1d635  UNICODE: drop support of glib2 for Unicode processing
        3e94b64da  Got rid of 'local' provider.
        c4c0fd690  CONF: removed unused 'sbus_timeout' option
        10069b1d3  Got rid of 'secrets' responder and it's support in KCM
        5bb5380cb  libsecrets was disbanded and merged into KCM responder as this is the only its user now.
        9466aa4d9  KCM: secrets db: got rid of legacy json format support
        f5431c3a7  KCM: secrets db: got rid of legacy encrypted payload format
        dfb97f071  crypto: removed sss_encrypt()/sss_decrypt() helpers as those aren't used anymore.
        29f8a795f  TESTS: avoid cross-test tainting of os.environ
        1e64a762f  KCM: secdb: treat secdb_get_cc() == ENOENT the same way as corresponding key_by_*() == ENOENT (mostly)
        03f6ef367  krb5_child: fixed incorrect checks on length value
        01ff8155b  MONITOR: reduce logs severity around signalling and termination of services to avoid useless in those cases backtraces

    Anuj Borah (12):
        b6fe76e7e  Tests: SSSD is generating lot of LDAP queries in a very large environment Issue: https://github.com/SSSD/sssd/issues/5121 Bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=1772513
        9b24b8db2  Tests: Add support to verify authentication indicators in pam_sss_gss
        85723a7b8  Tests: fix sss_cache to also reset cached timestamp
        a67d3bc80  Test: Fix RHEL9.0 Regression - alltests-tier1
        bd422ccdf  Tests: Suppress log message
        c3a8aad2b  Tests: RHEL9.0 Regression - alltests-tier1_2
        aab4fe9cf  Tests: SSSD logs improvements: clarify which config option applies to each timeout in the logs
        10d33986c  Tests: Fix RHEL8.5 failures for IDM-CI
        b22f6195c  Tests: sss_cache prints spurious error messages
        9121fbf9d  Tests: Remove shadow-utils test cases from sssd repo
        51eaed9d0  Tests: Fix Failure of sssctl_local test
        8e22258c1  Tests: support subid ranges managed by FreeIPA

    Assaf Morami (1):
        b9f8c2f99  p11_child: do_card partially fix loop exit condition when searching for token

    David Ward (5):
        a9218fbe0  p11_child: Restore functionality of --wait_for_card
        f3aa4b47a  p11_child: Ensure OpenSSL cleanup is performed
        3f1d03fc6  p11_child: Handle failure from p11_kit_uri_new()
        f5a9d8141  p11_child: Return updated CK_SLOT_INFO from wait_for_card()
        a036fc871  p11_child: Fix printing of non-null-terminated strings in do_card()

    Jakub Jelen (1):
        dab4448de  p11_child: Add missing newline after log message

    Jakub Vavra (2):
        ccebfc9cf  Tests: Add test_nss_get_by_name_with_private_group.
        a5716cd74  Tests: Add AD Parameters tests ported from bash.

    Justin Stephenson (10):
        1dae17bf9  TESTS: Make test_kcm_renewals idempotent
        d41e956c6  MONITOR: Return success from genconf with no config
        9f58bef3e  CI: unset DEBUGINFOD_URLS
        4b7b6fa70  KCM: Add krb5-libs dependency in spec
        fd3e397cf  KCM: Remove unneeded allocation
        3d8dd1282  debug: Add chain ID support for journald logger
        3343b5a81  DP: Log offline warning for REQ_TRACE tracking
        26086212a  Responder: Log client uid that started a request
        82e051e1f  TOOLS: Add sss_analyze utility
        097feb329  SSSCTL: Add analyze command

    Mantas Mikulėnas (1):
        1a1e914b9  NSS client: avoid using NETDB_INTERNAL if daemon is not available

    Massimiliano Torromeo (1):
        57247096b  TEST: Use absolute path for the MODPATH assertions in python tests

    Pavel Březina (12):
        a2fc3a3ad  Update version in version.m4 to track the next release
        a1f7035b3  remove deprecated talloc_autofree_context()
        575e1899e  fix warnings around sss_getenv()
        9e47b63e4  configure: do not unset PYTHON_PREFIX and PYTHON_EXEC_PREFIX
        b606eb62c  spec: fix invalid condition
        dfb6594e3  ad: fallback to ldap if cldap is not available in libldap
        aca2e08ba  krb5: remove unused mem_ctx from get_krb5_data_from_cred()
        55c5de2d5  kcm: replace existing credentials to avoid unnecessary ccache growth
        770c7ce9c  debug: fix unused variable warnings
        bb6d9d9cf  monitor: fix unused variable warning
        11c7f6a65  pot: update pot files
        bd71ae53f  Release sssd-2.6.0

    Paweł Poławski (2):
        44525a999  General: Hardeninig getenv() usage
        c1dd12114  general: Fix compilation warnings

    Sergio Durigan Junior (1):
        efd155f0a  Improve assertion when verifying paths for Python modules

    Shridhar Gadekar (2):
        818e4f925  Tests: Randomize sudo refresh timeouts
        e0d85ab68  Tests: improve sssd refresh timers for sudo queries

    Steeve Goveas (3):
        6f1188a06  TEST: Add id and fix indentation in docstrings
        1d4095fbb  TEST: usermod -d needs absolute path
        f0925489a  Tests: Add firewalld package install on clients

    Sumit Bose (9):
        cdc75c539  tests: do not use libcheck include file in cmocka tests
        7fdff741a  test: replace deprecated libcheck macros
        26654d3e5  cache_req: cache_first fix for fully-qualified names
        ef6aa9e44  krb5: fix ccache ownership for offline Smartcard authentication
        e92988a62  debug: reduce logging of GetAccountDomain() in the frontends
        ca8b655fb  debug: suppress backtrace for backend errors
        2a617c0ef  sdap: always create sdap object for a forest root
        4be5fcd9a  sysdb: more specific mpg search filter
        794127106  krb5: use hidden file when creating config snippets

    Timotej Lazar (1):
        8ed53d284  Include sys/types.h in debug.h

    Weblate (3):
        861e226b5  po: update translations
        e8055b8a2  po: update translations
        629f149eb  po: update translations

    Yuri Chornoivan (1):
        3e7aa1071  Fix minor typo: indicated -> indicate
