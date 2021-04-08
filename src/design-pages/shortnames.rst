.. highlight:: none

Shortnames in trusted domains
=============================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/3001

Problem statement
-----------------
When SSSD is joined to a standalone domain, user & group resolution and user
authentication can be done only using the short names without the domain
component. The same does not happen in a trust relationship with an AD forest,
where the fully-qualified names have to be explicitly used.

Use cases
---------
Allow the Administrator of an IdM deployment in a trust relationship with an AD
forest to configure its IdM servers and associated IdM clients to allow user
& group resolution and user authentication in all domains (or a subset of the
domains) to be possible by using only the short names without the domain
component, as it's done by some 3rd party solutions.
It's important to mention that the Administrator has also the possibility to
configure it for directly AD joined clients, although it cannot be done in a
centralized way (meaning that the configuration has to be done per SSSD
client).

Overview of the solution
------------------------
In order to have it implemented a few internal changes have to be done in order
to use the shared ``cache_req`` module for responder look-ups, allowing then
SSSD to perform the domain-less look-ups when not explicitly set up in the
domain to use only fully-qualified names for those operations.

Once domain-less searches are allowed, SSSD will have to support receiving an
ordered list of domains which will be looked-up first so the Administrator can
have a better control and avoid a bunch of unnecessary look-ups. The list of
the ordered domains can be provided in three different ways and those are
described below according to their precedence order:

* sssd.conf: the admin can set up the ``domain_resolution_order`` option in
  the ``[sssd]`` section;
* ``ipaDomainResolutionOrder`` set by IPA ID-view: the admin can set up the
  attribute per views on IPA server;
* ``ipaDomainResolutionOrder`` set globally: the admin can set up the attribute
  globally on IPA server;

In case some method, for some reason, fails to be applied there's an automatic
fallback to the next method (of course, respecting the precedence order).

In case there are conflicting names (like Administrator) the first name matched
will be returned, so it's recommended to use fully-qualified names on those
situations.

Once it's done and the subdomain where the look-up will be done allows the
use of non-fully-qualified names the Administrator is ready to make use of
this new feature.

It's really important to mention that the domain resolution order will be
**completely** ignored in case the domain has ``use_fully_qualified_names``
configure option set to ``True``.

Implementation details
----------------------
This section will focus on the changes done after having the ``cache_req``
module being used by the responders.

Basically a few parts of SSSD have to be changed in order to have this
feature in place:

 * subdomains: The subdomains have to support the ``use_fully_qualified_names``
   configure option;

 * ipa/sysdb: Those two parts have to support fetching and storing the
   ``ipaDomainResolutionOrder`` attribute from IPA servers, so those can be
   used for SSSD when performing the look-ups;

 * cache_req: This is the part that has been changed more and the changes are:

   * Descend into all subdomains during the lookups: It has been changed for
     all cache_req plugins but the "host_by_name" one;

   * When processing the domains a new list of domains is built, basically by
     doing:

     * Add the domains specified by ``domain_resolution_order`` (or
       equivalent method to set those up);

     * Add all other domains by the order they're presented in the
       ``sssd.conf`` file, flattening those so it's ensured that a look-up
       will reach all the domains' subdomains. Is important to mention that
       the subdomains, when not specified, are added to the flatten list of
       domains in a random order;

Configuration changes
---------------------
The configuration changes on SSSD side are quite simple:

 * ``domain_resolution_order`` ::

    [sssd]
    ...
    domain_resolution_order = ad.example, ipa.example
    ...

 * subdomain changes::

    [domain/ipa.example/ad.example]
    use_fully_qualified_names = False

How To Test
-----------
For testing this feature the person you'll have to have an environment with a
working AD Trust relationship and then follow at least one of the following
methods:

 * Client side: Set up ``domain_resolution_order`` attribute in [sssd]'s
   section of sssd.conf file::

    [sssd]
    ...
    domain_resolution_order = ad.example, ipa.example
    ...

 * IPA side:

   * View: Once a view is properly set up, the person can just call::

     # ipa idview-mod --domain-resolution-order="ad.example:ipa.example"

   * Globally::

     # ipa config-mod --domain-resolution-order="ad.example:ipa.example"

NOTE: Yes, the list set up on IPA side is separated by colon (:) while the one
in SSSD side is separated by comma (.).

And that's all. With those changes the operations that could be done using
fully-qualified-names now can be done by just using shortnames (obviously,
having exactly the same results).

How To Debug
------------
The best way to debug this feature is actually diving into the logs generated
by ``cache_req``, which shows the exactly order the look-up followed during the
request.

For instance::

    $ id Administrator

Will generate logs like (this is part of NSS logs)::

    CR #0: Setting name [Administrator]
    CR #0: Performing a multi-domain search
    ...
    CR #0: Using domain [ipa.example]
    ...
    CR #0: Using domain [ad.example]

Authors
-------
 * Fabiano Fidencio <fidencio@redhat.com>
 * Jakub Hrozek <jhrozek@redhat.com>
