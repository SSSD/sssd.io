SSSD 2.0.0 Release Notes
========================

Highlights
----------

This release removes or deprecates functionality from SSSD, therefore the SSSD team decided it was time to bump the major version number. The sssd-1-16 branch will be still supported (most probably even as a LTM branch) so that users who rely on any of the removed features can either migrate or ask for the features to be readded.

Except for the removed features, this release contains a reworked internal IPC and a new default storage back end for the KCM responder.

Platform support removal
~~~~~~~~~~~~~~~~~~~~~~~~

-  Starting with SSSD 2.0, upstream no longer supports RHEL-6 and its derivatives. Users of RHEL-6 are encouraged to stick with the sssd-1-16 branch.

Removed features
~~~~~~~~~~~~~~~~

-  The Python API for managing users and groups in local domains (``id_provider=local``) was removed completely. The interface had been packaged as module called ``pysss.local``
-  The LDAP provider had a special-case branch for evaluating group memberships with the RFC2307bis schema when group nesting was explicitly disabled. This codepath was adding needless additional complexity for little performance gain and was rarely used.
-  The ``ldap_groups_use_matching_rule_in_chain`` and ``ldap_initgroups_use_matching_rule_in_chain`` options and the code that evaluated them was removed. Neither of these options provided a significant performance benefit and the code implementing these options was complex and rarely used.

Deprecated features
~~~~~~~~~~~~~~~~~~~

-  The local provider (``id_provider=local``) and the command line tools to manage users and groups in the local domains, such as ``sss_useradd`` is not built by default anymore. There is a configure-time switch ``--enable-local-domain`` you can use to re-enable the local domain support. However, upstream would like to remove the local domain completely in a future release.
-  The ``sssd_secrets`` responder is not packaged by default. The responder was meant to provide a REST API to access user secrets as well as a proxy to Custodia servers, but as Custodia development all but stopped and the local secrets handling so far didn't gain traction, we decided to not enable this code by default. This also means that the default SSSD configuration no longer requires libcurl and http-parser.

Changed default settings
~~~~~~~~~~~~~~~~~~~~~~~~

-  The ``ldap_sudo_include_regexp`` option changed its default value from ``true`` to ``false``. This means that wild cards in the ``sudoHost`` LDAP attribute are no longer supported by default. The reason we changed the default was that the wildcard was costly to evaluate on the LDAP server side and at the same time rarely used.

New features
~~~~~~~~~~~~

-  The KCM responder has a new back end to store credential caches in a local database. This new back end is enabled by default and actually uses the same storage as the ``sssd-secrets`` responder had used, so the switch from sssd-secrets to this new back end should be completely seamless. The ``sssd-secrets`` socket is no longer required for KCM to operate.
-  The list of PAM services which are allowed to authenticate using a Smart Card is now configurable using a new option ``pam_p11_allowed_services``.

Packaging Changes
-----------------

-  The ``sss_useradd``, ``sss_userdel``, ``sss_usermod``, ``sss_groupadd``, ``sss_groupdel``, ``sss_groupshow`` and ``sss_groupmod`` binaries and their manual pages are no longer packaged by default unless ``--enable-local-provider`` is selected.
-  The sssd_secrets responder is no longer packaged by default unless ``--enable-secrets-responder`` is selected.
-  The new internal IPC mechanism uses several private libraries that need to be packaged - ``libsss_sbus.so``, ``libsss_sbus_sync.so``, ``libsss_iface.so``, ``libsss_iface_sync.so``, ``libifp_iface.so`` and ``libifp_iface_sync.so``
-  The new KCM ccache back end relies on a private library ``libsss_secrets.so`` that must be packaged in case either the KCM responder or the secrets responder are enabled.

Documentation Changes
---------------------

-  The ``ldap_groups_use_matching_rule_in_chain`` and ``ldap_initgroups_use_matching_rule_in_chain`` options were removed.
-  The ``ldap_sudo_include_regexp`` option changed its default value from ``true`` to ``false``.

Known issues
------------

-  <`https://github.com/SSSD/sssd/issues/4802- <https://github.com/SSSD/sssd/issues/4802->`_ The sbus codegen script relies on "python" which might not be available on all distributions

..

-  There is a script that autogenerates code for the internal SSSD IPC. The script happens to call "python" which is not available on all distributions. Patching the ``sbus_generate.sh`` file to call e.g. python3 explicitly works around the issue

..

Tickets Fixed
-------------

-  `#4727 <https://github.com/SSSD/sssd/issues/4727>`_ - Don't package sssd-secrets by default
-  `#4704 <https://github.com/SSSD/sssd/issues/4704>`_ - KCM: Default to a new back end that would write to the secrets database directly
-  `#4556 <https://github.com/SSSD/sssd/issues/4556>`_ - Remove CONFDB_DOMAIN_LEGACY_PASS
-  `#4541 <https://github.com/SSSD/sssd/issues/4541>`_ - Disable host wildcards in sudoHost attribute (ldap_sudo_include_regexp=false)
-  `#4520 <https://github.com/SSSD/sssd/issues/4520>`_ - Remove the special-case for RFC2307bis with zero nesting level
-  `#4519 <https://github.com/SSSD/sssd/issues/4519>`_ - Remove the pysss.local interface
-  `#4518 <https://github.com/SSSD/sssd/issues/4518>`_ - Remove support for ldap_groups_use_matching_rule_in_chain and ldap_initgroups_use_matching_rule_in_chain
-  `#4337 <https://github.com/SSSD/sssd/issues/4337>`_ - Only build the local provider conditionally
-  `#3967 <https://github.com/SSSD/sssd/issues/3967>`_ - Make list of local PAM services allowed for Smartcard authentication configurable


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_16_3..sssd-2_0_0

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

    Jakub Hrozek (57):
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
        6788cd734  Updating translations for the 2.0 release
        38fb7c1ac  Update version for the 2.0 release

    Lukas Slebodnik (6):
        86de91f93  krb5_locator: Make debug function internal
        276f2e345  krb5_locator: Simplify usage of macro PLUGIN_DEBUG
        09dc1d9dc  krb5_locator: Fix typo in debug message
        aefdf7035  krb5_locator: Fix formatting of the variable port
        9680ac9ce  krb5_locator: Use format string checking for debug function
        93caaf294  PAM: Allow to configure pam services for Smartcards

    Pavel Březina (21):
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

    amitkuma (1):
        1adf2f982  confdb: Remove CONFDB_DOMAIN_LEGACY_PASS
