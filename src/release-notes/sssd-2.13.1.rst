SSSD 2.13.1 Release Notes
=========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

- Support of Python2 is deprecated and will be dropped in a future release.
- Support of OpenSSL < 3.0.8 is deprecated and will be dropped in a future release.

New features
~~~~~~~~~~~~

- New ``oidc_child`` option ``--client-auth-method`` to select between authentication
  with client secret, mutual-TLS/mTLS (RFC 8705) and JWT client assertion
  (RFC 7523). For mTLS all key types supported by libcurl can be used. For JWT
  RS256, ES256, ES384 and ES512 with matching key types are supported.
- New ``oidc_child`` option ``--pkcs12-client-creds`` to specify the path to a PKCS#12
  file with certificate and private key for certificate based authentication.
  Password to unlock the private key can be given with ``--client-secret`` or
  ``--client-secret-stdin`` options.

Important fixes
~~~~~~~~~~~~~~~

- Fixed an issue where SSSD fails to start when DNS is unresponsive.
- SSSD no longer crashes if ``ldap_read_rootdse = never`` and
  ``enumerate = true``

Tickets Fixed
-------------

* `#5371 <https://github.com/SSSD/sssd/issues/5371>`__ - Pinpad card reader for login authentication yet you are asked also enter pin on pc keyboard
* `#7289 <https://github.com/SSSD/sssd/issues/7289>`__ - [rule/allows_nss_options]: Attribute 'offline_timeout_random_offset' is not allowed in section 'nss'. Check for typos
* `#7341 <https://github.com/SSSD/sssd/issues/7341>`__ - sssd.conf(5): override_gid: "Override the primary GID value with the one specified." Ambiguous wording, no mention of default
* `#8718 <https://github.com/SSSD/sssd/issues/8718>`__ - 'sssctl analyze --help' shows incorrect command 'sss_analyze' in usage field

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.13.0..2.13.1

    Akshay Sakure (3):
        b292c6ddb  Component: sssd-tools
        7b9e0059a  sssd man-page: Improve man-page for override_gid
        b388d22db  sssd man-page: Fix man-page for offline_timeout*

    Alexey Tikhonov (4):
        6e2b87aa4  KRB5: read keytab copy in offline mode too
        fa138120c  sdap: defer libldap global options setup to first connection
        7682b02e3  Makefile: krb5 plugins: don't export internal symbols
        9a3938fc5  RESOLV: handle empty addr list properly

    Dan Lavu (1):
        d19f6860e  refactoring ipa tests for hostname framework changes.

    Iker Pedrosa (2):
        1b6efb03f  tests: add TMT plan for passkey testing
        f21a1432f  ci: add TMT passkey tests to packit workflow

    Jakub Vávra (2):
        a4bbfb40b  Tests: Fix test_refresh_contain_timestamp
        e08f1bd13  Tests: Update LdapOperations to fail on bind immediately

    Justin Stephenson (1):
        eecbb52ab  tests: Clarify approx match filter

    Madhuri Upadhye (1):
        d77df8e58  tests: poll for KCM TGT renewal instead of fixed sleep

    Pavel Březina (2):
        c3acaa3a5  sdap: let callers mark SSSD as offline if kinit fails
        0ab98c7b3  sdap: handle missing rootDSE gracefully

    Samuel Cabrero (1):
        9826dca05  sdap: Reduce log level when get_naming_context() fails

    Simo Sorce (3):
        e12ff3c62  Correct x400Address type check in crypto.m4
        e30bd32e9  Update certmap for OpenSSL 4.0 compatibility
        52547f7f9  Add const qualifier to X509_NAME pointers

    Sumit Bose (13):
        67444c41f  p11_child: ignore failure of C_GetTokenInfo
        cd1849205  pam: handle protected authentication path
        89accfc15  authtok: remove sss_authtok_set_sc_keypad()
        072f8ec11  pam_sss: fix potential memory leak
        8c59fa3e6  pam: refactor pack_cert_data
        22ee18410  krb5: restart krb5_child for Smartcard authentication
        adf76523c  crypto: add get_jwk_from_pkcs12()
        d50a06969  oidc_child: add pkcs12-client-creds option
        7b51a9ba6  oidc_child: add JWT authentication
        d217bba46  test: add tests for oidc_child 'get-device-code'
        04f661d6e  oidc_child: remove potential double-free in JSON code
        28ca8cc28  oisc_child: add missing NULL checks
        cd3809bd1  oidc_child: clarify why a value isn't copied

    aborah-sudo (2):
        1c764c59b  Tests: fix the tests to check the new pattern
        12d538c42  Tests: Disable test_authentication_indicators

    dependabot[bot] (2):
        87b819c73  ci: bump cross-platform-actions/action from 0.32.0 to 1.0.0
        004a8be12  ci: bump cross-platform-actions/action from 1.0.0 to 1.2.0

    kkz (1):
        cb1bdedaa  resolv: Fix incorrect variable used in ares_parse_txt_reply() error check

    krishnavema (1):
        feef76172  tests: implement multi-token support for smart card authentication

    sssd-bot (4):
        92172fc3a  pot: update pot files
        57209f99c  Release sssd-2.13.1
        b9154c27b  pot: update pot files
        711680648  Release sssd-2.13.1

