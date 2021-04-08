Matching and Mapping Certificates
=================================

Related tickets:
 * `[RFE] Use one smartcard and certificate for authentication to distinct logon accounts <https://pagure.io/SSSD/sssd/issue/3050>`_

Related IPA design page:
 * `<http://www.freeipa.org/page/V4/User_Certificates#Certificate_Identity_Mapping>`_

Problem statement
-----------------

Mapping
^^^^^^^
Currently it is required that a certificate used for authentication is
either stored in the LDAP user entry or in a matching override. This might
not always be applicable and other ways are needed to relate a user with
a certificate.

Matching
^^^^^^^^
Even if SSSD will support multiple certificates on a Smartcard in
the context of `<https://pagure.io/SSSD/sssd/issue/3050>`_ it might be
necessary to restrict (or relax) the current certificate selection in
certain environments.

Use cases
---------

Mapping
^^^^^^^
In some environments it might not be possible or would cause unwanted
effort to add certificates to the LDAP entry of the users to allow Smartcard
based authentication. Reasons might be:

 * Certificates/Smartcards are issued externally
 * LDAP schema extension is not possible or not allowed

Matching
^^^^^^^^
A user might have multiple certificate on a Smartcard which are suitable
for authentication. But on some host in the environment only certificates
from a specific CA (while all other CAs are trusted as well) or with some
special extension should be valid for login.

Overview of the solution
------------------------
To match a certificate a language/syntax has to be defined which allows
to reference items from the certificate and compare the values with the
expected data. To map the certificates to a user the language/syntax should
allow to relate certificate items with LDAP attributes so that the value(s)
from the certificate item can be used in a LDAP search filter.


Implementation details
^^^^^^^^^^^^^^^^^^^^^^
Since certificates from different CAs (i.e. a different issuer) might have
different properties and might be used in different domains mapping rules
cannot be applied unconditionally but only to "matching" certificates. On
the other hand it is not sufficient to know that a certificate is
valid for authentication if it cannot be determine which users should be
authenticated. This illustrates that mapping and matching rules should be
used together.

Besides the two rules there are two additional optional items to improve
mapping and matching. Mapping rules should be accompanied by a domain
list which contains a list of DNS domain names in which the user should
be searched. This will help to speed up searches and to avoid to leak
information to unrelated (but trusted) domains. In a complex environment
with many trusted domains a certificate might be assigned to any user. And
since it might be possible that the certificate is assigned to multiple users
searching cannot be stop after one matching user was found. This means that
without a domain list every single trusted domain has to be checked. If the
domain list a missing the default should be to only search the local domain.

If certificates from many different issuers are used in an environment
it might be useful to have a matching rules which defines the minimal
requirements at a certificate. This rule will of courses not restrict
the issuer but will match all issuers. On the other hand there might be
issuers where the certificates needs special attention and more than the
minimal requirement are needed. To make sure that for this issuer there
is no fallback to the catch-all rules the rules will be processed by priority
and if a rule with a given priority will match no rules with lower priority
will be consulted. To be consistent with other priorities used in IPA a low
numerical value corresponds to a high priority while a higher numerical value
will lead to a lower priority. A missing value stands for the lowest priority.

As a result there are four items which build certificate authentication rule,
the mapping and matching rule, a domain list and the priority. All items are
optional. If there is no rule at all the current behavior is used as default.

