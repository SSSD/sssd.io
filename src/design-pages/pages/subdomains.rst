Sub-Domains in SSSD
-------------------

Currently SSSD assumes that each domain configured in sssd.conf
represents exactly one domain in the backend. For example if only the
domains DOM1 and DOM2 are configured in sssd.conf a request for a user
for DOMX will return an error message and no backend is queried.

In an environment where different domains can trust each other and SSSD
shall handle user from domains trusting each other every single domain
must be configured in sssd.conf. Besides that this is cumbersome there
is an additional issue with respect to group memberships. SSSD by design
does not support group memberships between different configured domains,
e.g. a user A from domain DOM1 cannot be a member of group G from domain
DOM2.

It would be nice if SSSD can support trusted domains in the sense that

-  only one domain has to be configured in sssd.conf and all trusted
   domains are available through SSSD
-  a user can be a member of a group in a different trusted domain

To achieve this SSSD must support the concept of domains inside of a
configured domain which we like to call sub-domain in the following.
Instead of creating a list of know domains from the data in sssd.conf
the PAM and NSS responder must query each backend for the names of the
domains the backend can handle. If the backend does not support the new
request the domain name from sssd.conf must be used as a fallback.

If a request for a simple user name (without @domain\_name, i.e. no
domain name is know) is received the first configured domain in
sssd.conf and all its sub-domains is queried first before moving to the
next configured domains and its sub-domains.

If a request with a fully qualified user name is received the backend
handling this (sub-)domain is queried directly. If the requested domain
is not know the configured domains are asked again for a list a
supported domains with a

-  force flag to indicate the the backed should try to updated the list
   of trusted domains unconditionally
-  the name of the unknown domain which can be used as a hint in the
   backend to find the specific domain and see if it is a trusted domain
   (the backend may pass this hint on to a configured server and let the
   server do the work)

This process might take some but since it will only happen once for each
unknown domain and there may be environment where it is only possible to
find a trusted domain with the help of the domain name this is
acceptable. Nevertheless, since a search for an unknown domain will lead
to some amount of network activity and system load there should be some
precaution implemented to avoid attacks based on random domain names
(maybe blacklists and timeouts).

With these considerations three development tasks can be identified to
add sub-domain support to SSSD

-  new get\_domains method: a new method to get the list of supported
   domains from the backend must be defined so that the responders and
   providers can use them
-  add get\_domains to providers: providers which can handled trusted
   domains, currently IPA and winbind, must implement the new method
-  add get\_domains to the responders: the responders must call
   get\_domains to get a list of supported domains and use the
   configured domain name as a fallback (this might be split into two
   task, first call get\_domains once at startup without force flag and
   name of searched domain; second call get\_domains if domain cannot be
   found with force flag and name of searched domain)

The first task must be solved first but is only a minor effort. The other
two must wait for the first but also require some more work.

For the first implementation it is sufficient that sub-domains work only
if the user name is fully qualified and that the domain name has to be
given in full and that short domain names are not supported. But it
should be kept in mind user names in general are not fully qualified and
that there are trust environments where short names are available to
safe some typing for the users.
