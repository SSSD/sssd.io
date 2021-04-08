.. highlight:: none

Multiple server addresses or names in kdcinfo files
===================================================

Related ticket(s):
------------------
   * https://pagure.io/SSSD/sssd/issue/3973
   * https://pagure.io/SSSD/sssd/issue/3974
   * https://pagure.io/SSSD/sssd/issue/3975


Problem statement
-----------------
When a user authenticates using Kerberos, the KDCs that will actually be
used are either discovered by libkrb5 with the help of DNS SRV records,
or the KDCs are configured explicitly in ``/etc/krb5.conf.`` or provided
by a special `locator plugin`.

Because the administrator expects that the servers they defined in
``sssd.conf`` would be used for both authentication through SSSD and by
applications that use libkrb5, such the Kerberos command line tools like
``kinit``, SSSD provides a locator plugin for libkrb5 that allows SSSD to
inform libkrb5 about the servers SSSD had configured.

However, SSSD, at least in the typical use case, only writes the information
about the single server it connects to and changes the address only when
the daemon reconnects to a different server. This creates a problem in case
the server whose address is written in the kdcinfo file is unreachable
but no action towards sssd that would provoke a fail over (such as a
user login over PAM) is executed. In that case, the kdcinfo file contains
stale entries and because from libkrb5 point of view, the kdcinfo files
are authoritative and if the information present there is not useful,
libkrb5 cannot reach any KDCs from that domain.

To improve the situation, this design page proposes adding a new sssd option
that, if set, would enable sssd to write additional host names into the
kdcinfo files which would then allow the plugin to iterate over these
items and in turn allow libkrb5 to have sort of a failover for entries
configured in sssd.conf or autodiscovered by SSSD.

Use cases
---------
A typical sequence that triggers this problem is this:
   * log in with a PAM service to a machine. This causes a KDC address to
     be written to the kdcinfo file
   * disable the KDC server, e.g. by enabling a restrictive firewall rule
   * call kinit on the client where the kdcinfo file was written

Overview of the solution
------------------------
The Kerberos locator plugin reads the address(es) from per-realm text files
written by SSSD located in the ``/var/lib/sss/pubconf`` directory. At the
moment, the plugin can already read multiple entries, but currently only
numerical addresses are supported.

On a high level, implementing this RFE requires several changes:
   * change the Kerberos locator plugin so that it can also consume
     host names in addition to numerical addresses. These host names
     would be resolved in the plugin itself and passed to libkrb5 with
     the help of a callback function libkrb5 provides to the plugin
   * add a new SSSD option that would limit the number of entries that
     SSSD writes to the kdcinfo plugin. This is needed to avoid time
     outs in case the network was truly unreachable. The default value
     of the option could perhaps be different in master and sssd-1-16
     where master could default to writing multiple entries, but
     sssd-1-16 would default the option to 0 in order to not change
     behaviour of a stable branch.
   * extend the online callback which the SSSD fail over component uses
     to write the current server to the kdcinfo files to also write
     additional server host names in addition to the current server address
   * to enable writing multiple server addresses, the request to resolve
     a server for a service should be extended to resolve host names
     up to the specified limit

When it comes to resolving the servers, there are several scenarios to
consider:

   * The servers can be enumerated using an option. This includes
     ``krb5_server/krb5_backup_server`` for the krb5 provider and
     ``ipa_server/ipa_backup_server`` and ``ad_server/ad_backup_server``
     for the IPA and AD providers.
   * The servers can be completely autodiscovered. Typically this is
     done by either omitting the ``*_server`` options completely or
     using the ``_srv_`` identifier. As long as the list is omitted
     or the ``_srv_`` record is the first one in the list, any fail
     over service resolution would trigger the DNS SRV lookups and
     resolve the whole list. It is useful to note that the ``_srv_``
     identifier is not permitted in the backup server list explicitly,
     but the AD provider does resolve a SRV query into the backup
     server list. That is done in case an AD site is used, then the servers
     from the AD site are added as 'primary' and the global servers
     form the 'backup' list.
   * A mix of the above. The most complex case from the point of
     this RFE is a list that starts with a host name, but includes
     the ``_srv_`` identifier later on, e.g. ``krb5_server = kdc.example.com,
     _srv_``. In this case, currently calling the fail over resolution
     would only resolve the host name of ``kdc.example.com``, but not
     the SRV query, so unless the fail over code is extended, the
     host names originating from the SRV query would not be known
     after the service resolution finishes.

