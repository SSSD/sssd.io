SSSD 2.10.0 Release Notes
=========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* **IMPORTANT note for downstream maintainers!**

  This release features significant improvements of "running with less
  privileges (under   unprivileged service user)" feature. There is still a
  ``./configure`` option ``--with-sssd-user=`` available that allows downstream
  package maintainers to choose if support of non-root service user should be
  built. In case such support is built, a preferred way to configure service
  user is simply by starting SSSD under this user; for example, using
  ``User=/Group=`` options of systemd sssd.service file. Upstream defaults are
  to build ``--with-sssd-user=sssd`` and to install systemd service with
  ``User=/Group=sssd``. In this case, only several helper processes -
  ``ldap_child``, ``krb5_child`` and ``selinux_child`` - are executed with
  elevated capabilities (that are now granted using fine grained file
  capabilities instead of SUID bit). All other SSSD components run without any
  capabilities. In this scenario it's still possible to re-configure SSSD to run
  under ``root`` (if needed for some reason): besides changing ``User/Group=``
  options, some other tweaks of systemd service files are required.

  A legacy method to configure a service user - sssd.conf ``user`` option - is
  now deprecated and its support isn’t built by default. It can be enabled using
  ``--with-conf-service-user-support`` ``./configure`` option if needed (for
  example, due to backward compatibility requirements of stable releases).

  Further, no matter if SSSD is built ``--with-sssd-user=sssd`` or
  ``--with-sssd-user=root``, when it's configured to run under ``root`` (in both
  cases) it still runs without capabilities, the same way as when it's
  configured to run under ``sssd`` user. The only difference is from the DAC
  perspective.

  Important note: owner of ``/etc/sssd/sssd.conf`` file (and snippets) should
  match the user configured to start SSSD service. Upstream spec file and
  service files change ownership of existing ``sssd.conf`` to sssd during
  package installation and at runtime for seamless upgrades / transition period
  only.

  Additionally, this release fixes a large number of issues with "socket
  activation of responders" feature, making it operable out-of-the-box when the
  package is built ``--with-sssd-user=sssd``. Please take a note, that user
  configured to run main sssd.service and socket activated responders (if used)
  should match (i.e. if sssd.service is re-configured from upstream defaults to
  ``root`` then responders services also should be re-configured).

  Downstream package maintainers are advised to carefully inspect changes in
  ``contrib/sssd.spec.in``, ``src/sysv/systemd/*`` and ``./configure`` options
  that this release brings!

* sssctl ``cache-upgrade`` command was removed. SSSD performs automatic upgrades
  at startup when needed.

* Support of ``enumeration`` feature (i.e. ability to list all users/groups
  using ``getent passwd/group`` without argument) for AD/IPA providers is
  deprecated and might be removed in further releases. Those who are interested
  to keep using it awhile should configure its build explicitly using
  ``--with-extended-enumeration-support`` ./configure option.

* A number of minor glitches of ``sssd-2.10.0-beta1`` around building and
  packaging were fixed.

New features
~~~~~~~~~~~~

* The new tool ``sss_ssh_knownhosts`` can be used with ssh's
  ``KnownHostsCommand`` configuration option to retrieve the host's public keys
  from a remote server (FreeIPA, LDAP, etc.). This new tool, which is more
  reliable, replaces ``sss_ssh_knownhostsproxy``. The latter is no longer built
  by default, but its build can be forced with the ``./configure`` option
  ``--with-ssh-known-hosts-proxy``.

Packaging changes
~~~~~~~~~~~~~~~~~

* Building SSSD now unconditionally requires availability of ``ucred``/
  ``SO_PEERCRED`` to enforce certain security checks at runtime (see ``man 7
  unix`` for details).

* SSSD now requires ``libini`` not older than v1.3

* Explicit ``--with-semanage`` ./configure switch was removed, going forward
  ``--with-selinux`` includes this.

* ``sssd_pam`` binary lost public ``rx`` bits and got ``cap_dac_read_search=p``
  file capability to be able to use GSSAPI

* Support of OpenSSL older than 1.0.1 was dropped

* Support of ``--without-infopipe`` ``./configure`` option was dropped. Feature
  is long time out of experimental state. Since building it doesn't require any
  additional dependencies, there is not much sense to keep option available.
  Those who not interested in feature can skip installing sssd-ifp sub-package.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* Default ``ldap_id_use_start_tls`` value changed from ``false`` to ``true`` for
  improved security.

* Added a ``ldap_use_ppolicy`` option for backends with broken ppolicy extension
  handling.

* Obsolete ``config_file_version`` option was removed.

* Option ``reconnection_retries`` was removed since it is no longer used. SSSD
  switch to a new architecte of internal IPC between SSSD processes where
  responders do not connect to backend anymore and therefore this option is no
  longer used.

Tickets Fixed
-------------

* `#3686 <https://github.com/SSSD/sssd/issues/3686>`__ - [RFE] Support GPOs from different domain controllers
* `#4523 <https://github.com/SSSD/sssd/issues/4523>`__ - TOOLS: Add feature to delete the cached GPOs
* `#4659 <https://github.com/SSSD/sssd/issues/4659>`__ - Make Fleet Commander related code work for unprivileged users
* `#5013 <https://github.com/SSSD/sssd/issues/5013>`__ - Duplicate sssd_pac process when using IPA backend
* `#5022 <https://github.com/SSSD/sssd/issues/5022>`__ - socket activated services incompatible with default implicit sssd.conf
* `#5198 <https://github.com/SSSD/sssd/issues/5198>`__ - monatomically should have been monotonically
* `#5418 <https://github.com/SSSD/sssd/issues/5418>`__ - Problem with transition user's credentials through pam-stack
* `#5518 <https://github.com/SSSD/sssd/issues/5518>`__ - openssh 8.5 will support KnownHostsCommand
* `#5536 <https://github.com/SSSD/sssd/issues/5536>`__ - Backend running as non-root user cannot kill child processes after timeout
* `#5708 <https://github.com/SSSD/sssd/issues/5708>`__ - SSSD incorrectly works with AD GPO during user login
* `#5861 <https://github.com/SSSD/sssd/issues/5861>`__ - openssl3 deprecated some functions
* `#6286 <https://github.com/SSSD/sssd/issues/6286>`__ - Problem with routing when name of destination is added to the request key
* `#6442 <https://github.com/SSSD/sssd/issues/6442>`__ - PAC errors when no PAC configured
* `#6647 <https://github.com/SSSD/sssd/issues/6647>`__ - sssd fails to compile with --with-selinux=no
* `#6652 <https://github.com/SSSD/sssd/issues/6652>`__ - IPA: previously cached netgroup member is not remove correctly after it is removed from ipa
* `#6659 <https://github.com/SSSD/sssd/issues/6659>`__ - sssd_be segfault at 0 ip 00007f16b5fcab7e sp 00007fffc1cc0988 error 4 in libc-2.28.so[7f16b5e72000+1bc000]
* `#6666 <https://github.com/SSSD/sssd/issues/6666>`__ - LDAP bind fails, but basic ldap tools work
* `#6718 <https://github.com/SSSD/sssd/issues/6718>`__ - file_watch-tests fail in v2.9.0 on Arch Linux
* `#6720 <https://github.com/SSSD/sssd/issues/6720>`__ - [sssd] User lookup on IPA client fails with 's2n get_fqlist request failed'
* `#6733 <https://github.com/SSSD/sssd/issues/6733>`__ - New covscan errors in 'passkey' code
* `#6739 <https://github.com/SSSD/sssd/issues/6739>`__ - autofs mounts: Access to non-existent file very slow since 2.9.0
* `#6744 <https://github.com/SSSD/sssd/issues/6744>`__ - sssd-be tends to run out of system resources, hitting the maximum number of open files
* `#6766 <https://github.com/SSSD/sssd/issues/6766>`__ - [RHEL8] sssd : AD user login problem when modify ldap_user_name= name and restricted by GPO Policy
* `#6768 <https://github.com/SSSD/sssd/issues/6768>`__ - [RHEL8] sssd attempts LDAP password modify extended op after BIND failure
* `#6790 <https://github.com/SSSD/sssd/issues/6790>`__ - gpo_child process terminates with SIGSEGV.
* `#6802 <https://github.com/SSSD/sssd/issues/6802>`__ - sss_certmap_test fail in v2.9.1 on Arch Linux
* `#6803 <https://github.com/SSSD/sssd/issues/6803>`__ - [sssd] SSSD enters failed state after heavy load in the system
* `#6889 <https://github.com/SSSD/sssd/issues/6889>`__ - Crash in `pam_passkey_auth_done`
* `#6897 <https://github.com/SSSD/sssd/issues/6897>`__ - Monitor attaches service d-tor to a wrong sbus connection
* `#6911 <https://github.com/SSSD/sssd/issues/6911>`__ - SBUS chaining is broken for getAccountInfo and other internal D-Bus calls
* `#6920 <https://github.com/SSSD/sssd/issues/6920>`__ - sssd-sudo missing debug statement in its .service file
* `#6922 <https://github.com/SSSD/sssd/issues/6922>`__ - ‘CURLOPT_PROTOCOLS’ is deprecated
* `#6926 <https://github.com/SSSD/sssd/issues/6926>`__ - KCM should handle its own configuration itself
* `#6942 <https://github.com/SSSD/sssd/issues/6942>`__ - SSSD goes offline during initgroups of trusted user if a group is missing SID
* `#6956 <https://github.com/SSSD/sssd/issues/6956>`__ - Incorrect handling of reverse IPv6 update results in update failure
* `#6986 <https://github.com/SSSD/sssd/issues/6986>`__ - The sss_nss_mc_destroy_ctx() function will close the TCP socket of the daemon process
* `#7007 <https://github.com/SSSD/sssd/issues/7007>`__ - pamstack_oldauthtok is not used during prelim check
* `#7009 <https://github.com/SSSD/sssd/issues/7009>`__ - sssd-2.9.2-1.el8 breaks smart card authentication
* `#7011 <https://github.com/SSSD/sssd/issues/7011>`__ - Smart card reader with pinpad
* `#7014 <https://github.com/SSSD/sssd/issues/7014>`__ - Reduce the amount of memory allocated by KCM and avoid zeroing it when not necessary
* `#7061 <https://github.com/SSSD/sssd/issues/7061>`__ - sssd_pam segfaults during password-based SSH-login
* `#7072 <https://github.com/SSSD/sssd/issues/7072>`__ - sssd_kcm "leaks" around 86MiB of memory per day
* `#7084 <https://github.com/SSSD/sssd/issues/7084>`__ - Invalid handling groups from child domain
* `#7094 <https://github.com/SSSD/sssd/issues/7094>`__ - Incorrect IdM product name in man sssd.conf
* `#7109 <https://github.com/SSSD/sssd/issues/7109>`__ - gdm smartcard login fails with "system error 4" in case of multiple identities
* `#7136 <https://github.com/SSSD/sssd/issues/7136>`__ - Improve documentation for allowing e-mail address as username
* `#7152 <https://github.com/SSSD/sssd/issues/7152>`__ - passkey cannot fall back to password
* `#7173 <https://github.com/SSSD/sssd/issues/7173>`__ - AD users are unable to log in due to case sensitivity of user because the domain is found as an alias to the email address.
* `#7189 <https://github.com/SSSD/sssd/issues/7189>`__ - socket leak
* `#7197 <https://github.com/SSSD/sssd/issues/7197>`__ - Errors in krb5_child.log every time a user authenticates - Pre-authentication failed: No pkinit_anchors supplied
* `#7232 <https://github.com/SSSD/sssd/issues/7232>`__ - error: The following pages are not translated ./sss_ssh_knownhosts.1.xml
* `#7250 <https://github.com/SSSD/sssd/issues/7250>`__ - SSSD is not fully registering the domains if the cache is empty
* `#7278 <https://github.com/SSSD/sssd/issues/7278>`__ - sssd master build failure
* `#7284 <https://github.com/SSSD/sssd/issues/7284>`__ - sssd master fails console login
* `#7319 <https://github.com/SSSD/sssd/issues/7319>`__ - PAC and PAM responders can crash if backend takes too long time to process getDomains()
* `#7375 <https://github.com/SSSD/sssd/issues/7375>`__ - [RFE] Add option to configure timeout to reconnect to primary servers
* `#7404 <https://github.com/SSSD/sssd/issues/7404>`__ - CRL option soft_crl doesn't check CRL at all, if nextupdate date has passed
* `#7411 <https://github.com/SSSD/sssd/issues/7411>`__ - GPO application fails with more > 1host in security filter
* `#7449 <https://github.com/SSSD/sssd/issues/7449>`__ - Man pages broken
* `#7451 <https://github.com/SSSD/sssd/issues/7451>`__ - sssd is skipping GPO evaluation with auto_private_groups
* `#7456 <https://github.com/SSSD/sssd/issues/7456>`__ - 2FA is being enforced after upgrading 2.9.1->2.9.4
* `#7502 <https://github.com/SSSD/sssd/issues/7502>`__ - Remove leftovers of old reconnection code
* `#7503 <https://github.com/SSSD/sssd/issues/7503>`__ - Pending (chained) DP requests aren't processed if backend restarts (affected sssd-2.10+)
* `#7532 <https://github.com/SSSD/sssd/issues/7532>`__ - EL9/CentOS Stream 9 lost offline smart card authentication
* `#7590 <https://github.com/SSSD/sssd/issues/7590>`__ - GPO access control might fail if ldap_user_name is set
* `#7606 <https://github.com/SSSD/sssd/issues/7606>`__ - Deprecated code used in 'sss_client/pam_sss.c'

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.0..2.10.0

    Abhijit Roy (2):
        3788f4800  sssctl: Adding options for nss
        be8913eb8  sdap_idmap: Enabling further debugging for to understand the underlying reason for Could not convert objectSID.

    Alejandro López (50):
        b2a4ff2aa  FILE WATCH: Callback not executed on link or relative path
        90c549072  TESTS: Fix doble slash comments
        1d69fdb73  SYSDB: Make enum sysdb_obj_type public
        99d0ab82e  IPA: Use a more specific filter when searching for BE_REQ_USER_AND_GROUP
        7f2881647  PAM: Fix a possible segmentation fault
        dc9466e73  AD: The shortcut must be used equally on _send() and _done()
        ca7c9f606  TEST: Fix pam-srv-tests to correctly treat the test name
        dc508f032  IPA: Do not try to add duplicate values to the LDAP attributes
        1b45f29f4  UTIL: New function string_in_list_size()
        2b8fed591  UTIL: add_strings_lists() becomes add_strings_lists_ex()
        de258f011  RESPONDER: attr_in_list() is replaced by string_in_list_size()
        b50415978  IPA: Do not duplicate the entry attributes.
        2c59fd211  NSS: Replace notification message by a less scary one
        22f8eee9c  UTILS: Create a macro for the --config option
        049edefec  UTILS: Add the db file name to server_setup()'s parameters
        7cc28f327  CONFDB: Allow loading an empty configuration
        e6c1d3abc  CONFDB: Fixed some missing dependencies in a header file
        0485342f7  KCM: Handle its own configuration
        93ee0159a  KCM: Remove the oldest expired credential if no more space.
        96d8b77ae  KCM: Display in the log the limit as set by the user
        e01378ae7  CI: Corrected the path to the logs
        58c7b6479  KCM: Clean the pipe after the test has finished
        54744f295  TESTS: Give KDC time to initialize
        230e7757a  LOGROTATE: logrotate should also signal sssd_kcm
        c73b7eb80  KCM: Replace a hard-coded constant by a macro
        3cba6d115  KCM: Fixed a wrong check
        126920546  KCM: Remove unused cc_be_type from struct kcm_ccdb
        2eb67afc0  KCM: When freeing the client, check that it is not NULL.
        edb63cde4  KCM: sss_iobuf_init_empty() shall not zero memory
        fe6c35add  KCM: Reduce the amount of memory allocated for the packages
        b4f9f63bd  KCM: Do not zero memory when not need.
        cbae68553  KCM: Fix a memory "leak"
        54395cbe3  KCM: sss_iobuf_get_*() functions must take a const struct
        4c159b019  TESTS: Make the AS_STR() macro available in common.h
        747c85f82  KCM: Securely erase memory used for secrets
        953c6bee4  SSH: Support ssh's KnownHostsCommand
        018de1c0d  MAN: sss_ssh_knownhosts.1 must also be translated
        2bb00e25d  TESTS: Improvements to test_iobuf
        c67e41d8d  SSH: Make sss_ssh_knownhostsproxy build conditional
        e556bfd0d  TESTS: Fix the ssh configuration
        c858d577c  TESTS: Fix the ssh configuration - II
        be42ada11  BACKENDS: Move the netlink watching to the backends
        ce9924c3a  TEST: Exclude libnl-3 from valgrind tests
        b821c77f2  MAN: Make disable_netlink in `man sssd.conf` conditional
        77f224674  MAN PAGES: Fix broken man pages
        3d1bf5d89  SSH: Remove two unused configuration options
        6c1d2aac8  TESTS: Add example tests for D-Bus
        823d78702  SSH: sss_ssh_knownhosts must accept port numbers
        1c91ea05c  MONITOR: Link DbusConnection and sbus_connection
        e0ec488c1  MONITOR: Set destructor for the right connection

    Alexander Bokovoy (1):
        dceb7df59  install udev rules to access security tokens by sssd-passkey

    Alexey Tikhonov (248):
        df8472ccb  MAN: fix issue with multithread build
        076a1136a  RESPONDER: avoid log backtrace in case access denined
        74d0f4538  BUILD: Accept krb5 1.21 for building the PAC plugin
        2fd5374fd  SYSDB: in case (ignore_group_members == true) group is actually complete
        f6bbd591d  KRB5: avoid another attempt to free 'cc' in 'done:' section if first attempt failed.
        ff5096bb7  KRB5: use proper function to deallocate mem
        7f308c6fe  KRB5: avoid FORWARD_NULL
        b69ff375a  KRB5: fix memory leak
        758227017  KRB5: fix memory leak
        a83be8fb5  KRB5: avoid RESOURCE_LEAK
        01f0d067f  KRB5: fixed RESOURCE_LEAK
        fd7da517d  LDAP: fixed RESOURCE_LEAK
        eca00ef47  LDAP: fixed leak of `kprinc`
        d02533cac  UTILS: fixed USE_AFTER_FREE
        9240bca7d  ENUMERATION: conditional build of enumeration support for providers other than LDAP
        e91a90cf0  SPEC: sync with Fedora spec file
        7902bd6e1  SPEC: make permissions of config folders consistent
        a540f914c  TOOLS: get rid of strings duplications
        91d32fee1  SPEC: make ownership of sssd.conf consistent with config folders.
        fcfffb5cf  UTILS: swap order of seteuid()/setegid()
        9380c8eff  SBUS: warn loudly if bus denies access
        d91c944c9  IFP: add a comment to 'org.freedesktop.sssd.infopipe.service' to avoid potential confusion
        16d3308b4  MAN: only mention 'files' provider if its support is built
        7f7cfc92c  PROXY: missing `proxy_resolver_lib_name` isn't an error
        8079d93ff  Fix compilation warning ``` ../src/responder/pam/pamsrv_cmd.c: In function ‘pam_reply’: ../src/responder/pam/pamsrv_cmd.c:1188:10: warning: unused variable ‘pk_preauth_done’ [-Wunused-variable] 1188 | bool pk_preauth_done = false; ``` in case SSSD is built without 'passkey' support.
        ae3bac934  CONF: allow 'sssd:sssd' ownership for config snippets
        9fe559402  DP: ENOTSUP isn't a fatal failure for target c-tor
        41427f957  IFP: allow running under non-root user
        15a22136e  UTILS: remove unused code (files manipulations)
        12a2033e0  SPEC: restore proper ownership of `deskprofilepath` broken in d163a120b922a49b458dc9568d90c4066cee2d73
        daf6096de  SPEC: `gpocachepath` doesn't need public r-x access
        7d14e529c  UTILS: include name of the file that failed perform_checks() in the debug log
        c4b5fda55  Get rid of '--dbus-activated'.
        50e7891bc  CONFDB: removed unneeded wrapper
        b639f335d  CONF: there is no use for CONFDB_FALLBACK_CONFIG
        e0903de48  SBUS: additional details in debug messages
        abd91303f  MONITOR: debug messages updates
        49f59cd43  SYSTEMD: removed unneeded capabilities
        19c741c48  SYSV/NSS: avoid chmod() in sssd_nss
        9cb397280  SYSTEMD::IFP: don't restrict ExecStartPre=chown(log)
        8e1d2bb47  SYSTEMD: replace deprecated 'PermissionsStartOnly=true' with '+'
        9d7dd81c0  SYSTEMD: several comments to service files
        01bee47a1  SUDO service: ${DEBUG_LOGGER} was missed for 'sudo'
        b90021b82  CONFDB: get rid of "lastUpdate"
        e57093067  CONFDB: get rid of 'config_file_version'.
        9efd79b01  SSSDConfig: use 'setuptools' instead of 'distutils'
        0a254e434  BUILD: get rid of `--with-semanage` ./configure switch
        88d8afbb1  MC: a couple of additions to 'recover from invalid memory cache size' patch
        086e46f1f  Stop supporting libini older than 1.3
        421a818f8  configure: use 'LDB_CFLAGS'
        b0212b04f  SSS_CLIENT: replace `__thread` with `pthread_*specific()`
        ed4b1a5b1  RESPONDER: remove unused code
        afabbb95e  BUILD: make support of 'ucred' a hard requirement
        246ae4497  RESPONDER: rely on SO_PEERCRED instead of socket path
        62732b697  PAM: get rid of private socket as it's not used anymore
        db1a919ff  RESPONDER: get rid of "private pipes" completely.
        8c8702803  CLIENT:NSS: never resolve 'sssd' user/group
        1451c6e03  CLIENT:PAM: trust peer if it runs under 0 or SSSD_USER uid
        b6f44f103  INTG-TESTS: fake SO_PEERCRED on responder side as well
        a3a376218  RESPONDER: protection from (cctx->cmd_line == NULL)
        4b0c58be5  RESPONDER: protection from failed `snprintf()`
        3eae4cc52  SPEC: 'sssd-proxy' requires 'libsss_certmap.so'
        2617dcfd6  UTIL: use proper specifier for 'DEBUG_CHAIN_ID_FMT_*'
        098bf64a0  Don't provide 'uint64_t' as POPT_ARG_LONG.
        2a3e47af2  CLIENT: move all socket paths checks to a single function
        41f8a6892  CLIENT: remove check for rw-rw-rw-
        4255a0fed  KRB5: a comment to explain the need for explicit `sss_pac_check_and_open()`
        079f433db  CLIENT: reduce code duplication
        57ed0de68  CLIENT: add an optional check of server credentials
        1f8ec39c3  CLIENT: reduce code duplication
        4e1a794f8  CLIENT: SUDO: force check of server credentials
        32b67e67c  CLIENT: move sudo/autofs/ssh related code
        8d0a88eee  SUDO: refuse to serve clients running under non-root
        ff2a7118e  SUDO: make 'sssd_sudo' socket sssd:sssd owned
        4a01583f0  PAM: no need for root:root owned socket
        4d6551e8b  RESPONDER: remove support for custom pipe_fd
        8f58e22ac  SUDO: don't overwrite major error code with minor one
        ad70f159f  CLIENT: fixed a mistype in `check_socket_cred()`
        271bb6c7a  CLIENT: fix covscan complain
        39cd0baa0  DP: reduce log level in case a responder asks for unknown domain
        5bbc14658  CI: don't run sssd-2.10+ on 'centos-8'
        97c05c4e3  LOGS: added missing new line
        c4e80942f  SYSTEM TESTS: run core set of tests against SSSD
        958a5e25c  SSS_CLIENT: MC: in case mem-cache file validation fails,
        0344c41ac  SSS_CLIENT: check if mem-cache fd was hijacked
        2bcfb7f92  SSS_CLIENT: check if reponder socket was hijacked
        d6940c6f9  P11_CHILD: reduce code duplication
        4cdb41751  DEBUG: added missing new line
        0c1d11bcb  SERVER: `setpgid()`:
        522b98c9b  CLIENT:NSS: never resolve initgroups for 'sssd' user
        059b58f76  SERVICES: allow to run socket activated sssd_nss under SSSD_USER
        a7851156e  PROXY: strip SUID bit off 'proxy_child'
        b4b72aacc  LDAP: move `select_principal_from_keytab()` to 'ldap_child'
        28068cdb8  MONITOR: remove MONITOR_DEF_FORCE_TIME
        dd7aaaf2f  MONITOR: switch user to configured before exec(service)
        ec77ec4e8  SPEC: clean up mem-cache files on uninstall
        6dba6c4b4  MONITOR: proper error check of failed `prctl()`
        c11734eb6  Fleet commander: store deskprofiles under user running SSSD
        2ef0f838e  IFP: don't trigger backtrace in case of ACL check fail
        859f58118  TESTS: multihost: chown sssd.conf to service user
        895b462d7  TESTS: multihost: make get_property() with older 'systemctl'
        c6c333def  UTILS: additional debug if `mkstemp()` fails
        40e5309a0  MONITOR: remove useless trailing '\'
        40cea81b1  MONITOR: remove 'opt_netlinkoff' removal notice
        419120f4a  MONITOR: replace fprintf() with ERROR()
        d79e0e74e  MNITOR: cosmetics
        102c30a57  MONITOR: get rid of unsed FLAGS_GEN_CONF definition
        47da0b6bc  SPEC: make most folders group accessible
        521f88ef8  SPEC: make '%{pipepath}/private' sssd:sssd owned
        52fa441b9  Make all SSSD processes a member of sssd supplementary group.
        60853c6fa  NSS: don't `fchown()` mem-cache files
        f4ad8c2ab  UTILS: add capabilities management helpers
        4a44cca40  Get rid of `--genconf` and `--genconf-section` monitor options.
        8d1b3ef7e  SSS_INI: const correctness
        cff8e1f99  CONFDB: split confdb_setup() into 2 steps
        b1cbf5f59  CONFDB: always delete old ldb-file
        87b77a011  MONITOR: no need to read domain list twice
        e306d93f9  MONITOR: remove unused mt_ctx::conf_path
        34f7c2eac  MONITOR: move keyring setup code to a function
        fd23a94ff  MONITOR: move nscd check code to a function
        a05b02506  SSS_INI: remove 'const' specifier from getter
        d7042fed2  DEBUG: a couple of message changes
        0d686b5d7  TOOLS: remove the upgrade-cache command
        5bd52025e  SYSTEMD: remove unused CAP_KILL
        304fe7541  SYSTEMD: responders do not need any capabilities
        1ea6965c9  MONITOR: startup logic was changed
        0e2ed444e  KRB5_/LDAP_CHILD: print capabilities at startup
        2a59991be  sssd.service: run under SSSD_USER by default
        4c42ca7a9  SPEC: make sure cache files are accessible
        aa7cddfa9  SPEC: make sure config files are accesible
        b88d56a39  SYSTEMD: KCM capabilities
        9fbaf6d74  SSS_INI: only check file ownership from 'sssd'
        583ea7f2d  SYSTEMD: remove "PIDFile="
        6ca4e4722  CONF: store pid file in /run/sssd
        29b1e474c  UTILS: make pidfile readable by everyone
        e2c26e810  SPEC: replace SUID bit with more fine-grained capabilities
        84c3034dc  SYSTEMD: set "SecureBits=noroot noroot-locked"
        9eed3873a  SPEC: make conf folder g+rx
        07f00135f  TESTS: system: skip 'passkey' tests if SSSD runs under non-root
        869ee9652  SPEC: build Fedora >= 41 package with sssd user support
        d45b85b7c  SSSDConfig: chown() sssd.conf to SSSD service user
        128777896  MONITOR: free 'tmp_ctx' in case of failure too
        e37a8c789  MAN: 'monitor' exit codes description
        cb4dbea61  SPEC/SYSTEMD: try harder making sure logs ownership matches service user
        4085ee079  UTILS: inotify: avoid potential NULL deref
        6dec94468  BUILD: only link SYSTEMD_DAEMON_LIBS if needed
        de928a283  BUILD: only search for SYSTEMD libs if needed
        c3578ad6f  BUILD: require initscript=systemd for syslog=journald
        4d29b915a  BUILD: don't use '--disable-dbus-tests'
        ce9488d6b  INTG-TESTS: replace '--without-semanage' with '--without-selinux'
        12e743234  BUILD: link 'krb5_child' against 'libsystemd' if needed
        01d09bb87  SPEC: use sysusers as additional source
        5045e4344  SPEC: enabled 'sysusers' for f-41+
        5b9a2f813  SPEC: define a home dir for 'sssd' user
        b67a29ff5  SPEC: suppress `chown` errors
        c25568fce  SPEC: build RHEL9 `--with-libsifp`
        57c4ccdca  BUILD: get rid of `--with-semanage` leftovers
        ab2671c00  DEBUG: reduce log level in case a responder asks for unknown domain
        0515eac56  TESTS: 'config_file_version' option doesn't exist
        65ca6725f  CI: remove unused stuff (lcov, ...)
        0f0aaa25e  CI: drop support of centos-stream-8
        61e7372c8  CI: enable centos-stream-10
        d8e831164  PAC: add 'sssd' user to the list of 'allowed_uids'
        92c902abd  BUILD: make support of 'sssd.conf::user' option configurable
        a226b2450  SPEC: manage /run/sssd using tmpfiles.d
        b3a487a4d  LDAP_CHILD: replace `become_user()` with `sss_drop_all_caps()`
        2891e7462  KRB5_CHILD: keep 'set-user-ID' in `k5c_become_user()`
        dc637c973  RESPONDER: use proper context for getDomains()
        ef66a27ab  KCM: run under SSSD_USER by default
        18aecfd42  make install: catch up with the spec-file
        f58be95ce  MAKE: only add 'AmbientCapabilities' template if
        7bab23612  SYSTEMD: chown() sssd.conf in service file
        5531e1de5  SYSTEMD: don't chown() logs
        a008accec  TOOLS: don't overwrite config.ldb
        19df6a5d2  SSH: sanity check to please coverity
        7c913edc8  CLIENT:idmap: fix coverity warning
        f32b021eb  MONITOR: increase 'services_startup_timeout'
        6de231d76  MONITOR: quit if any of providers didn't start
        ac6536d13  CI: remove http-parser dependency
        3dc8f6926  KRB5: make sure `get_tgt_times()` always set `tgtt`
        2e3f1ab7d  KRB5: TGT RENEWAL: try renew old ccaches immediately
        671a4de2e  KRB5: TGT RENEWAL: avoid flooding KDC
        eb334ccd7  KRB5: make sure FILE: TGT is still renewable
        5fc9590e2  CLIENT: a bit more accurate data type handling
        6db9030f8  SPDX migration
        1812aaf7b  SPEC: strip public rx bits from 'proxy_child'
        fc5c1a1af  UTILS: reduce log level if `sss_krb5_touch_config()` fails
        58da100df  ENUMERATION: enable support for 'proxy' provider
        0562646cc  PAM: grant 'cap_dac_read_search=p' to sssd_pam
        b1ce55a91  DEBUG: added missing newline
        fc2a26c30  TS_CACHE: never try to upgrade timestamps cache
        f0d45464c  SYSDB: remove index on `dataExpireTimestamp`
        5e77d3d44  sssd.supp: remove outdated entries
        6283742c4  sssd.supp: suppress invalid read in dlopen
        7c83a7600  SPEC: add new systemtap-sdt-dtrace to build deps
        e4ae4d612  BUILD: configure logrotate to work with non-root-group writable folder
        a7d0bbeb5  SPEC: merge 'sssd-polkit-rules' into 'sssd-common'
        ec7a80f91  CI: capture full 'config.log' from ./configure
        78cf0cf25  TESTS: don't use deprecated 'sssd.conf::user' option
        0728b2fdc  TESTS: passkey: force 'root' service user
        b26b32de4  Unit tests: use ".invalid" domain name for OCSP responder
        e5140ab08  BUILD: drop suppot of '--without-infopipe' ./configure option
        77c913f7b  TOOLS/LOGS: remove redundant check
        54a1e9173  SYSDB: mistype fix
        c65d99ca6  sssctl: remove unneded include
        dbbdd0396  sssctl: mark internal function as static
        e6cf9e4b4  TOOLS: removed `sss_route_cmd::handles_init_err`
        f825fecb5  TOOLS: cache-expire: skip init and root-check
        61813cdf0  TOOLS: cache-remove: skip init
        620fed160  TOOLS: client-data-backup: skip init and root-check
        0d099538b  TOOLS: client-data-restore: skip init
        3621a587a  TOOLS: mistype fix
        3dcc17bb2  TOOLS: logs-fetch: skip init
        59e5037db  TOOLS: logs-remove: skip init
        09cf1a9a8  TOOLS: sssctl_wrap_command(): remove unneeded args
        a58979334  TOOLS: get rid of unused `void *pvt`
        97a8d9ff4  TOOLS: cache-index: skip init
        f86fb707b  sss_cache: remove a crutch
        432f280ad  TOOLS: skip confdb_init if no context ptr provided
        14d4e01d8  TOOLS: get rid of code duplication
        50b457941  TOOLS: use `sss_tool_confdb_init()` everywhere
        604be8d1c  CONFDB: move sanity check
        c0c46bf6a  SPEC: don't fail uninstallation if 'alternatives' fails
        2dae1f64d  SYSTEMD: chown all artifacts at startup
        fb8aa35f4  SYSDB: drop the code that upgrades from v < 15
        842dbbbbe  SYSDB: only monitor (and tests) should create cache files
        0aab0b184  SYSDB: removed unused define
        f83ea91aa  SYSTEMD: shell expansion of * doesn't work in ExecStartPre
        43cfcfeed  SPEC: build C9S '--with-files-provider'
        ff1d8b764  SPEC: build C9S '--with-extended-enumeration-support'
        c62986827  SPEC: build C9S '--with-ssh-known-hosts-proxy'
        41dfdccc8  RESOLV: removed unused argument
        8227599e0  RESOLV: supress deprecation warnings
        a86ee649a  Require OpenSSL >= 1.0.1
        f6ad1828c  SYSTEMD: chown gpo-cache as well
        0330ebeba  CLIENT:PAM: replace deprecated `_pam_overwrite`
        312e0ebac  Revert "ci: allow deprecated functions during build"
        10bf7ab41  SPEC: use '/run/sssd' as a home dir for 'sssd' user
        39856247e  CLIENT:PAM: avoid NULL deref
        60f282d2c  SPEC: keep 'sssd-polkit-rules' on RHEL9
        c9026bf09  Move 'nscd' helper functions out of 'utils'
        7f0f5a6cc  CONFDB: introduce helper to read a full list of configured services,
        28bb1467f  IFP: use new helper to retrieve services list
        59c48f7df  socket_activated_responders: check confdb
        32e7616e2  socket_activated_responders: log to syslog instead of stdout
        272ee81b7  TESTS:INTG: 'implicit files domain' not supported
        dbf476355  CONFDB: don't hard fail in add_implicit_services()
        9bb7b9201  CONFDB: mistype fix

    Andre Boscatto (4):
        4d1711178  mans: fix typo in ldap_idmap_autorid_compat
        9abcaf905  man: fix wrong product name
        b3124173d  man: improving documentation about username and email
        945cebcf7  sssd: adding mail as case insensitive

    Andreas Hasenack (1):
        2b5f1cc47  Fix format string used for time values

    Andreas Schneider (1):
        39f5b9ac2  ad_gpo_child: Improve libsmbclient code

    Christopher Byrne (3):
        4e345cc4c  initscripts: Allow Gentoo initscripts to work with sssd user
        fce2d97df  BUILD: Wire up sysusers, udev and tmpfiles config for optional install
        8421f34de  cfg_rules.ini: Add missing ldap_user_passkey entry.

    Dan Lavu (43):
        4dae6def1  Adding testcase for bz2166627
        69f93bf81  Updating ad_multihost test
        24a08aca8  TESTS: Porting sss_override test suite
        f05d4ec1e  tests: adding group and importance markers
        bd839b85e  Updating ad_multihost test
        cb72984e2  Updating ad_multihost test
        95678ad7e  Adding test case for bz2167728
        92e85f1a1  tests: consolidation, refactoring and organizing, renaming of some tests
        90eca38ec  tests: updating poor assertion in dyndns
        9d1fccb5e  tests: adding background refresh tests to the new framework
        a80e236b8  tests: adding testcase for gh7174 email case insensitivity
        795b13c18  tests: fixing typo in test_authentication.py
        03f68e81d  tests: test case audit and house keeping
        b164766ac  tests: removing genconf, chown tests and updating passkey dirs
        4b2553d42  tests: updating makefile.am to include tests
        7f48c7c44  tests: adding gpo system tests
        f9c0c6d8d  tests: adding proper requirement for sss_ssh_knownhosts
        252f36520  tests: updating gpo auto private group test case
        88ac37d98  tests: housekeeping - test_kcm.py
        c19cac208  tests: fixing gpo test case
        9a852565b  tests: housekeeping - test_gpo.py
        9808b6987  tests: test_autofs.py - adding error messages
        f5f00f40b  tests: fixing auto_private_group test cases
        415fa416b  test: housekeeping - sudo
        30d394d61  tests: housekeeping - test_cache.py
        447deb030  tests: housekeeping, test_proxy.py
        f43dcc30a  tests: housekeeping - test_trusts.py -> test_ipa_trusts.py
        f70411aac  tests: housekeeping, test_files.py
        8c19d7b6f  tests: housekeeping, test_ldap.py
        7716d13c2  tests: housekeeping, test_authenticaiton.py
        4d1c4d7f3  tests: housekeeping - test_failover.py
        c3ce4bc1a  tests: remove multihost basic tests
        fcda45b05  tests: housekeeping - schema
        4fc351ca8  tests: fixing test step language
        edb35afcf  tests: housekeeping, test_identity.py
        34cd828d5  tests: updating gpo test case to test all auto_private_group values
        14d7796a7  tests: housekeeping - sss_override
        0be58a26e  tests - housekeeping - logging
        97571b16d  tests: removing intg/test_confdb.py
        e442fdf71  tests: removing intg/test_files_ops.py
        ef2a61857  tests: improving gpo tests to be run against ad and samba
        b1bee78de  tests: removing intg/test_sudo.py
        4295e0032  tests: removing intg/test_kcm.py

    Daniel Bershatsky (1):
        9fe254f46  SSS_CLIENT: Follow API changes in libsubid

    Denis Zlobin (1):
        11a77e8b8  sbus: Fix codegen template for async client

    Dominika Borges (2):
        d1428aac1  doc: improve `failover_primary_timeout` option
        3bc526eb6  doc: improve ad_access_filter option

    Dusan Uradnik (1):
        83eec3639  sbus: store dbus connection name in domain.conn_name

    Elena Mishina (1):
        f09a66cac  po: update translations

    François Cami (1):
        0368c368a  Fix typo: found => find

    Gaël PORTAY (2):
        46fbc499d  Add missing debian operation system in help string
        7b32dc0ab  Allow unknown operation system build

    Günther Deschner (1):
        1bf51929a  Fix the build with Samba 4.20

    Iker Pedrosa (14):
        906a677c9  passkey: write mapping data to file
        0588bd3b5  passkey: fix two covscan issues
        702f7c236  passkey: rename function
        40e0592df  test: basic tests for ldap_user_extra_attrs
        bfab49075  man: clarify passkey PIN prompt
        2c05926ed  passkey: omit user-verification
        38d334ea0  man: clarify user credentials for `cache_credentials`
        5a211ec94  CI: build passkey for centos-9
        3edc04d17  CI: clean configure.sh
        39a0de22d  CI: clean distro.sh
        05ea3f1be  CI: clean deps.sh
        292ef326b  CI: upload cwrap logs
        5841348fa  man: fix default value for pam_passkey_auth
        bb72b53d3  spec: change passkey_child owner

    Jakub Jelen (2):
        b7da2450a  doc: Fix configuration option pam_p11_allowed_services type
        459d0989e  Allow smart card authentication in vlock

    Jakub Vavra (36):
        121b3bbff  Tests: Modify expiring/expired password test for RHEL 8.
        469905bfa  Tests: Add conditional skip for simple ifp test.
        3e3d09864  Tests: Skip test_0016_ad_parameters_ad_hostname_valid on other architectures.
        54903c0e3  Tests: Improve stability of test_0004_bz2110091
        6540a67c9  Tests: Print krb5.conf when joining realm.
        8fc5aadb1  Tests: Split package installation to different transactions.
        e73efe153  Tests: Handle dns with systemd resolved.
        39dde256e  tests: Add missing pytest marker config.
        88a386e12  Tests: Skip tests unstable on other archs and tweak realm join.
        8264cb573  Tests: Fix AD param sasl tests.
        4a9f8ebb8  Tests: adjoin in test_00015_authselect_cannot_validate_its_own_files
        7a3cc7a7b  Tests: Fix autofs cleanups
        0f1a6e350  Tests: Add a test for bz1900973 kcm delete expired tickets
        38db355aa  Tests: Add a test for kcm log rotation SSSD-5687
        ff8f248b0  Tests: Fix tokengroups tests.
        df1b74546  Tests: Retry realm join as it is flaky on multiarch setups
        a5270f898  Tests: Change path to keytabs to reflect whole domain in them
        5fb0a9ddc  Tests: Add importance and ticket to multihost
        b66035f3d  Tests: Revert change of retun type of realm_join
        9d6caaed3  Tests: Add a plugin for a per-test logging
        684d18b4b  Tests: Add single retry for realm leave
        2fa6ec2cc  Tests: Set ciphers for kerberos
        ef581c971  Tests: Add pytest.ini with marker converted to basic suite
        998503210  Tests: Fix OsError in test_kcm_debug_level_set
        1358f417a  CI: Add sssd testlib to pythonpath for prci multihost
        3caac5f7b  Tests: Tweak per-test log to de-duplicate output
        e3af77c73  Tests: Per-test logging: Fix exception on missing call phase.
        20175f413  Tests: Add oddjob package to master for multihost/alltests
        759d261c1  Tests: Refactor AD tests from files provider to proxy one.
        0a397c28d  Tests: Fix ipa/conftest.py for fedora.
        0935ce945  Tests: Fix hostmap tests not to depend on user-nsswitch.conf
        43c5b9445  Tests: refactor sssd.conf backup and restore
        1c2aa8250  Tests: Fix test_kcm_ssh_login_creates_kerberos_ticket
        7c6bc58a1  Tests: Move polarion.yaml to src/tests/
        f30902faa  Tests: Update reference to polarion.yaml
        5339573f0  Tests: Add test for bz 1913284 keytab permission denied

    Jakub Vávra (26):
        aacb789b7  Tests: Split package installation transactions and add error logging.
        76ec4919f  Tests: Add extra debug to test_0003_gssapi_ssh.
        6319e4276  Tests: Switch test_0001_memcache_sid to reuse adjoin code.
        de5e22e2d  Tests: Add journalctl when systemctl sssd fails.
        8aa72b162  Tests: Update ad parameters ported for non-root.
        59d19d909  Tests: Add extra sssd restart on master for samba tests.
        f160242d7  Tests: Add fixing sssd.conf ownership after realm join.
        bc1a8e963  Tests: Fix PEP8 on updated AD suites.
        31bd16f65  Tests: Update expect as passwd password change message changed.
        9a5a54cfb  Tests: Update password change expect to work
        cbc441511  Tests: Add extra output in package_mgmt when operation fails.
        d7d2b9673  Tests: Move logging settings change to test start
        979c25f38  Tests: Update ad multiforest and multidomain suites.
        60fa73053  Tests: Update code handling journald.conf
        9f7916129  tests: Drop already ported tests from alltest
        f37aa4669  tests: Add loading kernel module sch_netem for tc tool
        48e681215  tests: Drop test_bz1221992 that is invalid on RHEL 10
        49904292d  test: Do not overwrite /etc/nsswitch.conf by authselect
        27995f5d6  Tests: Drop tests converted to system from basic to save resources in prci
        7e5477706  Tests: Handle missing ldap_child.log in AD parameters
        4e95d6f6c  tests: Skip tests dependend on ldap_use_ppolicy when not available.
        fc000fa60  tests: Add fallback log directory for custom_log.py
        33fdf759b  tests: change parameters for pytest.mark.flaky to max_runs
        0d07b4986  tests: Update code handling systemd-resolved for F42.
        6f8bc2bec  tests: Addd sssd.log when sssd does not start.
        17c37e444  tests: Update ldap test to use journal utility.

    John Veitch (2):
        30a9f4f38  Update sssd.in to remove -f option from sysv init script
        4e4860185  Add --logger=files option to sysv init script

    Justin Stephenson (37):
        fe751c316  Passkey: Adjust IPA passkey config error log level
        fa326be9c  IPA: Log missing IPA config data on default level
        f3f7a4ce1  Change "non_kerberos" to "local" authentication
        d019132bd  Add local auth policy
        43d89dd2d  PAM: Fail empty password in passkey fallback
        348c8f535  Passkey: Warning display for fallback
        a20dadc7e  Makefile: Respect `BUILD_PASSKEY` conditional
        eadee9a2a  pam: Conditionalize passkey code
        7cf9a1ff0  ipa: Add `BUILD_PASSKEY` conditional for passkey codepath
        12762d629  pam: Remove unneeded passkey verification call
        bec58bf45  CI: Add Fedora 40+ to install CI scripts
        eebb43def  Proxy: Avoid ldb_modify failed error
        b516f1e4f  Passkey: Add child timeout handler
        053b6e14c  Passkey: Conditional fixes
        57dac1e29  Passkey: Allow kerberos preauth for "false" UV
        ae920b9ab  tests: Improve read write pipe child tests
        1f4fffdb7  util: Realloc buffer size for atomic safe read
        6f8f7c82b  Passkey: Increase conv message size for prompting
        ad9bf1bbc  use systemd-sysusers
        45e06b770  man: Improve LDAP security wording
        847aa7121  ldap: Switch ldap_id_use_start_tls default to True
        6814b2788  CI: Add dependabot to get updates of github actions
        60fdacfd8  passkey: Add krb5 preauthentication prompt support
        6ed1eff44  passkey: Skip processing non-passkey mapping data
        1d33bde42  Passkey: Fix coverity memory overrun error
        a134074c2  Passkey: Fix coverity RESOURCE_LEAK
        22d35690b  Passkey: Fix valgrind error and missing free
        1bacf4985  Tests: Python black formatting fixes
        c9a333c52  krb5: Allow fallback between responder questions
        6c1272edf  krb5: Add fallback password change support
        f860f10a5  PAM: Print PAM Data once on incoming requests
        c15bd3aeb  krb5: Move soft_terminate_krb5_child to static
        b32f59603  man: Add local_auth_policy table
        914ce0947  passkey: Return error during passkey processing
        d7d51126a  passkey: Improve passkey mapping handling
        4d5177404  configure: use RUNDIR macro for config_pidpath
        3a644161d  sdap: Log hint for ignore unreadable references

    Kaushik Banerjee (4):
        0f351c2bb  Tests: Restart systemd-journald instead of stop/start
        7067b579b  Tests: Disable journald rate limiting during alltests pytest session
        39ecf47a3  Tests: Move journald rate disable to common/fixtures.py
        c58f071b5  man: Use c_rehash instead of deprecated cacertdir_rehash

    Lizhou Sha (1):
        7077328f5  SPEC: Add Requires: sssd-krb5-common for KCM ticket renewals

    Madhuri Upadhye (25):
        377ec31a8  Test: Test search filter specific user override or a specific group override
        2965db1cc  Tests: Gating fixes for RHEL8.9 and RHEL9.3
        9c50b8ec1  Tests: Add package for tc command
        57499ff65  Tests: When adding attributes ldap_user_extra_attrs with mail value in sssd.conf the cross-forest query stop working
        ac5480af3  Tests: Minor fix in test_adtrust
        ea34b805b  Test: Check case-insensitive while checking with group lookup for a overrideuser
        6bed4b7bc  Tests: Package download
        e3dd7cf47  Tests: Add package for IPA tests
        66c0a2d00  tests: add passkey tests for sssctl and non-kerberos authentication
        f4c9d6efd  tests: add passkey tests for authentication failures
        173f31148  Tests: Add passkey test cases for following scenario
        8fd2df732  Tests: Add method to detet the files provider
        90e46836d  Tests: tier1/test_service: Remove files provider
        0b26b6fd1  Tests: alltests/test_krb5: Replace files provider
        55bcb883e  Tests: passkey: Add a ssh key as a passkey mapping
        d42c5e7da  Tests: Deleting coverted test cases
        9aaa71303  Tests: Add the test case passkey for fips enable
        ca684cd15  Tests: rename fips passkey test's recording files path
        f13510276  Test: Update tc when mapping and key are added
        4e0b648d1  Test: Check the TGT of user after auth for passkey
        3bac8c9cc  Test: Passkey test cases
        55db5db15  Tests: housekeeping: Description in passkey tests
        216231770  Test: housekeeping: test_sss_ssh_knownhosts.py => test_ipa.py
        9e6ca53ad  Tests: Remove converted test cases
        f4bf66d08  Tests: Force delete to local user

    Masahiro Matsuya (1):
        8804a2c68  TESTS: test_0017_filesldap is missing staticmethod

    Mathias Olsson (1):
        f6f83c480  check for protected authentication path

    Ondrej Valousek (2):
        f05bd34e8  AD provider: Read sAMAccountName attribute unconditionally
        7a27e5391  AD: Construct UPN from the sAMAccountName

    Patrik Rosecky (22):
        0f911c10d  Tests: converted multihost/test_config.py
        01853a10f  Tests: convert intg/test_memory_cache.py to system tests
        5ced01570  tests: multihost/basic/sssctl_config_check.py converted
        28aeb13a2  Tests: converted intg/test_memory_cache to test_id
        fe61c459a  tests: converted multihost/basic/test_ldap.py
        e32f899a1  Tests: sssctl_config_check: test for incorrectly set value
        376534022  tests: convert multihost/basic/test_basic to test_kcm and test_authentication
        64422699a  Tests: converted alltests/test_pasword_policy.py to tests/test_ldap.py
        620af3b3f  Tests: alltest/test_sssctl_local.py converted to system/tests/sssctl.py
        ea7273b3d  Tests: multihost/basic/test_files converted
        8ecfe20ef  Tests:alltests/test_rfc2307.py converted to test_ldap.py
        b07a7552a  Tests: alltests/test_sss_cache.py converted to multihost/test_sssctl.py
        ce117ae0c  TESTS: topology set to KnownTopologyGroup.AnyProvider
        e9189052a  Tests: converted alltests/test_default_debug_level
        a5f636bb4  Tests: alltests/test_autoprivategroup.py converted to system/test_auto_private_groups.py
        c2360811d  Tests: alltests/test_ldap_extra_attrs.py converted to system/tests/test_schema.py
        ae2420afb  Tests: fix flake8 issues
        543eda195  Tests: multihost/test_sssctl_analyzer.py converted to system/test_sssctl_analyze.py
        d3a2bd087  Tests: alltests/test_config_validation converted
        ea7de588d  Tests: alltests/test_offline.py converted
        e235afee2  tests: multihost/basic/test_kcm converted
        23afc3bb7  Tests: convert multihost/alltests/test_cache_testing to system/test_sss_cache

    Pavel Březina (79):
        650e8d0a4  Update version in version.m4 to track the next release
        b033b0dda  ipa: correctly remove missing attributes on netgroup update
        8b014bf15  cache_req: remove unused field cache_behavior from state
        32f578229  cache_req: fix propagation of offline status with cache_first = true
        06d6e2702  pot: update pot files
        b9bb35c1a  ci: move to new centos8 buildroot repository url
        5c72905ec  ci: run workflows on sssd-2-9
        43dd400dc  tests: add pytest-importance plugin to system tests
        d3fd983be  tests: add pytest-output plugin to system tests
        50df528cc  tests: add requirements to system tests
        03e39e196  tests: drop tier from system tests
        f8848028a  tests: fix doctring in test_config__add_remove_section
        f3793fc7c  ci: generate polarion xmls from system tests
        1d268bc19  ci: run system test in collect only mode first
        7f3431a77  tests: fix doctring in test_memory_cache__invalidate_group_after_stop
        dd21de843  readme: remove github actions badges
        2f08f87be  git: add commit template for tests
        641e5f73d  mc: recover from invalid memory cache size
        1e5dfc187  sss_iface: do not add cli_id to chain key
        fdc8329ef  pot: update pot files
        725c5541d  tests: include passkey test code only if passkey is built
        233a846e8  tests: add sssd_test_framework.markers plugin
        61bf109a7  SSSDConfig: set PYTHONPATH to make setuptools work on centos8
        9dccf7ff6  ci: install latest SSSD code on IPA server
        4f5b1a25a  intg: return status code for calls requiring it in fake nss module
        b9c1d7d66  sbus: add destination to request key
        9f8551a19  sbus: centralize communication to a single dbus server
        a25b16ed7  sbus: correctly handle reply on signal chaining
        ab486cbc7  sbus: convert calls in dp_resp_client.c into signals
        d9b2b8e58  sbus: disable chaining for SetActive and SetInconsistent
        529af409a  sss_iface: split connection to dbus server and service registration
        8b47a9a31  backend: connect to private dbus in a blocking way
        9a47e2b04  dp: remove client registration code
        174fb9e00  sbus: log sender of received message
        10c1942e4  sbus: make sbus_connect_private_send static
        9ece4e133  dp: build dp_sbus_domain_active/inconsistent only with files provider
        fbff09892  dependapot: add ci prefix to commit messages
        17cf4bbb7  ci: get frozen Fedora releases in the matrix
        26047f07c  ipa: do not go offline if group does not have SID
        a3ea75877  pot: update pot files
        736430aa0  spec: use sysusers directly from sssd tarball
        76d3b5a45  ad: do not print backtrace if SSSD domain name is not the same as DNS name
        3e976dc6a  ad: do not print backtrace if SOM is missing in GPO
        0f9611cdc  tests: adapt to new firewall API
        2e75d735e  scripts: sign tarball with sssd project key
        c7a6e62d1  scripts: create checksum file for release tarball
        7076c5bb2  krb5_child: fix order of calloc arguments
        e9253e0a7  tests: fix isort, black and mypy errors
        9eea993b7  tests: add tests for sss_ssh_knownhosts
        603399a43  pam: fix invalid #if condition
        41cafd63e  tests: fix isort issue
        3488b9e95  tests: use different home dir then /tmp for local user
        7293eeea5  scripts: add sssd.sysusers to srpm generated by make_srpm.sh
        e9738e369  failover: add failover_primary_timeout option
        b026d625a  ci: explicitly set which topologies are already provisioned
        bf436377b  ci: use python 3.11 for system tests
        15ab9be57  pot: update pot files
        7c443ab4b  scripts: add support for beta and rc versions
        5ae05315e  configure: use runstatedir for default pid path
        aefc8cea8  Release sssd-2.10.0-beta1
        eadb87267  version: replace dash with tilda
        fad092b08  ci deps: do not use -- to denote positional arguments anymore
        9f363f86b  ci: do not collect pytest-mh logs in separate file
        b7a47ffa5  ci: disable show-capture in system tests
        6de89309d  pot: update pot files
        28239d6c9  scripts: switch back to dash for pre-releases
        b44cb5766  Release sssd-2.10.0-beta2
        d213e59cd  tests: update the tests to work with latest pytest-mh
        8e59f7700  tests: use podman instead of ssh to speed up in PR CI
        ccdee0042  tests: stabilize test_sudo__refresh_random_offset
        b9a279b4e  ci: switch back to ssh connections in system tests
        72232cc14  tests: add topology marker back to test_ldap__password_change_using_ppolicy
        c006b88d9  tests: avoid skipif in the system tests for feature detection
        b4bca9822  make_srpm: fallback to tar if git archive fails
        8be21725a  conf: remove unused reconnection_retries
        263cb2e73  sbus: terminate ongoing chained requests if backend is restarted
        2eef90a0c  po: fix sv language
        6ec5aa0da  pot: update pot files
        217b3fad3  Release sssd-2.10.0

    Pavel Raiskup (1):
        c1434c1ae  rpm: drop the --remote argument from git-archive call

    Petr Mikhalicin (1):
        ae6b9163b  pam_sss: fix passthrow of old authtok from another pam modules at PAM_PRELIM_CHECK

    Samuel Cabrero (25):
        738bb5330  GPO: Defer SMB server choice until id connection established when processing referrals
        98efb5ec9  GPO: Remove unused local variable
        992606711  SYSDB: Add sysdb_gpos_base_dn()
        e1692772b  GPO: Fetch the GPO's displayName attribute
        568ca5dee  SYSDB: Store GPO's displayName in sysdb
        35801347e  SYSDB: Store the GPO's filesystem path in sysdb entry
        66fd8a048  SYSDB: Always canonicalize GPO guid
        cf59da1aa  SYSDB: Add new index for gpoGUID and make searches on it case insensitive
        095e31eb2  SSSCTL: Prepare for extended help in subcommands
        18a17bcd5  SSSCTL: Add gpo-show command
        6dc9166c2  SSSCTL: Add sssctl gpo-list command
        be735999d  SYSDB: Add a function to delete GPO entry by GPO GUID
        afee68b11  SSSCTL: Add sssctl gpo-remove command
        c5b16eec4  SSSCTL: Add gpo-purge command
        54179a094  SSSCTL: Add the new cached GPOs management commands to release notes
        85a238c6b  TESTS: Extend sysdb-tests to check case-insensitive store operations
        d2b734b92  SYSDB: Use SYSDB_NAME from cached entry when updating users and groups
        ecda21a44  BUILD: Fix os detection
        d75727e66  TOOLS: Adjust sssctl user-checks default PAM service for SUSE
        e299525ec  LDAP: New option to trigger password change in case of grace login with expired password
        36d828925  BE: Maintain the list of periodic tasks
        423e5b937  WATCHDOG: Use a constant instead of the signal name
        fae131ad4  WATCHDOG: Send SIGRTMIN+1 signal when clock shift is detected
        07ce89e14  BE: Handle SIGRTMIN+1 signal to reschedule periodic tasks
        fdf7e75ce  MAN: Document SIGRTMIN+1 signal usage

    Scott Poore (1):
        1082f2563  Tests: add follow-symlinks to sed for nsswitch

    Sebastian Andrzej Siewior (1):
        32b72c7c3  tests: Drop -extensions from openssl command if there is no -x509

    Shridhar Gadekar (9):
        535a8c6a7  Tests: move unstable default_debug to tier2
        11eef225c  Tests: fix default debug level for typo
        587cd8dc2  Tests: move test_access_control.py to tier2
        27dd3f508  Tests: Adding c-ares markers for related tests
        fd3ed8afd  Test: drop c_ares tests from gating
        6efb2779b  Test: dropping unstable dyndns tests
        5ebf98a86  Tests: drop dyndns testcase from gating
        0171bcb06  Test: gating sssd after crash
        08aa08e07  Tests: moving duplicate backtrace from gating

    Stanisław Pitucha (1):
        1980e2c41  LDAP: Allow ignoring the ppolicy extension

    Sumit Bose (61):
        01d02794e  sysdb: fix string comparison when checking for overrides
        39b6337f3  AD: add missing AD_AT_DOMAIN_NAME for sub-domain search
        455611952  krb5: make sure sockets are closed on timeouts
        8a8869994  fail_over: protect against a segmentation fault
        d99aa97da  ldap: return failure if there are no grace logins left
        67c11c2eb  ad: use sAMAccountName to lookup hosts
        75f2b35ad  watchdog: add arm_watchdog() and disarm_watchdog() calls
        cca9361d9  sbus: arm watchdog for sbus_connect_init_send()
        8466f0e4d  sssct: allow cert-show and cert-eval-rule as non-root
        0817ca3b3  certmap: fix partial string comparison
        2bc426fa7  test: fix linking issue
        9474e0f4f  ci: remove unused clang-analyzer from dependencies
        760191875  utils: enable talloc null tracking
        c38699232  proxy: add support for certificate mapping rules
        ffd467430  intg: add NSS module for nss-wrapper support
        54f558966  intg: replace files with proxy provider in PAM responder test
        8952f6d8f  confdb: add new option for confdb_certmap_to_sysdb()
        f5f8030ad  intg: use file and proxy provider in PAM responder test
        4d475e41a  intg: add proxy auth with fallback test
        a7b19bcb4  ipa: reduce log level of some HBAC log messages
        962e9d052  PAM: fix Smartcard offline authentication
        e9e6d80e2  ci: make valgrind suppression more relaxed for test_ipa_subdomains_server
        cffe6e09c  nssidmap: fix sss_nss_getgrouplist_timeout() with empty secondary group list
        5e7cd889d  pam: fix Smartcard auth with files provider
        8ff7fdc12  sssctl: do not require root for user-checks
        9b73614c4  LDAP: make groups_by_user_send/recv public
        c02e09afe  ad: gpo evalute host groups
        ff23e7e28  sysdb: remove sysdb_computer.[ch]
        5f63d9bfc  sdap: add set_non_posix parameter
        44ec3e463  pam: fix SC auth with multiple certs and missing login name
        29a77c6e7  sdap: add search_bases option to groups_by_user_send()
        a153f13f2  sdap: add naming_context as new member of struct sdap_domain
        b439847bc  sss-client: handle key value in destructor
        409f175f0  krb5: lower log level in sss_krb5_get_init_creds_password()
        4f38fd10c  krb5: increase log level in map_krb5_error()
        bf6cb6dcd  krb5: add OTP to krb5 response selection
        7c33f9d57  krb5: make sure answer_pkinit() use matching debug messages
        e26cc6934  krb5: make prompter and pre-auth debug message less irritating
        0d5e8f117  pam_sss: prefer Smartcard authentication
        05df81679  pam: fix storing auth types for offline auth
        79c384fb0  test: set 'local_auth_policy = only' for all passkey test
        d7db79716  ad-gpo: use hash to store intermediate results
        0de6c3304  ad: refresh root domain when read directly
        7239dd679  dist: set capabilities during make install
        1199bd10c  conf: update path permissions
        f1c621816  oidc_child: fix wrong usage of '%*s'
        4cf9625b8  sbus: retry Hello if ERR_SBUS_NO_REPLY was received
        b25e510ad  ad: use right memory context in GPO code
        48c0607b4  configure: use prefix for systemd paths if needed
        12150fcbb  configure: user ${datadir} in polkitdir
        986bb7262  sysdb: do not fail to add non-posix user to MPG domain
        4dc966228  p11_child: enhance 'soft_crl' option
        af799964e  krb5_child: do not try passwords with OTP
        077d2993a  pam_sss: add missing optional 2nd factor handling
        71160e350  man: add details for ad_access_filter
        f22c966ff  LDAP: read ldap_use_ppolicy as boolean
        a33114020  oidc_child: use CURLOPT_PROTOCOLS_STR if available
        0e836edcf  cert util: replace deprecated OpenSSL calls
        67ba42c48  pam: only set SYSDB_LOCAL_SMARTCARD_AUTH to 'true' but never to 'false'.
        69f63f1fa  sdap: allow to provide user_map when looking up group memberships
        5f5077ac1  ad: use default user_map when looking of host groups for GPO

    Thorsten Scherf (1):
        4729ec077  SSH: fix typo in sss_ssh_knownhosts man page

    Tomas Halman (3):
        f0bba9d51  dyndns: PTR record updates separately
        830a2e3d6  Handle child-domain group membership
        ecb0c6370  GPO evaluation of primary group

    Tomasz Kłoczko (1):
        402793059  Bump DocBook DTD version to latest stable 4.5

    Weblate (6):
        799e56d61  po: update translations
        058898168  po: update translations
        96f568cbd  po: update translations
        d13dc329b  po: update translations
        786844730  po: update translations
        c265745f4  po: update translations

    aborah (31):
        2096f4552  Tests: Fix gating tests for 9.3
        75ae9e87a  Tests: Netgroups do not honor entry cache nowait percentage
        d14be798b  Tests: Skip test_0001_bz2021196
        34dba5a38  Tests: Add ssh module that is fast, reliable, accurate
        567412087  Tests: Fix alltest tier1_3 tests with new ssh module
        7f94e5ca4  Tests: Fix IPA tire1_2 tests
        476ba5618  Tests: Increase PAM_MISC_CONV_BUFSIZE to max at 4096 instead of 512 bytes
        5e86af8a3  Tests: Update test_ldap_password_policy.py::test_maxage as per the new sssd change
        2487c99c8  Tests: Fix test_0002_bz1928648 with new ssh module
        fe99271ba  Tests: sssd-be tends to run out of system resources, hitting the maximum number of open files
        d8742c51f  Tests: Update tire1_2 test cases with new ssh module
        66908221b  Tests: Update tier1 test cases with new ssh module
        3ff79e284  Tests: Fix test_0008_1636002
        34ef9c5f3  Tests: Fix test_maxage
        755c2157e  Tests: Fix KCM::test_client_timeout
        4b83a68e3  Tests: Update sssh module for tier 1_3, 1_4 and 2
        763106ff5  Tests: Add sleep time to test_bz785908
        160d7c4f4  Tests: Ldap referrals.
        bcbc0b319  Tests: Enabling proxy_fast_alias shows "ldb_modify failed: [Invalid attribute syntax]" for id lookups.
        5f3c82d3c  Tests: Port rootdse test suit to new test framework.
        23087669e  Tests: Fix ipa test for gating.
        fa503bcc5  Tests: Drop files provider from tests test_sssctl_local.py
        83f1ba781  Tests: Drop files provider from tests test_sssctl_ldap.py
        56280faad  Tests: Drop files provider from tests test_multidomain.py
        5999e0704  Tests: Fix the test failures for tier-1-pytest-alltests-tier1-2 for non root configuration
        0d60e3dc0  Tests: Fix RHEL10 failures
        815d89f86  Tests: Fix ipa tests for RHEL10
        15fe8a11d  Tests: Fix RHEL9.5 issue
        f7c53d1ff  Tests: Fix tier1_2 tests for rhel10
        a3ecd25a3  Tests: Fix tier2 tests for RHEL10
        6dec9f7c7  Tests: Port ipa/test_authentication_indicators to new test framework

    dependabot[bot] (10):
        0456ecad6  build(deps): bump DamianReeves/write-file-action
        2f5b29999  build(deps): bump actions/checkout from 3 to 4
        ff42d8899  build(deps): bump vapier/coverity-scan-action from 1.2.0 to 1.7.0
        cbb107314  build(deps): bump linuxdeepin/action-cppcheck
        3922f4d79  build(deps): bump actions/download-artifact from 3 to 4
        f5f5d83f7  build(deps): bump github/codeql-action from 2 to 3
        35ef26b62  build(deps): bump actions/upload-artifact from 3 to 4
        2e1c2f354  build(deps): bump DamianReeves/write-file-action from 1.2 to 1.3
        bf99d6065  build(deps): bump vapier/coverity-scan-action from 1.7.0 to 1.8.0
        1a3554b2d  build(deps): bump actions/setup-python from 4 to 5

    licunlong (1):
        a997ee7bd  cli: caculate the wait_time in milliseconds

    lisa (1):
        9506b7b30  Convert multihost/ad/test_idmap to test_identity

    roy214 (1):
        ed3726c37  sssctl: add error analyzer

    shridhargadekar (5):
        2b222dd30  Test: Dropping the assertion of ssh from analyzer list
        2176b7d84  Tests: sssctl_analyze diff location
        43e3cf1e0  Test: files_provider replaced with proxy
        fa9f6882b  Tests: sudo defaults rule
        5ed2e37c2  Tests: automount segfault fix

    spinningTops (1):
        0717974bf  Expose flat_name for use in homedir path

    wangcheng (1):
        01131ba7c  IPA: Change sysdb_attrs_add_val to sysdb_attrs_add_val_safe in debug output

    xuraoqing (1):
        cb9319677  fixed memory leak due to use popt incorrectly
