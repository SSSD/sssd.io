.. highlight:: none

D-Bus Interface: Users and Groups
=================================

Related ticket(s):

-  `​https://pagure.io/SSSD/sssd/issue/2150 <https://pagure.io/SSSD/sssd/issue/2150>`__

Related design page(s):

-  `DBus Responder <https://docs.pagure.org/SSSD.sssd/design_pages/dbus_responder.html>`__

Problem statement
----------------~

This design document describes how users and groups are represented on
SSSD D-Bus interface.

Use cases
---------

-  Listing users and groups in access control GUI
-  Obtaining extra information about user that is not available through
   standard APIs

D-Bus Interface
---------------

org.freedesktop.sssd.infopipe.Users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Object paths implementing this interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  /org/freedesktop/sssd/infopipe/Users

Methods
^^^^^^^

-  o FindByName(s:name)
-  o FindByID(u:id)
-  ao ListByName(s:filter, u:limit)

   -  filter: possible asterisk as wildcard character; minimum length is
      required
   -  limit: maximum number of entries returned, 0 means unlimited or to
      maximum allowed number

-  ao ListByDomainAndName(s:domain\_name, s:filter, u:limit)

   -  filter: possible asterisk as wildcard character; minimum length is
      required
   -  limit: maximum number of entries returned, 0 means unlimited or to
      maximum allowed number

Signals
^^^^^^^

None.

Properties
^^^^^^^^^^

None.

org.freedesktop.sssd.infopipe.Users.User
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Object paths implementing this interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  /org/freedesktop/sssd/infopipe/Users/$DOMAIN/$UID

Methods
^^^^^^^

-  void UpdateGroupsList()

   -  Performs initgroups on the user.

Signals
^^^^^^^

None.

Properties
^^^^^^^^^^

-  s name

   -  The user's login name.

-  u uidNumber

   -  The user's UID.

-  u gidNumber

   -  The user's primary GID.

-  s gecos

   -  The user's real name.

-  s homeDirectory

   -  The user's home directory

-  s loginShell

   -  The user's login shell

-  a{sas} extraAttributes

   -  Extra attributes as configured by the SSSD. The key is the
      attribute name, value is array of strings that contains the
      values.

-  ao groups

   -  An array of object paths representing the groups the user is a
      member of.

org.freedesktop.sssd.infopipe.Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Object paths implementing this interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  /org/freedesktop/sssd/infopipe/Groups

Methods
^^^^^^^

-  o FindByName(s:name)
-  o FindByID(u:id)
-  ao ListByName(s:filter, u:limit)

   -  filter: possible asterisk as wildcard character; minimum length is
      required
   -  limit: maximum number of entries returned, 0 means unlimited or to
      maximum allowed number

-  ao ListByDomainAndName(s:domain\_name, s:filter, u:limit)

   -  filter: possible asterisk as wildcard character; minimum length is
      required
   -  limit: maximum number of entries returned, 0 means unlimited or to
      maximum allowed number

Signals
^^^^^^^

None.

Properties
^^^^^^^^^^

org.freedesktop.sssd.infopipe.Groups.Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Object paths implementing this interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  /org/freedesktop/sssd/infopipe/Groups/$DOMAIN/$GID

Methods
^^^^^^^

None.

Signals
^^^^^^^

None.

Properties
^^^^^^^^^^

-  s name

   -  The group's name.

-  u gidNumber

   -  The group's primary GID.

-  ao users

   -  A list of the group's member user objects.

-  ao groups

   -  A list of the group's member group objects.

Overview of the solution
------------------------

New D-Bus interfaces will be implemented in the IFP responder.

Find methods perform online lookup if the entry is missing or expired.

Listing methods always perform online lookup to ensure that even
recently added entries are in the list.

Listing methods can return only a limited number of entries. Number of
entries returned can be controlled by **limit** parameter with hard
limit set in sssd.conf with a new configuration option
**filter\_limit**. This option can be present in [ifp] and [domain]
sections to set this limit for data provider filter searches ([domain]
section) and also global hard limit for the listing methods itself
([ifp] section). This limit is supposed to improve performance with large
databases so we process only a small number of records. If the option is
set to 0, the limit is disabled.

Filter may contain only '\*' asterisk as a wildcard character, it does
not support complete set of regular expressions. The asterisk can be
present on the beginning of the filter '\*filter', its end 'filter\*',
both sides '\*filter\*' or even in the middle '\*fil\*ter\*', since it
is supported by both LDAP and LDB. However, only prefix-filter
('filter\*'), can take the performance boost from indices so other filter
may not perform so good with huge databases.

Configuration changes
---------------------

The following options will be created in the [ifp] and [domain]
sections:

-  wildcard\_search\_limit (uint32)

See the `wildcard refresh design page
<https://docs.pagure.org/SSSD.sssd/design_pages/wildcard_refresh.html>`__
for more details.

How To Test
-----------

Call the D-Bus methods and properties. For example with **dbus-send**
tool.

Authors
-------

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
-  Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
