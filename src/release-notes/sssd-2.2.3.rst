SSSD 2.2.3 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

-  allow_missing_name now treats empty strings the same as missing names.
-  'soft_ocsp' and 'soft_crl options have been added to make the checks for revoked certificates more flexible if the system is offline.
-  Smart card authentication in polkit is now allowed by default.
-  ssh_use_certificate_matching_rules now allows no_rules and all_rules values (see man page for description).

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  Fixed several memory management errors that caused SSSD to crash under some circumstances.
-  Handling of FreeIPA users and groups containing '@' sign now works.
-  Issue when autofs was unable to mount shares was fixed.
-  SSSD was unable to hande ldap_uri containing URIs with different port numbers. This was fixed.

Packaging Changes
-----------------

-  Added sssd-ldap-attributes man page.

Documentation Changes
---------------------

-  Added new sssd-ldap-attributes man page.
-  Added option monitor_resolv_conf.
-  Added option ssh_use_certificate_matching_rules
-  Improved AD GPO options man page.
-  Improved sssd-systemtap man page.

Tickets Fixed
-------------

-  `#3648 <https://github.com/SSSD/sssd/issues/3648>`_ - sssd should not always read entire autofs map from ldap
-  `#3701 <https://github.com/SSSD/sssd/issues/3701>`_ - SSSD service is crashing: dbus_watch_handle() is invoked with corrupted 'watch' value
-  `#3751 <https://github.com/SSSD/sssd/issues/3751>`_ - Propagate error about multiple entries found from cache_req to responder
-  `#4111 <https://github.com/SSSD/sssd/issues/4111>`_ - use the ERROR and PRINT macros consistently
-  `#4252 <https://github.com/SSSD/sssd/issues/4252>`_ - [RFE] Regular expression used in sssd.conf not being able to consume an @-sign in the user/group name.
-  `#4607 <https://github.com/SSSD/sssd/issues/4607>`_ - Stop calling umask(0) in selinux_child now that libsemanage has been fixed
-  `#4696 <https://github.com/SSSD/sssd/issues/4696>`_ - [RFE] SSSD smart smard card, configure to soft fail when CRL not available
-  `#4854 <https://github.com/SSSD/sssd/issues/4854>`_ - sss_ssh_authorizedkeys: no output when attribute value contains trailing whitespace
-  `#4899 <https://github.com/SSSD/sssd/issues/4899>`_ - test_pam_responder.py needs improvement
-  `#4918 <https://github.com/SSSD/sssd/issues/4918>`_ - sssctl config-check giving the wrong error message when there are only snippet files and no sssd. conf
-  `#4967 <https://github.com/SSSD/sssd/issues/4967>`_ - SSSDConfig: some options are unknown
-  `#4995 <https://github.com/SSSD/sssd/issues/4995>`_ - Non FIPS140 compliant usage of PRNG
-  `#5000 <https://github.com/SSSD/sssd/issues/5000>`_ - sss_obfuscate fails to rewriting comments
-  `#5041 <https://github.com/SSSD/sssd/issues/5041>`_ - Let IPA client read IPA objects via LDAP and not via extdom plugin when resolving trusted users and groups
-  `#5044 <https://github.com/SSSD/sssd/issues/5044>`_ - Trusted domain user logins succeed after using ipa trustdomain-disable
-  `#5045 <https://github.com/SSSD/sssd/issues/5045>`_ - Improve ``sssd_nss`` debug messages
-  `#5046 <https://github.com/SSSD/sssd/issues/5046>`_ - systemctl status sssd says No such file or directory about "default" when keytab exists but is empty file
-  `#5049 <https://github.com/SSSD/sssd/issues/5049>`_ - support for defaults entry is failing in sssd sudo against Openldap server
-  `#5058 <https://github.com/SSSD/sssd/issues/5058>`_ - sss_client: usage of srand()/rand() may be disruptive for the user of lib
-  `#5064 <https://github.com/SSSD/sssd/issues/5064>`_ - KCM: ccache is created with kdc_offset=INT32_MAX
-  `#5065 <https://github.com/SSSD/sssd/issues/5065>`_ - [RFE] pam_sss allow_missing_name should allow whitespace-only string
-  `#5066 <https://github.com/SSSD/sssd/issues/5066>`_ - Null dereference in sssctl/sssctl_domains.c:sssctl_domain_status_active_server()
-  `#5072 <https://github.com/SSSD/sssd/issues/5072>`_ - automount on RHEL7 gives the message 'lookup(sss): setautomntent: No such file or directory'
-  `#5073 <https://github.com/SSSD/sssd/issues/5073>`_ - ldap_uri failover doesn't work with different ports
-  `#5075 <https://github.com/SSSD/sssd/issues/5075>`_ - sssd failover leads to delayed and failed logins
-  `#5076 <https://github.com/SSSD/sssd/issues/5076>`_ - Smart Card authentication in polkit
-  `#5077 <https://github.com/SSSD/sssd/issues/5077>`_ - autofs: delete possible duplicate of an autofs entry
-  `#1731 <https://github.com/SSSD/sssd/issues/1731>`_ - Split sssd-ldap man page

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-2_2_2..sssd-2_2_3

    Alex Rodin (7):
        f24e5ab53  Added ERROR and PRINT macros to the tools
        111144cdb  Update sss_ssh.c
        05c078e60  Update __init__.py.in
        258e9a558  Added PRINT macro in the sssctl tool
        c6271470b  Update README.md
        16124d411  Updated test_pam_responder.py
        83fb5c355  Created a new sssd-ldap-attributes.5 man page

    Alexey Tikhonov (39):
        39e16cca4  providers/ipa/: add_v1_user_data() amended
        3cc0db2fc  responder/cache_req: added debug helper function
        bf2770fa9  responder/nss: improved debug messages
        6f3607835  responder/nss: DCE
        f69c7d0cd  responder: log cmdline of client pid
        e47f143bc  SSS_CLIENT: got rid of using PRNG
        00c60805a  util/server: amended close_low_fds()
        5086353eb  util/sss_krb5.c: elimination of unreachable code
        8f275460a  util/sss_krb5: find_principal_in_keytab() was amended
        716aebab5  util/sss_krb5: fixed few memory handling issues
        e778fa18a  util/sss_krb5: debug messages fixes
        75b1fe684  sssctl/sssctl_domains.c: null dereference fixed
        f3e89aa02  MMAP_CACHE: use CSPRNG to init hash table seed
        bb8b59dde  Moved unsecure sss_rand() out of crypto lib
        24d9d213c  Reduces code duplication
        0102a253e  sss_ssh_knownhostsproxy: relocated O_NONBLOCK setting
        3c09e9dce  sss_ssh_knownhostsproxy: fixed Coverity issue
        a163f65e3  util/sss_krb5: amended sss_krb5_get_error_message()
        4239a85c7  Amended sss_krb5_get_error_message() usage.
        33c94b682  ldap_child: sanitization of error handling
        f9f6a3df8  KEYTAB_CLEAN_NAME macro was replaced
        337a1adf7  SBUS: defer deallocation of sbus_watch_ctx
        b22e5116c  util/server.c: become_daemon() made static
        c654265b3  server:become_daemon(): got rid of unused codepath
        86dc869a8  server:become_daemon(): handle fail of fork()
        9536a911b  server:become_daemon(): fixed waitpid()-loop
        148eae6a8  server:become_daemon(): fix read of uninitialized value
        848cdbc7b  server:become_daemon(): change handling of chdir() fail
        5655df4e9  server:become_daemon(): handle fail of setsid()
        b72c4fa8a  util/memory: sanitization
        f2245b53b  util/memory: helper(s) to securely erase mem was reworked
        0165ef119  tools/sss_seed: proper zeroization of sensitive data
        be7f73127  util: fixed potential mem leak in s3crypt_gen_salt()
        78127eaee  util/sha512_crypt_r: got rid of redundant mem align
        1f667ea3d  util/sha512_crypt_r: removed misleading comments
        275e062b2  util/sha512_crypt_r: proper zeroization of sensitive data
        ad1ae003e  db/sysdb_ops: proper zeroization of sensitive data
        109c21ef6  util/authtok: set destructor in sss_authtok_new()
        0a6fdec57  LDAP: proper handling of master password

    Ariel O. Barria (1):
        c53311ed9  sss_obfuscate: do not fail if sssd.conf contains non-ascii characters

    Fabiano Fidêncio (1):
        43aae7e3b  TESTS: Re-add tests for `kdestroy -A`

    Jakub Hrozek (3):
        dd781242b  KCM: Fix typo in allocation check
        2c9bdcf57  KCM: Set kdc_offset to zero initially
        a41451d01  sudo: use objectCategory instead of objectClass in ad sudo provider

    Jakub Jelen (1):
        3a96bab5f  Allow smart card authentication in polkit

    Lukas Slebodnik (1):
        f0f0003ce  IFP: Fix talloc hierarchy for members of struct ifp_list_domains_state

    MIZUTA Takeshi (4):
        df010718a  sss_client/idmap/common_ex.c: fix sss_nss_timedlock() to return errno
        3d92b14d0  util/server.c: fix handling when error occurs in waitpid()
        1311f728a  Fix timing to save errno
        9f398c7b0  Add processing to save errno before outputting DEBUG

    Michal Židek (8):
        bc35fa2f6  Bumping the version to track the 2.2.3 development
        cb04b1418  SPECFILE: Add 'make' as build dependency
        53d4393e6  memcache: Stop using the word fastcache for memcache
        68bdcebc6  MAN: GPO and built-in groups
        8b31be528  bash_rc: Build with systemtap
        5e768c826  MAN: Missing man pages in src/man/po/po4a.cfg
        9d1258ec7  MAN: Fix errors in Japanese translation
        8607b4822  Update the translations for the 2.2.3 release

    Niranjan M.R (4):
        07e2850ce  pytest: Use idm:DL1 module to install 389-ds
        f68bb1bfe  pytest: Update README with instructions to execute tests
        c5359c18c  pytest/testlib: Add python-ldap as dependency
        bd1400027  Makefile.am: Use README.md instead of README

    Pavel Březina (49):
        65de0d36c  sss_ptr_hash: keep value pointer when destroying spy
        0d477763d  autofs: fix typo in test tool
        5097684dc  sysdb: add expiration time to autofs entries
        eadfba5c6  sysdb: add sysdb_get_autofsentry
        fb83d8205  sysdb: add enumerationExpireTimestamp
        d01ddb06d  sysdb: store enumeration expiration time in autofs map
        e9fc00999  sysdb: store original dn in autofs map
        4efe83c27  sysdb: add sysdb_del_autofsentry_by_key
        8b2ab4887  cache_req: add autofs map entries plugin
        1fc3e4a14  cache_req: add autofs map by name plugin
        85c86687b  cache_req: add autofs entry by name plugin
        7726093e7  autofs: convert code to cache_req
        e5165199c  autofs: use cache_req to obtain single entry in getentrybyname
        29b1ffd01  autofs: use cache_req to obtain map in setent
        ad8b4c16d  dp: add dp_error_to_ret
        0d56c1aa4  dp: add dp_no_output type to be used in dp_set_method
        0e7298639  dp: add additional autofs methods
        2a0b74a56  dp: replace autofs handler with enumerate method
        d096eeb18  ldap: add base_dn to sdap_search_bases
        f3f223202  ldap: rename sdap_autofs_get_map to sdap_autofs_enumerate
        66e1eda6d  ldap: implement autofs get map
        f3aaaca4b  ldap: implement autofs get entry
        e050872d1  autofs: allow to run only setent without enumeration in test tool
        09781a337  autofs: always refresh auto.master
        e016ada3b  sysdb: invalidate also autofs entries
        399b2a656  sss_cache: invalidate also autofs entries
        b241e0790  ci: allow distribution specific supression files
        4488908f5  ci: suppress Debian valgrind errors
        206d994ed  ci: add Debian 10
        b13409606  ifp: call tevent_req_post in case of error in ifp_user_get_attr_send
        c08ae6cff  sudo: get timezone information from previous value when constructing new usn
        89b256dfe  ci: enable on demand runs
        46754e546  ci: set build name to pull request or branch name
        73bd961c7  ci: notify that build awaits executor
        6baf291ba  ci: convert to scripted pipeline
        50cf3849c  db: fix potential memory leak in sysdb_store_selinux_config
        b32347d35  ldap: do not store empty attribute with ldap_rfc2307_fallback_to_local_users = true
        f95db37aa  sss_ptr_hash: pass new hash_entry_t to custom delete callback
        08f015907  failover: make sure we switch to anoter server if only port differs
        b31f1e26c  autofs: remove unused enum
        14b44e721  autofs: delete possible duplicate of an autofs entry
        f295a028c  ci: store artifacts in jenkins for on-demand runs
        6da8555a0  ci: allow to specify systems where tests should be run for on-demand tests
        f80751eaa  ci: add Fedora 31
        e079a2f8a  ci: install python2 on Fedora 31 and RHEL 8 so python2 bindings can be built
        f084e757e  ci: disable python2 bindings on Fedora 32+
        5d425c10e  man: add missing new line to autofs_attributes.xml
        456e576b8  pam_sss: treat whitespace name as missing name if allow_missing_name is set
        0096d77f2  sudo: add ldap_sudorule_object_class_attr

    Paweł Poławski (2):
        fb3a8b3c1  selinux: Keep explicite umask() calls
        f4a500aff  files_ops: Remove unused functions parameter

    REIM THOMAS (1):
        274b4f92c  MAN: Provide minimum information on GPO access control

    Samuel Cabrero (12):
        f67109c46  SYSDB: Delete linked local user overrides when deleting a user
        4981fe341  SYSDB: Convert cached domain 'enumerated' attribute from bool to uint
        f6ada94ae  SDAP: Add provider name to enumeration and cleanup tasks
        4555b8179  LDAP: Return errno_t for ldap id enumeration task setup functions
        acca871d7  LDAP: Rename enumeration and cleanup functions to contain the provider
        2995a895d  AD: Rename enumeration functions to contain the provider name
        7375083a8  LDAP: Improve ldap_id_setup_enumeration error logic
        d91c1f4ae  LDAP: Remove unnecessary task pointer
        66873cac4  LDAP: Move enum fields to id provider context
        d20a7f9d5  MONITOR: Propagate error when resolv.conf does not exists in polling mode
        9b6323d8e  MONITOR: Add a new option to control resolv.conf monitoring
        d57c67e4e  MONITOR: Resolve symlinks setting the inotify watchers

    Sumit Bose (15):
        27b141f38  ipa: use LDAP not extdom to lookup IPA users and groups
        2e1614870  utils: extend some find_domain_* calls to search disabled domain
        3c871a3f7  ipa: support disabled domains
        13297b8aa  ipa: ignore objects from disabled domains on the client
        b12e7a495  sysdb: add sysdb_subdomain_content_delete()
        fa3e53bb9  ipa: delete content of disabled domains
        9ba136ce2  ipa: use the right context for autofs
        02d86b2a7  ssh: add ssh_use_certificate_keys option to config checks
        1a6b6c928  ssh: apply certificate matching rules
        d2da89098  ssh: add option ssh_use_certificate_matching_rules
        30d0ccd49  ssh: enable p11_child logging
        31ebf912d  p11_child: allow verification with no_verification option
        389e2eeb0  p11_child: add 'soft_ocsp' and 'soft_crl options
        b9a53cfca  ipa: add failover to override lookups
        707fdf040  ipa: add failover to access checks

    Thorsten Scherf (1):
        6a203ac22  Fix option type for ldap_group_type

    Tomas Halman (9):
        44d46cf28  LDAP: Systemtap ldap probes fail without filter
        7fd907cbe  LDAP: extend LDAP systemtap probes of attr list
        88b875f6b  LDAP: Add probes to be able print ldap attributes
        c4568a9a9  MAN: update systemtap man page
        c79097074  TESTS: tests have to be linked with systemtap
        c7c08e12c  MAN: Update SystemTap man page
        469f1acd6  IPA: Utilize new protocol in IPA extdom plugin
        587c8cb9d  INI: sssctl config-check giving the wrong message
        414c11154  TESTS: check "sssctl config-check" output

    pedrosam (1):
        16be48f47  cache_req: propagate multiple entries error to the caller
