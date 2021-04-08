.. highlight:: none

Use Active Directory's DNS sites
================================

Related ticket(s):

-  `RFE sssd should support DNS
   sites <https://pagure.io/SSSD/sssd/issue/1032>`__

Problem Statement
-----------------

In larger Active Directory environments there is typically more than one
domain controller. Some of them are used for redundancy, others to build
different administrative domains. But in environments with multiple
physical locations each location often has at least one local domain
controller to reduce latency and network load between the locations.

Now clients have to find the local or nearest domain controller. For
this the concept of sites was introduce where each physical location can
be seen as an individual site with a unique name. The naming scheme for
DNS service records was extended (see e.g.
`http://technet.microsoft.com/en-us/library/cc759550(v=ws.10).aspx <http://technet.microsoft.com/en-us/library/cc759550(v=ws.10).aspx>`__)
so that clients can first try to find the needed service in the local
site and can fall back to look in the whole domain if there is no local
service available.

Additionally clients have to find out about which site they belong to.
This must be done dynamically because clients might move from one
location to a different one on regular basis (roaming users). For this a
special LDAP request, the (C)LDAP ping
(`http://msdn.microsoft.com/en-us/library/cc223811.aspx <http://msdn.microsoft.com/en-us/library/cc223811.aspx>`__),
was introduced.

Overview view of the solution
-----------------------------

General considerations
^^^^^^^^^^^^^^^^^^^^^^

The solution in SSSD should take into account that other types of
domains, e.g. a FreeIPA domain, want to implement their own scheme to
discover the nearest service of a certain type. A plugin interface where
the configured ID provider can implement methods to determine the
location of the client looks like the most flexible solution here.

Since the currently available (AD sites) or discussed schemes
(`http://www.freeipa.org/page/V3/DNS\_Location\_Mechanism <http://www.freeipa.org/page/V3/DNS_Location_Mechanism>`__)
use DNS SRV lookups the plugin will be called in this code path. Since
network lookups will be needed the plugin interface must allow
asynchronous operations. SSSD prefers the tevent\_req style for
asynchronous operations where the plugin has to provide a \*\_send and a
\*\_recv method. Besides a list of server names which will be handled as
primary servers, like the servers currently returned by DNS SRV lookups,
the \*\_recv method can additionally return a list of fallback servers
to make full use of the current fallback infrastructure on SSSD.

Sites specific details
^^^^^^^^^^^^^^^^^^^^^^

The plugin of the AD provider will do the following steps:

#. do a DNS lookup to find any DC
#. send a CLDAP ping to the first DC returned to get the client's site
#. after a timeout send a CLDAP ping to the next DC on the list
#. if after an overall timeout no response is received the CLDAP lookups
   will be terminated and the client's site is unknown
#. if the clients site is known a DNS SRV
   \_service.\_protocol.site-name.\_sites.domain.name for primary server
   and \_service.\_protocol.domain.name for backup server is send,
   otherwise only one with \_service.\_protocol.domain.name is done
#. if primary and backup server lists are available all primary servers
   are removed from the backup list

The results of the different step should be available with one of the
debug levels reserved for tracing to make debugging easier and to allow
acceptance tests to validate the behavior with the help of the debug
logs.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

struct resolv\_ctx should get 3 new members, two function pointer to
hold the \*\_send and \*\_recv method of the plugin and a pointer to
private data for the plugin. Since most of the structs related to the
fail-over and resolver code are private a setter method to add the
pointers should be added as well. This is more flexible than adding
additional arguments to resolv\_init().

Besides the the service type and protocol and domain, which are all
available in struct srv\_data, the plugin should get a tevent context
and its private data as arguments. With this the plugin interface might
look like: ::

    typedef struct tevent_req *(*location_plugin_send_t)(TALLOC_CTX *mem_ctx, struct tevent_context *ev, const char *service, const char *protocol, const char *domain, void *private_data);
    typedef int (*location_plugin_recv_t)(TALLOC_CTX *mem_ctx, struct tevent_req *req, int *status, int *timeouts, struct ares_srv_reply **primary_reply_list, struct ares_srv_reply **backup_reply_list);

