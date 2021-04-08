Lookup Users by Certificate
===========================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2596 <https://pagure.io/SSSD/sssd/issue/2596>`__
-  `https://pagure.io/SSSD/sssd/issue/546 <https://pagure.io/SSSD/sssd/issue/546>`__
-  `https://pagure.io/freeipa/issue/4238 <https://pagure.io/freeipa/issue/4238>`__
   (design page:
   `http://www.freeipa.org/page/V4/User\_Certificates <http://www.freeipa.org/page/V4/User_Certificates>`__)

Problem statement
~~~~~~~~~~~~~~~~~

As stated in ticket
`#2596 <https://pagure.io/SSSD/sssd/issue/2596>`__ applications doing
user authentication based on certificates, e.g. web servers, need a way
to map the certificate presented by the client to a specific user.
Although there are various ways to derive a user name from special
entries in the certificate so far there is no generally accepted scheme.
The most general and in some cases the only possible way is to look up
the certificate directly in the LDAP server. This requires that the
certificate is stored in the LDAP server which we will assume for this
initial design. (In a second part user lookups based on the certificate
content will be added, this requires that the syntax for the mapping is
specified in
`http://www.freeipa.org/page/V4/User\_Certificates#Certificate\_Identity\_Mapping <http://www.freeipa.org/page/V4/User_Certificates#Certificate_Identity_Mapping>`__)

The primary interface to lookup users by certificate would be D-BUS.

Use cases
~~~~~~~~~

The primary use case is described in ticket
`#2596 <https://pagure.io/SSSD/sssd/issue/2596>`__. If Apache is
configured to use certificate based client authentication modules like
mod\_lookup\_identity has access to the PAM encoded certificate via
environment variables. With this data as input mod\_lookup\_identity
should call a D-BUS method like
*org.freedesktop.sssd.infopipe.GetUserAttrByCert* which will return the
data of the user the certificate belongs similar to the *GetUserAttr*
method.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

Besides adding the D-Bus method to the InfoPipe responder the generic
LDAP backend should be able to search and read the certificate data if
available from a LDAP server and store it to the cache. The internal
sysdb interface must be extended to search cached entries with the
certificate as input.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

LDAP backend
^^^^^^^^^^^^

Reading certificate data if available just requires adding a new user
attribute which will be requested during LDAP searches for a user. In
general the certificate is stored as a DER encoded binary on the LDAP
server. **Question: should we add an option like
ldap\_user\_cert\_encoding to support other encodings a server might
send to us, or shall we add it only when there is a real use case?**
Internally the certificate should be stored DER encoded to the cache as
well because this encoding is the most unambiguous encoding (e.g. with
PEM encoding it is not clear if the base64 blob should have line breaks
or not and if the enclosing '-----BEGIN CERTIFICATE-----' and '-----END
CERTIFICATE-----' should be stored as well and if line break should be
added here or not?)

To search a user with the help of the certificate the DER encoded binary
ticket must be transformed into a search filter. In this case it would
be something like 'userCertificate=\\23\\a5\\3e......' where each byte
from the certificate is represented by a hex value prepended by a
'\\'. The filter should be generated in a subroutine which accepts the
DER encoded certificate with base64 ASCII armor and returns the search
filter. This way the subroutine can later be extended to accept
configuration options for the identity mapping and can return different
search filters for those cases. Since the requirement for LDAP and sysdb
search filters are the same there should be an option indicating if a
LDAP or sysdb filter is needed, because the attribute names might be
different.

Although it would be possible to handle the binary DER data directly I
think using a base64 ASCII armor to handle the data as a string is
useful to avoid adding code for handling binaries e.g. in the S-BUS
requests to the backends.

SYSDB API
^^^^^^^^^

A new call sysdb\_search\_user\_by\_cert() should be added which get the
DER encoded certificate with base64 ASCII armor as input and use the
function described above to get a proper search filter. Currently it
will be only the search filter for the binary certificate. Other than
that the new call will act like to other sysdb\_search\_user\_by\_\*()
calls.

InfoPipe
^^^^^^^^

