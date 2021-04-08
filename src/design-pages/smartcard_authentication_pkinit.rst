Smartcard Authentication - PKINIT
=================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/3270 <https://pagure.io/SSSD/sssd/issue/3270>`__

Problem statement
~~~~~~~~~~~~~~~~~

Currently Smartcard Authentication is only used to authenticate against
the local system. PKINIT would provide a method to use Kerberos for
authentication and get a Kerberos Ticket Granting Ticket (TGT) during
the authentication so that network resources can be accessed with
Kerberos/GSSAPI.

Use cases
~~~~~~~~~

Client systems which joined to Kerberos based domains like Active
Directory (AD) or FreeIPA can use Smartcard authentication to replace
password based authentication and still get full single-sign-on (SSO)
access to the resources of the domain.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

SSSD's KRB5 provider will detect the presence of the PKINIT
pre-authentication method using the responder interface of recent MIT
Kerberos version. This is similar to the current detection of password
authentication (single-factor authentication, 1FA) and two-factor
authentication (2FA). Based on the available pre-authentication methods
and if a Smartcard with a suitable certificate is currently accessible
by SSSD the user will be prompted differently about what credentials
should be entered for authentication.

+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| Available pre-authentication types   | suitable Smartcard present   | User prompting                                                                                            |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| pkinit                               | no                           | Ask to insert Smartcard and enter PIN                                                                     |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| pkinit                               | yes                          | Ask for PIN                                                                                               |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 1FA, pkinit                          | no                           | Ask for password                                                                                          |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 1FA, pkinit                          | yes                          | Ask for PIN, fallback to password if no PIN is given                                                      |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 2FA, pkinit                          | no                           | Ask for first and second factor                                                                           |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 2FA, pkinit                          | yes                          | Ask for PIN, fallback to first and second factor if no PIN is given                                       |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 1FA, 2FA, pkinit                     | no                           | Ask for first and optional second factor                                                                  |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 1FA, 2FA, pkinit                     | yes                          | Ask for PIN, fallback to first and optional second factor if no PIN is given                              |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 1FA                                  | no                           | Ask for password                                                                                          |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 1FA                                  | yes                          | Ask for PIN (for local authentication), fallback to password if no PIN is given                           |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 2FA                                  | no                           | Ask for first and second factor                                                                           |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 2FA                                  | yes                          | Ask for PIN (for local authentication), fallback to first and second factor if no PIN is given            |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 1FA, 2FA                             | no                           | Ask for first and optional second factor                                                                  |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
| 1FA, 2FA                             | yes                          | Ask for PIN (for local authentication), fallback to first and optional second factor if no PIN is given   |
+--------------------------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+

Ideally the prompting will be configurable so that it can be adopted for
other non-IPA/non-AD use cases but the primary goal is to have sensible
defaults which work well for IPA and AD.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

The responder interface indicates the availability of PKINIT if there is
KRB5\_RESPONDER\_QUESTION\_PKINIT in the
krb5\_responder\_question\_list(). During the SSSD pre-auth run this can
be used to signal the availability to the client. During authentication
it should be used to set the answer if the Smartcard authentication
credentials including the PIN and other details are available.

Since it is possible that there are multiple certificates on the
Smartcard and even that multiple Smartcards are accessible at the same
time the MIT Kerberos PKINIT plugin must be called in a way to make sure
that only the right certificate is used. The right certificate here is
the one that was previously selected either by SSSD's PAM responder or
the user.

To select a certificate MIT Kerberos provides the "X509\_user\_identity"
option which can be set with krb5\_get\_init\_creds\_opt\_set\_pa().
This is the same option which can be set with the -X option of the kinit
command. For PKCS\ `#11 <https://pagure.io/SSSD/sssd/issue/11>`__ the
syntax of the identify string is ::

    PKCS11:[module_name=]modname[:slotid=slot-id][:token=token-label][:certid=cert-id][:certlabel=cert-label]

