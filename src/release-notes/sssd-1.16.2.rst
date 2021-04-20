SSSD 1.16.2 Release Notes
=========================

Highlights
----------

New Features
~~~~~~~~~~~~

-  The smart card authentication, or in more general certificate authentication code now supports OpenSSL in addition to previously supported NSS (#3489). In addition, the SSH responder can now return public SSH keys derived from the public keys stored in a X.509 certificate. Please refer to the ``ssh_use_certificate_keys`` option in the man pages.
-  The files provider now supports mirroring multiple passwd or group files. This enhancement can be used to use the SSSD files provider instead of the nss_altfiles module

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  A memory handling issue in the ``nss_ex`` interface was fixed. This bug would manifest in IPA environments with a trusted AD domain as a crash of the ns-slapd process, because a ``ns-slapd`` plugin loads the ``nss_ex`` interface (#3715)
-  Several fixes for the KCM deamon were merged (see #3687, #3671, #3633)
-  The ``ad_site`` override is now honored in GPO code as well (#3646)
-  Several potential crashes in the NSS responder's netgroup code were fixed (#3679, #3731)
-  A potential crash in the autofs responder's code was fixed (#3752)
-  The LDAP provider now supports group renaming (#2653)
-  The GPO access control code no longer returns an error if one of the relevant GPO rules contained no SIDs at all (#3680)
-  A memory leak in the IPA provider related to resolving external AD groups was fixed (#3719)
-  Setups that used multiple domains where one of the domains had its ID space limited using the ``min_id/max_id`` options did not resolve requests by ID properly (#3728)
-  Overriding IDs or names did not work correctly when the domain resolution order was set as well (#3595)
-  A version mismatch between certain newer Samba versions (e.g. those shipped in RHEL-7.5) and the Winbind interface provided by SSSD was fixed. To further prevent issues like this in the future, the correct interface is now detected at build time (#3741)
-  The files provider no longer returns a qualified name in case domain resolution order is used (#3743)
-  A race condition between evaluating IPA group memberships and AD group memberships in setups with IPA-AD trusts that would have manifested as randomly losing IPA group memberships assigned to an AD user was fixed (#3744)
-  Setting an SELinux login label was broken in setups where the domain resolution order was used (#3740)
-  SSSD start up issue on systems that use the libldb library with version 1.4.0 or newer was fixed.

Packaging Changes
-----------------

-  Several new build requirements were added in order to support the OpenSSL certificate authentication

Documentation Changes
---------------------

-  The files provider gained two new configuration options ``passwd_files`` and ``group_files.`` These can be used to specify the additional files to mirror.
-  A new ``ssh_use_certificate_keys`` option toggles whether the SSH responder would return public SSH keys derived from X.509 certificates.
-  The ``local_negative_timeout`` option is now enabled by default. This means that if SSSD fails to find a user in the configured domains, but is then able to find the user with an NSS call such as getpwnam, it would negatively cache the request for the duration of the local_negative_timeout option.

Tickets Fixed
-------------

-  `#4758 <https://github.com/SSSD/sssd/issues/4758>`_ - /usr/libexec/sssd/sssd_autofs SIGABRT crash daily due to a double free
-  `#4756 <https://github.com/SSSD/sssd/issues/4756>`_ - [RFE] sssd.conf should mention the FILES provider as valid config value for the 'id_provider'
-  `#4755 <https://github.com/SSSD/sssd/issues/4755>`_ - home dir disappear in sssd cache on the IPA master for AD users
-  `#4752 <https://github.com/SSSD/sssd/issues/4752>`_ - Race condition between concurrent initgroups requests can cause one of them to return incomplete information
-  `#4751 <https://github.com/SSSD/sssd/issues/4751>`_ - Weirdness when using files provider and domain resolution order
-  `#4750 <https://github.com/SSSD/sssd/issues/4750>`_ - Change of: User may not run sudo --> a password is required
-  `#4749 <https://github.com/SSSD/sssd/issues/4749>`_ - Samba can not register sss idmap module because it's using an outdated SMB_IDMAP_INTERFACE_VERSION
-  `#4748 <https://github.com/SSSD/sssd/issues/4748>`_ - Utilizing domain_resolution_order in sssd.conf breaks SELinux user map
-  `#4741 <https://github.com/SSSD/sssd/issues/4741>`_ - sssd fails to download known_hosts from freeipa
-  `#4737 <https://github.com/SSSD/sssd/issues/4737>`_ - Request by ID outside the min_id/max_id limit of a first domain does not reach the second domain
-  `#4735 <https://github.com/SSSD/sssd/issues/4735>`_ - SSSD with ID provider 'ad' should give a warning in case the ldap schema is manually changed to something different than 'ad'.
-  `#4734 <https://github.com/SSSD/sssd/issues/4734>`_ - sssd not honoring dyndns_server if the DNS update process is terminated with a signal
-  `#4729 <https://github.com/SSSD/sssd/issues/4729>`_ - The SSSD IPA provider allocates information about external groups on a long lived memory context, causing memory growth of the sssd_be process
-  `#4725 <https://github.com/SSSD/sssd/issues/4725>`_ - ipa 389-ds-base crash in krb5-libs - k5_copy_etypes list out of bound?
-  `#4720 <https://github.com/SSSD/sssd/issues/4720>`_ - Hide debug message domain not found for well known sid
-  `#4711 <https://github.com/SSSD/sssd/issues/4711>`_ - externalUser sudo attribute must be fully-qualified
-  `#4703 <https://github.com/SSSD/sssd/issues/4703>`_ - A group is not updated if its member is removed with the cleanup task, but the group does not change
-  `#4699 <https://github.com/SSSD/sssd/issues/4699>`_ - GPO: SSSD fails to process GPOs If a rule is defined, but contains no SIDs
-  `#4698 <https://github.com/SSSD/sssd/issues/4698>`_ - Make nss netgroup requests more robust
-  `#4693 <https://github.com/SSSD/sssd/issues/4693>`_ - The tcurl module logs the payload
-  `#4690 <https://github.com/SSSD/sssd/issues/4690>`_ - KCM: Payload buffer is too small
-  `#4686 <https://github.com/SSSD/sssd/issues/4686>`_ - Fix usage of str.decode() in our tests
-  `#4684 <https://github.com/SSSD/sssd/issues/4684>`_ - LOGS: Improve debugging in case the PAM service is not mapped to any GPO rule
-  `#4680 <https://github.com/SSSD/sssd/issues/4680>`_ - confdb_expand_app_domains() always fails
-  `#4678 <https://github.com/SSSD/sssd/issues/4678>`_ - Application domain is not interpreted correctly
-  `#4676 <https://github.com/SSSD/sssd/issues/4676>`_ - PyErr_NewExceptionWithDoc configure check should not use cached results for different python versions
-  `#4666 <https://github.com/SSSD/sssd/issues/4666>`_ - SSSD's GPO code ignores ad_site option
-  `#4665 <https://github.com/SSSD/sssd/issues/4665>`_ - sss_groupshow no longer labels MPG groups
-  `#4655 <https://github.com/SSSD/sssd/issues/4655>`_ - sssctl COMMAND --help fails if sssd is not configured
-  `#4654 <https://github.com/SSSD/sssd/issues/4654>`_ - Reset the last_request_time when any activity happens on Secrets and KCM responders
-  `#4650 <https://github.com/SSSD/sssd/issues/4650>`_ - Implement sss_nss_getsidbyuid and sss_nss_etsidbygid for situations where customers define UID == GID
-  `#4640 <https://github.com/SSSD/sssd/issues/4640>`_ - Enable local_negative_timeout by default
-  `#4628 <https://github.com/SSSD/sssd/issues/4628>`_ - Fix pep8 issues on our python files.
-  `#4618 <https://github.com/SSSD/sssd/issues/4618>`_ - ID override GID from Default Trust View is not properly resolved in case domain resolution order is set
-  `#4583 <https://github.com/SSSD/sssd/issues/4583>`_ - sudo: report error when two rules share cn
-  `#4576 <https://github.com/SSSD/sssd/issues/4576>`_ - refresh_expired_interval does not work with netgrous in 1.15
-  `#4546 <https://github.com/SSSD/sssd/issues/4546>`_ - Files provider supports only BE_FILTER_ENUM
-  `#4495 <https://github.com/SSSD/sssd/issues/4495>`_ - extend sss-certmap man page regarding priority processing
-  `#4463 <https://github.com/SSSD/sssd/issues/4463>`_ - Certificates used in unit tests have limited lifetime
-  `#4429 <https://github.com/SSSD/sssd/issues/4429>`_ - Support alternative sources for the files provider
-  `#4366 <https://github.com/SSSD/sssd/issues/4366>`_ - GPO retrieval doesn't work if SMB1 is disabled
-  `#3694 <https://github.com/SSSD/sssd/issues/3694>`_ - Group renaming issue when "id_provider = ldap" is set.


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_16_1..sssd-1_16_2

    Fabiano Fidêncio (77):
        16fe3a349  TESTS: Fix E501 pep8 issues on test_ldap.py
        b4d72adc1  TESTS: Fix E20[12] pep8 issues on python-test.py
        018fe983c  TESTS: Fix E501 pep8 issues on python-test.py
        3fac321c1  TESTS: Fix E251 pep8 issues on python-test.py
        71dc7aa5c  TESTS: Fix E231 pep8 issues on python-test.py
        01e7730da  TESTS: Fix E265 pep8 issues on python-test.py
        e3f0de237  TESTS: Fix E128 pep8 issues on python-test.py
        5e86d31f9  TESTS: Fix E302 pep8 issues on python-test.py
        0e16e020b  TESTS: Fix W391 pep8 issues on python-test.py
        4593a2f12  TESTS: Fix E228 pep8 issues on python-test.py
        8b53952cb  TESTS: Fix E261 pep8 issues on python-test.py
        629563edc  TESTS: Fix E701 pep8 issues on python-test.py
        f64f99dd5  TESTS: Fix E305 pep8 issues on python-test.py
        7b9c3e69e  TESTS: Fix E20[12] pep8 issues on pysss_murmur-test.py
        9dc4c1555  TESTS: Fix E211 pep8 issues on pysss_murmur-test.py
        8e00bbcab  TESTS: Fix E20[12] pep8 issues on pyhbac-test.py
        235917c17  TESTS: Fix E261 pep8 issues on pyhbac-test.py
        87fe92e90  TESTS: Fix W391 pep8 issues on pyhbac-test.py
        25e0e4b09  TESTS: Fix E501 pep8 issues on pyhbac-test.py
        01012f0d7  TESTS: Fix E302 pep8 issues on pyhbac-test.py
        00f267a32  TESTS: Fix E305 pep8 issues on pyhbac-test.py
        4c3ddbb11  TESTS: Fix E711 pep8 issues on sssd_group.py
        a7acb83aa  TESTS: Fix E305 pep8 issues on sssd_netgroup.py
        c13c7dd58  TESTS: Fix E501 pep8 issues on utils.py
        e27a07b94  TESTS: Fix E305 pep8 issues on conf.py
        6df889594  CONTRIB: Fix E501 pep8 issues on sssd_gdb_plugin.py
        942edc402  CONTRIB: Fix E305 pep8 issues on sssd_gdb_plugin.py
        40fab0e80  TESTS: Fix E302 pep8 issues on test_enumeration.py
        38cec2116  TESTS: FIX E501 pep8 issues on pysss_murmur-test.py
        a907aa073  CI: Enable pep8 check
        89f5332cc  CI: Ignore E722 pep8 issues on debian machines
        cce64caa7  TESTS: Fix E501 pep8 issues on test_netgroup.py
        718bce1f8  NSS: Remove dead code
        e5c74ab06  CONFDB: Start a ldb transaction from sss_ldb_modify_permissive()
        f405a4a36  TOOLS: Take into consideration app domains
        a73d70f7e  TESTS: Move get_call_output() to util.py
        885da2c88  TESTS: Make get_call_output() more flexible about the stderr log
        14b485b11  TESTS: Add a basic test of `sssctl domain-list`
        a40c6b428  KCM: Use json_loadb() when dealing with sss_iobuf data
        bfc6d9d61  KCM: Remove mem_ctx from kcm_new_req()
        2f11cf256  KCM: Introduce kcm_input_get_payload_len()
        786c40023  KCM: Do not use 2048 as fixed size for the payload
        b09cd3072  KCM: Adjust REPLY_MAX to the one used in krb5
        96fdbb2cb  KCM: Fix typo in ccdb_sec_delete_list_done()
        e588e24c9  KCM: Only print the number of found items after we have it
        519354d07  SERVER: Tone down shutdown messages for socket-activated responders
        4ab8734cc  MAN: Improve docs about GC detection
        851d31264  NSS: Add InvalidateGroupById handler
        709c42f0c  DP: Add dp_sbus_invalidate_group_memcache()
        ccd349f02  ERRORS: Add ERR_GID_DUPLICATED
        a537df2ea  SDAP: Add sdap_handle_id_collision_for_incomplete_groups()
        a2e743cd2  SDAP: Properly handle group id-collision when renaming incomplete groups
        514b2be08  SYSDB_OPS: Error out on id-collision when adding an incomplete group
        8655dd075  SECRETS: reset last_request_time on any activity
        cefadc6ee  KCM: reset last_request_time on any activity
        26592d1aa  RESPONDER: Add sss_client_fd_handler()
        2f7006567  RESPONDER: Make use of sss_client_fd_handler()
        04c236ca8  SECRETS: Make use of sss_client_fd_handler()
        01ef93a43  KCM: Make use of sss_client_fd_handler()
        1ab24b392  TESTS: Rename test_idle_timeout()
        ac9c3ad82  TESTS: Add test for responder_idle_timeout
        a30d0c950  TESTS: Fix typo in test_sysdb_domain_resolution_order_ops()
        cf4f5e031  SYSDB: Properly handle name/gid override when using domain resolution order
        10a0bda92  TESTS: Increase test_resp_idle_timeout* timeout
        28436b573  COVERITY: Add coverity support
        e55141348  MAKE_SRPM: Add --output parameter
        4568d68d5  Add .copr/Makefile
        d5c3070c3  CACHE_REQ: Don't force a fqname for files provider' output
        7f6ff80cf  cache_req: Don't force a fqname for files provider output
        a16d9743e  tests: Add a test for files provider + domain resolution order
        74a514722  man: Users managed by the files provider don't have their output fully-qualified
        8f4b18db0  Revert "CACHE_REQ: Don't force a fqname for files provider' output"
        f9b42e393  selinux_child: workaround fqnames when using DRO
        179c7fb36  sudo_ldap: fix sudoHost=defaults -> cn=defaults in the filter
        0f897b18f  Revert "sysdb custom: completely replace old object instead of merging it"
        f9e4c9341  sysdb_sudo: completely replace old object instead of merging it
        f8025ae01  tlog: only log in tcurl_write_data when SSS_KCM_LOG_PRIVATE_DATA is set to YES

    Jakub Hrozek (33):
        888d37d08  Bumping the version to track 1.16.2 development
        67645557d  IPA: Handle empty nisDomainName
        da6946012  TESTS: Fix E266 pep8 issues on test_ldap.py
        b4c08cb32  TESTS: Fix E231 pep8 issues on test_session_recording.py
        f02b0bddd  TESTS: Fix E501 pep8 issues on test_session_recording.py
        1129979bf  TESTS: Fix E303 pep8 issues on test_ldap.py
        250751bf8  SYSDB: When marking an entry as expired, also set the originalModifyTimestamp to 1
        0f6b5b02a  IPA: Qualify the externalUser sudo attribute
        f22528922  NSS: Adjust netgroup setnetgrent cache lifetime if midpoint refresh is used
        4a9100a58  TESTS: Add a test for the multiple files feature
        2d43eaf43  SDAP: Improve a DEBUG message about GC detection
        d2633d922  LDAP: Augment the sdap_opts structure with a data provider pointer
        35d6fb7ca  TESTS: Add an integration test for renaming incomplete groups during initgroups
        ba2d5f7a0  SYSDB: sysdb_add_incomplete_group now returns EEXIST with a duplicate GID
        91d1e4c13  MAN: Document which principal does the AD provider use
        d69e1da37  FILES: Do not overwrite and actually remove files_ctx.{pwd,grp}_watch
        1f8bfb697  FILES: Reduce code duplication
        81f16996c  FILES: Reset the domain status back even on errors
        c1bce7da6  FILES: Skip files that are not created yet
        77d63f561  FILES: Only send the request for update if the files domain is inconsistent
        65034a715  DYNDNS: Move the retry logic into a separate function
        b57dfac8a  DYNDNS: Retry also on timeouts
        3cff2c5e5  AD: Warn if the LDAP schema is overriden with the AD provider
        8a8285cf5  SYSDB: Only check non-POSIX groups for GID conflicts
        10213efaf  Do not keep allocating external groups on a long-lived context
        2952de740  CACHE_REQ: Do not fail the domain locator plugin if ID outside the domain range is looked up
        320cc4638  MAN: Fix the title of the session recording man page
        e354ec745  DP/LDAP: Only increase the initgrTimestamp when the full initgroups DP request finishes
        50a90eb24  LDAP: Do not use signal-unsafe calls in ldap_child SIGTERM handler
        7567215ca  AUTOFS: remove timed event if related object is removed
        9adc750a0  RESPONDERS: Enable the local negative timeout by default
        df8e1055b  LDAP: Suppress a loud debug message in case a built-in SID can't be resolved
        23c65bd29  Updating the translations for the 1.16.2 release

    Justin Stephenson (3):
        e32e17d04  DEBUG: Print simple allow and deny lists
        c1208b485  CONFDB: Add passwd_files and group_files options
        0d6d493f6  FILES: Handle files provider sources

    Lukas Slebodnik (21):
        15989964d  CI: Add dbus into debian dependencies
        a26330932  intg: convert results returned as bytes to strings
        adb9823dc  SYSDB: Remove unused parameter from sysdb_cache_connect_helper
        0b784c622  SPEC: Add gcc to build dependencies
        810935f67  UTIL: Use alternative way for detecting PyErr_NewExceptionWithDoc
        f0bcadfb0  CONFIGURE: drop unused check
        afe7060fa  SYSDB: Return ENOENT for mpg with local provider
        b0aa567b0  sysdb-tests: sysdb_search_group_by_name with local provider
        92addd7ba  selinux_child: Allow to query sssd
        51c6c4833  selinux_child: Fix crash with initialized key
        1e6381c81  BUILD: Remove unnecessary *flags from test_ipa_dn
        597677993  BUILD: Remove ldap libraries from SSSD_LIBS
        38158852c  BUILD: Remove ldap libraries from TOOL_LIBS
        11ff270f9  BUILD: Remove pcre libs from common *_LIBS
        a63c28695  BUILD: Remove pcre from krb5_child
        a10cd9ec0  BUILD: Remove libcollection form common *libs
        17f5b50d8  BUILD: Reduce dependencies of sss_signal
        af9c031a9  BUILD: Remove cares from sssd_secrets
        acc799684  BUILD: Remove libini_config from common libs
        a887e33fb  MONITOR: Do not use two configuration databases
        bc7b4a3be  CI: Prepare for python3 -> python

    Michal Židek (6):
        abf377672  AD: Missing header in ad_access.h
        7a42831b2  GPO: Add ad_options to ad_gpo_process_som_state
        744e2b4d0  GPO: Use AD site override if set
        e6e5fe349  GPO: Fix bug with empty GPO rules
        39d37f6da  GPO: DEBUG msg when GP to PAM mappings overlap
        f3f1bd4ac  GPO: Debugging default PAM service mapping

    Pavel Březina (3):
        47ad0778b  sudo ldap: do not store rules without sudoHost attribute
        cd4590de2  sysdb custom: completely replace old object instead of merging it
        fe58f0fbf  sssctl: move check for version error to correct place

    Richard Sharpe (1):
        8550c06fd  nss-imap: add sss_nss_getsidbyuid() and sss_nss_getsidbygid()

    Sumit Bose (38):
        0f8add07b  intg: enhance netgroups test
        19f5dd0b8  TESTS: simple CA to generate certificates for test
        0dc7f9066  TESTS: replace hardcoded certificates
        cbcb2dab1  TESTS: remove NSS test databases
        86c06c3b3  test_ca: add empty index.txt.attr file
        37a84285a  nss: initialize nss_enum_index in nss_setnetgrent()
        08db22b1b  nss: add a netgroup counter to struct nss_enum_index
        46a4c2656  nss-idmap: do not set a limit
        2c4dc7a4d  nss-idmap: use right group list pointer after sss_get_ex()
        b13cc2d14  NSS: nss_clear_netgroup_hash_table() do not free data
        c6b99b070  winbind idmap plugin: support inferface version 6
        095bbe17b  winbind idmap plugin: fix detection
        5b3941612  p11_child: move verification into separate functions
        6514c4bd8  p11_child: add verification option
        9971ee45e  utils: add get_ssh_key_from_cert()
        f5e1aaf86  utils: move p11 child paths to util.h
        2f897afd6  utils: add cert_to_ssh_key request
        176e4d24a  tests: add test for cert_to_ssh_key request
        842daeb71  ssh: use cert_to_ssh_key request to verify certifcate and get keys
        4f63a1a97  ssh: add option ssh_use_certificate_keys and enhance man page
        7190e0ef5  utils: remove unused code from cert utils
        165f58ab7  tests: add SSH responder tests
        b5136cd9a  p11_child: split common and NSS code into separate files
        6d6e4a5d1  p11_child: add OpenSSL support
        4eed225be  TESTS: make some cert auth checks order independent
        075f2f3ab  p11_child: allow tests to use OpenSSL version of p11_child
        ee76c686c  certmap: fix issue found by Coverity in OpenSSL version
        8adf6eadd  SPEC/CI: enable openssl build for Debian and upcoming versions
        8127b585a  certmap: allow missing empty EKU in OpenSSL version
        6191cf81d  KCM: be aware that size_t might have different size than other integers
        8aa56a9e8  sysdb: add sysdb_getgrgid_attrs()
        032221568  ipa: use mpg aware group lookup in get_object_from_cache()
        e66517dcf  ipa: allow mpg group objects in apply_subdomain_homedir()
        ad6ab3528  AD/LDAP: do not fall back to mpg user lookup on GC connection
        2571accde  cifs idmap plugin: use new sss_nss_idmap calls
        8ae68aa27  winbind idmap plugin: use new sss_nss_idmap calls
        54c040cb4  libwbclient-sssd: use new sss_nss_idmap calls
        b8da03b42  pysss_nss_idmap: add python bindings for new sss_nss_idmap calls

    Thorsten Scherf (1):
        6d3632290  man: Add FILES as a valid config option for 'id_provider'

    Yuri Chornoivan (1):
        a0173060a  MAN: Fix minor typos

    amitkuma (1):
        b8db8c2d8  sssctl: Showing help even when sssd not configured

    amitkumar50 (2):
        56839605d  MAN: Add sss-certmap man page regarding priority processing
        4ab4a26ea  MAN: Clarify how comments work in sssd.conf
