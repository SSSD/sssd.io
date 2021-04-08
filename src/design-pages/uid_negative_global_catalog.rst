.. highlight:: none

Using the Global Catalog to speed up lookups by ID
==================================================

Related ticket(s):
------------------
     https://pagure.io/SSSD/sssd/issue/3468

Problem statement
-----------------
When SSSD is connected to a forest with multiple domains, each lookup,
unless qualified with the domain name, iterates over all the domains.
Moreover, some lookups, such as by-ID cannot be qualified using the
NSS interface at all.

This means the SSSD will issue N LDAP searches for N domains. If
the object SSSD is searching for exists in the LDAP database in one of the
domains, the performance impact can be mitigated with the already existing
option ``cache_first``, which will, even for non-qualified searches, first
check if the requested object exists in the local database and if it does,
searches the corresponding domain only.

But this option doesn't solve the problem of looking for objects, especially
numerical IDs, that do not exist in the remote database at all. A search for
such non-existent object will always traverse all the domains every time the
negative cache from a previous request expires.

In environments that use the Global Catalog, this issue can be mitigated
by locating the object's domain in the Global Catalog, provided that the
search key is present in the Global Catalog in the first place.

Use-cases
---------
Currently the primary use-case is SSSD joined to an AD forest consisting of
multiple domains and configured with ``id_provider=ad``, because only the AD
provider supports Global Catalog lookups. There are some plans to implement
the Global Catalog e.g. for FreeIPA, but so far no implementation exists.

At the same time, only environment that use POSIX UID and GID attributes set
by the administrator will benefit from this enhancement, becase if the client
maps the IDs algorithmically from the SIDs, the AD provider is already able
to shortcut the by-ID request after computing the SID from the requested
ID and realizing that the domain SID does not come from the current domain.

The current state of Global Catalog support in SSSD
---------------------------------------------------
The Global Catalog is an LDAP database, which contains a subset of attributes
about objects from all the domains in the whole forest. What attributes
are replicated to the Global Catalog is defined by the `Partial Attribute Set <https://social.technet.microsoft.com/wiki/contents/articles/23097.active-directory-attributes-in-the-partial-attribute-set.aspx>`_.
It is possible to query for the attributes
that are replicated to the Global Catalog using an LDAP query based in
the ``cn=schema,cn=configuration`` subtree and check for the presence of
``isMemberOfPartialAttributeSet=TRUE``, for example::

    ldapsearch -Y GSSAPI \
               -H ldap://dc.win.trust.test:389 \
               -b cn=schema,cn=configuration,dc=win,dc=trust,dc=test \
               '(&(objectClass=attributeSchema)(isMemberOfPartialAttributeSet=TRUE))'

It is important to note that because the POSIX attributes such as
``uidNumber`` or ``gidNumber`` are neither part of the default Active
Directory schema, nor replicated to the Global Catalog by default.
To learn how to extend the schema to set the POSIX attributes at all,
follow the `Install Identity Management for UNIX Components <https://technet.microsoft.com/en-us/library/cc731178.aspx>`_
article on the Microsoft TechNet site. How to extend the Partial Attribute Set
is described for example in the `AD DS: Global Catalogs and the Partial Attribute Set <https://blogs.technet.microsoft.com/scotts-it-blog/2015/02/28/ad-ds-global-catalogs-and-the-partial-attribute-set/>`_
TechNet blog post.

The purpose of using the Global Catalog in SSSD is two-fold:

 * to avoid having to connect to the LDAP server of a DC from every domain in the forest

 * to look up the cross-domain members of Universal Groups, which are only present in the Global Catalog

Because not all the attributes required by SSSD are guaranteed to be
replicated to the Global Catalog (especially the ``uidNumber`` and
``gidNumber`` attributes), SSSD runs a search that checks for
the presence of any objects with either ``uidNumber`` or ``gidNumber``
during the very first request for a numerical ID. If no objects with
either attribute are present, the Global Catalog support is disabled
except for looking up Universal Group members.

However, at the moment, SSSD will either use whole entry it finds in
the Global Catalog or not use the Global Catalog at all. This puts
a bit of responsibility on the administrator in the sense that the
object in the Global Catalog must contain all the required entries or
the administrator might need to disable the Global Catalog support
manually in the configuration file.  In the future (see e.g. ticket
`3538 RFE: Use the global catalog only to look up the entry DN
<https://pagure.io/SSSD/sssd/issue/3538>`_) we would like to change the
logic so that it uses the Global Catalog to look up the entry DN, but
then it would look up the entry attributes in the LDAP directory of the
object's domain. However, that enhancement is out of scope of what this
design page describes.

Overview of the solution
------------------------
A new Data Provider method ``getAccountDomain()`` whose purpose is to locate
a domain an object resides in will be added. At the moment, only the AD
provider will implement this handler.

