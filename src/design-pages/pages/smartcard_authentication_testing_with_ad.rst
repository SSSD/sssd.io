Smartcard authentication - Testing with AD
==========================================

As mentioned on `SmartcardAuthenticationStep1
<https://docs.pagure.org/SSSD.sssd/design_pages/smartcard_authentication_step1.html>`__
the primary focus of the development was the authentication to an IPA
client. Nevertheless, the general authentication code path is the same
and when the needed requirements are met it can be used to authenticate
on a AD domain client as well. But please note that as with an IPA
client this will only be a local authentication, so far no Kerberos
tickets will be available after authentication. pkinit will be added in
one of the next steps.

As with IPA the current requirement is that the full certificate is
stored in the user's LDAP entry in AD. Since the AD CA uses the
userCertificate attribute for this as well we will further assume that
this attribute is used to store the certificate.

By default the SSSD AD provider does not read certificates, so this must
be set in sssd.conf with the option ::

    ldap_user_certificate = userCertificate;binary

*(I guess it would make sense to set this by default)*

Additionally, the AD provider will not create the indication file for
the pam\_sss client that pre-authentication is available and it has to
be created manually ::

    touch /var/lib/sss/pubconf/pam_preauth_available

*(I guess it would make sense that the PAM responder creates the file is
certificate authentication is enabled.)*

Next, certificate authentication must be enabled in the pam section of
sssd.conf by setting ::

    pam_cert_auth = True

Finally, CA certificates should be imported in the systems NSS database
to be able to verify the certificate. ::

    certutil -d /etc/pki/nssdb -A -n 'My Issuer' -t CT,CT,CT -a -i /path/to/cert/in/PEM/format

These steps are needed on the client and now we will discuss how a
certificate can be added to the AD user entry and together with the keys
to a Smartcard.

Certificates from AD CA
-----------------------

If you do not have a Certificate Server in your AD domain you have to
install one by enabling the 'Active Directory Certificate Service' on
one of the servers in the domain.

To allow users to request certificates follow the steps in
`https://msdn.microsoft.com/en-us/library/cc770857.aspx <https://msdn.microsoft.com/en-us/library/cc770857.aspx>`__
.

Now AD user should be able to request a user certificate from the AD CA.
For this the user should open the Management Console, e.g. via
Start->Run->\ *mmc*. In the Management Console the Certificates snap-in
can be activated via File->Add/Remove-Snap-ins.
In the Certificates snap-in the 'All Tasks' context menu should offer
'Automatically Enroll and Retrieve Certificates' where you can choose
new user certificate template which was created in the instructions from
MSDN. If no templates are available you should check the steps from the
MSDN instructions again or check if there is already a certificate
generated for the user by looking at the 'Personal' folder of the
Certificates snap-in. Here you will find the freshly created certificate
as well.

Now you have to write the certificate and the keys to a Smartcard. You
can use a suitable Windows tool for this. Or you can export the data and
write it to a Smartcard from a GNU/Linux client which will be explained in
the following.

To export the certificate select it in the Certificates Snap-in and call
'Export' from the 'All Tasks' context menu. In the export wizard the
private key must be exported as well. The generated file can now be
copied to a GNU/Linux host.

The file created on the AD side is PKCS#12 formatted and can be inspected
on the GNU/Linux side with the *openssl pkcs12* utility. NSS, which is
currently used by SSSD to access the Smartcard, expected that the
Smartcard will contain the certificate together with the public and
private key in separate objects, connected by the same label and id.
We will use pkcs11-tool from the opensc package to write the data to the
card. In general p11tool from the gnutls project can be used as well but
support for writing public keys was added quite recently (gnutls-3.4.6)
so it might no be available on your platform. There might be an issue
with pkcs11-tool as well, if after writing to the card the certificate
and the public key are only visible after you logged into the card, i.e.
entered the PIN, you need a newer version of pkcs11-tool as well.

Extracting keys and certificate from PKCS#12 file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extracting the certificate and storing it in DER encoding ::

    openssl pkcs12 -in ./ad_user.pfx -nokeys -out ./cert.pem
    openssl x509 -in ./cert.pem -outform der -out ./cert.der

Extracting the private key and storing it in DER format. Please note
that the private key in priv.pem and priv.der is not encrypted, please
remove the files as soon as possible ::

    openssl pkcs12 -in ./ad_user.pfx -nocerts -nodes -out ./priv.pem
    openssl rsa -in ./priv.pem -outform der -out ./priv.der

Extracting the public key from the certificate and storing it in DER
encoding ::

    openssl x509 -in ./cert.pem -pubkey -noout | openssl rsa -pubin -outform der -out ./pubkey.der

Writing certificate and keys to a Smartcard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First write the certificate data to the Smartcard by calling ::

    pkcs11-tool --module my_pkcs11_module.so --slot 0 -w ./cert.der -y cert -a 'My Label' --id 0123456789abcdef0123456789abcdef01234567

where *my\_pkcs11\_module.so* and *My Label* should be replaced by
suitable values. The id value is typically the Subject Key Identifier
which is typically the sha1 hash value of the public key bit string from
the certificate. The value can either obtained from the output of ::

    openssl x509 -in ./cert.pem -text | grep -A 1 'Subject Key Identifier:'