An upcoming use-case might require and extension of the current mapping and
matching rule or a completely different syntax is needed to cover a use
case. To make it possible to add new rule styles there should be a tag
prefix to indicate what style is expected to follow. For the tag I would
suggest a strings of upper-case ASCII characters ``(A(0x41)-Z(0x5a)`` and
numbers ``(0(0x30)-9(0x39)`` with a trailing colon ``(:(0x3a))``.
E.g. ``KRB5:', 'RFC4523:', 'LDAP:``.

SSSD will provide a library which will consume the rules to generate LDAP
search filters for its own usages to server matching users on remote LDAP
servers or in the local cache. Additionally it will provide an interface to
check if a given user object will match according to the rules which can
be use by the PKINIT matching plugin.

Matching
^^^^^^^^
The pkinit plugin of MIT Kerberos must find a suitable certificate
from a Smartcard as well and has defined the following syntax
(see the pkinit_cert_match section of the ``krb5.conf`` man page or
`<http://web.mit.edu/Kerberos/krb5-1.14/doc/admin/conf_files/krb5_conf.html>`_
for details). The main components are:

 * ``<SUBJECT>regular-expression``
 * ``<ISSUER>regular-expression``
 * ``<SAN>regular-expression``
 * ``<EKU>extended-key-usage-list``
 * ``<KU>key-usage-list``

And can be grouped together with a prefixed ``&&`` (and) or ``||`` (or)
operator (``&&`` is the default). If multiple rules are given they are
iterated with the order in the configuration file as long as a rule matches
exactly one certificate.

While ``<SUBJECT>`` and ``<ISSUER>`` are (IMO) already quite flexible I can
see some potential extensions for the other components.

``<EKU>`` and ``<KU>`` in MIT Kerberos only accept certain string values
related to some allowed values in those field as defined in
`<https://www.ietf.org/rfc/rfc3280.txt>`_. The selection is basically
determined by what is supported on server side of the pkinit plugin of MIT
Kerberos. Since we plan to extend pkinit and support local authentication
without pkinit as well I would suggest to allow ``OID`` strings or an integer
value in the ``<KU>`` case as well (the comparison is done on the ``OID``
level nonetheless).

The ``<SAN>`` component in MIT Kerberos only checks the
``otherName`` SAN component for the ``id-pkinit-san OID``
as defined in `<https://www.ietf.org/rfc/rfc4556.txt>`_
or the ``szOID_NT_PRINCIPAL_NAME`` ``OID`` as mentioned in
`<https://support.microsoft.com/en-us/kb/287547>`_. While this is sufficient
for the default pkinit user case of MIT Kerberos I would suggest to extend
this component by allowing to specific the other SAN component, e.g.
``<SAN:rfc822Name>``.

The prefix tag for this type of matching rules would be ``KRB5:`` and I
would suggest to take this a default, i.e. if the prefix tag is missing
``KRB5:`` will be assumed.

Mapping
^^^^^^^
Since different certificates, e.g. issued by different CAs, might have
different mapping rule, a matching rule must be added if there are more
than 1 mapping rule. A single mapping rule without a matching rule might
be used as default/catch-all rule in this case.

With trusted AD forests the mapped users might come from trusted domains as
well. To avoid searching in every single domain a list of expected domains
can be added to each mapping rule. If the list is empty the local domain
is assumed by default.

Similar to Active Directory we will require a dedicated LDAP attribute in
the user entry (anchor) to map the certificate to the user entry. Mapping
rules which allow to search users based on some data from the certificate
and common LDAP attributes make it easy to roll out certificate based
authentication in existing environments. E.g. if one of the SAN attributes
in the certificate contains the email address of the user a single mapping
rule is needed to map every user with a certificate. No changes to existing
LDAP user objects are needed.

On the other hand certificates issues by external CA might not contain
data to reliable match all users based on common LDAP attributes. Or it
should be possible to authenticate with a single certificate as multiple
different users. In those cases a dedicated attributes is needed in the
user entry which contains some information about the certificate like the
``altSecurityIdentities`` attribute used by Active Directory.

A specific per-user attribute also relates to other authentication methods
available for a users. Password hashes and Kerberos keys are stored in the
user entry as well. OTP tokens are managed in separate objects but contain
the DN of the user as a unique reference. In all cases the removal of a
single attribute will disable/remove a specific authentication method for
a specific user.

Finally, since mapping is about searching a user entry in the LDAP tree
the dedicated attribute can be indexed to speed up the searches and help
to avoid a high server load.

Compatibility with Active Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
With trusted AD forests we have to support the mapping
anchors used by AD which is typically an issue-subject pair like e.g.
``X509:<I>C=US,O=InternetCA,CN=APublicCertificateAuthority<S>C=US,O=Fabrikam,OU=Sales,CN=Jeff Smith``.
Active Directory uses a per-user LDAP attribute
`altSecurityIdentities <https://msdn.microsoft.com/en-us/library/cc220106.aspx>`_
to allow arbitrary user-certificate mappings if there is no suitable
user-principal-name entry in the SAN of the certificate or if a single
certificate should be used to authenticate as different users.

Unfortunately there is no single document where all values
and use-case of this attribute are listed. The best overview I found is in
`<https://blogs.msdn.microsoft.com/spatdsg/2010/06/18/howto-map-a-user-to-a-certificate-via-all-the-methods-available-in-the-altsecurityidentities-attribute/>`_
In `<https://msdn.microsoft.com/en-us/library/ms677943%28v=vs.85%29.aspx>`_ it
is explained how ``altSecurityIdentities`` is used for user object and only
mentions the issue-subject pair as an example, but does not mention other
cases. `<https://msdn.microsoft.com/en-us/library/hh536384.aspx>`_ explains what
is required for ``PKINIT`` which includes the issuer-subject pair but allows
5 other variants as well. (Interestingly, the user related page says that
using only the issuer ``<I>`` is allowed but not using only the subject
``<S>`` while the PKINIT page says that using only the subject ``<S>`` is
allowed and does not list a usage with only the issue ``<I>``. I guess it is
a typo in the user page, because ``<S>`` contains user specific information
while ``<I>`` is the same for all certificates from the given issuer).

So it looks like the most important variant is the issuer-subject pair. This
one is e.g. created when a certificate is added via the 'Name Mappings'
context menu entry in AD's 'Users and Computers' utility ('Advanced Features'
must be activated in the 'View' menu). The attribute value might look like::

    altSecurityIdentities: X509:<I>O=Red Hat,OU=prod,CN=Certificate Authority<S>DC
    =com,DC=redhat,OU=users,OID.0.9.2342.19200300.100.1.1=sbose,E=sbose@redhat.co
    m,CN=Sumit Bose Sumit Bose

First it can be seen that X.500 ordering is used. Second, if RDN
types not explicitly mentioned in the RFCs are used, you are
on your own. As can be seen AD can translate the deprecated
OID `1.2.840.113549.1.9.1
<http://www.oid-info.com/get/1.2.840.113549.1.9.1>`_ and uses ``E`` as
NSS. But the OID `0.9.2342.19200300.100.1.1 <http://www.oid-info.com/get/0.9.2342.19200300.100.1.1>`_
which is explicitly mentioned in RFC4514 is
not translated as UID but the plain OID syntax is used (my guess it that
Microsoft tries to be compatible with "older" versions because the UID
was added in RFC2253 from 1997 but was not present in the RFC1779 from
1995 and RFC1485 from 1993).

Besides ``altSecurityIdentities`` AD uses the SAN with the
``szOID_NT_PRINCIPAL_NAME`` OID to map users. It has to be noted that AD
does not only look at the ``userPrincipalName`` LDAP attribute to map the
principal from the certificate but uses the default principal of an AD user
``samAccountName@AD.REALM`` as well. Interestingly a ``Kerberos:user@AD.REALM``
entry in ``altSecurityIdentities`` did not work in my tests and AD denied
login. So what AD does currently matches how SSSD tried to resolve a
fully-qualified name against AD.
`MS-PKCS Appendix A <https://msdn.microsoft.com/en-us/library/cc238488.aspx>`_
explicitly says that id-pkinit-san is ignored it does not have to be
included for this mapping rule.

Using the Certificate as an anchor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For IPA and other generic LDAP servers an LDAP attribute like
e.g. ``userCertificate`` is a good anchor as well and is currently already
used to allow local authentication with a Smartcard. Since it is the
current default I would suggest that an empty mapping rule with use the
LDAP attribute configured by the SSSD option ``ldap_user_certificate``
as anchor and search with the whole certificate.

It has to be noted that having the binary certificate in the userCertificate
LDAP attribute is not sufficient for pkinit on AD. Either checks in the
matching rule, e.g. checking if a SAN with ``szOID_NT_PRINCIPAL_NAME`` OID is
available, or mapping rules from above should be used if pkinit is required
with AD.

Some notes about DNs
^^^^^^^^^^^^^^^^^^^^
The X.500 family of standards define names as "SEQUENCE OF
RelativeDistinguishedName" where the sequence is "starting with the root and
ending with the object being named" (see X.501 section 9.2 for details). On
the other hand RFC4514 section 2.1 says "Otherwise, the output consists of
the string encoding of each ``RelativeDistinguishedName`` in the ``RDNSequence``
(according to Section 2.2), starting with the last element of the sequence
and moving backwards toward the first." This means that the ASN.1 encoded
issuer and subject DN from the X.509 certificate can be either displayed
as string in the

  * X.500 order: ``DC=com,DC=example,CN=users,CN=Certuser``

or in the

 * LDAP order: ``CN=Certuser,CN=Users,DC=example,DC=com``

As a consequence different tools will use a different order when printing
the issuer and subject DN. While NSS's certutil will use the LDAP order,
'openssl x509' and gnutls's certtool will use the X.500 order (the latter
might change due to `<https://gitlab.com/gnutls/gnutls/issues/111>`_).

