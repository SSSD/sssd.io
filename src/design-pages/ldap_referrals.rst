LDAP Referrals
--------------

Pre-requisites
~~~~~~~~~~~~~~

sdap\_id\_op enhancements
^^^^^^^^^^^^^^^^^^^^^^^^^

#. Disentangle sdap\_id\_op setup from failover configuration
#. Handle async resolver needs for referrals. We need to look up
   referred servers and take the first IP returned by DNS.
#. Add idle disconnection timer for connections (see Ticket
   `#1036 <https://pagure.io/SSSD/sssd/issue/1036>`__, needs to have
   its priority bumped up). We don't want to be hanging onto referred
   servers forever.

Single-entry lookup
~~~~~~~~~~~~~~~~~~~

#. Perform lookup on standard server connection
#. Get referral reply
#. Acquire sdap connection to the referred server
#. Perform lookup on referred server
#. Repeat as needed until referral depth limit is reached

Multiple-entry lookup
~~~~~~~~~~~~~~~~~~~~~

First approximation: just process each referral as a series of
single-entry lookups, gathering all results at the end.

Optimizations
~~~~~~~~~~~~~

#. Keep lookup cache/hashtable of entries pointing to the same referred
   entry (I suspect the value is low here, as the chance of multiple
   replies referring to the same entry is unlikely).
#. In the case of multiple referred entries to the same LDAP server, can
   we bundle them into single requests? (Probably not. Referrals will
   end up requiring BASE searches. Most LDAP servers don't support
   subtree searches on DN)
#. Keep a hash/lookup table of sdap\_id\_op links. Don't reconnect
   unless we have to (such as when performing auth via LDAP simple
   bind).

   #. Keep separate sdap\_id\_op links for ID and AUTH. ID always uses
      the default bind credentials, AUTH can drop the bind and
      reconnect.

Relationship to multiple search bases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Only the primary server will need multiple bases. The referrals will end
up as base searches, thereby ignoring the multiple search base values.

Referrals should *ignore* the base filtering of ticket
`#960 <https://pagure.io/SSSD/sssd/issue/960>`__.

How do we handle originalDN? I think we need to save originalDN as it
would have appeared on the primary server, not the referred server.

Research: how are we doing this now? I remember that we hit this before
when dealing with referrals. Did we solve it for all referral types or
only some?

Finally, related to the search filtering, ticket
`#960 <https://pagure.io/SSSD/sssd/issue/960>`__ should do its
filtering based on the originalDN value, not the referred DN.

Questions needing research
~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Do all referrals give a complete answer? (i.e. If they refer locally,
   is it relative?)

   -  `http://www.ietf.org/rfc/rfc3296.txt <http://www.ietf.org/rfc/rfc3296.txt>`__
      says that "The ref attribute values SHOULD NOT be used as a
      relative name-component of an entry's DN [RFC2253]."

#. Can we keep a connection open to rebind? i.e. If we're performing
   AUTH, do we have to open a new socket connection to perform a new
   simple bind, or can we drop and bind again?)
#. How do we treat unreachable referral servers?

   #. As missing entries. This might cause cache issues with flaky
      networks, as we always treat missing entries as definitive
      deletion of the entry for our cache. I believe this is how things
      are handled now with the openldap internal referral chasing, but I
      need to research this.
   #. Any unreachable referral server results in SSSD going offline.
      This is potentially chaotic, as it introduces multiple points of
      failure resulting in offline operation.
   #. Flag unreachable entries as "complete", thereby having SSSD rely
      on their presence or absence in the cache. While this sounds nice
      in theory, I think this would probably be very difficult to get
      right, especially with enumeration. I recommend deferring this as
      a future optimization and going with one of the other approaches
      (or possibly make the other approaches into an sssd.conf option).

#. How do we handle nested referrals?

   -  Option: Handle all referrals at a particular depth before
      descending further. This can help avoid attempts to create
      duplicate sdap\_id\_ops. The downside to this approach is that
      situations where entries are coming from multiple servers will
      only ever function as quickly as the slowest server in the set.
   -  Option: Track nestings as additional subreq levels. Add careful
      sdap\_id\_op acquisition locking and proceed into nestings as
      quickly as they are available. This is more complicated to get
      right, but probably will provide a noticeable gain in complex
      setups.

Stuff to Test
~~~~~~~~~~~~~

#. Entry referrals

   #. Same server different DN
   #. Different server same DN
   #. Different server different DN

#. Subtree referrals

   #. Same server different DN
   #. Different server different DN

#. Referral on bind attempt (referred AUTH)
#. Referred password change
