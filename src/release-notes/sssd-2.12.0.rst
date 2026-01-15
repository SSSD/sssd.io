SSSD 2.12.0 Release Notes
=========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* After startup SSSD already creates a Kerberos configuration snippet typically
  in ``/var/lib/sss/pubconf/krb5.include.d/localauth_plugin`` if the AD or IPA
  providers are used. This enables SSSD's localauth plugin. Starting with this
  release the an2ln plugin is disabled in the configuration snippet as well. If
  this file or its content are included in the Kerberos configuration it will
  fix CVE-2025-11561.
* Previously deprecated ``--with-extended-enumeration-support`` ``./configure``
  option was removed.
* SSSD now allows using machine credentials from a trusted AD domain or Kerberos
  realm if no suitable domain-local credentials are available.

New features
~~~~~~~~~~~~

* SSSD now supports authentication mechanism selection through PAM using a
  JSON-based protocol. This feature enables passwordless authentication
  mechanisms in GUI login environments that support the protocol. Feature will
  be supported by GNOME Display Manager (GDM) starting with GNOME 50. While
  currently optimized for GNOME, the JSON protocol design allows for future
  support in other display managers. authselect is the recommended approach and
  will handle the necessary PAM stack modifications automatically starting with
  version 1.7 through the new option ``with-switchable-auth`` which provides a
  new PAM service called ``switchable-auth``. Manual PAM configuration is also
  possible. For more technical details and implementation specifications, see
  the `design documentation
  <https://sssd.io/design-pages/passwordless_gdm.html>`__
* Generic SSSD LDAP provider (``id_provider = ldap``) now supports fetching
  subid ranges, a feature previously supported only by the IPA provider.

Packaging changes
~~~~~~~~~~~~~~~~~

* This update makes it possible to not grant CAP_SETUID and CAP_SETGID to
  ``krb5_child`` binary in a situation where it is not required to store
  acquired TGT after user authentication. Taking into account that it is already
  possible to avoid using CAP_DAC_READ_SEARCH if keytab is readable by SSSD
  service user, and usage of 'selinux_child' isn't always required, this allows
  to build a setup with completely privilege-less SSSD to serve certain use
  cases. In particular, this might be used to build a container running SSSD on
  OCP with a restricted profile.
* A new configure option ``--with-ldb-modules-path=PATH`` option to specify LDB
  modules path at build time.
* ``--with-allow-remote-domain-local-groups`` ``./configure`` option was
  removed.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* An option ``ipa_enable_dns_sites``, that never worked due to missing server
  side implementation, was removed.
* A new option ``pam_json_services`` is now available to enable JSON protocol to
  communicate the available authentication mechanisms.
* The default value of ``session_provider`` option was changed to ``none`` (i.e.
  disabled) no matter what ``id_provider`` used. Previously
  ``session_provider`` was enabled by default for ``id_provider = ipa`` case.
  The primary tool it was intended to support, "Fleet Commander," has become
  obsolete.
* The option ``ipa_subid_ranges_search_base`` was deprecated in favor of
  ``ldap_subid_ranges_search_base``.
* Support of previously deprecated ``ad_allow_remote_domain_local_groups``
  config option was removed completely.
* ``ipa_dyndns_update``, ``ipa_dyndns_ttl``, and ``ipa_dyndns_iface`` legacy
  options were removed.
* A new option, ``dyndns_address``, has been introduced to specify network
  addresses that are allowed or excluded from dynamic DNS updates. The
  ``dyndns_iface`` option has been extended to support the exclusion of network
  interfaces.

Tickets Fixed
-------------