or by inspecting the public key with ::

    openssl asn1parse -inform der -in ./pubkey.der
        0:d=0  hl=4 l= 290 cons: SEQUENCE
        4:d=1  hl=2 l=  13 cons: SEQUENCE
        6:d=2  hl=2 l=   9 prim: OBJECT            :rsaEncryption
       17:d=2  hl=2 l=   0 prim: NULL
       19:d=1  hl=4 l= 271 prim: BIT STRING
    openssl asn1parse -inform der -in ./pubkey.der -strparse 19 -noout -out /dev/stdout |sha1sum

where the *19* in the second call has to match the offset value shown
for the *BIT STRING* component in the output of the first call.

The label and the id should be the same when writing the public and the
private key object to indicated to applications that the 3 objects
belong to each other.

As a second step the public key is written to the Smartcard by calling ::

    pkcs11-tool --module my_pkcs11_module.so --slot 0 -w ./pubkey.der -y pubkey -a 'My Label' --id 0123456789abcdef0123456789abcdef01234567

And finally the private key can be written by calling ::

    pkcs11-tool --module my_pkcs11_module.so --slot 0 -w ./priv.der -y privkey -a 'My Label' --id 0123456789abcdef0123456789abcdef01234567 -l

Since the private key must be protected by the PIN you have to login to
the Smartcard first, this is done with the help of the *-l* option which
instructs *pkcs11-tool* to ask for the PIN and login before writing the
certificate.

Now the Smartcard content should look like ::

    pkcs11-tool --module my_pkcs11_module.so --slot 0 --list-objects -l
    Logging in to "My Token".
    Please enter User PIN:
    Private Key Object; RSA
      label:      My Label
      ID:         0123456789abcdef0123456789abcdef01234567
      Usage:      decrypt, sign, unwrap
    Public Key Object; RSA 2048 bits
      label:      My Label
      ID:         0123456789abcdef0123456789abcdef01234567
      Usage:      encrypt, verify, wrap
    Certificate Object, type = X.509 cert
      label:      My Label
      ID:         0123456789abcdef0123456789abcdef01234567

If the PKCS#11 module is properly added to the system's NSS database (see
`https://docs.pagure.org/SSSD.sssd/design_pages/smartcard_authentication_step1#configuring-ipa-client-for-local-authentication-with-a-smartcard <https://docs.pagure.org/SSSD.sssd/design_pages/smartcard_authentication_step1.html#configuring-ipa-client-for-local-authentication-with-a-smartcard>`__
for details) p11\_child should be able to return the certificate ::

    /usr/libexec/sssd/p11_child --pre --nssdb=/etc/pki/nssdb

If this works well SSSD should now be able to authenticate the AD user
with the help of the Smartcard.

Certificate from an external CA
-------------------------------

There are various ways how to get a certificate from an external CA, see
e.g.
`https://blog-nkinder.rhcloud.com/?p=179 <https://blog-nkinder.rhcloud.com/?p=179>`__
how to generate the keys on a Smartcard, request a certificate from a CA
and store it on the Smartcard. As a result the certificate and all the
needed keys are already on the Smartcard. In the following we will
explain how to make AD aware of it and enable local Smartcard login for
an AD user.

In other situations the certificate and the keys might be available as
files. The previous section should help to convert the file content into
DER encoded objects and write them to a Smartcard.

Reading the certificate from the Smartcard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The certificate can be read with various tools like *certutil*,
*pkcs11-tool* or *p11tool*. But using SSSD'S *p11\_child* has the
advantage that it is verified that SSSD can access the certificate as
well. ::

    /usr/libexec/sssd/p11_child --pre --nssdb=/etc/pki/nssdb | tail -1 | base64 -d > ./cert.der

should write the DER encode certificate data into the file *cert.der*.
If there are any issue you can call ::

    /usr/libexec/sssd/p11_child --pre -d 10 --debug-fd=2 --nssdb=/etc/pki/nssdb

to see the full debug output which might help to identify what is going
wrong.

Writing the certificate to AD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the following operations the permissions of the AD user which should
get the certificate are sufficient. So either login as the user or call
*kinit `aduser@AD.DOMAIN <mailto:aduser@AD.DOMAIN>`__*.

First the distinguished name (DN) of the user object in AD has to be
identified with ::

    ldapsearch -Y GSSAPI -H ldap://ad-dc.ad.domain -b 'dc=ad,dc=domain' samAccountName=aduser dn

In the most easy case the DN will look like
*CN=aduser,CN=Users,DC=ad,DC=domain*.

With this DN a simple LDIF file can be created ::

    dn: CN=aduser,CN=Users,DC=ad,DC=domain
    changetype: modify
    add: userCertificate
    userCertificate:< file:cert.der

With this LDIF file the certificate can be loaded into the aduser entry ::

    ldapmodify -Y GSSAPI -H ldap://ad-dc.ad.domain -f file.ldif

Now SSSD can check if the certificate belongs to the aduser and can
authenticate the aduser locally with the Smartcard. Please note that
SSSD might have a valid user entry in the cache and will not read the
freshly added certificate immediately. To force a refresh just call
*sss\_cache -u `aduser@ad.domain <mailto:aduser@ad.domain>`__*.