Implementation details
----------------------
The interface the locator plugin uses to communicate with libkrb5 is a
callback function provided by the caller (libkrb5), SSSD is supposed
to pass a struct sockaddr to the caller. The Kerberos locator plugin
is already capable of iterating over multiple addresses, but currently
really only numerical addresses are supported and the plugin converts
the string representation of the address into struct sockaddr by calling
``getaddrinfo(3)`` with the ``AI_NUMERICHOST`` parameter. We should extend
the locator plugin code by calling getaddrinfo for entries that do not
represent an address to resolve a host name and pass its address. This
can be a first self-contained step in the implementation.

The kdcinfo files are written (using ``write_krb5info_file``) either
during an online callback or in a special-case for IPA trust clients. The
special case is already doing something similar to what this page
is about by looking into a subsection representing a trusted domain
(e.g. ``[domain/ipa.test/win.trust.test]``) and resolving all the servers
in that list either by name or based on a site selection. However, this
is done during the subdomain provider operation, not during a resolver
callback and all the addresses configured in the ``sssd.conf`` file are
always resolved and written to the config file.

The ``write_krb5info_file`` receives a linked list of ``struct fo_server``
structures which contains the address, if already resolved, or at least
a host name in the ``struct server_common`` member structure. Since the
callback should already be synchronous and not do much work on its own, it
would be best if the callback was already invoked with the data provided,

There are two kinds of servers in the fail over module - primary and
backup.  The backup servers are supposed to only be used temporarily
and sssd periodically tries to connect to one of the primary servers.
However, from the fail over code point of view, even adding a "backup"
server still means the server is added to the same linked list, just with
a flag denoting that the server is not primary, therfore iterating over
a single list would iterate over both the primary and backup servers.

Before changing the online callbacks, it would be useful to implement and
read the ``krb5_kdcinfo_lookahead`` option so that there is already an
upper limit when the callbacks write the extra host names.

The next step of implementation could be extending the online
callbacks that call the ``write_krb5info_file`` functions. There are
several of them, ``ad_resolve_callback``, ``ipa_resolve_callback``
and ``krb5_resolve_callback``. The callbacks receive the current
``struct fo_server`` instance. The callbacks would then keep iterating
over the linked list until either the list is exhausted or as many as
``krb5_kdcinfo_lookahead`` items are processed. The host name from the
``struct server_common`` structure would be read using ``fo_get_server_name``
and written to the array passed to ``write_krb5info_file``.

One question to consider is whether to use the ``fo_server`` instances before
the current one, i.e. those that SSSD tried before and couldn't connect to.
I think it would make sense to add them to the end of the list, at least
for the primary servers not from a SRV query, because sssd never reconnects
to a server earlier in the list as long as later server works. The SRV queries
are different in this respect in the sense that they time out and force
SSSD to resolve the whole list once a server is requested again (typically
either during authentication or once the LDAP connection expires).

Finally, the case where the fail over code needs to do additional lookups
in order to resolve at least the amount of host names requested by the
``krb5_kdcinfo_lookahead`` should be addressed. The caller that initializes
the fail over service (maybe with ``be_fo_add_service``) should provide
a hint with the value of the lookahead option. Then, if a request for
server resolution is triggered, the fail over code would resolve a server
and afterwards check if enough ``fo_server`` entries with a valid hostname
in the ``struct server_common`` structure. If not, the request would
check if any of the ``fo_server`` structures represents a SRV query and
try to resolve the query to receive more host names.