A new method GetUSerAttrByCert() must be implemented which expected the
PEM encoded certificate and an array of attribute names. **Question:
Should we only support PEM here or other formats as well? In this case
we need a third parameter indicating the encoding of the certificate
data.**.
InfoPipe will convert the certificate into DER encoding with base64 ASCII
armor, search the cache and eventually forward the request to the backend.
The request to the backend is processed similar to a request by name,
only that a new filter name, e.g. DP\_CERT\_ID "cert", is needed.

Since it is in general not obvious to which domain a certificate
belongs, the search must iterate over all domains in case no matching
certificate was found. For the cases where there is a strong 1:1
relationship between the issuer of a certificate and a domain,
configuration options for this can be added later.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

A new user attribute open 'ldap\_user\_certificate' will be added to the
LDAP provider. By default only the IPA provider will set a value for it
to avoid reading about 1k of data which is not needed in the other
providers. **Question: Does this make sense or shall we enable it for
other providers as well?**

How To Test
~~~~~~~~~~~

First a certificate must be load to a IPA user entry, it can be any kind
of certificate as long as it is valid an DER or PEM encoded. Until IPA
has some import utilities ldapmodify should be used. A LDIF file might
look like this: ::

    dn: uid=cert_user,cn=users,cn=accounts,dc=ipa,dc=devel
    changetype: modify
    add: userCertificate;binary
    userCertificate;binary::MII...=

where MII...= indicates the base64 encoded certificate data. If you have
a PEM encoded certificate you can just use the base64 part here. If the
certificate is DER encoded it can be transformed to base64 with ::

    base64 < ./certificate_file.der | tr -d '\n'

Testing can be done with the help of the dbus-send utility: ::

    # dbus-send --system --print-reply  --dest=org.freedesktop.sssd.infopipe \
                                             /org/freedesktop/sssd/infopipe/Users \
                                             org.freedesktop.sssd.infopipe.Users.FindByCertificate \
                                             string:"-----BEGIN CERTIFICATE-----.......-----END CERTIFICATE-----"
    method return sender=:1.1479 -> dest=:1.1498 reply_serial=2
       object path "/org/freedesktop/sssd/infopipe/Users/ipa_2edevel/240600004"

    # dbus-send --system --print-reply --dest=org.freedesktop.sssd.infopipe /org/freedesktop/sssd/infopipe/Users/ipa_2edevel/240600004 org.freedesktop.DBus.Properties.Get string:"org.freedesktop.sssd.infopipe.Users.User" string:"name"
    method return sender=:1.1479 -> dest=:1.1529 reply_serial=2
       variant       string "cert_user"

    # dbus-send --system --print-reply --dest=org.freedesktop.sssd.infopipe /org/freedesktop/sssd/infopipe/Users/ipa_2edevel/240600004 org.freedesktop.DBus.Properties.GetAll string:"org.freedesktop.sssd.infopipe.Users.User"
    method return sender=:1.1479 -> dest=:1.1530 reply_serial=2
       array [
          dict entry(
             string "name"
             variant             string "cert_user"
          )
          dict entry(
             string "uidNumber"
             variant             uint32 240600004
          )
          dict entry(
             string "gidNumber"
             variant             uint32 240600004
          )
          dict entry(
             string "gecos"
             variant             string "ipa u1"
          )
          dict entry(
             string "homeDirectory"
             variant             string "/home/cert_user"
          )
          dict entry(
             string "loginShell"
             variant             string "/bin/sh"
          )
          dict entry(
             string "groups"
             variant             array [
                   object path "/org/freedesktop/sssd/infopipe/Groups/ipa_2edevel/240600004"
                   object path "/org/freedesktop/sssd/infopipe/Groups/ipa_2edevel/240600005"
                   object path "/org/freedesktop/sssd/infopipe/Groups/ipa_2edevel/240600006"
                ]
          )
          dict entry(
             string "extraAttributes"
             variant             array [
                ]
          )
       ]

The first dbus-send command shows the lookup by certificate, the
following two just illustrate how a single property or all can be
requested from the returned object path.

Authors
~~~~~~~

-  Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