If a plugin is defined it can then be called in resolve\_srv\_cont()
instead of get\_srv\_query(). If it is not defined either the result of
get\_srv\_query() can be used or a default request with the same
interface as the plugin can be used. I think the latter one would make
the code flow more easy to follow.

Additionally, if s backup server list is returned the results must be
added to the server list in resolve\_srv\_done().

Finding a DC for the CLDAP ping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To find any DC in the domain samba look for a \_ldap.\_tcp.domain.name.
I would suggest to use \_ldap.\_tcp.domain.name as well for the SSSD
implementation.

Sending the CLDAP ping
^^^^^^^^^^^^^^^^^^^^^^

The CLDAP ping is a LDAP search request with a filter like ::

    (&(&(DnsDomain=ad.domain)(DomainSid=S-1-5-21-1111-2222-3333))(NtVer=0x01000016))

and the attribute "NetLogon". The flags given with the NtVer component
of the search filter will be different for a domain member (AD provider)
and an IPA server in an environment with trusts (IPA provider).

A domain member will belong to a site and the following flags from
/usr/include/samba-4.0/gen\_ndr/nbt.h should be used
'NETLOGON\_NT\_VERSION\_5 \| NETLOGON\_NT\_VERSION\_5EX \|
NETLOGON\_NT\_VERSION\_IP'. A trusted server does not belong to one of
the sites of trusting domain so it can only ask for the closest site
with 'NETLOGON\_NT\_VERSION\_5 \| NETLOGON\_NT\_VERSION\_5EX \|
NETLOGON\_NT\_VERSION\_WITH\_CLOSEST\_SITE'. Maybe
NETLOGON\_NT\_VERSION\_WITH\_CLOSEST\_SITE is useful for a domain member
as well if e.g. the services on the local site are not available.

Parsing the server response
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The server response is a single attribute "NetLogon" which is a binary
blob containing multiple NDR encoded values. This value can be decoded
with ndr\_pull\_netlogon\_samlogon\_response() from the Samba library
libndr-nbt.

Side note about struct resolv\_ctx and the usage of resolv\_init()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In previous discussions it was said that resolv\_init() should be only
called once during the initialization of a provider, preferable from the
common responder code. This means that there is only one instance of the
resolv\_ctx for the whole provider.

Currently resolv\_init() is called at two other places as well, in
ipa\_dyndns.c and sdap\_async\_sudo\_hostinfo.c. I think the only reason
for calling resolv\_init() at those two place is, that both needed to
call some low level resolve routines which need a resolv\_ctx as
parameter and that there is no easy way to get the resolv\_ctx because
it is hidden in a private struct. Instead of adding an appropriate
getter method which returns the current resolve\_ctx resolv\_init() was
called for a second time.

If the resolv\_init() calls are removed from those two places with the
help of a getter method or similar, I think the prev and next members
can be removed from struct resolv\_ctx as well. Because there will not
be a list of resolver contexts, but only one.

How to test
-----------

If this feature is tested the following scenarios can be considered:

AD domain does only has a single site
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  site name might be 'Default-First-Site-Name' but it can be renamed or
   localized as well
-  SSSD should be able to discover the site, e.g.
   'Default-First-Site-Name'
-  SSSD should connect to any DC.

AD domain has sites but the local site of the SSSD client has no domain controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  SSSD should be able to discover the local site
-  SSSD should connect to a any DC

AD domain has sites and the local site of the SSSD client has a domain controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  SSSD should be able to discover the local site
-  SSSD should connect to a DC from the local site

Besides inspection the log files with a high debug level to connection
to the domain controller can also be verified with the netstat or ss
utilities.

Useful links
------------

-  `How DNS Support for Active Directory
   Works <http://technet.microsoft.com/en-us/library/cc759550(v=ws.10).aspx>`__
-  `LDAP
   Ping <http://msdn.microsoft.com/en-us/library/cc223811.aspx>`__
-  `Domain Controller Response to an LDAP
   Ping <http://msdn.microsoft.com/en-us/library/cc223813.aspx>`__
-  `NETLOGON\_NT\_VERSION Options
   Bits <http://msdn.microsoft.com/de-de/library/cc223801.aspx>`__

Author(s)
---------

Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
