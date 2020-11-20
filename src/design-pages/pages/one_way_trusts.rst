One way trust support
=====================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2579 <https://pagure.io/SSSD/sssd/issue/2579>`__

Problem statement
~~~~~~~~~~~~~~~~~

The next IPA release will support one-way trusts. SSSD needs to add
support for this feature in its server mode.

Use cases
~~~~~~~~~

One-way trust to Active Directory where FreeIPA realm trusts Active
Directory forest using cross-forest trust feature of AD but the AD
forest does not trust FreeIPA realm. Users from AD forest can access
resources in FreeIPA realm.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

At a high level, SSSD needs to examine the trust objects whether they
are one-way or two way trusts. For each one-way trust, SSSD needs to
fetch and store the keytab and use the keytab to secure the connection.
For two-way trusts, we can keep using the existing code that reuses the
IPA realm and the system keytab for both IPA and AD connections. Care
must be taken to remove keytabs of trusts that were removed as well.

Fetching the keytab would be done by calling the ``ipa-getkeytab``
utility for every one-way trust. The keytab would only be (re)fetched if
it's missing or if attempting to use the keytab failed. On the IPA
server, we must make sure that the IPA server identity is allowed to
read the keytab.

Because handling multiple keytabs increases the risk of failing
connections in case the trust wasn't setup correctly, we need to modify
the failover code to not set the whole back end offline in case
connecting to a subdomain AD server fails. Instead, the subdomain will
be marked as inactive for a short period of time, during which it would
act as offline. The proper way of solving this problem would be to
rework the failover module so that it can act per domain, not only per
back end, however, that change is out of scope for this release.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

This section describes all the required changes in detail.

Reading the subdomains in the IPA subdomain handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The IPA subdomain handler will include the attribute
``ipaNTTrustDirection`` when reading the trust objects. Currently this
attribute is not readable by the host principal, so the IPA ACIs must be
relaxed (ipa ticket?). If the trust direction is set to an OR of
``lsa.LSA_TRUST_DIRECTION_OUTBOUND`` and
``lsa.LSA_TRUST_DIRECTION_INBOUND``, then it's a two-way trust and we'll
just use the existing code that re-uses the IPA keytab for the AD
trusted domain as well. If the attribute is only
``lsa.LSA_TRUST_DIRECTION_OUTBOUND``, we handle the trust as a one-way
trust. The trust type can be stored in ``ipa_ad_server_ctx``. If the
trust direction is set to ``lsa.LSA_TRUST_DIRECTION_INBOUND`` only, then
we would log this trust object as unsupported and continue.

Each ``sss_domain_info`` structure will be created as ``inactive`` in
the subdomain code. After enumerating the trusted domains, the subdomain
handler will check if a keytab already exists for every one-way trusted
domain. If yes, the domain is ready to use and can be enabled. If there
is no keytab, the subdomain handler will fork out a call to
``ipa-getkeytab``, fetch the keytab and store it under
``/var/lib/sss/keytabs``. The ``ipa-getkeytab`` call will be done using
Kerberos credentials the host has. IPA ACIs must be modified accordingly
to allow the IPA server principals to fetch the trust keytabs, but nobody
else. The SSSD invocation of ``ipa-getkeytab`` will not limit the
enctypes in any way, we just rely on IPA creating the objects in LDAP in
the correct manner.

The directory ``/var/lib/sss/keytabs`` must only be accessible to the
sssd user. As an additional security measure, the directory will also
receive a SELinux context stricter than the default ``sssd_var_lib_t``.
That way, processes that are able to access the sssd state directory,
which is public, will not be able to access the keytabs. If fetching the
keytab succeeds, the domain would be enabled. The SELinux policy must
also be adjusted to allow calling ``ipa-getkeytab`` by the ``sssd_be``
process.

If any trust relationships were removed, the corresponding keytabs must
be removed from the disk as well.

Changes to the AD id\_ctx instantiation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With two-way trust, we can keep using the default IPA principal and
keytab.

With one-way trust, the keytab retrieved from the IPA server must be
used. Also, the principal must be passed into the
``ad_create_default_options`` function. The custom values must be set
before we proceed to instantiate LDAP provider options. The only AD
provider option we need to set is AD\_KRB5\_REALM.

In the LDAP provider, we must take care that the following sdap options
are set correctly:

-  SDAP\_SASL\_AUTHID - must be set to the NetBIOS name of the IPA
   domain. (A domain ``TRUST.COM`` would set this value to ``TRUST$``.
   We would use the ``IPA_FLATNAME`` attribute, not truncate the DNS
   domain).
-  SDAP\_SASL\_REALM - must be set to the AD realm
-  SDAP\_KRB5\_KEYTAB - must be set to the per-domain keytab retrieved
   from IPA

