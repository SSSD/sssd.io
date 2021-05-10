SSSD 2.5.0 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* ``secrets`` support is deprecated and will be removed in one of the next versions of SSSD.
* ``local-provider`` is deprecated and will be removed in one of the next versions of SSSD.
* SSSD's implementation of ``libwbclient`` was removed as incompatible with modern version of Samba.
* This release deprecates ``pcre1`` support. This support will be removed completely in following releases.
* A home directory from a dedicated user override, either local or centrally managed by IPA, will have a higher precedence than the ``override_homedir`` option.
* ``debug-to-files``, ``debug-to-stderr`` command line and undocumented ``debug_to_files`` config options were removed.

New features
~~~~~~~~~~~~

* Added support for automatic renewal of renewable TGTs that are stored in KCM ccache. This can be enabled by setting ``tgt_renewal = true``. See the sssd-kcm man page for more details. This feature requires MIT Kerberos krb5-1.19-0.beta2.3 or higher.
* Backround sudo periodic tasks (smart and full refresh) periods are now extended by a random offset to spread the load on the server in environments with many clients. The random offset can be changed with ``ldap_sudo_random_offset``.
* Completing a sudo full refresh now postpones the smart refresh by ``ldap_sudo_smart_refresh_interval`` value. This ensure that the smart refresh is not run too soon after a successful full refresh.
* If ``debug_backtrace_enabled`` is set to ``true`` then on any error all prior debug messages (to some limit) are printed even if ``debug_level`` is set to low value (for details see ``man sssd.conf``: ``debug_backtrace_enabled`` description).
* Besides trusted domains known by the forest root, trusted domains known by the local domain are used as well.
* New configuration option ``offline_timeout_random_offset`` to control random factor in backend probing interval when SSSD is in offline mode.

Important fixes
~~~~~~~~~~~~~~~

* ``ad_gpo_implicit_deny`` is now respected even if there are no applicable GPOs present
* During the IPA subdomains request a failure in reading a single specific configuration option is not considered fatal and the request will continue
* unknown IPA id-range types are not considered as an error
* SSSD spec file ``%postun`` no longer tries to restart services that can not be restarted directly to stop produce systemd warnings

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* Added ``tgt_renewal``, ``tgt_renewal_inherit``, and ``krb5_*`` KCM options to enable, and tune behavior of new KCM renewal feature.
* Added ``ldap_sudo_random_offset`` (default to ``30``) to add a random offset to backround sudo periodic tasks (smart and full refresh).
* Introduced new option 'debug_backtrace_enabled' to control debug backtrace.
* Added ``offline_timeout_random_offset`` configuration option to control maximum size of random offset added to offline timeout SSSD backend probing interval.
* Long time deprecated and undocumented ``debug_to_files`` option was removed.

Tickets Fixed
-------------

