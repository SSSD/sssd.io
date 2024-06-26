SSSD 2.10.0-beta2 Release Notes
===============================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* A number of minor glitches of ``sssd-2.10.0-beta1`` around building and packaging were fixed.

Packaging changes
~~~~~~~~~~~~~~~~~

* ``sssd_pam`` binary lost public ``rx`` bits and got ``cap_dac_read_search=p`` file capability to be able to use GSSAPI

Tickets Fixed
-------------

* `#7404 <https://github.com/SSSD/sssd/issues/7404>`__ - CRL option soft_crl doesn't check CRL at all, if nextupdate date has passed
* `#7411 <https://github.com/SSSD/sssd/issues/7411>`__ - GPO application fails with more > 1host in security filter
* `#7449 <https://github.com/SSSD/sssd/issues/7449>`__ - Man pages broken
* `#7451 <https://github.com/SSSD/sssd/issues/7451>`__ - sssd is skipping GPO evaluation with auto_private_groups

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.9.0..2.10.0-beta1

    Alejandro López (2):
        77f224674  MAN PAGES: Fix broken man pages
        3d1bf5d89  SSH: Remove two unused configuration options

    Alexey Tikhonov (4):
        1812aaf7b  SPEC: strip public rx bits from 'proxy_child'
        fc5c1a1af  UTILS: reduce log level if `sss_krb5_touch_config()` fails
        58da100df  ENUMERATION: enable support for 'proxy' provider
        0562646cc  PAM: grant 'cap_dac_read_search=p' to sssd_pam

    Christopher Byrne (2):
        4e345cc4c  initscripts: Allow Gentoo initscripts to work with sssd user
        fce2d97df  BUILD: Wire up sysusers, udev and tmpfiles config for optional install

    Dan Lavu (1):
        f9c0c6d8d  tests: adding proper requirement for sss_ssh_knownhosts

    Daniel Bershatsky (1):
        9fe254f46  SSS_CLIENT: Follow API changes in libsubid

    Iker Pedrosa (1):
        bb72b53d3  spec: change passkey_child owner

    Jakub Vávra (7):
        60fa73053  Tests: Update code handling journald.conf
        9f7916129  tests: Drop already ported tests from alltest
        f37aa4669  tests: Add loading kernel module sch_netem for tc tool
        48e681215  tests: Drop test_bz1221992 that is invalid on RHEL 10
        49904292d  test: Do not overwrite /etc/nsswitch.conf by authselect
        27995f5d6  Tests: Drop tests converted to system from basic to save resources in prci
        7e5477706  Tests: Handle missing ldap_child.log in AD parameters

    Justin Stephenson (1):
        4d5177404  configure: use RUNDIR macro for config_pidpath

    Madhuri Upadhye (2):
        4e0b648d1  Test: Check the TGT of user after auth for passkey
        3bac8c9cc  Test: Passkey test cases

    Pavel Březina (7):
        eadb87267  version: replace dash with tilda
        fad092b08  ci deps: do not use -- to denote positional arguments anymore
        9f363f86b  ci: do not collect pytest-mh logs in separate file
        b7a47ffa5  ci: disable show-capture in system tests
        6de89309d  pot: update pot files
        28239d6c9  scripts: switch back to dash for pre-releases
        b44cb5766  Release sssd-2.10.0-beta2

    Sumit Bose (5):
        b25e510ad  ad: use right memory context in GPO code
        48c0607b4  configure: use prefix for systemd paths if needed
        12150fcbb  configure: user ${datadir} in polkitdir
        986bb7262  sysdb: do not fail to add non-posix user to MPG domain
        4dc966228  p11_child: enhance 'soft_crl' option

    Weblate (1):
        786844730  po: update translations

    aborah (4):
        0d60e3dc0  Tests: Fix RHEL10 failures
        815d89f86  Tests: Fix ipa tests for RHEL10
        15fe8a11d  Tests: Fix RHEL9.5 issue
        f7c53d1ff  Tests: Fix tier1_2 tests for rhel10

    shridhargadekar (1):
        5ed2e37c2  Tests: automount segfault fix
