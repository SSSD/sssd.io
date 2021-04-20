SSSD 1.16.4 Release Notes
=========================

Highlights
----------

New Features
~~~~~~~~~~~~

-  The list of PAM services which are allowed to authenticate using a Smart Card is now configurable using a new option ``pam_p11_allowed_services``. (#2926)
-  A new configuration option ``ad_gpo_implicit_deny`` was added. This option (when set to True) can be used to deny access to users even if there is not applicable GPO. Normally users are allowed access in this situation. (#3701)
-  The LDAP authentication provider now allows to use a different method of changing LDAP passwords using a modify operation in addition to the default extended operation. This is meant to support old LDAP servers that do not implement the extended operation. The password change using the modification operation can be selected with ``ldap_pwmodify_mode = "ldap_modify"`` (#1314)
-  The ``auto_private_groups`` configuration option now takes a new value ``hybrid``. This mode autogenerates private groups for user entries where the UID and GID values have the same value and at the same time the GID value does not correspond to a real group entry in LDAP (#3822)

Security issues fixed
~~~~~~~~~~~~~~~~~~~~~

-  CVE-2019-3811: SSSD used to return "/" in case a user entry had no home directory. This was deemed a security issue because this flaw could impact services that restrict the user's filesystem access to within their home directory. An empty home directory field would indicate "no filesystem access", where sssd reporting it as "/" would grant full access (though still confined by unix permissions, SELinux etc).

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  The IPA provider, in a setup with a trusted Active Directory domain, did not remove cached entries that were no longer present on the AD side (#3984)
-  The Active Directory provider now fetches the user information from the LDAP port and switches to using the Global Catalog port, if available for the group membership. This fixes an issue where some attributes which are not available in the Global Catalog, typically the home directory, would be removed from the user entry. (#2474)
-  The IPA SELinux provider now sets the user login context even if it is the same as the system default. This is important in case the user has a non-standard home directory, because then only adding the user to the SELinux database ensures the home directory will be labeled properly. However, this fix causes a performance hit during the first login as the context must be written into the semanage database.
-  The sudo responder did not reflect the case_sensitive domain option (#3820)
-  A memory leak when requesting netgroups repeatedly was fixed (#3870)
-  An issue that caused SSSD to sometimes switch to offline mode in case not all domains in the forest ran the Global Catalog service was fixed (#3902)
-  The SSH responder no longer fails completely if the ``p11_child`` times out when deriving SSH keys from a certificate (#3937)
-  The negative cache was not reloaded after new sub domains were discovered which could have lead to a high SSSD load (#3683)
-  The negative cache did not work properly for in case a lookup fell back to trying a UPN instead of a name (#3978)
-  If any of the SSSD responders was too busy, that responder wouldn't have refreshed the trusted domain list (#3967)
-  A potential crash due to a race condition between the fail over code refreshing a SRV lookup and back end using its results (#3976)
-  Sudo's runAsUser and runAsGroup attributes did not match properly when used in setups with domain_resolution_order
-  Processing of the values from the ``filter_users`` or ``filter_groups`` options could trigger calls to blocking NSS API functions which could in turn prevent the startup of SSSD services in case nsswitch.conf contained other modules than ``sss`` or ``files`` (#3963)

Tickets Fixed
-------------

-  `#4940 <https://github.com/SSSD/sssd/issues/4940>`_ - NSS responder does no refresh domain list when busy
-  `#3967 <https://github.com/SSSD/sssd/issues/3967>`_ - Make list of local PAM services allowed for Smartcard authentication configurable
-  `#4813 <https://github.com/SSSD/sssd/issues/4813>`_ - sssd only sets the SELinux login context if it differs from the default
-  `#4814 <https://github.com/SSSD/sssd/issues/4814>`_ - sudo: search with lower cased name for case insensitive domains
-  `#4860 <https://github.com/SSSD/sssd/issues/4860>`_ - nss: memory leak in netgroups
-  `#4478 <https://github.com/SSSD/sssd/issues/4478>`_ - When sssd is configured with id_provider proxy and auth_provider ldap, login fails if the LDAP server is not allowing anonymous binds.
-  `#4865 <https://github.com/SSSD/sssd/issues/4865>`_ - CURLE_SSL_CACERT is deprecated in recent curl versions
-  `#4887 <https://github.com/SSSD/sssd/issues/4887>`_ - SSSD must be cleared/restarted periodically in order to retrieve AD users through IPA Trust
-  `#4886 <https://github.com/SSSD/sssd/issues/4886>`_ - sssd returns '/' for emtpy home directories
-  `#4904 <https://github.com/SSSD/sssd/issues/4904>`_ - sss_cache prints spurious error messages when invoked from shadow-utils on package install
-  `#4839 <https://github.com/SSSD/sssd/issues/4839>`_ - The config file validator says that certmap options are not allowed
-  `#4917 <https://github.com/SSSD/sssd/issues/4917>`_ - If p11_child spawned from sssd_ssh times out, sssd_ssh fails completely
-  `#4934 <https://github.com/SSSD/sssd/issues/4934>`_ - sssd config-check reports an error for a valid configuration option
-  `#4715 <https://github.com/SSSD/sssd/issues/4715>`_ - [RFE] Allow changing default behavior of SSSD from an allow-any default to a deny-any default when it can't find any GPOs to apply to a user login.
-  `#3516 <https://github.com/SSSD/sssd/issues/3516>`_ - AD: do not override existing home-dir or shell if they are not available in the global catalog
-  `#4932 <https://github.com/SSSD/sssd/issues/4932>`_ - sssd_krb5_locator_plugin introduces delay in cifs.upcall krb5 calls
-  `#4876 <https://github.com/SSSD/sssd/issues/4876>`_ - SSSD changes the memory cache file ownership away from the SSSD user when running as root
-  `#4920 <https://github.com/SSSD/sssd/issues/4920>`_ - RemovedInPytest4Warning: Fixture "passwd_ops_setup" called directly
-  `#4309 <https://github.com/SSSD/sssd/issues/4309>`_ - Revert workaround in CI for bug in python-{request,urllib3}
-  `#4950 <https://github.com/SSSD/sssd/issues/4950>`_ - UPN negative cache does not use values from 'filter_users' config option
-  `#4955 <https://github.com/SSSD/sssd/issues/4955>`_ - filter_users option is not applied to sub-domains if SSSD starts offline
-  `#4925 <https://github.com/SSSD/sssd/issues/4925>`_ - SSSD netgroups do not honor entry_cache_nowait_percentage
-  `#4956 <https://github.com/SSSD/sssd/issues/4956>`_ - IPA: Deleted user from trusted domain is not removed properly from the cache on IPA clients
-  `#4949 <https://github.com/SSSD/sssd/issues/4949>`_ - crash in dp_failover_active_server
-  `#4931 <https://github.com/SSSD/sssd/issues/4931>`_ - sudo: runAsUser/Group does not work with domain_resolution_order
-  `#2356 <https://github.com/SSSD/sssd/issues/2356>`_ - RFE Request for allowing password changes using SSSD in DS which dont follow OID's from RFC 3062
-  `#4816 <https://github.com/SSSD/sssd/issues/4816>`_ - Enable generating user private groups only for users with no primary GID
-  `#4936 <https://github.com/SSSD/sssd/issues/4936>`_ - Responders: processing of ``filter_users</span>/<span class="title-ref">filter_groups`` should avoid calling blocking NSS API

Packaging Changes
-----------------

-  Several files in the reference specfile changed permissions to avoid issues with verifying the file integrity with ``rpm -V`` in case SSSD runs as a different user than the default user it is configured with (#3890)

Documentation Changes
---------------------

-  The AD provider default value of ``fallback_homedir`` was changed to ``fallback_homedir = /home/%d/%u`` to provide home directories for users without the ``homeDirectory`` attribute.
-  A new option ``ad_gpo_implicit_deny``, defaulting to False (#3701)
-  A new option ``ldap_pwmodify_mode`` (#1314)
-  A new option ``pam_p11_allowed_services`` (#2926)
-  The ``auto_private_groups`` accepts a new option value ``hybrid`` (#3822)
-  Improved documentation of the Kerberos locator plugin


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_16_3..sssd-1_16_4

    Alexey Tikhonov (5):
        d6ed04f01  Fix error in hostname retrieval
        acce03265  lib/cifs_idmap_sss: fixed unaligned mem access
        2fb5be471  ci/sssd.supp: fixed c-ares-suppress-leak-from-init
        6ff01196f  negcache: avoid "is_*_local" calls in some cases
        5b0bb56a0  Monitor: changed provider startup timeout

    Fabiano Fidêncio (1):
        2b3b41dad  man/sss_ssh_knownhostsproxy: fix typo pubkeys -> pubkey

    Jakub Hrozek (54):
        6bb137cda  Updating the version to track 1.16.4 development
        a57d9ec05  src/tests/python-test.py is GPLv3+
        3badebcc9  src/tests/intg/util.py is licensed under GPLv3+
        e4864db4e  src/tests/intg/test_ts_cache.py is licensed under GPLv3+
        444b463fb  src/tests/intg/test_sudo.py is licensed under GPLv3+
        a54221750  src/tests/intg/test_sssctl.py is licensed under GPLv3+
        252758908  src/tests/intg/test_ssh_pubkey.py is licensed under GPLv3+
        e92040a60  src/tests/intg/test_session_recording.py is licensed under GPLv3+
        33c668e36  src/tests/intg/test_secrets.py is licensed under GPLv3+
        7dc03ff9b  src/tests/intg/test_pysss_nss_idmap.py is licensed under GPLv3+
        3ae7458ad  src/tests/intg/test_pam_responder.py is licensed under GPLv3+
        62a1eb3b2  src/tests/intg/test_pac_responder.py is licensed under GPLv3+
        02008a016  src/tests/intg/test_netgroup.py is licensed under GPLv3+
        7283ee1d0  src/tests/intg/test_memory_cache.py is licensed under GPLv3+
        23df59891  src/tests/intg/test_local_domain.py is licensed under GPLv3+
        5eee13a0d  src/tests/intg/test_ldap.py is licensed under GPLv3+
        85486d23d  src/tests/intg/test_kcm.py is licensed under GPLv3+
        895524e61  src/tests/intg/test_infopipe.py is licensed under GPLv3+
        e7afe9f0e  src/tests/intg/test_files_provider.py is licensed under GPLv3+
        c2296d02c  src/tests/intg/test_files_ops.py is licensed under GPLv3+
        8cc67107e  src/tests/intg/test_enumeration.py is licensed under GPLv3+
        85d939d65  src/tests/intg/sssd_passwd.py is licensed under GPLv3+
        aa5f81746  src/tests/intg/sssd_nss.py is licensed under GPLv3+
        1f244c034  src/tests/intg/sssd_netgroup.py is licensed under GPLv3+
        44d637d05  src/tests/intg/sssd_ldb.py is licensed under GPLv3+
        8a1092b6a  src/tests/intg/sssd_id.py is licensed under GPLv3+
        31f3f7982  src/tests/intg/sssd_group.py is licensed under GPLv3+
        744ae1a07  src/tests/intg/secrets.py is licensed under GPLv3+
        b5c42f4c5  src/tests/intg/ldap_local_override_test.py is licensed under GPLv3+
        b94cf691f  src/tests/intg/ldap_ent.py is licensed under GPLv3+
        fa125f1bc  src/tests/intg/krb5utils.py is licensed under GPLv3+
        89248d04f  src/tests/intg/kdc.py is licensed under GPLv3+
        bcbc2f26d  src/tests/intg/files_ops.py is licensed under GPLv3+
        df5297fd5  src/tests/intg/ent_test.py is licensed under GPLv3+
        ce5a90b34  src/tests/intg/ent.py is licensed under GPLv3+
        79f70d675  src/tests/intg/ds_openldap.py is licensed under GPLv3+
        3ee03cfcb  src/tests/intg/ds.py is licensed under GPLv3+
        de47b6600  src/config/setup.py.in is licensed under GPLv3+
        02d234004  src/config/SSSDConfig/ipachangeconf.py is licensed under GPLv3+
        9ba105f8b  Explicitly add GPLv3+ license blob to several files
        e7e942ceb  SELINUX: Always add SELinux user to the semanage database if it doesn't exist
        bca193576  pep8: Ignore W504 and W605 to silence warnings on Debian
        876f1cb87  LDAP: minor refactoring in auth_send() to conform to our coding style
        7eb18ab68  LDAP: Only authenticate the auth connection if we need to look up user information
        118c44f90  NSS: Avoid changing the memory cache ownership away from the sssd user
        4c1b2d4df  TESTS: Only use __wrap_sss_ncache_reset_repopulate_permanent to finish test if needed
        15f017770  UTIL: Add a is_domain_mpg shorthand
        e01473aa7  UTIL: Convert bool mpg to an enum mpg_mode
        e0c34a688  CONFDB: Read auto_private_groups as string, not bool
        e09dffedc  CONFDB/SYSDB: Add the hybrid MPG mode
        271544b63  CACHE_REQ: Add cache_req_data_get_type()
        c083df056  NSS: Add the hybrid-MPG mode
        64b855dbd  TESTS: Add integration tests for auto_private_groups=hybrid
        4f47ff665  Updating the translations for the 1.16.4 release

    Lukas Slebodnik (26):
        86de91f93  krb5_locator: Make debug function internal
        276f2e345  krb5_locator: Simplify usage of macro PLUGIN_DEBUG
        09dc1d9dc  krb5_locator: Fix typo in debug message
        aefdf7035  krb5_locator: Fix formatting of the variable port
        9680ac9ce  krb5_locator: Use format string checking for debug function
        93caaf294  PAM: Allow to configure pam services for Smartcards
        4d3841ca3  UTIL: Fix compilation with curl 7.62.0
        e80e869a9  test_pac_responder: Skip test if pac responder is not installed
        de7f87730  INTG: Show extra test summary info with pytest
        517fe0710  CI: Modify suppression file for c-ares-1.15.0
        8e6c52f6b  sss_cache: Do not fail for missing domains
        0a27a4716  intg: Add test for sss_cache & shadow-utils use-case
        498aaac23  sss_cache: Do not fail if noting was cached
        7983826c3  test_sss_cache: Add test case for invalidating missing entries
        088eb5451  pyhbac-test: Do not use assertEquals
        b27ab9e75  SSSDConfigTest: Do not use assertEquals
        07d7eeaec  SSSDConfig: Fix ResourceWarning unclosed file
        3c0213fe5  SSSDConfigTest: Remove usage of failUnless
        8f0a2acdc  BUILD: Fix condition for building sssd-kcm man page
        9e6a22489  NSS: Do not use deprecated header files
        6c8084778  sss_cache: Fail if unknown domain is passed in parameter
        3ec716bb0  test_sss_cache: Add test case for wrong domain in parameter
        280512167  test_files_provider: Do not use pytest fixtures as functions
        0fb6543ec  test_ldap: Do not uses pytest fixtures as functions
        688134ee5  Revert "intg: Generate tmp dir with lowercase"
        f44161733  ent_test: Update assertions for python 3.7.2

    Michal Židek (1):
        c96a38294  GPO: Add gpo_implicit_deny option

    Pavel Březina (9):
        2d9286102  sudo: respect case sensitivity in sudo responder
        720a423a0  nss: use enumeration context as talloc parent for cache req result
        486b5523b  netgroups: honor cache_refresh_percent
        93a3a20b6  sdap: add sdap_modify_passwd_send
        be591f08f  sdap: add ldap_pwmodify_mode option
        8d6fa4961  sdap: split password change to separate request
        0a52934c4  sdap: use ldap_pwmodify_mode to change password
        e2f00aea6  sudo ipa: do not store rules without sudoHost attribute
        705fd73e5  be: remember last good server's name instead of fo_server structure

    Sumit Bose (22):
        3dc885344  intg: flush the SSSD caches to sync with files
        1a7c6ab6e  LDAP: Log the encryption used during LDAP authentication
        9e8587956  BUILD: Accept krb5 1.17 for building the PAC plugin
        d1c930809  tests: fix mocking krb5_creds in test_copy_ccache
        19e6c50df  tests: increase p11_child_timeout
        d33ec6442  Revert "IPA: use forest name when looking up the Global Catalog"
        74568bdde  ipa: use only the global catalog service of the forest root
        0a27fba0a  utils: make N_ELEMENTS public
        911d7bb58  ad: replace ARRAY_SIZE with N_ELEMENTS
        382400869  responder: fix domain lookup refresh timeout
        8ffc64c10  ldap: add get_ldap_conn_from_sdom_pvt
        0b5a35969  ldap: prefer LDAP port during initgroups user lookup
        f80dad680  ldap: user get_ldap_conn_from_sdom_pvt() where possible
        1791eed5d  krb5_locator: always use port 88 for master KDC
        6bb46a671  NEGCACHE: initialize UPN negative cache as well
        720907dd7  NEGCACHE: fix typo in debug message
        faede6d27  NEGCACHE: repopulate negative cache after get_domains
        cca33946f  ldap: add users_get_handle_no_user()
        19fbcd1d4  ldap: make groups_get_handle_no_group() public
        c3821674f  ipa s2n: fix typo
        b424c8a1b  ipa s2n: do not add UPG member
        3bed774e9  ipa s2n: try to remove objects not found on the server

    Thorsten Scherf (1):
        5e70cf569  CONFIG: add missing ldap attributes for validation

    Tomas Halman (4):
        28792523a  nss: sssd returns '/' for emtpy home directories
        31637fdfa  ssh: sssd_ssh fails completely on p11_child timeout
        340de230e  ssh: p11_child error message is too generic
        96e4d713a  krb5_locator: Allow hostname in kdcinfo files

    Victor Tapia (1):
        8ba47275a  GPO: Allow customization of GPO_CROND per OS

    mateusz (1):
        db06ec55f  Added note about default value of ad_gpo_map_batch parameter
