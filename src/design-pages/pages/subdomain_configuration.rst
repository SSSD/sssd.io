.. highlight:: none

Trusted domain configuration
============================

Related ticket(s):
 * https://pagure.io/SSSD/sssd/issue/2599

Problem statement
-----------------
When SSSD is joined to a standalone domain, the Administrator can easily
configure the settings of the joined domain in ``sssd.conf``. However,
when SSSD is joined to a domain that trusts other domain(s), such as
IPA-Active Directory trusts or an Active Directory forest with multiple domains,
the Administrator can `only` tweak settings of the joined domain, but not
any of the trusted domains.

While we introduced the ``subdomain_inherit`` option which works for some
use cases, it does not help if the subdomain needs parameters different
from the main domain and is not user-friendly.

This design page describes a new feature that allows admins to configure
parameters of a trusted domain (a subdomain) in standard SSSD configuration
files in similar way as the main domain's parameters.

Use cases
---------
This section lists two use-cases that were explicitly considered
during design.

Use Case 1: Filtering users from a specific OU in a trusted Active Directory domain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As an Administrator, I want to set a different search base for users and
groups in a trusted Active Directory domain, to filter out users from an
organizational unit that contains only inactive users, so that only active
users and groups are visible to the system.

Use Case 2: Pinning SSSD running on IPA server only to selected Active Directory servers and/or sites
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As an Administrator, I want to disable autodiscovery of Active Directory
servers and sites in the trusted Active Directory domain and instead list
servers and/or sites manually, so that I can limit the list of Active
Directory DCs that SSSD communicates with and avoid reaching out to servers
that are not accessible.

Overview of the solution
------------------------
A new section in SSSD configuration that corresponds to the trusted domain
can be added where the trusted domain options can be set.

This section's base name will be the same as the main domain section with
the ``/<subdomain name>`` suffix, where the ``<subdomain name>`` part
is the trusted domain's name. To read the available domains, including
the autodiscovered trusted ones, run ``sssctl domain-list``. For example
if the main domain's (IPA) name is ``ipadomain.test`` and the trusted
(Active Directory) domain's name is ``addomain.test``, then the configuration
sections will look like this::

    [domain/ipadomain.test]
    # this is the main domain section

    [domain/ipadomain.test/addomain.test]
    # this is the trusted domain section

Note that `not all options available for the main domain will also be
available in the new subdomain section`. Here are some options that will
be supported in upstream version 1.15:

 * ``ldap_search_base``
 * ``ldap_user_search_base``
 * ``ldap_group_search_base``
 * ``ad_server``
 * ``ad_backup_server``
 * ``ad_site``
 * ``use_fully_qualified_names``

Other options might be added later as appropriate. Upstream already plans
on making it possible to add the options previously
settable with ``subdomain_inherit`` with `ticket 3337
<https://pagure.io/SSSD/sssd/issue/3337>`_.

Implementation details
----------------------
In the first iteration, the subdomain initialization code will read the
options directly from the subdomain section, if set.

As an additional improvement, the ``dp_options`` structure will be expanded
with a boolean flag that signifies whether the option is overridable or not
so the code can be made a bit more generic. This work is tracked separately
with `ticket 3336 <https://pagure.io/SSSD/sssd/issue/3336>`_.

How To Test
-----------
This section lists several test cases that are important for users of
this feature.

Test the LDAP search base configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Testing this feature differs when SSSD is directly joined to an Active
Directory domain and when SSSD is running on an IPA client joined to an
IPA domain with trust relationship to an Active Directory domain. When
SSSD is joined directly, the subdomain configuration must be applied on
all clients. In an IPA-AD trust setup, the changes are only needed on the
IPA server as the SSSD on the IPA server is the component that does all
the user and group lookups.

The steps to test this scenario are:

 * Configure an IPA server and set it in a trust relationship with an
   Active Directory domain.
 * In ``sssd.conf`` on the IPA server, add trusted domain section and
   redefine some of the supported search base options for this section
   (for example ``ldap_user_search_base``) to point to only a specific OU::
 
     [domain/ipadomain.test/addomain.test]
     ldap_user_search_base = ou=finance,dc=addomain,dc=test
 
 * Restart SSSD on the server
 * Make sure that only users from within the configured search domain
   are resolvable
 * Please note that when restricting the group search base,
   it is good idea to disable the TokenGroups support, otherwise
   SSSD will still resolve all groups the user is a member of as the
   TokenGroups attribute contains a flat list of SIDs. See also `this blog post
   <https://jhrozek.wordpress.com/2016/12/09/restrict-the-set-of-groups-the-user-is-a-member-of-with-sssd/>`_
   for more details
 * Make sure that also on a IPA client, only the users from within the
   configured search base are resolvable

