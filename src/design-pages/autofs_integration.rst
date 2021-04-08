SSSD and automounter integration
================================

This design page describes integration of autofs and SSSD in a more
centralized manner. The discussion started on SSSD mailing list and then
in `Red Hat
Bugzilla <https://bugzilla.redhat.com/show_bug.cgi?id=683523>`__. This
page summarizes the discussions and design.

Autofs is able to look up maps stored in LDAP. However, autofs does all
the lookups on its own. Even though autofs uses the ``nsswitch.conf``
configuration file, there is no glibc interface such as those for
retrieving users and groups and by extension no nscd caching.

The benefits of the integration would be:

-  unified configuration of LDAP servers, timeout parameters, DNS SRV
   lookups, ...
-  only one connection to the LDAP server open
-  caching of the data
-  offline access - even though if the client cannot connect to the LDAP
   server chances are that the NFS server is unreachable as well
-  back end abstraction - data may be stored in NIS or other databases
   and accessed by the automounter transparently

The solution we selected is to provide a new automounter lookup module
that would communicate with SSSD.

autofs lookup modules
---------------------

There are several internal interfaces within autofs implemented as
shared libraries, one is the lookup module.

A lookup module is implemented for each information source and they each
have a fixed interface. Upon loading, automount will get the library
entry points via dlopen(). There are several entry points such as:

-  ``lookup_init()`` and ``lookup_done()`` are called when the module is
   first used and when the module is no longer needed.
-  ``lookup_read_master()`` is called at program start to read the
   master map.
-  ``lookup_read_map()`` reads the entire map.
-  ``lookup_mount()`` looks up an automount map key.

The lookup module is passed autofs internal data structures and must
handle all the corner cases there can be - so the lookup module
shouldn't be exposed outside autofs and should be developed as part of
autofs.

The lookup modules are named ``<autofs library dir>/lookup_<source>.so``
where ``<source>`` is the source name from the "automount:" line of
``/etc/nsswitch.conf``. So the SSSD lookup module would be named
``lookup_sss.so`` and selected in nsswitch.conf with the directive
``automount: files sss`` (to allow for local client overrides) or just
``automount: sss``.

In particular, the lookup module calls an iterator to walk through the
<key, value> pairs in a map or lookup a key by name in a map.

The lookup\_sss module needs to connect to SSSD and request the data
from SSSD somehow. This would be done by adding a couple of functions
into the libnss\_sss.so module. The lookup\_sss.so module would dlopen()
libnss\_sss.so and dlsym() the functions needed.

The API provided by SSSD
------------------------

The SSSD API would live in libnss\_sss.so. That means polluting the
library a little with functions that are not strictly
name-service-switch related, but would allow us to reuse a fair amount
of code and talk to the NSS responder socket easily.

The API itself would define the following functions:

-  iterator start that would allocate the private struct automtent and
   pass it out as context

        ``errno_t _sss_setautomntent(const char *mapname, void **context);``

-  iterator end that would free the private struct automtent

        ``errno_t _sss_endautomntent(void **context);``

-  function that returns the next (key,value) pair given a context

        ``errno_t _sss_getautomntent_r(const char **key, const char **value, void *context);``

        The ``key`` and ``value`` strings are allocated with
        ``malloc()`` and must be freed by the caller

-  function that looks up data for a given key

        ``errno_t _sss_getautomntbyname_r(const char *key, const char **value, void *context);``

        The ``value`` string is allocated with ``malloc()`` and must be
        freed by the caller

The context parameter is a private structure defined in the libnss\_sss
library that would keep track of the iterator: ::

    struct automtent {
        const char *mapname;
        size_t cursor;
        /* Other data TBD as needed */
    };

The iterator is passed as the last parameter of the functions which may
seem a bit odd, but it is an autofs convention. Because the sole
consumer of this interface would be autofs itself, I decided to keep it
the autofs way.

When the API functions are called, SSSD would send a request through the
NSS pipe to the responder, which would consult the back end similar to
how other name service switch requests are handled.

Storing the data in SSSD cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the first version, SSSD should just schedule a periodic task to
download automounter data similar to how user/group enumeration task is
scheduled. The automounter maps can potentially be huge, so we might
need to optimize the download task in later versions. One idea for
future enhancement is to use entryUSN number in deployments that support
it.

