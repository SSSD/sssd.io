SSSD 2.7.1 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

* Added a new krb5 plugin ``idp`` and a new binary ``oidc_child`` which performs
  **OAuth2** authentication against FreeIPA. This, however, can not be tested
  yet because this feature is still under development on the FreeIPA server
  side. Nevertheless, we have decided to include this in the release in order to
  enable the functionality on the clients immediately when the FreeIPA project
  delivers this feature without the need to update the clients.

General information
~~~~~~~~~~~~~~~~~~~

* SSSD can now handle multi-valued RDNs if a unique name must be determined with the help of the RDN.

Important fixes
~~~~~~~~~~~~~~~

* A regression in ``pam_sss_gss`` module causing a failure if ``KRB5CCNAME`` environment variable was not set was fixed.

Packaging changes
~~~~~~~~~~~~~~~~~

* ``sssd-ipa`` doesn't require ``sssd-idp`` anymore

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* New option ``implicit_pac_responder`` to control if the PAC responder is started for the IPA and AD providers, default is ``true``.
* New option ``krb5_check_pac`` to control the PAC validation behavior.
* multiple ``crl_file`` arguments can be used in the ``certificate_verification`` option.

Tickets Fixed
-------------

- `#4677 <https://github.com/SSSD/sssd/issues/4677>`__ - Add man page for sssd_krb5_localauth_plugin
- `#5134 <https://github.com/SSSD/sssd/issues/5134>`__ - Inefficiency of sdap_nested_group_deref_direct_process()
- `#5868 <https://github.com/SSSD/sssd/issues/5868>`__ - Harden kerberos ticket validation
- `#5961 <https://github.com/SSSD/sssd/issues/5961>`__ - [RFE] Allow SSSD to use anonymous pkinit for FAST
- `#5967 <https://github.com/SSSD/sssd/issues/5967>`__ - [RFE] Implement time logging for the LDAP queries and warning of high queries time
- `#6086 <https://github.com/SSSD/sssd/issues/6086>`__ - [Improvement] add SSSD support for more than one CRL PEM file name with parameters certificate_verification and crl_file
- `#6114 <https://github.com/SSSD/sssd/issues/6114>`__ - sssd runs out of proxy child slots and doesn't clear the counter for Active requests
- `#6122 <https://github.com/SSSD/sssd/issues/6122>`__ - 'getent hosts' not return hosts if they have more than one CN in LDAP
- `#6170 <https://github.com/SSSD/sssd/issues/6170>`__ - Regression "Missing internal domain data." when setting ad_domain to incorrect
- `#6180 <https://github.com/SSSD/sssd/issues/6180>`__ - Regression in pam_sss_gss in handling KRB5CCNAME
- `#6181 <https://github.com/SSSD/sssd/issues/6181>`__ - Add idp authentication indicator in man page of sssd.conf

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.7.0..2.7.1

    Alexey Tikhonov (3):
        e0e23dfbb  SPEC: drop sssd-ipa dependency on sssd-idp
        0ef863f11  sssctl: fixed log message
        64b387159  SDAP: sdap_nested_group_deref_direct_process(): store 'state->members' in a hash table to reduce computational complexity during "new member" check.

    Anonymous (25):
        0eb470f64  po: update translations
        1d4f8a865  po: update translations
        0c617aac7  po: update translations
        0429439e1  po: update translations
        7f137099d  po: update translations
        ce389491e  po: update translations
        4a6a86399  po: update translations
        c6028dc05  po: update translations
        203f53f7f  po: update translations
        bd3af70fe  po: update translations
        4fb521f82  po: update translations
        b7fc2cc7b  po: update translations
        37eeb49cd  po: update translations
        db7330de1  po: update translations
        53285ebd6  po: update translations
        374e46e1f  po: update translations
        c2d6854ac  po: update translations
        7ac8d2e91  po: update translations
        36c4bea4d  po: update translations
        8820b9bf3  po: update translations
        53dc281ff  po: update translations
        b0d968403  po: update translations
        45e0519f0  po: update translations
        30a845f85  po: update translations
        80af4e571  po: update translations

    Anuj Borah (4):
        439b8c3c5  Tests: Fix ns_account test with sleep time
        53ca66388  Tests: Fix sss_analyzer tests
        7edcd1fa5  Tests: Enabling ssctl_ldap test cases
        a86265f75  Tests: Fix ns_account test with clear_sssd_cache

    Elena Mishina (1):
        188d81487  po: update translations

    Göran Uddeborg (1):
        167f87e52  po: update translations

    Iker Pedrosa (4):
        0751f1cf9  CI: update flake8 action reference
        84e3a8d6a  p11_child: enable more than one CRL PEM file
        abac841d5  CI: flake8 move target to pull_request_target
        e7cc73c2c  CI: update actions version

    Luna Jernberg (1):
        2a2c05745  po: update translations

    Madhuri Upadhye (4):
        181070c47  Tests: ipa: Add automation of BZ1859751
        5187a2d5d  Tests: Document: Document to run the tests using multihost config.
        5945dac51  Tests: Document: Setup python virtual environment to run pytest.
        ebda07b9f  Test: ipa: remove useless fixture call

    Pavel Borecki (1):
        0d7db9e8c  po: update translations

    Pavel Březina (13):
        14044af08  ci: switch to write-file-action
        e0c2c0e3f  ci: disable Jenkins jobs
        7d55af151  ci: enable ci for sssd-2-7
        2aeab5062  ci: fix syntax for flake8 job
        74dd00498  ci: enable copr builds for CentOS Stream 8
        af9f390c2  configure: fix libkrad detection
        b92255ee5  cert: fix assignment discards _const_ qualifier from pointer target type
        51600e451  ci: allow deprecated functions during build
        f20db24af  man: add idp indicator
        0eae7db9e  pam_sss_gss: KRB5CCNAME may be NULL
        bd5a48bfb  po: translate sssd_krb5_localauth_plugin.8.xml
        1a2754f81  pot: update translations
        4c02953f9  Release sssd-2.7.1

    Piotr Drąg (1):
        5457584dc  po: update translations

    Shridhar Gadekar (1):
        21052b97a  Tests:port rfc2307 username begin with a space

    Steeve Goveas (7):
        6c0e6fc8e  TEST: Fix docstrings for successful polarion import
        deaca2f54  TEST: Update default debug levels expected in logs
        6e92bb2f3  TEST: Add missing markers in pytest.ini
        0bad124d7  TEST: Implement time logging for the LDAP queries
        eeaa77a27  TEST: Add test for memcache SID
        bc14ede7d  TEST: Update and sort ad pytest.ini
        3dbcb812a  TEST: Install iproute-tc for tc

    Sumit Bose (20):
        bca43389d  spec: mention oidc_child in description
        8547e6995  sdap: move some functions from sysdb to sdap
        75a70ac9c  sdap: rename functions copied from sysdb
        10f86ad3c  sdap: replace sysdb_attrs_primary_name() with sdap_get_primary_name()
        c15318224  sdap: move sysdb_attrs_primary_name() into sdap_get_primary_name()
        19b452015  sdap: make sdap_get_primary_name() aware of multi-valued RDNs
        676b5dce1  sdap: removed unused dom parameter from sdap_get_primary_name()
        26bbaf7f6  sdap: add tests for sdap_get_primary_name
        90617845c  proxy: lower child count even if there is an error
        2e4786e70  proxy: finish request if proxy_child is terminated
        3cb0dda53  data_provider: add dp_client_cancel_timeout()
        7ad0a6d51  proxy: remove DP client timeout handler
        80ffa314c  ad: add fallback in ad_domain_info_send()
        a912c1251  ad: make new PAC buffers available
        d6354e0a9  tests: add PAC upn_dns_info test
        1c90333b0  krb5: add krb5_check_pac option
        8e265c766  pac: apply new pac check options
        e71632735  ad: enable the PAC responder implicitly for AD provider
        fcc1bd84f  monitor: add implicit_pac_responder option.
        0dc42cbaa  localauth: improve localauth add man page

    Tomas Halman (2):
        f42190619  SPEC: python egg info format change
        c90153def  make: clean python new files

    Yuri Chornoivan (1):
        9c93f3922  po: update translations

    김인수 (2):
        2d03e3b12  po: update translations
        ccf55aff0  po: update translations
