SSSD 2.5.1 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

* ``auto_private_groups`` option can be set centrally through ID range setting in IPA (see ``ipa idrange`` commands family). This feature requires SSSD update on both client and server. This feature also requires ``freeipa 4.9.4`` and newer.

Important fixes
~~~~~~~~~~~~~~~

* Fix ``getsidbyname`` issues with IPA users with a user-private-group

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* Default value of ``ldap_sudo_random_offset`` changed to ``0`` (disabled). This makes sure that sudo rules are available as soon as possible after SSSD start in default configuration.

Tickets Fixed
-------------

- `#2765 <https://github.com/SSSD/sssd/issues/2765>`_ - [RFE] Expand kerberos ticket renewal in KCM
- `#4216 <https://github.com/SSSD/sssd/issues/4216>`_ - [RFC] IPA: allow switching off user private groups for trusted AD users
- `#5607 <https://github.com/SSSD/sssd/issues/5607>`_ - SSSD fails nss_getby_name for IPA user with SID if the user has user private group
- `#5609 <https://github.com/SSSD/sssd/issues/5609>`_ - [RFE] Randomize the SUDO timeouts upon reconnection
- `#5614 <https://github.com/SSSD/sssd/issues/5614>`_ - SSSD Error Msg Improvement: Server resolution failed: [2]: No such file or directory
- `#5615 <https://github.com/SSSD/sssd/issues/5615>`_ - SSSD Error Msg Improvement:  Failed to resolve server 'server.example.com': Error reading file
- `#5616 <https://github.com/SSSD/sssd/issues/5616>`_ - sssd.conf man page: parameter dns_resolver_server_timeout and dns_resolver_op_timeout
- `#5628 <https://github.com/SSSD/sssd/issues/5628>`_ - kcm: return KRB5_FCC_INTERNAL when opcode is not found or not implemented
- `#5638 <https://github.com/SSSD/sssd/issues/5638>`_ - Responder: potential NULL deref
- `#5650 <https://github.com/SSSD/sssd/issues/5650>`_ - sss_pac_make_request fails on systems joined to Active Directory.
- `#5660 <https://github.com/SSSD/sssd/issues/5660>`_ - sudo commands incorrectly exports the KRB5CCNAME environment variable

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.5.0..2.5.1

    Alexey Tikhonov (2):
        9777427fa  UTIL/SECRETS: mistype fix
        fbf33babe  TOOLS: removed unneeded debug message

    Deepak Das (4):
        43b9b0922  SSSD man: man_dns_resolver_parameter_modification
        7190f6b5d  SSSD man: man_dns_resolver_parameter_modification
        d35f36f0f  SSSD Log: log_error_reading_file_msg_modification
        9c06088de  SSSD Log: no_such_file_or_directory_modification

    Iker Pedrosa (1):
        ac1a07a30  responder: fix covscan issues

    Jakub Vavra (1):
        5b5e3827a  Tests: Add test_ipa_missing_secondary_ipa_posix_groups

    Joakim Tjernlund (1):
        597a6c2a7  Gentoo/openrc: Add sssd-kcm service script

    Justin Stephenson (6):
        dbde4e692  SECRETS: Resolve mkey path correctly
        c917f9774  RESPONDER: Generate incrementing client ID
        bee426c8d  SBUS: Send Client ID across to DP interfaces
        7ed878723  RESPONDER LOGS: Log the Client ID where accessible
        d0e358945  CACHE_REQ: Log the Client ID of the cache request
        4f1a06d15  DP: Propagate down the client id and sender name

    Madhuri Upadhye (3):
        6eb845d09  Test: IPA: filter_groups option partially filters the group from 'id' output
        98400ef64  Tests: common: Update the remove_sss_cache function
        33f136f8f  Tests: alltests: Code update for test_kcm_check_socket_path

    Pavel Březina (9):
        a95db4e1b  Update version in version.m4 to track the next release
        9b017dbc8  KCM: return KRB5_FCC_INTERNAL for unknown or not implemented operation
        b099498f5  ipa: read auto_private_groups from id range if available
        706627cf7  cache_req: consider mpg_mode of each domain
        850af600d  pot: update pot files
        a3cb98120  sudo: disable ldap_sudo_random_offset by default
        669ee920d  readme: update documentation repository
        c415dde65  pot: update pot files
        5674aaedf  pot: update pot files

    Paweł Poławski (2):
        1c6556104  README: Update documentation links
        ecb2ae7a8  krb5_child: Honor Kerberos keytab location

    Steeve Goveas (2):
        348512b09  TEST: Fixes after running new tests downstream
        e147d2722  TEST: add ldap_sudo_random_offset 0 to offline test

    Sumit Bose (7):
        9cb89666e  nss: fix getsidbyname for IPA user-private-groups
        367465249  kcm: use %zu as format for size_t
        b75ef442d  pac: allow larger PACs
        73cbe0b1a  utils: add mod_defaults_list
        70a808d5a  pam: replace first argument of filter_responses()
        f491979d4  pam: parse pam_response_filter values only once
        2a4c38334  pam: change default for pam_response_filter

    Weblate (1):
        1f6377d59  po: update translations
