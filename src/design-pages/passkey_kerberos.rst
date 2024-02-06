Passkey authentication Kerberos integration
=======================================================

Related ticket(s):
------------------
 * https://github.com/SSSD/sssd/issues/6228

Problem statement
-----------------
The use of new tools to authenticate users, such as 2FA, U2F and FIDO2, is
becoming increasingly popular. Currently SSSD provides local authentication of
a centrally managed user with passkeys, but it doesn't provide any way to
authenticate remotely to a system. This diminishes the value provided by SSSD
in some environments like big companies and governments, where remote
authentication is a common pattern.

This design is an extension of the
`enable passkey authentication <https://sssd.io/design-pages/passkey_authentication.html>`__,
where a centrally managed user can authenticate locally in a system with a
passkey token. It describes a Kerberos pre-authentication mechanism using
passkey authentication. Once it is completed, the received initial ticket
granting ticket (TGT) can be used for single sign-on into other
Kerberos-enabled services.

For that purpose SSSD needs to be modified to accommodate the new workflow,
while still allowing the old one, where the user was authenticated locally
without issuing any Kerberos ticket. The new workflow is used for online
authentication against an IPA server. The old workflow is used for any offline
authentication and for AD and other LDAP servers.

For the purpose of this feature, passkey is a FIDO2 compatible device supported
by the libfido2 library.

Use cases
---------
As a user, not only do I want to sit in front of a system enrolled into a
centralized identity management solution and log in (desktop and/or terminal)
using a passkey device connected to the system, but I also want to get a
Kerberos ticket to identify myself to other services.

Solution overview
-----------------
.. uml:: ../diagrams/passkey_kerberos_architecture_diagram.pu

* SSSD provides a pre-authentication method implementation (pre-auth plugin) to
  MIT Kerberos library.

* When both the libkrb5 and the KDC support the same pre-authentication method,
  KDC responds to an AS-REQ message with a request to provide the assertion
  data required by the pre-authentication method.
  
* SSSD's pre-auth plugin obtains the assertion data from the passkey.

* The assertion data is sent by libkrb5 back to the KDC server as a part of the
  AS-REQ exchange.

* The KDC server in turn relays the request to the ipa-otpd, which retrieves
  the user information and ask the passkey_child to validate the assertion.

* Once validated the Kerberos KDC issues a ticket and sends it to SSSD via
  libkrb5.

Authentication method policy
****************************

This design adds some complexity to the authentication process, as it adds
another mechanism. This may lead to a degraded user experience. For this
reason, the following authentication policy is implemented:

* In the online case, the default policy is to ``try only methods which will
  return a Kerberos ticket``. The order for the authentication methods 
  mechanisms can be tuned with the :ref:`auth_order<auth-order>` option.

* For the offline case, in order to offer a consistent behaviour with the
  online case, the user object stores the available authentication methods.
  The authentication is performed based on the available methods for the user,
  the tuning from :ref:`local_auth_policy<local-auth-policy>` option, and the
  order defined in :ref:`auth_order<auth-order>`.

* The user may decide to skip the passkey authentication by entering some
  characters in the interactive prompt; or if the user-verification is enabled,
  by entering an empty PIN.

Implementation details
----------------------

General overview
****************
When SSSD support for passkey authentication is enabled, the KDC advertises
the support for passkey during AS-REQ request. If information about the
Kerberos principal on the KDC side allows use of passkey authentication, KDC
responds with a pre-authentication data to choose passkey authentication.

If the KDC doesn't support passkey authentication, or if the KDC isn't
available, then the local authentication with passkey of a centrally managed
user is performed.

The following sequence diagram illustrates the workflow taking into account all
the components involved in it:

.. uml:: ../diagrams/passkey_kerberos_sequence_diagram.pu

* The user tries to login with a centrally managed account in the system.

* PAM relays this request to SSSD’s PAM responder.

* The PAM responder retrieves the user information from the cache.

* The PAM responder tries to pre-authenticate the user.

* The IPA provider executes the krb5_child, which in turn uses libkrb5 to
  communicate with the Kerberos KDC.

* libkrb5 sends an AS-REQ with the pre-authentication data.

* Kerberos KDC receives the AS-REQ and queries Kerberos database driver (KDB)
  for the information about the Kerberos principal. It finds out that the
  principal object supports passkey pre-authentication. Then, KDC side of the
  pre-authentication method implementation uses RADIUS protocol to communicate
  with IPA server side (ipa-otpd daemon listens over UNIX domain socket used by
  the KDC). The RADIUS message Access-Request is sent to ipa-otpd.

* ipa-otpd retrieves the user information and generate the assertion request
  data (more information on the format in :ref:`kerberos-kdc-ipa-otpd`), which
  is used to fill the Reply-Message that is returned to the Kerberos KDC.

* The passkey assertion request data produced by the KDC side of the
  pre-authentication method implementation is returned to libkrb5 in an error
  response.

