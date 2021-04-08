Smartcard authentication - Step 1 (local authentication)
========================================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/546 <https://pagure.io/SSSD/sssd/issue/546>`__
-  `https://pagure.io/SSSD/sssd/issue/2711 <https://pagure.io/SSSD/sssd/issue/2711>`__

Problem statement
~~~~~~~~~~~~~~~~~

Smartcard based authentication is another alternative to password based
authentication. Other than OTP tokens where all authentication data can
be entered at a password prompt Smartcards require special hardware and
software to access the credentials stored on the card.

Currently solutions are based on the pam\_pkcs11 module which e.g.
requires special configuration to map the certificate stored on a
Smartcard to a user. Since SSSD already can map certificates to users
(see e.g. `LookupUsersByCertificate
<https://docs.pagure.org/SSSD.sssd/design_pages/lookup_users_by_certificate.html>`__)
integration would be much easier. Additionally features like different
authentication types per user or per service would only be possible with
SSSD.

Use cases
~~~~~~~~~

Local authentication
^^^^^^^^^^^^^^^^^^^^

If there is a Smartcard reader connected to a system the user can
authenticate to the system by placing his smartcard into the reader,
give his name (might not be needed in some cases) and the Smartcard PIN
at the login prompt and is authenticated successfully if the certificate
on the Smartcard is valid and satisfies other, configurable criteria.
This includes authentication at a text or graphical console but local
services like *su* and *sudo* as well.

Remote authentication with ssh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To avoid password authentication ssh supports public-private key based
authentication from the beginning. Since the certificates on the
Smartcard are stored together with the PIN protected private key this
key material can be used for ssh authentication as well. On the client
side a ssh client program is needed which is able to access the
Smartcard. On the server side only the public key from the certificate
is needed in a suitable format for ssh. With the help of the
*sss\_ssh\_authorized\_keys* utility SSSD can make this information
available to the sshd running on the server if the certificate is stored
together with the other user data in a central storage, e.g. LDAP.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

To enable certificate based authentication in SSSD *pam\_cert\_auth*
must be set to *True* in the *[pam]* section of *sssd.conf*.

Additional option to tune e.g. the certificate validation will be added
later.

How to test
~~~~~~~~~~~

In the following it is assumed that SSSD is running on an IPA client.

Hardware reader and card
^^^^^^^^^^^^^^^^^^^^^^^^

Configuring IPA client for local authentication with a Smartcard
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

The most easy way to test is with a Smartcard reader and a Smartcard. If
the Smartcard reader is supported by the *coolkey* package the needed
PKCS#11 modules is already added to the central NSS database at
/etc/pki/nssdb during the installation of the package. In case a different
PKCS#11 module is needed it can be added with modutil ::

    modutil modutil -dbdir /etc/pki/nssdb -add "My PKCS#11 modules" -libfile libmypkcs11.so

(if the PKCS#11 modules in not in the default library search path and
full path is needed).

Now *certutil* should ask for a PIN and show your certificate, if the
reader is connected and the card is in ::

    certutil -L -d /etc/pki/nssdb -h all

Most probably the certificate on the card is currently not assigned to
an IPA user. To do this the certificate can be extracted with ::

    certutil -L -d /etc/pki/nssdb -n 'Certificate Nick-Name' -a

which will dump the PEM encoded certificate. Since the *ipa* utility
expected the base64 string from the PEM encoding in a single line ::

    certutil -L -d /etc/pki/nssdb -n 'Certificate Nick-Name' -a | grep -v -- '----' |tr -d '[\n\r]'

will dump it in a single line. Now *ipa user-mod username
--certificate=MIIE......* can be used to load the certificate into the
user entry. Please note that the --certificate option is only available
with FreeIPA 4.2 or later.

If *pam\_cert\_auth = True* in the *[pam]* section of *sssd.conf*, the
card is inserted in the reader and the certificate loaded in the user
entry e.g. the console login prompt should now ask for a PIN instead of
a password and if the correct PIN is entered the user should be
successfully authenticated and logged in.

