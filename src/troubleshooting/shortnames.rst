SSSD and shortnames
###################

Lets start with the definition of ``fully qualified name``:

.. note::

    Fully qualified user name is the situation when user name is followed with domain name,
    for example ```bob@corp.abc.com`` instead of just ``bob``. On Windows systems it can be called
    ``SAM`` account (``Security Account Manager``) and writted different way: ``domain_name\user_name``.
    UPN (User Principal Name) is another alias for this naming convention.
    In case of Active Directory (AD) this type of entry may be called ``DN``
    (``Distinguished Name``), where separated blocks will have value:
    CN=bob,OU=Users,DC=corp,DC=abc,DC=net


Single domain scenario
**********************

Imaginate the simplest scenario - SSSD is configured with single domain in ``sssd.conf``
called ``ldap.vm`` representing LDAP backend as data provider.

.. code-block:: ini

    [sssd]
    config_file_version = 2
    services = nss, pam, sudo
    debug_level = 0x3ff0
    domains = ldap.vm
    user = root

    [nss]
    debug_level = 0x3ff0

    [pam]
    debug_level = 0x3ff0

    [sudo]
    debug_level = 0x3ff0

    [domain/ldap.vm]
    debug_level = 0x3ff0
    id_provider = ldap
    ldap_uri = _srv_
    ldap_tls_reqcert = demand
    ldap_tls_cacert = /shared/enrollment/ldap/cacert.asc
    dns_discovery_domain = ldap.vm

In this case every user / group query will land on this single domain.
Example of query is ``getent passwd bob``. SSSD will be ask about user ``bob``
and it will start searching for it across all configured domains.
As we have only one domain found user will be ``bob@ldap.vm``

Multiple domains scenario
*************************

Lets discuss more complicated scenario where SSSD serves two domains in sssd.conf.

.. code-block:: ini

    [sssd]
    config_file_version = 2
    services = nss, pam, sudo
    debug_level = 0x3ff0
    domains = users.vm, admins.vm
    user = root

    [nss]
    debug_level = 0x3ff0

    [pam]
    debug_level = 0x3ff0

    [sudo]
    debug_level = 0x3ff0

    [domain/users.vm]
    debug_level = 0x3ff0
    id_provider = ldap
    ldap_uri = _srv_
    ldap_tls_reqcert = demand
    ldap_tls_cacert = /shared/enrollment/ldap/cacert.asc
    dns_discovery_domain = users.vm

    [domain/admins.vm]
    debug_level = 0x3ff0
    id_provider = ldap
    ldap_uri = _srv_
    ldap_tls_reqcert = demand
    ldap_tls_cacert = /shared/enrollment/ldap/cacert.asc
    dns_discovery_domain = admins.vm

Example of query is again ``getent passwd bob``. This time SSSD will check first domain
from config file (users.vm), then if user is not found it will check next domain
in config file (admins.vm). This will be continued till result is found or all domains
from config file enumerated.

But what if we want to ask specified domain for the user? It is simple, just
fully qualified name needs to be used: ``getent passwd bob@users.vm``.

Now imaginate situation where in company there are hundred of users and only few
administrators. Asking all the users to type fully qualified name everytime they
are logging into systems can be annoying and lead to errors. For this usecase
``shortnames`` has been introduced in SSSD [1]. It is possible to set default "domain"
everytime only username will used rather than fully qualified name. Option
responsible for this is ``default_domain_suffix``.
When default_domain_suffix is set it content will be appended to all user / group
names before SSSD will start processing them.
In our exampple setting ``default_domain_suffix = users.vm`` will result with
Bob being able to log in to the system with just ``bob`` rather than fully
qualified ``bob@users.vm``.
But what with the administrators? Now they will have to use full qualified name
like ``admin_smith@admins.vm``. Otherwise they username will not be resolved
as simple ``admin_smith`` will be converted to ``admin_smith@users.vm`` due to
default_domain_suffix set.

Shortnames and /etc/passwd based users
**************************************

Imaginate the situation where we have two source of users in the system: good old
/etc/passwd file and SSSD wrapping ldap.vm domain from examples above. We would like
to /etc/passwd be evaluated first and then domain data provider.
SSSD has ``files provider`` feature allowing it tread /etc/passwd and /etc/groups
content as yet another domain listed in sssd.conf. What we also want is to users
be able to login using simple username.

.. code-block:: ini

    [sssd]
    config_file_version = 2
    services = nss, pam, sudo
    debug_level = 0x3ff0
    domains = files, ldap.vm
    user = root
    default_domain_suffix = ldap.vm

    [nss]
    debug_level = 0x3ff0

    [pam]
    debug_level = 0x3ff0

    [sudo]
    debug_level = 0x3ff0

    [domain/files]
    debug_level = 0x3ff0
    id_provider = files

    [domain/ldap.vm]
    debug_level = 0x3ff0
    id_provider = ldap
    ldap_uri = _srv_
    ldap_tls_reqcert = demand
    ldap_tls_cacert = /shared/enrollment/ldap/cacert.asc
    dns_discovery_domain = ldap.vm

Now the problem starts as default_domain_suffix is set in sssd.conf.
As a result every user query without fully qualified name will land on ``ldap.vm`` domain.
This mean that the content of /etc/passwd will not be evaluated.

To avoid this simple trick is needed. Just modify ``/etc/nssswitch.conf`` and make
sure that part related to passwd and group has ``files`` before ``sss`` set.

.. code-block:: ini

    .
    .
    #passwd:     sss files systemd
    passwd:     files files systemd
    #group:      sss files systemd
    group:      files sss systemd
    .
    .

As a result glibc will first try to evaluate /etc/passwd in search for user, and then
will jump to SSSD.

Shortnames in IPA
*****************

SSSD can access AD domain via IPA data provider. In this case of scenario
it is possbie to apply IPA specified shortnames related setting on the IPA
server itself. More details can be found on [2].



SSSD configuration options related to shortnames
************************************************

Bellow are some usefull sssd.conf options related to shortnames usage with SSSD.

.. note::

    default_domain_suffix (string)

        This string will be used as a default domain name for all names without a domain name component. The main use case is environments where the primary domain is intended for managing host policies and all users are located in a trusted domain. The option allows those users to log in just with their user name without giving a domain name as well.

        Please note that if this option is set all users from the primary domain have to use their fully qualified name, e.g. user@domain.name, to log in. Setting this option changes default of use_fully_qualified_names to True. It is not allowed to use this option together with use_fully_qualified_names set to False.

        Default: not set

.. note::

    use_fully_qualified_names (bool)

        Use the full name and domain (as formatted by the domain's full_name_format) as the user's login name reported to NSS.

        If set to TRUE, all requests to this domain must use fully qualified names. For example, if used in LOCAL domain that contains a "test" user, getent passwd test wouldn't find the user while getent passwd test@LOCAL would.

        NOTE: This option has no effect on netgroup lookups due to their tendency to include nested netgroups without qualified names. For netgroups, all domains will be searched when an unqualified name is requested.

        Default: FALSE (TRUE if default_domain_suffix is used)

.. note::

    domain_resolution_order

        Comma separated list of domains and subdomains representing the lookup order that will be followed. The list doesn't have to include all possible domains as the missing domains will be looked up based on the order they're presented in the “domains” configuration option. The subdomains which are not listed as part of “lookup_order” will be looked up in a random order for each parent domain.

        Please, note that when this option is set the output format of all commands is always fully-qualified even when using short names for input. In case the administrator wants the output not fully-qualified, the full_name_format option can be used as shown below: “full_name_format=%1$s” However, keep in mind that during login, login applications often canonicalize the username by calling getpwnam(3) which, if a shortname is returned for a qualified input (while trying to reach a user which exists in multiple domains) might re-route the login attempt into the domain which users shortnames, making this workaround totally not recommended in cases where usernames may overlap between domains.

        Default: Not set

.. note::
       full_name_format (string)
           A printf(3)-compatible format that describes how to compose a fully
           qualified name from user name and domain name components.

           The following expansions are supported:

           %1$s
               user name

           %2$s
               domain name as specified in the SSSD config file.

           %3$s
               domain flat name. Mostly usable for Active Directory domains,
               both directly configured or discovered via IPA trusts.

           Each domain can have an individual format string configured. See
           DOMAIN SECTIONS for more info on this option.

.. note::

    override_homedir (string)

        Override the user's home directory. You can either provide an absolute value or a template. In the template, the following sequences are substituted:

        %u
            login name

        %U
            UID number

        %d
            domain name

        %f
            fully qualified user name (user@domain)

        %l
            The first letter of the login name.

        %P
            UPN - User Principal Name (name@REALM)

        %o
            The original home directory retrieved from the identity provider.

        %H
            The value of configure option homedir_substring.

        %%
            a literal '%'

        This option can also be set per-domain.

        example:

            override_homedir = /home/%u

        Default: Not set (SSSD will use the value retrieved from LDAP)

[1] https://docs.pagure.org/sssd.sssd/design_pages/shortnames.html
[2] https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/windows_integration_guide/short-names#setting-dro-globally
