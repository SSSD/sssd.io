.. highlight:: none

D-Bus Interface: Domains
========================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2187 <https://pagure.io/SSSD/sssd/issue/2187>`__

Related design page(s):

-  `DBus Responder <https://docs.pagure.org/SSSD.sssd/design_pages/dbus_responder.html>`__

Problem statement
-----------------

This design document describes how domain objects are exposed on the
bus.

D-Bus Interface
---------------

org.freedesktop.sssd.infopipe.Domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Object paths implementing this interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  /org/freedesktop/sssd/infopipe/Domains

Methods
^^^^^^^

-  ao List()

   -  Returns list of domains.

-  ao FindByName(s:domain\_name)

   -  Returns object path of *domain\_name*.

Signals
^^^^^^^

None.

Properties
^^^^^^^^^^

None.

org.freedesktop.sssd.infopipe.Domains.Domain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Object paths implementing this interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  /org/freedesktop/sssd/infopipe/Domains/\*

Methods
^^^^^^^

-  ao ListSubdomains()

   -  Returns all subdomains associated with this domain.

Signals
^^^^^^^

None.

Properties
^^^^^^^^^^

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

How To Test
~~~~~~~~~~~

Call the D-Bus methods and properties. For example with **dbus-send**
tool.

Authors
~~~~~~~

-  Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
