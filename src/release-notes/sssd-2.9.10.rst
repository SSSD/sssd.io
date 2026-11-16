SSSD 2.9.10 Release Notes
=========================

Highlights
----------

New features
~~~~~~~~~~~~

- Unified passwordless login in the GUI. SSSD now supports a rich authentication
  selection interface. Users can login with smartcards, passkey, External IdPs
  and passwords directly within the graphical user interface.

Important fixes
~~~~~~~~~~~~~~~

- Fixed 32-bit integer overflow in Kerberos/KCM timestamp handling. Kerberos
  timestamps are now treated as unsigned 32-bit values, correcting credential-cache
  and ticket expiry/renewal calculations for dates after January 2038.
- SSSD no longer crashes if ``ldap_read_rootdse = never`` and
  ``enumerate = true``
- `CVE-2026-80048 <https://nvd.nist.gov/vuln/detail/cve-2026-80048>`_
- `CVE-2026-104048 <https://nvd.nist.gov/vuln/detail/cve-2026-104048>`_
- `CVE-2026-104035 <https://nvd.nist.gov/vuln/detail/cve-2026-104035>`_
- `CVE-2026-88252 <https://nvd.nist.gov/vuln/detail/cve-2026-88252>`_
- `CVE-2026-104044 <https://nvd.nist.gov/vuln/detail/cve-2026-104044>`_
- `CVE-2026-104042 <https://nvd.nist.gov/vuln/detail/cve-2026-104042>`_
- `CVE-2026-104030 <https://nvd.nist.gov/vuln/detail/cve-2026-104030>`_
- `CVE-2026-104032 <https://nvd.nist.gov/vuln/detail/cve-2026-104032>`_
- `CVE-2026-104031 <https://nvd.nist.gov/vuln/detail/cve-2026-104031>`_
- `CVE-2026-104037 <https://nvd.nist.gov/vuln/detail/cve-2026-104037>`_
- `CVE-2026-104029 <https://nvd.nist.gov/vuln/detail/cve-2026-104029>`_
- `CVE-2026-104033 <https://nvd.nist.gov/vuln/detail/cve-2026-104033>`_
- `CVE-2026-104043 <https://nvd.nist.gov/vuln/detail/cve-2026-104043>`_
- `CVE-2026-104045 <https://nvd.nist.gov/vuln/detail/cve-2026-104045>`_
- `CVE-2026-92821 <https://nvd.nist.gov/vuln/detail/cve-2026-92821>`_
- `CVE-2026-104036 <https://nvd.nist.gov/vuln/detail/cve-2026-104036>`_
- `CVE-2026-104039 <https://nvd.nist.gov/vuln/detail/cve-2026-104039>`_
- `CVE-2026-104038 <https://nvd.nist.gov/vuln/detail/cve-2026-104038>`_
- `CVE-2026-90994 <https://nvd.nist.gov/vuln/detail/cve-2026-90994>`_
- `CVE-2026-90463 <https://nvd.nist.gov/vuln/detail/cve-2026-90463>`_
- `CVE-2026-90996 <https://nvd.nist.gov/vuln/detail/cve-2026-90996>`_
- `CVE-2026-90995 <https://nvd.nist.gov/vuln/detail/cve-2026-90995>`_
- `CVE-2026-90462 <https://nvd.nist.gov/vuln/detail/cve-2026-90462>`_
- `CVE-2026-68742 <https://nvd.nist.gov/vuln/detail/cve-2026-68742>`_
- `CVE-2026-68743 <https://nvd.nist.gov/vuln/detail/cve-2026-68743>`_
- `CVE-2026-68744 <https://nvd.nist.gov/vuln/detail/cve-2026-68744>`_
- `CVE-2026-14474 <https://nvd.nist.gov/vuln/detail/cve-2026-14474>`_
- `CVE-2026-14476 <https://nvd.nist.gov/vuln/detail/cve-2026-14476>`_

Packaging changes
~~~~~~~~~~~~~~~~~

