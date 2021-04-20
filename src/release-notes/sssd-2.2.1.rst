SSSD 2.2.1 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

-  New options were added which allow sssd-kcm to handle bigger data. See manual pages for ``max_ccaches``, ``max_uid_caches`` and ``max_ccache_size``.
-  SSSD can now automatically refresh cached user data from subdomains in IPA/AD trust.

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  Fixed issue with SSSD hanging when connecting to non-responsive server with `ldaps:// <ldaps://>`_
-  SSSD is now restarted by systemd after crashes.
-  Fixed refression when dyndns_update was set to True and dyndns_refresh_interval was not set or set to 0 then DNS records were not updated at all.
-  Fixed issue when ``default_domain_suffix`` was used with ``id_provider = files`` and caused all results from files domain to be fully qualified.
-  Fixed issue with sudo rules not being visible on OpenLDAP servers
-  Fixed crash with ``auth_provider = proxy`` that prevented logins

Packaging Changes
-----------------

None

Documentation Changes
---------------------

A new option ``dns_resolver_server_timeout`` was added A new option ``max_ccaches`` was added A new option ``max_uid_ccaches`` was added A new option ``max_ccache_size`` was added A new option ``ocsp_dgst`` was added

Tickets Fixed
-------------

-  `#3919 <https://github.com/SSSD/sssd/issues/3919>`_ - sssd failover does not work on connecting to non-responsive <ldaps://server
-  `#4250 <https://github.com/SSSD/sssd/issues/4250>`_ - Conflicting default timeout values
-  `#4413 <https://github.com/SSSD/sssd/issues/4413>`_ - sssd-kcm cannot handle big tickets
-  `#4515 <https://github.com/SSSD/sssd/issues/4515>`_ - p11_child should work wit openssl1.0+
-  `#4704 <https://github.com/SSSD/sssd/issues/4704>`_ - KCM: Default to a new back end that would write to the secrets database directly
-  `#4827 <https://github.com/SSSD/sssd/issues/4827>`_ - port to pcre2
-  `#4880 <https://github.com/SSSD/sssd/issues/4880>`_ - multihost tests: ldb-tools is needed for multihost tests
-  `#4890 <https://github.com/SSSD/sssd/issues/4890>`_ - SSSD doesn't clear cache entries for IDs below min_id.
-  `#4983 <https://github.com/SSSD/sssd/issues/4983>`_ - SSSD is not refreshing cached user data for the ipa sub-domain in a IPA/AD trust
-  `#4996 <https://github.com/SSSD/sssd/issues/4996>`_ - EVP_PKEY_new_raw_private_key() was only added in OpenSSL 1.1.1
-  `#4998 <https://github.com/SSSD/sssd/issues/4998>`_ - sssd-kcm calls sssd-genconf which triggers nscd warning
-  `#5006 <https://github.com/SSSD/sssd/issues/5006>`_ - Logins fail after upgrade to 2.2.0
-  `#5009 <https://github.com/SSSD/sssd/issues/5009>`_ - Reasonable to Restart sssd on crashes?
-  `#5014 <https://github.com/SSSD/sssd/issues/5014>`_ - sudo: incorrect usn value for openldap
-  `#5015 <https://github.com/SSSD/sssd/issues/5015>`_ - dyndns_update = True is no longer not enough to get the IP address of the machine updated in IPA upon sssd.service startup
-  `#5018 <https://github.com/SSSD/sssd/issues/5018>`_ - nss_cmd_endservent resets the wrong index
-  `#5020 <https://github.com/SSSD/sssd/issues/5020>`_ - sssd config option "default_domain_suffix" should not cause the files domain entries to be qualified
-  `#4911 <https://github.com/SSSD/sssd/issues/4911>`_ - proxy provider is not working with enumerate=true when trying to fetch all groups
-  `#5012 <https://github.com/SSSD/sssd/issues/5012>`_ - Typo in systemd.m4 prevents detection of systemd.pc
-  `#4950 <https://github.com/SSSD/sssd/issues/4950>`_ - UPN negative cache does not use values from 'filter_users' config option
-  `#5002 <https://github.com/SSSD/sssd/issues/5002>`_ - p11_child::do_ocsp() function implementation is not FIPS140 compliant
-  `#5008 <https://github.com/SSSD/sssd/issues/5008>`_ - p11_child::sign_data() function implementation is not FIPS140 compliant
-  `#5024 <https://github.com/SSSD/sssd/issues/5024>`_ - permission denied on logs when running sssd as non-root user
-  `#4995 <https://github.com/SSSD/sssd/issues/4995>`_ - Non FIPS140 compliant usage of PRNG
-  `#3895 <https://github.com/SSSD/sssd/issues/3895>`_ - FAIL test-find-uid
-  `#4935 <https://github.com/SSSD/sssd/issues/4935>`_ - Problem with tests/cmocka/test_dyndns.c
-  `#4993 <https://github.com/SSSD/sssd/issues/4993>`_ - utils: sss_hmac_sha1() function implementation is not FIPS140 compliant
-  `#4995 <https://github.com/SSSD/sssd/issues/4995>`_ - Non FIPS140 compliant usage of PRNG
-  `#4996 <https://github.com/SSSD/sssd/issues/4996>`_ - EVP_PKEY_new_raw_private_key() was only added in OpenSSL 1.1.1

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-2_2_0..sssd-2_2_1

    Alex Rodin (1):
        ff8284e22  tests/cmocka/test_dyndns.c: Switching from tevent_loop_once() to tevent_loop_wait()

    Alexey Tikhonov (14):
        6839e6720  util/crypto/libcrypto: changed sss_hmac_sha1()
        ee23b8e3a  util/crypto/libcrypto: changed sss_hmac_sha1()
        e8e0f4079  util/secrets: memory leaks are fixed
        8aa0dfdf6  util/crypto/nss/nss_nite: params sanitization
        d603d34a6  crypto/libcrypto/crypto_nite: HMAC calculation changed
        e232a98a0  util/find_uid.c: fixed debug message
        0897be2ab  util/find_uid.c: fixed race condition bug
        8be1a0e82  util/crypto: removed erroneous declaration
        e839acd1f  util/crypto/sss_crypto.c: cleanup of includes
        9f4b7d9fb  util/crypto: generate_csprng_buffer() changed
        93d0aba5a  util/crypto: added sss_rand()
        bfc02ea2c  crypto/libcrypto/crypto_nite.c: memory leak fixed
        548ea5746  FIPS140 compliant usage of PRNG
        1f528861d  crypto/nss: some nss_ctx_init() params made const

    Jakub Hrozek (34):
        3ee29f4b5  Updating the version for the 2.2.1 release
        2a53df354  TESTS: Install expect to drive password-change modifications
        71ae2eda2  TESTS: Also add LDAP password when creating users
        7ad11b289  TESTS: Test changing LDAP password with extended operation and modification
        dfa50c214  TEST: Add a multihost test for not returning / for an empty home dir
        0a10d863f  MONITOR: Don't check for the nscd socket while regenerating configuration
        db99504a5  SYSDB: Add sysdb_search_with_ts_attr
        f27955297  BE: search with sysdb_search_with_ts_attr
        1a08b53de  BE: Enable refresh for multiple domains
        bb0bd61ac  BE: Make be_refresh_ctx_init set up the periodical task, too
        9d49c90ce  BE/LDAP: Call be_refresh_ctx_init() in the provider libraries, not in back end
        d1eb0a70d  BE: Pass in attribute to look up with instead of hardcoding SYSDB_NAME
        41305ef5a  BE: Change be_refresh_ctx_init to return errno and set be_ctx->refresh_ctx
        ac72bb4ab  BE/LDAP: Split out a helper function from sdap_refresh for later reuse
        2cb294e6d  BE: Pass in filter_type when creating the refresh account request
        7443498cc  BE: Send refresh requests in batches
        0fbc317ac  BE: Extend be_ptask_create() with control when to schedule next run after success
        576f3691a  BE: Schedule the refresh interval from the finish time of the last run
        b72adfcc3  AD: Implement background refresh for AD domains
        d76756ef4  IPA: Implement background refresh for IPA domains
        1d0e75e9c  BE/IPA/AD/LDAP: Add inigroups refresh support
        792235097  BE/IPA/AD/LDAP: Initialize the refresh callback from a list to reduce logic duplication
        60c876aef  IPA/AD/SDAP/BE: Generate refresh callbacks with a macro
        039384b88  MAN: Amend the documentation for the background refresh
        7a08d1dea  DP/SYSDB: Move the code to set initgrExpireTimestamp to a reusable function
        cdc44a05d  IPA/AD/LDAP: Increase the initgrExpireTimestamp after finishing refresh request
        ca02a20c1  MAN: Get rid of sssd-secrets reference
        84eca2e81  MAN: Document that it is enough to systemctl restart sssd-kcm.service lately
        f74b97860  SECRETS: Use different option names from secrets and KCM for quota options
        940002ca2  SECRETS: Don't limit the global number of ccaches
        f00db73d7  KCM: Pass confdb context to the ccache db initialization
        f024b5e46  KCM: Configurable quotas for the secdb ccache back end
        247aa4800  TESTS: Add tests for the configurable quotas
        41da9ddfd  Don't qualify users from files domain when default_domain_suffix is set

    Jakub Jelen (1):
        db46cd089  pam_sss: Add missing colon to the PIN prompt

    Lukas Slebodnik (1):
        e1b678c0c  PROXY: Return data in output parameter if everything is OK

    Michal Židek (2):
        39686a584  TESTS: ldb-tools and sssd-tools are required for multihost tests
        b35d88ebf  Update the translations for the 2.2.1 release

    Niranjan M.R (1):
        0b210838e  TESTS: Test kvno correctly displays vesion numbers of principals

    Pavel Březina (11):
        1ea7e7708  ci: disable timeout
        8f22e7952  ci: switch to new tooling and remove 'Read trusted files' stage
        209edb3e1  ci: rebase pull request on the target branch
        230de12b9  ci: print node on which the test is being run
        6815844da  sudo: use proper datetime for default modifyTimestamp value
        b1ea33eca  systemd: add Restart=on-failure to sssd.service
        7b4635c84  man: fix description of dns_resolver_op_timeout
        3807de1d9  man: fix description of dns_resolver_timeout
        99e2a107f  failover: add dns_resolver_server_timeout option
        e97ff0adb  failover: change default timeouts
        049f3906b  config: add dns_resolver_op_timeout to option list

    Sam Morris (1):
        8d64e9f52  build: fix detection of systemd.pc

    Samuel Cabrero (1):
        06479a1d7  nss: Fix command 'endservent' resetting wrong struct member

    Sumit Bose (10):
        e7e212b49  negcache: add fq-usernames of know domains to all UPN neg-caches
        7f0a8f506  p11_child: prefer better digest function if card supports it
        60748f69d  p11_child: fix a memory leak and other memory mangement issues
        e9091aba9  pam: make sure p11_child.log has the right permissions
        8119ee216  ssh: make sure p11_child.log has the right permissions
        9339c445b  BE: make sure child log files have the right permissions
        ba01db0dc  utils: remove unused prototype (cert_to_ssh_key)
        a97ec73e0  utils: move parse_cert_verify_opts() into separate file
        ad9dd137e  p11_child: make OCSP digest configurable
        5574de0f8  pam: fix loop in Smartcard authentication

    Tomas Halman (9):
        01ea70fa8  MAN: ldap_user_home_directory default missing
        2c965b04f  pcre: port to pcre2
        d2adfcf54  CACHE: SSSD doesn't clear cache entries
        2d657dffb  LDAP: failover does not work on non-responsive ldaps
        15cc1e404  CONFDB: Files domain if activated without .conf
        31e08f300  TESTS: adapt tests to enabled default files domain
        5b235bbdb  BE: Introduce flag for be_ptask_create
        1c7521898  BE: Convert be_ptask params to flags
        f2c69a67a  DYNDNS: dyndns_update is not enough

    Yuri Chornoivan (1):
        6925b9cdc  Fix minor typos in docs
