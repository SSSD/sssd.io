SSSD 1.16.5 Release Notes
=========================

Highlights
----------

New Features
~~~~~~~~~~~~

-  New option ad_gpo_ignore_unreadable was added that allows SSSD to ignore unreadable GPO containers in AD.
-  It is possible to configure auto_private_groups per subdomain or with subdomain_inherit.

Security issues fixed
~~~~~~~~~~~~~~~~~~~~~

-  A flaw was found in sssd Group Policy Objects implementation. When the GPO is not readable by SSSD due to a too strict permission settings on the server side, SSSD will allow all authenticated users to login instead of denying access. (CVE-2018-16838)

Notable bug fixes
~~~~~~~~~~~~~~~~~

-  Multiple URI specified in ldap_uri did not work properly if they differed only in port number.
-  Several issues with SUDO rules processing have been fixed.
-  SSSD sometimes incorrectly started in offline mode. This was fixed.
-  Issue with missing nested groups after add/remove operation on the sever was fixed.
-  A use-after-free error causing SSSD service to crash was fixed.

Tickets Fixed
-------------

-  `#4933 <https://github.com/SSSD/sssd/issues/4933>`_ - cached_auth_timeout not honored for AD users authenticated via trust with FreeIPA
-  `#4947 <https://github.com/SSSD/sssd/issues/4947>`_ - Write a list of host names up to a configurable limit to the kdcinfo files
-  `#4857 <https://github.com/SSSD/sssd/issues/4857>`_ - [RFE] Need an option in SSSD so that it will skip GPOs that have groupPolicyContainers, unreadable by SSSD
-  `#4938 <https://github.com/SSSD/sssd/issues/4938>`_ - [RFE]: Optionally disable generating auto private groups for subdomains of an AD provider
-  `#4931 <https://github.com/SSSD/sssd/issues/4931>`_ - sudo: runAsUser/Group does not work with domain_resolution_order
-  `#4832 <https://github.com/SSSD/sssd/issues/4832>`_ - KCM: If the default ccache cannot be found, fall back to the first one
-  `#4493 <https://github.com/SSSD/sssd/issues/4493>`_ - online detection in case sssd starts before network does appears to be broken
-  `#4937 <https://github.com/SSSD/sssd/issues/4937>`_ - Responders: ``is_user_local_by_name()`` should avoid calling nss API entirely
-  `#4948 <https://github.com/SSSD/sssd/issues/4948>`_ - Lookahead resolving of host names to provide names for the kdcinfo plugin
-  `#4986 <https://github.com/SSSD/sssd/issues/4986>`_ - The server error message is not returned if password change fails
-  `#4902 <https://github.com/SSSD/sssd/issues/4902>`_ - Double free error in tev_curl
-  `#4890 <https://github.com/SSSD/sssd/issues/4890>`_ - SSSD doesn't clear cache entries for IDs below min_id.
-  `#3895 <https://github.com/SSSD/sssd/issues/3895>`_ - FAIL test-find-uid
-  `#3919 <https://github.com/SSSD/sssd/issues/3919>`_ - sssd failover does not work on connecting to non-responsive <ldaps://server
-  `#5018 <https://github.com/SSSD/sssd/issues/5018>`_ - nss_cmd_endservent resets the wrong index
-  `#4980 <https://github.com/SSSD/sssd/issues/4980>`_ - Removing domain from ad_enabled_domains is not reflected in cache
-  `#5026 <https://github.com/SSSD/sssd/issues/5026>`_ - Paging not enabled when fetching external groups, limits the number of external groups to 2000
-  `#3648 <https://github.com/SSSD/sssd/issues/3648>`_ - sssd should not always read entire autofs map from ldap
-  `#5033 <https://github.com/SSSD/sssd/issues/5033>`_ - IFP: GetUserAttr does not search by UPN
-  `#5044 <https://github.com/SSSD/sssd/issues/5044>`_ - Trusted domain user logins succeed after using ipa trustdomain-disable
-  `#5042 <https://github.com/SSSD/sssd/issues/5042>`_ - Integration tests use python2 unconditionally
-  `#5077 <https://github.com/SSSD/sssd/issues/5077>`_ - autofs: delete possible duplicate of an autofs entry
-  `#3701 <https://github.com/SSSD/sssd/issues/3701>`_ - SSSD service is crashing: dbus_watch_handle() is invoked with corrupted 'watch' value
-  `#4968 <https://github.com/SSSD/sssd/issues/4968>`_ - sudo: do not update last usn when updating expired rules
-  `#4969 <https://github.com/SSSD/sssd/issues/4969>`_ - sudo: always use server highest usn for smart refresh
-  `#5014 <https://github.com/SSSD/sssd/issues/5014>`_ - sudo: incorrect usn value for openldap
-  `#5049 <https://github.com/SSSD/sssd/issues/5049>`_ - support for defaults entry is failing in sssd sudo against Openldap server
-  `#5085 <https://github.com/SSSD/sssd/issues/5085>`_ - Impossible to enforce GID on the AD's "domain users" group in the IPA-AD trust setup
-  `#4489 <https://github.com/SSSD/sssd/issues/4489>`_ - TESTS: make intgcheck is not always passing in the internal CI (enumeration tests)
-  `#5092 <https://github.com/SSSD/sssd/issues/5092>`_ - Force LDAPS over 636 with AD Provider
-  `#5053 <https://github.com/SSSD/sssd/issues/5053>`_ - Watchdog implementation or usage is incorrect
-  `#4657 <https://github.com/SSSD/sssd/issues/4657>`_ - nested group missing after updates on provider
-  `#5073 <https://github.com/SSSD/sssd/issues/5073>`_ - ldap_uri failover doesn't work with different ports
-  `#5106 <https://github.com/SSSD/sssd/issues/5106>`_ - Expecting appropriate error message when new password length is less than 8 characters when ldap_pwmodify_mode = ldap_modify in sssd.conf
-  `#5123 <https://github.com/SSSD/sssd/issues/5123>`_ - SSSD-1-16: sbus_auto_reconnect(): "off-by-one error" in ``reconnection_retries`` interpretation \`

Packaging Changes
-----------------

-  None.

Documentation Changes
---------------------

-  Added new option ldap_sasl_maxssf
-  Added new option ad_gpo_ignore_unreadable


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_16_4..sssd-1_16_5

    Alexey Tikhonov (13):
        33ac11fb7  Util: added facility to load nss lib syms
        8ba8b7136  responder/negcache: avoid calling nsswitch NSS API
        cc6d16a20  negcache_files: got rid of large array on stack
        5bba0d33e  TESTS: moved cwrap/test_negcache to cmocka tests
        b05f98e34  ci/sssd.supp: getpwuid() leak suppression
        37718f82c  util/tev_curl: Fix double free error in schedule_fd_processing()
        7b3c8e8c5  util/find_uid.c: fixed debug message
        fb50da239  util/find_uid.c: fixed race condition bug
        e294f7351  providers/ipa/: add_v1_user_data() amended
        f845355e3  SBUS: defer deallocation of sbus_watch_ctx
        0c620666d  util/watchdog: fixed watchdog implementation
        c0d64190a  TESTS: added sss_ptr_hash unit test
        a1bdab36e  SBUS: fixed off-by-one error" in sbus_auto_reconnect()

    Branen Salmon (1):
        7fe2b4465  knownhostsproxy: friendly error msg for NXDOMAIN

    Fabiano Fidêncio (1):
        bcb79f676  INTG: Increase the sleep() time so the changes are reflected on SSSD

    Jakub Hrozek (34):
        f2f5539b6  Updating the version for 1.16.5
        fedfc4fa5  SYSDB: Inherit cached_auth_timeout from the main domain
        6f6b3b1f4  AD: Allow configuring auto_private_groups per subdomain or with subdomain_inherit
        eaceb6a21  SDAP: Add sdap_has_deref_support_ex()
        2c97edb4b  IPA: Use dereference for host groups even if the configuration disables dereference
        6c568c912  KCM: Fall back to using the first ccache if the default does not exist
        e4dd2843a  krb5: Do not use unindexed objectCategory in a search filter
        7d8b28ad6  SYSDB: Index the ccacheFile attribute
        23fb7ea2f  krb5: Silence an error message if no cache entries have ccache stored but renewal is enabled
        0a637fff4  PAM: Also cache SSS_PAM_PREAUTH
        4ab1b754a  LDAP: Return the error message from the extended operation password change also on failure
        05b37ac18  TESTS: Add a unit test for UPNs stored by sss_ncache_prepopulate
        0ca64be4d  IPA: Allow paging when fetching external groups
        bca2f94aa  SYSDB: Add sysdb_search_with_ts_attr
        3ee57e7fa  BE: search with sysdb_search_with_ts_attr
        6bd021d22  BE: Enable refresh for multiple domains
        c56e16525  BE: Make be_refresh_ctx_init set up the periodical task, too
        936b423eb  BE/LDAP: Call be_refresh_ctx_init() in the provider libraries, not in back end
        5c60056ec  BE: Pass in attribute to look up with instead of hardcoding SYSDB_NAME
        8a8b23441  BE: Change be_refresh_ctx_init to return errno and set be_ctx->refresh_ctx
        0ef02c908  BE/LDAP: Split out a helper function from sdap_refresh for later reuse
        87cd4ec85  BE: Pass in filter_type when creating the refresh account request
        cb118860a  BE: Send refresh requests in batches
        b7110e05e  BE: Extend be_ptask_create() with control when to schedule next run after success
        e1830ba30  BE: Schedule the refresh interval from the finish time of the last run
        25b66e245  AD: Implement background refresh for AD domains
        468ee8bfe  IPA: Implement background refresh for IPA domains
        159d1afd3  BE/IPA/AD/LDAP: Add inigroups refresh support
        c3956d254  BE/IPA/AD/LDAP: Initialize the refresh callback from a list to reduce logic duplication
        8f027707e  IPA/AD/SDAP/BE: Generate refresh callbacks with a macro
        1754e3e08  MAN: Amend the documentation for the background refresh
        75b669567  DP/SYSDB: Move the code to set initgrExpireTimestamp to a reusable function
        06fed80b6  IPA/AD/LDAP: Increase the initgrExpireTimestamp after finishing refresh request
        fd8865e80  sudo: use objectCategory instead of objectClass in ad sudo provider

    Lukas Slebodnik (16):
        7b9524231  BUILD: Add macro for checking python3 modules
        44735f87d  BUILD: Fix typo of detecting python module for intgcheck
        cf2b5ec3f  BUILD: Move checking of python2 modules for intgcheck
        f9a4f722c  BUILD: Add macro for checking pytest for intgcheck
        03ba5e766  BUILD: Change value of variable HAVE_PYTHON2/3_BINDINGS
        cd0d38c07  BUILD: Move python checks for intgcheck to macro
        958f02dc6  INTG: Do hot hardcode version of python/pytest in intgcheck
        ec785153f  BUILD: Prefer python3 for intgcheck
        3a8ae6dad  intg: Install python3 dependencies for intgcheck on new distros
        4c2df3aa6  pyhbac: Fix warning Wdiscarded-qualifiers
        ed26a1e32  SSSDConfig: Add minimal test for parse method
        4f577e2f2  SSSDConfig: Fix SyntaxWarning "is not" with a literal
        8557cd9f1  TESTS: Add minimal test for pysss encrypt
        8bc81b313  pysss: Fix DeprecationWarning PY_SSIZE_T_CLEAN
        0ba6af645  pysss_murmur: Fix DeprecationWarning PY_SSIZE_T_CLEAN
        c962c70ef  testlib: Fix SyntaxWarning "is" with a literal

    Michal Židek (3):
        ad058011b  GPO: Add option ad_gpo_ignore_unreadable
        a4974d1a9  Updated translation files.
        c2053e909  translation: Add missing new lines

    Pavel Březina (79):
        5ad7f5e81  ipa: store sudo runas attribute with internal fqname
        3a18e33f9  sudo: format runas attributes to correct output name
        23ad178aa  ci: enable sssd-ci for 1-16 branch
        f988c870b  ci: switch to new tooling and remove 'Read trusted files' stage
        8003e3249  ci: rebase pull request on the target branch
        85dab318c  ci: print node on which the test is being run
        c9c2b6012  ad: remove subdomain that has been disabled through ad_enabled_domains from sysdb
        0e16ec74c  sysdb: add sysdb_domain_set_enabled()
        800d24dcc  ad: set enabled=false attribute for subdomains that no longer exists
        b2cd4a74e  sysdb: read and interpret domain's enabled attribute
        3c6c9d4d9  sysdb: add sysdb_list_subdomains()
        5605fa5f8  ad: remove all subdomains if only master domain is enabled
        0b6f14408  ad: make ad_enabled_domains case insensitive
        795606177  sss_ptr_hash: add sss_ptr_get_value to make it useful in delete callbacks
        00926ab45  sss_ptr_hash: keep value pointer when destroying spy
        49ad0b9b8  autofs: fix typo in test tool
        ccf14f490  sysdb: add expiration time to autofs entries
        57e33404e  sysdb: add sysdb_get_autofsentry
        c36605002  sysdb: add enumerationExpireTimestamp
        11ffb775d  sysdb: store enumeration expiration time in autofs map
        efe44597a  sysdb: store original dn in autofs map
        49b5baf0e  sysdb: add sysdb_del_autofsentry_by_key
        466560623  autofs: move data provider functions to responder common code
        01b7dc921  cache_req: add autofs map entries plugin
        e683556dc  cache_req: add autofs map by name plugin
        6fe479a21  cache_req: add autofs entry by name plugin
        b0043a95f  autofs: convert code to cache_req
        27d2dcfb7  autofs: use cache_req to obtain single entry in getentrybyname
        61a7bf4d2  autofs: use cache_req to obtain map in setent
        ca1ee9933  dp: replace autofs handler with enumerate method
        0b780a0d5  dp: add additional autofs methods
        fb9a42d95  ldap: add base_dn to sdap_search_bases
        bd15a135c  ldap: rename sdap_autofs_get_map to sdap_autofs_enumerate
        fcb6f55c0  ldap: implement autofs get map
        2e4525837  ldap: implement autofs get entry
        3e04a8127  autofs: allow to run only setent without enumeration in test tool
        ac712654f  autofs: always refresh auto.master
        58f3d5469  sysdb: invalidate also autofs entries
        9131b90f0  sss_cache: invalidate also autofs entries
        5157fccfd  ci: add Debian 10
        6b2c9e822  ci: allow distribution specific supression files
        c8a4c8e2e  ci: suppress Debian valgrind errors
        c097e2b91  ifp: let cache_req parse input name so it can fallback to upn search
        cc7b9366f  ifp: call tevent_req_post in case of error in ifp_user_get_attr_send
        b0e56ee31  ci: add Debian suppresion path
        900ebdbdb  ci: use python2 version of pytest
        d7fe86145  ci: pep8 was renamed to pycodestyle in Fedora 31
        28668d2f1  ci: remove left overs from previous rebase
        50dffac31  pysss: use METH_VARARGS | METH_KEYWORDS instead of just METH_KEYWORDS
        fc0be68fc  ci: enable on demand runs
        1f6fdb98e  ci: set build name to pull request or branch name
        7374ac4d6  ci: notify that build awaits executor
        3a4d13c27  ci: convert to scripted pipeline
        04bd7372f  autofs: remove unused enum
        416064949  autofs: delete possible duplicate of an autofs entry
        91f7b6c65  ci: store artifacts in jenkins for on-demand runs
        8b75c2118  ci: allow to specify systems where tests should be run for on-demand tests
        88f2c6317  ci: add Fedora 31
        c2e2f384c  ci: install python2 on Fedora 31 and RHEL 8 so python2 bindings can be built
        5bdfc48f4  ci: disable python2 bindings on Fedora 32+
        638431001  sudo: do not update last usn value on rules refresh
        38d00c4b4  sudo: always use server highest known usn for smart refresh
        fb2c54b69  man: update sudo smart refresh documentation to reflect new USN behavior
        19e8a02b0  sudo: use proper datetime for default modifyTimestamp value
        a1be9af74  sudo: get timezone information from previous value when constructing new usn
        634c1e0e4  sudo: add ldap_sudorule_object_class_attr
        80e6f714f  nss: use real primary gid if the value is overriden
        d8eec7173  ci: add rhel7
        7e6ab55b2  ci: set sssd-ci notification to pending state when job is started
        b9d419f84  ci: archive ci-mock-result
        ec8f5fd5e  tests: fix race condition in enumeration tests
        702e5fd29  ci: add CentOS 7
        191f3722f  sss_sockets: pass pointer instead of integer
        9a7c044dc  memberof: keep memberOf attribute for nested member
        78cf8b132  ci: keep system list outside repository
        1066130bf  ci: remove old dependency repository
        7f46c85dc  sss_ptr_hash: pass new hash_entry_t to custom delete callback
        4b1d1a099  failover: make sure we switch to another server if only port differs
        ddf0a59a6  sdap: provide error message when password change fail in ldap_modify mode

    Samuel Cabrero (2):
        2173201b5  SUDO: Allow defaults sudoRole without sudoUser attribute
        9673ca898  nss: Fix command 'endservent' resetting wrong struct member

    Simo Sorce (1):
        bad7c631b  Add TCP level timeout to LDAP services

    Sumit Bose (30):
        b927dc7c8  ipa: ipa_getkeytab don't call libnss_sss
        ceb4c8e21  pam: introduce prompt_config struct
        d453f92e1  authtok: add dedicated type for 2fa with single string
        ca65bfdab  pam_sss: use configured prompting
        c91c6dd4b  PAM: add initial prompting configuration
        efefac9f4  getsockopt_wrapper: add support for PAM clients
        558b54327  intg: add test for password prompt configuration
        e6734785f  winbind idmap plugin: update struct idmap_domain to latest version
        f5d031ba4  SDAP: allow GSS-SPNEGO for LDAP SASL bind as well
        373b1136c  sdap: inherit SDAP_SASL_MECH if not set explicitly
        cb94d00f3  DP: add NULL check to be_ptask_{enable|disable}
        9b8c66d53  tests: fix enctypes in test_copy_keytab
        3a92a87d4  CI: use python3-pep8 on Fedora 31 and later
        8f45a020d  BUILD: fix libpython handling in Python3.8
        934341e1e  negcache: add fq-usernames of know domains to all UPN neg-caches
        370dbcc62  ci: add pam wrapper
        2ea937af4  utils: extend some find_domain_* calls to search disabled domain
        698e27d8b  ipa: support disabled domains
        cc42fe7da  ipa: ignore objects from disabled domains on the client
        a9f03f01b  sysdb: add sysdb_subdomain_content_delete()
        124957a91  ipa: delete content of disabled domains
        fbd38903a  ipa: use LDAP not extdom to lookup IPA users and groups
        a967afdd0  ipa: use the right context for autofs
        489706399  ipa: add failover to override lookups
        a4dd1eb50  ipa: add failover to access checks
        3f370ad8c  sdap: update last_usn on reconnect
        44e76055d  ad: allow booleans for ad_inherit_opts_if_needed()
        b2aca1f7d  ad: add ad_use_ldaps
        07d19249a  ldap: add new option ldap_sasl_maxssf
        9b875b87f  ad: set min and max ssf for ldaps

    Tomas Halman (7):
        c225ed7ff  krb5: Write multiple dnsnames into kdc info file
        dab55626c  Providers: Delay online check on startup
        ec0c31a71  krb5: Lookahead resolving of host names
        fb3f1af38  CACHE: SSSD doesn't clear cache entries
        442cd6583  LDAP: failover does not work on non-responsive ldaps
        5b571efa6  CONFDB: Files domain if activated without .conf
        e48cdfb69  TESTS: adapt tests to enabled default files domain