This makes it important to specific the order which is used by SSSD
for mapping and matching. I would prefer the LDAP order here. E.g. by
default the AD CA uses the DN of the users entry in AD as subject in
the issues certificate. So a matching rule like ``<SUBJECT:dn>`` could
tell SSSD to directly search the user based on its DN (which BTW is the
original intention of the subject field in the certificate, only that the
DN should be looked up in a more general DAP as defined by X.500 and not
in the lightweight version called LDAP)

Another issue is the limited set of attribute names/types required by
the RFCs (see section 4.1.2.4 of RFC 3280 and section 3 of RFC 4514). If
e.g. the deprecated OID `1.2.840.113549.1.9.1 <http://www.oid-info.com/get/1.2.840.113549.1.9.1>`_
is used all tools are able to identify it as an
email address but OpenSSL displays it as ``emailAddress=user@example.com``,
certtool as ``EMAIL=user@example.com`` and certutil as ``E=user@example.com``. So
matching rules should try to avoid attribute names or only the ones from
`RFC 4514 <https://www.ietf.org/rfc/rfc4514.txt>`_:

 * ``CN      commonName (2.5.4.3)``
 * ``L       localityName (2.5.4.7)``
 * ``ST      stateOrProvinceName (2.5.4.8)``
 * ``O       organizationName (2.5.4.10)``
 * ``OU      organizationalUnitName (2.5.4.11)``
 * ``C       countryName (2.5.4.6)``
 * ``STREET  streetAddress (2.5.4.9)``
 * ``DC      domainComponent (0.9.2342.19200300.100.1.25)``
 * ``UID     userId (0.9.2342.19200300.100.1.1)``


