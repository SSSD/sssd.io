.. highlight:: none

Active Directory client DNS updates
===================================

Related ticket(s):

-  `RFE AD dyndns
   updates <https://pagure.io/SSSD/sssd/issue/1504>`__

Problem Statement
-----------------

Clients enrolled to an Active Directory domain may be allowed to update
their DNS records stored in AD dynamically. At the same time, Active
Directory servers support DNS aging and scavenging, which means that
stale DNS records might be removed from AD after a period of inactivity.

While DNS scavenging is not enabled on Active Directory servers by
default, the SSSD should support this use case and refresh its DNS
records to simulate the behavior of Windows AD clients and keep their
address records from being removed if scavenging is used. The SSSD
should also enable the clients to update their DNS records if their IP
address changes.

Overview of Windows client side DNS updates
-------------------------------------------

This section provides a brief overview of how Windows clients may update
their DNS records and how scavenging is configured and performed in a
Windows domain. For more complete information, please follow the links
at the bottom of this page.

Windows Resource Record information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To be able to detect if the resource record is stale, every dynamically
created RR in the Windows DNS has a timestamp that is updated with the
dynamic update if scavenging is enabled. Manually created DNS records do
not have a timestamp. In order to update the timestamp, the DNS records
are refreshed periodically even if they actually haven't changed, just
to bump the timestamp.

A special timestamp value of 0 can be set to the resource record,
indicating unlimited lifetime of the record. Such record is never
scavenged.

Update and refresh
^^^^^^^^^^^^^^^^^^

When a Windows client updates its DNS information, it may perform either
an update or a refresh.

-  an *update* is performed when the IP address of a client changes.
   Involves a refresh and a change of the IP address(es).
-  a *refresh* does not change the IP addresses themselves, but rather
   only updates the timestamp of existing resource record, keeping it
   from being scavenged.

In order to maintain a heartbeat on the resource records, the Windows
clients perform updates and/or refreshes under conditions outlined in
the next section.

Scavenging timeouts
^^^^^^^^^^^^^^^^^^^

In the zone properties, there are two timeout settings that are
affecting the scavenging

-  No-refresh interval - minimal interval between last refresh after
   which the record can be refreshed again
-  Refresh interval - interval during which the refreshes are allowed.
   After the refresh interval passes, the stale records can be
   scavenged. In other words, the refresh interval starts at
   ``timestamp + no_refresh_interval``.

Windows clients update and refresh intervals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For Windows clients, refreshes or updates generally occur for the
following reasons:

-  the computer is restarted
-  the DHCP lease is renewed
-  periodically every 24 hours by default

   -  this is configurable in the windows registry using the
      ``DefaultRegistrationRefreshInterval`` key under the
      ``HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TcpIp\Parameters``
      subkey

The SSSD updates should be modeled to be close to what the Windows
clients do.

SSSD clients refresh intervals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The SSSD would perform the dynamic DNS update or refresh under the
following conditions:

-  the back end becomes online

   -  this would also cover the case where computer is restarted. For
      long-running deployments where the SSSD is almost never offline,
      the back end would only ever become online after bootup

-  periodically based on a configuration option

   -  the configuration option could be named
      ``dyndns_refresh_interval`` or similar and it would default to 24
      hours
   -  the granularity will be seconds. AD interface also allows to set
      the refresh and no-refresh interval in hours, too, so our
      granularity should not be lower. Seconds also allow expressing
      other values that might for instance map to DHCP leases easier.
   -  admin could change the option to be same as DHCP lease for example
      to simulate the case where Windows workstations refresh the
      address after lease is renewed

Overview of the solution
------------------------

Because the DNS records scavenging is not on by default on the server
side, the client side DNS updates would be off by default as well. A new
configuration option, called ``dyndns_update`` (bool) would control
whether the DNS update should be performed.

Addresses used during the update
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We will reuse a similar mechanism used in the IPA provider where the
address used to connect to the AD server LDAP connection is used by
default. Optionally, for machines that use IP aliasing or setups that
wish to update both IPv4 and IPv6 addresses of an interface at the same
time there will be an option ``dyndns_iface``.

Contrary to IPA dynamic DNS update that generates the PTR record in the
bind dyndb plugin, AD wouldn't update the PTR record on its own when
only A/AAAA record is updated. To be able to keep the forward and
reverse zones in sync, the AD dynamic update message would also include
updating the PTR records. PTR records update would not be on by default
and could be turned on by setting an option (perhaps
``dyndns_update_ptr``) to true.

Future and optional enhancements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Currently the information on whether scavenging is enabled and how
   often is it performed is stored in GPOs. When SSSD has the ability to
   process Group Policies, we would add a new special value to the
   periodical update option that would tell the SSSD to simply honour
   the Group Policies.
-  We could also integrate with netlink to perform IP address refresh on
   DHCP lease renewals. This could be filed as a separate ticket and
   implemented later.

Implementation details
----------------------

For the update itself, we can simply use the nsupdate utility the way we
use it in IPA domain. The update code is already there, it is mostly a
matter of splitting the code to be IPA-agnostic.

One change compared to the IPA code would be that IPA only sends the
refresh when the addresses change, to avoid unnecessary zone transfers
on the IPA server. As stated above Windows clients typically refresh
their address even if nothing changed, so our update code would run
unconditionally, too, based on timed events.

#. The use of ``resolv_init`` in the dynamic DNS update code should be
   inspected. If it is not needed anymore and the resolver code could
   already be told per-request to only go to DNS and ignore
   ``/etc/hosts``, the initialization should be removed.
