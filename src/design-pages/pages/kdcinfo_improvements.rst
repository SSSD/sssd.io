.. highlight:: none

Kdcinfo files for trusted domains
=================================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/3291
    https://pagure.io/SSSD/sssd/issue/3652
    https://pagure.io/SSSD/sssd/issue/941

Problem statement
-----------------
When user authenticates using Kerberos, the KDCs that will actually be
used are typically discovered by libkrb5 with the help of DNS SRV records,
unless the KDCs are configured explicitly in ``/etc/krb5.conf.``

Because the administrator typically expects that the servers they defined
in ``sssd.conf`` would be used for both authentication through SSSD and
for the Kerberos command line tools such as ``kinit``, SSSD provides a
locator plugin for libkrb5 that allows SSSD to inform libkrb5 the servers
SSSD had configured. However, up until now, this plugin was only functional
for the joined domain, not for the trusted domains. This means, that the
administrator had to either rely on the DNS SRC records to be correct
or manually configure ``krb5.conf.``. The former is not true in many
real-world deployments and the latter is non-obvious.and doesn't allow
the administrator to specify e.g.  the Active Directory site.

Use cases
---------
There are three separate, but interconnected use-cases:

 * An SSSD client joined to an Active Directory domain directly
 * SSSD running on an IPA master with a trust established towards an AD domain
 * SSSD running on an IPA client

In all three cases, the information provided by SSSD for the locator
plugin would allow the administrator to pin the SSSD to a specific AD KDC
for authentication using configuration options such as ``ad_server`` or
``ad_site``. In addition, command line tools such as ``kinit`` would then
connect to the DCs discovered by SSSD as well.

Overview of the solution
------------------------
The Kerberos locator plugin reads the address(es) from text files written
by SSSD located in the ``/var/lib/sss/pubconf`` directory.

On a high level, implementing this RFE requires several changes:

 * The code that sets up AD connections to trusted domains when SSSD is
   running on IPA masters must be augmented to create the kdcinfo files that
   the Kerberos locator reads
 * Similarly, the AD provider must be enhances to create the kdcinfo
   files for cases where the SSSD is joined to an AD domain directly
 * Becase the IPA provider on IPA clients is currently only able to perform
   the full fail over for the IPA domain (at the moment the fail over is
   bound to the back end, not the domain), the IPA provider must be extended
   to read a configured list of servers or an AD site from the configuration,
   resolve this input into a list of IP addresses and write the list into
   the kdcinfo files
 * Finally, the Kerberos locator plugin itself must be enhanced to allow
   reading multiple addresses and call the callback function provided
   by libkrb5 for each of the addresses

Implementation details
----------------------
Writing the kdcinfo files on AD clients and IPA masters is a relatively
straightforward change, the ``write_kdcinfo`` flag of the ``krb5_service``
must be set according to the value of the ``krb5_use_kdcinfo`` configuration
option.

The scope of extending the locator plugin is changing the plugin to read
a list of ``(host, port)`` tuples from a newline-separated list in the
kdcinfo file and calling the provided callback function ``cbfunc`` in turn
for each for the addresses.

The biggest change, at least code-wise is the support for the IPA clients.
There, the subdomain provider must first read either the list of servers
from the subdomain section (using the ``ad_server`` option value) or
the AD site from the ``ad_site`` option. If neither of those is present,
the subdomain is skipped. If servers are defined using the ``ad_server``
option, a new resolver request would resolve the host names from this
list into a list of IP addresses and write those into the kdcinfo file.
Care must be taken so that any unresolvable address is just skipped.
If a site is configured, then the IPA subdomains provider would first
resolve the servers in this site using a DNS SRV query and then call the
same request to resolve the host names into addresses as in the case where
the host names were configured. Finally, the addresses are also written
to the kdcinfo files.

In the case where host names are specified using the ``ad_server`` option,
all of the host names will be resolved and written into the kdcinfo file.
In the case where the site is configured, the first 5 host names resolved
from the DNS SRV query will be resolved. Using more host names wouldn't
make sense anyway, because either the SSSD authentication time out would
abort the ``krb5_child`` helper or ``kinit`` itself would time out.

Configuration changes
---------------------
No new configuration options are added. However, on IPA clients
the following configuration::

    [domain/ipa.domain/ad.domain]
    ad_server = dc1.ad.domain, dc2.ad.doma

Or this configuration::

    [domain/ipa.domain/ad.domain]
    ad_site = localsite

Would now trigger the DNS resolution of either the host names
or the site and then the host names in the site and populate
the kdcinfo files.

How To Test
-----------
On an AD client or an IPA master, the kdcinfo files are populated in
response to a request towards the trusted domain. Therefore a valid test
is to make sure that after resolving a user from a trusted domain::

    getent passwd user@child.domain

a valid kdcinfo file with an address of the DC that SSSD contacted in
order to resolve the user is present. Given the example above, the
file would be located at::

    /var/lib/sss/pubconf/kdcinfo.CHILD.DOMAIN

In case of the IPA client, the kdcinfo files are generated after startup
and then subsequently during each periodic invocation of the subdomains
provider

In all cases, either shutting down SSSD or bringing SSSD into the offline
mode (e.g with the ``SIGUSR1`` signal) should remove all the kdcinfo files.

In all cases, calling a command line Kerberos tool such as ``kinit``
should read the kdcinfo file and contact the AD DC specified in the
kdcinfo file. This can be verified using e.g. ``strace.`` or by using
the ``KRB5_TRACE`` variable.

In all cases, disabling the ``krb5_use_kdcinfo`` option must prevent
the kdcinfo files from being generated.

How To Debug
------------
Information on which servers were discovered and written to the kdcinfo
files are present in the SSSD debug logs.

The kdcinfo files are textual and can be inspected using e.g. ``cat``.

Finally, whether the kdcinfo files are being used and which DCs are being
contacted can be seen either in the ``krb5_child.log`` with a very high
debug level (one that enables the KRB5_TRACE messages). Whether the kdcinfo
files are being used from other command line utilities can be inspected
by using the ``KRB5_TRACE`` environment variable, e.g.::

    KRB5_TRACE=/dev/stderr kinit user@DOMAIN

Future development
------------------
At the moment, setting the AD DCs or site must be done on each and every
IPA client by either modifying the sssd.conf file, or (better) dropping
a configuration snippet into the ``/etc/sssd/conf.d`` directory. We would
also like to, in one of the future releases, provide means of mapping an
IPA host or a host group to an AD site so that this configuration can be
done centrally.

Additionally, we would like to extend the kdcinfo file generation on AD
clients as well so that the client can optionally write multiple addresses
into the kdcinfo files in order to provide a way of failing over between
multiple DCs from outside SSSD, for example from ``kinit.``

Authors
-------
 * Sumit Bose <sbose@redhat.com>
 * Jakub Hrozek <jhrozek@redhat.com>
