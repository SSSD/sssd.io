.. highlight:: none

Support for multiple D-Bus interfaces on single object path
===========================================================

Related ticket(s):

-  `IFP: support multiple interfaces for
   object <https://pagure.io/SSSD/sssd/issue/2339>`__

Problem Statement
-----------------

Currently our D-Bus implementation supports having only one interface
registered per one object path prefix. This can be rather limiting
feature since it is often useful to separate shared methods and
properties under one interface that can even have the same
implementation for different object types. This will soon become a
serious drawback when the Infopipe starts supporting signals and new
objects. SSSD already supports few specialized interfaces such as
DBus.Properties and DBus.Introspectable but those are currently
hardcoded to the S-Bus dispatching logic which can be avoided with
direct support for multiple interfaces.

Current state
-------------

The D-Bus interface in the InfoPipe is defined by a sbus\_vtable
structure and associated with a single object path or an object path
prefix followed by '\*' wildcard. For example the current list of
InfoPipe interfaces looks as follows: ::

    static struct sysbus_iface ifp_ifaces[] = {
        { "/org/freedesktop/sssd/infopipe", &ifp_iface.vtable },
        { "/org/freedesktop/sssd/infopipe/Domains*", &ifp_domain.vtable },
        { "/org/freedesktop/sssd/infopipe/Components*", &ifp_component.vtable },
        { NULL, NULL },
    };

There is only one allowed wildcard '\*' and if present it has to be the
last character of the object path.

The dispatch logic is:

#. Lookup the vtable by object path from the message
#. Check that the interface name is the same as the interface define in
   the message, if not check if the interface in the message is one of
   the hard coded interfaces
#. Fail if the interface is invalid
#. Find and execute the method handler

Proposed solution
-----------------

The structure sysbus\_iface combines an object path (pattern) and a list
of supported interfaces on this object path.

There can still be only one supported wildcard and that is '\*' but it
is possible to use it everywhere and multiple times in one object path.

The dispatch logic is:

#. Acquire interface and object path from D-Bus message
#. Find an object path pattern that matches the object path from the
   message, if more than one such pattern exist then the first one
   defined is used
#. Find a list of interfaces associated with this object path pattern,
   if not found continue with next pattern that matches
#. Execute a message handler that is associated with both object path
   and interface

Authors
-------

-  Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
