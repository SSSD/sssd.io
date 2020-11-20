Certificate mapping and matching rules for all providers
========================================================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/3500

Problem statement
-----------------
Currently Smartcard authentication with rule based mapping and matching of user
and certificate is only available for the IPA provider. For all other providers
Smartcard authentication is only possible if the full certificate is added to a
local override for the given user.

To offer more flexibility and easier configuration the support of mapping and
matching rules should be added to the other providers as well. This includes
the files provider which which mean that Smartcard authentication for local
users will become more flexible as well.

Use cases
---------
Active Directory
^^^^^^^^^^^^^^^^
In Active Directory environments, where Smartcard authentication for SSH is not
needed, Smartcard authentication should be enabled for all AD users with a
simple configuration and the mapping similar to the one users by Active
Directory itself.

Local users
^^^^^^^^^^^
SSSD should be used as a replacement for ``pam_pkcs11`` to authenticate users
defined in ``/etc/passwd`` with the help of a Smartcards. The configuration options
should be similarly flexible as the ones of ``pam_pkcs11``.


Overview of the solution
------------------------
In general mapping and matching certificates and users is already discussed in
`Matching and Mapping Certificates`_.
This page already contains some discussion about how the rules can be added to
the SSSD configuration file ``sssd.conf`` in section `Storing matching and mapping
configuration`_.

.. _Matching and Mapping Certificates: https://docs.pagure.org/SSSD.sssd/design_pages/matching_and_mapping_certificates.html
.. _Storing matching and mapping configuration: https://docs.pagure.org/SSSD.sssd/design_pages/matching_and_mapping_certificates.html#storing-matching-and-mapping-configuration

To make it easy to drop rules even as config snippet in ``/etc/sssd/conf.d/`` the
rules contain the domain name of the related SSSD domain in the section name.
Additionally the list of applicable domain in the rule can be used to make sure
the right rules are uses in a multi domain configuration (AD provider).

Since for local user only a user name and not an LDAP search filter is needed
to find them, rules for local user and remote user should be handled
differently. Rules for remote users can be added as ``[certmap/domain/rule_name]``
sections while rules for local user can be added as ``[certmap/domain/user_name].``

Implementation details
----------------------
Certificate mapping and matching rules for remote user can be added as::

        [certmap/domain/rule_name]
        matchrule = <ISSUER>^CN=My-CA,DC=MY,DC=DOMAIN$
        maprule = (userCertificate;binary={cert!bin})
        domains = my.domain, your.domain
        priority = 10

For a local user the rule would look like::

        [certmap/files/username]
        matchrule = <SUBJECT>^CN=User.Name,DC=MY,DC=DOMAIN$

where it is assumed that the SSSD domain with the files provider for local
users is called 'files'.  The 'domains' option is ignored for local users. It
is possible to add a rule which can map multiple users with a suitable map
rule::

        [certmap/files/email]
        matchrule = &&<ISSUER>^CN=My-CA,DC=MY,DC=DOMAIN$<SAN:rfc822Name>.*@email\.domain
        maprule = ({subject_rfc822_name.short_name})

which would use the name part of an email addresses from the 'email.domain'
domain stored in the Subject Alternative Names section of the certificate as
user name.

Internally the AD, LDAP and files provider will read the rule data from confdb
and store the rules in the cache of the corresponding domain as it is currently
already done by the IPA provider. The other SSSD components can then use the
data from the cache as that already do it for the IPA provider.

Configuration changes
---------------------
There is a new configuration section type ``[certmap/domain/name]`` which is
processed by the backend of the SSSD domain 'domain'.  The IPA provider will
continue to use the certificate mapping and matching rules defined on the IPA
server.

The options for the new section correspond to the options available for the
``ipa certmaprule-add``, namely ``matchrule``, ``maprule``, ``priority``
and ``domains.``

How To Test
-----------
Make sure all general requirements for Smartcards authentication with SSSD are met:
 * the ``pscs-lite`` package is installed and the service and socket are enabled
   and running.
 * a suitable PKCS#11 module is installed, typically this mead that the
   ``opensc`` package is installed

 * ``pam_cert_auth = True`` is set in the ``[pam]`` section of ``sssd.conf``

 * suitable CA certificates to verify the certificate on the Smartcard are added
   to ``/etc/pki/nssdb`` or ``/etc/sssd/pki/sssd_auth_ca_db.pem`` depending of a
   NSS or openSSL build of SSSD is used.

Active Directory
^^^^^^^^^^^^^^^^
Assuming that the client system is already joined to AD as SSSD is configured
to lookup and authenticate AD user you only need to add suitable mapping and
matching rules with::

        [certmap/ad.domain.name/rule_name]
        matchrule = ....
        maprule = ....

where ``ad.domain.name`` must match the domain name given in the
``[domain/...]`` section defining the AD domain.

Local users
^^^^^^^^^^^
If a ``sssd.conf`` file exist and a domain for local users with the ``files``
provider is already configured only suitable mapping and matching rules must be
added with the name of the domain for the local users.

If SSSD is running without a ``sssd.conf`` file to just handle lookups of local
users a minimal ``sssd.conf`` must be created to enable Smartcard
authentication for local users::

        [sssd]
        services = nss, pam
         
        [pam]
        pam_cert_auth = True
         
        [certmap/implicit_files/local_user]
        matchrule = _matching_rule_for_local_user_ 

