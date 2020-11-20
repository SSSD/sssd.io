.. highlight:: none

D-Bus Signal: Notify Property Changed
=====================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2233 <https://pagure.io/SSSD/sssd/issue/2233>`__

Related design page(s):

-  `DBus Responder <https://docs.pagure.org/SSSD.sssd/design_pages/dbus_responder.html>`__

Problem statement
-----------------

This design document describes how to implement
org.freedesktop.DBus.Properties.PropertiesChanged signal for SSSD
objects exported in the IFP responder.

D-Bus Interface
---------------

org.freedesktop.DBus.Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Signals
^^^^^^^

-  PropertiesChanged(s interface\_name, {sv} changed\_properties, as
   invalidated\_properties)

   -  interface\_name: name of the interface on which the properties are
      defined
   -  changed\_properties: changed properties with new values
   -  invalidated\_properties: changed properties but the new values are
      not send with them
   -  this signal is emitted for every property annotated with
      org.freedesktop.DBus.Property.EmitsChangedSignal, this annotation
      may be also used for the whole interface meaning that every
      property within this interface emits the signal

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

Changes in properties are detected in new LDB plugin inside a *mod*
hook. The plugin writes list of changed properties in a TDB-based
changelog which is periodically consumed by IFP responder. IFP then
emits PropertiesChanged signal per each modified object.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

TDB Format
^^^^^^^^^^

-  **TDB Name**: *ifp\_changelog.tdb*
-  **Key**: dn of modified object
-  **Value**: chained list of modified properties in the form
   *total\_num\\0prop1\\0prop2\\0...\\0*

IFP Side
^^^^^^^^

#. TDB database is created on IFP start and deleted on IFP termination.

   -  on IFP start:

      -  if TDB file does not exist it is created
      -  if TDB file exist (unexpected termination of IFP) it is
         flushed, we do not care about the data inside

   -  on correct IFP termination

      -  the TDB file is deleted

#. A periodic task *IFP: notify properties changed* is created, it is
   responsible for emitting the *PropertiesChanged* signal

   -  Periodic task flow:

      #. Lock TDB for read-only access
      #. Traverse the TDB and remember dn and properties for all
         modified objects
      #. Flush TDB
      #. Release the lock
      #. Create and emit D-Bus signal per each object that is exported
         on IFP bus and supports *PropertiesChanged* signal

LDB Plugin Side
^^^^^^^^^^^^^^^

#. If TDB file does not exist just quit
#. If modified object supports the signal store it in the TDB

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

In IFP section:

-  **ifp\_notification\_interval**: period of *IFP: notify properties
   changed*, disabled if 0, default 300 (5 minutes)

How To Test
~~~~~~~~~~~

#. Hook onto *PropertiesChanged* signal, e. g. with *dbus-monitor'̈́'*
#. Trigger change of user/group
#. Signal should be received

Questions
~~~~~~~~~

#. Do we want to use *changed\_properties* or *invalidated\_properties*

Authors
~~~~~~~

-  Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
