SSSD 1.15.1 Release Notes
=========================

Highlights
----------

-  Several issues related to starting the SSSD services on-demand via socket activation were fixed. In particular, it is no longer possible to have a service started both by sssd and socket-activated. Another bug which might have caused the responder to start before SSSD started and cause issues especially on system startup was fixed.
-  A new ``files`` provider was added. This provider mirrors the contents of ``/etc/passwd`` and ``/etc/group`` into the SSSD database. The purpose of this new provider is to make it possible to use SSSD's interfaces, such as the D-Bus interface for local users and enable leveraging the in-memory fast cache for local users as well, as a replacement for ``nscd``. In future, we intend to extend the D-Bus interface to also provide setting and retrieving additional custom attributes for the files users.
-  SSSD now autogenerates a fallback configuration that enables the files domain if no SSSD configuration exists. This allows distributions to enable the ``sssd`` service when the SSSD package is installed. Please note that SSSD must be build with the configuration option ``--enable-files-domain`` for this functionality to be enabled.
-  Support for public-key authentication with Kerberos (PKINIT) was added. This support will enable users who authenticate with a Smart Card to obtain a Kerberos ticket during authentication.

Packaging Changes
-----------------

-  The new files provider comes as a new shared library ``libsss_files.so`` and a new manual page
-  A new helper binary called ``sssd_check_socket_activated_responders`` was added. This binary is used in the ``ExecStartPre`` directive to check if the service that corresponds to socket about to be started was also started explicitly and abort the socket startup if it was.

Documentation Changes
---------------------

-  A new PAM module option ``prompt_always`` was added. This option is related to fixing <`https://github.com/SSSD/sssd/issues/4025which <https://github.com/SSSD/sssd/issues/4025which>`_ changed the behaviour of the PAM module so that ``pam_sss`` always uses an auth token that was on stack. The new ``prompt_always`` option makes it possible to restore the previous behaviour.

Tickets Fixed
-------------