* `#6439 <https://github.com/SSSD/sssd/issues/6439>`__ - dyndns_update and alias IP addresses getting registered
* `#7274 <https://github.com/SSSD/sssd/issues/7274>`__ - Clarify root permissions for KCM
* `#7921 <https://github.com/SSSD/sssd/issues/7921>`__ - AD user in external group is not cleared when expiring the cache
* `#7967 <https://github.com/SSSD/sssd/issues/7967>`__ - sssd client nss coredump
* `#7968 <https://github.com/SSSD/sssd/issues/7968>`__ - cache_credentials = true not working in sssd master
* `#8005 <https://github.com/SSSD/sssd/issues/8005>`__ - Socket activation doesn't work for 'sssd_pam'
* `#8021 <https://github.com/SSSD/sssd/issues/8021>`__ - potentially dangerous id mapping between local and domain users
* `#8022 <https://github.com/SSSD/sssd/issues/8022>`__ - sssd-idp is available but not functional on Fedora 42
* `#8030 <https://github.com/SSSD/sssd/issues/8030>`__ - Support subuid with generic LDAP provider
* `#8059 <https://github.com/SSSD/sssd/issues/8059>`__ - IPA idoverride and auto private groups - behavior change with the copr repo @sssd/nightly
* `#8089 <https://github.com/SSSD/sssd/issues/8089>`__ - Including innapropriate IPv6 addresses in dyndns_update
* `#8108 <https://github.com/SSSD/sssd/issues/8108>`__ - After I log in offline with a cached password hash, sssd stays offline forever because my account requires MFA
* `#8194 <https://github.com/SSSD/sssd/issues/8194>`__ - sss_nss: hang when looking up a group with stale cache entry and a LDAP provider
* `#8292 <https://github.com/SSSD/sssd/issues/8292>`__ - Test failure: ssh with OTP login in IPA environment
* `#8300 <https://github.com/SSSD/sssd/issues/8300>`__ - SSSD checks PAC from MIT Kerberos and fails
* `#8331 <https://github.com/SSSD/sssd/issues/8331>`__ - kerberos ccache filename is replaced on every concurrent login with the same user


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    Alexey Tikhonov (111):
        cd325f645  PAM: keep 'LISTEN_PID' and 'LISTEN_FDS'
        63976d827  'gemini-code-assist' config
        94151af9e  SPEC: add missing '\'
        6f448e1cc  UTILS: removed stray declaration
        78c140081  UTILS: moved code used only by 'monitor'
        f9b226b01  Moved define used by ldap_child only out
        03da01d74  libkrb5 passkey plugin doesn't use 'libsss_util.so'
        0fb034b7d  'libsss_cert' doesn't use 'libsss_child'
        c00c6e214  CHILD_COMMON: unify structs 'response' and 'io_buffer'
        03f526333  UTILS: split child helpers code
        24e9f9b15  UTILS: don't use shared 'IN_BUF_SIZE'
        91c528ac6  Helpers defined in 'child_utils.h' aren't really used in child processes.
        10ad5a0ca  Rename 'sss_child_ctx_old' -> 'sss_child_ctx'
        81b2f2041  New `sss_child_start()` helper
        47b544a37  KRB5: make use of `sss_child_start()`
        511b44b8e  LDAP: make use of `sss_child_start()`
        3b435ce3c  Delete 'exec_child()'
        92f977a46  IDP: make use of `sss_child_start()`
        afffec389  CHILD HELPERS: make activate_child_timeout_handler() internal
        9324feb8a  AD pw renewal: make use of `sss_child_start()`
        ce528fd55  AD GPO: make use of `sss_child_start()`
        5b72f1143  responder/ifp: use sss_child_start() for p11_child certificate validation
        9f2ac0886  sss_child_start(): allow NULL output _io arg
        e5f4348fb  SSH: refactor ssh_cert_to_ssh_key.c to use sss_child_start()
        839a73099  CHILD HELPERS: extend `sss_child_start()`
        96a7fc75d  AD GPO: handle stuck 'gpo_child'
        bd6dfc2cc  CHILD HELPERS: handle '--chain-id' as a basic arg
        452f205e6  IPA_SELINUX: make use of `sss_child_start()`
        9be8b15b2  PAM:CERT: make use of `sss_child_start()`
        0e8f8876e  PAM:PASSKEY: make use of `sss_child_start()`
        5e2586bb3  DYNDNS: make use of `sss_child_start()`
        db8a601d0  Cosmetics around close-fd helpers
        a831c0003  CHILD HELPERS: make `child_io_destructor()` private
        4cd3aac5a  CHILD HELPERS: make `child_handler_setup()` and `child_handler_destroy()` kind of "private".
        e4adf7e4a  CHILD HELPERS: make `exec_child_ex()` private
        9f2e11ca5  CHILD HELPERS: cosmetics around namings
        301dc67a1  CHILD HELPERS: check return code of `sss_fd_nonblocking()`
        fd92f450c  KRB5 PASSKEY PLUGIN: ensure space for NULL termination
        18cba6e7d  Cosmetics: indentation fix
        8bddb6a51  Renamed 'child_common.c' to 'child_handlers.c'
        b871b0cc2  CHILD HELPERS: make sure 'child_out_fd' isn't used
        7e8b62e0a  Make sure previously rotated logs are chown-ed as well.
        d8ac44297  spec: don't dereference links while chown-ing in %post
        878e5d627  SSS_CLIENT:MC: simplify logic and
        a6030b79c  Drop support of 'ad_allow_remote_domain_local_groups'
        4fca91791  conf: support only bool value for 'enumerate' option
        e60fcddbb  ENUMERATION: drop support of enumeration for IPA/AD
        bab9aa34e  KCM: corrected debug messages
        07b720ee4  KCM: verbosity
        b8b92dfea  KCM: don't trigger backtrace if 'uuid_by_name' fails
        f3af8c89a  CLIENT: fix thread unsafe access to autofs struct.
        488e540dd  gpo_child: don't include 'util/signal.c'
        2f3b3db88  OIDC_CHILD: fix compilation warning
        9c139765e  OIDC_CHILD: use `sss_erase_mem_securely()` wrapper
        acc75d16b  Get rid of useless `SSSD_MAIN_OPTS` define.
        21edc74dc  Makefile: tools do not need to link against 'sss_client' code
        2628fb926  Makefile: get rid of useless 'SSSD_LCL_TOOLS_OBJ'
        74b640627  Move 'DEBUG_CHAIN_ID_FMT_*' from 'util.h'
        bfa052d2d  Include <libintl.h> in 'debug.h'
        c186e2019  OIDC_CHILD: use DEBUG_CHAIN_ID_FMT_RID
        e97a22815  Helpers to do a basic setup of a child process.
        9e9c42002  KRB5_CHILD: use new helper to setup a process
        1f9c14448  OIDC_CHILD: use new helper to setup a process
        5ae5837fe  AD_GPO_CHILD: use new helper to setup a process
        ac5d345ea  P11_CHILD: use new helper to setup a process
        03a5279e2  PASSKEY_CHILD: use new helper to setup a process
        300a9621d  SELINUX_CHILD: use new helper to setup a process
        7ad2aa8f2  SELINUX_CHILD: fix includes
        167301955  DUMMY_CHILD TEST: use new helper to setup a process
        cbfba4ed1  DEBUG: use 'debug_prg_name' if 'debug_log_file' isn't set
        6aa7c9a04  PROXY_CHILD: use new helper to setup a process
        bbbd1504d  SPEC: require reasonably up to date 'libldb' version
        1d488d53c  CONTRIB:fedconfig: enable '--with-subid'
        fcbf23d46  MAN: fix missing `with_subid` condition
        6fcf7c3a8  SUBID:IPA: correct OC
        9901ed36c  SUBID: deprecate `ipa_subid_ranges_search_base`
        ae98d8e38  LDAP: add subid ranges support
        7a516505d  SUBID: don't require search bases to be set in advance
        9014ced63  man: document subid LDAP attributes
        0edeb89c3  DEBUG: lower debug level of several messages
        79028efff  SUBID: resolve owner DN instead of guessing
        f255e37fa  SUBID: sanitize range owner dn
        95994dd91  SUBID: trusted subdomains aren't currently supported
        407eda3e9  IFP: use correct error code for timeout
        4f3b98a8f  CHILD HANDLERS: add standard timeout handler
        b384d1f15  ad_machine_pw_renewal: remove unused variables
        863673729  ad_machine_pw_renewal: use sss_child_handle_timeout()
        d57290a08  PAM/P11: get rid of unused 'pam_check_cert_state::child_status'
        1019f9a8c  PAM/P11: use sss_child_handle_timeout()
        d97d14f27  PAM/PASSKEY: use sss_child_handle_timeout()
        7f3e0dccc  CHILD HELPERS: let generic timeout handler set 'io->in_use'
        bee133590  KRB5_CHILD: use sss_child_handle_timeout()
        a326df494  OIDC_CHILD: use sss_child_handle_timeout()
        87b8e5066  DYNDNS: use a proper 'timeout_handler'
        55c63c3d3  DYNDNS: use sss_child_handle_timeout()
        10f9eb290  PROXY: provide 'dumpable' and 'backtrace' args to child process
        ed230fc93  PROXY: delete unused define
        2ad8cbf97  PROXY: use `sss_child_handle_timeout()`
        ec3e97470  PAM/P11: debug message fixed
        2a1048b59  CONFIG: disable 'session_provider' by default
        407104127  IPA: remove 'ipa_enable_dns_sites' option
        87e72fd01  KCM: root can't access arbitrary KCM cache
        d9ab8a8a0  KRB5: let 'krb5_child' tolerate missing cap-set-id
        116f10e99  DP: use 'SSSDBG_CONF_SETTINGS' to log options
        16099f243  IDP: avoid logging value of 'idp_client_secret'
        44b938a2f  OIDC_CHILD: don't log 'post_data' content
        c3dc228b8  KRB5_CHILD: comment fixed
        6378238be  KRB5_CHILD: only setup/check ccache if can later use it
        2a991f2f4  KRB5_CHILD: use ruid/rgid instead of CAP_DAC_READ_SEARCH
        e2273e09a  KRB5_CHILD: allow `k5c_ccache_check()` during SSS_PAM_PREAUTH
        735fe23a2  KRB5_CHILD: don't check if FILE:/DIR: path accessible in advance

    Américo Monteiro (2):
        34d01e748  po: update translations
        63d82d9ce  po: update translations

    André Boscatto (1):
        e35516214  tests: Adding nested group test case for simple access control

    Arda Gurcan (1):
        e98a777ee  NSS: Reject empty name lookups in client library

    Dan Lavu (14):
        2d0291da7  adding pytest markers to help keep track of transformation status
        6f9aed5a3  tests: skipping simple access control tests that have been rewritten.
        2121f9b8d  removing deprecated pam_ldap pam_krb proxy provider multihost tests
        c3f3672a1  tests: improving sss_override to adhere to new guidelines
        e32903268  removing intg resolver test.
        3f708bda4  adding ldap resolver provider tests
        0cae6821b  test_infopipe, standardizing the provider amongst all tests
        f2ccc6e5f  updating some test logic and adding test cases
        a276441fe  removing intg ifp tests
        a9f9c5c4e  Replacing provider conditionals with set_server method
        fc159ed23  fixing and making automatic kcm renewal test more foriving
        449913a8a  adding subid test
        160bbb3f2  adding parametrized enumeration enabled tests
        5b5dce2fa  removing intg enumeration tests.

    Gleb Popov (25):
        dab5ca5ca  Introduce cli_creds_set_{u,g}id() macros and use them to fix the build on FreeBSD
        ead2e0e04  Make use of ucred helpers in tests
        93b041c9e  Provide the struct spwd definition if shadow.h isn't available
        791618a94  Fall back to ftruncate in case of CoW file system
        6760771a9  oidc_child: Use the sss_prctl wrapper
        30d6e9f1d  sbus_generate.sh: Use portable shebang
        06bdffe02  inotify.m4: Fix usage of $sss_extra_libdir
        c44491e76  Link sss_util to INOTIFY_LIBS, this module calls into inotify API
        b6455e0f4  Link test_inotify to INOTIFY_LIBS
        6d124aecc  Include sys/wait.h where needed
        0e66577e3  Introduce FreeBSD CI
        74d3adb08  SSSDConfig.py: Support running on FreeBSD
        6be934a49  FreeBSD CI: Put the job's output under logging groups
        445d374b1  FreeBSD CI: Install the softhsm2 dependency
        caab178df  Fix building of test_pam_srv.c on FreeBSD
        55c13ed99  When running on FreeBSD skip tests that are using fget{pw,gr}ent
        e6738a219  util-tests.c: Properly bring back the value of TZ
        16db74ca2  util-tests.c: Use TMPDIR (or fall back to /tmp) to store test's temporary files
        1c8958d1e  resolv-tests: Do not perform leak checking when running on FreeBSD
        14b285e52  test_iobuf.c: Only run the test_sss_iobuf_secure subtest on Linux
        56b247db5  strtonum.c: Clear errno if it was set to EINVAL to make behavior consistent
        a881e10da  file_watch.c: Do not pass IN_IGNORED to inotify_add_watch
        b0af250cf  config/cfg_rules.ini: Make regexp's more POSIX compliant
        47b38f178  sss_unique_file: Ensure correct group ownership on the created file
        9a776480a  check_file-tests: Ensure correct group ownership on the created file

    Hosted Weblate (1):
        4617eb2ab  po: update translations

    Iker Pedrosa (33):
        424ae7c62  ci: fix dependabot.yml schema validation
        fb4d5ad23  util: implement pam_get_response_data()
        bc4bfcd9e  sss_client: add EIdP to prompt_config structure
        af9459e10  Responder: tune prompts in the GUI
        316579af7  Responder: generate JSON message for GUI
        b04803459  Responder: unpack JSON reply from GUI
        2fda8e081  Responder: check PAM service file for JSON protocol
        b3dc37aaf  Responder: new option `pam_json_services`
        c5af066c0  Responder: call JSON message generation
        123252183  SSS_CLIENT: forward available auth JSON message
        48381a3f0  Responder: parse GUI reply
        e327f0d74  Test: adapt test_pam_srv to JSON message
        8d24366e5  Responder: check return value for json_string()
        7c70f1dc1  Responder: update JSON message format
        6c38800b6  sss_client: modify smartcard in prompt_config structure
        5f2fc24c1  util: implement pam_get_response_data_all_same_type()
        b4699ddbe  Responder: generate JSON message for smartcard
        0640200f0  Responder: parse reply for smartcard
        6011466b0  Responder: refactor JSON functions to reduce args
        18dd52646  Responder: extend smartcard JSON request message
        78ec10f28  Responder: extend smartcard JSON reply message
        be9164f28  Responder: make `decode_pam_passkey_msg()` public
        7e9e18e9f  Responder: generate JSON message for passkey
        efaa9c1de  util: implement function to set passkey PIN
        3cbf1aaa8  Responder: parse reply for passkey
        4cb99a248  krb5_child: advertise authentication methods
        bc1460c3d  Responder: fix passkey auth when user-verification is off
        6b40318a8  Responder: add `gdm-switchable-auth` to `pam_p11_allowed_services` defaults
        784982265  sss_client: prevent JSON auth during password change preauth
        aa2ac83f9  Responder: change authentication mechanism detection
        811ecc1f9  man: clarify and fix `pam_json_services` compilation
        cc1b9e029  krb5: port pre-authentication retry logic
        df15165db  krb5_child: fix OTP authentication for PAM stacked tokens

    Jakub Vávra (10):
        713da1341  Tests: Move test_ldap_referrals from gating (tier1)
        2d308e2e9  Tests: Add missing markers for ticket plugin
        0ceb44874  Tests: Move test_sssctl__analyze_without_root_privileges from gating
        ca0db6d5e  Tests: Make multihost custom-log more resilient.
        481700d49  Tests: Update polarion team name
        b301b1f57  Tests: Update keytab rotation tests.
        baeb2daad  Tests: Drop failing ported test_idmap
        c5e643185  Tests: Skip tests unstable on other architectures.
        bf23a6e94  Tests: Add umockdev and virtsmarcard as test dependencies
        9ed926242  Tests: Update test_0003_ad_parameters_junk_domain_invalid_keytab

    Justin Stephenson (34):
        6c29c14a2  UTIL: Add string_ends_with utility function
        e7a3cace2  CONFDB: Store domain ID override templates
        f1768ba70  SYSDB: Support ID override templates
        753c76f07  IPA: Support ID override templates
        3533bd5af  tests: Stabilize analyze child logs
        a38790fcf  ipa: remove IPA dyndns legacy options
        f84bc3336  tests: test_sssctl__analyze_child_logs handle timing issue
        17b9188f8  ci: Workaround pylibssh Failed to open session
        5e16b0de6  ci: Install libssh-dev
        9cbb08da8  sysdb: Execute override code even if no templates exist
        5aa8c23a6  tests: update test_sudo network utilities
        9c0ca193c  ipa: additional IPA hosts/hostgroups debugging
        cf562deb0  ci: constraints - pin to branch for pylibssh workaround
        2c2fd60df  ipa: Handle auto private group lookup with login override
        1c64f1c50  tests: auto private group lookup with login override
        be6359b8b  ci: Remove intgcheck on debian-latest
        520f9279d  ci: Update python version to latest minor version
        08a7195b0  ci: get changed script handle run for master push (non-PR)
        63639ecb1  ci: Override shell builtin bash options for get-changed script
        5a800d9c7  ci: remove pylibssh workaround
        40ee0a5c1  SYSDB: Add sysdb_add_bool()
        85b632d13  SYSDB: Dont store gid 0 for non-posix groups
        bedc2161a  SDAP: Remove sdap_store_group_with_gid()
        984d794a9  man: Clarify the user_attributes option
        f2e8e51a4  ipa: Fix typo in trust type conditional
        50527dc96  ipa: improve unknown trust type error return
        e9216fc1e  pam: Remove PAM_PASSKEY_VERIFICATION_OMIT mode
        304f298c9  pam: Skip passkey_local() in Kerberos auth flow
        879d07315  passkey: Remove SYSDB_PASSKEY_USER_VERIFICATION
        be5df3412  authtok: Set Kerberos passkey PIN to NULL when UV is false
        b0146aefc  util: Add string_begins_with() helper
        358a708fb  simple: Resolve group names in SID format
        4482fac2e  tests: Remove preferred topology from simple access test
        be8421707  tests: Update sssctl config-check tests

    Madhuri Upadhye (7):
        4e7ac3bb1  intg: Remove ldap_local_override_test.py
        1e3464a0f  Tests: Add IPA HBAC Test Cases for Validating Access Control Rules and Group Membership Refresh
        790228c87  tests: standardize HBAC test name format
        90fd80240  tests: Remove hardcoded domain and fix type errors in netgroup tests
        63771a1a3  tests: Add netgroup tests for incomplete triples and complex hierarchy
        2b43681d4  tests: Add netgroup offline and nested hierarchy
        6413f60b1  tests: add IPA ID view test for user lookup by email

    Mark Johnston (1):
        2d6ef923e  find_uid.c: Add FreeBSD implementation

    Ondrej Valousek (1):
        684e5683d  allow use machine credentials from trusted domain :relnote: SSSD now allows using machine credentials from a trusted AD domain or Kerberos realm if no suitable domain-local credentials are available

    Patrick Bruenn (1):
        38a6a4a79  BUILD: Accept krb5 1.22 for building the PAC plugin

    Pavel Březina (43):
        76bce06f1  Update version in version.m4 to track the next release
        44b6324e0  spec: remove old Obsoletes
        ab6d62423  spec: remove old Provides
        9bdc21729  spec: always build with sssd user
        cca790052  spec: always use sysusers to create the sssd user
        eefdd01a2  spec: remove build_subid condition as it is always enabled
        9d83e67f2  spec: always build kcm renewals
        538d745d3  spec: remove build_passkey as it is always enabled
        f9f1a8097  spec: build idp only on f43+ and rhel10+
        88ad51932  spec: remove _hardened_build
        0e3ceca17  spec: remove ldb_version
        6562eb881  spec: add comment to samba_package_version
        5b9b9ae4b  spec: move packages required for p11_child tests together
        85f41f91e  spec: remove systemtap-sdt-dtrace version condition
        dde42a2c7  spec: use upstream_version variable when producing downstream_version
        9e6f6a988  spec: use autochangelog
        3a59decab  spec: target f41+ and rhel10+
        5b342ca2e  spec: use version_no_tilde
        c7bf90643  spec: use correct url for the tarball
        caeeaf7c1  spec: support gpg verification
        1b884f056  ci: add packit configuration
        8daa3e11a  ci: remove custom copr builds
        87dae847d  packit: get version from version.m4 for upstream builds
        f7ad10cf8  SSSDConfig: allow last section to be empty
        c92580bdc  ci: add pre-commit configuration
        afd88cf05  ci: add python-system-tests as requirement to the result job
        c6d1d6995  whitespace: fix issues found by pre-commit
        6924d6782  ci: add automation for creating new release
        901a62320  ci: move build to standalone workflow
        bab82018e  ci: only run changed tests for test only changes
        6958eecde  ci: use parallel build
        2e5ad5b9e  ci: automatically add Reviewed-by trailer when Accepted label is set
        b85463686  ci: add autobackport workflow
        e557ac751  ci: remove final result job
        af225a0ef  ci: remove result job from analyze-target
        f100cb6d2  ci: remove result job from static-code-analysis
        6f4e1f9a4  ci: run long jobs only if Accepted label is not set
        d6ea55552  sbus: defer notification callbacks
        816eb1e20  cache_req: allow cache_first mode only if there is more than one domain
        00547f67a  tests: filter_groups by name and lookup by id with expired cache
        97fa9e775  intg: remove ent_test.py
        475752768  scripts: authenticate git push for release
        e6927eb94  scripts: use sssd-bot token for release script

    Samuel Cabrero (1):
        698f99202  SSSCTL: config-check: do not return an error if snippets directory does not exists

    Scott Poore (4):
        e92df278f  test: Add Passwordless GDM tests for External IdP
        0511cc275  system tests: add bare topologies to mhc.yaml
        05fa421b1  Tests:  Adding GDM Passkey tests
        502391658  intg: remove test_session_recording.py

    Sumit Bose (28):
        16d61ee1a  sysdb: add sysdb_get_direct_parents_ex()
        2a19873c8  ipa: improve handling of external group memberships
        297ecc467  authtok: add IS_PW_OR_ST_AUTHTOK()
        3b106f188  krb5: offline with SSS_AUTHTOK_TYPE_PAM_STACKED
        b17c6c5e6  ci: add missing intgcheck artifacts
        9f72fcd7f  ipa: improve handling of external group memberships
        2a388e751  tests: test removal of external group membership
        9939c39d1  krb5: disable Kerberos localauth an2ln plugin for AD/IPA
        fbf8ae713  tests: add pysss_nss_idmap system test
        399f7a273  intg: remove test_pysss_nss_idmap.py
        e95d3fe01  test: check is an2ln plugin is disabled or not
        c78855c19  tests: add test_pac_responder.py
        be020a3c4  intg: remove test_pac_responder.py
        e661b5390  ipa: filter DNs for ipa_add_trusted_memberships_send()
        7ddb51fdf  utils: add new error code ERR_CHECK_NEXT_AUTH_TYPE
        0adc2e778  krb5_child: use ERR_CHECK_NEXT_AUTH_TYPE instead of EAGAIN
        da82d1d5b  krb5_child: clarify EAGAIN returned by krb5_get_init_creds_password()
        d865ac345  ipa: check for empty trusts in ipa_get_trust_type()
        60ba493e9  krb5: fix OTP authentication
        9579e08cc  spec: clarify description of sssd-idp package
        794e80f4f  sysdb: add sysdb_search_user_by_upn_with_view_res()
        43f22b968  cache_req: use sysdb_search_user_by_upn_with_view_res()
        fe61b85b4  sysdb:: remove sysdb_getpwupn()
        6d8f9d7e9  tests: lookup user with overrides with email
        c12320108  pac: fix issue with pac_check=no_check
        72a42d5cb  sysdb: do not treat missing id-override as an error
        1a8c30250  ipa s2n: do not try to update user-private-group
        08c2ccf50  tests: check user lookup after view change

    Tomas Halman (10):
        fb00f4702  Exclude specific IP addresses from dynamic DNS updates
        997ffd1ae  tests: Migrate missing tests to new framework
        b01df9a4e  tests: Remove obsolete sssctl tests
        cf974c66a  tests: migrate sssctl tests to new framework
        b1d425a5e  Filter IPv6 addresses not suitable for DNS updates
        637b7bcb7  test: check temporary address exclusion
        1b7110438  IPA: Fail with short names
        481609659  IPA: remove re-declaration of `ipa_trusted_subdom_init`
        09f574f00  IPA: remove CONFDB_DEFAULT_FULL_NAME_FORMAT_INTERNAL
        836042459  tests: SSSD must refuse to start on IPA with short names

    Yuri Chornoivan (4):
        7acb8ef77  Fix typo in sssd-ldap.5.xml
        ac9fd622b  Fix typo in sssd-idp.5.xml
        417d32d01  Fix typos in sss-certmap.5.xml
        7b829bcd1  Update sss-certmap.5.xml

    aborah-sudo (3):
        576b8675c  Tests: Add additional Infopipe tests for untested interfaces
        a73ea6ebd  Tests: Refactor sssctl tests: consolidate and fix config-check
        5e7f36803  Tests: Add comprehensive sssctl functionality tests

    dependabot[bot] (7):
        a0383378e  build(deps): bump actions/checkout from 4 to 5
        0d31ab57a  build(deps): bump actions/setup-python from 5 to 6
        925c9d32c  build(deps): bump github/codeql-action from 3 to 4
        0fb839ad1  build(deps): bump actions/upload-artifact from 4 to 5
        8942d3000  ci: bump cross-platform-actions/action from 0.29.0 to 0.32.0
        4d68ca714  ci: bump actions/checkout from 4 to 6
        1280ffe06  ci: bump actions/upload-artifact from 5 to 6

    fossdd (1):
        fbeba7ac2  sss_prctl: avoid redefinition of prctl_mm_map

    krishnavema (2):
        8c32d7fae  tests: adding user su smartcard login test
        0d2b75f43  tests:Added IPA Certificate Authority Tests

    liberodark (1):
        7a903e83e  confdb: Add --with-ldb-modules-path configure option

    shridhargadekar (5):
        9856b6dda  Tests: cache_credentials = true not working
        b33327ac3  Tests: Adjusting priority of a test case
        80ccb593c  Test: HBAC affecting AD-users ipa-group membership
        ec81ea23b  Tests: ADuser external group cache update
        a0574f78d  Tests: Rectify the docstring n testcode

    sssd-bot (2):
        6749ec8b1  pot: update pot files
        1a1cf163b  Release sssd-2.12.0

