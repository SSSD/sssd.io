SSSD 2.14.0-beta2 Release Notes
===============================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

- Added polkit rule to grant the sssd user access to the gnome-remote-desktop
  virtual PC/SC daemon (grd-pcscd), enabling smartcard authentication over RDP
  sessions.
- SSSD now forwards the GDM_AUTH_SESSION_ID environment variable from PAM
  clients to p11_child and krb5_child processes, enabling smartcard
  authentication in remote desktop sessions where PCSC operations must be
  redirected to a remote provider.
- Support of OpenSSL < 3.0.8 was dropped.
- new oidc_child option –client-auth-method to select between authentication
  with client secret, mutual-TLS/mTLS (RFC-8705) and JWT client assertion
  (RFC-7523). For mTLS all key types supported by libcurl can be used. For JWT
  RS256, ES256, ES384 and ES512 with matching key types are supported.
- new oidc_child option –pkcs12-client-creds to specify the path to a PKCS#12
  file with certificate and private key for certificate based authentication.
  Password to unlock the private key can be given with –client-secret or
  –client-secret-stdin options.
- Support of Python2 was dropped.

New features
~~~~~~~~~~~~

- UIDs and GIDs mentioned in the new options filter_uids and filter_gids will
  make SSSD avoid the LDAP search and just say that they don’t exist. They are
  comma-separated lists of simple values or ranges: filter_uids = 0-999, 1234,
  2000-2099
- The NSS responder gained a new SSS_NSS_GETORIGBYUSERNAME_WITH_GROUPS request,
  exposed by ``libsss_nss_idmap``, that returns a user’s original data together
  with its group memberships in a single call. It is intended to be used by the
  FreeIPA extdom plugin. The ``libsss_nss_idmap`` version was bumped accordingly
  (new SSS_NSS_IDMAP_0.8.0 symbol version).
- Active Directory and Entra ID hybrid setups can now use Entra ID for
  authentication while identities come from AD. Setting
  ``idp_auth_user_identifier_attr`` to ``onPremisesImmutableId`` makes
  ``oidc_child`` decode the synchronized AD objectGUID so it matches the UUID
  stored in the SSSD cache.

Important fixes
~~~~~~~~~~~~~~~

- CVE-2026-104041
- CVE-2026-80048
- CVE-2026-104035
- CVE-2026-104048
- CVE-2026-88252
- CVE-2026-104044
- CVE-2026-104042
- CVE-2026-104030
- CVE-2026-104032
- cve-2026-104046
- CVE-2026-104031
- CVE-2026-104037
- CVE-2026-104029
- CVE-2026-104047
- CVE-2026-104045
- CVE-2026-104043
- CVE-2026-104033
- CVE-2026-92821
- CVE-2026-104039
- CVE-2026-104036
- CVE-2026-104038
- CVE-2026-90463
- CVE-2026-90996
- CVE-2026-90994
- CVE-2026-90995
- CVE-2026-90462
- CVE-2026-87853
- CVE-2026-68743
- CVE-2026-68742
- CVE-2026-68744
- CVE-2026-14474
- CVE-2026-14476
- Fixed an issue where SSSD fails to start when DNS is unresponsive.
- SSSD no longer crashes if ``ldap_read_rootdse = never`` and
  ``enumerate = true``

Packaging changes
~~~~~~~~~~~~~~~~~

- New configure option ‘–with-vendordir’ to enable reading the vendor provided
  configuration file.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

- The “gdm-password” service was removed from the default
  pam_p11_allowed_services list, so it is no longer offered Smartcard
  authentication by default. The previous behavior can be restored by adding
  “pam_p11_allowed_services = +gdm-password” to the [pam] section of sssd.conf.
- ‘autofs’ responder now supports ``allowed_uids`` config option that defaults
  to “0”
- New option ``idp_auth_user_identifier_attr`` selects the userinfo or token
  attribute used to identify the authenticated user. It has no default and must
  be set explicitly for AD and Entra ID hybrid deployments. The
  ``idp_userinfo_endpoint`` has to request the attribute with ``$select``.
- New section [prompting/cert_auth] with the new options ‘pin_prompt’,
  ‘keypad_prompt’ and ‘user_name_hint’.

Tickets Fixed
-------------

