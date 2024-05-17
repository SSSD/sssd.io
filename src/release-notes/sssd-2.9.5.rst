SSSD 2.9.5 Release Notes
========================

Highlights
----------

Security
~~~~~~~~

* Moderate. CVE-2023-3758. Fixed a race condition flaw in GPO policy
  application. `GHSA-7pwr-cfrc-px4f <https://github.com/advisories/GHSA-7pwr-cfrc-px4f>`_

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* Added `failover_primary_timout` configuration option. This can be used to
  configure how often SSSD tries to reconnect to a primary server after a
  successful connection to a backup server. This was previously hardcoded to 31
  seconds which is kept as the default value.

Tickets Fixed
-------------

* `#5708 <https://github.com/SSSD/sssd/issues/5708>`__ - SSSD incorrectly works with AD GPO during user login
* `#7109 <https://github.com/SSSD/sssd/issues/7109>`__ - gdm smartcard login fails with "system error 4" in case of multiple identities
* `#7136 <https://github.com/SSSD/sssd/issues/7136>`__ - Improve documentation for allowing e-mail address as username
* `#7152 <https://github.com/SSSD/sssd/issues/7152>`__ - passkey cannot fall back to password
* `#7173 <https://github.com/SSSD/sssd/issues/7173>`__ - AD users are unable to log in due to case sensitivity of user because the domain is found as an alias to the email address.
* `#7189 <https://github.com/SSSD/sssd/issues/7189>`__ - socket leak
* `#7197 <https://github.com/SSSD/sssd/issues/7197>`__ - Errors in krb5_child.log every time a user authenticates - Pre-authentication failed: No pkinit_anchors supplied
* `#7250 <https://github.com/SSSD/sssd/issues/7250>`__ - SSSD is not fully registering the domains if the cache is empty
* `#7319 <https://github.com/SSSD/sssd/issues/7319>`__ - PAC and PAM responders can crash if backend takes too long time to process getDomains()
* `#7375 <https://github.com/SSSD/sssd/issues/7375>`__ - [RFE] Add option to configure timeout to reconnect to primary servers

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.4..2.9.5

    Abhijit Roy (2):
        c1ba9da77  sssctl: Adding options for nss
        c04165764  sdap_idmap: Enabling further debugging for to understand the underlying reason for Could not convert objectSID.

    Alexey Tikhonov (6):
        e3d0f0d7e  IFP: don't trigger backtrace in case of ACL check fail
        182b6c621  UTILS: inotify: avoid potential NULL deref
        ea2d0aab3  INTG-TESTS: backport `sync_files_provider()` from b9c1d7d667d49080c27641fb4a800bd4c2612d43
        8dcf23f21  DEBUG: reduce log level in case a responder asks for unknown domain
        06e10708d  CI: remove unused stuff (lcov, ...)
        b0fda92e7  RESPONDER: use proper context for getDomains()

    Andre Boscatto (2):
        33bb96fee  man: improving documentation about username and email
        dd0f63246  sssd: adding mail as case insensitive

    Andreas Hasenack (1):
        ed4c9b00a  Fix format string used for time values

    Andreas Schneider (1):
        bca6c4eff  ad_gpo_child: Improve libsmbclient code

    Dan Lavu (4):
        55e641fbb  tests: adding testcase for gh7174 email case insensitivity
        829e868f9  tests: fixing typo in test_authentication.py
        7c57e0f09  tests: audit and rename test cases
        7d260f7d9  tests: adding gpo system tests

    Denis Zlobin (1):
        f3d96061e  sbus: Fix codegen template for async client

    Günther Deschner (1):
        343ff2def  Fix the build with Samba 4.20

    Iker Pedrosa (1):
        10c49b1a5  man: fix default value for pam_passkey_auth

    Jakub Jelen (1):
        70be3583c  doc: Fix configuration option pam_p11_allowed_services type

    Jakub Vavra (14):
        9490f2565  Tests: Add single retry for realm leave
        33cce2910  Tests: Set ciphers for kerberos
        ae2f5e91f  Tests: Add pytest.ini with marker converted to basic suite
        28c41415a  Tests: Fix OsError in test_kcm_debug_level_set
        39ea88c2b  CI: Add sssd testlib to pythonpath for prci multihost
        e1bc03b14  Tests: Tweak per-test log to de-duplicate output
        dd921afa5  Tests: Per-test logging: Fix exception on missing call phase.
        fa7536d18  Tests: Add oddjob package to master for multihost/alltests
        a61cc9c99  Tests: Fix ipa/conftest.py for fedora.
        afe7d8d86  Tests: Fix hostmap tests not to depend on user-nsswitch.conf
        c6dda0ef5  Tests: refactor sssd.conf backup and restore
        9e62e660e  Tests: Fix test_kcm_ssh_login_creates_kerberos_ticket
        b87fe4fb5  Tests: Move polarion.yaml to src/tests/
        c8f783999  Tests: Update reference to polarion.yaml

    Jakub Vávra (9):
        d55bc6f24  Tests: Split package installation transactions and add error logging.
        540bf3932  Tests: Update expect as passwd password change message changed.
        80f87d17c  Tests: Add extra debug to test_0003_gssapi_ssh.
        cc52f6f3c  Tests: Switch test_0001_memcache_sid to reuse adjoin code.
        d17f7ffd8  Tests: Add journalctl when systemctl sssd fails.
        87e3edf22  Tests: Update ad parameters ported for non-root.
        0911ffcd2  Tests: Add extra sssd restart on master for samba tests.
        0deb3f62c  Tests: Add fixing sssd.conf ownership after realm join.
        6afc435ed  Tests: Fix PEP8 on updated AD suites.

    Justin Stephenson (7):
        1c3664d3f  Tests: Python black formatting fixes
        23849f751  krb5: Allow fallback between responder questions
        8d9ae754b  krb5: Add fallback password change support
        6d6bc3c49  krb5: Move soft_terminate_krb5_child to static
        f36ecd2c2  man: Add local_auth_policy table
        b363fa860  passkey: Return error during passkey processing
        f0fba6cd2  passkey: Improve passkey mapping handling

    Madhuri Upadhye (3):
        57a8fffa4  Tests: alltests/test_krb5: Replace files provider
        c9977cafa  Tests: passkey: Add a ssh key as a passkey mapping
        83e2e6be3  Test: Update tc when mapping and key are added

    Patrik Rosecky (1):
        566ebfbb0  tests: multihost/basic/test_kcm converted

    Pavel Březina (8):
        181503747  krb5_child: fix order of calloc arguments
        ee06f2fe6  tests: fix isort, black and mypy errors
        bebb15072  pam: fix invalid #if condition
        786a4ebf0  tests: fix isort issue
        16e4b5d44  tests: use different home dir then /tmp for local user
        14f32f681  failover: add failover_primary_timeout option
        a2fbe0449  tests: remove passkey_requires_root from passkey tests
        595c4c6d2  Release sssd-2.9.5

    Sebastian Andrzej Siewior (1):
        a453f9625  tests: Drop -extensions from openssl command if there is no -x509

    Sumit Bose (15):
        50077c325  pam: fix SC auth with multiple certs and missing login name
        a7621a5b4  sdap: add search_bases option to groups_by_user_send()
        6a8e60df8  sdap: add naming_context as new member of struct sdap_domain
        8bf319242  sss-client: handle key value in destructor
        31ee5eccd  krb5: lower log level in sss_krb5_get_init_creds_password()
        923cb398d  krb5: increase log level in map_krb5_error()
        5b9bc0a1a  krb5: add OTP to krb5 response selection
        c3725a13e  krb5: make sure answer_pkinit() use matching debug messages
        87b54bd84  krb5: make prompter and pre-auth debug message less irritating
        d06b4a3ed  pam_sss: prefer Smartcard authentication
        b6eae6f05  pam: fix storing auth types for offline auth
        5a1e1526e  test: set 'local_auth_policy = only' for all passkey test
        e1bfbc249  ad-gpo: use hash to store intermediate results
        db27a51f2  ad: refresh root domain when read directly
        a2bd43441  oidc_child: fix wrong usage of '%*s'

    Tomasz Kłoczko (1):
        37025a19a  Bump DocBook DTD version to latest stable 4.5

    Weblate (1):
        26c9dc6f3  po: update translations

    dependabot[bot] (4):
        bfcb27275  build(deps): bump actions/download-artifact from 3 to 4
        32390d0bd  build(deps): bump github/codeql-action from 2 to 3
        aa63f7777  build(deps): bump actions/upload-artifact from 3 to 4
        87a46c32d  build(deps): bump DamianReeves/write-file-action from 1.2 to 1.3

    lisa (1):
        2422af6cb  Convert multihost/ad/test_idmap to test_identity

    shridhargadekar (3):
        b1e8c210c  Test: Dropping the assertion of ssh from analyzer list
        631c599b5  Tests: sssctl_analyze diff location
        925cb2a9d  Tests: sudo defaults rule
