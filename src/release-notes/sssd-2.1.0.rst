SSSD 2.1.0 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

-  Any provider can now match and map certificates to user identities. This feature enables to log in with a smart card without having to store the full certificate blob in the directory or in user overrides. Please see `The design page <../../design_pages/certmaps_for_LDAP_AD_file.md>`_ for more information (#3500)
-  ``pam_sss`` can now be configured to only perform Smart Card authentication or return an error if this is not possible.
-  ``pam_sss`` can also prompt the user to insert a Smart Card if, during an authentication it is not available. SSSD would then wait for the card until it is inserted or until timeout defined by ``p11_wait_for_card_timeout`` passes.
-  The device or reader used for Smart Card authentication can now be selected or restricted using a PKCS#11 URI (see RFC-7512) specified in the ``p11_uri`` option.
-  Multiple certificates are now supported for Smart Card authentication even if SSSD is built with OpenSSL
-  OCSP checks were added to the OpenSSL version of certificate authentication
-  A new option ``crl_file`` can be used to select a Certificate Revocation List (CRL) file to be used during verification of a certificate for Smart Card authentication.
-  Certificates with Elliptic Curve keys are now supported (#3887)
-  It is now possible to refresh the KCM configuration without restarting the whole SSSD deamon, just by modifying the ``[kcm]`` section of ``sssd.conf`` and running ``systemctl restart sssd-kcm.service``.
-  A new configuration option ``ad_gpo_implicit_deny`` was added. This option (when set to True) can be used to deny access to users even if there is not applicable GPO. Normally users are allowed access in this situation. (#3701)
-  The dynamic DNS update can now batch DNS updates to include all address family updates in a single transaction to reduce replication traffic in complex environments (#3829)
-  Configuration file snippets can now be used even when the main ``sssd.conf`` file does not exist. This is mostly useful to configure e.g. the KCM responder, the implicit files provider or the session recording with setups that have no explicit domain (#3439)
-  The ``sssctl user-checks`` tool can now display extra attributes set with the InfoPipe ``user_attributes`` configuraton option (#3866)

Security issues fixed
~~~~~~~~~~~~~~~~~~~~~

-  CVE-2019-3811: SSSD used to return "/" in case a user entry had no home directory. This was deemed a security issue because this flaw could impact services that restrict the user's filesystem access to within their home directory. An empty home directory field would indicate "no filesystem access", where sssd reporting it as "/" would grant full access (though still confined by unix permissions, SELinux etc).

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  Many fixes for the internal "sbus" IPC that was rewritten in the 2.0 release including crash on reconnection (#3821), a memory leak (#3810), a proxy provider startup crash (#3812), sudo responder crash (#3854), proxy provider authentication (#3892), accessing the ``extraAttributes`` InfoPipe property (#3906) or a potential startup failure (#3924)
-  The Active Directory provider now fetches the user information from the LDAP port and switches to using the Global Catalog port, if available for the group membership. This fixes an issue where some attributes which are not available in the Global Catalog, typically the home directory, would be removed from the user entry. (#2474)
-  Session recording can now be enabled also for local users when the session recording is configured with ``scope=some`` and restricted to certain groups.
-  Smart Card authentication did not work with the KCM credentials cache because with KCM root cannot write to arbitrary user's credential caches (#3903)
-  A KCM bug that prevented SSH Kerberos credential forwarding from functioning was fixed (#3873)
-  The KCM responder did not work with completely empty database (#3815)
-  The sudo responder did not reflect the case_sensitive domain option (#3820)
-  The SSH responder no longer fails completely if the ``p11_child`` times out when deriving SSH keys from a certificate (#3937)t
-  An issue that caused SSSD to sometimes switch to offline mode in case not all domains in the forest ran the Global Catalog service was fixed (#3902)
-  If any of the SSSD responders was too busy, that responder wouldn't have refreshed the trusted domain list (#3967)
-  The IPA SELinux provider now sets the user login context even if it is the same as the system default. This is important in case the user has a non-standard home directory, because then only adding the user to the SELinux database ensures the home directory will be labeled properly. However, this fix causes a performance hit during the first login as the context must be written into the semanage database.
-  A memory leak when requesting netgroups repeatedly was fixed (#3870)
-  The ``pysss.getgrouplist()`` interface that was removed by accident in the 2.0 version was re-added (#3493)
-  Crash when requesting users with the ``FindByNameAndCertificate`` D-Bus method was fixed (#3863)
-  SSSD can again run as the non-privileged sssd user (#3871)
-  The cron PAM service name used for GPO access control now defaults to a different service name depending on the OS (Launchpad #1572908)

Packaging Changes
-----------------

-  The sbus code generator no longer relies on existance of the "python" binary, the python2/3 binary is used depending on which bindings are being generated (#3807)
-  Very old libini library versions are no longer supported

Documentation Changes
---------------------

-  Two new ``pam_sss`` options ``try_cert_auth`` and ``require_cert_auth`` can restrict authentication to use a Smart Card only or wait for a Smart Card to be inserted.
-  A new option ``p11_wait_for_card_timeout`` controls how long would SSSD wait for a Smart Card to be inserted before failing with ``PAM_AUTHINFO_UNAVAIL``.
-  A new option ``p11_uri`` is available to restrict the device or reader used for Smart Card authentication.

Tickets Fixed
-------------

-  `#4940 <https://github.com/SSSD/sssd/issues/4940>`_ - NSS responder does no refresh domain list when busy
-  `#4934 <https://github.com/SSSD/sssd/issues/4934>`_ - sssd config-check reports an error for a valid configuration option
-  `#4932 <https://github.com/SSSD/sssd/issues/4932>`_ - sssd_krb5_locator_plugin introduces delay in cifs.upcall krb5 calls
-  `#4927 <https://github.com/SSSD/sssd/issues/4927>`_ - gdm login not prompting for username when smart card maps to multiple users
-  `#4920 <https://github.com/SSSD/sssd/issues/4920>`_ - RemovedInPytest4Warning: Fixture "passwd_ops_setup" called directly
-  `#4917 <https://github.com/SSSD/sssd/issues/4917>`_ - If p11_child spawned from sssd_ssh times out, sssd_ssh fails completely
-  `#4916 <https://github.com/SSSD/sssd/issues/4916>`_ - Missing sssd-files in last section(SEE ALSO) of sssd man pages
-  `#4909 <https://github.com/SSSD/sssd/issues/4909>`_ - "Corrupted" name of "Hello" method of org.freedesktop.DBus sssd sbus interface on Fedora Rawhide
-  `#4906 <https://github.com/SSSD/sssd/issues/4906>`_ - crash when requesting extra attributes
-  `#4904 <https://github.com/SSSD/sssd/issues/4904>`_ - sss_cache prints spurious error messages when invoked from shadow-utils on package install
-  `#4902 <https://github.com/SSSD/sssd/issues/4902>`_ - Double free error in tev_curl
-  `#4901 <https://github.com/SSSD/sssd/issues/4901>`_ - Wrong spelling of method
-  `#4897 <https://github.com/SSSD/sssd/issues/4897>`_ - incorrect example in the man page of idmap_sss suggests using \* for backend sss
-  `#4896 <https://github.com/SSSD/sssd/issues/4896>`_ - Re-setting the trusted AD domain fails due to wrong subdomain service name being used
-  `#4895 <https://github.com/SSSD/sssd/issues/4895>`_ - KCM destroy operation returns KRB5_CC_NOTFOUND, should return KRB5_FCC_NOFILE if non-existing ccache is about to be destroyed
-  `#4894 <https://github.com/SSSD/sssd/issues/4894>`_ - SSSD 2.0 has drastically lower sbus timeout than 1.x, this can result in time outs
-  `#4891 <https://github.com/SSSD/sssd/issues/4891>`_ - extraAttributes is org.freedesktop.DBus.Error.UnknownProperty: Unknown property
-  `#4888 <https://github.com/SSSD/sssd/issues/4888>`_ - PKINIT with KCM does not work
-  `#4887 <https://github.com/SSSD/sssd/issues/4887>`_ - SSSD must be cleared/restarted periodically in order to retrieve AD users through IPA Trust
-  `#4886 <https://github.com/SSSD/sssd/issues/4886>`_ - sssd returns '/' for emtpy home directories
-  `#4881 <https://github.com/SSSD/sssd/issues/4881>`_ - sss_cache shouldn't return ENOENT when no entries match
-  `#4878 <https://github.com/SSSD/sssd/issues/4878>`_ - The proxy provider does not copy reply from the child
-  `#4876 <https://github.com/SSSD/sssd/issues/4876>`_ - SSSD changes the memory cache file ownership away from the SSSD user when running as root
-  `#4875 <https://github.com/SSSD/sssd/issues/4875>`_ - Abort LDAP authentication if the check_encryption function finds out the connection is not authenticated
-  `#4873 <https://github.com/SSSD/sssd/issues/4873>`_ - sssd support for for smartcards using ECC keys
-  `#4869 <https://github.com/SSSD/sssd/issues/4869>`_ - Missing concise documentation about valid options for sssd-files-provider
-  `#4866 <https://github.com/SSSD/sssd/issues/4866>`_ - Unable to su to root when logged in as a local user
-  `#4865 <https://github.com/SSSD/sssd/issues/4865>`_ - CURLE_SSL_CACERT is deprecated in recent curl versions
-  `#4864 <https://github.com/SSSD/sssd/issues/4864>`_ - RefreshRules_recv marks the wrong request as done
-  `#4863 <https://github.com/SSSD/sssd/issues/4863>`_ - Perform some basic ccache initialization as part of gen_new to avoid a subsequent switch call failure
-  `#4862 <https://github.com/SSSD/sssd/issues/4862>`_ - SSSD 2.x does not sanitize domain name properly for D-bus, resulting in a crash
-  `#4861 <https://github.com/SSSD/sssd/issues/4861>`_ - sbus: allow non-root execution
-  `#4856 <https://github.com/SSSD/sssd/issues/4856>`_ - sssctl user-checks does not show custom IFP user_attributes
-  `#4855 <https://github.com/SSSD/sssd/issues/4855>`_ - Off-by-one error in retrieving host name causes hostnames with exactly 64 characters to not work
-  `#4853 <https://github.com/SSSD/sssd/issues/4853>`_ - sssd ifp crash when trying FindByNameAndCertificate
-  `#4852 <https://github.com/SSSD/sssd/issues/4852>`_ - Restarting the sssd-kcm service should reload the configuration without having to restart the whole sssd
-  `#4848 <https://github.com/SSSD/sssd/issues/4848>`_ - sssctl user-show says that user is expired if the user comes from files provider
-  `#4845 <https://github.com/SSSD/sssd/issues/4845>`_ - session not recording for local user when groups defined
-  `#4844 <https://github.com/SSSD/sssd/issues/4844>`_ - sudo: sbus2 related crash
-  `#4842 <https://github.com/SSSD/sssd/issues/4842>`_ - Files: The files provider always enumerates which causes duplicate when running getent passwd
-  `#4841 <https://github.com/SSSD/sssd/issues/4841>`_ - pam_unix unable to match fully qualified username provided by sssd during smartcard auth using gdm
-  `#4839 <https://github.com/SSSD/sssd/issues/4839>`_ - The config file validator says that certmap options are not allowed
-  `#4835 <https://github.com/SSSD/sssd/issues/4835>`_ - The simultaneous use of strncpy and a length-check in client code is confusing Coverity
-  `#4824 <https://github.com/SSSD/sssd/issues/4824>`_ - Printing incorrect information about domain with sssctl utility
-  `#4823 <https://github.com/SSSD/sssd/issues/4823>`_ - SSSD does not batch DDNS update requests
-  `#4822 <https://github.com/SSSD/sssd/issues/4822>`_ - Invalid domain provider causes SSSD to abort startup
-  `#4821 <https://github.com/SSSD/sssd/issues/4821>`_ - SSSD should log to syslog if a domain is not started due to a misconfiguration
-  `#4820 <https://github.com/SSSD/sssd/issues/4820>`_ - Remove references of sss_user/group/add/del commands in man pages since local provider is deprecated
-  `#4815 <https://github.com/SSSD/sssd/issues/4815>`_ - crash related to sbus_router_destructor()
-  `#4809 <https://github.com/SSSD/sssd/issues/4809>`_ - KCM: The secdb back end might fail creating a new ID with a completely empty database
-  `#4808 <https://github.com/SSSD/sssd/issues/4808>`_ - [RFE] Add option to specify a Smartcard with a PKCS#11 URI
-  `#4807 <https://github.com/SSSD/sssd/issues/4807>`_ - sssd startup issues since 1.16.2 (PID file related)
-  `#4806 <https://github.com/SSSD/sssd/issues/4806>`_ - sssd 2.0.0 segfaults on startup
-  `#4804 <https://github.com/SSSD/sssd/issues/4804>`_ - sbus2: fix memory leak in sbus_message_bound_ref
-  `#4802 <https://github.com/SSSD/sssd/issues/4802>`_ - The sbus codegen script relies on "python" which might not be available on all distributions
-  `#4797 <https://github.com/SSSD/sssd/issues/4797>`_ - Reuse sysdb_error_to_errno() outside sysdb
-  `#4794 <https://github.com/SSSD/sssd/issues/4794>`_ - When passwords are set to cache=false, userCertificate auth fails when backend is offline
-  `#4793 <https://github.com/SSSD/sssd/issues/4793>`_ - When AD provider is offline, usercertmap fails
-  `#4715 <https://github.com/SSSD/sssd/issues/4715>`_ - [RFE] Allow changing default behavior of SSSD from an allow-any default to a deny-any default when it can't find any GPOs to apply to a user login.
-  `#4670 <https://github.com/SSSD/sssd/issues/4670>`_ - RFE: Require smartcard authentication
-  `#4621 <https://github.com/SSSD/sssd/issues/4621>`_ - [RFE] Allow sssd to read the certificate attributes instead of blob look-up against the LDAP
-  `#4600 <https://github.com/SSSD/sssd/issues/4600>`_ - sssd-kcm failed to start on F-27 after installing sssd-kcm
-  `#4591 <https://github.com/SSSD/sssd/issues/4591>`_ - SYSDB: Lowercased email is stored as nameAlias
-  `#4526 <https://github.com/SSSD/sssd/issues/4526>`_ - Make sure sssd is a replacement for pam_pkcs11 also for local account authentication
-  `#4515 <https://github.com/SSSD/sssd/issues/4515>`_ - p11_child should work wit openssl1.0+
-  `#4478 <https://github.com/SSSD/sssd/issues/4478>`_ - When sssd is configured with id_provider proxy and auth_provider ldap, login fails if the LDAP server is not allowing anonymous binds.
-  `#4466 <https://github.com/SSSD/sssd/issues/4466>`_ - Snippets are not used when sssd.conf does not exist
-  `#4440 <https://github.com/SSSD/sssd/issues/4440>`_ - a bug in libkrb5 causes kdestroy -A to not work with more than 2 principals with KCM
-  `#4365 <https://github.com/SSSD/sssd/issues/4365>`_ - sssctl config-check does not check any special characters in domain name of domain section
-  `#4364 <https://github.com/SSSD/sssd/issues/4364>`_ - usermod -a -G bar foo fails due to some file providers races
-  `#4309 <https://github.com/SSSD/sssd/issues/4309>`_ - Revert workaround in CI for bug in python-{request,urllib3}
-  `#4296 <https://github.com/SSSD/sssd/issues/4296>`_ - consider adding sudo-i to the list of pam_response_filter services by default
-  `#3858 <https://github.com/SSSD/sssd/issues/3858>`_ - dynamic dns - remove detection of 'realm' keyword support
-  `#3516 <https://github.com/SSSD/sssd/issues/3516>`_ - AD: do not override existing home-dir or shell if they are not available in the global catalog
-  `#2986 <https://github.com/SSSD/sssd/issues/2986>`_ - convert dyndns timer to be_ptask


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_16_3..sssd-2_1_0

    Adam Williamson (1):
        e4469fbdb  sbus: use 120 second default timeout

    Alexey Tikhonov (16):
        170625872  Fix error in hostname retrieval
        15bde7dab  util/tev_curl: Fix double free error in schedule_fd_processing()
        8e9e8011c  CONFIG: validator rules & test
        484b48ff4  sss_client/common.c: fix Coverity issue
        9959fbe70  sss_client/common.c: fix off-by-one error in sizes check
        bc92d36c9  sss_client/common.c: comment amended
        6e2df759d  sss_client/nss_services.c: indentation fixed
        08d5dabc5  sss_client/nss_services.c: fixed incorrect mutex usage
        0d96e175a  sss_client: global unexported symbols made static
        49c13e9aa  providers/ldap: abort unsecure authentication requests
        53cc1187d  providers/ldap: fixed check of ldap_get_option return value
        a04d088d9  providers/ldap: init sasl_ssf in specific case
        38ebae7e0  sbus/interface: fixed interface copy helpers
        12f74f8c9  lib/cifs_idmap_sss: fixed unaligned mem access
        d575d85c0  Util: fixed mistype in error string representation
        9ad7173ee  TESTS: fixed bug in guests startup function

    Amit Kumar (1):
        a2d543f61  providers: disable ldap_sudo_include_regexp by default

    Fabiano Fidêncio (19):
        2b3b41dad  man/sss_ssh_knownhostsproxy: fix typo pubkeys -> pubkey
        65bd6bf05  providers: drop ldap_{init,}groups_use_matching_rule_in_chain support
        5dafa8177  ldap: remove parallel requests from rfc2307bis
        7d483737f  tests: adapt common_dom to files_provider
        2243b3489  tests: adapt test_sysdb_views to files provider
        35a200d5b  tests: adapt sysdb-tests to files_provider
        6ebcc59b9  tests: adapt sysdb_ssh tests to files provider
        064ca0b46  tests: adapt auth-tests to files provider
        a8a9e66a8  tests: adapt tests_fqnames to files provider
        99b5bb544  sysdb: sanitize the dn on cleanup_dn_filter
        728e4be10  sysdb: pass subfilter and ts_subfilter to sysdb_search_*_by_timestamp()
        2e8fe6a3d  tests: adapt test_ldap_id_cleanup to files provider
        a24f0c202  tests: remove LOCAL_SYSDB_FILE reference from test_sysdb_certmap
        5a87af912  tests: remove LOCAL_SYSDB_FILE reference from test_sysdb_domain_resolution_order_
        15342ebe8  tests: remove LOCAL_SYSDB_FILE reference from test_sysdb_subdomains
        c075e2865  tests: remove LOCAL_SYSDB_FILE reference from common_dom
        b8946c46e  local: build local provider conditionally
        82d51b7fe  pysss: fix typo in comment
        0e211b8ba  pysss: remove pysss.local

    George McCollister (1):
        7354e59e0  build: remove hardcoded samba include path

    Jakub Hrozek (93):
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
        2f34087cf  Updating the version before the 2.0 release
        4d7f07893  TESTS: the sys package was used but not imported
        aafaacd59  TESTS: Remove tests database in teardown
        0294bcf7c  TESTS: Properly set argv[0] when starting the secrets responder
        80811f941  KCM: Move a confusing DEBUG message
        ca73eedba  KCM: Fix a typo
        24b151e07  UTIL: Add libsss_secrets
        fdfa36ae0  SECRETS: Use libsss_secrets
        e0bf64a73  KCM; Hide the secret URL as implementation detail instead of exposing it in the JSON-marshalling API
        0b9001e3a  UTIL: libsss_secrets: Add an update function
        24ba21206  KCM: Add a new back end that uses libsss_secrets directly
        f91adcc8e  TESTS: Get rid of KCM_PEER_UID
        7dd1991c9  TESTS: Add tests for the KCM libsss_secrets back end
        f74feb08b  KCM: Change the default ccache storage from the secrets responder to libsecrets
        fcbedf46f  BUILD: Do not build the secrets responder by default
        7dce2461e  Updating the version to track 2.1 development
        81dce1979  KCM: Don't error out if creating a new ID as the first step
        945865ae1  SELINUX: Always add SELinux user to the semanage database if it doesn't exist
        ec7665973  pep8: Ignore W504 and W605 to silence warnings on Debian
        941e67b0b  TESTS: Add a test for whitespace trimming in netgroup entries
        1e67da79a  TESTS: Add two basic multihost tests for the files provider
        7b3794fbe  FILES: The files provider should not enumerate
        7794caec3  p11: Fix two instances of -Wmaybe-uninitialized in p11_child_openssl.c
        fc29c3eb9  UTIL: Suppress Coverity warning
        f0603645f  PYSSS: Re-add the pysss.getgrouplist() interface
        0882793e4  IFP: Use subreq, not req when calling RefreshRules_recv
        c42fb8de5  CI: Make the c-ares suppression file more relaxed to prevent failures on Debian
        8007d6150  INI: Return errno, not -1 on failure from sss_ini_get_stat
        4b52ed061  MONITOR: Don't check for pidfile if SSSD is already running
        92b8f8d40  SSSD: Allow refreshing only certain section with --genconf
        c53fc08a7  SYSTEMD: Re-read KCM configuration on systemctl restart kcm
        fc25224ea  TEST: Add a multihost test for sssd --genconf
        66da9d9db  TESTS: Add a multihost test for changing sssd-kcm debug level by just restarting the KCM service
        75696ddc8  RESPONDER: Log failures from bind() and listen()
        09091b4b6  LDAP: minor refactoring in auth_send() to conform to our coding style
        57fc60c9d  LDAP: Only authenticate the auth connection if we need to look up user information
        807bbce25  PROXY: Copy the response to the caller
        61e4ba589  NSS: Avoid changing the memory cache ownership away from the sssd user
        02c15d40e  KCM: Deleting a non-existent ccache should not yield an error
        46e52b036  TESTS: Add a test for deleting a non-existent ccache with KCM
        f94881d4d  MAN: Explicitly state that not all generic domain options are supported for the files provider
        b3285f9f8  AD/IPA: Reset subdomain service name, not domain name
        aaaa9a3e8  IPA: Add explicit return after tevent_req_error
        bb98486fb  MULTIHOST: Do not use the deprecated namespace
        334950e4b  KCM: Return a valid tevent error code if a request cannot be created
        7c441a132  KCM: Allow representing ccaches with a NULL principal
        d0eae0598  KCM: Create an empty ccache on switch to a non-existing one
        ac95d4f07  TESTS: Add a multihost test for ssh credentials forwarding
        d409df332  MAN: Add sssd-files(5) to the See Also section
        05c6ed550  TESTS: Add a simple integration test for retrieving the extraAttributes property
        713e4f929  TESTS: Don't fail when trying to create an OU that already exists
        6a8e906ec  Updating translations for the 2.1 release
        3aee2b3a8  Updating the version for the 2.1.0 release

    Lukas Slebodnik (35):
        86de91f93  krb5_locator: Make debug function internal
        276f2e345  krb5_locator: Simplify usage of macro PLUGIN_DEBUG
        09dc1d9dc  krb5_locator: Fix typo in debug message
        aefdf7035  krb5_locator: Fix formatting of the variable port
        9680ac9ce  krb5_locator: Use format string checking for debug function
        93caaf294  PAM: Allow to configure pam services for Smartcards
        101934f29  BUILD: Fix issue with installation of libsss_secrets
        677a93372  BUILD: Add missing deps to libsss_sbus*.so
        53ed60b87  BUILD: Reduce compilation of unnecessary files
        e5dc30e00  MAN: Fix typo in ad_gpo_implicit_deny default value
        05ba237af  CONFIGURE: Add minimal required version for p11-kit
        d143319bc  SBUS: Silence warning maybe-uninitialized
        1ee12b055  UTIL: Fix compilation with curl 7.62.0
        4f824eca2  test_pac_responder: Skip test if pac responder is not installed
        fdbe67a88  INTG: Show extra test summary info with pytest
        5e703d3d4  p11_child: Fix warning cast discards ‘const’ qualifier from pointer target type
        f02714d6f  CI: Modify suppression file for c-ares-1.15.0
        88c0c3fcd  sss_cache: Do not fail for missing domains
        325df4aca  intg: Add test for sss_cache & shadow-utils use-case
        71475f1ed  sss_cache: Do not fail if noting was cached
        415094687  test_sss_cache: Add test case for invalidating missing entries
        9b06c750b  pyhbac-test: Do not use assertEquals
        c4db34c17  SSSDConfigTest: Do not use assertEquals
        769dc2447  SSSDConfig: Fix ResourceWarning unclosed file
        21bba0509  SSSDConfigTest: Remove usage of failUnless
        39b3b0e4a  BUILD: Fix condition for building sssd-kcm man page
        f2a327f5a  DIST: Do not use conditional include for template files
        afd23bd7f  NSS: Do not use deprecated header files
        2de3c5fb2  sss_cache: Fail if unknown domain is passed in parameter
        159a2316b  test_sss_cache: Add test case for wrong domain in parameter
        7133c7fc7  Remove macro ZERO_STRUCT
        686a8f5f1  test_files_provider: Do not use pytest fixtures as functions
        948cd08cd  test_ldap: Do not uses pytest fixtures as functions
        577346336  Revert "intg: Generate tmp dir with lowercase"
        54d7175d0  ent_test: Update assertions for python 3.7.2

    Madhuri Upadhye (1):
        dd2e6f26e  pytest: Add test cases for configuration validation

    Michal Židek (4):
        3bd67c772  GPO: Add gpo_implicit_deny option
        10fa27edd  CONFDB: Skip 'local' domain if not supported
        8a3517c54  confdb: Always read snippet files
        b66f8dc3b  CONFDB: Remove old libini support

    Niranjan M.R (20):
        c0374e1cb  Python3 changes to multihost tests
        aba6fe447  Minor fixes related to converting of ldap attributes to bytes
        e573f5779  test-library: fixes related to KCM, TLS on Directory server
        ac622b771  Multihost-SanityTests: New test case for ssh login with KCM as default
        74f24e9b3  pytest: Remove installing idm module
        4276b3f73  pytest/testlib: Add function to create organizational Unit
        a62caa0e3  pytest/testlib: Fix related to removing kerberos database
        2ac3efd11  pytest: Add test for sudo: search with lower cased name for case insensitive domains
        58d11ae61  pytest/testlib: function to create sudorules in ldap
        783330657  pytest/testlib: remove space in CA DN
        56842e706  pytest/conftest.py: Delete krb5.keytab as part of cleanup
        0e8f9ffe9  pytest: split kcm test cases in to separate file.
        a0280715c  testlib: Update update_resolv_conf() to decode str to bytes
        ac04d19fd  testlib: Replace Generic Exception with SSSDException and LdapException
        6dcc34d09  pytest/sudo: Modify fixture to restore sssd.conf
        ba87d7834  pytest/sudo: Rename create_sudorule to case_sensitive_sudorule
        4dcef8832  pytest/sudo: call case_sensitive_sudorule fixture instead of create_sudorule
        a5133f3ab  pytest/sudo: Add 2 fixtures set_entry_cache_sudo_timeout and generic_sudorule
        fa2106a7a  pytest/sudo: Add Testcase: sssd crashes when refreshing expired sudo rules.
        5c550e72e  pytest: use ConfigParser() instead of SafeConfigParser()

    Pavel Březina (46):
        7e9f0a0c9  include stdarg.h directly in debug.h
        40e3863ef  pam_add_response: fix talloc context
        c2ed0caee  sss_ptr_hash: add sss_ptr_get_value to make it useful in delete callbacks
        9c9a43283  sss_ptr_list: add linked list of talloc pointers
        e347b5557  sbus: move sbus code to standalone library
        564c0798a  sbus: add sbus sssd error codes
        b49ee1bfc  sbus: add new implementation
        7f3ed0787  sbus: build new sbus implementation
        f91e90a76  sbus: disable generating old api
        06631b456  sbus: fix indirect includes in sssd
        2963f2d91  sbus: add sss_iface library
        924f80983  sbus: convert monitor
        c7e2d7a56  sbus: convert backend
        e50fb8ace  sbus: convert responders
        de3a63c4b  sbus: convert proxy provider
        fbe2476a3  sbus: convert infopipe
        aaecabf2d  sbus: convert sssctl
        5edba6ce4  sbus: remove old implementation
        7c1dd71c3  sbus: add new internal libraries to specfile
        3d1b64585  sbus: make tests run
        c0c8499b6  tests: disable parse_inp_call_dp, parse_inp_call_attach in responder-get-domains-tests
        55d5b4354  sbus: register filter on new connection
        8c8f74b0d  sbus: fix typo
        30f4adf87  sbus: check for null message in sbus_message_bound
        ca50c4051  sbus: replace sbus_message_bound_ref with sbus_message_bound_steal
        c895fa244  sbus: add unit tests for public sbus_message module
        d7f0b58e2  sudo: respect case sensitivity in sudo responder
        4ffe3ab90  proxy: access provider directly not through be_ctx
        4c5a1afa0  dp: set be_ctx->provider as part of dp_init request
        9245bf1af  sbus: read destination after sender is set
        b821ee3ca  sbus: do not try to remove signal listeners when disconnecting
        f1f9af528  sbus: free watch_fd->fdevent explicitly
        dfa7bf113  be: use be_is_offline for the main domain when asking for domain status
        250e82252  sudo: use correct sbus interface
        8fbaf2241  sudo: fix error handling in sudosrv_refresh_rules_done
        c74b430ba  sbus: remove leftovers from previous implementation
        4760eae9b  sbus: allow access for sssd user
        406b731dd  nss: use enumeration context as talloc parent for cache req result
        f47940356  sss_iface: prevent from using invalid names that start with digits
        36255b893  ci: add ability to run tests in jenkins
        bf248a397  ci: add Fedora 29
        bc1e8ffd5  sbus: do not use signature when copying dictionary entry
        194438830  sbus: avoid using invalid stack point in SBUS_INTERFACE
        e185b0394  sbus: improve documentation of SBUS_INTERFACE
        138059b2c  ci: add Fedora Rawhide
        ffd7536df  sbus: terminated active ongoing request when reconnecting

    Sumit Bose (63):
        1e2398870  intg: flush the SSSD caches to sync with files
        b03179ead  sbus: dectect python binary for sbus_generate.sh
        7c619ae08  sysdb: extract sysdb_ldb_msg_attr_to_certmap_info() call
        d1dd7f770  sysdb_ldb_msg_attr_to_certmap_info: set SSS_CERTMAP_MIN_PRIO
        0bf709ad3  sysdb: add attr_map attribute to sysdb_ldb_msg_attr_to_certmap_info()
        d9cc38008  confdb: add confdb_certmap_to_sysdb()
        15301db1d  AD/LDAP: read certificate mapping rules from config file
        06f7005d3  sysdb: sysdb_certmap_add() handle domains more flexible
        9386ef605  confdb: add special handling for rules for the files provider
        275eeed24  files: add support for Smartcard authentication
        9fdc5f1d8  responder: make sure SSS_DP_CERT is passed to files provider
        d42f44d54  PAM: add certificate matching rules from all domains
        0c739e969  doc: add certificate mapping section to man page
        16941c47a  intg: user default locale
        442ae7b1d  PAM: use better PAM error code for failed Smartcard authentication
        91aea762d  test_ca: test library only for readable
        a45a410dc  test_ca: set a password/PIN to nss databases
        d332c8a0e  getsockopt_wrapper: add support for PAM clients
        657f3b89b  intg: add Smartcard authentication tests
        e18c67c38  ci: add http-parser-devel for Fedora
        e29b82077  p11: handle multiple certs during auth with OpenSSL
        42f69e26e  p11_child: add --wait_for_card option
        2e4ecf5a8  PAM: add p11_wait_for_card_timeout option
        d33a8bed5  pam_sss: make flags public
        d3a18f061  pam_sss: add try_cert_auth option
        49be8974b  pam_sss: add option require_cert_auth
        5cdb6968f  intg: require SC tests
        46fd681a7  p11_child: show PKCS#11 URI in debug output
        f7b2152a4  p11_child: add PKCS#11 uri to restrict selection
        725b65081  PAM: add p11_uri option
        4a22fb6bb  tests: add PKCS#11 URI tests
        dbd717fe5  PAM: return short name for files provider users
        91c608d0e  p11_child: add OCSP check ot the OpenSSL version
        3c096c9ad  p11_child: add crl_file option for the OpenSSL build
        46c483c09  files: add session recording flag
        b4063b2d3  ifp: fix typo causing a crash in FindByNameAndCertificate
        55470b17e  pam_sss: return PAM_AUTHINFO_UNAVAIL if sc options are set
        6286f8120  p11_child(NSS): print key type in a debug message
        ef631f9e6  pam_test_srv: set default value for SOFTHSM2_CONF
        a0cdc3bdf  tests: add ECC CA
        a7421b526  test_pam_srv: add test for certificate with EC keys
        d64d9cfbe  p11_child(openssl): add support for EC keys
        ad3356d10  utils: refactor ssh key extraction (OpenSSL)
        41c4661b6  utils: add ec_pub_key_to_ssh() (OpenSSL)
        4e627add3  utils: refactor ssh key extraction (NSS)
        3906e5f41  utils: add ec_pub_key_to_ssh() (NSS)
        53e6fdfd8  BUILD: Accept krb5 1.17 for building the PAC plugin
        08bba3a6e  tests: fix mocking krb5_creds in test_copy_ccache
        1617f3e3d  tests: increase p11_child_timeout
        6f113c7dd  LDAP: Log the encryption used during LDAP authentication
        9096fc01c  Revert "IPA: use forest name when looking up the Global Catalog"
        62d671b87  ipa: use only the global catalog service of the forest root
        d33eaac87  p11_child(openssl): do not free static memory
        e49e9f727  krb5_child: fix permissions during SC auth
        ea7ada6c0  idmap_sss: improve man page
        3eb99a171  PAM: use user name hint if any domain has set it
        e32920a9c  utils: make N_ELEMENTS public
        e1ff063ff  ad: replace ARRAY_SIZE with N_ELEMENTS
        c01364341  responder: fix domain lookup refresh timeout
        eaece8b2e  ldap: add get_ldap_conn_from_sdom_pvt
        b2352a01f  ldap: prefer LDAP port during initgroups user lookup
        3cb9a3db9  ldap: user get_ldap_conn_from_sdom_pvt() where possible
        05350abdf  krb5_locator: always use port 88 for master KDC

    Thorsten Scherf (1):
        85e363086  CONFIG: add missing ldap attributes for validation

    Tomas Halman (14):
        de8c9caf6  doc: remove local provider reference from manpages
        081b18e75  confdb: log an error when domain is misconfigured
        0be037bbe  doc: Add nsswitch.conf note to manpage
        7a2e56d06  test_config: Test for invalid characker in domain
        f62f3b290  UTIL: move and rename sysdb_error_to_errno to utils
        ed476c870  DYNDNS: Drop support for legacy NSUPDATE
        291071cb3  SSSCTL: user-show says that user is expired
        df9e4802c  DYNDNS: Convert dyndns timer to be_ptask
        5565dd365  DYNDNS: SSSD does not batch DDNS update requests
        90f32399b  nss: sssd returns '/' for emtpy home directories
        814889a7f  ifp: extraAttributes is UnknownProperty
        ee9fdb08f  SSSCTL: user-checks does not show custom attributes
        e1755a00f  ssh: sssd_ssh fails completely on p11_child timeout
        52c833613  ssh: p11_child error message is too generic

    Victor Tapia (1):
        bc65ba9a0  GPO: Allow customization of GPO_CROND per OS

    amitkuma (1):
        1adf2f982  confdb: Remove CONFDB_DOMAIN_LEGACY_PASS

    mateusz (1):
        938dd6c1a  Added note about default value of ad_gpo_map_batch parameter
