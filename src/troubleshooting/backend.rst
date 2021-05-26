Troubleshooting Backend
=======================

A ``backend``, often also called ``data provider``, is an SSSD child process.
This process talks to LDAP server, performs different lookup queries and stores
the results in the cache. The SSSD Cache is a local database containing identity
and authentication information which may be reused later to speed up answering
client queries. SSSD backend also performs online ``authentication``
against LDAP or Kerberos and ``applies access and password policy``
to the user that is about to log in.


Understanding the backend component
-----------------------------------

Backend process and its files
*****************************

There is one back-end process ``/usr/libexec/sssd/sssd_be`` for each
domain configured within ``sssd.conf`` and ``enabled``. If the domain is disabled
(by default) then a dedicated backend process will not be created.
Each backend process manages one SSSD domain defined in the configuration
file and also its trusted domains (referred to as subdomains) that are
auto-discovered at start up.

Let’s take a look at this example configuration.

.. code-block:: ini

    [sssd]
    services = nss, pam, sudo
    domains = IPA.PB, AD.PB
    config_file_version = 2

    [domain/IPA.PB]
    id_provider = ipa
    access_provider = ipa
    ipa_domain = ipa.pb

    [domain/AD.PB]
    id_provider = ad
    ad_domain = ad.pb
    ad_server = _srv_

    [domain/AC.PB]
    id_provider = ad
    ad_domain = ad.pb
    ad_server = _srv_

We have three domains configured, but only two enabled: ``IPA.PB`` and ``AD.PB``.
Each enabled domain has its own cache file, which is shared between the parent domain
and its subdomains and its own log file. The cache file is stored in
``/var/lib/sss/db/$domain.ldb`` and the log file is located at
``/var/log/sssd/$domain.log``.

The following example shows us the SSSD backend processes and cache and log
files location:

.. code-block:: console

    # ps aux | grep sssd_be
    /usr/libexec/sssd/sssd_be --domain IPA.PB --uid 0 --gid 0 --debug-to-files
    /usr/libexec/sssd/sssd_be --domain AD.PB --uid 0 --gid 0 --debug-to-files

    # ls -l /var/log/sssd/
    -rw-------. 1 root root 73870 Mar 20 10:50 sssd_IPA.PB.log
    -rw-------. 1 root root 73870 Mar 20 10:50 sssd_AD.PB.log

    # ls -l /var/lib/sss/db/
    -rw-------. 1 root root 1286144 Mar 20 10:50 cache_IPA.PB.ldb
    -rw-------. 1 root root 1286144 Mar 20 10:50 cache_AD.PB.ldb

Data provider work flow
***********************

The SSSD backend provides several services: ``id``, ``auth``, ``access``, etc.
(refer to sssd manual page for the full list of services). Each service is
associated with one data provider through a configuration option, for example
the identity service is set to IPA provider with ``id_provider = ipa``. Usually only
id and access providers are set, having the others default to the same provider
as id. Data provider tells SSSD how to talk with specific server implementation
(LDAP, IPA, Active Directory, Kerberos) and how its data schema and features
are translated into SSSD cache.

When an SSSD responder calls a backend method a series of operations is initiated.
First a new Data Provider request is created. This request decides what provider
module and which method from this module will handle the responder’s request.
Then it executes this method and awaits until it is finished. After that a reply
is constructed and sent back to the responder.

The flow goes like this: ``Backend Method Called`` -> ``Create Data Provider request``
-> ``Load provider method`` -> ``Run provider method`` -> ``Provider method finished`` ->
``Finish Data Provider request`` -> ``Return result`` to the caller.

Enable logging
**************

First, to actually see something in the log file we need to enable logging by
setting a debug level.

