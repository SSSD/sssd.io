.. highlight:: none

DBus responder
==============

Related ticket(s):

-  `Provide an experimental DBus responder to retrieve custom
   attributes from SSSD
   cache <https://pagure.io/SSSD/sssd/issue/2072>`__
-  `Extend the LDAP backend to retrieve extended set of
   attributes <https://pagure.io/SSSD/sssd/issue/2073>`__

Problem Statement
-----------------

The contemporary centralized user databases such as IPA or Active
Directory store many attributes that describe the user. Apart from
attributes that are related to a "computer user" entry such as user
name, login shell or an ID, the databases often store data about the
physical user represented by the entry, such as telephone number. Since
the SSSD already has means of connecting to the remote directory,
including advanced features like offline support or fail over, it would
appear as a natural choice for retrieving these attributes. However, the
only interface the SSSD provides towards the system at the moment is the
standard `POSIX
interface <https://www.gnu.org/software/libc/manual/html_node/Name-Service-Switch.html>`__
and a couple of ad-hoc application specific responders (sudo, ssh,
autofs). The purpose of this document is to describe a design of a new
responder, that would listen on the system bus and allow third party
consumers to retrieve custom attributes stored in a centralized database
via a DBus call.

The DBus interface design
-------------------------

This section gathers feedback expressed in mailing lists, private e-mail
conversations and IRC discussions and summarizes feature requests and
areas that need improvement into a design proposal of both the DBus API
and several required changes in the core SSSD daemon.

Cached objects
~~~~~~~~~~~~~~

`D-Bus Interface: Cached
Objects <https://docs.pagure.org/SSSD.sssd/design_pages/dbus_cached_objects.html>`__

Object exposed on the bus
~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of a single interface returning object attributes in an
LDAP-like way, the interface would be built in an object-oriented
fashion. Each object (i.e. a user or a group) would be identified with an
object path and methods would be available to the interface user to make
it possible to retrieve either a single object or a set of object.

The interface will support users, groups and domains.

Representing users and groups on the bus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`D-Bus Interface: Users and
Groups <https://docs.pagure.org/SSSD.sssd/design_pages/dbus_users_and_groups.html>`__

Representing SSSD processes on the bus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **object path**: /org/freedesktop/sssd/infopipe/Components/monitor
-  **object path**:
   /org/freedesktop/sssd/infopipe/Components/Responders/$responder\_name
-  **object path**:
   /org/freedesktop/sssd/infopipe/Components/Backends/$sssd\_domain\_name

-  **method** org.freedesktop.sssd.infopipe.ListComponents()

   -  returns: Array of object paths representing component objects

-  **method** org.freedesktop.sssd.infopipe.ListResponders()

   -  returns: Array of object paths representing component objects

-  **method** org.freedesktop.sssd.infopipe.ListBackends()

   -  returns: Array of object paths representing component objects

-  **method** org.freedesktop.sssd.infopipe.FindMonitor()

   -  returns: Object path representing the monitor object

-  **method** org.freedesktop.sssd.infopipe.FindResponderByName(String
   name)

   -  *name*: The name of the responder to retrieve
   -  returns: Object path representing the responder object

-  **method** org.freedesktop.sssd.infopipe.FindBackendByName(String
   name)

   -  *name*: The name of the backend to retrieve
   -  returns: Object path representing the backend object

The name "Components" is chosen to not imply any particular
implementation on SSSD side.

The component objects implements
org.freedesktop.sssd.infopipe.Components interface, which is define as:

-  **method** org.freedesktop.sssd.infopipe.Components.Enable()

   -  returns: nothing
   -  note: changes will be visible after SSSD is restarted

-  **method** org.freedesktop.sssd.infopipe.Components.Disable()

   -  returns: nothing
   -  note: changes will be visible after SSSD is restarted

-  **method**
   org.freedesktop.sssd.infopipe.Components.ChangeDebugLevel(Uint32
   debug\_level)

   -  *debug\_level*: Debug level to set
   -  returns: nothing
   -  note: changes will be permanent but do not require restart of the
      daemon

-  **property** String name

   -  The name of this service.

-  **property** Uint32 debug\_level

   -  The name of this service.

-  **property** Boolean enabled

   -  Whether the service is enabled or not

-  **property** string type

   -  Type of the component. One of "monitor", "responder", "backend".

This approach will completely distinguish SSSD processes from services
and domains, which are logical units that should not contain any
information about SSSD architecture.

Representing service objects on the bus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API should include methods to represent service object(s) and
provide basic information and configuration abilities.

-  **object path**: /org/freedesktop/sssd/infopipe/Services/$service

-  **method** org.freedesktop.sssd.infopipe.ListServices()

   -  returns: Array of object paths representing Service objects

-  **method** org.freedesktop.sssd.infopipe.FindServiceByName(String
   name)

   -  *name*: The name of the service to retrieve
   -  returns: Object path representing the service object

The service object will in the first iteration include several
properties describing the domain. As this iteration doesn't allow any
modification, only properties and not methods are considered:

