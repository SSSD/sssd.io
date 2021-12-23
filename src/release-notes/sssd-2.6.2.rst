SSSD 2.6.2 Release Notes
========================

Highlights
----------

Important fixes
~~~~~~~~~~~~~~~

* Quick log out and log in did not correctly refresh user's initgroups in `no_session` PAM schema due to lingering systemd processes.

Tickets Fixed
-------------

- `#5744 <https://github.com/SSSD/sssd/issues/5744>`__ - Lookup with fully-qualified name does not work with 'cache_first = True'
- `#5820 <https://github.com/SSSD/sssd/issues/5820>`__ - sssd_be segfault due to empty forest root name
- `#5822 <https://github.com/SSSD/sssd/issues/5822>`__ - Groups are missing while performing id lookup as SSSD switching to offline mode due to the wrong domain name in the ldap-pings(netlogon).
- `#5842 <https://github.com/SSSD/sssd/issues/5842>`__ - [sss_analyze] packaging issues
- `#5873 <https://github.com/SSSD/sssd/issues/5873>`__ - LDAP sp_expire policy does not match other libraries
- `#5875 <https://github.com/SSSD/sssd/issues/5875>`__ - CLDAP ping timeout is too long
- `#5876 <https://github.com/SSSD/sssd/issues/5876>`__ - Covscan failures introduced in 2.6 release (part 1)
- `#5877 <https://github.com/SSSD/sssd/issues/5877>`__ - Covscan failures introduced in 2.6 release (part 2)
- `#5878 <https://github.com/SSSD/sssd/issues/5878>`__ - Covscan failures introduced in 2.6 release (part 3)
- `#5893 <https://github.com/SSSD/sssd/issues/5893>`__ - Passwordless (GSSAPI) SSH not working due to missing "includedir /var/lib/sss/pubconf/krb5.include.d" directive in /etc/krb5.conf
- `#5900 <https://github.com/SSSD/sssd/issues/5900>`__ - pam responder does not call initgroups to refresh the user entry
- `#5911 <https://github.com/SSSD/sssd/issues/5911>`__ - FindByValidCertificate() treats unconfigured CA as "Invalid certificate provided"
- `#5919 <https://github.com/SSSD/sssd/issues/5919>`__ - sssd does not use kerberos port that is set.


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.6.1..2.6.2

    Alexey Tikhonov (8):
        6dae77c8e  Monitor: reduce log severity and add error text in case of fail to read from netlink fd.
        beb5dd52f  SSS_CLIENT: fixed few covscan issues
        5ee8657c3  SPEC: avoid weak dependencies
        d4357235c  P11_CHILD: fix mem leak in case get_preferred_rsa_mechanism() doesn't match anything.
        33ab11103  pot: update pot files
        1f75fbf8a  pot: update pot files
        977d450e6  pot: update pot files
        36ba613a3  Release sssd-2.6.2

    Anuj Borah (2):
        29515aceb  Tests: Podman supports subid ranges managed by FreeIPA
        cde563495  Tests: Fix pytest-alltests-tier1

    Dan Lavu (1):
        c6ad2827b  Adding multidomain test cases for bz2013297 and bz2018432

    David Ward (11):
        886ba4655  p11_child: Fix printing of non-null-terminated strings in wait_for_card()
        e3e274665  p11_child: Include return value of PKCS #11 API calls in debug messages
        d1f0dbf1d  p11_child: Make debug messages about URI matching more specific
        bd8b5260f  p11_child: Perform URI matching inside wait_for_card()
        2bd61f4b9  p11_child: Check if module supports C_WaitForSlotEvent()
        8a4c222b5  p11_child: Allow slot changes to take effect before resuming search
        17ac12908  p11_child: Adjust exit conditions when looping over modules/slots
        33fa634b6  p11_child: Skip uninitialized tokens
        1c24c3eee  p11_child: Combine subsequent loops over certificate list
        4d877816e  p11_child: Filter certificate list in place
        1cc7b8021  p11_child: Handle failure when obtaining module list or names

    Dhairya Parmar (1):
        be6871094  TEST: Lookup with fully-qualified name with 'cache_first = True'

    Iker Pedrosa (8):
        a34e30900  ifp: fix covscan issues
        9c447dc85  usertools: force local user for sssd process user
        3d25724dc  man: sssd.conf and sssd-ifp clarify user option
        2a3035d30  contrib: sssd krb5 configuration snippet
        46843d021  test: fix pep8 complaint
        1e747fad4  krb5: write kdcinfo.* file with port configuration
        8d54b8c02  man: update ifp options for FindByValidCertificate
        fd0f087ad  ifp: improve FindByValidCertificate() error

    Jakub Vavra (1):
        23b9c5e96  Tests: Add test for bz1636002.

    Justin Stephenson (16):
        3ef7952e6  Analyzer: Remove python-click dependency
        e8e7e23af  util: Split chain ID tevent functions
        6f217eac8  RESPONDER: Remove extraneous client ID logging
        9296eaf9a  sbus: Remember outgoing request chain ID
        2b6edf773  RESPONDER: Support chain ID logging
        526f73149  chain_id: Add support for custom debug format
        cb70739f3  krb5_child: Add chain ID logging support
        60712f31f  gpo: Add chain ID logging support
        c92d39a30  ipa_selinux: Add chain ID logging support
        be482ac39  p11_child: Add chain ID logging support
        06d3e79c3  proxy_child: Add chain ID logging support
        1959a2bb4  Analyzer: Parse the responder request ID
        0ba456f9e  Analyzer: Add --child argument to 'request show'
        7825e0d32  Analyzer: Search all responder log files
        9d6270817  Analyzer: Avoid circular import
        1110bd59e  Analyzer: Fail if chain ID support is missing

    Pavel Březina (2):
        a56b8d1aa  utils: ignore systemd and sd-pam process in get_active_uid_linux()
        9acd11771  intg: remove unused is_secrets_socket()

    Scott Poore (1):
        21caecae8  Tests: add docstring in intg/test_infopipe.py

    Shridhar Gadekar (4):
        c6207ead3  Tests: autofs lookups for unknown mounts are delayed for 50s
        2b41ffd44  removed the testcase
        23afbce7b  Verifies: #5832 Bug: https://bugzilla.redhat.com/show_bug.cgi?id=2013218
        b2eb01e54  Tests: Removed secondary group shown in cache

    Stanislav Levin (1):
        ca1d7e291  sss-analyze: Fix self imports

    Steeve Goveas (5):
        a10172a9d  Test: Update marker to tier1_2 for some ad tier1 tests
        94bc8a35a  Test: fix the restore of ldap.conf in test_0016_forceLDAPS
        5615ffa67  TEST: Remove check for rhel 9 to enable CRB repo
        1831c50d6  TESTS: Add tier2 marker for ipa tests
        34ee1b3e7  TEST: Add missing polarion requirements to tests

    Sumit Bose (6):
        b37e2713a  ad: require name when looking up root domain
        4508ef5f7  ad: move current site and forest name to a more global context
        99c416191  ad: use already discovered forest name
        918abaf37  ad: make ad_srv_plugin_ctx_switch_site() public
        724293d08  ad: only send cldap-ping to our local domain
        c0941810f  cldap: use dns_resolver_server_timeout timeout for cldap ping

    Tomas Halman (1):
        54dd529d2  CONFDB: check the return values

    Vincent Vanlaer (1):
        664720355  LDAP: expire accounts when today >= shadowExpire

    Weblate (2):
        662f92963  po: update translations
        d0079cd93  po: update translations