.. code-block:: c

    src/util/debug.h
    #define SSSDBG_FATAL_FAILURE  0x0010   0b00000000 00010000 /* level 0 */
    #define SSSDBG_CRIT_FAILURE   0x0020   0b00000000 00100000 /* level 1 */
    #define SSSDBG_OP_FAILURE     0x0040   0b00000000 01000000 /* level 2 */
    #define SSSDBG_MINOR_FAILURE  0x0080   0b00000000 10000000 /* level 3 */
    #define SSSDBG_CONF_SETTINGS  0x0100   0b00000001 00000000 /* level 4 */
    #define SSSDBG_FUNC_DATA      0x0200   0b00000010 00000000 /* level 5 */
    #define SSSDBG_TRACE_FUNC     0x0400   0b00000100 00000000 /* level 6 */
    #define SSSDBG_TRACE_LIBS     0x1000   0b00010000 00000000 /* level 7 */
    #define SSSDBG_TRACE_INTERNAL 0x2000   0b00100000 00000000 /* level 8 */
    #define SSSDBG_TRACE_ALL      0x4000   0b01000000 00000000 /* level 9 */
    #define SSSDBG_BE_FO          0x8000   0b10000000 00000000 /* level 10*/

                                  0xB7F0   0b10110111 11110000
                                  0xF7F0   0b11110111 11110000
                                  0x3FF0   0b00111111 11110000


There are few ways to achieve this:

- Using ``debug_level`` directive in domain section in ``sssd.conf``.

.. code-block:: console

    # cat /etc/sssd.conf
    ...
    [domain/IPA.PB]
    ...
    debug_level = 0x3ff0
    ...

- Using ``sss_debuglevel`` tool which will set the level only for current SSSD
  instance and will set the original level when SSSD is restarted.

.. code-block:: console

    # systemctl start sssd.service
    # sss_debuglevel 0x3ff0

- Using ``sssctl`` util:

.. code-block:: console

    # sssctl debug-level <VAL>
    # sssctl --debug <VAL>


Debug level ``0x3ff0`` contains enough information for all basic tasks.
Higher level providers details on input and output operations that creates
only noise that makes the log hard to read in most of the cases so I do not
recommend setting it unless it is needed.

Reading the logs
----------------

This section contains a description of the most fundamental parts of the
backend and how are they described by log messages. We are trying to keep log
messages and format as consistent as possible for all SSSD parts.

Each log line contains some core information like:

- Timestamp

- Responder / module identifier

- Function identifier

- Debug level

- Debug payload

Sample SSSD log output example:

.. code-block:: sssd-log

    (Tue Nov 20 12:23:21 2020) [sssd[nss]] [cache_req_send] (0x0400): CR #59: New request 'User by name'
    (Tue Nov 20 12:18:56 2020) [sssd[be[ldap.vm]]] [be_resolve_server_process] (0x1000): Saving the first resolved server
    (Tue Nov 20 12:18:56 2020) [sssd[be[ldap.vm]]] [be_resolve_server_process] (0x0200): Found address for server master.ldap.vm: [192.168.100.20] TTL 0
    (Tue Nov 20 12:18:56 2020) [sssd[be[ldap.vm]]] [sdap_uri_callback] (0x0400): Constructed uri 'ldap://master.ldap.vm:389'

In the following chapters we will exclude the first column timestamp in the log snippets.


Validating options
******************

On startup, the backend prints into the domain log options read by SSSD
together with their configured values including options not explicitly specified
in the ``sssd.conf``. This is useful to see how the SSSD is configured.

.. code-block:: sssd-log

    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_enumeration_search_timeout has value 60
    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_auth_disable_tls_never_use_in_production is FALSE
    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_page_size has value 1000
    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_deref_threshold has value 10
    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_sasl_canonicalize is FALSE
    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_connection_expire_timeout has value 900
    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_disable_paging is FALSE
    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_idmap_range_min has value 200000
    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_idmap_range_max has value 2000200000
    [be[IPA.PB]] [dp_get_options] (0x0400): Option ldap_idmap_range_size has value 200000


Data Provider request life cycle
********************************

Usually, there is one thing that goes wrong. User is not found or is not
permitted access, authentication fails, group membership does not contain all
members, etc. It is good to first look at data provider configuration to know
what providers are being used and then to the data provider request itself to
see how it finished. This will give us indicate where to look next.