The responder's ``cache_req`` module will call this handler before iterating
over domains. For all domains except the one returned from the handler,
the ``cache_req`` module will set the requested object into negative cache.
This would cause the subsequent loops over the domains to just skip the
domains where the entry was not found and only look up the entry in the
domain that the ``getAccountDomain()`` method returned.

Implementation details
----------------------
There are two parts to the implementation - the responder side, which mostly
touches the ``cache_req`` code and the provider side. The responder side
would also require adding some API to the negative cache module.

Responder changes - cache_req and negative cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
On the responder side, the ability to locate a domain of a requested object
will be provided by new ``cache_req`` plugin methods. Not all plugins will
be augmented with the methods that call the domain locator - at least in
the first iteration, only the plugins that search objects by ID will use
the new Data Provider API.

When looking up an entry, the ``cache_req`` request must first decide
whether it is worth calling the domain locator request at all. The locator
request should only be called when there are multiple domains to search
and the request is not already qualified with a domain name. Similarly,
the domain locator should not be called if the request is only evaluating
the cached data (``bypass_dp=True``, which is typically set during the
first pass when the ``cache_first`` option is enabled). Of course, the
locator would also only be called for plugins that implement the associated
methods.

When all the above evaluates into calling the locator (e.g. searching
a user UID while multiple domains are defined), the first step before
actually calling the locator DP method should still be looking into the
cache. This additional step ensures that looking up an ID from the first
defined domain in a setup with many domains wouldn't needlessly hit the
Global Catalog, while the entry is still cached in sysdb.

Finally, the responder would call the ``getAccountDomain`` Data Provider
method. If calling the DP method returns an error, this error is in no way
fatal, but instead, the ``cache_req`` code resumes the original codepath
where all domains are searched sequentially. One error code that signifies
that the back end as a whole doesn't support locating ID's domain must be
added. When the ``cache_req`` code would receive this error code, it
would never call the domain locator again for this domain.

On returning success from the ``getAccountDomain`` method, the string
returned from the method will contain the domain where the ID was found.
Only one domain can be returned, conflicting values in the ID space will
be detected on the provider side and handled by returning an error, which
will fall back to the sequential lookups.

The returned domain name will be used to set a negative cache entry for
the looked up object in all domains except the one that was returned.
It is important to only mark (sub)domains that belong to the same "main"
domain with these negative cache entries, especially because internally
in the ``cache_req`` code, we use a flattened domain list to iterate over
in order to support custom domain lookup priorities. After this is done,
the ``cache_req`` code would loop back into its original logic, but the
negative cache entries will ensure that domains that do not contain this
ID are skipped.

Because the loop over domains is resumed only after the locator was called,
there needs to be a way to avoid calling the locator too often. To this end,
a new negative cache container would be added. Under this container, we will
store the values of the objects we look up to notify the ``cache_req`` code
that either the locator must be called again or that calling the locator
can be skipped this time and the per-domain-per-ID negative cache entries
can be reused again during the loop over domains.

Provider changes - the ``getAccountDomain`` implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All providers except ``id_provider=ad`` will set a dummy ``getAccountDomain``
handler which always returns ``ERR_GET_ACCT_DOM_NOT_SUPPORTED``. Therefore,
for all domains except the ones with the AD provider, the
``getAccountDomain`` method will only be called once and then disabled.

The AD provider implementation of the ``getAccountDomain`` method will
search the Global Catalog with an empty search base, thus searching across
all the domains in the forest. Two details are important to bring up with
respect to this search:

    * In order for this lookup to be useful even for non-existant IDs,
      the Global Catalog search must be "authoritative". In other words,
      not finding the entry in the Global Catalog must be considered as if
      the entry doesn't exist.

    * Because the POSIX IDs are not replicated by default to the Global
      Catalog, the ``getAccountDomain`` request must check if any POSIX
      IDs at all are replicated to the Global Catalog at all.


Configuration changes
---------------------
None. However, it should be noted that disabling the Global Catalog support
as a whole in SSSD would disable the ``getAccountDomain`` in the sense that
it would always return ``ERR_GET_ACCT_DOM_NOT_SUPPORTED`` which would in turn
instruct the responder to never call the ``getAccountDomain`` request again

Therefore, disabling the Global Catalog can be used to disable this
new functionality.

How To Test
-----------
To test the functionality itself, an AD forest with multiple domains should
be used. Please make sure the POSIX attributes are present and replicated
to the Global Catalog. Requesting a POSIX ID from domain outside the joined
one should first consult the Global Catalog and then proceed to only searching
the individual domain where the ID was located.

It is important to test that there are no regressions in setups that either
do not use POSIX IDs at all or do not replicate the POSIX IDs to the Global
Catalog. In these setups, as well as configurations that use a different ID
provider, the ``cache_req`` code must only attempt to call the locator once.

Similarly, setups that use multiple domains (and remember that since
Fedora-26, all SSSD installations automatically enable the ``files``
provider) must see no regressions.

Authors
-------
 * Jakub Hrozek ``<jhrozek@redhat.com>``
