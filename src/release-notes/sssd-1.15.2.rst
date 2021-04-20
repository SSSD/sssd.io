SSSD 1.15.2 Release Notes
=========================

Highlights
----------

-  It is now possible to configure certain parameters of a trusted domain in a configuration file sub-section. In particular, it is now possible to configure which Active Directory DCs the SSSD talks to with a configuration like this:

..

::

       [domain/ipa.test]
       # IPA domain configuration. This domain trusts a Windows domain win.test

..

::

       [domain/ipa.test/win.test]
       ad_server = dc.win.test

..

-  Several issues related to socket-activating the NSS service, especially if SSSD was configured to use a non-privileged userm were fixed. The NSS service now doesn't change the ownership of its log files to avoid triggering a name-service lookup while the NSS service is not running yet. Additionally, the NSS service is started before any other service to make sure username resolution works and the other service can resolve the SSSD user correctly.
-  A new option ``cache_first`` allows the administrator to change the way multiple domains are searched. When this option is enabled, SSSD will first try to "pin" the requested name or ID to a domain by searching the entries that are already cached and contact the domain that contains the cached entry first. Previously, SSSD would check the cache and the remote server for each domain. This option brings performance benefit for setups that use multiple domains (even auto-discovered trusted domains), especially for ID lookups that would previously iterate over all domains. Please note that this option must be enabled with care as the administrator must ensure that the ID space of domains does not overlap.
-  The SSSD D-Bus interface gained two new methods: ``FindByNameAndCertificate`` and ``ListByCertificate``. These methods will be used primarily by IPA and `mod_lookup_identity <https://github.com/adelton/mod_lookup_identity/>`_ to correctly match multple users who use the same certificate for Smart Card login.
-  A bug where SSSD did not properly sanitize a username with a newline character in it was fixed.

Packaging Changes
-----------------

None in this release

Documentation Changes
---------------------

-  A new option ``cache_first`` was added. Please see the Highlights section for more details
-  The ``override_homedir`` option supports a new template expansion ``l`` that expands to the first letter of username

Tickets Fixed
-------------

-  `#4350 <https://github.com/SSSD/sssd/issues/4350>`_ - Newline characters (n) must be sanitized before LDAP requests take place
-  `#4349 <https://github.com/SSSD/sssd/issues/4349>`_ - sssd-secrets doesn't exit on idle
-  `#4347 <https://github.com/SSSD/sssd/issues/4347>`_ - sssd ignores entire groups from proxy provider if one member is listed twice
-  `#4197 <https://github.com/SSSD/sssd/issues/4197>`_ - when group is invalidated using sss_cache dataExpireTimestamp entry in the domain and timestamps cache are inconsistent
-  `#3709 <https://github.com/SSSD/sssd/issues/3709>`_ - [RFE] Add more flexible templating for override_homedir config option
-  `#3640 <https://github.com/SSSD/sssd/issues/3640>`_ - Make it possible to configure AD subdomain in the server mode
-  `#4354 <https://github.com/SSSD/sssd/issues/4354>`_ - chown in ExecStartPre of sssd-nss.service hangs forever
-  `#1885 <https://github.com/SSSD/sssd/issues/1885>`_ - Login time increases strongly if more than one domain is configured
-  `#3362 <https://github.com/SSSD/sssd/issues/3362>`_ - use the sss_parse_inp request in other responders than dbus


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 sssd-1_15_1..sssd-1_15_2

    Fabiano Fidêncio (7):
        ef268f9e6  RESPONDER: Wrap up the code to setup the idle timeout
        4358d7647  SECRETS: Shutdown the responder in case it becomes idle
        9286d0d41  CACHE_REQ: Move cache_req_next_domain() into a new tevent request
        8bb668063  CACHE_REQ: Check the caches first
        b7430c4f4  NSS: Don't set SocketUser/SocketGroup as "sssd" in sssd-nss.socket
        e19327b3b  NSS: Ensure the NSS socket is started before any other services' sockets
        ecaf0bb27  NSS: Don't call chown on NSS service's ExecStartPre

    Ignacio Reguero (1):
        7f97e6098  UTIL: first letter of user name template for override_homedir

    Jakub Hrozek (9):
        efd5c076f  Updating the version for the 1.15.2 release
        87ca3fda3  Allow manual start for sssd-ifp
        43d076010  NSS: Fix invalidating memory cache for subdomain users
        cab319e2d  UTIL: Add a new macro SAFEALIGN_MEMCPY_CHECK
        9a9b5e115  UTIL: Add a generic iobuf module
        321ca2827  BUILD: Detect libcurl during configure
        ca90f2102  UTIL: Add a libtevent libcurl wrapper
        91b0592cd  TESTS: test the curl wrapper with a command-line tool
        4c9419d98  Updating the translations for the 1.15.2 release

    Justin Stephenson (1):
        5424b90e8  MAN: Add dyndns_auth option

    Lukas Slebodnik (3):
        f09e045d4  test_secrets: Fail in child if sssd_secrets cannot start
        f8d34835b  test_utils: Add test coverage for %l in override_homedir
        db37eca43  util-test: Extend unit test for sss_filter_sanitize_ex

    Michal Židek (4):
        ebe05e32b  data_provider: Fix typo in DEBUG message
        231bd1b34  SUBDOMAINS: Configurable search bases
        62a1570f0  SUBDOMAINS: Allow options ad(_backup)_server
        61854f17c  MAN: Add trusted domain section man entry

    Pavel Březina (4):
        0dacb781f  cache_req: use rctx as memory context during midpoint refresh
        828fe7528  CACHE_REQ: Make cache_req_{create_and_,}add_result() more generic
        7cd226414  CACHE_REQ: Move result manipulation into a separate module
        606015a4f  CACHE_REQ: shortcut if object is found

    Petr Čech (2):
        57a924e71  sss_cache: User/groups invalidation in domain cache
        ed2a5dad1  PROXY: Remove duplicit users from group

    Sumit Bose (7):
        ba926c98b  sysdb: allow multiple results for searches by certificate
        2b80496ce  cache_req: allow multiple matches for searches by certificate
        861dbe079  ifp: add ListByCertificate
        ef55b0e47  ifp: add FindByNameAndCertificate
        16c9d63d9  PAM: allow muliple users mapped to a certificate
        7aadfa545  nss: ensure that SSS_NSS_GETNAMEBYCERT only returns a unique match
        3fd8ea55d  IPA: get overrides for all users found by certificate

    Thorsten Scherf (1):
        e0815d726  Fixed typo in debug output

    Victor Tapia (1):
        ee2906c1d  UTIL: Sanitize newline and carriage return characters.
