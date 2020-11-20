.. highlight:: none

D-Bus Interface: Cached Objects
===============================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2338 <https://pagure.io/SSSD/sssd/issue/2338>`__

Related design page(s):

- `DBus Responder <https://docs.pagure.org/SSSD.sssd/design_pages/dbus_responder.html>`__

Problem statement
-----------------

This design document describes how objects can be marked as cached.

Use cases
---------

-  Allow tools like graphical user management to display a list of users
   who recently logged in.

D-Bus Interface
---------------

org.freedesktop.sssd.infopipe.Cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Object paths implementing this interface
""""""""""""""""""""""""""""""""""""""""

-  /org/freedesktop/sssd/infopipe/Users
-  /org/freedesktop/sssd/infopipe/Groups

Methods
"""""""

-  ao List()
-  ao ListByDomain(s:domain\_name)

   -  Returns list of objects that contains *cached* attribute.

Signals
"""""""

None.

Properties
""""""""""

None.

org.freedesktop.sssd.infopipe.Cache.Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Object paths implementing this interface
""""""""""""""""""""""""""""""""""""""""

-  /org/freedesktop/sssd/infopipe/Users/\*
-  /org/freedesktop/sssd/infopipe/Groups/\*

Methods
"""""""

-  b Store()
-  b Remove()

   -  Those methods will add/remove *cached* attributed to the object
      under *path* implementing this interface.

Signals
"""""""

None.

Properties
""""""""""

None.

Overview of the solution
------------------------

New sysdb attribute *ifp\_cached* is created for users and groups
objects. If this attribute is present, the object is considered to be
cached on IFP D-Bus. The introspection of an object path */obj/path*
will report all cached objects in the subtree */obj/path/\**.

How To Test
-----------

Call the D-Bus methods and properties. For example with **dbus-send**
tool. A cached object is supposed to appear in introspection.

Authors
-------

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
-  Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
