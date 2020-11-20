Support for non-POSIX users and groups
======================================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/3310

Problem statement
-----------------
SSSD, with its D-Bus interface is appealing to applications as a gateway
to an LDAP directory where users and groups are stored. However, contrary
to the traditional SSSD deployment where all users and groups either have
POSIX attributes or those attributes can be inferred from the Windows SIDs,
in many cases the users and groups in the application support scenario have
no POSIX attributes. At the same time, SSSD especially on the back end
(LDAP provider) level currently requires the presence of either an UID
number or a Windows SID.

This feature tracks adding support for user and group resolution through
the D-Bus interface and authn/authz through the PAM interface even for
setups without UIDs or Windows SIDs present on the LDAP directory side.

Use cases
---------
 * As an application developer, I want to fetch user attributes for my
   application from an LDAP server that only uses a fairly generic LDAP
   objectclasses such as ``groupOfNames`` for groups or ``person`` for users.
   The application can either issue D-Bus calls itself or rely on Apache modules
   such as `mod_lookup_identity <https://github.com/adelton/mod_lookup_identity/>`_
 * As an application developer, I want to authenticate users to my
   application using the
   `mod_authnz_pam <https://github.com/adelton/mod_authnz_pam>`_ module even if
   the users lack PAM attributes.

Overview of the solution
------------------------
On a high level, the biggest change is tweaking the internal LDAP searches
so that they are less restrictive and match users and groups based on just
the requested key (typically a name or a UPN) and the configured objectclass.

Whether SSSD will restrict the lookups to only POSIX accounts or allow even
non-POSIX lookups will be controlled `at the domain level`. This is important
for several reasons:

    * To avoid "leaking" the non-POSIX accounts or, perhaps more importantly,
      their non-POSIX group memberships to interfaces such as NSS that otherwise
      require a complete POSIX entry. While these checks could be implemented by
      the POSIX interfaces as well, making the distinction at the domain level
      is much safer.

    * To minimize the number of inconsistencies. These include:

      * One interface requesting a non-POSIX user through a D-Bus call,
        then later a POSIX interface searching for the same user. The latter
        call, having a more restrictive filter, would not match the object
        in the domain and because we tend to treat the domain reply as
        authoritative, remove the cached non-POSIX users.

      * Mixed POSIX and non-POSIX group memberships would require a large amount
        of special-casing and very careful testing to make sure requests
        for such hybrid user would return the correct group memberships
        but at the same time not remove the non-POSIX parts in all cases.

      * Interfaces that serve both the POSIX and non-POSIX case such as
        the D-Bus interface need to know whether to return only the list
        of POSIX group membership if a user that has POSIX attributes
        is requested. The interfaces cannot assume the intent of the caller and
        forcing the caller to decide based on the target domain helps here.

In short, by forcing to make the distinction on the domain level, the SSSD
code would be made more robust and error-prone while limiting the complexity.

Configuration-wise, this change would allow to define a new section type
in SSSD called ``[application]`` in addition to the current ``[domain]``.
Internally, this would create an SSSD domain as well, just marked as a
non-POSIX one.

An application domain section can be either defined as a standalone
domain, listing all the needed options or can be used in conjunction with
a traditional POSIX domain in mixed setups. In this case, the application
domain can use the ``inherit_from`` option to inherit all options from the
"sibling" POSIX domain.  Any options specified in the application domain
override the POSIX domain options. Examples of both are given in the
"How to test" section below.

An application domain would be skipped during lookups by interfaces that
require POSIX attributes, such as ``sudo`` or ``NSS``. Better distinction
must be made for interfaces that support both POSIX and non-POSIX users,
though and the details are discussed below.

In the simplest case, only a single domain will be defined. The tricky part
are setups that must serve data to both the application from a non-POSIX
domain and for the OS. For these setups, two ``[domain/]`` sections pointing
to the same remote server must be defined, one marked as ``posix`` and one
marked as ``application`` type (see below).

To distinguish between accounts with the same name that exist in both
these domains by interfaces that support both POSIX and application domains,
a qualified name is the safest way.

