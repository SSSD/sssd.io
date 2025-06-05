SSSD 2.11.0 Release Notes
=========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* The deprecated tool ``sss_ssh_knownhostsproxy`` was finally removed, together
  with the ``./configure`` option ``--with-ssh-known-host-proxy`` used to build it.
  It is now replaced by a stub which displays an error message. Instead of this
  tool, you must now use ``sss_ssh_knownhosts`. Please check the
  sss_ssh_knownhosts(1) man page for detailed information.
* Support for the previously deprecated ``sssd.conf::user`` option
  (``--with-conf-service-user-support`` ``./configure`` option) was removed.
* When both IPv4 and IPv6 address families are resolvable, but the primary is
  blocked on firewall, SSSD attempts to connect to the server on the secondary
  family.
* During startup SSSD won't check NSCD configuration to issue a warning in a
  case of potential conflict.
* Previously deprecated ``--with-files-provider`` configure option and thus
  support of ``id_provider = files`` were removed.
* Previously deprecated ``--with-libsifp`` configure option and ``sss_simpleifp'
  library were removed.
* ``krb5-child-test`` was removed. Corresponding tests under ``src/tests/system/``
  are aimed to provide a comprehensive test coverage of ``krb5_child``
  functionality.
* SSSD doesn't create any more missing path components of DIR:/FILE: ccache
  types while acquiring user's TGT. The parent directory of requested ccache
  directory must exist and the user trying to log in must have ``rwx`` access to
  this directory. This matches behavior of ``kinit``.
* The DoT for dynamic DNS updates is supported now. It requires new version of
  ``nsupdate`` from BIND 9.19+.
* The option default_domain_suffix is deprecated. Consider using the more
  flexible domain_resolution_order instead.

New features
~~~~~~~~~~~~

* New generic id and auth provider for Identity Providers (IdPs), as a start
  Keycloak and Entra ID are supported. Given suitable credentials this provider
  can read users and groups from IdPs and can authenticate IdP users with the
  help of the OAUTH 2.0 Device Authorization Grant (RFC 8628)
* SSSD IPA provider now supports IPA subdomains, not only Active Directory. This
  IPA subdomain support will enable SSSD support of IPA-IPA Trust feature, the
  full usable feature coming in a later FreeIPA release. Trusted domain
  configuration options are specified in the ``sssd-ipa`` man page.

Important fixes
~~~~~~~~~~~~~~~

* ``sssd_kcm`` memory leak was fixed.
* If the ssh responder is not running, ``sss_ssh_knownhosts`` will not fail (but
  it will not return the keys).

Packaging changes
~~~~~~~~~~~~~~~~~

* **Important note for downstream maintainers.**

  A set of capabilities required by privileged binaries was further reduced to:

  .. code-block:: text

      krb5_child cap_dac_read_search,cap_setgid,cap_setuid=p
      ldap_child cap_dac_read_search=p
      selinux_child cap_setgid,cap_setuid=p
      sssd_pam cap_dac_read_search=p

  Keep in mind that even with a limited set of fine grained capabilities, usual
  precautions still should be taken while packaging binaries with file
  capabilities: it's very important to make sure that those are executable only
  by root/sssd service user. For this reason upstream spec file packages it as:

  .. code-block:: text

      -rwxr-x---. 1 root sssd

  Failing to do so (i.e. allowing non-privileged users to execute those
  binaries) can impose systems installing the package to a security risk.

* New configure option ``--with-id-provider-idp`` to enable and disable building
  SSSD's IdP id provider, default is enabled.
* ``--with-nscd-conf`` ``./configure`` option was removed.
* Support of deprecated ``ad_allow_remote_domain_local_groups`` sssd.conf option
  isn't built by default. It can be enabled using
  ``--with-allow-remote-domain-local-groups`` ``./configure`` option.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* The id_provider and auth_provider options support a new value ``idp``. Details
  about how to configure the IdP provider can be found in the sssd-idp man page.
* New optional fourth value for AD provider configuration option
  ad_machine_account_password_renewal_opts to select the command to update the
  keytab, currently ``adcli`` and ``realm`` are allowed values
* The pam_sss.so module gained a new option named "allow_chauthtok_by_root". It
  allows changing realm password for an arbitrary user via PAM when invoked by
  root.
* New ``ldap_read_rootdse`` option allows you to specify how SSSD will read
  RootDSE from the LDAP server. Allowed values are "anonymous", "authenticated"
  and "never"
* Until now dyndns_iface option supported only "*" for all interfaces or exact
  names. With this update it is possible to use shell wildcard patterns (e. g.
  eth*, eth[01], ...).
* ``ad_allow_remote_domain_local_groups`` option is deprecated and will be removed
  in future releases.
* the ``dyndns_server`` option is extended so it can be in form of URI
  (dns+tls://1.2.3.4:853#servername). New set of options ``dyndns_dot_cacert`,
  ``dyndns_dot_cert`` and ``dyndns_dot_key`` allows to configure DNS-over-TLS
  communication.
