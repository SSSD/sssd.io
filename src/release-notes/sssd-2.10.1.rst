SSSD 2.10.1 Release Notes
=========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* ``krb5-child-test`` was removed. Corresponding tests under 'src/tests/system/'
  are aimed to provide a comprehensive test coverage of 'krb5_child'
  functionality.

* SSSD doesn't create anymore missing path components of DIR:/FILE: ccache types
  while acquiring user's TGT. The parent directory of requested ccache directory
  must exist and the user trying to log in must have 'rwx' access to this
  directory. This matches behavior of 'kinit'.

* The DoT (DNS over TLS) for dynamic DNS updates is supported now. It requires
  new version of ``nsupdate`` from BIND 9.19+.

* The option default_domain_suffix is deprecated. Consider using the more
  flexible domain_resolution_order instead.

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

* Support of deprecated ``ad_allow_remote_domain_local_groups`` sssd.conf option
  isn't built by default. It can be enabled using
  '--with-allow-remote-domain-local-groups' ./configure option.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* ``ad_allow_remote_domain_local_groups`` option is deprecated and will be removed
  in future releases.
* the ``dyndns_server`` option is extended so it can be in form of URI
  (dns+tls://1.2.3.4:853#servername). New set of options ``dyndns_dot_cacert``,
  ``dyndns_dot_cert`` and ``dyndns_dot_key`` allows to configure DNS-over-TLS
  communication.
* Added ``exop_force`` value for configuration option ``ldap_pwmodify_mode``. This
  can be used to force a password change even if no grace logins are left.
  Depending on the configuration of the LDAP server it might be expected that
  the password change will fail.


Tickets Fixed
-------------

* `#7510 <https://github.com/SSSD/sssd/issues/7510>`__ - No way to configure ``debug_backtrace_enabled`` for `ldap_/krb_child``
* `#7612 <https://github.com/SSSD/sssd/issues/7612>`__ - sssd does not lookup user gid's at reboot without \*.ldb files
* `#7642 <https://github.com/SSSD/sssd/issues/7642>`__ - AD machine account password renewal via adcli doesn't honor ad_use_ldaps setting
* `#7664 <https://github.com/SSSD/sssd/issues/7664>`__ - sss_ssh_knownhosts fails on F41
* `#7671 <https://github.com/SSSD/sssd/issues/7671>`__ - Mismatch between input and parsed domain name when default_domain_suffix is set.
* `#7715 <https://github.com/SSSD/sssd/issues/7715>`__ - sssd backend process segfaults when krb5.conf is invalid


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.10.0..2.10.1

    Alejandro López (3):
        fe7297931  SSH: sss_ssh_knownhosts must ignore DNS errors
        ad5747ac1  OPTS: Add the option for DP_OPT_DYNDNS_REFRESH_OFFSET
        6eb7683e9  TESTS: Also test default_dyndns_opts

    Alexey Tikhonov (41):
        78b1081e9  When using SPDX expression the booleans must be in all caps.
        d75d2fe97  Get rid of on-house MIN/MAX definitions
        74b0c4ee0  DEBUG: add 'debug_backtrace_enable' getter
        8ddfe87dd  UTILS: simplify / comment a bit better
        3451786d0  DEBUG: propagate debug_backtrace_enabled to child processes
        90c509287  INI: remove unused helpers
        9007c859b  INI: stop using 'libini_config' for access check
        340671f16  INI: relax config files checks
        8db2df4fc  Configuration: make sure /etc/sssd and everything
        dfaf15b14  INI: don't report used snippets in `sss_ini_add_snippets()`
        65d6e03ea  SSSCTL: change error message to be more accurate
        537ce34e0  INI: add verbose error messages
        4acd8a3c8  chown() gpo cache recursively.
        cb0a86885  MAN: mistypes fixes
        65272cfda  SPEC: require OpenSSL >= 1.0.1
        afd7754fa  SPEC: untie capabilities of different binaries
        53431f935  LDAP_CHILD: replace 'cap_dac_override' with 'cap_dac_read_search'
        b81a266b4  LDAP_CHILD: don't require any capabilities besides 'cap_dac_read_search'
        f344f3a4c  LDAP_CHILD: require only 'cap_dac_read_search=permitted'
        a9023c777  Describe current capabilities usage.
        59ccf3e08  CLIENT: don't try to lookup `getservbyport(0, ...)`
        35909fdf7  SSSDConfig: chown file to root:sssd
        963e0c6d4  'dtrace' was moved to a separate package on C10S as well
        f2f1ee8b6  Enable CI for 'sssd-2-10' branch
        1e4bb2183  KRB5: verbosity around ccname handling
        ce85278b1  KRB5: don't pre-create parent dir(s) of wanted DIR:/FILE:
        f0957bc01  KRB5: skip `switch_creds()` in PKINIT case
        f21107a22  KRB5: 'fast-ccache-uid/gid' args aren't used anymore
        cfbb36e2f  KRB5: don't require effective CAP_DAC_READ_SEARCH
        d2892fe5b  KRB5: verbosity
        29a8a22db  KRB5: drop cap_set*id as soon as possible
        be5174d93  KRB5: 'krb5_child' doesn't require effective capabilities
        0890828d9  become_user() moved to src/monitor
        01bc3708b  KRB5: cosmetics
        dcef16bb7  Deprecate and make support of 'ad_allow_remote_domain_local_groups'
        0ab5ce326  KRB5: mistype fix
        8e5864d58  sss_semanage code is only used by 'selinux_child'
        b853b20c4  sss_selinux code is only used by 'ipa_selinux'
        89627db1c  UTILS: shared helper to print current process credentials
        1614c5e51  SELINUX_CHILD: only cap_set*id is required
        3c0c33d5b  Ignore '--dumpable' argument in 'krb5_child' and 'ldap_child' to avoid leaking host keytab accidentially.

    Dan Lavu (5):
        f990b0ff7  tests: rm intg/test_sss_cache.py
        be90cc62f  tests: adding gpo customer test scenario to use the ldap attribute name
        c6b9e2645  tests: removing intg/ts_cache.py
        0ceefae81  tests: converting all the ldb cache tests to use one provider
        195c6a661  tests: adding system/tests/readme.rst as a quick primer

    Jakub Vávra (4):
        f3c985ca4  Tests: Add missing returncode to test_0004_bz1638295
        8a085c52d  tests: Unify packages available on client for ipa suites
        ba2b247c2  Tests: Update sst to rhel-sst-idm-sssd for polarion.
        0f9074e20  Tests: Add ssh to services for authentication with ssh tests.

    Jan Engelhardt (5):
        1984036bb  build: remove superfluous WITH_IFP leftover
        1a743a412  sssd: always print path when config object is rejected
        62fac0be1  build: unbreak detection for x400Address
        09f6d72b9  build: stop overriding CFLAGS
        42e800e14  build: fix spellos in configure.ac

    Justin Stephenson (2):
        a7196c752  ipa: Check sudo command threshold correctly
        9e3fbbc67  analyzer: fix two crashes

    Madhuri Upadhye (2):
        2eec5ebba  Test: Passkey test cases with diffferent auth_methods
        46ec31c6e  Test: Add the test when we replace id_provider

    Pavel Březina (2):
        9bfa366a8  po: update pot files
        7de1c5f4d  Release sssd-2.10.1

    Scott Poore (1):
        0229f4195  man: sssd.conf update defaults for certmap maprule

    Sumit Bose (9):
        d523261c3  ldap: add 'exop_force' value for ldap_pwmodify_mode
        e609bb6d1  tests: add 'expo_force' tests
        ee47dbca1  pam_sss: add some missing cleanup calls.
        cac2e40ac  subdomains: check when going online
        76ce51d46  ssh: do not use default_domain_suffix
        d89edf89d  responders: deprecate default_domain_suffix option
        5e0204859  ldap_child: make sure invalid krb5 context is not used
        d2d229d21  dyndns: collect nsupdate debug output
        9c87e6e79  ldap: make sure realm is set

    Tomas Halman (2):
        6b0f92b65  Missing 'dns_update_per_family' option
        c228b79e0  Add DoT support for DNS updates

    Yaakov Selkowitz (1):
        05ceef324  SPEC: require systemtap-sdt-dtrace on ELN

    aborah-sudo (2):
        c2d10011b  Tests: Test transformation of bash-ldap-id-ldap-auth netgroup
        a7cc6cbf3  Tests: Reverse the condition and fail

    santeri3700 (1):
        8adf0cc45  ad: honor ad_use_ldaps setting with ad_machine_pw_renewal