From the krb5.conf man page: "All keyword/values are optional. modname
specifies the location of a library implementing
PKCS\ `#11 <https://pagure.io/SSSD/sssd/issue/11>`__. If a value is
encountered with no keyword, it is assumed to be the modname. If no
module-name is specified, the default is opensc-pkcs11.so. slotid=
and/or token= may be specified to force the use of a particular smartcard
reader or token if there is more than one available. certid= and/or
certlabel= may be specified to force the selection of a particular
certificate on the device. See the pkinit\_cert\_match configuration
option for more ways to select a particular certificate to use for
PKINIT."

Sending the 'modname', 'token-label' and 'certid' would be sufficient to
select the certificate on the
PKCS\ `#11 <https://pagure.io/SSSD/sssd/issue/11>`__ level. But
unfortunate this does not contain any detail of the certificate itself.
It is recommended that 'certid' which maps to CKA\_ID
PKCS\ `#11 <https://pagure.io/SSSD/sssd/issue/11>`__ attribute is the
SHA1 value of the modulus of the RSA key but this is not enforced at any
place. To make sure that the PKINIT plugin really users the certificate
we expect it to use pkinit\_cert\_match must be used. Unfortunately
there is no direct library call to set it the plugin will read it
directly from the profile of the krb5\_context. This means that SSSD
must modify the profile can create a new krb5\_context with
krb5\_init\_context\_profile(). While looking for a value for
pkinit\_cert\_match the PKINIT plugin first checks if the option can be
found a realm sub-section in the [libdefaults] section where the realm
must match the realm of the client principal, i.e. the principal which
tries to authenticate.

As matching string
"<ISSUER>certificateIssuer<SUBJECT>certificateSubject" can be used.
Although there is a NSS implementation for the PKINIT plugin available
in the MIT Kerberos source code it is neither used in recent Fedora or
RHEL versions but the OpenSSL implementation is used. To avoid when
translating the ASN.1 representation of the issuer and subject from the
certificate to a DN string krb5\_child should use OpenSSL
unconditionally for this translation independent of the setting of the
'--with-crypto' configure option.

With "X509\_user\_identity" and "pkinit\_cert\_match" set the available
choices for the PKINIT plugin should be sufficiently restricted so that
not accidentally a wrong certificate is selected. It should even prevent
the scenario where an attacker replaces the Smartcard between mapping
the Smartcard to a system user and doing the PKINIT based
authentication.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

/etc/krb5.conf
^^^^^^^^^^^^^^

Besides 'pkinit\_anchor' there are two krb5.conf options which might
need to be set on the client to make PKINIT work,
'pkinit\_eku\_checking' and 'pkinit\_kdc\_hostname'.

By default the PKINIT plugin of MIT Kerberos expects that the KDC
certificate contains the id-pkinit-KPKdc EKU as defined in RFC 4556 and
has the KDC's hostname in id-pkinit-san as defined in RFC4556 as well.

If id-pkinit-san is missing 'pkinit\_kdc\_hostname' can be set to the
hostname of the KDC as stored in the dNSName in the SAN of the
certificate. If the dNSName SAN is missing as well, PKINIT won't work.

If the id-pkinit-KPKdc EKU is not set 'pkinit\_eku\_checking' can be set
to 'kpServerAuth' is the certificate of the KDC at least contains the
id-kp-serverAuth EKU. If this is missing as well 'pkinit\_eku\_checking'
can be set to 'none', but this is not recommended.

See the krb5.conf man page for details about the options.

In theory it would be possible that SSSD sets this options automatically
to make PKINIT work without adding options to krb5.conf manually. One
way would be to inspect the certificate presented by the KDC and set to
options according to the certificate content. But since SSSD does not
have any knowledge what content would be expected it might unknowingly
lower the security by receiving a spoofed ticket. It would be possible
to add now options for SSSD but then it would be more easy to add the
options directly to /etc/krb5.conf. With the recently introduced
/etc/krb5.conf.d/ drop-in directory for config snippets a suitable
snippets must be only created once and added to /etc/krb5.conf.d/ on the
clients.
