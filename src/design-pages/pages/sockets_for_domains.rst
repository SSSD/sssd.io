Sockets for domains in a multi-tenant setup
===========================================

Problem statement
-----------------

Currently, sssd offers the following types of sockets, one per
responder:

-  /var/lib/sss/pipes/nss
-  /var/lib/sss/pipes/pac
-  /var/lib/sss/pipes/pam
-  /var/lib/sss/pipes/ssh

That is good for typical OS-level operation where sssd offers services
it has set up (in /etc/sssd/sssd.conf) and offers services about all
domains it is IPA-enrolled to or otherwise configured.

However, if sssd is to be used as an identity and authentication
services for containerized applications, each container might be run
just for one domain or subset of domains configured for host's sssd. For
example, sssd might be configured for domains prod.example.com,
dev.example.com, cust1.example.com, cust2.example.com. The host might
run four containers, and each container should have access to just one
of these domains. Plus fifth container (perhaps some monitoring
application) should have access to prod.example.com, cust1.example.com,
and cust2.example.com.

If we want to use the sssd running on the host and take advantage of
caching and common configuration, access to sssd's services would be
done by mounting the sockets (or directory with the sockets) to the
container. However, the current set of sockets gives access to all
domains and sssd does not have any way to distinguish what the identity
of the peer requesting the service. An attempt was made to add a kernel
call which would allow to determine the cgroups of the peer in non-racey
way but it does not look like the call will be added:
`https://bugzilla.redhat.com/show\_bug.cgi?id=1063939 <https://bugzilla.redhat.com/show_bug.cgi?id=1063939>`__.

Goals
-----

Make it possible for containers to consume services for only a subset of
domains.

Make it possible for sssd to provide services only for a subset of
domains, based on some criteria.

Proposal
--------

Idea
~~~~

Since it is not possible to determine the identity of the peer (which
sssd could then use to map to the list of domains it should serve),
let's make it possible to create on the fly additional sockets which
could then be passed to the container and which would be pre-configured
to only serve certain set of domains. By reading from given socket, sssd
would then know that the peer should only be handled in the context of
one or set of domains.

The sockets need to be created without sssd restarting -- it needs to be
online operation.

Interface
~~~~~~~~~

Add dbus call which would take a list of domains and would return
directory path containing the sockets that can be used when only a given
set of domains should be addressable.

Sssd is welcome to reuse the same directory when the same set of domains
is requested with the next call. So there won't be another set of
sockets created per each new container -- the subsequent calls will just
use the already created ones. Sssd just needs to make sure the list of
domains matches.

Q: should there also be a list of responders that should be supported?
Would that be useful for some use cases, possibly making for more secure
setup?