* `#3835 <https://github.com/SSSD/sssd/issues/3835>`__ - [RFE] Provide interface which returns group-memberships by name for a given user
* `#4658 <https://github.com/SSSD/sssd/issues/4658>`__ - memory leak in sssd_nss
* `#5129 <https://github.com/SSSD/sssd/issues/5129>`__ - id_provider = proxy proxy_lib_name = files returns * in password field, breaking PAM authentication
* `#5371 <https://github.com/SSSD/sssd/issues/5371>`__ - Pinpad card reader for login authentication yet you are asked also enter pin on pc keyboard
* `#5898 <https://github.com/SSSD/sssd/issues/5898>`__ - Improve the 'sssctl analyze' help output
* `#7289 <https://github.com/SSSD/sssd/issues/7289>`__ - [rule/allows_nss_options]: Attribute 'offline_timeout_random_offset' is not allowed in section 'nss'. Check for typos
* `#7323 <https://github.com/SSSD/sssd/issues/7323>`__ - pam_initgroups_scheme: no value type in heading description
* `#7324 <https://github.com/SSSD/sssd/issues/7324>`__ - pam_gssapi_services: no value type in heading description
* `#7325 <https://github.com/SSSD/sssd/issues/7325>`__ - pam_gssapi_check_upn: no value type in heading description
* `#7326 <https://github.com/SSSD/sssd/issues/7326>`__ - pam_gssapi_indicators_map: no value type in heading description
* `#7335 <https://github.com/SSSD/sssd/issues/7335>`__ - sssd.conf(5): id_provider : no default mentioned
* `#7336 <https://github.com/SSSD/sssd/issues/7336>`__ - sssd.conf(5): selinux_provider: "Use the value of `id_provider`, if set and can handle SELinux loading requests". What happens if it cannot handle loading requests?
* `#7339 <https://github.com/SSSD/sssd/issues/7339>`__ - sssd.conf(5): "Please see the section “FAILOVER” for more information about the service resolution." No such section "FAILOVER"
* `#7340 <https://github.com/SSSD/sssd/issues/7340>`__ - sssd.conf(8): dns_resolver_server_timeout: "Defines the amount of time (in milliseconds) SSSD would try to talk to DNS server before trying next DNS server." Ambiguous wording
* `#7341 <https://github.com/SSSD/sssd/issues/7341>`__ - sssd.conf(5): override_gid: "Override the primary GID value with the one specified." Ambiguous wording, no mention of default
* `#7345 <https://github.com/SSSD/sssd/issues/7345>`__ - sssd.conf(8): FILE FORMAT: Are parameter values case sensivite? is TRUE == true?
* `#7351 <https://github.com/SSSD/sssd/issues/7351>`__ - sssd.conf(5): cached_auth_timeout: ambiguous explanation
* `#7380 <https://github.com/SSSD/sssd/issues/7380>`__ - sssd.conf: session recording: no mention of [session_recording] heading 
* `#7899 <https://github.com/SSSD/sssd/issues/7899>`__ - Map certificate to multiple users in Active Directory when using GNOME GUI - Login error
* `#8574 <https://github.com/SSSD/sssd/issues/8574>`__ - oidc_child: AD+Entra hybrid authentication fails with UUID mismatch when using id_provider=ad and auth_provider=idp
* `#8705 <https://github.com/SSSD/sssd/issues/8705>`__ - SetuptoolsDeprecationWarning: setup.py install is deprecated.
* `#8718 <https://github.com/SSSD/sssd/issues/8718>`__ - 'sssctl analyze --help' shows incorrect command 'sss_analyze' in usage field
* `#8796 <https://github.com/SSSD/sssd/issues/8796>`__ - Use-after-free crash in PAM responder during YubiKey / PKCS#11 authentication
* `#8803 <https://github.com/SSSD/sssd/issues/8803>`__ - sssd 2.13.1 FTBFS oidc
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

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.13.0..2.14.0-beta2

    Abhinay Reddy Peddireddy (1):
        2cfcedaa2  Man: fix sss_obfuscate(8) domain option and synopsis
    
    Akash Sundarkar (1):
        a613ba39f  man: fix SEE ALSO punctuation after pam_sss
    
    Akshay Sakure (34):
        30a4940f5  Component: sssd-tools
        5b6c11d50  sssd man-page: Improve man-page for override_gid
        c183ecbd2  sssd man-page: Fix man-page for offline_timeout*
        817b00258  sssd man-page: Add reference to FAILOVER section
        0c3c833ce  sssd man-page: Add missing data type in man-page
        0f774ac5a  man: Remove obsolete RHEL 5 krb5.conf note from sssd-ad
        6042cc78d  sssd man-page: Add headings [] for all services
        e98665e6a  man: Remove obsolete RHEL 5 krb5.conf note from sssd-ipa
        49b9b9331  man: Replace ipa_hbac_selinux -> ipa_selinux_refresh in sssd-ipa
        8ceca0ecc  man: Replace 'bool' by 'boolean' in sssd-ipa
        731246d93  sssd man-page: Add Default for id_provider
        abbf3d311  Config: Allow description parameter in [session_recording] section
        76d708af6  Man: Add note about debug* options for [session_recording] in sssd.conf
        51877b78e  sssd man-page: Improve FILE FORMAT section
        a4b91e434  man: Replace ldap_opt_timout -> ldap_opt_timeout
        037a32471  man: Add Default for vetoed_shells in sssd.conf(5)
        abe187dce  man: Replace bool -> boolean across sssd man-pages
        bd2fcb64c  man: Correct typos in sssd.conf(5) man-page
        571cbe60f  man: Correct default for ldap_user_nds_login* options
        3e6f6691e  man: Correct default for ldap_host_object_class option
        dbacad96f  man: Remove duplicate sentence from intro sssd-kcm(8)
        a8f5e9d41  man: Correction of typo in pam_sss(8)
        4f992249a  sssd.conf man: Improve explanation for cached_auth_timeout
        71d4fbc35  man: Correct the ports for ad_use_ldaps option
        e817d4c68  man: Improvement in desc for smart refresh in sssd-sudo
        90fd02816  man: Improve description for dns_resolver_server_timeout
        78ea2f0f6  Remove obsolete entry_cache_computer_timeout option
        1f5ace4d7  Fix: Remove an orphaned include local.xml
        5d1a759e7  Man: Remove note about obsolete option ipa_dyndns_iface
        7b1f75e51  Man: Improve description for dyndns_refresh_interval
        15541998f  Man: Remove empty <para></para> from sssd-ad.5.xml
        d351ef4a5  Man: Correct the minor typo in sssd-ad.5.xml
        193f7d0b1  Man: Improve description for selinux_provider option
        e80d33de5  sssctl: Improve the 'sssctl analyze' help output
    
    Alejandro López (1):
        0b2632bdb  NSS: Add options to exclude UID and GID
    
    Alexey Tikhonov (57):
        958a18617  IPA: memory leak fixed
        b070171e8  KRB5: read keytab copy in offline mode too
        35d24a4cf  ipa: fix memory leak in ipa_s2n_get_list iteration
        5e25d395e  ipa: free stale attrs in `ipa_s2n_get_list()` iteration
        6a3698787  build: replace deprecated setup.py with direct file installation
        622fa7f7b  Get rid of Python2 support
        b84e7fa85  sdap: defer libldap global options setup to first connection
        9adeb2734  Makefile: krb5 plugins: don't export internal symbols
        b6e7f0518  RESOLV: handle empty addr list properly
        eedf37aae  build: require OpenSSL >= 3.0.8
        ebcb72ac2  p11_child: replace deprecated OpenSSL 1.0 API calls
        86e1f0195  passkey_child: drop OpenSSL < 3.0 compatibility shim
        fd996b764  certmap: drop OpenSSL < 3.0 digest API compatibility macros
        051053c0d  cert: drop OpenSSL < 3.0 EC and RSA key extraction code
        5cf1074ea  certmap: drop pre-3.0 x400Address ASN1_TYPE code path
        ac48b23d9  cert: replace deprecated `EVP_PKEY_base_id()`
        685909f42  certmap: sanity check in `get_x400address_data()`
        b7d7f3e32  cert: avoid using static local variables
        f4062b643  Remove usage of `CRYPTO_cleanup_all_ex_data()`
        87fc5478c  passkey_child: remove duplicate includes
        645a43125  certmap: remove unused `ASN1_TYPE_unpack_sequence()`
        7ae2bdd37  p11_child: fix wrong check for failing `OCSP_response_get1_basic()`
        6506858fc  Make: don't compile 'oidc_child_get_jwk.c'
        fa7a55949  PAM: fix use-after-free during p11_child processing
        27651161b  cfg_rules: allow ldap_sasl_authid/ldap_krb5_keytab/krb5_keytab
        46726af9d  ci: harden pull_request_target workflows against pwn requests
        b04d2fef0  ci: drop 'analyze-target.yml'
        ba207eab7  gpo: reject path traversal in gPCFileSysPath
        ff8c1b19b  sudo: warn when ldap_sudo_search_base falls back to root DN
        b58482fdd  CI: don't specify 'push:'/'pull_request:' branches
        6ffc60137  CI: add retry logic to Bodhi API calls in get-matrix.py
        f5be5002a  NSS: fix initgroups packet heap disclosure
        2839e8ccf  nss: validate addrlen in sss_nss_protocol_parse_addr()
        bef9d1261  pam: validate auth_token_length in extract_authtok_v1()
        16882cd5d  sudo: don't warn about search base when it was set by provider
        e1e171d8f  pam_sss: cast to GdmPamExtensionMessage in binary prompt macro
        f3a324918  IDP: fix user matching in `eval_access_token_buf()`
        42db41215  LDAP: fix fail-open in ppolicy access check on zero results
        00b51c155  PAM: avoid NULL deref when service item is missing
        8dbdcf998  PAM: fix out-of-bounds read in v1 request parser
        72b45d1c8  SYSDB: sanitize SID string in `sysdb_search_entry_by_sid_str()`
        c7f1b8a3d  NSS: reject empty request body before body[blen - 1] access
        79821dc9a  NSS: factor request body validation into a helper
        e83a030e3  NSS: bound service parser reads to the request body length
        a27f5da15  SPEC: 'sssd-idp' requires 'libsss_idmap'
        f069803fd  autofs: fix out-of-bounds reads in request parsers
        7b50db503  autofs: free per-request context on successful replies
        5d127f22a  autofs: add 'allowed_uids' option to the autofs responder
        152bf19eb  NSS: factor out group resolution code
        838aa796b  NSS: guard against NULL domain in initgroups group resolver
        f1962aa1d  NSS: fixed leaking `tmp_ctx`
        7e1d12a27  NSS: fixed leaking `cmd_ctx`
        ecdb5909d  NSS: add SSS_NSS_GETORIGBYUSERNAME_WITH_GROUPS command
        d606a8c0a  TESTS: cmocka: new 'SSS_NSS_GETORIGBYUSERNAME_WITH_GROUPS' test
        9485f68f1  RESPONDER SBUS: get rid of `-sss_resp_reset_ncache_*`
        55b35d47c  negcache: replace selective resets with a single recreate helper
        5b54a9cb3  negcache: limit max mem size consumed by negative cache
    
    Dan Lavu (30):
        8f170d08a  refactoring ipa tests for hostname framework changes.
        e5b407ccd  tests: fixing mypy linting errors
        2ca8395d7  tests: updating pysss_nss_idmap error with more detail
        72b30514e  tests: fixing authselect teardown order
        3a426b8b8  tests: improving offline authentication tests
        d7804880f  tests: parametrizing group lookup by names test
        628b2d6f1  tests: removing multihost tests that have been rewritten
        8c6fcf1c8  Revert "tests: removing multihost tests that have been rewritten"
        cf19b165c  Revert "tests: parametrizing group lookup by names test"
        6e0cb656e  tests: adding rewritten dynamic dns tests
        83cf5786a  removing old multihost dyndns tests
        2373a46f9  KCM: fix use-after-free of ccache name during TGT renewal
        854dcda45  KCM: free auth_data on TGT renewal setup failure
        3efe24807  tests: widen KCM TGT renewal poll window
        a9112d2a0  tests: remove multihost/alltests/test_sudo.py
        5cc2c3bec  tests: remove multihost/alltests/test_sss_cache.py
        bf174cabd  tests: remove multihost/ad/test_sudo.py
        c731a532e  tests: remove multihost/alltests/test_sssctl_analyzer.py
        a074d5a22  tests: remove multihost/alltests/test_autoprivategroup.py
        d8be988b0  tests: remove multihost/alltests/test_rfc2307.py
        1e18d9d29  tests: adding gpo test case for traversal bug
        cb758f1f8  tests: add GPO regression tests for local group collision and verbose Samba logging
        2d2dafdda  test rewrite: legacy intg test_pam_responder.py - first batch
        3e43f26d9  test(smartcard): use client.auth.su.vlock_smartcard() in vlock test
        43540d3ff  test rewrite: legacy intg test_pam_responder.py - remaining batch
        c94c57a29  Skipping test_smartcard__certificate_owner_resolved_with_two_tokens_and_missing_name test
        cbdb054a1  tests: remove legacy intg test suite
        5ce9d9ed9  CI: trim unused deps.sh/distro.sh helpers, rename matrix key, fix keytab leak
        056c2e71f  CI: drop Debian as a build target
        ba468b8ae  tests: collapse su/ssh parametrization in test_gpo.py
    
    Ezri Zhu (2):
        abfc37bf5  get_json_string_array_by_id_list: take base_url as parameter
        5cb6eb2ec  get_json_string_array_by_id_list: batch lookups with getByIds
    
    Gleb Popov (4):
        17fe0f7d7  FreeBSD CI: Stop installing Python setuptools as a dependency
        a6915134a  FreeBSD CI: Explicitly pass --datadir and --sysconfdir to configure
        35b38806f  FreeBSD CI: Do not reference an unset LOCALBASE variable
        df5a5649b  FreeBSD CI: Switch to 15.1-RELEASE
    
    Harsh Bhadauriya (2):
        0aba18586  man: fix doubled "are" in sssd-ldap(5)
        f399fc14f  man: fix YOUR-CLIENT-SCERET typo in sssd-idp(5)
    
    Hosted Weblate (3):
        73470fdb5  po: update translations
        0f58c33f4  Update translation files
        28eb873c9  po: update translations
    
    Iker Pedrosa (5):
        d54cf526c  tests: add TMT plan for passkey testing
        210f50f50  ci: add TMT passkey tests to packit workflow
        334449b9d  ci: fix error handling in passkey TMT plan SSH commands
        167b5a9c9  ci: use hardware.memory syntax for TMT passkey tests
        943ecbb36  ci: update passkey TMT plan for native CentOS Stream 10 execution
    
    Jakub Vávra (13):
        1b802f4cb  Tests: Fix test_refresh_contain_timestamp
        9df13ca25  Tests: Update LdapOperations to fail on bind immediately
        d02bdba92  Tests: Update test_nss_user_login_with_overriding_home_directory
        14eaad116  Tests: Auto skip tests dependent on ldbsearch when unavailable
        03a99dc0c  Tests: Switch tests using ldap adparameters ported to ldifde
        c8ae1da83  tests: Update ds tests to rely less on hostname
        e7c9de672  tests: Fix regex warnings
        732279cb4  ci: Swap flake and isort for ruff and reorder jobs
        e047064a1  tests: Fix test used in c-ares gating to be more resilient
        16a338155  ci: Fix duplicated python-system-tests in static-code-analysis
        d052df099  tests: Fix E713 [*] Test for membership should be `not in`
        be221ad82  tests: add AD forest multidomain system tests
        c611c7818  tests: Align AD forest test names and grouping
    
    Joan Torres Lopez (6):
        9a4833c15  pam: guard GDM JSON response free against NULL pointer
        f2696b80a  pam: Forward GDM_AUTH_SESSION_ID from PAM client to child processes
        b1f2ffc7d  polkit: Add rule for gnome-remote-desktop pcscd access
        56addc8f9  PAM: Stop treating gdm-password as a Smartcard-capable service
        8333265f7  PAM: Move PKCS11_LOGIN_TOKEN_NAME export out of add_pam_cert_response()
        46c017ac6  TESTS: cmocka: new 'test_pam_cert_auth_gdm_smartcard' test
    
    Justin Stephenson (13):
        21674dd96  tests: Clarify approx match filter
        d145b19db  ci: Clear cache before installing built rpms
        c64f9f5bb  ci: Remove dnf workaround during rpm install
        75df4f574  ci: Dont run system tests for man page only PRs
        7d0fe067a  dp: Return only a single error code through sssd.dataprovider interfaces
        ada5e6f26  sdap: Remove unused value error code assignment
        df9116178  nss: guard against length underflow in packet
        3dbcfe345  autofs: avoid leaked enumeration contexts after map
        7227f9130  authtok: add length to unpack passkey blob
        115e74514  pam: guard against zero-length string auth tokens
        ed02f9d35  pam: prevent null dereference in kerberos passkey flow
        271ca7ab3  authtok: Make sss_auth_unpack_passkey_blob static
        aee4b51b1  util: Use remaining size instead of full size
    
    Kaushik Banerjee (1):
        359c0716f  man: krb5_ccachedir is no longer created by SSSD
    
    Madhuri Upadhye (18):
        32dedfbf8  tests: mark KCM TGT renewal test as flaky
        20eeac6e2  Tests:  LDAP+KRB5 krb_misc tests
        233db39fc  tests: poll for KCM TGT renewal instead of fixed sleep
        c6deebc4f  Tests: fix GSSAPI SSH test setup for krb5_confd_path
        20798e7d7  tests: port force-LDAPS coverage to system tests
        6dd9bf262  Tests: Fix AD work on STIG-hardened systems
        5340857a1  Tests: Fix AD tests on STIG-hardened systems
        bf003fcaa  Fix STIG fixture to handle sshd drop-in config files
        cf3873782  Enable AES Kerberos encryption on AD for FIPS:STIG compatibility
        60c20e109  tests: add sudo search base warning suppression test
        b1acbd80b  fix(docs): repair malformed quote tag in Spanish sssd-ifp.5 translation
        ea5c387f9  tests: convert bash ldap service_map suite to system tests
        5cc59cf8a  tests: cover sssctl debug-level when SSSD is stopped and for PAC
        f7abb7c97  tests: wait for DNS resolve failure before checking logs
        0d1754dcf  tests: remove multihost tests already converted to system tests
        b1c984a59  tests: drop unused converted pytest marker from multihost
        0b3557017  tests: fix false positive journal check for ldap_sudo_search_base warning
        2698990f9  tests: apply journal stdout check to sudo_provider=none case
    
    Martin Vogt (1):
        83b95ee99  Enable file caching in OpenSC by exporting XDG_CACHE_HOME. Add note in sssd.conf.5 about filecaching support in OpenSC and SSSD and how to turn it of in opensc.conf.
    
    Masahiro Matsuya (3):
        319f8185f  cfg_rules: add pwfield to allowed_domain_options
        e3f869d7a  man: document pwfield per-domain usage in NSS section
        3efabe8aa  test_kcm: use config_apply instead of start to avoid proxy domain auth issue
    
    OpenCode Agent (1):
        2708454a6  oidc_child: support Entra onPremisesImmutableId identifiers
    
    Pavel Březina (44):
        4272a6460  scripts: fix release notes generation
        40f3a62a7  release: install jq as needed dependency
        77941322c  Update version in version.m4 to track the next release
        c5b631ee6  sdap: let callers mark SSSD as offline if kinit fails
        4df8758e6  release: use version instead of HEAD as the target commit
        b14cd28ad  release: compute previous version automatically
        bb89d86b9  release: create stable branch and backport label for master releases
        2578e1adb  release: add create-stable-branch parameter
        add87d48b  release: fix hardcoded origin in git fetch
        aa119f6a6  release: add tip about suggesting changes in release notes PR
        9266fb8d3  release: move release notes generation before any push
        9b15bc549  release: make sure to fetch all tags
        dd58a9b42  release: use GH_TOKEN variable for release notes
        2cc7dfa18  sdap: handle missing rootDSE gracefully
        3324e56a5  scripts: correctly authenticate git commands
        df13bd95f  ci: serialize make distcheck in build.yml
        dda8a5a93  ci: actually run the whitespace test
        d7b3b996a  tests: fix whitespace_test for files missing newline at eof
        fc740af93  ci: use ubuntu-26-04 runner to workaroud issues on ubuntu-24-04
        bb787e0de  tests: fix test_ldap_krb5__keytab_selects_correct_principal_with_multiple_realms
        a5fbabfe3  nss: fix potential memory leak if packet grow fails
        4aed64dea  krb5_locator: make input buf const
        7383252f0  krb5: add env vars to override kdcinfo addresses
        ea6d518ee  child_handlers: add extra_env parameter to exec_child_ex
        c73384d69  child_handlers: propagate extra_env parameter to sss_child_start
        c7b896b99  sdap_get_tgt_send: take kdc_address as parameter
        e5d8d0fe3  tests: fix ASan crash in test_schedule_get_domains_task
        3ceacfc24  ldap: fix unused state
        639f0b45c  remove mem_ctx from get_subdomains_recv
        101446fe2  release: do not auto-create stable branch for pre-releases
        323c2a142  release: mark GitHub release as pre-release for pre-release versions
        33378a993  test: fix missing cmocka prerequisite includes in test_nfsidmap.c
        30501ce4c  oidc_child: escape single quotes in Entra ID OData filters
        5f7d6bbd9  tests: automatically collect coredumps
        fe619fc46  ci: move system tests from Github Actions to Testing Farm
        d76af0f55  ci: add polarion metadata check to static analyzers
        a44d7358b  responder: back off accept() on fd exhaustion to stop busy-spin
        b7234202f  ipa: compare users with domain awareness against HBAC rules
        9f08547a2  kcm: prune per-connection credential cache on destroy
        d5f68d903  KCM: set the client fd non-blocking to avoid event-loop hangs
        2c8f6382c  KCM: allocate body buffer only once
        4a7e9ac4a  KCM: reject request bodies smaller than the protocol header
        0721b661f  KCM: add kcm_recv_timeout to avoid stuck requests
        b8d0f29f8  ci: remove sssd db prior restarting it on ipa container
    
    Peter Šišan (12):
        3fc553ccb  tests: adds sss_override takes precedence over override homedir
        be8795bd3  tests: adds override homedir does not take precedence over sss_override
        9a4a04f21  tests: removes legacy multihost test
        13e33be28  tests: removes legacy test testing tevent C library
        f4a03dfc2  tests: remove tevent_loop.c
        f0dcd01c2  tests: remove legacy test `test_bz1146198_bz1144011`
        b04d5e32f  tests: add test_ldap__display_password_expiration_warning
        2b4fea8ce  tests: remove test_bz748856
        0bf3904e7  tests: add test_ldap__display_grace_logins_when_password_has_expired
        a0e15e01c  tests: remove `test_bz954323`
        099874721  tests: add `test_ldap__authentication_fails_once_password_max_age_is_reached`
        46c4ce17c  tests: remove `test_ldap_pasword_policy.py` and `change_user_password_while_expired.sh`
    
    Philipp Tomsich (1):
        4195e0edd  ci: Install libssh-devel for the passkey TMT plan
    
    Rakesh Kumar (4):
        c0f53bc9b  Man: Improvement in max_ccache_size parameter
        aab54c1b9  Man: Fix krb5_use_fast demand option description
        86d81c108  Fix: Preserve explicitly set 'none' provider values
        53e7c5858  Fix ldap_use_ppolicy name in LDAP ppolicy test docstring
    
    Renan Rodrigo (1):
        f0d41ac22  Fix FTBFS with GDM 51 PAM extension headers
    
    Samuel Cabrero (7):
        8df514eaf  sssctl: Add missing new line
        1d1b73558  confdb: Add UsrEtc support
        b955a2395  doc: Document the config file hierarchy when vendor dir is enabled
        aac3f007a  SYSTEMD: Add vendor provided configuration file as a triggering condition
        edf4a0f9b  sdap: Reduce log level when get_naming_context() fails
        db3ca0ec4  AD: Initialize data_provider in struct sdap_options
        972f78e1b  SDAP: Warn about ldap_sudo_search_base only if sudo target is enabled
    
    Scott Poore (11):
        b59de87a8  Tests: Adding flaky marker to retry GDM critical
        5a61d3e77  Tests: skip nonposix nested test for older sssd
        4b915fcbd  Tests: add ldap_sudo_search_base warning test
        dbeed82c2  Tests: multihost ldap to ldaps
        1f921d48d  Tests: multihost ssh use ip and sssd snippet perms
        a6d78a796  Tests: multihost remove stderr redirect
        425421c86  Test: add sssd conf backup to test_0002_1736796
        18a990218  Tests: multihost change passwd setting for STIG
        1ca4a82a4  Tests: multihost passwd change remove comments
        282077579  Tests: multihost ldap password policy fixes
        493e37fe5  tests: clear sssd cache in teardown of AD idmap range tests
    
    Shradha Jawale (1):
        a7ffa5a56  man: Fix filter_users_in_groups and pam_gssapi_check_upn options.
    
    Simo Sorce (3):
        ab6713f78  Correct x400Address type check in crypto.m4
        b197d9d3f  Update certmap for OpenSSL 4.0 compatibility
        770ae6cb0  Add const qualifier to X509_NAME pointers
    
    Sumit Bose (28):
        f3a36bec2  krb5: restart krb5_child for Smartcard authentication
        d6483bb5c  p11_child: ignore failure of C_GetTokenInfo
        016bc7a2a  pam: handle protected authentication path
        f3aea6728  authtok: remove sss_authtok_set_sc_keypad()
        084268fc2  pam_sss: fix potential memory leak
        50a38380e  pam: refactor pack_cert_data
        810038113  crypto: add get_jwk_from_pkcs12()
        ec078ea0e  oidc_child: add pkcs12-client-creds option
        6577434c7  oidc_child: add JWT authentication
        9a3487d75  test: add tests for oidc_child 'get-device-code'
        f72a7a69d  oidc_child: remove potential double-free in JSON code
        44cd06ba7  oisc_child: add missing NULL checks
        c2f9fff0c  oidc_child: clarify why a value isn't copied
        10bad8b1d  oidc_child: change default with no auth method
        3a7170b96  SECURITY.md: add initial template
        c720d02a6  SECURITY.md: add SSSD specific information
        0684b61e7  p11_child: use X509_STORE_get1_objects() is available
        11ba589f6  pam: add cert_auth prompting options
        415a4b480  ipa: do not use infinite timeout for certmap lookups
        ae43f1f33  ipa: error out during issues reading IPA configuration
        671d22410  nfs idmap: error out if buffer is too small
        e29bb9220  test: test nfs idmap plugin id to name functions
        e83a29cea  ldap: pwd_expire_policy_warn does not overwrite errors
        57d68184a  test: pwd_expire_policy_warn does not overwrite errors (IPA)
        1a258a48f  ldap: show expired message if shadow lastChange is missing or 0
        aaaea88b6  test: pwd_expire_policy_warn does not overwrite errors (LDAP)
        ef63462f3  krb5: filter AD host principals during TGT validation
        64c46aa79  tests: add unit tests for get_validation_principal()
    
    Tomas Halman (4):
        db521e9e3  certmap: check that SID exists in certificate
        f3e65b06c  PAM: clear state pointer before freeing state itself
        69fde641a  Treat shadowExpire=0 correctly
        7c1cbce7a  IDP: Clean old items from open_request_table
    
    Vincent Wilms (1):
        addb8c93b  pam: keep preauth indicator for socket activation
    
    aborah-sudo (10):
        04d593755  Tests: fix the tests to check the new pattern
        c20c27003  Tests: Disable test_authentication_indicators
        2f8fc072d  Tests: use client IP instead of sys_hostname for SSH login
        ad0e9f6f5  Tests: add socket activation tests for all-responder and sudo scenarios
        0c68df15e  tests: convert cached_auth_timeout bash tests to system tests
        0f15e0624  tests: convert multihost failover and connection timeout tests to system tests
        bab9ac4de  tests: convert sudo offline and full_refresh bash tests to system tests
        d192273e1  tests: convert offline auth bash tests to system tests
        3aceab178  Tests: Convert ldap failover uri list bash tests to system tests
        c496977d1  Tests: Convert remaining single-server ldap failover bash tests
    
    dependabot[bot] (7):
        fa413a969  ci: bump cross-platform-actions/action from 0.32.0 to 1.0.0
        9dfd78c7c  ci: bump cross-platform-actions/action from 1.0.0 to 1.2.0
        750457f83  ci: bump cross-platform-actions/action from 1.2.0 to 1.3.0
        0ac0e28de  ci: bump actions/checkout from 6 to 7
        f2de43262  ci: bump actions/setup-python from 6 to 7
        f1e86f0a9  ci: bump cross-platform-actions/action from 1.3.0 to 1.5.0
        020a517a3  ci: bump vapier/coverity-scan-action from 1.8.0 to 1.9.0
    
    divinehawk (3):
        55d415e44  pam: add pam_add_response_no_send()
        bf006997f  pam: offer local Smartcard authentication in the JSON message
        bef12aa35  tests: check local Smartcard authentication in the JSON message
    
    hagaikwa-redhat (1):
        9238b410e  man: fix TENNANT-ID typo in sssd-idp(5) example
    
    kkz (3):
        4a800e56a  resolv: Fix incorrect variable used in ares_parse_txt_reply() error check
        57dfda6bd  oidc_child: Fix logic error in Keycloak lookup
        3eaaefc03  krb5: Fix logic errors in OAuth2 code verification
    
    krishnavema (12):
        e5b65979f  tests: implement multi-token support for smart card authentication
        47f67f025  Add default timeout handling for soft_ocsp and regression tests for smart card authentication (resolves: RHEL-5043)
        11817a6d1   Tests: Smart card authentication tests for SSSD's CKF_PROTECTED_AUTHENTICATION_PATH (hardware pinpad) support
        9f4cdb5e6  test: Add smart card unlock console test with vlock
        360376d19   tests: migrate KCM to system tests
        d7254d1a5  tests: migrate multihost/ad/test_automount.py to system tests
        ec98b1cce  tests: remove multihost/ad/test_automount.py
        6a3b2b593   tests: adding rewritten journald logging tests
        f3fa53395  tests: address review, merge journald identifier tests
        4cda93cf6  tests: migrate multihost/alltests/test_default_debug_level.py
        1257a7bef  tests: add autofs test for default autofs_provider behavior
        ebc266470  tests: add AD smart card certificate authentication test
    
    sssd-bot (4):
        78c7e42c6  pot: update pot files
        a2d842d34  Release sssd-2.14.0-beta1
        b25aae8e9  pot: update pot files
        8810f8323  Release sssd-2.14.0-beta2
    
    tong_1001 (2):
        00a7620ff  delete useless tmp_ctx variable from pam_dom_forwarder()
        043de0435  fix potential memory leak
    
    zhaoshuang (1):
        e3a7a4dd4  Plug memory leak: add missing dbus_message_unref