The ``services`` option is needed to enable SSSD's pam responder. Since the
domain for local users is called ``implicit_files`` by default any certificate
mapping and matching rule for local users should use this name as well as long
as there is no other domain explicitly configured for local users with a
different name (see above).

Migrating from pam_pkcs11.conf
------------------------------
pam_pkcs11 offers different mappers as well. In the following some examples
will illustrate how to rewrite an existing pam_pkcs11 configuration for SSSD.
You can find all option available for SSSD's mapping and matching rules in the
`sss-certmap man page`_.

.. _sss-certmap man page: https://jhrozek.fedorapeople.org/sssd/1.16.0/man/sss-certmap.5.html

LDAP mapper
^^^^^^^^^^^
::

  mapper ldap {
        debug = false;
        module = /usr/$LIB/pam_pkcs11/ldap_mapper.so;
        # where base directory resides
        basedir = /etc/pam_pkcs11/mapdir;
        # hostname of ldap server
        ldaphost = "localhost";
        # Port on ldap server to connect
        ldapport = 389;
        # Scope of search: 0 = x, 1 = y, 2 = z
        scope = 2;
        # DN to bind with. Must have read-access for user entries under "base"
        binddn = "cn=pam,o=example,c=com";
        # Password for above DN
        passwd = "test";
        # Searchbase for user entries
        base = "ou=People,o=example,c=com";
        # Attribute of user entry which contains the certificate
        attribute = "userCertificate";
        # Searchfilter for user entry. Must only let pass user entry for the login user.
        filter = "(&(objectClass=posixAccount)(uid=%s))"
  }

Most of the option needed by the pam_pkcs11 LDAP mapper are already set in the
related ``[domain/...]`` section in ``sssd.conf``. As can be see with the configuration
above pam_pkcs11 would search the certificate in the LDAP server by using the
full certificate and trying to find it in the ``userCertificate`` attribute. The
matching certmap rule would look like::

        [certmap/ldap.domain/ldap]
        maprule = (userCertificate;binary={cert!bin})

cn/pwent mapper
^^^^^^^^^^^^^^^
::

  mapper cn {
        debug = false;
        module = internal;
        # module = /usr/$LIB/pam_pkcs11/cn_mapper.so;
        mapfile = file:///etc/pam_pkcs11/cn_map;
  }

Here the ``cn`` is read from the subject of the certificate and lookup in the
``cn_map`` file where the matching local user name can be found as well.  For each
local user name in the ``cn_map`` file create a rule like::

        [certmap/files/local_user_name]
        matchrule = <SUBJECT>^CN=cn_from_cn_map,.*

mail mapper
^^^^^^^^^^^
::

  mapper mail {
        debug = false;
        module = internal;
        # module = /usr/$LIB/pam_pkcs11/mail_mapper.so;
        # Declare mapfile or
        # leave empty "" or "none" to use no map
        mapfile = file:///etc/pam_pkcs11/mail_mapping;
  }

Similar as for the ``cn/pwent`` mapper for each entry in mail_mapping create a rule like::

        [certmap/files/local_user_name]
        matchrule = <SAN:rfc822Name>^email@from.mail.mapping$

If the name part of the email address exactly matches the user name you can use
a single rule like::

        [certmap/files/email]
        matchrule = <SAN:rfc822Name>.*@expected.email.domain
        maprule = ({subject_rfc822_name.short_name})

ms mapper
^^^^^^^^^
::

  mapper ms {
        debug = false;
        module = internal;
        # module = /usr/$LIB/pam_pkcs11/ms_mapper.so;
        ignorecase = false;
        ignoredomain = false;
        domain = "domain.com";
  }

Similar as for the email case a rule like::

        [certmap/files/ms]
        matchrule = <SAN:ntPrincipalName>.*@domain.com
        maprule =({subject_nt_principal.short_name})

would lead to a similar mapping.


How To Debug
------------
For Smartcard authentication 3 SSSD component are used, the PAM responder,
``p11_child`` and the configured backend. To enable debugging output in the log
files the ``debug_level`` option must be set in the ``[pam]`` and
``[domain/...`` sections of sssd.conf. Since ``p11_child`` is called by the PAM
responder it will inherit the ``debug_level`` set in the ``[pam]`` section. In
the debug logs the following step should be visible.

If certificate based authentication is enabled (``pam_cert_auth = True``) the
PAM responder will first in the ``SSS_PAM_PREAUTH`` step call ``p11_child`` if
Smartcard authentication is allowed for the given PAM service (see
``pam_p11_allowed_services`` in the ``sssd.conf`` man page for details). If
``p11_child`` can return a valid certificate the PAM responder first does a
user lookup by certificate and then a user lookup by name. If both lookups will
return the same cache entry the ``SSS_PAM_PREAUTH`` step will return the needed
details to the ``pam_sss`` PAM module and Smartcard authentication can proceed.

After the user entered the PIN for the Smartcard the PAM responder will in the
``SSS_PAM_AUTHENTICATE`` step first send the authentication request to the
backend to handle server-side authentication like e.g. PKINIT. If the backend
is offline or cannot handle Smartcard authentication it will return
``PAM_AUTHINFO_UNAVAIL`` and the PAM responder will try local Smartcard
authentication which involves the same steps done during the
``SSS_PAM_PREAUTH`` steps only that ``p11_child`` is called in ``auth`` mode
instead of ``preauth`` and that it receives the PIN as well.

Authors
-------
 * Sumit Bose ``<sbose@redhat.com>``
