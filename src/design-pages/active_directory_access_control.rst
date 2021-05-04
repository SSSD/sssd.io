Adding the ad_access_filter option
==================================

Related ticket(s):

-  `RFE:Add a new option
   ad\_access\_filter <https://pagure.io/SSSD/sssd/issue/2082>`__
-  `RFE:Change the default of
   ldap\_access\_order <https://pagure.io/SSSD/sssd/issue/1975>`__
-  `issues when combining the AD provider and
   ldap\_access\_filter <https://pagure.io/SSSD/sssd/issue/1977>`__

Somewhat related:

-  `Document the best practices for AD access
   control <https://pagure.io/SSSD/sssd/issue/2083>`__

Problem Statement
-----------------

The recommended way of connecting a GNU/Linux client to an Active Directory
domain is using the `AD
provider <http://jhrozek.fedorapeople.org/sssd/1.11.0/man/sssd-ad.5.html>`__.
However, in the default configuration of the Active Directory provider,
only account expiration is checked. Very often, the administrator needs
to restrict the access to the client machine further, limiting the
access to a certain user, group of users, or using some other custom
filtering mechanism. In order to do so, the administrator is required to
use an alternative access control provider. However, none of the
alternatives provide the full required functionality for all users
resolvable by the AD provider, moreover they are hard to configure. This
design page proposes extension of the AD access provider to address
these concerns.

Current access control options
------------------------------

With the existing SSSD, the administrator has two basic means to
restrict access control to the GNU/Linux client - using the `simple access
control
provider <http://jhrozek.fedorapeople.org/sssd/1.11.0/man/sssd-simple.5.html>`__
or configuring the LDAP access control provider. Each approach has its
pros and cons.

Using the simple access provider
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The simple access provider grants or denies access based on the contents
of allow and deny lists. There are separate lists for user and group
names as well as allowed and denied objects.

The following example shows configuration that grants access to user
named ``tux`` and group called ``linuxadmins``. ::

     access_provider = simple
     simple_allow_users = tux
     simple_allow_groups = linuxadmins

-  Pros:

   -  Easy to configure
   -  Realmd provides an interface to configure the simple access
      provider using its CLI

-  Cons:

   -  Account expiration is not checked
   -  Limited expressiveness. No way to combine several clauses
   -  Does not align with the LDAP structure the Active Directory uses

Using the LDAP access provider
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The LDAP access provider offers a way to configure the access control
decision based on whether the user matches a preconfigured filter.
Moreover, the LDAP access provider also offers chaining other LDAP based
checks. For the vanilla AD environment, only account expiration check
applies.

The following example illustrates configuration that allows access to
those users, who are members of group named ``linuxadmins`` AND have a
valid home directory set using the ``ldap_access_filter`` directive. The
users who match the configured filter are also checked whether they are
expired (``ldap_access_order`` contains ``expire``). ::

        access_provider = ldap
        ldap_access_order = filter, expire
        ldap_account_expire_policy = ad
        ldap_access_filter = (&(memberOf=cn=admins,ou=groups,dc=example,dc=com)(unixHomeDirectory=*))
        ldap_sasl_mech = GSSAPI
        ldap_sasl_authid = CLIENT_SHORTNAME$@EXAMPLE.COM
        ldap_schema = ad

-  Pros:

   -  Allows the administrator to base access control on a custom LDAP
      filter, making it possible to combine several conditions
   -  Conditions are not limited to user names or group membership

-  Cons:

   -  Nontrivial and clumsy configuration that must include several low
      level LDAP settings, otherwise set automatically by the AD
      provider. Defeats the whole purpose of the AD provider
   -  The admin needs to combine AD and LDAP providers. Judging by
      experience from triaging support cases with Red Hat support, this
      is a problem for many admins.
   -  Account expiration check must be configured separately, which is
      not obvious
   -  No support for users from trusted AD domains
   -  No realmd integration

Proposed solution
-----------------

The proposal is to add a new access filter configuration option to the
existing AD access provider. Adding the option to the AD provider would
greatly simplify the configuration when compared to the LDAP access
control, while maintaining the full expressiveness of
``ldap_access_filter``. The new option would be called
``ad_access_filter``. If the new option was set, then the AD access
provider would first match the entry against the filter in that option.
If the entry matched, then the account would be checked for expiration.

The following example illustrates an example similar to the one above,
using the proposed AD options: ::

        access_provider = ad
        ad_access_filter = (&(memberOf=cn=admins,ou=groups,dc=example,dc=com)(unixHomeDirectory=*))

The main advantage is simplified configuration. The admin doesn't have
to know or understand what "SASL ID" is.

