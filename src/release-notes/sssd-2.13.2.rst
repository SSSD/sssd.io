SSSD 2.13.2 Release Notes
=========================

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

New features
~~~~~~~~~~~~

- UIDs and GIDs mentioned in the new options filter_uids and filter_gids will
  make SSSD avoid the LDAP search and just say that they don’t exist. They are
  comma-separated lists of simple values or ranges: filter_uids = 0-999, 1234,
  2000-2099

Important fixes
~~~~~~~~~~~~~~~

- PAM pre-auth indicator persisted under socket activation — previously it was
  removed when a socket-activated PAM responder exited on idle, silently disabling
  Smartcard/passkey/configured prompting until restart.
- Fixed 32-bit integer overflow in Kerberos/KCM timestamp handling. Kerberos
  timestamps are now treated as unsigned 32-bit values, correcting credential-cache
  and ticket expiry/renewal calculations for dates after January 2038.

- `CVE-2026-104041 <https://nvd.nist.gov/vuln/detail/cve-2026-104041>`_
- `CVE-2026-80048 <https://nvd.nist.gov/vuln/detail/cve-2026-80048>`_
- `CVE-2026-104048 <https://nvd.nist.gov/vuln/detail/cve-2026-104048>`_
- `CVE-2026-104035 <https://nvd.nist.gov/vuln/detail/cve-2026-104035>`_
- `CVE-2026-88252 <https://nvd.nist.gov/vuln/detail/cve-2026-88252>`_
- `CVE-2026-104044 <https://nvd.nist.gov/vuln/detail/cve-2026-104044>`_
- `CVE-2026-104042 <https://nvd.nist.gov/vuln/detail/cve-2026-104042>`_
- `CVE-2026-104030 <https://nvd.nist.gov/vuln/detail/cve-2026-104030>`_
- `CVE-2026-104046 <https://nvd.nist.gov/vuln/detail/cve-2026-104046>`_
- `CVE-2026-104032 <https://nvd.nist.gov/vuln/detail/cve-2026-104032>`_
- `CVE-2026-104047 <https://nvd.nist.gov/vuln/detail/cve-2026-104047>`_
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
- `CVE-2026-87853 <https://nvd.nist.gov/vuln/detail/cve-2026-87853>`_
- `CVE-2026-68742 <https://nvd.nist.gov/vuln/detail/cve-2026-68742>`_
- `CVE-2026-68743 <https://nvd.nist.gov/vuln/detail/cve-2026-68743>`_
- `CVE-2026-68744 <https://nvd.nist.gov/vuln/detail/cve-2026-68744>`_
- `CVE-2026-14474 <https://nvd.nist.gov/vuln/detail/cve-2026-14474>`_
- `CVE-2026-14476 <https://nvd.nist.gov/vuln/detail/cve-2026-14476>`_
- `CVE-2026-12610 <https://nvd.nist.gov/vuln/detail/cve-2026-12610>`_

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

- The “gdm-password” service was removed from the default
  pam_p11_allowed_services list, so it is no longer offered Smartcard
  authentication by default. The previous behavior can be restored by adding
  “pam_p11_allowed_services = +gdm-password” to the [pam] section of sssd.conf.
- ‘autofs’ responder now supports ``allowed_uids`` config option that defaults
  to “0”

Tickets Fixed
-------------

