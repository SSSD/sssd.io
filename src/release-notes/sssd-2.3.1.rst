SSSD 2.3.1 Release Notes
========================

Highlights
----------

New features
~~~~~~~~~~~~

-  Domains can be now explicitly enabled or disabled using ``enable`` option in domain section. This can be especially used in configuration snippets.
-  New configuration options ``memcache_size_passwd``, ``memcache_size_group``, ``memcache_size_initgroups`` that can be used to control memory cache size.

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  Fixed several regressions in GPO processing introduced in sssd-2.3.0
-  Fixed regression in PAM responder: failures in cache only lookups are no longer considered fatal
-  Fixed regression in proxy provider: ``pwfield=x`` is now default value only for ``sssd-shadowutils`` target

Packaging changes
~~~~~~~~~~~~~~~~~

-  ``libwbclient`` is now deprecated and is not being built by default (use ``--with-libwibclient`` to build it)

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

-  Added option ``memcache_size_passwd``
-  Added option ``memcache_size_group``
-  Added option ``memcache_size_initgroups``
-  Added option ``enable`` in domain sections
-  Minor text improvements

Tickets Fixed
-------------

-  `#1024 <https://github.com/SSSD/sssd/issues/1024>`_ - SSSD user/group filtering is failing after "files" provider rebuilds cache
-  `#1031 <https://github.com/SSSD/sssd/issues/1031>`_ - When the passwd or group files are replaced, sssd stops monitoring the file for inotify events, and no updates are triggered
-  `#3728 <https://github.com/SSSD/sssd/issues/3728>`_ - When sssd service fails to start due to misconfiguration, the error message would be nice in /var/log/messages as well
-  `#3920 <https://github.com/SSSD/sssd/issues/3920>`_ - Add multiple domains tests to responder_cache_req-tests
-  `#4578 <https://github.com/SSSD/sssd/issues/4578>`_ - sssctl: Add memcache diagnostic and inspection commands
-  `#4667 <https://github.com/SSSD/sssd/issues/4667>`_ - sssd fails to release file descriptor on child logs after receiving HUP
-  `#4743 <https://github.com/SSSD/sssd/issues/4743>`_ - [RFE] Add "enabled" option to domain section
-  `#5075 <https://github.com/SSSD/sssd/issues/5075>`_ - sssd failover leads to delayed and failed logins
-  `#5103 <https://github.com/SSSD/sssd/issues/5103>`_ - GPO: Incorrect processing / inheritance order of HBAC GPOs
-  `#5115 <https://github.com/SSSD/sssd/issues/5115>`_ - mem-cache bug: only small fraction of memory allocated is actually used
-  `#5129 <https://github.com/SSSD/sssd/issues/5129>`_ - id_provider = proxy proxy_lib_name = files returns \* in password field, breaking PAM authentication
-  `#5135 <https://github.com/SSSD/sssd/issues/5135>`_ - Certificate attributes are not sanitized prior to ldap search
-  `#5142 <https://github.com/SSSD/sssd/issues/5142>`_ - RFE: Add option to specify alternate sssd config file location with "sssctl config-check" command.
-  `#5151 <https://github.com/SSSD/sssd/issues/5151>`_ - sssd is failing to discover other subdomains in the forest if LDAP entries do not contain AD forest root information
-  `#5153 <https://github.com/SSSD/sssd/issues/5153>`_ - Oddjob-mkhomedir fails when using NSS compat
-  `#5155 <https://github.com/SSSD/sssd/issues/5155>`_ - Document how to prevent invalid selinux context for default home directories in SSSD-AD direct integration.
-  `#5164 <https://github.com/SSSD/sssd/issues/5164>`_ - Change the message "Please enter smart card" to "Please insert smart card" on GDM login with smart-card
-  `#5167 <https://github.com/SSSD/sssd/issues/5167>`_ - AD: ad_access.c performs out-of memory check for wrong tevent request pointer
-  `#5170 <https://github.com/SSSD/sssd/issues/5170>`_ - SSSD must be able to resolve membership involving root with files provider
-  `#5181 <https://github.com/SSSD/sssd/issues/5181>`_ - system not enforcing GPO rule restriction. ad_gpo_implicit_deny = True is not working
-  `#5183 <https://github.com/SSSD/sssd/issues/5183>`_ - sssd 2.3.0 breaks AD auth due to GPO parsing failure
-  `#5186 <https://github.com/SSSD/sssd/issues/5186>`_ - sssd 2.3.0 buld errors due to issue with sv translation of man page
-  `#5190 <https://github.com/SSSD/sssd/issues/5190>`_ - GDM password prompt when cert mapped to multiple users and promptusername is False
-  `#5199 <https://github.com/SSSD/sssd/issues/5199>`_ - do not add fully-qualified suffix to already fully-qualified externalUser values in sudoers for IPA provider
-  `#5201 <https://github.com/SSSD/sssd/issues/5201>`_ - sssd-common: missing comma in file sssd_functions.stp
-  `#5217 <https://github.com/SSSD/sssd/issues/5217>`_ - NULL dereference in ``rotate_debug_files()``
-  `#5230 <https://github.com/SSSD/sssd/issues/5230>`_ - Deprecate SSSD's version of libwbclient
-  `#5236 <https://github.com/SSSD/sssd/issues/5236>`_ - sss_ssh_knownhostsproxy leads to silent failure for non-existent or non-co-operative hosts

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-2_3_0..sssd-2_3_1

    Alejandro Visiedo (2):
        66029529f  systemtap: Missing a comma
        ff8d7b8f0  config: [RFE] Add "enabled" option to domain section

    Alexander Bokovoy (1):
        48f9b2cb4  ipa: Do not qualify already qualified users in sudo rules

    Alexey Tikhonov (30):
        375887543  DEBUG: only open child process log files when required
        39480618a  CLIENT: fixed few CHECKED_RETURN (CWE-252) warnings
        014cbde8f  NSS: fixed FORWARD_NULL (CWE-476)
        ee16f3928  KCM: fixed NO_EFFECT (CWE-398)
        8088b3e3a  PROXY: suppress CPPCHECK_WARNING (CWE-456)
        b132fab8c  MC: fixed CPPCHECK_WARNING
        6701ad96a  CLIENT: fixed CPPCHECK_WARNING (CWE-476)
        144e78dfe  util/inotify: fixed CLANG_WARNING
        0c5711f9b  util/inotify: fixed bug in inotify event processing
        9c4d662de  TOOLS: fixed CLANG_WARNING
        e525ed6a6  TOOLS: fixed a couple of CLANG_WARNINGs
        14e5c31e5  CLIENT: fixed "Dereference of null pointer" warning
        464f809e0  RESPONDER/SUDO: fixed CLANG_WARNING
        83389697f  RESPONDER/NSS: fixed few CLANG_WARNINGs
        316c850ec  CACHE_REQ: fixed CLANG_WARNING
        64adcd410  PROVIDERS/LDAP: fixed CLANG_WARNING
        ce0699543  PROVIDERS/LDAP: fixed CLANG_WARNING
        5611d242f  PROVIDERS/IPA: fixed few CLANG_WARNINGs
        f61f972b2  DEBUG: fixed potential NULL dereference
        4fd05180b  TRANSLATIONS: updated translations to include new source file
        88e92967a  NEGCACHE: skip permanent entries in [users/groups] reset
        39e50096c  NSS: fixed UNINIT (CWE-457)
        2d90e6420  mem-cache: sizes of free and data tables were made consistent
        e12340e7d  NSS: avoid excessive log messages
        be8052bbb  NSS: enhanced debug during mem-cache initialization
        2ad4aa8f2  mem-cache: added log message in case cache is full
        b7f31936e  NSS: make memcache size configurable in megabytes
        b96b05bc4  mem-cache: comment added
        484507bf2  mem-cache: always cleanup old content
        3e7633bf0  Updated translation files: Japanese, Chinese (China), French

    David Ward (1):
        230a5068d  failover: fix documentation of default timeouts

    Lukas Slebodnik (2):
        79e01fc95  python-test.py: Do not use letter similar to numbers
        4c4b62b41  INTG: Do not use letter similar to numbers in python code

    Michal Židek (1):
        80e7163b7  NSS: make memcache size configurable

    Niranjan M.R (1):
        b52c4c954  pytest/testlib: Remove explcit encryption types from kdc.conf

    Pavel Březina (12):
        169ddae34  Update version in version.m4 to track the next release.
        532b75c93  test: avoid endian issues in network tests
        c226703fb  Provide new link for documentation: change sssd.github.io to sssd.io
        a08d4741c  pam_sss: fix missing initializer
        8969c43dc  files: allow root membership
        ffb9ad133  proxy: use 'x' as default pwfield only for sssd-shadowutils target
        f28eedc16  monitor: log to syslog when service fails to start
        cea0db2d6  po: fix sv translation
        0609d0f76  sss_ssh_knownhostsproxy: print error when unable to connect
        3be349b96  sss_ssh_knownhostsproxy: print error when unable to proxy data
        d999cbf46  Update the translations for the 2.3.1 release
        7e004b7c5  tests: discard const in test_confdb_get_enabled_domain_list

    Paweł Poławski (1):
        a06bf7885  AD: Enforcing GPO rule restriction on user

    Sumit Bose (19):
        aac4dbb17  NSS client: preserve errno during _nss_sss_end* calls
        3ea6e61cd  ad: remove unused libsbmclient form libsss_ad.so
        26c794da3  pam_sss: add SERVICE_IS_GDM_SMARTCARD
        3ed254765  pam_sss: special handling for gdm-smartcard
        a7c755672  ad_gpo_ndr.c: more ndr updates
        dce025b88  GPO: fix link order in a SOM
        8ca799ea9  sysdb: make sysdb_update_subdomains() more robust
        d3089173d  ad: rename ad_master_domain_\* to ad_domain_info_\*
        9aa26f651  sysdb: make new_subdomain() public
        2bad4d4b2  ad: rename ads_get_root_id_ctx() to ads_get_dom_id_ctx
        8c642a542  ad: remove unused trust_type from ad_subdom_store()
        3ae3286d6  ad: add ad_check_domain_{send|recv}
        e25e1e922  ad: check forest root directly if not present on local DC
        e58853f9c  DEBUG: use new exec_child(_ex) interface in tests
        df632eec4  ipa: add failover to subdomain override lookups
        31e574325  pam_sss: make sure old certificate data is removed before retry
        100839b64  PAM: do not treat error for cache-only lookups as fatal
        41a60c626  libwbclient-sssd: deprecate libwbclient-sssd
        a2b9a8446  certmap: sanitize LDAP search filter

    Thomas Reim (1):
        391b9c5e9  Minor fix in ad_access.c out of memory check

    Tomas Halman (3):
        61f4aaa56  sssctl: sssctl config-check alternative config file
        d8d743870  man: Document invalid selinux context for homedirs
        72b8e02c7  sssctl: sssctl config-check alternative snippet dir

    Yuri Chornoivan (1):
        f47ad87a8  general: fix minor typos

    ikerexxe (7):
        ceebe02ec  db/sysdb.c: remove unused variable
        437778b53  data_provider/dp_target_id: remove store statement from a never read variable
        54b1c19b6  p11_child/p11_child_common: remove store statement from a never read variable
        0cebd0f9e  autofs_test_client and sss_tools: remove store statements from never read variables
        5d9e2328c  responder/common/responder_packet: get packet length only once
        b92050261  Test: Add users_by_filter_multiple_domains_valid
        0cd3f5c0b  Test: Add groups_by_filter_multiple_domains_valid

    vinay mishra (1):
        02fbf47a8  Replaced 'enter' with 'insert'