* Added ``exop_force`` value for configuration option ``ldap_pwmodify_mode``. This
  can be used to force a password change even if no grace logins are left.
  Depending on the configuration of the LDAP server it might be expected that
  the password change will fail.

Tickets Fixed
-------------

* `#4646 <https://github.com/SSSD/sssd/issues/4646>`__ - Make sure periodical tasks use randomization
* `#4997 <https://github.com/SSSD/sssd/issues/4997>`__ - errno_t not exactly portable?
* `#5905 <https://github.com/SSSD/sssd/issues/5905>`__ - [RFE] Continue searching other PKCS#11 tokens if certificates are not found
* `#6601 <https://github.com/SSSD/sssd/issues/6601>`__ - smartcard login fails when network disconnected
* `#6665 <https://github.com/SSSD/sssd/issues/6665>`__ - LDAP auth happens after search failure
* `#6910 <https://github.com/SSSD/sssd/issues/6910>`__ - SSSD dyndns_ifname with wildcard
* `#7209 <https://github.com/SSSD/sssd/issues/7209>`__ - Tests: util-tests fails if time zone is not UTC
* `#7510 <https://github.com/SSSD/sssd/issues/7510>`__ - No way to configure ``debug_backtrace_enabled`` for ``ldap_/krb_child``
* `#7612 <https://github.com/SSSD/sssd/issues/7612>`__ - sssd does not lookup user gid's at reboot without ``*.ldb`` files
* `#7642 <https://github.com/SSSD/sssd/issues/7642>`__ - AD machine account password renewal via adcli doesn't honor ad_use_ldaps setting
* `#7664 <https://github.com/SSSD/sssd/issues/7664>`__ - sss_ssh_knownhosts fails on F41
* `#7671 <https://github.com/SSSD/sssd/issues/7671>`__ - Mismatch between input and parsed domain name when default_domain_suffix is set.
* `#7715 <https://github.com/SSSD/sssd/issues/7715>`__ - sssd backend process segfaults when krb5.conf is invalid
* `#7746 <https://github.com/SSSD/sssd/issues/7746>`__ - krb5_child couldn't parse pkcs11 objects if token label contains semicolon
* `#7781 <https://github.com/SSSD/sssd/issues/7781>`__ - New ``chown`` likely not working as expected.
* `#7793 <https://github.com/SSSD/sssd/issues/7793>`__ - Disk cache failure with large db sizes
* `#7876 <https://github.com/SSSD/sssd/issues/7876>`__ - Group enumeration does not work if group name contains ``#``
* `#7931 <https://github.com/SSSD/sssd/issues/7931>`__ - LDAPU1 Local auth mapping rule error
* `#7981 <https://github.com/SSSD/sssd/issues/7981>`__ - invalid memcache_delete_entry  errors  cause   in excess of 150 MB of /var/log/sssd/sss_nss.log entries per day.




Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.10.0..2.11.0

    Alejandro López (5):
        766820500  SSH: sss_ssh_knownhosts must ignore DNS errors
        9ee10f98e  OPTS: Add the option for DP_OPT_DYNDNS_REFRESH_OFFSET
        2c72834e6  TESTS: Also test default_dyndns_opts
        c2d95a3b3  SSH: sss_ssh_knownhost must succeed if the responder is stopped
        4ef4241cc  SSH: Remove sss_ssh_knownhostsproxy and keep the stub

    Alexander Bokovoy (1):
        8accd0476  oidc_child: fallback to ID and access tokens when looking up configured user identity

    Alexey Tikhonov (122):
        cbe3b0347  When using SPDX expression the booleans must be in all caps.
        b928dbe1f  Get rid of on-house MIN/MAX definitions
        b84ced06c  DEBUG: add 'debug_backtrace_enable' getter
        2300abbaa  UTILS: simplify / comment a bit better
        88b55de28  DEBUG: propagate debug_backtrace_enabled to child processes
        30a980384  INI: remove unused helpers
        1d19b8ad9  INI: stop using 'libini_config' for access check
        8472777ec  INI: relax config files checks
        518db322f  Configuration: make sure /etc/sssd and everything
        d7c977092  INI: don't report used snippets in `sss_ini_add_snippets()`
        4cc62d457  SSSCTL: change error message to be more accurate
        60d369c00  INI: add verbose error messages
        2d0f0480a  chown() gpo cache recursively.
        2d85f89f9  MAN: mistypes fixes
        71430f777  SPEC: require OpenSSL >= 1.0.1
        b74fe65b6  SPEC: untie capabilities of different binaries
        7ce14e7f7  LDAP_CHILD: replace 'cap_dac_override' with 'cap_dac_read_search'
        942799d5e  LDAP_CHILD: don't require any capabilities besides 'cap_dac_read_search'
        5ef1efc52  LDAP_CHILD: require only 'cap_dac_read_search=permitted'
        23d9c93b9  Describe current capabilities usage.
        507d2daa8  CLIENT: don't try to lookup `getservbyport(0, ...)`
        1f8040de2  SSSDConfig: chown file to root:sssd
        3294cdb09  CI: COPR: add c10s buildroot
        21c628055  'dtrace' was moved to a separate package on C10S as well
        1ef3cf525  KRB5: verbosity around ccname handling
        5e17bc22f  KRB5: don't pre-create parent dir(s) of wanted DIR:/FILE:
        541c42ba7  KRB5: skip `switch_creds()` in PKINIT case
        947f791d8  KRB5: 'fast-ccache-uid/gid' args aren't used anymore
        19dd64322  KRB5: don't require effective CAP_DAC_READ_SEARCH
        89d61e66b  KRB5: verbosity
        655387711  KRB5: drop cap_set*id as soon as possible
        19a871a9e  KRB5: 'krb5_child' doesn't require effective capabilities
        988e5fa84  become_user() moved to src/monitor
        a406c1b28  KRB5: cosmetics
        20d658bfb  Deprecate and make support of 'ad_allow_remote_domain_local_groups'
        110c4aead  KRB5: mistype fix
        c357838d8  sss_semanage code is only used by 'selinux_child'
        75f1b2bae  sss_selinux code is only used by 'ipa_selinux'
        5f2769267  UTILS: shared helper to print current process credentials
        84baae4b4  SELINUX_CHILD: only cap_set*id is required
        548fdb317  Ignore '--dumpable' argument in 'krb5_child' and 'ldap_child' to avoid leaking host keytab accidentially.
        5094a3d99  UTILS: reduce log level if `sss_krb5_touch_config()` fails
        af65c00b9  SPEC: conf files are owned by 'root:sssd'
        a20fa0ffd  SYSTEMD SERVICE: use "--no-dereference" for 'chown'
        4b35ac30c  SYSTEMD: traverse 'sssdconfdir' symlink while chown-ing
        561c51bd7  SYSTEMD: fix missing 'g+x' on /etc/sssd and subdirs
        6bd231cda  LOGROTATE: fix path to pid file
        85784e761  PAM: don't set PR_SET_DUMPABLE
        7ff2e486e  SELINUX_CHILD: fail immediately if set-id fails
        95160058c  SELINUX_CHILD: 'ret' argument of `prepare_response()` is always 0
        6e66cbb1f  SELINUX: get rid of response as it was redundant and
        6cb2de5de  Clear env of privileged 'sssd_pam' as a security hardening measure.
        50892b6bc  Don't clear 'sssd_pam' env when built for intg-tests
        8e8342a2b  certmap: remove stray export declaration
        9c0c97701  Delete 'lib/sifp'.
        e50d0fa4d  CI: remove C9S from platforms list.
        cf6503286  Get rid of 'local_negative_timeout' config option
        827a9bffa  Delete 'files provider'
        a71f9a6cb  IPA: verbosity
        003c699b4  TESTS: fix issue reported by 'black'
        196ad92ab  Fixed a mistype
        7f1b7c968  KCM: fix memory leak
        2a40db33a  RESPONDER: remove unreachable code
        5e16c957f  MONITOR: remove nscd conf check
        9e72bc242  KCM: another memory leak fixed
        164df1101  BUILD: introduce "--with-syslog=stderr" option
        c36c320d1  PAM: fix issue found by Coverity
        e2408c246  SPEC: suppress stderr of usermod
        f65d0eaa4  IPA: fixed misleading messages
        228072105  IPA: cosmetics
        9b6d8fe72  IPA: don't bother checking keytab ownership
        8bfc88e49  Get rid of '--with-conf-service-user-support' ./configure option
        281d9c3ed  SYSDB: don't add group members if 'ignore_group_members == true'
        5e882b366  SYSDB: update in sysdb_add_group_member_overrides()
        501663f2a  SYSDB: update in sysdb_add_group_member_overrides()
        6e01e4127  SYSDB: update in sysdb_add_group_member_overrides()
        6c50506c4  SYSDB: fix sysdb_add_group_member_overrides()
        a58aa915f  SYSDB: update in sysdb_add_group_member_overrides()
        108800dc9  SYSDB: update in sysdb_add_group_member_overrides()
        6aae3572a  SYSDB: update in sysdb_add_group_member_overrides()
        0a9ae2c2b  SYSDB: update in sysdb_add_group_member_overrides()
        f61b9bbb2  SYSDB: make `sysdb_get_user_members_recursively()` static
        ed6956e92  SYSDB: update in get_user_members_recursively()
        af5e0b705  capabilities: check if cap is supported
        9f5636f71  capabilities: don't rely on hardcoded set of supported capabilities
        764798d7a  SPEC: package 'enable_sssd_conf_dir' as a part of 'sssd-krb5-common'
        150d2ee09  Move 'STRUCT_CRED' definition into standalone header
        39f37c934  SYSDB: update in sysdb_add_group_member_overrides()
        b80deaeb5  SYSDB: update in sysdb_add_group_member_overrides()
        9bc6dc578  SYSDB: debug message fixed
        c7a979dc9  SYSDB: update in sysdb_add_group_member_overrides()
        6b46b7a7b  SYSDB: update in get_user_members_recursively()
        ca76b7c8f  DEBUG: a new helper that skips backtrace
        47b25f068  Avoid logging to the backtrace unconditionally in hot paths.
        331908d18  UTIL: sss_parse_internal_fqname() optimization
        6aa4b1e08  UTIL: sss_parse_internal_fqname() optimization
        707825679  UTIL: sized_domain_name() optimization
        5cdfc54bd  RESPONDER: sized_output_name() optimization
        f101c1bb5  UTIL: sss_output_name() optimization
        0267cd976  RESPONDER: delete sss_resp_create_fqname()
        83c0217c5  UTIL: remake sss_*replace_space() to inplace version
        1641dfd5b  UTIL: delete sss_fqname()
        804b22cfa  UTIL: sss_tc_fqname2() optimization
        4deee59a3  SPEC: relax Samba version req a bit
        923ec509b  DB: skip sysdb_add_group_member_overrides() completely
        60f384436  DB: don't provide 'expect_override_dn' to `sysdb_add_group_member_overrides()`
        ee1c2d177  UTIL: mark non string array properly
        fd562676c  IPA: return ENOENT if `ipa_get_config` yields nothing
        ad7dc210f  PAM: fixes following issue:
        81a377ded  Consolidate utf8 strings operations to libunistring
        4cc856ee8  SBUS: use ENETUNREACH instead of ENONET
        180bf1fc7  CLIENT: use ETIMEDOUT instead of ETIME
        ad30eb74e  CI: drop "missingInclude" from cppcheck
        8d7e50569  Move 'sss_python.*' under 'src/python'
        3a7776b84  Consolidate all Python related includes to 'sss_python.h'
        11e388e8f  Make sure "Python.h" is included last.
        ae32bbcdc  MAN: remove mention of a 'local domain'.
        449f4c1aa  UTIL: add a helper to print libldap diagnostics
        7eee7154f  LDAP: debug fail of ldap_set_option(LDAP_OPT_X_SASL_NOCANON)
        6d115a7a4  Replaces usage of 'sss_ldap_get_diagnostic_msg()'
        6d5b65046  UTILS: removed ununsed 'sss_ldap_get_diagnostic_msg()`
        0fc6768c6  RESPONDER: skip mem-cache invalidation

    Andrea Bolognani (1):
        8477aa065  configure: Require valgrind-devel when valgrind is enabled

    André Boscatto (3):
        36148c97c  man: Updating sssd-simple(5) man page
        d61ba818d  TESTS: Add access control simple filter tests
        41a0df2d4  TESTS: Add tests to cover access control access_filter (AD/LDAP)

    Dan Lavu (13):
        934ae04e1  tests: rm intg/test_sss_cache.py
        3054970e4  tests: adding gpo customer test scenario to use the ldap attribute name
        be0c232be  tests: removing intg/ts_cache.py
        d5b648498  tests: converting all the ldb cache tests to use one provider
        58a2fee59  tests: adding system/tests/readme.rst as a quick primer
        b060ed507  tests: moved ad specific authentication test and created test_ad.py
        132d2088a  tests: adding override_homedir test
        ffd5d0e10  tests: test_kcm.py fixing confusing error message
        0f0118490  tests: rm intg ssh_pubkey
        aebb4e130  tests: extending sss_override testcase to assert overridden user group memberships
        08a3c410b  tests: adding generic password change tests
        f8f7f843d  tests: removed overlapping test scenarios from authentication tests
        ab8342770  tests: adding preferred topology markers to select tests

    David Abdurachmanov (1):
        f3fdb4293  Properly check valgrind arches

    Denis Karpelevich (2):
        36b1d97b5  Parametrize sssctl tests 3.
        062e8ab6b  Parametrize sssctl tests 2.

    Dominika Borges (1):
        9c65b89fd  doc: improve description of ldap_disable_range_retrieval

    Evgeny Sinelnikov (1):
        b7d4a8065  cert util: add support build with OpenSSL older than 3.0

    Georgij Krajnyukov (4):
        3392a857c  P11_CHILD: Invert if statement to reduce code nesting
        8311d3cc8  P11_CHILD: Implement passing const args to get_pkcs11_uri
        1b3d5d829  P11_CHILD: Extract slot processing into separate function
        782a6dd54  P11_CHILD: Make p11_child iterate over all slots

    Gleb Popov (25):
        add0ed175  platform.m4: Teach to look for struct xucred in addition to struct ucred
        843aa089a  Extend util_creds.h with xucred case
        38fe14abb  Use LOCAL_PEERCRED option instead SO_PEERCRED where appropriate
        ed0af81a3  configure.ac: Check for the availability of the procctl() function
        9bb4cf15b  Introduce util/sss_prctl module to abstract out process controlling API
        3d4d9c48d  Make use of sss_prctl_* throughout the codebase
        cc48ad5ba  Add a reference to FreeBSD procctl into sssd.conf(5) manpage
        dbe820049  Fix build on FreeBSD by including sys/socket.h
        dfceb68dd  Use cli_creds_get_*() helpers wherever possible
        4f9a7dcd5  pam: Add option to allow changing auth token when running as root
        bf79a1597  configure.ac: Introduce --disable-linux-caps arg to make capabilities optional
        8008a2a82  Only include <sys/capability.h> if the header is present
        f566a3a8e  Add stub implementations for functions from capabilities.c if caps aren't available
        0b4a68a1b  Properly check the returning value of sss_set_cap_effective() calls
        606cf44f0  Use MAXHOSTNAMELEN as HOST_NAME_MAX if available
        e13ca3aba  Don't do setsockopt(TCP_USER_TIMEOUT) on systems that don't have it
        2f6c83a22  Include <sys/socket.h> because the code uses AF_INET
        d6da04d80  Fix build on systems that do not have pam_ext.h
        8672fba0c  Use cross-platform pthread_self() instead of Linux-specific SYS_gettid()
        fe10f5e6d  Add an implementation for pam_modutil_getlogin() for systems that do not have it
        0c2fef802  Define ENODATA if it isn't available
        58cced880  Include config.h before checking for HAVE_ERRNO_T
        641ef4823  Define ELIBACC and ELIBBAD if they aren't available
        889b1cddf  Include pam_appl.h due to pam_get_item() usage
        dc252b72a  Fix the in-house pam_modutil_getlogin() implementation

    Iker Pedrosa (2):
        ae6a0ff64  tests: add feature presence automation
        067dbf614  tests: improve feature presence automation

    Ivan Korytov (1):
        5c69acc93  tests: Update mock date to postpone timezone related failures

    Jakub Vávra (6):
        4a7ab02d8  Tests: Add missing returncode to test_0004_bz1638295
        ed666e9fa  tests: Unify packages available on client for ipa suites
        7514309bb  Tests: Update sst to rhel-sst-idm-sssd for polarion.
        098105486  Tests: Add ssh to services for authentication with ssh tests.
        53b26af6f  tests: Update mhc.yaml for relocated /data and /enrollment
        536f7fcdc  tests: Move /exports to /var/exports for autofs tests

    Jan Engelhardt (5):
        a2e91d20f  build: remove superfluous WITH_IFP leftover
        2b7915dd8  sssd: always print path when config object is rejected
        42d1837a8  build: unbreak detection for x400Address
        8cdebfcfe  build: stop overriding CFLAGS
        93eb0736e  build: fix spellos in configure.ac

    Justin Stephenson (26):
        7a8da2762  ipa: Check sudo command threshold correctly
        0bb136451  analyzer: fix two crashes
        bf99c163c  DEBUG: lower missing passkey data debug level
        4fbf96357  tests: have analyzer request child parse child log
        e58cf8031  ci: Remove internal covscan workflow
        c6294f5ff  ci: Add workflow for 'coverity' label in PRs
        d2232139a  CI: Fix coverity label multiline conditional
        463bf25a1  ci: Have coverity workflow run against PR code
        e87cc2c27  SYSDB: Store IPA trust type
        8879cf88f  Rename struct ipa_ad_server_ctx, and add id_ctx union member
        70daa0091  ipa: Make ipa_service_init() like ad_failover_init()
        1b0c6203e  ad: Combine 1+2way trust options creation functions
        0862fcb83  ipa: Make ipa server ad* functions generic
        dc7e28064  ipa: Add ipa subdomain provider initialization
        4378ea626  ipa: Support ipa subdomain account info requests
        f085fe0d0  ipa s2n: Remove check for SYSDB_UPN
        4eb75cc3a  ipa: Rename ipa_create_ad_1way_trust_ctx()
        b63321cc2  Handle missing SID for user private group
        de4cea5cb  ipa s2n: Ignore trusted IPA user private group
        129b54962  AD: Remove unused AD_AT_TRUST_TYPE attribute
        3c87b8117  man: IPA subdomain changes to sssd-ipa
        a7b3255f7  ipa: Set proper domain basedn for subdomain options
        5cb26ed6c  ci: include build description for covscan
        261191137  ci: Use pull_request_target for conditional
        ae59f2992  IPA: ipa_get_config_send() was updated
        e50533d66  Workaround PTR record lookup failure

    Krzesimir Nowak (1):
        39f9ff852  Assume that callbacks are not broken in OpenLDAP when cross-compiling

    Madhuri Upadhye (5):
        247797b2a  Tests: sss_ssh_knownhosts with port number
        163b1e316  Tests: Mark builtwith for knownhosts tests
        94e47c5ce  Test: Passkey test cases with diffferent auth_methods
        ef535319c  Test: Add the test when we replace id_provider
        481fa1bf6  Test: Add IPA ID view override test cases

    Michael Stone (3):
        5f7df3995  return here so MINOR_FAILURE isn't auto-promoted to FATAL_FAILURE
        9553c78fc  make log line match preceeding function name
        93f9db57a  add SSS_AUTHTOK_TYPE_PAM_STACKED

    Ondrej Valousek (1):
        56438ec78  Fix bug in objectclass_matched()

    Pavel Březina (5):
        0e8e6946b  Update version in version.m4 to track the next release
        a0f19feb1  ci: grab ipa logs from ipa host
        d0bfa08d8  ci: print duration of each test case
        de84e5721  idp: add sssd-idp.5.xml to po4a configuration
        b9cdd65b7  pot: update pot files

    SATOH Fumiyasu (1):
        51bf66730  SPEC: sssd.conf file is owned by 'root:sssd' and mode is 0640

    Samuel Cabrero (5):
        2e6fdb65f  CACHE_REQ: always return the first result in service by port lookups
        f911e3866  SYSDB: Use temporary memory context to allocate the results
        b1c164945  SYSDB: Allow multiple services associated to the same port
        56ef896e8  INTG-TESTS: Add Tests for service by name and by port lookups
        afc643ddf  IFP: Restrict destination

    Scott Poore (1):
        510130e84  man: sssd.conf update defaults for certmap maprule

    Sumit Bose (39):
        718454197  ldap: add 'exop_force' value for ldap_pwmodify_mode
        deefe9ad8  tests: add 'expo_force' tests
        2d408edd9  pam_sss: add some missing cleanup calls.
        8571d45b6  subdomains: check when going online
        ffec45bdb  ssh: do not use default_domain_suffix
        fb91349cf  responders: deprecate default_domain_suffix option
        fce94aec3  ldap_child: make sure invalid krb5 context is not used
        e4b26042a  dyndns: collect nsupdate debug output
        8c86abd6d  ldap: make sure realm is set
        10c753e1b  krb5_child: ignore Smartcard identifiers with a ':'
        70ab0c0d0  man: add missing third option of ad_machine_account_password_renewal_opts
        92697d467  ad: use realm renew for keytab renewal
        4c183b1f3  utils: add non-blocking read from child processes
        44ecd4525  configure.ac: add option for realm and adcli paths
        596bc5fb8  sdap: include sub-domain memberships in updates
        215a05340  sss-idmap: add support for more general POSIX id-mapping
        a27154b75  sss-idmap: add normalize and casefold options
        0dfd05798  idmap: rename comp_id() to compute_id()
        5b4f9466d  idmap: update doxygen config
        8c3074a97  sss-idmap: update library version
        c85ab24a4  certmap: allow prefix in rule in sssd.conf
        95f1a9c57  oidc_child: change verify_token() to decode_token()
        dc3165c35  Revert "sdap: include sub-domain memberships in updates"
        6f09d3f05  oidc_child: add more JSON helpers
        133a13b76  oidc_child: add user and group lookup
        9a2b031a0  oidc_child: inital tests for user and group lookups
        8be405571  oidc_child: fix issues found by Coverity
        7a2f9395c  krb5 idp: make sss_idp_oauth2_decode public
        578ae63b7  krb5: make k5c_attach_oauth2_info_msg() shareable
        810d41e02  utils: make child_exited() public
        9be8604e6  utils: make child_terminate() public
        ed68410d4  utils: make activate_child_timeout_handler() public
        cf3a1d85e  idp: initial implementation of IdP id provider
        b1cc4da87  confdb: idp provider uses MPGs by default
        66b062f75  idp: man page for SSSD's IdP id provider
        c16c13c55  idp: add configure option to disable IdP provider
        d8842a708  idp: add basic options to tune id-mapping
        f52988637  tests: initial IdP provider tests
        2f6c9b043  idp: add support and test for ignore_group_members option

    Tomas Halman (11):
        a822206c7  Missing 'dns_update_per_family' option
        fe26a9308  Add DoT support for DNS updates
        537e586ba  failover: Make failover work over IP families
        894971b64  tests: Check failover to secondary IP family
        95caf1aae  Pattern support for dyndns_iface option
        655cd72a7  man: clarify %o and %h homedir substitution
        4cb65932c  test: enumeration with # in the group name
        158b4cdb7  Enumerate object with escaped characters in name
        fcc108714  Configure how SSSD should access RootDSE.
        a3ad066c0  failover: fix fo_is_ip_address check
        2cf2e83a2  p11_child: Add timeout parameter

    Weblate (1):
        0c5c7538b  po: update translations

    Yaakov Selkowitz (1):
        6b2219015  SPEC: require systemtap-sdt-dtrace on ELN

    aborah-sudo (11):
        9c4a51fa1  Tests: Test transformation of bash-ldap-id-ldap-auth netgroup
        a926f43ac  Tests: Reverse the condition and fail
        604051080  Tests: SSSD fails to store users if any of the requested attribute is empty
        7b855ab92  Tests: Fix python black formation error
        befc4b66e  Tests: Fix the permission of snippet file
        e76849bab  Tests: ldap search base does not fully limit the Netgroup search base
        a3ed676c1  Tests: Test trasformation for netgroup with generic provider
        fdf0b500a  Tests: Fix test_008_wildcardsearch for RHEL10
        4ed56e58d  Tests: Rename test_misc.py to test_all_misc.py
        b4baf8add  Tests: Add proxy provider test cases for SSSD
        3d278ec5d  Tests: Add Infopipe tests for group properties, membership changes, and user attributes

    fossdd (4):
        91d8199d1  Fix missing include sys/types.h
        8edb14fad  MC: Use useconds_t instead of their reserved type
        8886a27b8  failover: Clarify message for local hosts file resolution failure
        459cc6b15  CLIENT: Define NETDB_INTERNAL if not already

    santeri3700 (1):
        d004e7b4b  ad: honor ad_use_ldaps setting with ad_machine_pw_renewal

    shridhargadekar (1):
        6ee49e617  Tests: add importance marker for sssctl analyze