* This information is passed between the various components until it reaches
  the PAM responder. It requests PAM to get the PIN from the user and it
  executes the passkey_child helper process with the assertion request data and
  the PIN as arguments.

* The passkey_child requests the assertion with the assertion request data and
  the PIN.

* The passkey returns the assertion data, which also is returned by the
  passkey_child.

* The PAM responder fills the pre-authentication with the assertion data. The
  PAM responder checks if it matches with the one stored in the LDAP attribute,
  and it fails if they don't match.

* libkrb5 send another AS-REQ but this time with the assertion in the
  pre-authentication.

* The Kerberos KDC generates the second Access-Request message, which contains
  the assertion data.

* ipa-otpd asks the passkey_child that is located in the FreeIPA server to
  validate the assertion data. It replies with Access-Accept/Reject depending
  on the authentication result.

* If the validation is successful the Kerberos KDC issues a ticket and wrap it
  in AS-REP.

* krb5_child stores the ticket and return the authentication success to the IPA
  provider. This information is propagated by the PAM responder, PAM and
  finally the user.

Data structures
***************
This section defines the data needed to obtain and verify the assertion.

Assertion request data
++++++++++++++++++++++
To obtain the assertion the following information is required:

* Domain (String)

* List of credential IDs in b64 (String)

* User-verification (Int)

* Cryptographic challenge (String)

.. _assertion-data:

Assertion data
++++++++++++++
To verify the assertion the following informations is required:

* Username (String)

* Domain (String)

* Used credential ID in b64 (String)

* Public key in b64 (String)

* COSE type (String)

* User-verification (Int)

* Cryptographic challenge (String)

* Authenticator data in b64 (String)

* Assertion signature in b64 (String)

.. _kerberos-kdc-ipa-otpd:

Kerberos KDC - ipa-otpd
+++++++++++++++++++++++
The Kerberos KDC is expected to provide the following json-formatted string
when generating the first Access-Request:

..  code-block:: json

    "passkey": {
        "phase": 0
    }

ipa-otpd is expected to return a json-formatted string with the assertion
request data:

..  code-block:: json

    "passkey": {
        "phase": 1,
        "state": "$ipa_otpd state",
        "data": {
            "domain": "$domain",
            "credential_id": "$credential_id_list",
            "user_verification": "$user_verification",
            "cryptographic_challenge": "$cryptographic_challenge"
        }
    }

The second Access-Request generated by the Kerberos KDC should contain the
following json-formatted string in the password field:

..  code-block:: json

    "passkey": {
        "phase": 2,
        "state": "$ipa_otpd state",
        "data": {
            "credential_id": "$credential_id",
            "cryptographic_challenge": "$cryptographic_challenge",
            "authenticator_data" :"$authenticator_data",
            "assertion_signature": "$assertion_signature",
            "user_id": "$user_id"
        }
    }

ipa-otpd - passkey_helper
+++++++++++++++++++++++++
The passkey_helper process located in the FreeIPA server needs to regenerate
the assertion data to be validated by the passkey. ipa-otpd executes the
passkey_helper and thus, it is in charge of providing the assertion data as
:ref:`previously specified<assertion-data>`.

Configuration options
*********************

sssd
++++

The following domain option can be used to tune the authentication policy:

.. _local-auth-policy:

* local_auth_policy: local authentication methods policy. Some backends (i.e.
  LDAP, proxy provider) only support a password base authentication, while
  others can handle PKINIT based Smartcard authentication (AD, IPA), two-factor
  authentication (IPA), or other methods against a central instance. By default
  in such cases authentication is only performed with the methods supported by
  the backend.

  To allow more convenient or secure authentication methods which are supported
  by SSSD, but not by the backend in cases where a central authentication is
  not strictly required the `local_auth_policy` option is added.

  There are four possible values for this option: match, only, enable and
  disable. ``match`` is used to match offline and online states for Kerberos
  methods. ``only`` ignores the online methods and only offer the local ones.
  ``enable`` and ``disable`` define the methods for local authentication. As an
  example, ``enable:passkey``, only enables passkey for local authencation.

  ``local_auth_policy`` is evaluated for all ``auth_providers``, including
  ``none``. The following configuration example allows local users to
  authenticate locally using any enabled method (i.e. smartcard, passkey).

..  code-block:: RST

  	[domain/shadowutils]
	id_provider = proxy
	proxy_lib_name = files
	auth_provider = none
	local_auth_policy = only

The following prompting option (i.e. [prompting/sudo]) can be used to tune the
authentication policy:

.. _auth-order:

* auth_order: authentication methods order policy. This is an ordered list of
  the authencation methods. If the method isn't available for the user, then it
  will be skipped. Example: passkey, 2fa, password. Default: password.

FreeIPA
+++++++

In order for the administrator to enhance security and disable deprecated
algorithms, a new IPA setting is required. This new option forces the use of a
COSE algorithm when generating the keys. The setting holds a string (i.e.
es256, rs256).

Authors
-------
 * Iker Pedrosa <ipedrosa@redhat.com>