Mapping with LDAP search filter syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Given the different requirements discussed above and since the goal of the
mapping rules is to create a LDAP search filter a filter template would be a
direct and flexible way to define mapping rules::

    (&(someAttr={certContent})(someOtherAttr=*{otherCertContent}*))

The syntax might be a bit verbose
but LDAP search filters are well documented and administrators
should already have a basic understanding.

For the templates in curly braces Python-style formatting strings are used.
Depending on the type of certificate data a sub-component can be specified
with a '.' or a conversion option can be given with a '!', e.g.:

 * {subject_nt_principal.short_name}, get the name part before the '@' sign
 * {issuer_dn!ad_x500}, get the issuer name string in x500 ordering and
   translate the attributes names as AD would do

A detailed list of templates can be found in the `sss-certmap man page
<https://www.mankier.com/5/sss-certmap>`_.

Examples
^^^^^^^^
The following example are for the FreeIPA use case and use the ''ipa
certmaprule-\*'' utilities which are described on the related
`IPA design page <http://www.freeipa.org/page/V4/Certificate_Identity_Mapping>`_.

All certificates from issuer CN=CA,dc=ISSUER,DC=COM with the extended key
usage 'ClientAuthentication' shall be mapped to a user by looking up with the
whole certificate, i.e. the certificate must be stored in the user entry::

    ipa certmaprule-add testrule \
                        --matchrule='<ISSUER>^CN=CA,dc=ISSUER,DC=COM$<EKU>clientAuth' \
                        --maprule='(userCertificate;binary={cert!bin})'
                        --priority=42

All certificates from issuer CN=CA,dc=ISSUER,DC=COM with the extended key
usage 'ClientAuthentication' shall be mapped to an AD user by looking up the
'altSecurityIdentities' attribute in the AD domain ad.dom.com::

    ipa certmaprule-add testrule \
                        --matchrule='<ISSUER>^CN=CA,dc=ISSUER,DC=COM$<EKU>clientAuth' \
                        --maprule='(altSecurityIdentities=X509:<I>{issuer_dn!ad_x500}<S>{subject_dn!ad_x500})' \
                        --domain=ad.dom.com \
                        --priority=42

