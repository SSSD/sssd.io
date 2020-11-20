.. highlight:: none

Detecting POSIX attributes in Global Catalog using the Partial Attribute Set
============================================================================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/3755

Problem statement
-----------------
In some environments with SSSD clients joined directly to an Active Directory
realm, replicating POSIX attributes such as ``uidNumber``, ``gidNumber`` or
``unixHomeDirectory`` to the Global Catalog might provide a substantial
performance benefit. As an example, if the numerical IDs are replicated
to the Global Catalog, then the SSSD is able to locate the domain the ID
resides in without iterating over the other domains.

However, the POSIX attributes are not replicated by default, so the SSSD
must check whether the attributes are replicated or not. There was a
straightforward check in SSSD which just ran a lookup for any entry with
POSIX attributes since several versions ago. In large environments, though,
this check was very inefficient and causing a high load on the servers.

This design page describes a different method of detecting the POSIX
attributes by inspecting the AD schema instead.

Use cases
---------
An SSSD client joined to an Active Directory domain directly. The AD domain
must be using POSIX attributes for user and group IDs, the changes in this
design page are irrelevant for domains that use ID mapping.

Overview of the solution
------------------------
Instead of issuing a wide search for any object that contains the
``uidNumber`` or ``gidNumber`` attribute, the SSSD will consult the
`Partial Attribute Set <https://social.technet.microsoft.com/wiki/contents/articles/23097.active-directory-attributes-in-the-partial-attribute-set.aspx>`_
which defines what attributes are replicated to the Global Catalog.
Which attributes are members of the Partial Attribute Set is described below.

In general terms, all attributes in the Active Directory schema
are represented by objects with the objectclass  `attributeSchema
<https://docs.microsoft.com/en-us/windows/desktop/AD/characteristics-of-attributes>`_.

The ``attributeSchema`` objects as well as all objectclasses
are exposed through a subtree called the `Schema Naming Context
<https://docs.microsoft.com/en-us/windows/desktop/ad/naming-contexts-and-partitions>`_

The Schema Naming Context is exposed typically at the
``cn=schema,cn=configuration,$FOREST_BASE_DN`` subtree, but its location is most
portably read from the ``schemaNamingContext`` attribute of the rootDSE.
One important thing to note about the Schema Naming Context is that its
location is the same across all DCs in the forest.

Each attribute is represented as an object under the schema
subtree and whether the attribute is replicated into the Global
Catalog or not is denoted by the `isMemberOfPartialAttributeSet
<https://msdn.microsoft.com/en-us/library/cc221098.aspx>`_ attribute value.

This search in an example domain called ``win.trust.test`` might be issues with::

    ldapsearch -LLL -Y GSSAPI \
               -H ldap://dc.win.trust.test \
               -b cn=schema,cn=configuration,dc=win,dc=trust,dc=test \
               '(|(cn=uidNumber)(cn=gidNumber))' \
               isMemberOfPartialAttributeSet

And the result, this time showing that neither attribute was replicated to the Global Catalog might look like::

    dn: CN=GidNumber,CN=Schema,CN=Configuration,DC=win,DC=trust,DC=test
    isMemberOfPartialAttributeSet: FALSE

    dn: CN=UidNumber,CN=Schema,CN=Configuration,DC=win,DC=trust,DC=test
    isMemberOfPartialAttributeSet: FALSE

As said earlier, the Schema Naming Context is the same across all domains in
the forest, so the search against a DC in a child domain would work as well
even though it's also based at ``CN=Configuration,DC=win,DC=trust,DC=test``::

    ldapsearch -Y GSSAPI \
               -H ldap://childdc.child.win.trust.test \
               -b CN=Schema,CN=Configuration,DC=win,DC=trust,DC=test
               '(|(cn=uidNumber)(cn=gidNumber))' \
               isMemberOfPartialAttributeSet


Implementation details
----------------------
First, the rootDSE parsing code must be extended to read the
``schemaNamingContext`` attribute from the rootDSE object and store it in
the ``sdap_options`` structure.

The search itself will be issued in the subdomains provider. Placing the
search in the subdomains provider instead of the handlers or the searches
makes it possible to remove much of the previous code as the subdomains
provider request is guaranteed to be executed before any user or group
request except for cases where the subdomains provider is explicitly
disabled with ``subdomains_provider=none``, but in that case it makes
little sense to use the Global Catalog in the first place.

Because of the property of the schema partition being replicated to all
DCs in the forest, the search can always be run after the SSSD connects
to the joined domain which triggers reading the rootDSE.

If neither or only one of the attributes would be found, the Global Catalog
support will be disabled. The same would happen in the case that the check
fails with an error as the Global Catalog itself is not required for SSSD
to function at least in a degraded mode.

The search as described in the previous section would be issued using the
LDAP connection, in particular the connection to the joined domain. The
LDAP connection must be used because the ``isMemberOfPartialAttributeSet``
attribute is typically not replicated to the Global Catalog itself. 

The old request (``sdap_gc_posix_check_send``) can probably just be
completely removed.

Configuration changes
---------------------
None.

How To Test
-----------
With an AD client that uses ID mapping, the request should not be ran
at all. The same is true if the Global Catalog support is explicitly
disabled by setting ``ad_enable_gc=false``.

With an AD client that uses POSIX attributes, the subdomains provider should include a search such as::

    [sdap_get_generic_ext_step] (0x0400): calling ldap_search_ext with [(&(objectclass=attributeSchema)(|(cn=uidNumber)(cn=gidNumber)))][cn=schema,cn=configuration,DC=win,DC=trust,DC=test]
    [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [cn]
    [sdap_get_generic_ext_step] (0x1000): Requesting attrs: [isMemberOfPartialAttributeSet]

If this search does not match the ``uidNumber`` and ``gidNumber`` schema
objects or of the objects are not replicated to the global catalog, the
Global Catalog support would be disabled irrespective of the ``ad_enable_gc``
configuration option value.

How To Debug
------------
The request is decorated with debug messages as usual.  In addition to
looking at the usual debug logs, ``netstat`` might be a handy tool to
check what port is SSSD connecting to.

Authors
-------
 * Jakub Hrozek <jhrozek@redhat.com>
