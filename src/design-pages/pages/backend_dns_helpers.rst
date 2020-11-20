.. highlight:: none

Backend DNS Helpers
===================

Problem Statement
-----------------

In our back ends we need to be able to find out which server we are
supposed to connect to. We have various ways to define a server, such as
using lists of servers, or a Service type, and then using DNS SRV
records, or in some cases other ways (for example, CLDAP queries for AD
Sites, Location discovery for IPA, etc.). Because our back ends use
asynchronous calls, we also need to be able to resolve DNS domain names
asynchronously to avoid stalling other operations (such as Kerberos
authentication for a user while trying to resolve the LDAP identity
server name). We need to be able to handle fallback cases and have
blacklists of servers we know are not reachable. We also want to be able
to share this information between the authentication, identity and other
providers within the same back end/domain.

General Approach
----------------

Given that most back ends need to configure servers to reach and need to
resolve their names and possibly allow for fallbacks to secondary
servers, a general mechanism should be provided for back ends so that we
have common basic helpers. Because some providers need the same
information (example: ldap id + Kerberos auth providers want to connect
to the same IPA server) it also make sense to provide this functionality
as a back end function.

The idea is to init a common set of structures to hold data + methods
that are passed to the providers at initialization time. More advanced
providers (IPA, AD) that have special needs for DNS discovery will also
be able to override the default helpers, otherwise the providers will
simply use the default common facility.

The helpers will use the tevent\_req interface and will be completely
asynchronous.

Methods
-------

We need a few basic methods to start:

#. Initialization method, to which we pass a list of servers:service we
   need to connect to from the specified provider. The first provider
   that sets up the list will initialize defaults; if no other provider
   adds any server:service item during initialization the default ones
   will be used by all.

2. A secondary implementation method that provides a DNS domain and the
   request to resolve SRV records instead of (or in addition to)
   providing a list of servers:services. The helper will decide when it
   is time to refresh the SRV list.

3. A simple method to ask for the first available server of type service
   in the list for this provider.

4. A method to give feedback about a returned result. If the resolved
   server is not reachable it should be blacklisted for some time. If
   all servers are blacklisted we should consider putting the whole
   domain offline.

State Information
-----------------

In the initial implementation the black and white lists of servers will
be kept in memory. This means that any status will be lost if the
process is restarted. In future we may decide to cache the lists on
persistent storage (the domain's LDB file) to avoid delays on quick
restarts.

Configuration
-------------

The first implementation step will focus on manually configured lists
and the default resolution mechanism. The list of servers can be
explicitly configured in sssd.conf.

The list can:

#. Include host names, host IP addresses in v4 format or host IP
   addresses in v6 format, and optionally a port number
#. Can have just one or multiple items
#. Can specify a domain name to be used to resolve SRV records
#. Can be empty in which case a default domain will be used (recovered
   from the host name or the domain options in resolv.conf)

SRV records are not used if an explicit list is provided. This is the
behaviour of the default helpers; other providers can provide their own
resolution methods.