Running an ssh client with Smartcard support
''''''''''''''''''''''''''''''''''''''''''''

The *ssh* client program distributed with Fedora or RHEL contains
patches which add Smartcard support to the utility. To activate it the
needed PKCS#11 module to talk to the Smartcard reader has to be made
available with the *-I* option ::

    ssh -I /usr/lib/libmypkcs11.so -l ipauser ipahost.ipa.domain

where the certificate has to be added to the IPA user entry as described
above.

Software certificates with libsoftokn3.so
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First a certificate together with the private key is needed.
Instructions how to create certificates with FreeIPA can e.g. be found
at
`http://www.freeipa.org/page/PKI <http://www.freeipa.org/page/PKI>`__.
Please store the certificate in a NSS database. Since in this this first
step the user is looked up with the help of the full certificate any
certificate valid for client authentication can be used. This means
instead of creating a new one an existing certificate can be used.
**Please do this only in test environment which will be discarded
afterwards. Copying certificates from a production environment is a
security breach.**

Configuring IPA client for local authentication with a Smartcard
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Like in the case with a hardware reader a PKCS#11 module to access
the certificate in the NSS DB must be added to the systems NSS DB in
/etc/pki/nssdb. The PKCS#11 module for accessing certificates and private
keys in a NSS database is *libsoftokn3.so*. But unfortunately this
module needs some configuration option when loaded. Although I guess
*modutil* should work as well I was only able to add the needed
parameters with *pk11install* from the coolkey package. In the
following we assume that the certificate and the private key is stored
in an NSS DB called *my\_cert* in the home directory of the user. ::

    pk11install -i -v -p /etc/pki/nssdb 'name=soft parameters="configdir=sql:/home/use/my_cert dbSlotDescription=\"My Slot\" dbTokenDescription=\"My Token\"" library=/usr/lib/libsoftokn3.so'

If *pam\_cert\_auth = True* in the *[pam]* section of *sssd.conf*, and
the certificate loaded in the user entry e.g. the console login prompt
should now ask for a PIN instead of a password and if the correct PIN is
entered the user should be successfully authenticated and logged in.

Running ssh client with Smartcard support
'''''''''''''''''''''''''''''''''''''''''

The PKCS#11 module for accessing certificates and private keys in a NSS
database is *libsoftokn3.so*. But unfortunately this modules needs some
configuration option when loaded and there is (AFAIK) currently no way
to pass them with the *ssh* command. Luckily there is p11-kit which can
be used to load *libsoftokn3.so* with options. In the following we
assume that the certificate and the private key is stored in an NSS DB
call *my\_cert* in the home directory of the user.

To configure p11-kit make sure *~/.config/pkcs11* and
*~/.config/pkcs11/modules* exists and create the following two files: ::

    cat > ~/.config/pkcs11/pkcs11.conf << EOF_EOF
    user-config: only
    EOF_EOF

::

    cat > ~/.config/pkcs11/modules/my_cert.module << EOF_EOF
    module: /usr/lib/libsoftokn3.so
    x-init-reserved: configdir='sql:/home/user/my_cert'
    critical: yes
    EOF_EOF

On 64bit systems you have to use */usr/lib64/libsoftokn3.so*.

Now *ssh* can be called with */usr/lib/p11-kit-proxy.so* (or the 64bit
version) ::

    ssh -I /usr/lib/p11-kit-proxy.so -l ipauser ipahost.ipa.domain

Software certificates with libsofthsm2.so
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since the *libsoftokn3.so* PKCS#11 module requires additional configuration
which most consumers like the *ssh* client (see above) or *kinit* do not
support and the workaround with *p11-kit-proxy.so* might not always be
possible the following section will show how the *libsofthsm2.so*
PKCS#11 module from the `OpenDNSSEC <http://www.opendnssec.org/>`__
project can be used. As above we assume that the certificate and the
corresponding private key are available.

Authors
~~~~~~~

-  Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