Configuration changes
---------------------
A new configuration option called ``krb5_kdcinfo_lookahead`` would be added.
This option would default to a sensible non-zero value in the master
branch, perhaps 3 so that attempting to resolve the extra host names does
not cause the libkrb5 operation to time out. If the patches are backported
to any stable branch, the option must default to 0 (disabled).

In the first iteration, we might want to just read a single number, but
in the future, the option should be extended to accept two numbers in the
``total:backup`` notation. This would mean write up to ``total`` servers,
but include up to ``backup`` servers from the backup list. This would be
useful in case none of the servers from the primary list are reachable,
because e.g. they all come from the same AD site, but servers outside the
site are reachable. This extension would only make sense if SSSD does not
resolve the host names on its own, which might be another future extension.

It might be a good idea to add a note to the ``sssd-ad`` and ``sssd-ipa``
man pages or even the shared fail over man page include file with a pointer
to how the kdcinfo files work so that the information is easy to discover
for administrators.

How To Test
-----------
Plugin test
   With any of the below tests or even after writing the host names to
   the kdcinfo files directly, make sure the first entry in the list is
   unreachable. Then call e.g. `kinit` and check that the operation succeeds.

Backwards compatibility test
   Set the ``krb5_kdcinfo_lookahead`` option to 0. Define multiple servers
   and perform Kerberos authentication. Make sure that only the current server
   is written to the kdcinfo files.

Write a list of servers
   Set the ``krb5_resolve_callback`` to a positive value. Make sure that the
   first entry in the kdcinfo files is an address and the other entries are
   host names from the configuration. This test case should be extended to
   make sure only so many entries as the value of the option are written,
   or if there are fewer entries in the config file, all are writen.

Fail over test
   Similar to the above, except make sure the first entry in the list cannot
   be contacted. Then, SSSD should resolve the next entry to the address
   and if applicable write the rest of the list.

Backup server test
   At the minimum, we should make sure that servers from the backup list
   are written to the kdcinfo files. If the option would implement the split
   ``total:backup`` value, then those should be tested as well.

(Optional) writing a previously tried, not working server
   If it is agreed during design review that also not working servers are to
   be written to the kdcinfo files (see the section about not working
   servers), then a test case should make sure those
   are written to the end of the list.

SRV resolution test
   Leave the server list (e.g. ``krb5_server``) option empty. Make sure
   a DNS SRV query for the configured realm returns valid servers and
   they are written to the config file.

Combined SRV and server list
   Set the ``krb5_server`` option to ``hostname, _srv_``. Set the
   ``krb5_kdcinfo_lookahead`` option to a value greater than 1. Make
   sure that the host names from the DNS SRV query are also present
   in the kdcinfo files.

IPA client test
   The test cases above should be repeated for an IPA client as well in
   case the IPA online callbacks are modified.

AD site test
   Add an AD client to a site or set the site in the config file. Make
   sure that the servers from the site are written first, followed
   by the global servers up to the ``krb5_kdcinfo_lookahead`` value.

How To Debug
------------
Any new code must be decorated with DEBUG messages. To debug the locator
plugin changes, using ``KRB5_TRACE`` or even calling ``strace`` might be
useful.

Future development
------------------
First, it might be useful to extend the resolver or fail over code to resolve
the names on its own to save some potentially blocking calls in the plugin.
There is already an example of ``resolv_hostport_list_send`` that can perhaps
be reused.

Additionally, we already plan for some time to include connectivity checks
with cLDAP ping or just plain ``connect()`` to make sure that servers that
cannot be contacted at all are not tried. This is of course outside of the
scope of this work, but should be kept in mind to not implement something
incompatible.

Authors
-------
 * Sumit Bose <sbose@redhat.com>
 * Tomas Halman <thalman@redhat.com>
 * Jakub Hrozek <jhrozek@redhat.com>