All certificates from issuer CN=CA,dc=ISSUER,DC=COM with the extended key
usage 'ClientAuthentication' shall be mapped to an IPA user by looking up the
'ipaCertMapData' attribute in the local IPA domain::

    ipa certmaprule-add testrule \
                        --matchrule='<ISSUER>^CN=CA,dc=ISSUER,DC=COM$<EKU>clientAuth' \
                        --maprule='(ipaCertMapData=X509:<I>{issuer_dn}<S>{subject_dn})' \
                        --priority=42

All certificates from issuer CN=AD-CA,dc=ISSUER,DC=COM with the extended key
usage 'ClientAuthentication' which have an AD NT principal from the AD.DOM
realm in the SANs shall be mapped to an AD user by looking up the
by principal or name in the domain ad.dom::

    ipa certmaprule-add testrule \
                        --matchrule='<ISSUER>^CN=AD-CA,dc=ISSUER,DC=COM$<EKU>clientAuth<SAN:ntPrincipalName>*@AD.DOM' \
                        --maprule='(|(userPrincipalName={subject_nt_principal})(samAccountName={subject_nt_principal.short_name}))' \
                        --domain=ad.dom \
                        --priority=42

Configuration changes
---------------------
No changes are needed on the client. New rules are picked up after some time or
after a restart of SSSD.

How To Test
-----------
The easiest way to test the mapping rules is the new ``ListByCertificate``
DBus method offered by SSSD's Infopipe::

    dbus-send --system --print-reply --dest=org.freedesktop.sssd.infopipe \
              /org/freedesktop/sssd/infopipe/Users \
              org.freedesktop.sssd.infopipe.Users.ListByCertificate \
              string:"$(cat cert.pem)" uint32:10
    method return time=1491995602.233163 sender=:1.616 -> destination=:1.757 serial=5 reply_serial=2
       array [
          object path "/org/freedesktop/sssd/infopipe/Users/ad_2edevel/1367242755"
          object path "/org/freedesktop/sssd/infopipe/Users/ad_2edevel/1367242776"
   ]


How To Debug
------------
Debug messages of the certificate mapping library are available in the SSSD
domain log file and in the krb5kdc.log if the library is used with IPA's
Kerberos certauth plugin.

Authors
-------
 * Sumit Bose <sbose@redhat.com>


Additional information for reference
------------------------------------

Matching - alternative RFC4523 syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*(The follow section was used to discuss an alternative to the KRB5 matching
rules. It was agreed that KRB5 rules will be used for a start.)*
Based on the X.509 ``CertificateAssertion`` syntax `RFC 4523 <https://www.ietf.org/rfc/rfc4523.txt>`_
introduces Generic String Encoding
Rules (``GSER``)-based (`RFC3641 <https://www.ietf.org/rfc/rfc3641.txt>`_)
and `RFC 3642 <https://www.ietf.org/rfc/rfc3642.txt>`_ syntax to write
``CertificateAssertions`` which can be used to match certificates as well.

A matching rule for an issuer would look like::

    { issuer "cn=CA,dc=example,dc=com" }

