IPA Server Mode
---------------

Related tickets:

-  `RFE Allow using UIDs and GIDs from AD in trust
   case <https://pagure.io/SSSD/sssd/issue/1821>`__
-  `RFE Determine how to map SID to UID/GID based on IdM server
   configuration <https://pagure.io/SSSD/sssd/issue/1881>`__
-  more to come

Problem Statement
~~~~~~~~~~~~~~~~~

FreeIPA is planning to make users and groups from trusted domains
available to legacy systems, e.g. systems where only nss\_ldap and
pam\_ldap are available. For this a new directory server plugin
(`https://pagure.io/freeipa/issue/3567 <https://pagure.io/freeipa/issue/3567>`__)
will accept the LDAP search request from the legacy systems for the
trusted users and groups, resolve the requested objects and send the
result back to the legacy client.

Since all trusted users and groups are resolvable on the IPA server via
the SSSD IPA provider the idea is that the new plugin will just run
getpwnam\_r(), getgrnam\_r() and related calls. The SSSD disk and memory
cache will help to answer those request fast without the need of
additional caching inside the directory server.

To offer reliable group lookups to legacy systems it must be possible to
lookup all the members of a group from a trusted domain and not only
show members which already logged in once on the FreeIPA server, which
is the current status on IPA clients with a recent version of SSSD.
Additionally legacy systems tend to rely on user and group enumerations.
Both requirements force an enumeration and caching of all trusted users
and groups on the FreeIPA server.

If the legacy systems used an algorithmic mapping scheme based on the
RID of the AD object and an offset to find a POSIX ID for the trusted
user or group the *--base-id* of the *ipa trust-add* command can be used
to get the same ID mapping. For legacy systems which read the POSIX IDs
directly from AD a new idrange type must be introduced on the FreeIPA
server
(`https://pagure.io/freeipa/issue/3647 <https://pagure.io/freeipa/issue/3647>`__)
to indicate that for those trusted users an groups the POSIX ID must be
read from AD.

All of the above can basically be solved with the current layout of the
FreeIPA server where winbind is doing the lookups against AD and SSSD is
using the extdom LDAP plugin to read this data via the directory server.
But it was decided to enhance SSSD to do the lookup. Some of the reasons
are:

-  resources, since SSSD has to run anyway on the FreeIPA server and is
   capable of the AD user and group lookups, winbind does not have to
   run anymore
-  avoid double caching, to work efficiently winbind has to do some
   caching on its own and as a result users and groups are cached twice
   on the FreeIPA server
-  configuration, winbind uses a separate configuration file while the
   IPA provider of SSSD can read e.g. the idranges directly from the
   FreeIPA server, this minimized to configuration effort and avoids
   conflicting configuration of different components

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

First sssd needs to know that it is running on an IPA server and should
not look up trusted users and groups with the help of the extdom plugin
but do the lookups on its own. For this a new boolean configuration
option, e.g. ipa\_server\_mode, should be introduced (SSSD ticket
`#1993 <https://pagure.io/SSSD/sssd/issue/1993>`__) which defaults to
*false* but is set to *true* during ipa-server-install or during updates
of the FreeIPA server
(`https://pagure.io/freeipa/issue/3652 <https://pagure.io/freeipa/issue/3652>`__)
if it is not already set.

Since AD by default requires an authenticate LDAP bind to do searches
SSSD needs credentials which are accepted by a trusted AD server.
Because if the trust relationship this can even be credentials from the
FreeIPA domain if Kerberos is user for authentication. So the easiest
way is just to use the local keytab which requires no changes on the
SSSD side, because the generic LDAP provider already knows how to handle
SASL bind with the local keytab. But currently AD LDAP server does not
accept the Kerberos ticket from a FreeIPA host, because the FreeIPA KDC
does not attach a PAC to the TGTs of host/ principals
(`https://pagure.io/freeipa/issue/3651 <https://pagure.io/freeipa/issue/3651>`__,
until this is fixed some dummy credentials, e.g. a keytab for a dummy
user, can be used).