The AD provider eventually calls ``sdap_set_sasl_options()`` from the
LDAP provider, we need to make sure this function receives the correct
values. During experimentation we were able to show that using multiple
different SASL users and different realms doesn't cause any problems in
SASL or LDAP libraries.

The only place that will keep using the IPA realm is the failover
instantiation. We need to keep using this hack until failover is
per-backend.

Subdomain offline status changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At the moment, the whole back end can be either online or offline and
the status applies to both the main domain and the subdomains alike. As
an effect, a failure to connect to a subdomain server would also make
the main domain operate offline. In many subdomain setups, it's actually
more convenient not to, because the subdomain server might be on a
different network segment, behind a different firewall etc. Instead, the
domain should only be made inactive.

The ``sss_domain_info`` structure would convert the 'bool disabled'
parameter into an ``enum sss_domain_state``. The supported values would
be:

-  *disabled* - the domain should not be used by either responder or
   provider. It was removed or disabled on the server.
-  *active* - the domain can be used by a responder and the data
   provider would forward its request to the backend
-  *inactive* - the domain can be used by a responder, but the data
   provider would just shortcut as if the domain was offline. For now,
   this option will be used by subdomains only.

The implementation would include renaming the existing
``be_mark_offline()`` function to be called ``be_mark_dom_offline()``
and modifying its behaviour. The existing code that sets the offline
status and runs the offline callbacks would be called for parent domains
only. For subdomains, we would mark the subdomain as inactive and
schedule a tevent request that would unconditionally reset inactive
domain to active. The request would be scheduled after
``offline_timeout`` seconds to be consistent with main domains from
user's perspective. Likewise, the ``be_reset_offline()`` function will
be extended to reset inactive domains to active as well as the SIGUSR1
and SIGUSR2 signal handlers. Finally, all calls to the
``be_is_offline()`` function should be inspected and the invocations
that are per-domain should be converted to a new function
``be_dom_is_offline()`` that would check the offline status for parent
domains and the offline state for subdomains. We should also make sure
the backend offline status structure is opaque as currently its
internals are readable by external users as well. Making the offline
status opaque would make it safer to perform modifications to the
offline code.

In both offline and inactive cases, the ID handlers would reply with
``DP_ERR_OFFLINE``. The crucial difference between offline and inactive
at this point would be that inactive domains are re-activated
unconditionally. When we modify the failover code to handle domains
separately, we'll be able to leverage per-domain online checks or
online/offline callbacks as well.

Detecting re-established trusts and re-fetching the keytabs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The trust keytabs would be fetched on each SSSD restart. This may seem
like a bit of a churn, but retrieving the keytab should be relatively
cheap since the SSSD instance runs on the local server. The advantage of
retrieving the keytabs again is that a simple sssd service restart would
provide an option for the admin to start from a clean slate. Either way,
SSSD service restarts on the server should be quite rare.

In cases the ``sdap_kinit_send()`` request fails, the sdap code would
return a special error code instead of blindly returning ``EIO`` as it
does at the moment. When the ``ipa_get_ad_acct`` request receives this
error code, it would re-run the subdomain request in order to check if
the trust relationship still exists and in order to re-fetch the keytab
again. In order to be able to run the subdomain request separately from
the subdomain back end handler, the subdomain code must be wrapped into
a separate tevent request as the code currently assumes it's being
called from the subdomain backend handler only.

After the keytabs are fetched again, we would attempt to detect if the
trust has been re-established by comparing the keys in the keytab. Using
krb5 calls to read the keytab is fine in the back end code, because the
keytabs will be readable by the SSSD user and could be accessed from the
provider code without elevating privileges. We can't rely on ``kvno``
here, because it is generally always 1. In case the keys differ, then
trust was re-established. In that case would re-set the inactive domain
status and re-run the account request. If the keys are the same, we just
leave the domain as inactive. The ``ipa_ad_trust_ctx`` structure for
each trust would contain a flag that would track that we already tried
refreshing the keytab so that we don't download them on each failed
attempt. This flag would be cleared by the online callbacks (either
periodical or with SIGUSR2).

In case the trust went away, the subdomain code should remove the
trusted domain already with the existing code (however, this must be
tested). In this case, also the keytab must be removed.

Future work
~~~~~~~~~~~

-  Handling failover and offline status on per-domain basis instead of
   per-backend basis should be done in the next release.
-  If we ever need to store the keytabs in the database instead of on
   the filesystem, we might want to switch from calling ipa-getkeytab to
   calling the LDAP extended operation ourselves. However, this is not
   planned at the moment.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

none

How To Test
~~~~~~~~~~~

Establish a one-way trust relationship with an AD domain. Make sure both
IPA and AD users are resolvable. It's prudent to test combinations of
one-way and two-way trusts with different forests. Make sure removing a
trust relationship removes the keytab from the filesystem. Make sure
that SSSD handles re-establishing a trust relationship.

Authors
~~~~~~~

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