#. A new module shared between IPA and AD providers shall be created.
   This module will contain generic functions related to dynamic DNS
   update such as:

   -  a variant of ``ipa_dyndns_add_ldap_iface`` decoupled from IPA
      dependencies
   -  function to gather all addresses of an interface
   -  utility functions

#. The existing ``fork_nsupdate_send`` request would be split out to a
   generic request that calls nsupdate with a specified message. This
   request would be placed in the module created in the previous step.
   The IPA provider would be converted to use these new generic request.
   The interface might look like: ::

           struct tevent_req *be_nsupdate_send(struct tevent_context *ev, const char *nsupdate_msg);
           errno_t be_nsupdate_recv(struct tevent_req *req, int *child_retval);

#. In the AD provider, a variant of IPA dyndns code would be created,
   using AD specific data structures and options. This interface would
   consist of a tevent request that would wrap ``fork_nsupdate_send``
   using ``struct ad_options`` and an initializer function called on
   provider startup.
#. If the ``dyndns_update`` option was set to ``true``, then the AD
   provider would:

   -  set up a periodic task running each ``dyndns_refresh_interval``
      hours updating the DNS records
   -  set up an online callback to run the DNS update when the back end
      goes online

List of all new configuration options
-------------------------------------

During design discussion, it was decided that the new options should be
not include the provider-specific prefix but rather be provider agnostic
to ease sharing the code and possibly allow other providers to use
dynamic DNS updates as well. The new options are:

#. ``dynds_update`` ``(bool)`` - whether to perform the dynamic DNS
   update. Defaults to false.
#. ``dyndns_refresh_interval`` ``(integer)`` - how often to run the
   periodic task to refresh the resource record
#. ``dyndns_iface`` ``(string)`` - instead of updating the DNS with the
   address used to connect to LDAP, which is the default, use all
   addresses configured on a particular interface
#. ``dyndns_update_ptr`` ``(bool)`` - whether to also update the reverse
   zone when updating the forward zone
#. ``dyndns_auth`` ``(string)`` - how should the ``nsupdate`` utility
   authenticate to DNS. Supported values would be ``gss-tsig`` and
   ``none``. IPA and AD providers would default to ``gss-tsig``. In 1.10
   this option would be undocumented and the only providers that would
   document the other options in their man pages would be IPA and AD.
   Future expansion of this feature into other providers would be as
   easy as hooking online callbacks into dynamic DNS update handler.

The existing ``ipa_dyndns_update``, ``ipa_dyndns_ttl`` and
``ipa_dyndns_iface`` options would map to these new options. The
``sssd-ipa`` manual page would be amended to list the new options
primarily and also list the old ones as a fallback, which would
eventually be removed.

How to test
-----------

#. Test that forward and reverse zone updates work

   -  Make sure DNS updates are enabled on the zone

      -  Right-click the zone and select the "General" tab
      -  There is a combo-box labeled "Dynamic updates". Toggle it to
         "Secure only".
      -  Click "Apply"

   -  Prepare a client with dynamically updated DNS address

      -  the easiest way is to join the client with realmd -
         ``realm join ad.domain.example.com``

   -  Test updates when the address has changed

      -  Change the address of a client
      -  Perform an action that would trigger an online callback such as
         login
      -  In the AD MMC check if the DNS address is the same as the new
         address on the client
      -  Depending on the settings of ``dyndns_iface`` or
         ``dyndns_update_ptr`` also check if all expected addresses have
         been updated in both forward and reverse zones.

   -  Test periodic refresh

      -  Set the periodic refresh (``dyndns_refresh_interval`` in this
         document) to some low value
      -  Wait until that value passes or modify the system time
      -  The timestamp of the resource records would be changed after
         SSSD ran its periodic task. The timestamp will be rounded down
         to the nearest hour by AD.

#. Test DNS scavenging

   -  Enroll two SSSD clients into AD

      -  Turn one of them off after enrollment. This client will be
         scavenged.
      -  Let the other one up and set its ``dyndns_refresh_interval`` to
         a value shorter than the scavenging interval

   -  Enable DNS scavenging on the server

      -  In the DNS MMC console, right-click the DNS server in the tree
         view, select Properties and navigate to the "Advanced" tab
      -  Enable the "Enable automatic scavenging of stale records"
         toggle and select a meaningful period
      -  Hit apply

   -  Enable DNS scavenging for the zone

      -  Open the DNS administrative console
      -  Right-click the zone and select the "General" tab.
      -  Click the "Aging" button
      -  Enable the "Scavenge stale resource records" toggle
      -  Set the no refresh and refresh interval to a low value.
      -  Check the "This zone can be scavenged after" text box. It
         should list a date and time shortly in the future.

   -  Let the scavenging interval pass

      -  The client that was turned off after enrollment should be
         scavenged. You should no longer be able to see its records in
         the DNS zones on the server.
      -  The other client's DNS records should remain intact in the DNS
         MMC console

Links and resources
-------------------

-  `Understanding aging and
   scavenging <http://technet.microsoft.com/en-us/library/cc759204%28v=ws.10%29.aspx>`__
-  `Using DNS Aging and
   Scavenging <http://technet.microsoft.com/en-us/library/cc757041%28v=ws.10%29.aspx>`__
-  `Don't be afraid of DNS Scavenging. Just be patient. by MSFT
   Networking
   Team <http://blogs.technet.com/b/networking/archive/2008/03/19/don-t-be-afraid-of-dns-scavenging-just-be-patient.aspx>`__

Author(s)
---------

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