Now the AD provider code can be used to lookup up the users and group of
the trusted AD domain. Only the ID-mapping logic should be refactored so
that the same code can be used in the standalone AD provider where the
configuration is read from sssd.conf and as part of the IPA provider
where the idrange objects read from the IPA server dictates the mapping.
Maybe libsss\_idmap can be extended to handle idranges for mappings in
AD as well, e.g. a specific error code can be used to indicate to the
caller that for this domain no algorithmic mapping is available and the
value from the corresponding AD attribute should be use (**SSSD
ticket?**).

A task (or a separate process) must be created to handle enumerations
efficiently without having to much impact on parallel running requests
(**SSSD ticket#**). Maybe we can find a scheme which allows to read only
a limited (configurable) number of users with their group memberships at
a time. This way the cache might not be complete at once but always
consistent with respect to group memberships of the caches users. If
eventually all users are read, the task will periodically look for new
users and update old entries.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

Add ipa\_server\_mode option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A new boolean option ipa\_server\_mode which defaults to false should be
added to the IPA provider. ipa\_get\_subdom\_acct\_send() should only be
called if ipa\_server\_mode is false. If ipa\_server\_mode is true
ipa\_account\_info\_handler() should return ENOSYS for subdomain
requests. A suitable tevent request will be handled in a different
ticket.

Enhance libsss\_idmap
^^^^^^^^^^^^^^^^^^^^^

#. Allow algorithmic mapping where the first RID is not 0 Currently it
   is implicitly assumed that the first POSIX ID of a range is mapped to
   the RID 0. To support multiple ranges for a single domain a different
   first RID must handled as well.
   Ticket: `#1938 <https://pagure.io/SSSD/sssd/issue/1938>`__
#. Add a range type to handle mappings in AD The idea is that ranges for
   IDs from AD can be used in libsss\_idmap as well, but whenever a
   mapping is requested for this range a specific error code like
   IDMAP\_ASK\_AD\_FOR\_MAPPING is returned to tell SSSD to do an AD
   lookup. This way SSSD does not need to inspect the ranges itself but
   all is done inside if libsss\_idmap. Additionally a new call is
   needed to check whether the returned externally managed ID belongs to
   a configured range, if not the ID cannot be mapped in the given
   configuration and the related object should be ignored.
   Ticket: `#1960 <https://pagure.io/SSSD/sssd/issue/1960>`__
#. Add an optional unique range identifier To be able to detect
   configuration changes in idranges managed by FreeIPA an identifier
   should be stored on the client together with the other idrange
   related data. For simplicity the DN of the related LDAP object on the
   FreeIPA server can be used here. The identifier should be optional,
   but if it is missing the range cannot be updated or deleted at
   runtime.
#. Allow updates and removal of ranges To support configuration changes
   at runtime, it must be possible to update and remove ranges. As a
   first step I would recommend that the changes will only affect new
   requests and not the cached data, because in general changes to
   centrally manages ranges should be done with care to avoid conflicts.
   In a later release we can decided if we just want to invalidate all
   cached entries of the domain which idrange was modified or if a
   smarter check is needed to invalidate only objects which are affected
   by the change.

Add plugin to LDAP provider to find new ranges
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently the range management code is in the generic LDAP provider and
can be used by the LDAP and AD provider. New ranges are allocated with
the help of a hash value of the domain SID.

If the IPA provider cannot find a range for a given domain it cannot
allocate a new range on its own but has to look up the idrange objects
on the FreeIPA server and use them accordingly. To allow the LDAP, AD
and IPA provider to use as much common code as possible I think a plugin
interface, similar to the one used to find the DNS site, to find a
missing range would be useful. The default plugin will be used by the
LDAP and the AD provider and the IPA provider will implement a plugin to
read the data from the server.

Remove assumption that subdomain users always have a primary user-private-group (UPG)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently the PAC responder assumes that subdomain users always have a
UPG as primary group. This will be only true for domains with
algorithmic mappings because here the POSIX IDs are managed by the
FreeIPA server and we are free to choose. But if the POSIX IDs are
manged externally we have to use what we get from external sources. E.g.
in the case where the POSIX IDs are managed by AD UIDs and GIDs are
separate name spaces and assuming the UPGs can be used would most
certainly lead to GID conflicts. The PAC responder has to respect the
idrange type or the mpg flag of the sss\_domain\_info struct and act
accordingly.

Additional the code paths where new subdomains are created must be
reviewed and wherever the mpg flag is set code must be added so that it
is set according to the range type.

Although I think that the code path where an IPA client (i.e.
ipa\_server-mode = false) looks up a trusted domain user adds the user
to the cache with the data it receives from the extdom plugin, it should
be verified that UPGs are not implicitly assumed here as well.

Integrate AD provider lookup code into IPA subdomain user lookup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the ipa\_server\_mode is selected IPA subdomain user and group
lookups should not be done with the help of the extdom plugin but
directly against AD with the help of LDAP of GC lookups. For this the
IPA provider must be able to call the related functions from the AD
provider. Since by default the POSIX attributes are not replicated to
the global catalog and supporting them is a requirement, I think it
would be sufficient make sure LDAP lookups are working as expected.
Additionally FreeIPA currently supports only one trusted domain global
catalog lookups for users and groups from the forest or different
forests can be added later.

Since the Kerberos hosts keys from the host keytab should be used as
credentials to access AD no changes are expected here.

It should be taken care that not accidentally the the AD SRV plugin is
loaded, see next section as well.

Enhance IPA SRV plugin to do AD site lookups as well
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From the AD point of view trusted domains do not belong to a specific
site. But recent version of AD return the next\_closest\_site for host
which do not belong to a site. To make sure that SSSD is communication
with an AD server which is network-wise reasonably near it would be
useful if the IPA SRV plugin can be enhanced to do CLDAP pings and AD
site lookups as well. Additionally the plugin must know when to use IPA
style and when AD style lookups.

This is a nice to have feature.

Implement or Improve enumeration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If enumeration is enable SSSD tries to update all users and groups at
startup. As a result the startup time where SSSD is basically blocked
and cannot serve requests even for data in the cache can be quite long.
A new tevent\_req task should be created which can read users and groups
from the AD domain in smaller chunks so that other request can always
slip in between. Ticket
`#1829 <https://pagure.io/SSSD/sssd/issue/1829>`__ contains a similar
request for the general use in SSSD. If we find a good scheme here, it
might be used for the general enumerations as well.

The task should make sure all users and groups are read after a while
without reading objects twice in a single run. Maybe it is possible to
add a special paged-search tevent request which returns after the first
page is read to the caller (instead of doing the paging behind the
scenes) which the results and a handle which would allow to continue the
the search with the next page? If this is a way to go creating this new
request would be another development subtask.

Additionally it has to be considered how to handle large groups. But
since we have to read all user as well it might be possible to just read
the group memberships of the user and build up the groups in the SSSD
cache and let the getgrp\*() calls only return entries from the cache
and never go to the server directly.

This new enumeration task will work independently of the NSS responder
in the IPA provider. It should be started at startup but should
terminate if there are no trusted domains. If later during a sub-domain
lookup trusted domains are found it should be started again.

How to test
~~~~~~~~~~~

If the ipa\_server\_mode is enable on a FreeIPA server which trusts an
AD server, *getent passwd AD\\username* or *id AD\\username* should
return the expected results for users and groups.

*getent group AD\\groupname* should return results depending the state
of enumeration. Immediately after startup with an empty cache e.g. the
'Domain User' group should only have a few members if any. After some
time more and more members should be displayed until the enumeration is
complete and all users and groups are in the SSSD cache.

Author(s)
~~~~~~~~~

Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