- `#2765 <https://github.com/SSSD/sssd/issues/2765>`_ - [RFE] Expand kerberos ticket renewal in KCM
- `#4415 <https://github.com/SSSD/sssd/issues/4415>`_ - Document that if two certificate matching rules with the same priority match only one is used
- `#4973 <https://github.com/SSSD/sssd/issues/4973>`_ - NSS responder should clear negative cache alongside with memcache
- `#5311 <https://github.com/SSSD/sssd/issues/5311>`_ - 'getent group ldapgroupname' doesn't show any LDAP users or some LDAP users when 'rfc2307bis' schema is used with SSSD.
- `#5330 <https://github.com/SSSD/sssd/issues/5330>`_ - automount sssd issue when 2 automount maps have the same key (one un uppercase, one in lowercase)
- `#5336 <https://github.com/SSSD/sssd/issues/5336>`_ - sssd's configure.ac breaks with Autoconf 2.69c (beta release of 2.70)
- `#5406 <https://github.com/SSSD/sssd/issues/5406>`_ - sssd-kcm starts successfully for non existent socket_path
- `#5459 <https://github.com/SSSD/sssd/issues/5459>`_ - Completely remove SSSD's implementation of libwbclient.
- `#5488 <https://github.com/SSSD/sssd/issues/5488>`_ - Unexpected (?) side effect of SSSDBG_DEFAULT change
- `#5505 <https://github.com/SSSD/sssd/issues/5505>`_ - SSSD Error Msg Improvement:   write_krb5info_file failed, authentication might fail.
- `#5514 <https://github.com/SSSD/sssd/issues/5514>`_ - [RFE] SSSD logs improvements: clarify which config option applies to each timeout in the logs
- `#5521 <https://github.com/SSSD/sssd/issues/5521>`_ - sssd tries to restart its unit which has RefuseManualStart=true
- `#5523 <https://github.com/SSSD/sssd/issues/5523>`_ - `setXYent()` fail to rewind.
- `#5528 <https://github.com/SSSD/sssd/issues/5528>`_ - SSSD  not detecting subdomain from AD forest (RHEL 8.3)
- `#5531 <https://github.com/SSSD/sssd/issues/5531>`_ - Authentication handshake (ldap_install_tls()) fails due to underlying openssl operation failing with EINTR
- `#5534 <https://github.com/SSSD/sssd/issues/5534>`_ - IPA missing secondary IPA Posix groups in latest sssd 1.16.5-10.el7_9.7
- `#5540 <https://github.com/SSSD/sssd/issues/5540>`_ - sssd not thread-safe in innetgr()
- `#5545 <https://github.com/SSSD/sssd/issues/5545>`_ - kcm: implement GET_CRED_LIST for faster iteration
- `#5556 <https://github.com/SSSD/sssd/issues/5556>`_ - [RFE] make 'random_offset' addon to 'offline_timeout' option configurable
- `#5561 <https://github.com/SSSD/sssd/issues/5561>`_ - No gpo found and ad_gpo_implicit_deny set to True still permits user login
- `#5563 <https://github.com/SSSD/sssd/issues/5563>`_ - sssd-2.4.2: build using autoconf 2.71 fails
- `#5568 <https://github.com/SSSD/sssd/issues/5568>`_ - pam_sss_gss.so doesn't work with large kerberos tickets
- `#5571 <https://github.com/SSSD/sssd/issues/5571>`_ - FreeIPA: New subid_range idrange entry breaks sudo domain resolution order
- `#5586 <https://github.com/SSSD/sssd/issues/5586>`_ - Clarify "single_prompt" option in "PROMPTING CONFIGURATION SECTION" section of sssd.conf man page
- `#5589 <https://github.com/SSSD/sssd/issues/5589>`_ - sss_override does not take precedence over override_homedir directive
- `#5596 <https://github.com/SSSD/sssd/issues/5596>`_ - sss_cache: reset originalModifyTimestamp in timestamp cache as well
- `#5598 <https://github.com/SSSD/sssd/issues/5598>`_ - NULL dereference in monitor_service_shutdown()
- `#5601 <https://github.com/SSSD/sssd/issues/5601>`_ - sssd-ldap(5) does not report how to disable the SUDO smart queries
- `#5603 <https://github.com/SSSD/sssd/issues/5603>`_ - document impact of indices and of scope on performance of LDAP queries
- `#5604 <https://github.com/SSSD/sssd/issues/5604>`_ - [RFE] improve the sssd refresh timers for SUDO queries
- `#5609 <https://github.com/SSSD/sssd/issues/5609>`_ - [RFE] Randomize the SUDO timeouts upon reconnection

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.4.2..2.5.0

    Alexander Bokovoy (3):
        32d2aa554  prompt config: fix covscan errors
        d73f12827  covscan: initialize ret variable before use
        42c9ca0cd  covscan: symlink() expects non-NULL second argument

    Alexey Tikhonov (43):
        1724482ca  DEBUG: replace localtime() with localtime_r()
        f553b57dd  DEBUG: replace gettimeofday() with time() if usec isn't needed
        5f840192e  DEBUG: cache string representation of last timestamp
        b8d8b3775  p11_child: fixed mistype in a debug message
        9da41eb91  SPEC: added 'BuildRequires: po4a'
        2a512fdf5  systemd configs: add CAP_DAC_OVERRIDE for ifp in certain case
        0fd0681d3  Moved ldb_debug_messages() out of UTILS to SYSDB
        0dfb188ee  Moved declaration of debug related helpers defined in debug.c from util.h to debug.h
        fee3883bb  DEBUG: use '--logger' as the only option to configure logger type.
        fc5b64e8b  DEBUG: make use of existing SSSD_DEBUG_OPTS macro
        c14e439cf  DEBUG: incorporate sss_set_logger() into DEBUG_INIT
        4d133e154  DEBUG: remove sss_set_logger() from public API
        cf6991704  DEBUG: added several comments to debug.h API and moved rarely used / "private" functions to the bottom.
        374d644f0  Moved SSSDBG_MASK_ALL out of debug.h since is it is only used in tests.
        dde57f768  DEBUG: incorporate open_debug_file() into DEBUG_INIT
        21334de23  MONITOR: added logging of cmd used to start services
        0cddb6712  DEBUG: introduce SSSDBG_TOOLS_DEFAULT
        66960c769  MONITOR: in case '-i' is given don't force logger to 'stderr' if its value specified explictly
        dab0ead20  SYSV: removed unused SUSE/sssd.id
        37d255b28  SYSV: replaced '-f' option in gentoo/sssd.in
        53ae9b1e3  pam_sss: fixed potential mem leak
        64340cacd  whitespace_test: remove 'debian' from exclude pattern as this is downstream specific.
        38905cac4  monitor: avoid NULL deref in monitor_service_shutdown()
        cbfccb173  BUILD: prefer PCRE2 over PCRE
        519d94342  util/regexp: local functions shall be static
        31bcb6f03  tests/test_dp_opts: mem leak fixed
        9aa6fb34b  tests/test_nested_groups: mem leak fixed
        0fbe5af1f  util/regexp: regular talloc d-tor shouldn't fail
        f2bcf74c4  sssd.supp: suppress false positive valgrind warning about 'pcre2_code' ptr
        846296d17  libwbclient-sssd: removed
        99beee3c3  LDAP: make connection log levels consistent
        f66b5aeda  DEBUG: got rid of most explicit DEBUG_IS_SET checks as a preliminary step for "logs backtrace" feature
        59ba14e5a  DEBUG: poor man's backtrace
        e3426ebeb  PAM: fixes a couple of covscan issues
        6b78b7aa8  CACHE_REQ: fixed REVERSE_INULL warning
        0aaf61c66  DEBUG: makes debug backtrace switchable
        97f046e72  DEBUG: log IMPORTANT_INFO if any bit >= OP_FAILURE is on
        f693078fe  CERTMAP: removed "sss_certmap initialized" debug
        6fb987b5c  SERVER: decrease log level in `orderly_shutdown()` to avoid backtrace in this case.
        80963d683  SBUS: changed debug level in sbus_issue_request_done() to avoid backtrace dump in case of 'ERR_MISSING_DP_TARGET'
        c8274b248  BUILD: deprecate 'local-provider'
        8736776a7  BUILD: deprecate 'secrets' support
        ce54789e7  DEBUG: fix _all_levels_enabled()

    Deepak Das (2):
        0ff8d462b  SSSD Log: write_krb5info_file word replacement
        f55c41b7a  SSSD Log: log_timeout_parameter_display

    Heiko Schlittermann (HS12-RIPE) (1):
        0e0951478  Fix setXYent(): rewind always

    Hugh Cole-Baker (1):
        a0179e31c  man: fix p11_uri example URIs

    Iker Pedrosa (3):
        49010b16e  configure: set CPP macro with AC_PROG_CPP
        da55e3e69  ldap: retry ldap_install_tls() when watchdog interruption
        9854ade16  spec: Remove ldconfig scripts

    Justin Stephenson (8):
        986964149  CI: Use builtin command for pycodestyle check
        993b66d48  KCM: Read and set KCM renewal and krb5 options
        599f0ad05  KCM: Prepare and execute renewals
        1dc3c33c8  SECRETS: Don't hardcode SECRETS_DB_PATH
        a55405b3e  TESTS: Add kcm_renewals unit test
        0202eb53a  INTG: Add KCM Renewal integration test
        ddcedbf3b  KCM: Conditionally build KCM renewals support
        ec932d351  KCM: Disable responder idle timeout with renewals

    Marco Trevisan (Treviño) (5):
        05e75dba3  test_pam_srv: Add test for CA certificate check using intermediate CA
        5ed48d2f8  p11_child_openssl: Free X509_VERIFY_PARAM if initialized
        018043bbd  p11_child: Add support for 'partial_chain' certificate_verification option
        7e3edb062  pam: Add custom pam_cert_verification setting to override default
        65c90d8f9  sssd.spec: BuildRequires on openssl tool

    Massimiliano Torromeo (1):
        cd843dafe  configure: Fix python headers detection with recent autoconf Resolves: https://github.com/SSSD/sssd/issues/5336

    Pavel Březina (17):
        9eeaf23ba  Update version in version.m4 to track the next release
        815197cb1  spec: do not use systemd to restart services with RefuseManualStart=true
        c796088ea  selinux: fix warning ‘security_context_t’ is deprecated
        3fba29f98  selinux: fix warning ‘matchpathcon’ is deprecated
        ecf26727c  selinux: make SEC_CTX and SELINUX_CTX typedef instead of macro
        9a39ceba2  kcm: remove unneeded kcm.h
        81130b232  kcm: add support for MIT extensions
        560e24790  kcm: add GET_CRED_LIST for faster iteration
        c79ee66fa  pot: update pot files
        61a03b2cc  man: document how to disable sudo smart and full refresh
        b3247eeb5  man: document how to tune sudo performance
        c0204c063  be: add be_ptask_postpone
        d9d5c291f  sudo: reschedule periodic tasks when full refresh is finished
        ca47accad  sudo: add ldap_sudo_random_offset
        e30129410  man: add krb5_options to po4a.cfg
        b3336ab97  pot: update pot files
        3f29bc26c  Release sssd-2.5.0

    Paweł Poławski (5):
        4f3734274  ncache: Fix misleading function comment
        e69943594  utils: Add description for CLEAR_MC_FLAG define
        6195ac70b  nss: Add negcache clearing sbus callback
        7a4974c87  nss: Clear negative cache when SIGHUP received
        191b53529  data_provider: Configure backend probing interval

    Sam Morris (6):
        b6efe6b11  responder/common/responder_packet: handle large service tickets
        c6a762835  responder/common/responder_packet: reduce duplication of code that handles larger-than-normal packets
        63f318f73  responder/common/responder_packet: add debug logging to assist with errors caused by overlarge packets
        37d331774  responder/common/responder_packet: further increase packet size for SSS_GSSAPI_SEC_CTX
        5c9fa75bd  responder/common/responder_packet: remove some unnecessary checks before growing packet
        b87619f9a  responder/common/responder_packet: allow packets of max size

    Shridhar Gadekar (2):
        2276fc426  Tests: alltests: fetch autofs maps after coming online
        eb61f1b2f  test: minor change in test doc string

    Steeve Goveas (6):
        b5c2389bc  TEST: Add function to control services
        b165acb6d  TEST: missing multihost in service_ctrl
        c7733c444  TEST: Update test docstrings enable polarion updates
        6a60406b1  TEST: Modify subsystem to sst_idm_sssd
        ba99c1fb6  modify check for rhel version before package install
        d264a2b65  TEST: remove pytest warning for yield_fixture

    Sumit Bose (14):
        509c2ac93  ipa: skip id-range of unknown type
        27172c955  ipa: add unit test for ipa_ranges_parse_results
        02d9625ef  ipa subdomains: do not fail completely if one step fails
        e865b008a  AD GPO: respect ad_gpo_implicit_deny if no GPO is present
        231d11187  negcache: use right domain in nss_protocol_fill_initgr()
        5d65411f1  sss_domain_info: add not_found_counter
        95adf488f  AD: read trusted domains from local domain as well
        e0fcec928  man: clarify single_prompt option
        691fe4944  nss: prefer homedir overrides over override_homedir option
        88eec1c22  nss client: make innetgr() thread safe
        29abf94e3  intg test: test is innetgr() is thread-safe
        7313efba2  man: clarify priority in sss-certmap man page
        de1709041  sss_cache: reset original timestamp and USN
        c227ea4ec  sysdb: add SYSDB_INITGR_EXPIRE to new user objects

    Tomas Halman (1):
        f1661c04a  DEBUG: Error is printed when everything is ok

    Weblate (2):
        341c5e358  po: update translations
        c07a7beb8  po: update translations

    aborah (4):
        634b3c940  TESTS: First smart refresh query contains modifyTimestamp even if the modifyTimestamp is 0
        231978812  Tests: Tests if shadow-utils are immune against bugs in 2006:0032
        421c0a774  Tests: getent group ldapgroupname doesn't show any LDAP users
        47b40cca0  Tests: automount sssd issue when 2 automount maps have the same key (one un uppercase, one in lowercase)

    ikerexxe (1):
        8e8ccca5d  TESTS: test socket path when systemd activation

    peptekmail (1):
        0e1452421  TEST: FIX: When generating a ssh pubkey from a cert extra padding is needed if a nonstandard eponent is chosen.

