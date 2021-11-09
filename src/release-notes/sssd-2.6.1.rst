SSSD 2.6.1 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

* New infopipe method ``FindByValidCertificate()`` which accepts the certificate as input, validates it against configured CAs, and outputs the user path on success. This is similar to the existing ``FindByCertificate()``, but that does not do any trust validation.

Packaging changes
~~~~~~~~~~~~~~~~~

* ``subid ranges`` support was enabled by default.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* Default value of ``ssh_hash_known_hosts`` setting was changed to false for the sake of consistency with OpenSSH that does not hash host names by default.

Tickets Fixed
-------------

- `#5224 <https://github.com/SSSD/sssd/issues/5224>`__ - Add client certificate validation D-Bus API
- `#5528 <https://github.com/SSSD/sssd/issues/5528>`__ - SSSD  not detecting subdomain from AD forest (RHEL 8.3)
- `#5672 <https://github.com/SSSD/sssd/issues/5672>`__ - Auth failures because of System Error
- `#5781 <https://github.com/SSSD/sssd/issues/5781>`__ - socket-activated services start as the sssd user and then are unable to read the confdb
- `#5783 <https://github.com/SSSD/sssd/issues/5783>`__ - proxy provider: secondary group is showing in sssd cache after group is removed
- `#5819 <https://github.com/SSSD/sssd/issues/5819>`__ - After sssd update to 1.16.5-10.el7_9.8.x86_64 the customer is facing slow connection/authentication (due to discovery of unexpected AD domains)
- `#5832 <https://github.com/SSSD/sssd/issues/5832>`__ - autofs lookups for unknown mounts are delayed for 50s
- `#5839 <https://github.com/SSSD/sssd/issues/5839>`__ - "Unable to obtain cached rules" filling up sssd_sudo.log
- `#5846 <https://github.com/SSSD/sssd/issues/5846>`__ - offline authentication and desktop profiles
- `#5848 <https://github.com/SSSD/sssd/issues/5848>`__ - Consistency in defaults between OpenSSH and SSSD
- `#5854 <https://github.com/SSSD/sssd/issues/5854>`__ - Add support for CKM_RSA_PKCS in smart card authentication.


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.6.0..2.6.1

    Alexey Tikhonov (17):
        625274738  DEBUG: fix missing "va_end"
        766fe6235  GPO: fixed compilation warning
        84a4230b1  KCM: fixed uninitialized value
        de6eba31e  Removed excessive includes around 'strtonum'
        a2cc7daef  'strtonum' helpers: usage sanitization
        3c17a57e7  'strto*()': usage sanitization
        a664e9ce0  TESTS: fixed a bug in define->string conversion
        86413e5f0  SUDO: decrease log level in case object wasn't found
        7cba8ed6a  KCM: delete malformed 'cn=default' entries
        e8b43cc82  SSH: changed default value of `ssh_hash_known_hosts` to false
        b30861d86  SPEC: enabled build of 'subid ranges' support
        d469a8105  SPEC: disable running files provider by default
        7121e56d7  INTG-TESTS: enable build of 'subid ranges' support
        bb8da4303  DEBUG: avoid backtrace dups.
        bd9038657  P11: refactoring of get_preferred_rsa_mechanism()
        71b6d548c  P11: add support of 'CKM_RSA_PKCS' mechanism
        b5073394d  TESTS: added two tests to check cert auth with specific RSA mechanisms: CKM_RSA_PKCS and CKM_SHA384_RSA_PKCS. (CKM_SHA384_RSA_PKCS is arbitrary chosen as one of CKM_SHA*_RSA_PKCS family)

    Anuj Borah (2):
        305120b9a  Tests: Regression 8.5 - sssd-ipa
        48234ed8e  Tests: sss_override does not take precedence over override_homedir directive

    Fernando Apesteguia (1):
        4292f9fdd  Fix untranslated string

    Iker Pedrosa (3):
        301659a66  proxy: allow removing group members
        cf75d897b  ifp: new interface to validate a certificate
        50e6070e4  Tests: ifp interface to validate certificate

    Justin Stephenson (2):
        60353300d  Tests: Fix warning about deprecated res_randomid()
        232ba7f0d  DP: Resolve intermediate groups prior to SR overlay

    Pavel Březina (4):
        bb94a18f0  cache_req: return success for autofs when ENOENT is returned from provider
        8db2485cd  sbus: maintain correct refcount before sending a reply
        19a902a16  pot: update pot files
        02183611c  Release sssd-2.6.1

    Shridhar Gadekar (1):
        bd521abe2  Tests: pam_sss_gss.so doesn't work with large kerberos tickets #5815

    Stanislav Levin (1):
        7bfdd3db8  pam_sss: Allow offline authentication against non-ipa-desktopprofiles aware DC

    Sumit Bose (1):
        4c48c4a77  ad: filter trusted domains

    Tomas Halman (2):
        92e167994  CONFDB: Change ownership of config.ldb
        7db6cfd06  CONFDB: Change ownership before dropping privileges

    Weblate (1):
        8406af355  po: update translations
