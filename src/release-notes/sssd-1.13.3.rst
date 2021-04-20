SSSD 1.13.3 Release Notes
=========================

Highlights
----------

-  A bug that prevented user lookups and logins after migration from winsync to IPA-AD trusts was fixed
-  The OCSP certificate validation checks are enabled for smartcard logins if SSSD was compiled with the NSS crypto library.
-  A bug that prevented the ``ignore_group_members`` option from working correctly in AD provider setups that use a dedicated primary group (as opposed to a user-private group) was fixed
-  Offline detection and offline login timeouts were improved for AD users logging in from a domain trusted by an IPA server
-  The AD provider supports setting up ``autofs_provider=ad``
-  Several usability improvements to our debug messages

Packaging Changes
-----------------

-  The ``p11_child`` helper binary is able to run completely unprivileged and no longer requires the setgid bit to be set

Documentation Changes
---------------------

-  A new option ``certificate_verification`` was added. This option allows the administrator to disable OCSP checks in case the OCSP server is not reachable

Tickets Fixed
-------------

-  `#2674 <https://github.com/SSSD/sssd/issues/2674>`_ [RFE] Unable to use AD provider for automount lookups
-  `#2985 <https://github.com/SSSD/sssd/issues/2985>`_ convert sudo timer to be_ptask
-  `#3713 <https://github.com/SSSD/sssd/issues/3713>`_ sudo: reload hostinfo when going online
-  `#3773 <https://github.com/SSSD/sssd/issues/3773>`_ Add Integration tests for local views feature
-  `#3788 <https://github.com/SSSD/sssd/issues/3788>`_ get_object_from_cache() does not handle services
-  `#3796 <https://github.com/SSSD/sssd/issues/3796>`_ Review p11_child hardening
-  `#3828 <https://github.com/SSSD/sssd/issues/3828>`_ We should mention SSS_NSS_USE_MEMCACHE in man sssd.conf(5) as well
-  `#3837 <https://github.com/SSSD/sssd/issues/3837>`_ fix man page for sssd-ldap
-  `#3842 <https://github.com/SSSD/sssd/issues/3842>`_ Check next certificate on smart card if first is not valid
-  `#3853 <https://github.com/SSSD/sssd/issues/3853>`_ Smartcard login when certificate on the card is revoked and ocsp check enabled is not supported
-  `#3871 <https://github.com/SSSD/sssd/issues/3871>`_ Try to suppress "Could not parse domain SID from [(null)]" for IPA users
-  `#3887 <https://github.com/SSSD/sssd/issues/3887>`_ Inform about SSSD PAC timeout better
-  `#3909 <https://github.com/SSSD/sssd/issues/3909>`_ AD provider and ignore_group_members=True might cause flaky group memberships
-  `#3915 <https://github.com/SSSD/sssd/issues/3915>`_ sssd: [sysdb_add_user] (0x0400): Error: 17 (File exists)


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_13_2..sssd-1_13_3

    Dan Lavu (1):
        de3370ca7  Clarify that subdomains always use service discovery

    Jakub Hrozek (7):
        03583e6e4  Upgrading the version for the 1.13.3 release
        3c52b17a2  DP: Do not confuse static analysers with dead code
        37cb25f70  BUILD: Only install polkit rules if the directory is available
        e4231dff1  IPA: Use search timeout, not enum timeout for searching overrides
        fee0024a3  AD: Add autofs provider
        9b8784899  MAN: Clarify when should TGs be disabled for group nesting restriction
        360cd32ef  Update translations for the 1.13.3 release

    Lukas Slebodnik (2):
        898309b7b  sbus_codegen_tests: Use portable definition of large constants
        ad8a36e29  DEBUG: Add missing new lines

    Michal Židek (1):
        fdbfa8c8b  MAN: sssd.conf should mention SSS_NSS_USE_MEMCACHE

    Pavel Březina (22):
        e736ccea5  SYSDB: Add missing include to sysdb_services.h
        d215702f4  LDAP: Mark globals in ldap_opts.h as extern
        be05c3f89  AD: Mark globals in ad_opts.h as extern
        2ce82341a  IPA: Mark globals in ipa_opts.h as extern
        713a7da0c  KRB5: Mark globals in krb5_opts.h as extern
        39843ca39  SUDO: convert periodical refreshes to be_ptask
        03c2affe7  SUDO: move refreshes from sdap_sudo.c to sdap_sudo_refresh.c
        1079a7c60  SUDO: move offline check to handler
        af3b1a9ef  SUDO: simplify error handling
        be1121afa  SUDO: fix sdap_id_op logic
        9ec429586  SUDO: fix tevent style
        5021ac65d  SUDO: fix sdap_sudo_smart_refresh_recv()
        a789a6dae  SUDO: sdap_sudo_load_sudoers improve iterator
        2099434cc  SUDO: set USN inside sdap_sudo_refresh request
        62f97308c  SUDO: built host filter inside sdap_sudo_refresh request
        699933748  SUDO: do not imitate full refresh if usn is unknown in smart refresh
        bbeaec95e  SUDO: fix potential memory leak in sdap_sudo_init
        cf6f8b46c  SUDO: obtain host information when going online
        bbfbada8a  SUDO: remove finalizer
        32c7b5c1c  SUDO: make sdap_sudo_handler static
        743544628  SUDO: use size_t instead of int in for cycles
        76170b96e  SUDO: get srv_opts after we are connected

    Pavel Reichl (1):
        be479e3d9  sysdb-tests: Fix warning - incompatible pointer type

    Petr Cech (2):
        5869cb41b  IPA_PROVIDER: Explicit no handle of services
        595ced74f  KRB5_CHILD: Debug logs for PAC timeout

    Sumit Bose (7):
        957ec3902  IPA: fix override with the same name
        e68d9dd2e  p11: allow p11_child to run completely unprivileged
        6a1b214b4  p11: check if cert is valid before selecting it
        14a983160  p11: enable ocsp checks
        9afa9b95b  ldap: skip sdap_save_grpmem() if ignore_group_members is set
        75359a03d  initgr: only search for primary group if it is not already cached
        fa5a6ab7e  LDAP: check early for missing SID in mapping check
