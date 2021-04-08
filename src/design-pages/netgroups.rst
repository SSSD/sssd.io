Netgroup NSS map support
========================

Overview of Netgroups
---------------------

Netgroups define network-wide groups used for permission checking when
fielding requests for remote mounts, remote logins, and remote shells.
For remote mounts, the information in netgroup is used to classify
machines; for remote logins and remote shells, it is used to classify
users.

Netgroups have a name, and contain one or more of the following members:

-  The name of another netgroup (supporting nested netgroups)
-  A three-tuple of (username,hostname,domainname) (parentheses
   included)

Overview of Netgroups in Name-Service Switch
--------------------------------------------

The interface and behavior of netgroups in libc is a multi-step
procedural interface as follows:

#. The user calls ``setnetgrent(netgroupname)``

   -  This sets an internal, global iterator to the start of the list of
      members for the netgroup specified by netgroupname

#. The user calls ``getnetgrent()`` repeatedly until it returns failure

   -  This returns one set of username, hostname and domainname for each
      call, until there are no more associated with the netgroupname

#. The user calls ``endnetgrent()``

   -  This cleans up after itself

Internally, libraries providing netgroups in libc must unroll the nested
netgroups so that all results are returned by ``getnetgrent()`` without
additional explicit calls.

Overview of Netgroups in LDAP
-----------------------------

Netgroups in LDAP are entries containing the objectClass
``nisNetgroup``. This objectClass specifies two options:

nisNetgroupTriple
    A netgroup, specified as a literal string. So it would be
    ``(hostname,username,domainname)``
memberNisNetgroup
    The name of another netgroup whose contents need to be rolled into
    this entry.

Complete example (taken from
`http://directory.fedoraproject.org/wiki/Howto:Netgroups <http://directory.fedoraproject.org/wiki/Howto:Netgroups>`__):

::

    dn: cn=LinuxTeam,ou=Netgroup,dc=example,dc=com
    objectClass: nisNetgroup
    objectClass: top
    cn: LinuxTeam
    nisNetgroupTriple: (,frank,example.com)
    nisNetgroupTriple: (,jill,example.com)
    memberNisNetgroup: QA
    memberNisNetgroup: Development
    memberNisNetgroup: Operations
    description: The Linux Team

SSSD
----

Overview of approach
--------------------

Netgroups will be processed similarly to how we handle enumerations in
SSSD.

High level
^^^^^^^^^^

#. When a ``setnetgrent()`` request arrives, we will first check the LDB
   cache and then we will go to the backends to update the cache.
#. Once the cache is readied, we will then construct a result object
   that we can iterate through to return the result set.
#. Once the result object is ready, we will reply to the
   ``setgetgrent()`` request to notify the calling application that it
   can start calling ``getnetgrent()``
#. The calling application will issue ``getnetgrent()`` calls until
   there are no more members available.
#. The calling application will call ``endnetgrent()``

Lower-level - setnetgrent
^^^^^^^^^^^^^^^^^^^^^^^^^

#. Incoming requests to the SSSD will behave similarly to the user and
   group enumeration code, except that the individual result objects for
   different netgroup names will be stored in a hash table keyed on the
   netgroup name.
#. During processing, if a netgroup contains nested netgroups, we will
   need to issue a recursive internal ``setnetgrent()`` request. This
   means we will need to have a nesting limit (and ideally,
   loop-detection)
#. The response object must contain the complete unrolled results of all
   of its child netgroups, so that we do not need to maintain multiple
   iterators for reading through the children.
#. The acknowledgement response to the initial ``setnetgrent()`` request
   will need to happen only after all nested netgroups have been cached.

Handling nested netgroups
^^^^^^^^^^^^^^^^^^^^^^^^^

During ``setnetgrent()`` processing, we will convert the results into a
collection object (see libcollection). For each nested group, we will
recurse into ``setnetgrent()`` and create a new collection object that
can be added to the parent collection. In this way, we will be able to
unroll the groups easily.

Later, in ``getnetgrent()`` processing, we will construct the response
from the stored collection object, rather than directly from the
ldb\_result object as we do with user and group enumerations.

Public interfaces:

::

    struct tevent_req setnetgrent_send(char *netgroupname, hash_table_t *nesting)

::

    errno_t setnetgrent_recv(tevent_req *req, struct collection **entries)

Internally, the processing for ``setnetgrent_send()`` is expected to
recurse into nested netgroups and add the resulting ``entries`` to its
own list using the ``col_add_collection_to_collection()`` interface with
the ``col_add_mode_clone`` mode.

Tracking nesting limits
^^^^^^^^^^^^^^^^^^^^^^^

The biggest danger in nesting is the risk of loops in the memberships.
To resolve this, I propose that we keep track of subrequests in a dhash
table. This would behave as follows:

#. In ``setnetgrent_send()`` we would first check whether the
   hash\_count of the hash table is equal to the nesting limit. If it
   is, we will return completion immediately.
#. Next we will check whether netgroupname already exists in the hash
   table. If it does, then we know we have looped and will simply return
   completion immediately.
#. At this point, we will add the current netgroup name to the hash
   table (with a NULL associated value) and continue processing this
   request.
#. In ``setnetgrent_recv()`` we will remove the requested netgroupname
   from the hash table and amend the result collection.

This will allow us to protect against both loops and excessive nesting
all at once.

Dangling Questions
------------------

#. Is it permissible for a single client to request multiple different
   netgroups concurrently?

   -  My reading of the documentation for [set\|get\|end]netgrent leads
      me to believe that this is not permitted by libc.

#. Maybe this is too low-level at this time, but is a cleanup task
   planned?

   -  Netgroups should be handled in the same way that users and groups
      are handled, so I will probably have to extend the existing
      cleanup task to also address the netgroups entries in the cache -
      sgallagh