In addition, the PAM responder will keep a list of application PAM services
so that if an unqualified name arrives from an OS-level PAM service (such
as ``ssh``), the PAM responder will know it is safe to skip the application
domains and route the PAM request to POSIX domains only. This would make life
easier for accounts that both use the application and OS-level PAM services
in the sense that the OS-level PAM interface will be usable even without
qualified names.

For distinguishing accounts between a POSIX and an application domain from
the D-Bus interface, a fully qualified name must be used. But since the
D-Bus interface is normally used only by the application, putting the
application domain first in the ``domains`` list should be enough to avoid
using qualified names from the application while still making it possible
to use the POSIX domain defined as second in the list.

Configuration changes
---------------------
A new SSSD domain option will be added. The option will be called
``domain_type`` and would support two values - ``posix`` and ``application``.
The default value will be ``posix``, the non-POSIX support will be enabled
by setting the ``domain_type`` to ``application``. This option will, however,
not be typically used. Instead, the ``application`` domain (see below)
would be defined.

A new ``application`` section will be read. The ``application`` section
will internally unroll into a ``domain`` section with ``domain_type``
set to ``application``. Additionally, the ``application`` section will enable
the administrator to link the application domain with a POSIX domain through
the ``inherit_from`` option described above.

The ``pam`` responder will gain a new option ``pam_app_services``. This
option will be empty by default. Only PAM services listed in this option will
be allowed to contact the ``application`` domains. This option will be added
to make sure that unqualified names can still be used in PAM conversations
in case both ``posix`` and ``applications`` domains are configured for SSSD.
In future, we might add a similar option (with ``UID`` of the caller of
the interface as the key) to the ``ifp`` responder as well, but such option
will not be added in the first iteration.

Implementation details
----------------------
When the ``domain_type`` is set to ``application``, SSSD responders that
are only usable on a POSIX system (currently ``nss``, ``ssh``, ``sudo``,
``kcm`` and ``secrets``) will skip over ``application`` type domains. This
logic will be implemented at the ``cache_req`` level and set by the caller,
which is the responder, by adding a ``cache_req`` option. In particular,
the ``cache_req`` requests will include an enum with allowed values
``CACHE_REQ_POSIX`` and ``CACHE_REQ_APP`` where the POSIX responders will
only use the ``CACHE_REQ_POSIX`` value. The logic that determines which
value the ``ifp`` and ``pam`` responders use is described below.