* `#4658 <https://github.com/SSSD/sssd/issues/4658>`__ - memory leak in sssd_nss
* `#5129 <https://github.com/SSSD/sssd/issues/5129>`__ - id_provider = proxy proxy_lib_name = files returns * in password field, breaking PAM authentication
* `#5898 <https://github.com/SSSD/sssd/issues/5898>`__ - Improve the 'sssctl analyze' help output
* `#7336 <https://github.com/SSSD/sssd/issues/7336>`__ - sssd.conf(5): selinux_provider: "Use the value of `id_provider`, if set and can handle SELinux loading requests". What happens if it cannot handle loading requests?
* `#7339 <https://github.com/SSSD/sssd/issues/7339>`__ - sssd.conf(5): "Please see the section “FAILOVER” for more information about the service resolution." No such section "FAILOVER"
* `#7345 <https://github.com/SSSD/sssd/issues/7345>`__ - sssd.conf(8): FILE FORMAT: Are parameter values case sensivite? is TRUE == true?
* `#7380 <https://github.com/SSSD/sssd/issues/7380>`__ - sssd.conf: session recording: no mention of [session_recording] heading
* `#8796 <https://github.com/SSSD/sssd/issues/8796>`__ - Use-after-free crash in PAM responder during YubiKey / PKCS#11 authentication
* `#8803 <https://github.com/SSSD/sssd/issues/8803>`__ - sssd 2.13.1 FTBFS oidc
* `#8821 <https://github.com/SSSD/sssd/issues/8821>`__ - Contradictory statement in sssd.conf man-page w.r.t. session_recording
* `#8823 <https://github.com/SSSD/sssd/issues/8823>`__ - Incorrect option ipa_hbac_selinux is documented in sssd-ipa man-page
* `#8829 <https://github.com/SSSD/sssd/issues/8829>`__ - sssd man-pages inconsistent about bool/boolean usage
* `#8914 <https://github.com/SSSD/sssd/issues/8914>`__ - Incorrect Default defined for ldap_user_nds_login_expiration_time option in sssd-ldap-attributes(5) man
* `#8916 <https://github.com/SSSD/sssd/issues/8916>`__ - Incorrect Default defined for ldap_host_object_class option in sssd-ldap-attributes(5) man
* `#9030 <https://github.com/SSSD/sssd/issues/9030>`__ - Possibly spurious warning about ldap_sudo_search_base
* `#9197 <https://github.com/SSSD/sssd/issues/9197>`__ - 'local' provider is removed from sssd but an orphaned include/local.xml file is present
* `#9317 <https://github.com/SSSD/sssd/issues/9317>`__ - LDAP/StartTLS: transient TLS handshake failure on an expiring connection marks the backend offline instead of reconnecting
* `#9367 <https://github.com/SSSD/sssd/issues/9367>`__ - pam: GDM switchable authentication never offers local Smartcard authentication

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.13.1..2.13.2

    Abhinay Reddy Peddireddy (1):
        5804e02c6  Man: fix sss_obfuscate(8) domain option and synopsis

    Akash Sundarkar (1):
        49e9c7cfd  man: fix SEE ALSO punctuation after pam_sss

    Akshay Sakure (21):
        fcb426ee5  sssd man-page: Add reference to FAILOVER section
        a7a308c34  sssd man-page: Improve FILE FORMAT section
        fb0365022  man: Replace ldap_opt_timout -> ldap_opt_timeout
        57f473339  man: Replace bool -> boolean across sssd man-pages
        f52555764  man: Add Default for vetoed_shells in sssd.conf(5)
        e0896f761  man: Correct default for ldap_user_nds_login* options
        8762de980  man: Correct default for ldap_host_object_class option
        3bdaf755d  Remove obsolete entry_cache_computer_timeout option
        8afefae77  Man: Remove note about obsolete option ipa_dyndns_iface
        c93208f4c  Man: Improve description for dyndns_refresh_interval
        308dcd38d  Man: Remove empty <para></para> from sssd-ad.5.xml
        48e15bac3  Man: Correct the minor typo in sssd-ad.5.xml
        79e08404e  Man: Improve description for selinux_provider option
        daceb0f9c  man: Remove obsolete RHEL 5 krb5.conf note from sssd-ipa
        ab6a9f8ef  man: Replace ipa_hbac_selinux -> ipa_selinux_refresh in sssd-ipa
        88ad4af5b  man: Replace 'bool' by 'boolean' in sssd-ipa
        c36b6445d  Config: Allow description parameter in [session_recording] section
        aac0d40f6  sssd man-page: Add headings [] for all services
        8e344af33  Man: Add note about debug* options for [session_recording] in sssd.conf
        ec746d4f8  Fix: Remove an orphaned include local.xml
        6e61e1e34  sssctl: Improve the 'sssctl analyze' help output

    Alejandro López (1):
        e7f5a851e  NSS: Add options to exclude UID and GID

    Alexey Tikhonov (35):
        8974a2d86  Make: don't compile 'oidc_child_get_jwk.c'
        f2c69b916  PAM: fix use-after-free during p11_child processing
        f0a3dbe60  cfg_rules: allow ldap_sasl_authid/ldap_krb5_keytab/krb5_keytab
        f47ae71fb  ci: harden pull_request_target workflows against pwn requests
        25bacdb4a  gpo: reject path traversal in gPCFileSysPath
        c29afbf02  sudo: warn when ldap_sudo_search_base falls back to root DN
        637f00441  CI: don't specify 'push:'/'pull_request:' branches
        2ee54d8cb  CI: add retry logic to Bodhi API calls in get-matrix.py
        064b6b123  ci: drop 'analyze-target.yml'
        8a4778c3a  CI: sssd-2-13: limit 'systems' tests to f-43/c10s
        12f3519a4  sudo: don't warn about search base when it was set by provider
        4bc7ece9f  pam_sss: cast to GdmPamExtensionMessage in binary prompt macro
        7ee3f005a  CI 2-10/12/13: use 'centos-10' for 'make-distcheck'
        815d76133  NSS: fix initgroups packet heap disclosure
        1ea0f2da7  pam: validate auth_token_length in extract_authtok_v1()
        cb806786d  nss: validate addrlen in sss_nss_protocol_parse_addr()
        8180e70a2  IDP: fix user matching in `eval_access_token_buf()`
        1a42db627  LDAP: fix fail-open in ppolicy access check on zero results
        202821ad2  PAM: avoid NULL deref when service item is missing
        e9879912c  NSS: reject empty request body before body[blen - 1] access
        d7b036c95  NSS: factor request body validation into a helper
        8fef807c8  NSS: bound service parser reads to the request body length
        5f3a1d780  PAM: fix out-of-bounds read in v1 request parser
        621bd64e8  SYSDB: sanitize SID string in `sysdb_search_entry_by_sid_str()`
        07997d1c1  SPEC: 'sssd-idp' requires 'libsss_idmap'
        f059d21f4  IPA: memory leak fixed
        639e9c164  ipa: fix memory leak in ipa_s2n_get_list iteration
        efb9f035e  ipa: free stale attrs in `ipa_s2n_get_list()` iteration
        139f9bba4  autofs: fix out-of-bounds reads in request parsers
        76e0de9fd  autofs: free per-request context on successful replies
        fbff265d9  autofs: add 'allowed_uids' option to the autofs responder
        4a28fc316  RESPONDER SBUS: get rid of `-sss_resp_reset_ncache_*`
        319a87a38  negcache: replace selective resets with a single recreate helper
        4f9e2c0a3  negcache: limit max mem size consumed by negative cache
        89460c81d  Additional fixes for krb5 timestamps overflow

    Bernhard M. Wiedemann (1):
        60117a7aa  Avoid int overflow after year 2038

    Dan Lavu (24):
        c6dca2df6  tests: fixing mypy linting errors
        79c3612ed  tests: updating pysss_nss_idmap error with more detail
        b03d567da  tests: fixing authselect teardown order
        521b64619  tests: improving offline authentication tests
        befdcf88e  KCM: fix use-after-free of ccache name during TGT renewal
        56a60973c  KCM: free auth_data on TGT renewal setup failure
        836d70b97  tests: widen KCM TGT renewal poll window
        1aa7c081a  tests: adding rewritten dynamic dns tests
        f9581fbbe  removing old multihost dyndns tests
        af9143bd8  tests: remove multihost/alltests/test_sudo.py
        57bc472a2  tests: remove multihost/alltests/test_sss_cache.py
        95f7c356b  tests: remove multihost/ad/test_sudo.py
        39a12164a  tests: remove multihost/alltests/test_sssctl_analyzer.py
        63e4da225  tests: remove multihost/alltests/test_autoprivategroup.py
        5ec91535b  tests: remove multihost/alltests/test_rfc2307.py
        34479abe0  tests: adding gpo test case for traversal bug
        2435fd152  tests: add GPO regression tests for local group collision and verbose Samba logging
        bc5c6a383  test rewrite: legacy intg test_pam_responder.py - first batch
        0299ef51e  test rewrite: legacy intg test_pam_responder.py - remaining batch
        736fd2ca3  tests: remove legacy intg test suite
        a78b25f05  CI: trim unused deps.sh/distro.sh helpers, rename matrix key, fix keytab leak
        40705a5da  CI: drop Debian as a build target
        e4320eca4  tests: collapse su/ssh parametrization in test_gpo.py
        be32d5e26  drop dyndns_refresh_interval from test_dyndns.py

    Ezri Zhu (2):
        62dc74ffc  get_json_string_array_by_id_list: take base_url as parameter
        ce3a687d9  get_json_string_array_by_id_list: batch lookups with getByIds

    Gleb Popov (4):
        efaf43845  FreeBSD CI: Chase the Python 3.12 switch
        c6a425eb0  FreeBSD CI: Explicitly pass --datadir and --sysconfdir to configure
        e287a12b2  FreeBSD CI: Do not reference an unset LOCALBASE variable
        1e79af895  FreeBSD CI: Switch to 15.1-RELEASE

    Harsh Bhadauriya (2):
        cb519dd90  man: fix doubled "are" in sssd-ldap(5)
        bde782322  man: fix YOUR-CLIENT-SCERET typo in sssd-idp(5)

    Iker Pedrosa (4):
        b095023a3  ci: fix error handling in passkey TMT plan SSH commands
        c180e8e71  ci: use hardware.memory syntax for TMT passkey tests
        66892aab1  ci: update passkey TMT plan for native CentOS Stream 10 execution
        d89021c83  ci: add missing `libssh-devel` dependency

    Jakub Vávra (11):
        20826c674  Tests: Update test_nss_user_login_with_overriding_home_directory
        c5d3a13f9  Tests: Auto skip tests dependent on ldbsearch when unavailable
        4c298a840  Tests: Switch tests using ldap adparameters ported to ldifde
        410aee124  tests: Update ds tests to rely less on hostname
        f1eac250a  tests: Fix regex warnings
        f4976fcd0  ci: Swap flake and isort for ruff and reorder jobs
        b45b691e3  tests: Fix test used in c-ares gating to be more resilient
        187be3ab7  ci: Fix duplicated python-system-tests in static-code-analysis
        3bcf687c2  tests: Fix E713 [*] Test for membership should be `not in`
        ebb8d5744  tests: add AD forest multidomain system tests
        630b0668f  tests: Align AD forest test names and grouping

    Joan Torres Lopez (6):
        ea5663382  pam: guard GDM JSON response free against NULL pointer
        4ab1173e1  pam: Forward GDM_AUTH_SESSION_ID from PAM client to child processes
        71323d7af  polkit: Add rule for gnome-remote-desktop pcscd access
        0dd2588a1  PAM: Stop treating gdm-password as a Smartcard-capable service
        ebd73f6c1  PAM: Move PKCS11_LOGIN_TOKEN_NAME export out of add_pam_cert_response()
        c003da660  TESTS: cmocka: new 'test_pam_cert_auth_gdm_smartcard' test

    Justin Stephenson (10):
        fba81a870  ci: Clear cache before installing built rpms
        aa9abafe7  ci: Remove dnf workaround during rpm install
        f446e191f  ci: Dont run system tests for man page only PRs
        551066d62  autofs: avoid leaked enumeration contexts after map
        d48ec1415  nss: guard against length underflow in packet
        029f138e8  authtok: add length to unpack passkey blob
        6497f90ce  pam: guard against zero-length string auth tokens
        51eaa7c51  pam: prevent null dereference in kerberos passkey flow
        abde6726b  authtok: Make sss_auth_unpack_passkey_blob static
        e36b8bebb  util: Use remaining size instead of full size

    Kaushik Banerjee (1):
        23e6e7aff  man: krb5_ccachedir is no longer created by SSSD

    Madhuri Upadhye (15):
        759042869  Tests:  LDAP+KRB5 krb_misc tests
        f72413f68  Tests: fix GSSAPI SSH test setup for krb5_confd_path
        486963f12  tests: port force-LDAPS coverage to system tests
        23c546bdd  Tests: Fix formatting issues in test_ldap_krb5.py
        3c461254d  Tests: Fix AD work on STIG-hardened systems
        a2fb79afa  Tests: Fix AD tests on STIG-hardened systems
        9fa1aeaad  Fix STIG fixture to handle sshd drop-in config files
        8ceea5b2f  Enable AES Kerberos encryption on AD for FIPS:STIG compatibility
        0082932f0  tests: add sudo search base warning suppression test
        b71f6f453  fix(docs): repair malformed quote tag in Spanish sssd-ifp.5 translation
        d41175c3f  tests: convert bash ldap service_map suite to system tests
        572ca8e2f  tests: cover sssctl debug-level when SSSD is stopped and for PAC
        cc2414017  tests: wait for DNS resolve failure before checking logs
        58b1cabcf  tests: remove multihost tests already converted to system tests
        1ec9dade4  tests: drop unused converted pytest marker from multihost

    Masahiro Matsuya (3):
        4f4c05636  test_kcm: use config_apply instead of start to avoid proxy domain auth issue
        2757da772  cfg_rules: add pwfield to allowed_domain_options
        b0a0c9a1d  man: document pwfield per-domain usage in NSS section

    Pavel Březina (17):
        8ebb848bb  ci: serialize make distcheck in build.yml
        41955deb5  ci: use ubuntu-26-04 runner to workaroud issues on ubuntu-24-04
        63dab7ad4  tests: fix test_ldap_krb5__keytab_selects_correct_principal_with_multiple_realms
        b4cfb7410  test: fix missing cmocka prerequisite includes in test_nfsidmap.c
        c2fc94163  nss: fix potential memory leak if packet grow fails
        4fa832bef  oidc_child: escape single quotes in Entra ID OData filters
        fddb3512e  tests: automatically collect coredumps
        e64336d52  ci: move system tests from Github Actions to Testing Farm
        e882bb0c2  ci: add polarion metadata check to static analyzers
        596c1861a  responder: back off accept() on fd exhaustion to stop busy-spin
        6d05a08de  kcm: prune per-connection credential cache on destroy
        da28c507b  ipa: compare users with domain awareness against HBAC rules
        9cb00bd9a  KCM: set the client fd non-blocking to avoid event-loop hangs
        bc6582156  KCM: allocate body buffer only once
        c21039798  KCM: reject request bodies smaller than the protocol header
        5fcbfe81c  KCM: add kcm_recv_timeout to avoid stuck requests
        ebd103ff6  ci: remove sssd db prior restarting it on ipa container

    Peter Šišan (12):
        fddb0ea8c  tests: adds sss_override takes precedence over override homedir
        7edbf2653  tests: adds override homedir does not take precedence over sss_override
        3b62afbb2  tests: removes legacy multihost test
        266eb4f71  tests: removes legacy test testing tevent C library
        630fe6c85  tests: remove tevent_loop.c
        726a06831  tests: remove legacy test `test_bz1146198_bz1144011`
        a4c156ef2  tests: add test_ldap__display_password_expiration_warning
        7fd192de7  tests: remove test_bz748856
        a735a5591  tests: add test_ldap__display_grace_logins_when_password_has_expired
        e95a26e4e  tests: remove `test_bz954323`
        27a13a654  tests: add `test_ldap__authentication_fails_once_password_max_age_is_reached`
        74a02f87e  tests: remove `test_ldap_pasword_policy.py` and `change_user_password_while_expired.sh`

    Philipp Tomsich (7):
        878f89c57  SDAP: Parse each attribute of an entry in message order
        b7270d6b1  Tests: Cover sdap_parse_entry() with repeated and irregular entries
        2ca54962b  SDAP: Match object class names exactly
        15a393b39  SDAP: Reject a DN or attribute description with a zero byte
        729c7e602  SDAP: Cap the precision used to print bervals
        9e7dd09a5  SDAP: Compare the class name length before its bytes
        378b779be  SDAP: Use the project's comment style in sdap_parse_entry()

    Rakesh Kumar (4):
        c6d3732e4  Man: Improvement in max_ccache_size parameter
        01be0a75d  Man: Fix krb5_use_fast demand option description
        b297e6560  Fix: Preserve explicitly set 'none' provider values
        a22921e67  Fix ldap_use_ppolicy name in LDAP ppolicy test docstring

    Renan Rodrigo (1):
        5427f77a5  Fix FTBFS with GDM 51 PAM extension headers

    Samuel Cabrero (2):
        dfce02b8c  AD: Initialize data_provider in struct sdap_options
        7bebad45f  SDAP: Warn about ldap_sudo_search_base only if sudo target is enabled

    Scott Poore (10):
        1ba8374ed  Tests: Adding flaky marker to retry GDM critical
        9f4fd0d1c  Tests: skip nonposix nested test for older sssd
        1ec4b3813  Tests: add ldap_sudo_search_base warning test
        ac918bdc3  Tests: multihost ldap to ldaps
        161f69043  Tests: multihost ssh use ip and sssd snippet perms
        7a6b8621a  Tests: multihost remove stderr redirect
        b3f67c502  Test: add sssd conf backup to test_0002_1736796
        747cb2f83  Tests: multihost change passwd setting for STIG
        817b83dd4  Tests: multihost ldap password policy fixes
        091f5773b  tests: clear sssd cache in teardown of AD idmap range tests

    Shradha Jawale (1):
        2c2e99cb5  man: Fix filter_users_in_groups and pam_gssapi_check_upn options.

    Sumit Bose (14):
        9884f3347  oidc_child: change default with no auth method
        5b2734f6a  p11_child: use X509_STORE_get1_objects() is available
        4018f1066  ipa: do not use infinite timeout for certmap lookups
        babdf5ac8  ipa: error out during issues reading IPA configuration
        e2130047a  nfs idmap: error out if buffer is too small
        ead2b1bcb  test: test nfs idmap plugin id to name functions
        57a352f6e  ldap: pwd_expire_policy_warn does not overwrite errors
        173ad00ba  test: pwd_expire_policy_warn does not overwrite errors (IPA)
        14c215969  ldap: show expired message if shadow lastChange is missing or 0
        54f0afcae  test: pwd_expire_policy_warn does not overwrite errors (LDAP)
        fc318dd03  krb5: filter AD host principals during TGT validation
        c4b6d409b  tests: add unit tests for get_validation_principal()
        47eb3c6f3  SDAP: Align sdap_parse_entry() with the coding style
        afa5e4211  ldap: retry TLS handshake on timeout

    Tomas Halman (4):
        c78c32fe6  certmap: check that SID exists in certificate
        13c46a7e9  PAM: clear state pointer before freeing state itself
        f624ad8fb  Treat shadowExpire=0 correctly
        6b4db9f60  IDP: Clean old items from open_request_table

    Vincent Wilms (1):
        3388fe47c  pam: keep preauth indicator for socket activation

    aborah-sudo (8):
        b6cde1092  Tests: use client IP instead of sys_hostname for SSH login
        45b501584  Tests: add socket activation tests for all-responder and sudo scenarios
        dbe78afbb  tests: convert multihost failover and connection timeout tests to system tests
        4765977b1  tests: convert cached_auth_timeout bash tests to system tests
        41ba1ca59  tests: convert sudo offline and full_refresh bash tests to system tests
        a2086102d  tests: convert offline auth bash tests to system tests
        932b64468  Tests: Convert ldap failover uri list bash tests to system tests
        3b16c093c  Tests: Convert remaining single-server ldap failover bash tests

    dependabot[bot] (5):
        4b6bdc109  ci: bump cross-platform-actions/action from 1.2.0 to 1.3.0
        8600ba6c4  ci: bump actions/checkout from 6 to 7
        adbafec6b  ci: bump actions/setup-python from 6 to 7
        193a39048  ci: bump vapier/coverity-scan-action from 1.8.0 to 1.9.0
        88d5e10a5  ci: bump cross-platform-actions/action from 1.3.0 to 1.5.0

    divinehawk (3):
        26dd809f0  pam: add pam_add_response_no_send()
        59606c872  pam: offer local Smartcard authentication in the JSON message
        3018ef927  tests: check local Smartcard authentication in the JSON message

    hagaikwa-redhat (1):
        9ed886f67  man: fix TENNANT-ID typo in sssd-idp(5) example

    kkz (2):
        489d0e291  oidc_child: Fix logic error in Keycloak lookup
        441ca937e  krb5: Fix logic errors in OAuth2 code verification

    krishnavema (3):
        40a649674  Add default timeout handling for soft_ocsp and regression tests for smart card authentication (resolves: RHEL-5043)
        f8350c3a2   tests: migrate KCM to system tests
        88b90b523  tests: add AD smart card certificate authentication test

    sssd-bot (2):
        fd27eb9fa  pot: update pot files
        246abb01a  Release sssd-2.13.2

    tong_1001 (2):
        498155f98  delete useless tmp_ctx variable from pam_dom_forwarder()
        2d11cacb7  fix potential memory leak

    zhaoshuang (1):
        77cddeca3  Plug memory leak: add missing dbus_message_unref