The LDAP schema used by autofs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are three schemas that can be used for storing autofs data in
LDAP. They do not differ in semantics the way RFC2307 and RFC2307bis
schemas differ in the member/memberuid attribute. The difference in
schemas is mostly attribute and objectclasses naming and how the DNs are
constructed. The DNs are also not used by the client. SSSD should
convert the data into a cache-specific schema. The cache specific schema
will be based on the RFC2307bis automounter schema, which is by far the
most widely used schema.

Each of the schemas define objectclass names for map and entry and
attribute names for map name (used by map) and key and value attribute
names (used by map entry). ::

    +----------------------+----------------------+------------+----------------------+
    | *attribute*          | *RFC2307bis*         | *NIS*      | *RFC2307 extension*  |
    +======================+======================+============+======================+
    | *map objectclass*    | automountMap         | nisMap     | automountMap         |
    +----------------------+----------------------+------------+----------------------+
    | *entry objectclass*  | automount            | nisObject  | automount            |
    +----------------------+----------------------+------------+----------------------+
    | *map attribute*      | automountMapName     | nisMapName | ou                   |
    +----------------------+----------------------+------------+----------------------+
    | *entry attribute*    | automountKey         | cn         | cn                   |
    +----------------------+----------------------+------------+----------------------+
    | *value attribute*    | automountInformation | nisMapEntr | automountInformation |
    |                      |                      | y          |                      |
    +----------------------+----------------------+------------+----------------------+

An example of the RFC2307bis schema showing an entry for /home/foo
included in the master map: ::

    dn: automountMapName=auto.master,dc=example,dc=com
    objectClass: top
    objectClass: automountMap
    automountMapName: auto.master

    dn: automountMapName=auto.master,dc=example,dc=com
    objectClass: automount
    cn: /home
    automountKey: /home
    automountInformation: auto.home

    dn: automountMapName=auto.home,dc=example,dc=com
    objectClass: automountMap
    automountMapName: auto.home

    dn: automountKey=foo,automountMapName=auto.home,dc=example,dc=com
    objectClass: automount
    automountKey: foo
    automountInformation: filer.example.com:/export/foo

Most, if not all, of the autofs documentation out there describes the
naming schema as per RFC2307bis, but it is technically possible to use
autofs objects created according to RFC2307bis and user/group objects
created according to plain RFC2307 in the same tree. Because the schemas
differ in attribute naming only, not semantically, it is trivial to
override the schema in the config file. We just need to pick the right
defaults and adjust according to user feedback.

One difference between filesystem entries and entries in LDAP is that
the "cn" attribute is case-insensitive, unlike key names which are
essentially directory names. This seems to be one of the reasons the
RFC2307bis schema was adopted.

SSSD Configuration
~~~~~~~~~~~~~~~~~~

The autofs support would be turned on by specifying
``autofs_provider = ldap`` in a domain section. A new search base
``ldap_autofs_search_base`` option will be introduced as well. The
periodic download task will default to ``ldap_search_base``.

SSSD will also include new attribute overrides for the new autofs map in
order to support all the schemas users might have been using.

This work is targeted at the same SSSD milestone as separating the cache
timeout parameters, so we might also need to include a new autofs cache
timeout.

We also need to create a migration document for users of the native
autofs LDAP support.

Fully Qualified Names
^^^^^^^^^^^^^^^^^^^^^

With user/group lookups, the domain can be specified by using a
"fully-qualified-name", for example ``getent passwd
jhrozek@redhat.com``. We should support
something similar with autofs. However, maps can include any characters
that are valid for filesystem path names, including '@', so there's a
potential conflict.

-  if there are more LDAP domains with autofs on, they are searched
   sequentially until a match is found. This is how user searches work,
   too
-  FQDN requests will be allowed by default, but not required unless
   ``use_fully_qualified_names`` is set to TRUE
-  The FQDN name-domain separator is @ by default, but SSSD allows it to
   be configurable even in the current version using the ``re_expression``
   parameter.

Future and miscellaneous work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first iteration will aim at providing a working autofs integration
for generic LDAP servers. There is a number of tasks that might not make
the first iteration but should be tracked and done in the future.

#. Native IPA automount schema

   -  autofs client does not know the concept of "locations" but that
      doesn't really matter. The locations objects in LDAP are of the
      "nscontainer" class and are only part of the DN. The client does
      not care about DNs, so we are safe storing the locations in cache
      as-is.

#. A migration script

   -  this can be lower priority with the migration documentation in
      place