The responders that are usable by both applications and the OS as well
(that's ``pam`` and ``ifp``) will set a flag for the ``cache_req``
request that will instruct the ``cache_req`` domain-loop to also consider
``application`` domains.

The ``ifp`` responder will consider ``application`` domains for all requests.
Therefore in order to resolve a POSIX user with only POSIX membership, the
request towards the ``ifp`` interface must be qualified with the domain name.

The ``pam`` responder will route requests only to POSIX domains by default.
Requests coming from PAM services listed in the ``pam_app_services`` option
will on the other hand only be routed to application domains.

The last change needed is for Kerberos authentication. Since the Kerberos
ticket returned cannot be owned by a POSIX owner in application domains,
especially in cases the system would otherwise use a FILE-based ccache,
we will use a temporary MEMORY-based ccache in the ``krb5_child`` process
destroy the ticket when ``krb5_child`` finishes and only return the resulting
error code from the child process to the Data Provider.

How To Test
-----------
The best way of testing this feature is to test the "full stack" together
with an application and the Apache modules. However, at the moment there
is a `bug in mod_lookup_identity
<https://bugzilla.redhat.com/show_bug.cgi?id=14367331>`_
that prevents the non-POSIX lookups from working.

However, isolated testing can be performed as well. All tests expect that the
LDAP server is populated with entries that do not contain POSIX attributes
or might contain POSIX attributes in the case of mixed setup tests. For testing
PAM authn and authz, the ``pam_test_client`` binary built from SSSD sources
can be used until ``sssctl`` provides a better way by fixing
https://pagure.io/SSSD/sssd/issue/3292.

The users in the test setup should be members of non-POSIX groups, or a
mix of POSIX and non-POSIX groups in the mixed scenario setups.

    #. SSSD with only the ``application`` domain can be reached through
       the D-Bus and PAM interfaces

       * Add a domain as follows::

            [sssd]
            domains = appdomain.test
            services = ifp, pam, nss

            [pam]
            pam_app_services = sss_test

            [ifp]
            user_attributes = +phone

            [application/appdomain.test]
            id_provider = ldap
            ldap_uri = ldap://server.test
            ldap_search_base = dc=test
            ldap_user_extra_attrs = phone:telephoneNumber

       * Note that the ``nss`` responder is added for testing purposes
         only to prove that the non-POSIX users cannot be resolved. The
         ``nss`` service can be removed in production. Also note that on
         a modern distribution, all the services can be socket-activated,
         so the services line is not required at all.

       * Make sure that a D-Bus call towards the SSSD interface can resolve
         the ``phone`` attribute of ``$user``::

            dbus-send --print-reply \
                      --system \
                      --dest=org.freedesktop.sssd.infopipe \
                      /org/freedesktop/sssd/infopipe \
                      org.freedesktop.sssd.infopipe.GetUserAttr \
                      string:$user array:string:phone

       * Test that calling a PAM application
         (for example ``pam_test_client auth $user``) succeeds with
         the correct password. Please note that testing
         ``auth_provider=krb5`` is also important here to make sure the
         krb5 provider can deal with ccaches that cannot be owned by a
         POSIX owner. Also note that it is important that the PAM application
         doesn't try to canonicalize the user with NSS calls like
         ``getpwnam()`` itself.

    #. No users or groups from the application domain can be resolved
       through the system interfaces

      * With the setup above, make sure that ``getent passwd $user``
        doesn't return the user and even doesn't contact the remote server.

      * Same test should be performed for the ``ssh``, ``sudo`` and other
        responders.

    #. A mixed setup with two domains, one ``posix`` and one ``application``
       reports the proper results from all interfaces

       * Modify the test domain to look like::

            [sssd]
            domains = appdomain.test, posixdomain.test
            services = ifp, pam, nss

            [pam]
            pam_app_services = sss_test

            [ifp]
            user_attributes = +phone

            [domain/appdomain.test]
            inherit_from = posixdomain.test

            [domain/posixdomain.test]
            id_provider = ldap
            ldap_uri = ldap://server.test

        * Make sure the LDAP server contains a mix of POSIX and non-POSIX
          users and groups. The POSIX users should be members of a mix of
          both POSIX and non-POSIX groups.

        * The tests from the first test case against a non-POSIX user
          should function as before

        * However, retrieving the POSIX users should now hit the domain
          ``posixdomain.test``, so the following should work:

          * ``getent passwd $posix_user`` should return the POSIX user
          * ``id $posix_user`` should return only POSIX groups the user
            is a member of and omit non-POSIX groups
          * ``getent group $posix_group`` should list all POSIX members
            of this group.

          In all the above tests, the NSS responder should skip the
          ``appdomain.test`` domain completely.

        * Since the ``appdomain.test`` domain comes first in the domain
          list, running ``GetUserAttr`` with an unqualified name should
          return non-POSIX users
        * Also invoking the ``GetUserGroups`` function should list their
          non-POSIX groups. Requests qualified to reach the
          ``posixdomain.test`` domain should only list POSIX groups.

    #. A mixed setup with two domains, one ``posix`` and one ``application``
       can be used for OS-level authentication and authorization

       * Use the setup from the previous test

       * Make sure that running a PAM application on the OS level (``su``
         or ``ssh`` are good tests) allows the user to log in using
         shortname as the NSS responder would skip the ``appdomain.test``
         completely when the PAM application calls ``initgroups`` and the
         PAM responder would skip the ``appdomain.test`` domain because
         the PAM service is not listed in the ``pam_app_services`` option

How To Debug
------------
Debug messages listing the domain type must be added to the ``cache_req``
code. Then, the regular method of issuing a request and watching the logs
should work. Expiring the cache and using the qualified names is recommended.

Authors
-------
    * Sumit Bose
    * Jakub Hrozek
    * Simo Sorce