-  **property** String name

   -  The name of this service.

-  service dependent properties

Other properties might be added upon request.

Representing domain objects on the bus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For some consumers (such as realmd), it's important to also know the
properties of a domain. The API should include methods to retrieve a
active domain object(s) and represent the domains as objects on the bus
as well.

-  **object path**: /org/freedesktop/sssd/infopipe/Domains/$domain

The synopsis of these calls would look like:

-  **method** org.freedesktop.sssd.infopipe.ListDomains()

   -  returns: Array of object paths representing Domain objects

-  **method**
   org.freedesktop.sssd.infopipe.ListSubdomainsByDomain(String name)

   -  returns: Array of object paths representing Domain objects
      associated with domain $name

-  **method** org.freedesktop.sssd.infopipe.FindDomainByName(String
   name)

   -  *name*: The name of the domain to retrieve
   -  returns: Object path representing the domain object

The domain object will in the first iteration include several properties
describing the domain. As this iteration doesn't allow any modification,
only properties and not methods are considered:

-  **property** String name

   -  The name of this domain. Same as the domain stanza in the
      sssd.conf

-  **property** String[] primary\_servers

   -  Array of primary servers associated with this domain

-  **property** String[] backup\_servers

   -  Array of backup servers associated with this domain

-  **property** Uint32 min\_id

   -  Minimum UID and GID value for this domain

-  **property** Uint32 max\_id

   -  Maximum UID and GID value for this domain

-  **property** String realm

   -  The Kerberos realm this domain is configured with

-  **property** String forest

   -  The domain forest this domain belongs to

-  **property** String login\_format

   -  The login format this domain expects.

-  **property** String fully\_qualified\_name\_format

   -  The format of fully qualified names this domain uses

-  **property** Boolean enumerable

   -  Whether this domain can be enumerated or not

-  **property** Boolean use\_fully\_qualified\_names

   -  Whether this domain requires fully qualified names

-  **property** Boolean subdomain

   -  Whether the domain is an autodiscovered subdomain or a
      user-defined domain

-  **property** ObjectPath parent\_domain

   -  Object path of a parent domain or empty string if this is a root
      domain

Other properties such as provider type or case sensitivity might be
added upon request. Right now, we need something other developers can
experiment with.

Synchronous getter behaviour
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Retrieving a property with a getter will always be synchronous and return
the value currently cached. The getter might schedule an out-of-band
update depending on the state of the cache object. The primary reason
for the getter being synchronous is to be able to be composable, in
other words being able to call N getters in a loop and construct a reply
message containing N properties without resorting to asynchronous updates
of the properties.

Callers that with to have an up-to-date view of the properties should
update the object by calling a special ``update`` (not included ATM)
method or subscribe to the PropertiesChanged interface.

SSSD daemon features
--------------------

Apart from features that will directly benefit the new interface, the
SSSD itself must adapt to some requirements as well.

Access control
~~~~~~~~~~~~~~

The DBus responder needs to limit who can request information at all and
what attributes can be returned.

Limiting access to the responder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DBus responder will re-use the same mechanism the PAC responder uses
where UIDs of clients that can contact the responder will be enumerated
in the "allowed\_uids" parameter of the responder configuration.

In a future enhancement, we might add a "self" mechanism, where client
will be allowed to read its own attributes. As limiting attribute access
might be different for this use-case, the first iteration of the
responder will not include the "self" mechanism.

Limiting access to attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The responder will have a whitelist of attributes that the client can
query. No other attributes will be returned. Requesting an attribute
that is not permitted will yield an empty response, same as if the
attribute didn't exist. The whitelist will include the standard set of
POSIX attributes as returned by i.e. ``getpwnam`` by default.

The administrator will be allowed to extend the whitelist in sssd.conf
using a configuration directive either in the ``[ifp]`` section itself
or per-domain. The configuration directive shall allow either explicitly
adding attributes to the whitelist (using ``+attrname``) or explicitly
remove them using ``-attrname``.

The following example illustrates explicitly allowing the
telephoneNumber attribute to be queried and removing the gecos attribute
from the whitelist. ::

        [ifp]
        user_attributes = +telephoneNumer, -gecos

Support for non-POSIX users and groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently the SSSD supports looking up POSIX users and groups, mostly
due to the fact that primary consumers are POSIX interfaces such as the
Name Service Switch. For instance, the search filters in back ends
require the presence of attributes ID.

In contrast, users and groups that consumers of this new interface
require often lack the POSIX attributes. The SSSD must be extended so
that even non-POSIX users and groups are handled well.

Do not require enumeration to be enabled to retrieve set of users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the moment, the SSSD can either fetch a single user (using getpwnam
for example) or all available users (using getpwent). As an effect, all
proposed DBus calls require enumeration to be switched on in order to be
able to retrieve sets of users. The SSSD needs to either grow a way to
retrieve several entries at once without enumerating or needs to make
enumeration much faster.

Authors
-------

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
-  Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
-  Stef Walter <`stefw@redhat.com <mailto:stefw@redhat.com>`__>