-  `#4145 <https://github.com/SSSD/sssd/issues/4145>`_ - When sssd.conf is missing, create one with id_provider=files
-  `#4253 <https://github.com/SSSD/sssd/issues/4253>`_ - Improve successful Dynamic DNS update log messages
-  `#4260 <https://github.com/SSSD/sssd/issues/4260>`_ - sssd doesn't update PTR records if A/PTR zones are configured as non-secure and secure
-  `#4263 <https://github.com/SSSD/sssd/issues/4263>`_ - Use the same logic for matching GC results in initgroups and user lookups
-  `#4293 <https://github.com/SSSD/sssd/issues/4293>`_ - handle default_domain_suffix for ssh requests with default_domain_suffix
-  `#4295 <https://github.com/SSSD/sssd/issues/4295>`_ - Implement a files provider to mirror the contents of /etc/passwd and /etc/groups
-  `#4303 <https://github.com/SSSD/sssd/issues/4303>`_ - [RFE] Add PKINIT support to SSSD Kerberos proivder
-  `#4331 <https://github.com/SSSD/sssd/issues/4331>`_ - Socket activation of SSSD doesn't work and leads to chaos
-  `#4332 <https://github.com/SSSD/sssd/issues/4332>`_ - SSSD does not start if using only the local provider and services line is empty
-  `#4333 <https://github.com/SSSD/sssd/issues/4333>`_ - Avoid running two instances of the same service
-  `#4342 <https://github.com/SSSD/sssd/issues/4342>`_ - Coverity warns about an unused value in IPA sudo code
-  `#4346 <https://github.com/SSSD/sssd/issues/4346>`_ - cache_req should use an negative cache entry for UPN based lookups
-  `#4025 <https://github.com/SSSD/sssd/issues/4025>`_ - Don't prompt for password if there is already one on the stack
-  `#2168 <https://github.com/SSSD/sssd/issues/2168>`_ - Reuse cache_req() in responder code


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_15_0..sssd-1_15_1

    Fabiano Fidêncio (11):
        2ddcd5785  IFP: Update ifp_iface_generated.c
        040ade7b2  MONITOR: Wrap up sending sd_notify "ready" into a new function
        00c0b7bc6  MONITOR: Don't timeout if using local provider + socket-activated responders
        86bcc81a6  MONITOR: Don't return an error in case we fail to register a service
        0adcf95a4  SYSTEMD: Add "After=sssd.service" to the responders' sockets units
        bd5e09bad  SYSTEMD: Avoid starting a responder socket in case SSSD is not started
        9c0c83eec  SYSTEMD: Don't mix up responders' socket and monitor activation
        e0ca21d9f  SYSTEMD: Force responders to refuse manual start
        189db5329  CACHE_REQ: Add cache_req_data_set_bypass_cache()
        ed891c0c5  PAM: Use cache_req to perform initgroups lookups
        5aaaf0817  TESTS: Adapt pam-srv-tests to deal with cache_req related changes

    Jakub Hrozek (42):
        33da7b13e  Updating the version to track the 1.15.1 release
        e947a871f  AD: Use ad_domain to match forest root domain, not the configured domain from sssd.conf
        a5ecc93ab  SUDO: Only store lowercased attribute value once
        99a32e4f5  NEGCACHE: Add API to reset all users and groups
        c3a225d4d  NSS: Add sbus interface to clear memory cache
        2d1a59f6c  UTIL: Add a new domain state called DOM_INCONSISTENT
        c109f063b  RESPONDER: Add a responder sbus interface to set domain state
        205a0b9e9  RESPONDER: A sbus interface to reset negatively cached users and groups
        b3ee4be9e  DP: Add internal DP interface to set domain state
        af28fa659  DP: Add internal interface to reset negative cache from DP
        5007103e8  DP: Add internal interface to invalidate memory cache from DP
        2c61b6eee  RESPONDER: Use the NEED_CHECK_DOMAIN macro
        26866484a  RESPONDER: Include the files provider in NEEDS_CHECK_PROVIDER
        50c740cbc  RESPONDER: Contact inconsistent domains
        8cfb42e19  UTIL: Add a generic inotify module
        90a103d60  CONFDB: Re-enable the files provider
        c71e0a671  FILES: Add the files provider
        c778c36c5  CONFDB: Make pwfield configurable per-domain
        ece2ac688  CONFDB: The files domain defaults to "x" as pwfield
        26577ac05  MAN: Document the pwfield configuration option
        4e17c050d  TESTS: move helper fixtures to back up and restore a file to a utility module
        1921d739f  TESTS: add a helper module with shared NSS constants
        8578fba15  TESTS: Add a module to call nss_sss's getpw* from tests
        3728db53a  TESTS: Add a module to call nss_sss's getgr* from tests
        8bdb8c097  TESTS: Add files provider integration tests
        f9f1310ba  MONITOR: Remove checks for sssd.conf changes
        ee6c7e8b5  MONITOR: Use the common inotify code to watch resolv.conf
        da95ec568  MAN: Add documentation for the files provider
        89e53f713  EXAMPLES: Do not point to id_provider=local
        0e7047c15  SBUS: Document how to free the result of sbus_create_message
        fc91d72f3  FILES: Fix reallocation logic
        1b55ac98d  TESTS: Remove unused import
        eed5bc53a  DOC: Deprecate README, add README.md
        78bb3676f  MONITOR: Enable an implicit files domain if one is not configured
        76b6d7fb9  TESTS: Enable the files domain for all integration tests
        13294bedc  TESTS: Test the files domain autoconfiguration
        5a660d3aa  CONFDB: Refactor reading the config file
        a4837791f  CONFDB: If no configuration file is provided, create a fallback configuration
        8718ff9cc  UTIL: Store UPN suffixes when creating a new subdomain
        afadeb1a5  SYSDB: When searching for UPNs, search either the whole DB or only the given domain
        538321890  CACHE_REQ: Only search the given domain when looking up entries by UPN
        f10ebaa51  Updating translations for the 1.15.1 release

    Justin Stephenson (5):
        1c7f9a676  FAILOVER: Improve port status log messages
        d0aae3c1e  SUDO: Add skip_entry boolean to sudo conversions
        1404f3aa5  TESTS: Add to IPA DN test
        fccd8f9ab  DYNDNS: Update PTR record after non-fatal error
        d694d4fdc  DYNDNS: Correct debug log message of realm

    Lukas Slebodnik (13):
        c369b0621  BUILD: Fix linking of test_wbc_calls
        2e505786d  Suppres implicit-fallthrough from gcc 7
        cbb0e683f  pam_sss: Suppress warning format-truncation
        c587e9ae5  TOOLS: Fix warning format-truncation
        bf0b4eb33  sssctl: Fix warning may be used uninitialized
        cb831fbbc  ldap_child: Fix use after free
        7b4704a10  SYSTEMD: Update journald drop-in file
        c029f707d  Partially revert "CONFIG: Use default config when none provided"
        e5d8b0e10  BUILD: Fix linking of test_sdap_initgr
        bac4458c8  intg: Fix python3 issues
        1f49be442  FILES: Remove unnecessary check
        d7a5943bd  Update link to commit template
        fe079dfc0  Use pagure links as a reference to upstream

    Pavel Březina (17):
        bc898b360  SBUS: remove unused symbols
        a3b2bc382  SBUS: use sss_ptr_hash for opath table
        ea872f140  SBUS: use sss_ptr_hash for nodes table
        b1afef0bc  SBUS: use sss_ptr_hash for signals table
        d8c459fea  ssh: fix number of output certificates
        e33744e8c  ssh: do not create again fq name
        2b5704cd9  sss_parse_inp_send: provide default_domain as parameter
        ddfd1900b  cache_req: add ability to not use default domain suffix
        7723e79f5  cache_req: search user by name with attrs
        9492b3b26  cache_req: add api to create ldb_result from message
        4df7aec64  cache_req: move dp request to plugin
        53c31b83e  cache_req: add host by name search
        a8191ce7a  ssh: rewrite ssh responder to use cache_req
        2ffa245e7  ssh: fix typo
        d9780d286  cache_req: always go to dp first when looking up host
        f2047f6c5  NSS: Rename the interface to invalidate memory cache initgroup records for consistency
        a60e6ec80  CONFDB: The files provider always enumerates

    Petr Čech (5):
        c3593f06d  LDAP: Better logging message
        3ee411625  SYSDB: Removing of sysdb_try_to_find_expected_dn()
        f1e3364a7  TEST: create_multidom_test_ctx() extending
        0b7ded15e  TESTS: Tests for sdap_search_initgr_user_in_batch
        334029028  IPA_SUDO: Unused value fix

    Sumit Bose (17):
        08bf6b4a2  sdap_extend_map: make sure memory can be freed
        454cf0c38  check_duplicate: check name member before using it
        0965a77c4  pam_sss: check conversation callback
        f561c2bd3  PAM: store user object in the preq context
        327a16652  PAM: fix memory leak in pam_sss
        254f3898c  PAM: use sentinel error code in PAM tests
        d47574404  utils: new error codes
        f70d946f8  LDAP/proxy: tell frontend that Smartcard auth is not supported
        dd17a3aad  authtok: enhance support for Smartcard auth blobs
        82c5971fa  PAM: forward Smartcard credentials to backends
        ead25e32c  p11: return name of PKCS#11 module and key id to pam_sss
        52f45837d  pam: enhance Smartcard authentication token
        2d527aab0  KRB5: allow pkinit pre-authentication
        bc0796763  authtok: fix tests on big-endian
        6dd271fdc  pam: use authtok from PAM stack if available
        54039570d  cache_req: use own namespace for UPNs
        c99bcc91e  PAM: Improve debugging on smartcard creds forward