- SSSD now supports authentication mechanism selection through PAM using a
  JSON-based protocol. This feature enables passwordless authentication
  mechanisms in GUI login environments that support the protocol. Feature will
  be supported by GNOME Display Manager (GDM) starting with GNOME 50. While
  currently optimized for GNOME, the JSON protocol design allows for future
  support in other display managers. authselect is the recommended approach and
  will handle the necessary PAM stack modifications automatically starting with
  version 1.7 through the new option ``with-switch-auth`` which provides a new
  PAM service called ``switchable-auth``. Manual PAM configuration is also
  possible. For more technical details and implementation specifications, see
  the design documentation: https://github.com/SSSD/sssd.io/pull/79

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

- The “gdm-password” service was removed from the default
  pam_p11_allowed_services list, so it is no longer offered Smartcard
  authentication by default. The previous behavior can be restored by adding
  “pam_p11_allowed_services = +gdm-password” to the [pam] section of sssd.conf.
- ‘autofs’ responder now supports ``allowed_uids`` config option that defaults
  to “0”
- A new option ``pam_json_services`` is now available to enable JSON protocol to
  communicate the available authentication mechanisms.

Tickets Fixed
-------------

* `#5129 <https://github.com/SSSD/sssd/issues/5129>`__ - id_provider = proxy proxy_lib_name = files returns * in password field, breaking PAM authentication
* `#5898 <https://github.com/SSSD/sssd/issues/5898>`__ - Improve the 'sssctl analyze' help output
* `#7289 <https://github.com/SSSD/sssd/issues/7289>`__ - [rule/allows_nss_options]: Attribute 'offline_timeout_random_offset' is not allowed in section 'nss'. Check for typos
* `#7335 <https://github.com/SSSD/sssd/issues/7335>`__ - sssd.conf(5): id_provider : no default mentioned
* `#7336 <https://github.com/SSSD/sssd/issues/7336>`__ - sssd.conf(5): selinux_provider: "Use the value of `id_provider`, if set and can handle SELinux loading requests". What happens if it cannot handle loading requests?
* `#7339 <https://github.com/SSSD/sssd/issues/7339>`__ - sssd.conf(5): "Please see the section “FAILOVER” for more information about the service resolution." No such section "FAILOVER"
* `#7340 <https://github.com/SSSD/sssd/issues/7340>`__ - sssd.conf(8): dns_resolver_server_timeout: "Defines the amount of time (in milliseconds) SSSD would try to talk to DNS server before trying next DNS server." Ambiguous wording
* `#7341 <https://github.com/SSSD/sssd/issues/7341>`__ - sssd.conf(5): override_gid: "Override the primary GID value with the one specified." Ambiguous wording, no mention of default
* `#7345 <https://github.com/SSSD/sssd/issues/7345>`__ - sssd.conf(8): FILE FORMAT: Are parameter values case sensivite? is TRUE == true?
* `#7351 <https://github.com/SSSD/sssd/issues/7351>`__ - sssd.conf(5): cached_auth_timeout: ambiguous explanation
* `#7380 <https://github.com/SSSD/sssd/issues/7380>`__ - sssd.conf: session recording: no mention of [session_recording] heading
* `#8292 <https://github.com/SSSD/sssd/issues/8292>`__ - Test failure: ssh with OTP login in IPA environment
* `#8331 <https://github.com/SSSD/sssd/issues/8331>`__ - kerberos ccache filename is replaced on every concurrent login with the same user
* `#8718 <https://github.com/SSSD/sssd/issues/8718>`__ - 'sssctl analyze --help' shows incorrect command 'sss_analyze' in usage field
* `#8796 <https://github.com/SSSD/sssd/issues/8796>`__ - Use-after-free crash in PAM responder during YubiKey / PKCS#11 authentication
* `#8821 <https://github.com/SSSD/sssd/issues/8821>`__ - Contradictory statement in sssd.conf man-page w.r.t. session_recording
* `#8823 <https://github.com/SSSD/sssd/issues/8823>`__ - Incorrect option ipa_hbac_selinux is documented in sssd-ipa man-page
* `#8829 <https://github.com/SSSD/sssd/issues/8829>`__ - sssd man-pages inconsistent about bool/boolean usage
* `#8914 <https://github.com/SSSD/sssd/issues/8914>`__ - Incorrect Default defined for ldap_user_nds_login_expiration_time option in sssd-ldap-attributes(5) man
* `#8916 <https://github.com/SSSD/sssd/issues/8916>`__ - Incorrect Default defined for ldap_host_object_class option in sssd-ldap-attributes(5) man
* `#9030 <https://github.com/SSSD/sssd/issues/9030>`__ - Possibly spurious warning about ldap_sudo_search_base
* `#9197 <https://github.com/SSSD/sssd/issues/9197>`__ - 'local' provider is removed from sssd but an orphaned include/local.xml file is present
* `#9367 <https://github.com/SSSD/sssd/issues/9367>`__ - pam: GDM switchable authentication never offers local Smartcard authentication

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.9..2.9.10

    Abhinay Reddy Peddireddy (1):
        942f0c97f  Man: fix sss_obfuscate(8) domain option and synopsis

    Akash Sundarkar (1):
        3cce42179  man: fix SEE ALSO punctuation after pam_sss

    Akshay Sakure (30):
        02810fffa  Component: sssd-tools
        aea06316c  sssd man-page: Improve man-page for override_gid
        0642cecf4  sssd man-page: Fix man-page for offline_timeout*
        c55c6a21e  sssd man-page: Add reference to FAILOVER section
        46390efb9  sssd man-page: Add headings [] for all services
        347a0d571  [backport: sssd-2-9] sssd man-page: Add Default for id_provider
        f747da059  man: Remove obsolete RHEL 5 krb5.conf note from sssd-ad
        1a47a29d1  sssd man-page: Improve FILE FORMAT section
        868d28b5d  Config: Allow description parameter in [session_recording] section
        c8233329d  Man: Add note about debug* options for [session_recording] in sssd.conf
        b2a4e780e  man: Replace ldap_opt_timout -> ldap_opt_timeout
        a1ebb46c5  man: Add Default for vetoed_shells in sssd.conf(5)
        83ed2518f  man: Replace bool -> boolean across sssd man-pages
        18cb10274  man: Correct default for ldap_user_nds_login* options
        138542d0d  man: Correct default for ldap_host_object_class option
        4d9ae5f87  man: Remove duplicate sentence from intro sssd-kcm(8)
        38701709e  man: Correction of typo in pam_sss(8)
        2cc98b5ab  sssd.conf man: Improve explanation for cached_auth_timeout
        98b56ee57  [backport: sssd-2-9] man: Remove obsolete RHEL 5 krb5.conf note from sssd-ipa
        15b1d85d9  [backport: sssd-2-9] man: Replace ipa_hbac_selinux -> ipa_selinux_refresh in sssd-ipa
        035b05bba  [backport: sssd-2-9] man: Replace 'bool' by 'boolean' in sssd-ipa
        7cca533b0  man: Correct the ports for ad_use_ldaps option
        83bbdd23c  man: Improvement in desc for smart refresh in sssd-sudo
        7ce8ce80e  man: Improve description for dns_resolver_server_timeout
        c773786e7  Remove obsolete entry_cache_computer_timeout option
        6150fd445  Fix: Remove an orphaned include local.xml
        d639b0cba  Man: Improve description for dyndns_refresh_interval
        ffbaa018a  Man: Remove empty <para></para> from sssd-ad.5.xml
        e72b0f955  Man: Improve description for selinux_provider option
        2597173d2  sssctl: Improve the 'sssctl analyze' help output

    Alexey Tikhonov (30):
        fb2a7d047  KRB5_CHILD: allow `k5c_ccache_setup()` during SSS_PAM_PREAUTH
        2c0c68911  ipa: fix memory leak in ipa_s2n_get_list iteration
        014329d0f  ipa: free stale attrs in `ipa_s2n_get_list()` iteration
        e6da18d97  cfg_rules: allow ldap_sasl_authid/ldap_krb5_keytab/krb5_keytab
        db7ffa3ea  PAM: fix use-after-free during p11_child processing
        e3600f605  ci: harden pull_request_target workflows against pwn requests
        91017d89f  gpo: reject path traversal in gPCFileSysPath
        71f52c4a1  sudo: warn when ldap_sudo_search_base falls back to root DN
        3225ef24f  CI: don't specify 'push:'/'pull_request:' branches
        e51789202  ci: drop 'analyze-target.yml'
        c8bfe7f35  sudo: don't warn about search base when it was set by provider
        dc591525a  CI 2-9: use 'centos-9' for 'make-distcheck'
        e1372d983  Bump version to track sssd-2.9.10 release
        e53b9e63e  pam: validate auth_token_length in extract_authtok_v1()
        f55d3ef9d  nss: validate addrlen in sss_nss_protocol_parse_addr()
        a96f9c4da  NSS: fix initgroups packet heap disclosure
        95a2eb252  LDAP: fix fail-open in ppolicy access check on zero results
        da28b654e  PAM: avoid NULL deref when service item is missing
        a345ea896  NSS: reject empty request body before body[blen - 1] access
        9819bb9c5  NSS: factor request body validation into a helper
        dcb62de4f  NSS: bound service parser reads to the request body length
        fe673972b  PAM: fix out-of-bounds read in v1 request parser
        204f87acb  SYSDB: sanitize SID string in `sysdb_search_entry_by_sid_str()`
        9084f0696  autofs: fix out-of-bounds reads in request parsers
        e45c8609a  autofs: free per-request context on successful replies
        5765f18da  autofs: add 'allowed_uids' option to the autofs responder
        ab5bd26b1  Additional fixes for krb5 timestamps overflow
        f7578f47a  CI: require ACCEPTED to be set
        dfeb1d535  CI: require backport label to be set
        b3876bfb0  PTASK: add sanity guards

    Bernhard M. Wiedemann (1):
        96aa78afa  Avoid int overflow after year 2038

    Dan Lavu (25):
        8d91c237f  tests: updating pysss_nss_idmap error with more detail
        b9d40b824  tests: manual backporting of test_memcache.py
        9bd99a547  tests: fixing authselect teardown order
        5fec3dd38  tests: improving offline authentication tests
        137d8e94b  KCM: fix use-after-free of ccache name during TGT renewal
        6420eef51  KCM: free auth_data on TGT renewal setup failure
        14e4f14ee  tests: widen KCM TGT renewal poll window
        64bcfb43a  removing deprecated pam_ldap pam_krb proxy provider multihost tests
        d5094ecae  tests: remove multihost/alltests/test_sssctl_analyzer.py
        3a0d7e71f  tests: remove multihost/alltests/test_sudo.py
        c2ecd7b46  tests: remove multihost/alltests/test_sss_cache.py
        255d2bf3f  tests: remove multihost/ad/test_sudo.py
        22514e289  tests: remove multihost/alltests/test_autoprivategroup.py
        6b6961588  tests: remove multihost/alltests/test_rfc2307.py
        19a06d7b3  tests: adding gpo test case for traversal bug
        cece72c53  tests: add GPO regression tests for local group collision and verbose Samba logging
        ba8e7e272  test rewrite: legacy intg test_pam_responder.py - first batch
        aa5f41c78  test rewrite: legacy intg test_pam_responder.py - remaining batch
        0f4c84024  tests: remove two-tokens smartcard test on this platform
        21f175c0e  tests: remove legacy intg test suite
        6ce5d7035  CI: trim unused deps.sh/distro.sh helpers, rename matrix key, fix keytab leak
        b1f6366ec  CI: drop Debian as a build target
        7986d86ff  CI: drop codeql job on this stable branch
        bbb11d103  tests: collapse su/ssh parametrization in test_gpo.py
        5ff6cdc88  tests: add AD forest short-name resolution cases

    Harsh Bhadauriya (1):
        9629ac181  man: fix doubled "are" in sssd-ldap(5)

    Iker Pedrosa (39):
        7d47dd3bd  util: implement pam_get_response_data()
        ecd8ebbcc  sss_client: add EIdP to prompt_config structure
        88c714949  Responder: tune prompts in the GUI
        b3a9cb2ac  Responder: generate JSON message for GUI
        a05cb30e0  Responder: unpack JSON reply from GUI
        470a3d1ee  Responder: check PAM service file for JSON protocol
        9d7998b87  Responder: new option `pam_json_services`
        a1777b281  Responder: call JSON message generation
        c85859645  SSS_CLIENT: forward available auth JSON message
        dbfb5185b  Responder: parse GUI reply
        970e1df5c  Test: adapt test_pam_srv to JSON message
        6540db694  Responder: check return value for json_string()
        b1307326e  Responder: update JSON message format
        c1d9b9d10  sss_client: modify smartcard in prompt_config structure
        7fd02b5ae  util: implement pam_get_response_data_all_same_type()
        faeec86c1  Responder: generate JSON message for smartcard
        fc69ec892  Responder: parse reply for smartcard
        a93959dfd  Responder: refactor JSON functions to reduce args
        3b56743da  Responder: extend smartcard JSON request message
        bb37515ad  Responder: extend smartcard JSON reply message
        ce9b0e9c6  Responder: make `decode_pam_passkey_msg()` public
        a0bc56928  Responder: generate JSON message for passkey
        b49fb1440  util: implement function to set passkey PIN
        9c6758568  Responder: parse reply for passkey
        590caf2a3  krb5_child: advertise authentication methods
        e6956137b  Responder: add `gdm-switchable-auth` to `pam_p11_allowed_services` defaults
        03ebcb71f  sss_client: prevent JSON auth during password change preauth
        d87b3fd6e  Responder: change authentication mechanism detection
        8395c756e  man: clarify and fix `pam_json_services` compilation
        c354593c4  krb5: port pre-authentication retry logic
        08b512d85  krb5_child: fix OTP authentication for PAM stacked tokens
        abbd851d2  krb5_child: fix enterprise principal parsing in keep-alive sessions
        9f623fa38  Files: fix build failure after sysdb_enumpwent removal
        a1501ee74  tests: add TMT plan for passkey testing
        cca8f42bb  ci: add TMT passkey tests to packit workflow
        5a0ccab33  ci: fix error handling in passkey TMT plan SSH commands
        93bc3aa51  ci: use hardware.memory syntax for TMT passkey tests
        0ee6556c4  ci: update passkey TMT plan for native CentOS Stream 9 execution
        f6f0b899d  ci: fixes for CentOS Stream 9

    Jakub Vávra (11):
        57eb04a2f  Tests: Fix test_refresh_contain_timestamp
        7f177de3f  Tests: Update LdapOperations to fail on bind immediately
        abfb84be7  Tests: Auto skip tests dependent on ldbsearch when unavailable
        8886dbb09  Tests: Switch tests using ldap adparameters ported to ldifde
        90189b15e  tests: Update ds tests to rely less on hostname
        b95e43781  tests: Fix regex warnings
        aab6074f5  ci: Swap flake and isort for ruff and reorder jobs
        50f7ec988  tests: Fix test used in c-ares gating to be more resilient
        e4ca855da  ci: Fix duplicated python-system-tests in static-code-analysis
        999019eb5  tests: add AD forest multidomain system tests
        f88566388  tests: Align AD forest test names and grouping

    Joan Torres Lopez (3):
        acf3ca823  PAM: Stop treating gdm-password as a Smartcard-capable service
        063c833df  PAM: Move PKCS11_LOGIN_TOKEN_NAME export out of add_pam_cert_response()
        c0bcaac24  TESTS: cmocka: new 'test_pam_cert_auth_gdm_smartcard' test

    Justin Stephenson (10):
        7efc3cec9  tests: Clarify approx match filter
        2a37ad447  ci: Clear cache before installing built rpms
        779aa6a0d  ci: Dont run system tests for man page only PRs
        e7b2f9f59  autofs: avoid leaked enumeration contexts after map
        f0866da1d  nss: guard against length underflow in packet
        9a98b0b1b  authtok: add length to unpack passkey blob
        3c4917867  pam: guard against zero-length string auth tokens
        3bfa7b79b  pam: prevent null dereference in kerberos passkey flow
        e36f80528  authtok: Make sss_auth_unpack_passkey_blob static
        cc37d2a29  util: Use remaining size instead of full size

    Madhuri Upadhye (12):
        85fb157b2  Tests: fix GSSAPI SSH test setup for krb5_confd_path
        08613394d  tests: port force-LDAPS coverage to system tests
        85b57abdf  Tests: Fix AD work on STIG-hardened systems
        0bd8e5dfc  Tests: Fix AD tests on STIG-hardened systems
        f330d00d4  Fix STIG fixture to handle sshd drop-in config files
        68a23dc90  Enable AES Kerberos encryption on AD for FIPS:STIG compatibility
        2f5d8e1d3  tests: convert bash ldap service_map suite to system tests
        ba96b9752  tests: cover sssctl debug-level when SSSD is stopped and for PAC
        acd151247  tests: wait for DNS resolve failure before checking logs
        14253a52f  tests: remove multihost tests already converted to system tests
        a345f4715  tests: fix EOF in test_config_validation.py
        16aad1e74  tests: remove leftover test_config_validation.py multihost suite

    Masahiro Matsuya (3):
        2663f5284  cfg_rules: add pwfield to allowed_domain_options
        0a08512d7  man: document pwfield per-domain usage in NSS section
        43ae9a2b3  test_kcm: use config_apply instead of start to avoid proxy domain auth issue

    Ondrej Valousek (1):
        be0d65ffc  Fix bug in objectclass_matched()

    Paul Adelsbach (1):
        8b9604604  pam: gate PAC indicator code on BUILD_SAMBA

    Pavel Březina (18):
        7640a7a3f  sdap: handle missing rootDSE gracefully
        1e07da20f  ci: serialize make distcheck in build.yml
        596bc73ab  ci: actually run the whitespace test
        763a32afa  tests: fix whitespace_test for files missing newline at eof
        2ea27a7de  ci: use ubuntu-26-04 runner to workaroud issues on ubuntu-24-04
        c3774b77e  nss: fix potential memory leak if packet grow fails
        6dd08f817  test: fix missing cmocka prerequisite includes in test_nfsidmap.c
        5318c7313  tests: automatically collect coredumps
        94c919d21  ci: move system tests from Github Actions to Testing Farm
        328be7696  ci: add polarion metadata check to static analyzers
        168c28897  ipa: compare users with domain awareness against HBAC rules
        74bdb9d43  kcm: prune per-connection credential cache on destroy
        bc884783d  responder: back off accept() on fd exhaustion to stop busy-spin
        c3445a52f  KCM: set the client fd non-blocking to avoid event-loop hangs
        de79cbfdb  KCM: allocate body buffer only once
        32ad86d08  KCM: reject request bodies smaller than the protocol header
        090bb4fbb  KCM: add kcm_recv_timeout to avoid stuck requests
        46055a1ce  ci: remove sssd db prior restarting it on ipa container

    Peter Šišan (12):
        9a7d0870e  tests: adds sss_override takes precedence over override homedir
        8f45d21be  tests: adds override homedir does not take precedence over sss_override
        56629d655  tests: removes legacy multihost test
        515f3a45a  tests: removes legacy test testing tevent C library
        0859296ef  tests: remove tevent_loop.c
        35f71c74f  tests: remove legacy test `test_bz1146198_bz1144011`
        42f7bee1b  tests: add test_ldap__display_password_expiration_warning
        098456c57  tests: remove test_bz748856
        b6645f610  tests: add test_ldap__display_grace_logins_when_password_has_expired
        414dec6bc  tests: remove `test_bz954323`
        a9fffc605  tests: add `test_ldap__authentication_fails_once_password_max_age_is_reached`
        5af5b593b  tests: remove `test_ldap_pasword_policy.py` and `change_user_password_while_expired.sh`

    Philipp Tomsich (7):
        3b277f9c1  SDAP: Parse each attribute of an entry in message order
        c71b7ce33  Tests: Cover sdap_parse_entry() with repeated and irregular entries
        de8db517f  SDAP: Match object class names exactly
        8c4e237dd  SDAP: Reject a DN or attribute description with a zero byte
        3693c919e  SDAP: Cap the precision used to print bervals
        ab0013a1c  SDAP: Compare the class name length before its bytes
        200417497  SDAP: Use the project's comment style in sdap_parse_entry()

    Rakesh Kumar (3):
        56275ac5e  Man: Improvement in max_ccache_size parameter
        41be30b77  Man: Fix krb5_use_fast demand option description
        19bb6ef2c  Fix: Preserve explicitly set 'none' provider values

    Samuel Cabrero (2):
        bae165d31  AD: Initialize data_provider in struct sdap_options
        01ba823fb  SDAP: Warn about ldap_sudo_search_base only if sudo target is enabled

    Scott Poore (9):
        081182ca9  Tests: skip nonposix nested test for older sssd
        faf321ca6  Tests: add ldap_sudo_search_base warning test
        a704abd3c  Tests: multihost ldap to ldaps
        af8316112  Tests: multihost ssh use ip and sssd snippet perms
        410913f6c  Tests: multihost remove stderr redirect
        9eb7f9832  Test: add sssd conf backup to test_0002_1736796
        40bc4a815  Tests: multihost change passwd setting for STIG
        3b084a20d  Tests: multihost ldap password policy fixes
        e3c946b9c  tests: clear sssd cache in teardown of AD idmap range tests

    Shradha Jawale (1):
        b331027e7  man: Fix filter_users_in_groups and pam_gssapi_check_upn options.

    Sumit Bose (13):
        314233a2e  krb5: fix OTP authentication
        f7ed80de3  krb5: restart krb5_child for Smartcard authentication
        fb3e1f5dd  ipa: do not use infinite timeout for certmap lookups
        2192da053  ipa: error out during issues reading IPA configuration
        811b3bf98  nfs idmap: error out if buffer is too small
        f53011b47  test: test nfs idmap plugin id to name functions
        b9b5c448d  ldap: pwd_expire_policy_warn does not overwrite errors
        0e6d8c660  test: pwd_expire_policy_warn does not overwrite errors (IPA)
        8d1c7213b  ldap: show expired message if shadow lastChange is missing or 0
        865b65437  test: pwd_expire_policy_warn does not overwrite errors (LDAP)
        f64bac3d5  krb5: filter AD host principals during TGT validation
        c137b8037  tests: add unit tests for get_validation_principal()
        35297e12d  SDAP: Align sdap_parse_entry() with the coding style

    Tomas Halman (3):
        c0a7e7f20  certmap: check that SID exists in certificate
        8574a7de4  PAM: clear state pointer before freeing state itself
        7a947e657  Treat shadowExpire=0 correctly

    aborah-sudo (6):
        a5f0ba92b  Tests: fix the tests to check the new pattern
        bc48200fb  Tests: Disable test_authentication_indicators
        c87df1ac2  Tests: use client IP instead of sys_hostname for SSH login
        70c7bd025  tests: convert cached_auth_timeout bash tests to system tests
        46712d888  tests: convert multihost failover and connection timeout tests to system tests
        d5aca80b4  tests: convert sudo offline and full_refresh bash tests to system tests

    dependabot[bot] (2):
        33a53cb3a  ci: bump actions/checkout from 6 to 7
        a9144756f  ci: bump actions/setup-python from 6 to 7

    divinehawk (3):
        3070c4efe  pam: add pam_add_response_no_send()
        35d3a3dc8  pam: offer local Smartcard authentication in the JSON message
        a61481b3c  tests: check local Smartcard authentication in the JSON message

    kkz (1):
        8da0898ab  resolv: Fix incorrect variable used in ares_parse_txt_reply() error check

    krishnavema (4):
        716d04ddc   tests: migrate KCM to system tests
        8a0df99c6   tests: adding rewritten journald logging tests
        e2174b212  tests: address review, merge journald identifier tests
        a11663348  tests: add AD smart card certificate authentication test

    sssd-bot (2):
        fd8834552  pot: update pot files
        f0cde37f8  Release sssd-2.9.10

    tong_1001 (2):
        09ffbe1e0  delete useless tmp_ctx variable from pam_dom_forwarder()
        8630c533b  fix potential memory leak

    zhaoshuang (1):
        0859ae52b  Plug memory leak: add missing dbus_message_unref

