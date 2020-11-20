Specify the DNS site a client is using
======================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2486 <https://pagure.io/SSSD/sssd/issue/2486>`__

Problem statement
-----------------

Even though the Active Directory provider is able to leverage DNS sites,
the site discovery is always automatic. There is no way to ``pin`` a
particular client into a particular site. This design document describes
a way to do so.

Use cases
---------

The site discovery relies on client being part of subnet. It is not
always practical or even possible to assign GNU/Linux machines to the right
subnet. Still, these clients should be able to leverage the nearest AD
site, even at the expense of manual configuration in ``sssd.conf``.

Overview of the solution
------------------------

The SSSD will gain a new AD provider option that would, if AD sites are
enabled, override any dynamically discovered sites. This option would
pin the client to a particular site not only for primary domain but also
for subdomains. The discovery search would only be used to find the
forest we are enrolled with.

For Global Catalog service discovery of the primary and secondary
domains would then be defined as follows:

-  primary domain - ``$HARDCODED_SITE._sites.$FOREST``
-  backup domain - ``$FOREST``

For pure LDAP searches, the domains would then be defined as:

-  primary domain - ``$HARDCODED_SITE._sites.$DOMAIN``
-  backup domain - ``$DOMAIN``

Above, $FOREST is auto-discovered and $DOMAIN is either the SSSD domain
name as defined in the config file (for the main SSSD domain) or
autodiscovered from object of class ``trustedDomain``.

In both cases, the full DNS search consists of
``_$service._$port.$domain``.

Especially for trusted domains, the overridden search domain might not
return anything, but the DNS resolver code is built such that it
iterates over search domains until the search yields some result.

Authentication against trusted domains
--------------------------------------

For trusted domains, we currently always talk to a local DC which gives
libkrb5 a referral to a trusted-domain specific DC that handles
authentication against a KDC from the trusted domain. This process is
completely opaque to SSSD, which means that Kerberos authentication
doesn't take the sites into account at all.

Implementation details
----------------------

The SSSD AD provider would gain a new option called ``ad_site``. This
option would be unset by default.

The SRV initialization function ``ad_srv_plugin_ctx_init()`` needs to be
adjusted to accept a site override as a ``const char *site_override``
since the site name is just a string. In the default case, where the
option is unset, this option would be set to NULL. In any case, the
``ad_get_client_site_send()/recv()`` request would run to completion
since we need to learn the forest name anyway. If the new option is set,
then the caller of ``ad_get_client_site_recv()`` would still read the
forest value, but ignore the site value and use the value of the
``ad_site`` option instead.

Configuration changes
---------------------

A new option ``ad_site`` as described above. The option would be both
described in man pages and implemented in the configAPI.

How To Test
-----------

The best testing would be performed using an AD test environment
consisting of at least two servers in the same domain. To test, join
both DCs to the same domain. Create two sites such that the IP address
of your SSSD client would set you in one of them.

Make sure that, by default, SSSD creates the kdcinfo file using the DC
in the autodetected site and authenticates you against the DCs from the
autodetected site. The latter can be verified using i.e. tcpdump and
krb5\_child log files.

Set the ``ad_site`` option to a non-default site. Verify, using tcpdump,
kdcinfo file contents and SSSD debug logs that SSSD redirects
communication to DCs in the non-default site.

Authors
-------

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