There is an identifier for ``keyUsage`` as well::

    { issuer "cn=CA,dc=example,dc=com" , keyUsage { digitalSignature , keyEncipherment }

But it looks like there is none specific for the ``extendedKeyUsage`` which
is important to separate certificate e.g. for email signing and for login
purposes. I think even ``nameConstraints`` cannot be use here because according
to X.509 "``nameConstraints`` matches if the subject names ..." which only
include the subject and the subject alternative names (please let me know
if there is a standardized way to add assertions for extensions like the
``extendedKeyUsage``).

Besides ``extendedKeyUsage`` there are other components in the certificate
where we want to add matching rules in the future which are currently
not handled by ``RFC4523``. E.g. 'Authority Information Access' (see
`RFC5280 section 4.2.2.1 <https://tools.ietf.org/rfc/rfc5280.txt>`_]
where information about ``CRLs`` or ``OCSP`` responders are stored. With
this we would be able to only select certificates which have an ``OCSP``
responder defined or where we known that the ``CRL`` is updated regularly.

Although it would be possible to add new assertion for our usage seamlessly
I think it would not be a good idea to do this without making sure that
they will be added to any new versions of ``RFC4523``. I currently have no idea
how easy or hard this would be and how this would limit our flexibility
to react on request from users and customers.

To restrict the matching not only to a single certificate but to a group
of certificates based on the subject (owner) name constraints as defined
in `RFC3280 section 4.2.1.11 <https://tools.ietf.org/html/rfc3280.html#section-4.2.1.11>`_
can be used. The constraints are applied to the subject name and subject
alternative names attributes in the certificate and consist of a list of
allowed names (``permittedSubtrees``) and rejected names (``excludedSubtrees``). For
directory names (the subject name and the related SAN attribute) an area in
the directory tree can be specified where the names should match. E.g. to
match all subject names from the 'research' department but not from
sub-departments of 'research'::

    { permittedSubtrees { ( base "CN=research,DC=example,DC=com" , minimum 1, maximum 1 ) } }

can be used. To allow everything but the 'no_access' subtree::

    { excludedSubtrees { ( base "CN=no_access,DC=example,DC=com" ) } }

an be used, 'minimum' and 'maximum' are not needed here because the default
for 'minimum' is '0' and a missing 'maximum' specifies the whole subtree.

Compared the regular-expressions this syntax makes it easy to reject
specific types of names. But it also requires that a full base is specified
and only a simple ``key_string``. This is of course more safe but it has
to be noted that the matching rules are only applied on valid and verified
certificates. Since CA certificates can contain name constraints as well and
`with p11-kit it is even possible to staple those extensions <http://nmav.gnutls.org/2016/06/restricting-scope-of-ca-certificates.html>`_
it would be possible to reject certificates system-wide already during
the verification.

Based on this I would suggest to reserve the prefix tag ``RFC4523:``
for this type of matching rule but postpone the implementation.

Issuer specific matching
^^^^^^^^^^^^^^^^^^^^^^^^
*(The following section was used to discuss an alternative to priorities but
it was decided that priorities are more flexible)*
Although the MIT Kerberos rules allow to select the issuer of a certificate
there are use cases where a more specific selection is needed. E.g. if
there are some default matching rules for all issuers and some other issuer
specific rules where the default rules should not apply. To make this
possible with the above scheme the default rules must have an ``<ISSUER>``
clause which matches all but the issuer with the specific rules. Writing
regular-expressions to not match a specific string or a list of strings
is at least error-prone if not impossible.

To make it easier to define issuer specific rules and default rules at the
same time and optional issuer string can be added to the rule to indicate
that for the given issuer only those rules should be considered. Given the
use-case I think it is acceptable to require that the full issuer must be
specified here in LDAP order (see below) and case-sensitive matching is used.

How the issuer string is linked to the matching rules depends on the storage
(LDAP or ``sssd.conf``, see below for details).

Future consideration
^^^^^^^^^^^^^^^^^^^^
*(The following section was used to discuss an alternative syntax for mapping
rules. It was decided that LDAP search filter syntax is more flexible and
better suited for a start)*
A mapping rule can use a similar syntax like the matching rule where the
LDAP attribute can be added with a ``:``, e.g:

 * ``<ISSUER:O.I.D.:ldapAttributeName:*>``
 * ``<SUBJECT:O.I.D.:ldapAttributeName:*>``
 * ``<SAN:O.I.D.:ldapAttributeName:*>``

where O.I.D. is either the OID or name of a RDN type or the OID or some
well-known-name of the SAN component respectively. Since the SUBJECT
might contain multiple RDNs of the same type always the "most specific"
is selected because in general this will be the most suited one to map the
certificate to a specific user. "most specific" means the last in X.500
order and the first in LDAP order (see discussion below for details).

If the O.I.D. is missing the full SUBJECT/ISSUER is used for mapping. If
'DN' is used as ``ldapAttributeName`` SUBJECT is expected to be the DN of
the user. If the O.I.D. is missing in the SAN case the same default as
with matching (id-pkinit-san and ``szOID_NT_PRINCIPAL_NAME`` OID) is used. If
both SAN values can be found in the certificate and are different the LDAP
search filter will combine both with the or-operator.

The optional ``*`` in the end indicates that a sub-string search
(``ldapAttributeName=*value*``) should be used and not an exact match
(``ldapAttributeName=value``). Please note that it depends on the server-side
definition of the LDAP attribute if case-sensitive or case-insensitive
matching is used.

Currently I see no usage for ``<KU>`` and ``<EKU>`` in mapping rules
because they do not contain any user-specific data. If at some point we
will have personal CAs we might consider to add ``<ISSUER>`` based mappings.

Most of the interesting values from the SAN should be directly map-able
to LDAP attributes. And processing the string representation of ``<SUBJECT>``
might be tricky as discussed below. Nevertheless it might be possible to
add to following in a future release if more complex operations on the
values are needed:

 * ``<SUBJECT:ldapAttributeName>/regexp/replacement/``
 * ``<SAN:O.I.D.:ldapAttributeName>/regexp/replacement/``

where "/regexp/replacement/" stands for optional sed-like substitution
rules. E.g. a rule like::

    <SUBJECT:samAccountName>/^CN=\([^,]*\).*$/\1/

would take the subject string ``CN=Certuser,CN=Users,DC=example,DC=com``
from the certificate and generate a LDAP search filter component
``(samAccountName=Certuser)`` which can be included in a LDAP search filter
which includes additional components like e.g. an ``objectClass``.

The search-and-replace does not has to be sed-like
because AFAIK there is not library which offers
this and I would like to avoid implementing it. GLib e.g. has
`g_regex_replace <https://developer.gnome.org/glib/stable/glib-Perl-compatible-regular-expressions.html#g-regex-replace>`_
Since we already have a GLib dependency in SSSD due to
some UTF-8 helper functions using might be acceptable as well. Nevertheless it
would be nice to hear if there are alternative libraries available as well.

Maybe even search-and-replace are not sufficient for all cases and something
like embedded lua scripts are needed. But since certificate mapping is
about access control and authorization it should be always considered if
adding a new attribute to the users LDAP entry which makes mapping easy
and straight-forward wouldn't be the better solution.

Storing matching and mapping configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*(Implementation is WIP )*
On the IPA server a new objectClass can be created to store an
matching-mapping-domain rule triple together with a specific issuer. All
attributes are optional because a missing mapping rule would mean that the
user entry will be search with the whole certificate. A missing matching
rule will indicate catch-all rule with a default mapping. If the domain is
missing only the local domain will be searched. If only a specific issuer
is given certificates from this issuer must be stored in the LDAP entry
of the user for the local domain to make authentication possible.

Specifying matching-mapping-domain rules in ``sssd.conf`` is a bit more
complicated because SSSD does not respect multiple entries with the same
keyword, only the last one is used. So all rules have to be added to a
single line. To make this less error-prone and more readable the rules
with all needed components can a added in individual INI-sections and in
the domain section on the name is referenced::

    [domain/some.domain]
    ...
    certificate_rules = cert_rule1, cert_rule2
    ...
    [certfificate_rule/cert_rule1]
    certificate_issuer = ....
    certificate_match = ....
    certificate_map = ....
    certificate_domains = ....

    [certfificate_rule/cert_rule2]
    certificate_issuer = ....
    certificate_match = ....
    certificate_map = ....
    certificate_domains = ...

As an alternative the rules components can be enclosed by curly-braces
``{}{}{}{}`` and each rule is separated by a comma ``,``. A single rule in
curly braces indicates a matching rule and the mapping will be done with
the whole certificate. A default/catch-all mapping rule will start with
an empty pair of curly braces followed by a pair containing the mapping
rule. Issuer specific rules will have three pairs of curly braces where
the first pair must contain an issuer string.

Examples
^^^^^^^^
* Only matching rule::

    [certificate_rule/msLogon] 
    certificate_match = <EKU>msScLogin

  only allow certificates with have the Microsoft OID for Smartcard logon
  ``1.3.6.1.4.1.311.20.2.2`` set, use the whole certificate to look-up the
  user in the local domain. The same result can be achieved with

* Matching rule with OID::

    [certificate_rule/msLogonOID]
    certificate_match = <EKU>1.3.6.1.4.1.311.20.2.2

  see above

* example::

    [certificate_rule/issuer_subject]
    matching_rule = <ISSUER>*my-company*<SAN:rfc822Name>*@my-company.com$
    mapping_rule = <ALT-SEC-ID-I-S:altSecurityIdentities>
    certificate_domains = my-company.com

  only allow certificates from the 'my-company' issuer which
  have an email address from the 'my-company.com' domain in the
  rfc882Name SAN attribute. Use AD style issuer-subject search filter
  ``(altSecurityIdentities=<I>cn=issuer,dc=my-company,dc=com<S>cn=user,dc=my-company,dc=com)``
  to find the matching user in the domain 'my-company.com'

