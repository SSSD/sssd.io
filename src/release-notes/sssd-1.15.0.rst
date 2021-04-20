SSSD 1.15.0 Release Notes
=========================

Highlights
----------

-  SSSD now allows the responders to be activated by the systemd service manager and exit when idle. This means the ``services`` line in sssd.conf is optional and the responders can be started on-demand, simplifying the sssd configuration. Please note that this change is backwards-compatible and the responders listed explicitly in sssd.conf's services line are managed by sssd in the same manner as in previous releases. Please refer to ``man sssd.conf(5)`` for more information
-  The sudo provider is no longer disabled for configurations that do not explicitly include the ``sudo`` responder in the ``services`` list. In order to disable the sudo-related back end code that executes the periodic LDAP queries, set the ``sudo_provider`` to ``none`` explicitly
-  The watchdog signal handler no longer uses signal-unsafe functions. This bug was causing a deadlock in case the watchdog was about to kill a stuck process
-  A bug that prevented TLS to be set up correctly on systems where libldap links with GnuTLS was fixed
-  The functionality to alter SSSD configuration through the D-Bus interface provided by the IFP responder was removed. This functionality was not used to the best of our knowledge, had no tests and prevented the InfoPipe responder from running as a non-privileged user.
-  A bug that prevented statically-linked applications from using libnss_sss was fixed by removing dependency on ``-lpthreads`` from the ``libnss_sss`` library (please see <`https://sourceware.org/bugzilla/show_bug.cgi?id=20500for <https://sourceware.org/bugzilla/show_bug.cgi?id=20500for>`_ an example on why linking with ``-lpthread`` from an NSS modules is problematic)
-  Previously, SSSD did not ignore GPOs that were missing the gPCFunctionalityVersion attribute and failed the whole GPO processing. Starting with this version, the GPOs without the gPCFunctionalityVersion are skipped.

Packaging Changes
-----------------

-  The Augeas development libraries are no longer required since the configuration manipulation interface was dropped from the InfoPipe responder
-  The libsss_config.so internal library was removed as well due to removal of the InfoPipe config management
-  In order to manage socket-activated or bus activated responders, each responder is now represented by a systemd service file (e.g. sssd-nss.service). All responders except InfoPipe, which is bus-activated, are also managed by a socket unit file (e.g. sssd-nss.socket)

Documentation Changes
---------------------

-  The sssd-secrets responder gained a new option max_payload_size that allows the administrator to limit the maximum size of a secret
-  A new option responder_idle_timeout was added to support idle termination of socket-activated responders
-  The sssd-ad and sssd-ipa man pages now summarize differences between the generic Kerberos/LDAP back end and the specialized IPA/AD back ends

Tickets Fixed
-------------