In comparison with the two legacy solutions explained above:

-  Pros

   -  Easy and intuitive configuration. Only one provider type is
      configured
   -  Sane defaults - always checks for expiration, also checks access
      filter if configured that way
   -  Would support users and groups from trusted domains by leveraging
      the existing AD provider infrastructure

-  Cons

   -  No realmd integration

Realmd integration
------------------

After a short discussion with the realmd upstream maintainer, it was
decided that these options do not fit the realmd use-cases well. If the
user needs to use such advanced techniques as LDAP filters, chances are
that he doesn't need a tool like realmd to set them up in the config
file.

Implementation details
----------------------

#. The default value of what AD access\_provider is set to should be
   changed

   -  Currently, if ``access_provider`` is not set explicitly, the
      default is ``permit``, thus allowing even expired accounts
   -  The new default would be ``ad``, checking account expiration even
      with a minimal configuration

#. A new option would be added. The new option would be called
   ``ad_access_filter``
#. The LDAP access provider must be extended to allow connecting to a GC
   and support subdomains in general

   -  Pass in ``struct sdap_domain`` and ``id_conn`` instead of using
      the connection from ``sdap_id_ctx`` directly
   -  The code must not read the ``sss_domain_info`` from ``be_ctx`` but
      only from ``sdap_domain`` in order to support subdomain users

#. The AD access provider must call the improved LDAP access provider
   internally with the right connection

   -  The default should be GC
   -  If POSIX attributes are in use and GC lookup wouldn't match,
      optionally fall back to LDAP. This fallback could be tried just
      once to speed up subsequent access control

#. The default chain of LDAP access filter the AD provider sets
   internally must be changed.

   -  Currently AD provider sets ``ldap_access_order=expire``. If (and
      only if) ``ad_access_filter`` was set, the LDAP chain would become
      ``ldap_access_order=filter,expire``

Parsing the ``ad_access_filter`` option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. The ``ad_access_filter`` option is a comma-separated list of filters
   that apply globally, per-domain or per-forest. The most specific
   match is used
#. If the ``ad_access_filter`` value starts with an opening bracket
   ``(``, it is used as a filter for all entries from all domains and
   forests

   -  example:
      ``(&(memberOf=cn=admins,ou=groups,dc=example,dc=com)(unixHomeDirectory=*))``

#. More advanced format can be used to restrict the filter to a specific
   domain or a specific forest. This format is ``KEYWORD:NAME:FILTER``

   -  KEYWORD can be one of ``DOM`` or ``FOREST``

      -  KEYWORD can be missing

   -  NAME is a label.

      -  if KEYWORD equals ``DOM`` or missing completely, the filter is
         applied for users from domain named NAME only
      -  if KEYWORD equals ``FOREST``, the filter is applied on users
         from forest named NAME only

   -  examples of valid filters are:

      -  apply filter on domain called dom1 only:

         -  ``dom1:(memberOf=cn=admins,ou=groups,dc=dom1,dc=com)``

      -  apply filter on domain called dom2 only:

         -  ``DOM:dom2:(memberOf=cn=admins,ou=groups,dc=dom2,dc=com)``

      -  apply filter on forest called EXAMPLE.COM only:

         -  ``FOREST:EXAMPLE.COM:(memberOf=cn=admins,ou=groups,dc=example,dc=com)``

#. If no filter matches the user's domain, access is denied

   -  example
      ``ad_access_filter = dom1:(memberOf=cn=admins,ou=groups,dc=dom1,dc=com), dom2:(memberOf=cn=admins,ou=groups,dc=dom2,dc=com)``,
      user logs in from dom3

Contingency plan
----------------

None needed. The existing options would still exist and function as they
do now.

How to test
-----------

#. Check that ``access_provider=ad`` without any other options allows
   non-expired users
#. Check that ``access_provider=ad`` without any other options denies
   expired users
#. Test that setting ``ad_access_filter`` restricts access to users who
   match the filter

   -  test that an expired user, even though he matches the filter, is
      denied access
   -  this test must include users from the primary domain as well as a
      sub domain
   -  Different filters should be tested to make sure the most specific
      filter applies

      -  example: add a restrictive filter for dom1 and permissive
         filter without specifying the domain. A user from dom1 must be
         denied access, while a user from other domain must be allowed
         access

#. When access is denied, the SSSD PAM responder must return a
   reasonable return code (6)

Future and optional enhancements
--------------------------------

In the future, we should extend the ``access_provider`` option itself
and allow chaining access providers. This enhancement would allow even
more flexibility and would allow the administrator to combine different
access providers, but is outside the scope of the change described by
this design page.

Author(s)
---------

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
-  Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