Debugging
"""""""""
The best way to debug the search base restrictions is to watch the SSSD
logs. The ``sdap_get_generic_*`` functions would log the filter and the
search base used with the search. Please remember to expire the SSSD caches
using ``sss_cache -E`` before issuing the lookup.

Test the AD site and AD server pinning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Similar to the previous test, the configuration differs for direct AD clients
and for IPA-AD trusts. For direct AD clients, the configuration file on all
clients must be modified. For IPA-AD trusts, only the configuration file
on the IPA masters must be changed.  However, note that while user and
group resolution in IPA-AD trust scenario flows through the IPA masters,
authentication is performed directly against the AD DCs. Currently there
is no way, except modifying ``krb5.conf`` on the IPA clients to pin IPA
clients to a particular AD DC server for authentication. This work is
tracked `in a separate ticket <https://pagure.io/SSSD/sssd/issue/3291>`_

For direct AD integration, restricting the AD DCs or the sites would also
work for authentication, as the SSSD would write the address to the AD DC to
contact into a libkrb5 `kdcinfo file` (see ``man sssd_krb5_locator_plugin``).

The steps to test this use-case are:

 * Configure the trusted domain section in ``sssd.conf`` as follows::

    [domain/parentdomain.test/trusteddomain.test]
    ad_server = dc1.trusteddomain.test

 * Restart SSSD
 * Resolve a user or authenticate as a user
 * The SSSD debug logs can be inspected to show what AD DCs were resolved
   and contacted
 * To make sure SSSD connects to the right AD DC, you can firewall off
   other DCs or modify the DNS SRV records for example

Debugging
"""""""""
SSSD logs which serves it contacts when a first request that causes the
connection to be established happens. Please note that the request might
be triggered by internal SSSD scheduling, especially in case of enumeration
or sudo rule download. To trigger reconnection, you can send the ``SIGUSR1``
signal to SSSD to bring it offline, then ``SIGUSR2`` again to force SSSD
to go online. Then issue a lookup with ``getent`` or ``id``.

To debug which DC does SSSD connect to during authentication, it is a good
idea to set the highest ``debug_level`` in the domain section (currently the
``debug_level`` is shared across the joined domain and the trusted domains)
so that the ``krb5_child.log`` and ``ldap_child.log`` files contains also
the ``KRB5_TRACE``-level messages.

Tools such as ``netstat`` or ``tcpdump`` could also be used to observe
the traffic.

Test short names for trusted domains
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using short names for trusted domains also differs between clients joined
directly to AD and clients in an IPA domain with a trust towards an
AD domain.

For the directly joined clients, simply disable the qualified names default
in the subdomains' section::

    [domain/win.trust.test]
    id_provider = ad
    ldap_id_mapping = True
    use_fully_qualified_names = false

    [domain/win.trust.test/child.win.trust.test]
    use_fully_qualified_names = false

If short names are set for a trusted domain, it is a good idea to consider
enabling the ``cache_first`` option to avoid extra LDAP searches across
all domains in case a shortname in a domain defined later in the domain
list is requested.

For IPA-AD trusts, the configuration described above might also work,
but since it has to be set on all clients, it is more convenient
to set the domain resolution order centrally on one of the IPA
servers. The SSSD part of that feature will be described in a separate
design document; the IPA part also has `its own design document
<https://www.freeipa.org/page/V4/AD_User_Short_Names>`_.

Debugging
"""""""""
Logs from both the ``nss`` and ``domain`` sections are useful here. The
logs from the ``nss`` service would show, through the ``cache_req``
functions, which domain's cache was consulted. In case of a cache miss or
cache expiration, the domain logs would show the LDAP searches and whether
the user was found and stored to cache.

Authors
-------
 * Michal Židek <mzidek@redhat.com>