- What providers are used for different backend services?

.. code-block:: sssd-log

    [be[IPA.PB]] [dp_load_configuration] (0x0100): Using [ipa] provider for [id]
    [be[IPA.PB]] [dp_load_configuration] (0x0100): Using [ipa] provider for [auth]
    [be[IPA.PB]] [dp_load_configuration] (0x0100): Using [ipa] provider for [access]
    [be[IPA.PB]] [dp_load_configuration] (0x0100): Using [ipa] provider for [chpass]
    [be[IPA.PB]] [dp_load_configuration] (0x0100): Using [ipa] provider for [sudo]
    [be[IPA.PB]] [dp_load_configuration] (0x0100): Using [ipa] provider for [autofs]
    [be[IPA.PB]] [dp_load_configuration] (0x0100): Using [ipa] provider for [selinux]
    [be[IPA.PB]] [dp_load_configuration] (0x0100): Using [ipa] provider for [hostid]
    [be[IPA.PB]] [dp_load_configuration] (0x0100): Using [ipa] provider for [subdomains]

- Each data provider request start and end is marked in logs. It is associated
  with other related messages with a number, using the format ``DP Request
  [$request-type #$request-number]``. We can see that there is one active data
  provider request of type Account in the following example and it finish with
  success. There are no more active requests when this one is finished.

.. code-block:: sssd-log

    [be[IPA.PB]] [dp_attach_req] (0x0400): DP Request [Account #1]: New request. Flags [0x0001].
    [be[IPA.PB]] [dp_attach_req] (0x0400): Number of active DP request: 1

    ... provider specific method logs ...
    [be[IPA.PB]] [dp_req_done] (0x0400): DP Request [Account #1]: Request handler finished [0]: Success
    [be[IPA.PB]] [_dp_req_recv] (0x0400): DP Request [Account #1]: Receiving request data.
    [be[IPA.PB]] [dp_req_reply_list_success] (0x0400): DP Request [Account #1]: Finished. Success.
    [be[IPA.PB]] [dp_req_reply_std] (0x1000): DP Request [Account #1]: Returning [Success]: 0,0,Success
    [be[IPA.PB]] [dp_table_value_destructor] (0x0400): Removing [0:1:0x0001:1:V:ad.pb:name=user-1@ad.pb] from reply table
    [be[IPA.PB]] [dp_req_destructor] (0x0400): DP Request [Account #1]: Request removed.
    [be[IPA.PB]] [dp_req_destructor] (0x0400): Number of active DP request: 0

- If the request is not successful, this is the place where we would see it:

.. code-block:: sssd-log

    [be[IPA.PB]] [dp_req_reply_std] (0x1000): DP Request [Subdomains #0]: Returning [Provider is Offline]: 1,1432158212,Offline

Failover information
********************

Failover is a crucial part of SSSD. If SSSD goes offline because it cannot
establish a connection to a server, this is the place to look for the cause.
It may be a DNS issue where we cannot resolve hostname or SRV records. It may
be a connection issue when the remote server is unrechable because it is behind
firewall, etc.

- Primary and backup server discovered with SRV DNS resolution or from configuration file

.. code-block:: sssd-log

    [be[IPA.PB]] [fo_discover_srv_done] (0x0400): Got 1 servers
    [be[IPA.PB]] [fo_add_server_to_list] (0x0400): Inserted primary server 'master.ipa.pb:389' to service 'IPA'

- The whole failover process:

.. code-block:: sssd-log

    # 1. We are trying to resolve IPA service
    [be[IPA.PB]] [fo_resolve_service_send] (0x0100): Trying to resolve service 'IPA'

    # 2. No cache resolution is present, we need to find server, pick one and resolve hostname
    [be[IPA.PB]] [get_port_status] (0x1000): Port status of port 0 for server '(no name)' is 'neutral'
    [be[IPA.PB]] [fo_resolve_service_activate_timeout] (0x2000): Resolve timeout set to 6 seconds

    #3. SRV DNS resolution requested
    [be[IPA.PB]] [resolve_srv_send] (0x0200): The status of SRV lookup is neutral
    [be[IPA.PB]] [resolv_discover_srv_next_domain] (0x0400): SRV resolution of service 'ldap'. Will use DNS discovery domain 'ipa.pb'
    [be[IPA.PB]] [resolv_getsrv_send] (0x0100): Trying to resolve SRV record of '_ldap._tcp.ipa.pb'
    [be[IPA.PB]] [schedule_request_timeout] (0x2000): Scheduling a timeout of 6 seconds
    [be[IPA.PB]] [schedule_timeout_watcher] (0x2000): Scheduling DNS timeout watcher
    [be[IPA.PB]] [resolv_getsrv_done] (0x1000): Using TTL [86400][request_watch_destructor] (0x0400): Deleting request watch
    [be[IPA.PB]] [fo_discover_srv_done] (0x0400): Got answer. Processing...

    #4. We have found one primary server
    [be[IPA.PB]] [fo_discover_srv_done] (0x0400): Got 1 servers
    [be[IPA.PB]] [fo_add_server_to_list] (0x0400): Inserted primary server   'master.ipa.pb:389' to service 'IPA'
    [be[IPA.PB]] [set_srv_data_status] (0x0100): Marking SRV lookup of service 'IPA' as 'resolved'

    #5. Now we need to resolve hostname
    [be[IPA.PB]] [get_server_status] (0x1000): Status of server 'master.ipa.pb' is 'name not resolved'
    [be[IPA.PB]] [resolv_gethostbyname_step] (0x2000): Querying files
    [be[IPA.PB]] [resolv_gethostbyname_files_send] (0x0100): Trying to resolve A record of 'master.ipa.pb' in files
    [be[IPA.PB]] [set_server_common_status] (0x0100): Marking server 'master.ipa.pb' as 'resolving name'
    [be[IPA.PB]] [resolv_gethostbyname_step] (0x2000): Querying files
    [be[IPA.PB]] [resolv_gethostbyname_files_send] (0x0100): Trying to resolve AAAA record of 'master.ipa.pb' in files
    [be[IPA.PB]] [resolv_gethostbyname_next] (0x0200): No more address families to retry
    [be[IPA.PB]] [resolv_gethostbyname_step] (0x2000): Querying DNS
    [be[IPA.PB]] [resolv_gethostbyname_dns_query] (0x0100): Trying to resolve A record of 'master.ipa.pb' in DNS
    [be[IPA.PB]] [schedule_request_timeout] (0x2000): Scheduling a timeout of 6 seconds
    [be[IPA.PB]] [schedule_timeout_watcher] (0x2000): Scheduling DNS timeout watcher
    [be[IPA.PB]] [sbus_remove_timeout] (0x2000): 0x2230a70
    [be[IPA.PB]] [id_callback] (0x0100): Got id ack and version (1) from Monitor
    [be[IPA.PB]] [resolv_gethostbyname_dns_parse] (0x1000): Parsing an A reply
    [be[IPA.PB]] [request_watch_destructor] (0x0400): Deleting request watch
    [be[IPA.PB]] [set_server_common_status] (0x0100): Marking server 'master.ipa.pb' as 'name resolved'

    #6. Success, now we will connect to this server
    [be[IPA.PB]] [be_resolve_server_process] (0x1000): Saving the first resolved server
    [be[IPA.PB]] [be_resolve_server_process] (0x0200): Found address for server master.ipa.pb: [10.34.78.100] TTL 1200
    [be[IPA.PB]] [ipa_resolve_callback] (0x0400): Constructed uri 'ldap://master.ipa.pb'
    [be[IPA.PB]] [sssd_async_socket_init_send] (0x0400): Setting 6 seconds timeout for connecting
    [be[IPA.PB]] [sdap_ldap_connect_callback_add] (0x1000): New LDAP connection to [ldap://master.ipa.pb:389/??base] with fd [21].

- If the failover process fails for some reason, it will be visible in these logs. For example:

.. code-block:: sssd-log

    [be[IPA.PB]] [fo_resolve_service_done] (0x0020): Failed to resolve server 'invalid.ipa.pb': Domain name not found
    [be[IPA.PB]] [set_server_common_status] (0x0100): Marking server 'invalid.ipa.pb' as 'not working'
    [be[IPA.PB]] [be_resolve_server_process] (0x0080): Couldn't resolve server (invalid.ipa.pb), resolver returned [11]: Resource temporarily unavailable
    [be[IPA.PB]] [be_resolve_server_process] (0x1000): Trying with the next one!
    [be[IPA.PB]] [fo_resolve_service_send] (0x0100): Trying to resolve service 'IPA'
    [be[IPA.PB]] [get_server_status] (0x1000): Status of server 'invalid.ipa.pb' is 'not working'
    [be[IPA.PB]] [get_server_status] (0x1000): Status of server 'invalid.ipa.pb' is 'not working'
    [be[IPA.PB]] [fo_resolve_service_send] (0x0020): No available servers for service 'IPA'
    [be[IPA.PB]] [be_resolve_server_done] (0x1000): Server resolution failed: [5]: Input/output error
    [be[IPA.PB]] [sdap_id_op_connect_done] (0x0020): Failed to connect, going offline (5 [Input/output error])
    [be[IPA.PB]] [be_mark_offline] (0x2000): Going offline!

Discovered subdomains
*********************

If the uses comes from a subdomain, it is good to know what subdomains
(trusted domains in IPA and AD terminology) were discovered and how they relate
to each other.

- Search for the following debug message to see what subdomains were discovered.

.. code-block:: sssd-log

    [be[IPA.PB]] [new_subdomain] (0x0400): Creating [ad.pb] as subdomain of [IPA.PB]!
    [be[IPA.PB]] [new_subdomain] (0x0400): Creating [child.ad.pb] as subdomain of [IPA.PB]!

LDAP operations
***************

We can see in the logs what LDAP operations were performed and how did they
finished and how many results were returned. If there is something unexpected
we can take the filter and search base and run a manual LDAP search to see if
the result match. If an LDAP operation fails and we are online it indicates
a problem on server (possible ACL issue).

.. code-block:: sssd-log

    # 1. What server are we connected to
    [be[IPA.PB]]  [sdap_print_server] (0x2000): Searching 10.34.78.100:389

    # 2. LDAP query with filter and search base
    [be[IPA.PB]]  [sdap_get_generic_ext_step] (0x0400): calling ldap_search_ext with [(&(objectClass=ipasudorule)(ipaEnabledFlag=TRUE)(|(!(memberHost=*))(hostCategory=ALL)(memberHost=fqdn=client.sssd.pb,cn=computers,cn=accounts,dc=ipa,dc=pb)(memberHost=cn=test-hg,cn=hostgroups,cn=accounts,dc=ipa,dc=pb)))][cn=sudo,dc=ipa,dc=pb].

    # 3. Requested attributes
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [objectClass]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [cn]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaUniqueID]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaEnabledFlag]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaSudoOpt]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaSudoRunAs]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaSudoRunAsGroup]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [memberAllowCmd]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [memberDenyCmd]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [memberHost]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [memberUser]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [sudoNotAfter]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [sudoNotBefore]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [sudoOrder]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [cmdCategory]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [hostCategory]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [userCategory]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaSudoRunAsUserCategory]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaSudoRunAsGroupCategory]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaSudoRunAsExtUser]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaSudoRunAsExtGroup]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaSudoRunAsExtUserGroup]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [externalUser]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [entryUSN]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x2000): ldap_search_ext called, msgid = 11
    [be[IPA.PB]] [sdap_op_add] (0x2000): New operation 11 timeout 6

    # 4. We process attributes of each object
    [be[IPA.PB]] [sdap_parse_entry] (0x1000): OriginalDN: [ipaUniqueID=ea0116a4-d262-11e6-8cd7-001a4a2312a7,cn=sudorules,cn=sudo,dc=ipa,dc=pb].
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [objectClass]
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [cn]
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [ipaUniqueID]
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [ipaEnabledFlag]
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [memberAllowCmd]
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [memberUser]
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [hostCategory]
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [ipaSudoRunAsUserCategory]
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [ipaSudoRunAsGroupCategory]
    [be[IPA.PB]] [sdap_parse_range] (0x2000): No sub-attributes for [entryUSN]

