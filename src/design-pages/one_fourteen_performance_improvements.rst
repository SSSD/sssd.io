Improve SSSD Performance with a timestamp cache
===============================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2602 <https://pagure.io/SSSD/sssd/issue/2602>`__
-  `https://pagure.io/SSSD/sssd/issue/2062 <https://pagure.io/SSSD/sssd/issue/2062>`__

Problem statement
~~~~~~~~~~~~~~~~~

At the moment SSSD doesn't perform well in large environments. Most of
the use-cases we've had reported revolved around logins of users who are
members of large groups or a large amount of groups. Another reported
use-case was the time it takes to resolve a large group.

While workarounds are available for some of the issues (such as using
``ignore_group_members`` for resolution of large groups), our goal is to
be able to perform well without these workarounds.

Use cases
~~~~~~~~~

-  User who is a member of a large amount of AD groups logs in to a
   GNU/Linux server that is a member of the AD domain.
-  User who is a member of a large amount of AD or IPA groups logs in to
   a GNU/Linux server that is a member of an IPA domain with a trust
   relationship to an AD domain
-  Administrator of a GNU/Linux server runs "ls -l" in a directory where
   files are owned by a large group. An example would be group called
   "students" in an university setup

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

During performance analysis with systemtap, we found out that the
biggest delay happens when SSSD writes an entry to the cache, especially
for large group entries. This is also confirmed by empirical evidence
from our users, where most deployments were OK with SSSD performance
once the cache was moved to tmpfs or even when ``ignore_group_members``
option was enabled.

We can't skip cache writes completely, even if no attributes changed,
because we store also the expiration timestamps in the cache. Also, even
if a single attribute (like the timestamp) changes, ldb would need to
unpack the whole entry, change the record, pack it back and then write
the whole blob.

In order to mitigate the costly cache writes, we should avoid writing
the whole cache entry on every cache update, but only write the entries
if something actually changed.

To avoid this, we will split the monolithic ldb cache representing the
sysdb cache into two ldb files. One would contain the entry itself and
would be fully synchronous. The other (new one) would only contain the
timestamps and would be open using the ``LDB_FLG_NOSYNC`` to avoid
synchronous cache writes.

This would have two advantages:

#. If we detect that the entry hasn't changed on the LDAP server at all,
   we could avoid writing into the main ldb cache which would still be
   costly. We would use the value of the ``modifyTimestamp`` attribute
   of the LDAP entry to see if the entry had changed or not.
#. The writes to the new async ldb cache would be much faster, because
   the entry is smaller and because the writes wouldn't call ``fsync()``
   due to using the async flag, but rather rely on the underlying
   filesystem to sync the data to the disk.

On SSSD shutdown, we would write a canary to both the timestamp cache
and the main sysdb cache, denoting graceful shutdown. On SSSD startup,
if the canary wasn't found or if the values differ, we would just ditch
the timestamp cache, which would result in refresh and write of the
entry on the next lookup.

The basic idea is to use a combination of the operational
``modifyTimestamp`` attribute and checking the entry itself to see if
the entry changed at all and if not, avoid writing to the cache.

Checking the value of ``modifyTimestamp`` would be enough for group
entries, which should be the first iteration of this work. For checking
if other entries (mostly users) have changed, we need to compare the
value of the attributes in the cache with what we are about to store in
the cache.

Therefore, these enhancements are proposed for the 1.14 versions, sorted
by the importance as observed with systemtap testing:

-  only write the cache entry if the ``modifyTimestamp`` of the original
   entry had changed. If it hasn't changed, only the timestamps would be
   written to the timestamp cache
-  if the ``modifyTimestamp`` had changed, compare the attributes of the
   cache entry with the attributes we are about to write. If there are
   no differences, only write to the timestamp cache
-  refactor the nested group processing to make sure expensive lookups
   (such as lookups of all members of the group, there can potentially
   be thousands of these) are only performed once and intermediate
   results are stored in-memory.
-  attempt to shortcut parsing the attributes of the entry returned from
   LDAP sooner. The idea behind this is that if the ``modifyTimestamp``
   did not change, we can reuse the entry we already cached.

Minor enhancements in later versions might include:

-  using syncrepl in the server mode for HBAC rules and external groups
   in refreshAndPersistMode. This would provide performance benefit for
   legacy clients that rely on server's HBAC rules for access control.
-  using syncrepl in the server mode for external groups in
   refreshAndPersistMode. This would mainly simplify the external groups
   handling, rather than improve performance
-  A lot of time is spent looking up attributes in the ``sysdb_attrs``
   array. This is something we might want to optimize after we're done
   with the cache writes.
-  We might even consider offering syncrepl in refreshOnly mode as an
   client-side option for enumeration. However, this would have to be an
   opt-in because every refresh causes the server to walk the changelog
   since the last refresh operation. Enabling this option on all clients
   would trash the server performance.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

The ``sysdb_ctx`` already contains a handle of the main sysdb cache. We
would add another ldb file that only contains the timestamp and the DN
of an entry. This ldb file would be opened in the nosync mode.
Attributes used for lookups, like ``dataExpireTimestamp`` must be
indexed in this database as well.

When storing a user or a group to sysdb using functions like
``sysdb_store_user``, we first check the difference between
``modifyTimestamp`` attributes. If there are no differences, only the
timestamp attributes, such as ``lastUpdate`` or ``dataExpireTimestamp``
would be updated in the timestamp cache. We need to do this check in the
lower-level sysdb calls to make sure this enhancement also works for
users and groups retrieved through the extop plugin.

If the value of ``modifyTimestamp`` differs, we proceed to checking the
diff between values in the cache and the values read from LDAP.

Details about shortcut of attribute parsing will be added to this design
page later.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

Currently no configuration changes are expected. We might add some if we
decide to implement on-demand syncrepl.

How To Test
~~~~~~~~~~~

If the entries on the server did not change (except timestamps), then
actions like user and group lookups and logins should be considerably
faster.

The SSSD should also correctly detect when the entries in fact did
change on the server. In this case, a full cache write will be
performed.

Authors
~~~~~~~

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
   with the kind help of
-  Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
-  Ludwig Krispenz
   <`lkrispen@redhat.com <mailto:lkrispen@redhat.com>`__>
-  Simo Sorce <`simo@redhat.com <mailto:simo@redhat.com>`__>