-  `#1739 <https://github.com/SSSD/sssd/issues/1739>`_ - Use command line arguments instead env vars for krb5_child
-  `#1243 <https://github.com/SSSD/sssd/issues/1243>`_ - Man pages do not specify that sssd dyndns_refresh_interval < 60 is pulled to 60 seconds
-  `#1285 <https://github.com/SSSD/sssd/issues/1285>`_ - [RFE] Socket-activate responders
-  `#1559 <https://github.com/SSSD/sssd/issues/1559>`_ - krb5_child: Remove getenv() ran as root
-  `#3060 <https://github.com/SSSD/sssd/issues/4093>`_ - better debugging of timestamp cache modifications
-  `#1171 <https://github.com/SSSD/sssd/issues/1171>`_ - [RFE] socket-activate the IFP responder
-  `#1193 <https://github.com/SSSD/sssd/issues/1193>`_ - cache_req: complete the needs of NSS responders
-  `#1198 <https://github.com/SSSD/sssd/issues/1198>`_ - nss_sss might leak memory when calling thread goes away
-  `#1256 <https://github.com/SSSD/sssd/issues/1256>`_ - Update man pages for any AD provider config options that differ from ldap/krb5 providers defaults
-  `#1257 <https://github.com/SSSD/sssd/issues/1257>`_ - Review and update SSSD's wiki pages for 1.15 Alpha release
-  `#1277 <https://github.com/SSSD/sssd/issues/1277>`_ - SSSCTL should not be case sensitive when searching for usernames or groups in a case-insensitive domain
-  `#1287 <https://github.com/SSSD/sssd/issues/1287>`_ - [RFE] Shutdown timeout for {socket,bus}-activated responders
-  `#1317 <https://github.com/SSSD/sssd/issues/1317>`_ - Unchecked return value of sss_cmd_empty_packet(pctx->creq->out);
-  `#1325 <https://github.com/SSSD/sssd/issues/1325>`_ - getsidbyid can fail in some cases due to cache_req refactoring
-  `#1326 <https://github.com/SSSD/sssd/issues/1326>`_ - getsidbyname does not work properly with case insensitive domains


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_14_2..sssd-1_15_0

    Amith Kumar (1):
        dfbbe39f4  MAN: Updation of sssd-ad man page for case when dyndns_refresh_interval < 60 seconds

    Carl Henrik Lunde (1):
        9676b464d  Prevent use after free in fd_input_available

    David Michael (1):
        baadb6080  BUILD: Find a host-prefixed krb5-config when cross-compiling

    Fabiano Fidêncio (34):
        da8801c36  SECRETS: Fix secrets rule in the allowed sections
        682c9c346  SECRETS: Add allowed_sec_users_options
        9ba53ac52  SECRETS: Delete all secrets stored during "max_secrets" test
        7171a7584  SECRETS: Add configurable payload size limit of a secret
        99b2352f9  BUILD: Drop libsss_config
        78b4b7e5e  IFP: Remove "ChangeDebugTemporarily" method
        51ce94d00  AUTOFS: Check return of sss_cmd_empty_packet()
        a290ab27e  SUDO: Drop logic to disable the backend in case the provider is not set
        953236782  MONITOR: Expose the monitor's services type
        eaff953c6  MONITOR: Pass the service type to the RegisterService method
        41e9e8b60  UTIL: Introduce --socket-activated cmdline option for responders
        9e59f73f8  UTIL: Introduce --dbus-activated cmd option for responders
        b1829f05c  RESPONDER: Make responders' common code ready for socket activation
        61cd5c830  AUTOFS: Make AutoFS responder socket-activatable
        40e9ad2bf  NSS: Make NSS responder socket-activatable
        e40936053  PAC: Make PAC responder socket-activatable
        6a7e28f06  PAM: Make PAM responder socket-activatable
        b33c275eb  SSH: Make SSH responder socket-activatable
        f37e795cd  SUDO: Make Sudo responder socket-activatable
        9222a4fcb  IFP: Make IFP responder dbus-activatable
        9b3cd1171  MONITOR: Split up check_services()
        2c9040b98  MONITOR: Deal with no services set up
        006ba8944  MONITOR: Deal with socket-activated responders
        9cd29d64f  MAN: Mention that the services' list is optional
        2797aca4d  MAN: "user" doesn't work with socket-activated services
        26f11a75d  MONITOR: Don't expose monitor_common_send_id()
        b46c4c0d3  SBUS: Add a time_t pointer to the sbus_connection
        7622d9d97  SBUS: Add destructor data to sbus_connection
        386c7340d  RESPONDER: Make clear {reset_,}idle_timer() are related to client
        32c766422  RESPONDER: Don't expose client_idle_handler()
        151a6de47  RESPONDER: Shutdown {dbus,socket}-activated responders in case they're idle
        560daa14e  RESPONDER: Change how client timeout is calculated
        087162b85  SERVER: Set the process group during server_setup()
        e6a5f8c58  WATCHDOG: Avoid non async-signal-safe from the signal_handler

    Howard Guo (1):
        d2f935426  sss_client: Defer thread cancellation until completion of nss/pam operations

    Jakub Hrozek (18):
        ae30cff21  Updating the version for the 1.14.3 development
        ef390162e  Updating the version to track sssd-1-15 development
        e5a984093  SYSDB: Split sysdb_try_to_find_expected_dn() into smaller functions
        24d8c85fa  SYSDB: Augment sysdb_try_to_find_expected_dn to match search base as well
        fbe6644aa  MONITOR: Do not set up watchdog for monitor
        ab792150c  MONITOR: Remove deprecated pong sbus method
        fd25e6844  MONITOR: Remove unused shutDown sbus method
        538a7f1dd  Qualify ghost user attribute in case ldap_group_nesting_level is set to 0
        65e791f84  tests: Add a test for group resolution with ldap_group_nesting_level=0
        2927dc45b  BUILD: Fix a typo in inotify.m4
        ed71fba97  SSH: Use default_domain_suffix for users' authorized keys
        ee576602d  SYSDB: Suppress sysdb_delete_ts_entry failed: 0
        150a0cc8f  STAP: Only print transaction statistics if the script caught some transactions
        1a71eeb4d  test_sssctl: Add an integration test for sssctl netgroup-show
        b4dd0867c  KRB5: Advise the user to inspect the krb5_child.log if the child fails with a System Error
        9e74a7ce9  IFP: Fix GetUserAttr
        36b56482c  Updating the translations for the 1.15.0 release
        885a47df0  Updating the version for the 1.15.0 release

    Justin Stephenson (2):
        6e27e8572  MAN: Document different defaults for AD provider
        8caf7ba50  MAN: Document different defaults for IPA provider

    Lukas Slebodnik (45):
        8f1316a0c  crypto: Port libcrypto code to openssl-1.1
        4117ae323  BUILD: Fix build without samba
        0c2be9700  libcrypto: Check right value of CRYPTO_memcmp
        65c85654d  crypto-tests: Add unit test for sss_encrypt + sss_decrypt
        96d239e83  crypto-tests: Rename encrypt decrypt test case
        11d2a1183  BUILD: Accept krb5 1.15 for building the PAC plugin
        bacc66dc6  dlopen-test: Use portable macro for location of .libs
        558b8f3cd  dlopen-test: Add missing libraries to the check list
        d708e53d0  dlopen-test: Move libraries to the right "sections"
        c7b3c43cf  dlopen-test: Add check for untested libraries
        6d11fdcd8  BUILD: Fix linking with librt
        a7f085d6a  KRB5: Remove spurious warning in logs
        900778b5a  TESTS: Check new line at end of file
        58aa8d645  UTIL: Fix implicit declaration of function 'htobe32'
        52cdb4275  SYSDB: Remove unused prototype from header file
        73c9330fa  sssctl: Fix missing declaration
        c101cb130  UTIL: Fix compilation of sss_utf8 with libunistring
        13b1d270f  CONFDB: Supress clang false passitive warnings
        8618716d6  SIFP: Fix warning format-security
        3d5bf48ac  RESPONDER: Remove dead assignment to the variable ret
        69fb159e1  Fix compilation with python3.6
        929bb1170  intg: Generate tmp dir with lowercase
        64344539b  LDAP: Fix debug messages after errors in *_get_send
        2df7a1fe4  LDAP: Removed unused attr_type from users_get_send
        823d8292c  LDAP: Remove unused parameter attr_type from groups_get_send
        8b026b55f  DP: Remove unused constants BE_ATTR_*
        ca68b1b4b  DP: Remove unused attr_type from struct dp_id_data
        3f2f973fa  LDAP: Remove attrs_type related TODO comments
        adc5f0d9d  sssd_ldb.py: Remove a leftover debug message
        c46dec3df  intg: Fix python2,3 urllib
        1fef02f87  intg: Avoid using xrange in tests
        00fc94cbe  intg: Avoid using iteritems for dictionary
        e1711a2b2  intg: Use bytes with hash function
        73c9e3d71  intg: Fix creating of slapd configuration
        1097a61a8  intg: Use bytes for value of attributes in ldif
        19398379a  intg: Use bytes as input in ctypes
        fd2dfed53  intg: Return strings from ctypes wrappers
        69f6b919b  intg: Convert output of executed commands to strings
        554734a20  intg: Return list for enumeration functions
        2a2014d70  SYSDB: Update filter for get object by id
        126698070  sysdb-tests: Add test for sysdb_search_object_by_id
        8a4a2b87f  sysdb: Search also aliases in sysdb_search_object_by_name
        daf3714bd  sysdb-tests: Add test for sysdb_search_object_by_name
        9657c178f  MONITOR: Fix warning with undefined macro HAVE_SYSTEMD
        31459a014  UTIL: Unset O_NONBLOCK for ldap connection

    Michal Židek (9):
        cbee11e91  sssctl: Flags for command initialization
        ff565da10  ipa: Nested netgroups do not work
        867bb85ec  common: Fix domain case sensitivity init
        d6e875c49  sssctl: Search by alias
        715abb607  sssctl: Case insensitive filters
        35ecfab87  tests: sssctl user/group-show basic tests
        1af143e25  MAN: sssctl debug level
        6a490b312  GPO: Skip GPOs without gPCFunctionalityVersion
        47680083e  gpo: Improve debug messages

    Mike Ely (1):
        cf5357ae8  ad_access_filter search for nested groups

    Pavel Březina (41):
        274996466  cache_req: move from switch to plugins; add logic
        0db2f3402  cache_req: move from switch to plugins, add plugins
        4169fb26e  cache_req: switch to new code
        e083a6bcf  cache_req: delete old code
        46703740e  sudo: do not store usn if no rules are found
        a22b0af19  nss: move nss_ctx->global_names to rctx
        1d5e69346  ifp: remove unused fields from state
        e4b147ed0  setent_notify: remove unused private context
        35d161765  sss_crypto.h: include required headers
        7b293a509  sss_output_name: do not require fq name
        39b4feb50  cache_req: fix initgroups by name
        f63607bfc  cache_req: skip first search on bypass cache
        b206e1abb  cache_req: encapsulate output data into structure
        3df5c41c1  cache_req: add ability to gather result from all domains
        9c98397b6  cache_req: add ability to filter domains by enumeration
        a79acee18  cache_req: add user enumeration
        12d771585  cache_req: add group enumeration
        2e13817e6  cache_req: add support for service by name
        c2fc9459c  cache_req: add support for service by port
        0ae7e46a3  cache_req: add support for services enumeration
        6b159f14f  cache_req: add support for netgroups
        4e2c15e6b  cache_req: allow shallow copy of result
        7be55c7de  cache_req: allow to return well known object as result
        7a2ca8d77  cache_req: return well known objects in object by sid
        1b33f4d5c  cache_req: make sure that we always fetch default attrs
        c85f75189  cache_req: allow upn search with attrs
        488518dde  cache_req: add object by name
        3be2628d8  cache_req: add object by id
        8f895983e  cache_req: make plug-ins definition const
        817e3ec31  cache_req: improve debugging
        bad19f954  cache_req: fix plugin function description
        122228f49  cache_req: allow to search subdomains without fqn
        2d12aae08  cache_req: do not set ncache if dp request fails
        0713b92ec  responders: unify usage of sss_cmd_send_empty and _error
        87d85db07  responders: remove checks that are handled inside cache_req
        7162dc780  responders: do not try to contact DP with LOCAL provider
        a5a3bbb0b  utils: add sss_ptr_hash module
        4049b63f8  nss: rewrite nss responder so it uses cache_req
        8d5292227  nss: make nss responder tests work with new code
        075d89886  nss: remove the old code
        ca367e0cb  dp_request_table: remove unused #includes

    Petr Cech (2):
        cb056fe82  SYSDB: Adding message to inform which cache is used
        0be56bb4a  SYSDB: Adding message about reason why cache changed

    Petr Čech (5):
        f4a1046bb  SYSDB: Adding lowercase sudoUser form
        23637e2fd  TESTS: Extending sysdb sudo store tests
        8c256b670  RESPONDER: Adding of return value checking
        e16b3174e  UTIL: Removing of never read value
        7e23edbaa  SYSDB: Fixing of sudorule without a sudoUser

    Sorah Fukumori (1):
        13adcd070  BUILD: Fix installation without samba

    Sumit Bose (11):
        3dd4c3eca  sysdb: add parent_dom to sysdb_get_direct_parents()
        49d3f0a48  sdap: make some nested group related calls public
        25699846b  LDAP/AD: resolve domain local groups for remote users
        c8fe1d922  PAM: add a test for filter_responses()
        ce43f710c  PAM: add pam_response_filter option
        ea11ed3ea  IPA/AD: check auth ctx before using it
        7e394400e  krb5: Use command line arguments instead env vars for krb5_child
        f78b2dd73  krb5: fix two memory leaks
        167b05b28  krb5: add tests for common functions
        50a6d0118  sss_ptr_hash_delete_all: use unsigned long int
        0b78b4e32  libwbclient-sssd: wbcLookupSid() allow NULL arguments

    Victor Tapia (1):
        d4063e9a2  MONITOR: Create pidfile after responders started