Authentication
**************

If authentication fail it is usually due to invalid or expired credentials.
It may also involve possible ``clock`` skew if using Kerberos when client’s
time differs from the KDC time. We log each phase of PAM authentication as
a separate data provider requests so we can get the exact phase that fails.

- We print input data for each phase. The following example shows successful
  authentication phase.

.. code-block:: sssd-log

    [be[IPA.PB]] [dp_pam_handler] (0x0100): Got request with the following data
    [be[IPA.PB]] [pam_print_data] (0x0100): command: SSS_PAM_AUTHENTICATE
    [be[IPA.PB]] [pam_print_data] (0x0100): domain: IPA.PB
    [be[IPA.PB]] [pam_print_data] (0x0100): user: admin@ipa.pb
    [be[IPA.PB]] [pam_print_data] (0x0100): service: su
    [be[IPA.PB]] [pam_print_data] (0x0100): tty: pts/1
    [be[IPA.PB]] [pam_print_data] (0x0100): ruser: pbrezina
    [be[IPA.PB]] [pam_print_data] (0x0100): rhost:
    [be[IPA.PB]] [pam_print_data] (0x0100): authtok type: 1
    [be[IPA.PB]] [pam_print_data] (0x0100): newauthtok type: 0
    [be[IPA.PB]] [pam] [pam_print_data] (0x0100): priv: 0
    [be[IPA.PB]] [pam_print_data] (0x0100): cli_pid: 29865
    [be[IPA.PB]] [pam_print_data] (0x0100): logon name: not set
    [be[IPA.PB]] [dp_attach_req] (0x0400): DP Request [PAM Authenticate #4]: New request. Flags [0000].
    ...
    [be[IPA.PB]] [dp_req_done] (0x0400): DP Request [PAM Authenticate #4]: Request handler finished [0]: Success
    [be[IPA.PB]] [_dp_req_recv] (0x0400): DP Request [PAM Authenticate #4]: Receiving request data.
    [be[IPA.PB]] [dp_req_destructor] (0x0400): DP Request [PAM Authenticate #4]: Request removed.
    [be[IPA.PB]] [dp_req_destructor] (0x0400): Number of active DP request: 0
    [be[IPA.PB]] [dp_pam_reply] (0x1000): DP Request [PAM Authenticate #4]: Sending result [0][IPA.PB]

- If communication with the remote server goes well, we always return success,
  however the PAM result is logged in the ``dp_pam_reply`` function:
  ``Sending result [0][IPA.PB]``. Value ``0`` means success, other values
  indicate problem, such as 17 which indicates invalid credentials.
  You can get the list of PAM status code and its meaning
  `here <http://pubs.opengroup.org/onlinepubs/8329799/chap5.htm#tagcjh_06_02_01>`_.

.. code-block:: sssd-log

    [be[IPA.PB]] [dp_pam_reply] (0x1000): DP Request [PAM Authenticate #4]: Sending result [17][IPA.PB]

- If you are unable to find any debug messages regarding to authentication,
  it is probably due to missing ``pam_sss`` in PAM configuration
  (for example in ``/etc/pam.d/system-auth``).

Access control
**************

If there is any access provider other than ``permit`` configured we may also find
out why the user access is denied (or the other way around, permitted).
This may indicate wrong host base access control configuration on IPA or
that the user account has expired, etc.

Access control is part of ``Account Management PAM Phase`` and
``PAM Account Request`` (for ipa provider also PAM SELinux Request,
thus to see where the access check begin look for the following messages:

.. code-block:: sssd-log

    [be[IPA.PB]] [dp_pam_handler] (0x0100): Got request with the following data
    [be[IPA.PB]] [pam_print_data] (0x0100): command: SSS_PAM_ACCT_MGMT
    ...
    [be[IPA.PB]] [dp_attach_req] (0x0400): DP Request [PAM Account #4]: New request. Flags [0000].
    ...
    [be[IPA.PB]] [dp_attach_req] (0x0400): DP Request [PAM SELinux #5]: New request. Flags [0000].

Which rules apply on the account check depends heavily on configuration of
``access_provider``. This provider is set to ``permit`` by default, which means
that all users can access. Please refer to SSSD manual page to see what
providers can be set. We use ``ipa`` provider in this example that involves
two checks in addition to LDAP policy: 1) Host Base Access Control (HBAC) and 2)
SELinux policy.

- Example of access granted. Notice that we return ``0`` in ``dp_pam_reply``:

.. code-block:: sssd-log

    [be[IPA.PB]] [dp_attach_req] (0x0400): DP Request [PAM Account #4]: New request. Flags [0000].
    ...
    [be[IPA.PB]] [hbac_evaluate] (0x0100): ALLOWED by rule [allow_all].
    [be[IPA.PB]] [hbac_evaluate] (0x0100): hbac_evaluate() >]
    [be[IPA.PB]] [ipa_hbac_evaluate_rules] (0x0080): Access granted by HBAC rule [allow_all]
    [be[IPA.PB]] [dp_req_done] (0x0400): DP Request [PAM Account #4]: Request handler finished [0]: Success
    [be[IPA.PB]] [_dp_req_recv] (0x0400): DP Request [PAM Account #4]: Receiving request data.
    [be[IPA.PB]] [dp_req_destructor] (0x0400): DP Request [PAM Account #4]: Request removed.
    [be[IPA.PB]] [dp_req_destructor] (0x0400): Number of active DP request: 0
    [be[IPA.PB]] [dp_attach_req] (0x0400): DP Request [PAM SELinux #5]: New request. Flags [0000].
    [be[IPA.PB]] [dp_attach_req] (0x0400): Number of active DP request: 1
    ...
    [be[IPA.PB]] [dp_req_done] (0x0400): DP Request [PAM SELinux #5]: Request handler finished [0]: Success
    [be[IPA.PB]] [_dp_req_recv] (0x0400): DP Request [PAM SELinux #5]: Receiving request data.
    [be[IPA.PB]] [dp_req_destructor] (0x0400): DP Request [PAM SELinux #5]: Request removed.
    [be[IPA.PB]] [dp_req_destructor] (0x0400): Number of active DP request: 0
    [be[IPA.PB]] [dp_pam_reply] (0x1000): DP Request [PAM Account #4]: Sending result [0][IPA.PB]

- Example of access denied due to missing HBAC rules (notice number
  ``6`` in ``dp_pam_reply``:

.. code-block:: sssd-log

    [be[IPA.PB]] [ipa_hbac_rule_info_done] (0x0080): No rules apply to this host
    [be[IPA.PB]] [ipa_pam_access_handler_done] (0x0020): No HBAC rules find, denying access
    [be[IPA.PB]] [dp_req_done] (0x0400): DP Request [PAM Account #5]: Request handler finished [0]: Success
    [be[IPA.PB]] [_dp_req_recv] (0x0400): DP Request [PAM Account #5]: Receiving request data.
    [be[IPA.PB]] [dp_req_destructor] (0x0400): DP Request [PAM Account #5]: Request removed.
    [be[IPA.PB]] [dp_req_destructor] (0x0400): Number of active DP request: 0
    [be[IPA.PB]] [dp_pam_reply] (0x1000): DP Request [PAM Account #5]: Sending result [6][IPA.PB]

- If you are unable to find any debug messages regarding to access control,
  it is probably due to missing ``pam_sss`` in PAM configuration
  (for example in ``/etc/pam.d/system-auth``).

Timeouts
********

Many SSSD operations have default timeouts set, often the timeouts are configurable
and can be found in the provider backend or sssd.conf man pages. Sample log
output below shows SSSD failing a search operation due to timeout.

.. code-block:: sssd-log

    [be[IPA.PB]] [sdap_op_timeout] (0x1000): Issuing timeout for 11
    [be[IPA.PB]] [sdap_op_destructor] (0x1000): Abandoning operation 11
    [be[IPA.PB]] [generic_ext_search_handler] (0x0040): sdap_get_generic_ext_recv failed [110]: Connection timed out

The actual SSSD operation which timed out may not be in the same section of the
log and requires searching earlier in the logs. We can search the logs for the
operation number(11 in the above logs) such as ``msgid = 11``.

.. code-block:: sssd-log

    [be[IPA.PB]] [sdap_print_server] (0x2000): Searching 10.34.78.100:389
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x0400): calling ldap_search_ext with [(&(cn=sudo-test)(|(objectClass=ipaUserGroup)(objectClass=posixGroup))(cn=*)(&(gidNumber=*)(!(gidNumber=0))))][cn=accounts,dc=idm,dc=example,dc=com].
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [objectClass]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [posixGroup]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [cn]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [userPassword]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [gidNumber]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [member]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaUniqueID]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaNTSecurityIdentifier]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [modifyTimestamp]
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [entryUSN]
    [be[IPA.PB]] [sssd[be[example.com]]] [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [ipaExternalMember]
    [be[IPA.PB]] [sssd[be[example.com]]] [sdap_get_generic_ext_step] (0x2000): ldap_search_ext called, msgid = 11
    [be[IPA.PB]] [sssd[be[example.com]]] [sdap_op_add] (0x2000): New operation 11 timeout 30

Note the last line contains the operation number and timeout value. The 30 second
timeout matches up with the log message where the timeout was triggered.

Performing manual LDAP query
****************************

It is often useful to run the same query as SSSD manually with ``ldapsearch`` tool.
Look for function named ``sdap_get_generic_ext_step`` to aquire the search base
and filter that SSSD used against an LDAP server and ``sdap_print_server`` to see
what server did it connect to. The messages are in form of:

.. code-block:: sssd-log

    [be[IPA.PB]] [sdap_print_server] (0x2000): Searching $ip:$port
    [be[IPA.PB]] [sdap_get_generic_ext_step] (0x0400): calling ldap_search_ext with [$filter][$search-base]

- Anonymous bind (no authentication)

.. code-block:: bash

    ldapsearch -x -H ldap://$ip:$port -b $search-base '$filter'

- Simple bind (authentication with credentials)

.. code-block:: bash

    ldapsearch -x -D "cn=Directory Manager" -w "$password" -H ldap://$ip:$port -b $search-base '$filter'

- GSSAPI (authentication through Kerberos)

.. code-block:: bash

    klist -k
    kinit -k '$principal'
    ldapsearch -Y GSSAPI -H ldap://$ip:$port -b $search-base '$filter'

Asking for help
***************

If you did not have any luck with debugging the issue yourself you can reach us
through `sssd-users <https://fedorahosted.org/mailman/listinfo/sssd-users>`_
mailing list or `#sssd channel on libera.chat <irc://irc.libera.chat/sssd>`_ IRC.

It would be great if you can also provide all the information that you have
found so far to speed things up. Such as:

- Description of the issue

- What do you expect that should happen

- What did you see in the logs

- All SSSD logs with debug level set to ``0x3ff0`` (please always ``include whole
  log files``, not only snippets)

- Version of SSSD an what server do you use

- Other information depending on the area of investigation

  - expected group membership

  - domains relationships

  - HBAC rules

  - Other access control settings

  - And everything that comes to your mind that you think may be helpful
