Passkey - Authentication in a centralized environment
=======================================================

Related ticket(s):
------------------
 * https://github.com/SSSD/sssd/issues/6228

Problem statement
-----------------
The use of new tools to authenticate users, such as 2FA, U2F and FIDO2, is
becoming increasingly popular and currently SSSD doesn’t provide any way to use
the latter. This diminishes the value provided by SSSD in some environments
like big companies and governments, where the usage of these authentication
mechanisms is becoming a common pattern.

SSSD should provide a way to authenticate users that use a passkey. This would
add more value by attracting the types of users mentioned in the previous
paragraph.

For the purpose of this feature, passkey is a FIDO2 compatible device supported
by the libfido2 library. If a hardware token implements other authentication
mechanisms aside from FIDO2, these aren't considered by this feature.

Use cases
---------
As a user, I want to sit in front of a system enrolled into a centralized
identity management solution and log in (desktop and/or terminal) using a
passkey device connected to the system.

Solution overview
------------------------
The objective is to use a passkey to locally authenticate a user against 
centralized identity management system. For that purpose an integration with an
LDAP server like AD or FreeIPA is needed.

First, the key is registered in the LDAP server. Then, the SSSD clients should
get the user credentials from this server, including the user key mapping data.
On top of that, SSSD should communicate with the key to get the information
stored in the device. Once this is done, SSSD should use all this data to
authenticate the user.

The biggest advantage of this approach is the usage of a central repository to
store the user's credentials. In the long term this gives more flexibility as
the users and keys can be authorized and revoked by the system administrator
easily.

Implementation details
----------------------

The implementation will loosely follow existing smartcard authentication in
SSSD. On top of that, and as mentioned before, the information will be stored
in two places: in the LDAP server and on the passkey. The server will contain
the public user credentials, including the user key mapping data, while the
passkey device will store the private key necessary to authenticate the user.

Key registration
****************
The first step is to register the user with a key. SSSD provides a helper
utility to handle the passkeys, and it can be used to create the key mapping
string (similar to pamu2fcfg). Instead of calling the helper utility from the
command line the system administrator uses 
`sssctl <https://docs.pagure.org/sssd.sssd/design_pages/sssctl.html>`__. This
enables to unify the user experience. If sssctl is run by an unprivileged user,
then additional udev rules might need to be configured. Please, check the
instructions from the key provider to know how to add them.

The output of this command can be set to the LDAP server in a dedicated
attribute. For AD we use the
`altSecurityIdentities <https://learn.microsoft.com/en-us/windows/win32/adschema/a-altsecurityidentities>`__
with a prefix (i.e. passkey). For FreeIPA we use a new attribute called
ipapasskey from the ipapasskeyuser objectclass. For any other LDAP server we
use the passkey attribute.

The format for server-side credentials for the key mapping is
``passkey:credentialId,pemPublicKey``.

The format for
`discoverable credentials <https://developers.yubico.com/WebAuthn/WebAuthn_Developer_Guide/Resident_Keys.html>`__ for the key mapping is
``passkey:credentialId,pemPublicKey,userId``.

IPA process
+++++++++++
FreeIPA provides a direct way to register the passkey attributes to the user
entry. As specified in FreeIPA's documentation this can be done with the
`ipa user-add-passkey` command or directly in the WebUI. This way FreeIPA can
take advantage of the SSSD and libfido2 integration to communicate with the
device in a single step.

AD (and any other LDAP server) process
++++++++++++++++++++++++++++++++++++++
The users, or the system administrator, calls sssctl. The user can manually
add this information to their AD object using AD's 'User and Computers'
utility, or any other attribute in case of another LDAP server.

LDAP attributes
***************
FreeIPA ID provider uses LDAP attribute ``ipaPassKey`` to retrieve the passkey
mapping data string as part of the user search in the backend. Store this in
the sysdb. The passkey mapping is obtained during the registration phase.
Example:

* ipapasskey: passkey:9S87qLk8/RxYJ3skwwYduomAM+/HDtz41N0+w/vRL6aGKJkLMsg+2OhO0E8pK5DuO1KmdK61K8PmH7jiYuOqbg==,9YE1s/f7J47h2A/DXCVFWulqoBXFzCSxcbGEBadkpSUFjwUudhPLnPUTv2qNamakXJgRYCZQ7vpS/t5zXMLnkw==

In the Active Directory case, the
`altSecurityIdentities <https://learn.microsoft.com/en-us/windows/win32/adschema/a-altsecurityidentities>`__
LDAP attribute is used to store the passkey mapping data. Example:

* altSecurityIdentities: passkey:9S87qLk8/RxYJ3skwwYduomAM+/HDtz41N0+w/vRL6aGKJkLMsg+2OhO0E8pK5DuO1KmdK61K8PmH7jiYuOqbg==,9YE1s/f7J47h2A/DXCVFWulqoBXFzCSxcbGEBadkpSUFjwUudhPLnPUTv2qNamakXJgRYCZQ7vpS/t5zXMLnkw==

Finally, IPA ``iparequireuserverification`` LDAP attribute is retrieved from
the IPA passkey configuration. Store this in the sysdb associated with  the IPA
domain. This attribute stores a string (on, off, default). Example:

* iparequireuserverification: on

User authentication with the key
********************************
The idea is to create a helper process similar to the p11_child. The helper
process receives the passkey’s user key mapping data as an argument alongside
other parameters (check
:ref:`Configuration options<configuration-options>` for more information).

This helper process heavily relies on the libfido2 library. The first steps
are to initialize the library and get the list of keys connected to the system.
Next the helper process loads the configuration parameters in the assert
structure, that comprises a collection of statements, each statement has a
mapping for a challenge, a credential, a signature, and ancillary attributes.
Finally, the helper process opens the key device and ask it for an
authentication according to the information provided in the
`assert <https://developers.yubico.com/libfido2/Manuals/fido_assert_new.html>`__
structure.

Call the passkey child in the PAM responder
+++++++++++++++++++++++++++++++++++++++++++
In ``pam_forwarder()`` check if passkey authentication is enabled (if
pam_passkey_auth boolean option is true and pam cmd == SSS_PAM_AUTHENTICATE).
If so, lookup the sysdb user object of the user logging in and read the sysdb
passkey mapping value. Parse out the key-handle and public-key strings from the
passkey mapping value. Read passkey related configuration options
(passkey_verification, passkey_child_timeout, debug_libfido2) and set up the
arguments (Domain, Key-handle and Public-key) for the passkey-child.

Execute the passkey_child passing the arguments listed above. The passkey PIN
is retrieved from the PAM conversation and written to the stdin of the
forked passkey child process(Similar to ``get_p11_child_write_buffer()``).
Check the passkey_child return code, return PAM_SUCCESS or failure based on the
result and call ``pam_reply()``. If the credential is discoverable, then the
passkey_child also prints the ``userId``, and the PAM responder has to
compare it with the one provided by the LDAP server. If they match, then it can
return PAM_SUCCESS.

Prompting implementation
************************
The prompting is handled by the PAM responder. For that purpose, the passkey
related authtokens is added in ``src/util/authtok.c``,
``sss_authtok_set_passkey_pin()`` and ``sss_authtok_get_passkey_pin()``.

In ``src/sss_client/pam_sss.c`` add a ``prompt_passkey()`` option which takes
the prompt as an argument to call ``do_pam_conversation()``. This sets the
type SSS_AUTHTOK_TYPE_PASSKEY_PIN.

In the PAM responder, ``pam_set_passkey_prompting_options()`` is added to
``src/responder/pam/pam_prompting_config.c`` to check and handle the PAM
prompting passkey configuration options.

``pc_list_add_passkey()`` copies the interactive prompt message to
``pc->data.passkey.prompt_inter`` and the touch prompt message to
``pc->data.passkey.prompt_touch`` and set type PC_TYPE_PASSKEY.

If interactive or touch options are set to false, then these values are set to
an empty string. If pam_sss reads an empty string for these prompts it does not
include them in the PAM conversation. This is done because we can't
fallback to a default prompt message in this situation, we need to skip the
interactive or touch prompt entirely.

Add the prompt message to the data buffer response back to pam_sss by adding
PC_TYPE_PASSKEY to case statements in ``pam_get_response_prompt_config()`` and
``pc_list_from_response()``. 

In ``prompt_passkey()``, 1 to 3 messages are provided to the PAM conversation
function. The first “Enter PIN:” PAM message is always created. If interactive
and/or touch prompts are enabled in the prompt configuration then those
messages are added to the pam message array and provided to the pam
conversation.

.. _configuration-options:

Configuration options
*********************
"pam_passkey_auth" enables the passkey device authentication.

"passkey_verification" is added to the SSSD configuration options. It is
similar to the “certificate_verification” option for the p11_child, as it
contains the parameters needed to tune the passkey_child helper
process. The list of parameters and their meaning:

* user_verification: if set to true, requires user verification (i.e. PIN,
  password) during authentication. If set to false, does not request user
  verification during authentication. The default is that the key itself
  decides what to do.

"passkey_child_timeout" sets the timeout for the PAM responder to wait for
passkey_child to finish.

"passkey_debug_libfido2" prints libfido2 library messages. It's under the
``[pam]`` section and it defaults to false.

Prompting Configuration
+++++++++++++++++++++++
Another section called [prompting/passkey] is added. This section is similar
to other prompting sections (i.e. 2fa). The list of options and their meaning:

* interactive: set to prompt a message and wait before testing the presence of
  a passkey device. Recommended if your device doesn’t have a tactile trigger.

* interactive_prompt=your prompt here: set individual prompt message for
  interactive mode. Default is: “Insert your Passkey device, then press ENTER.”

* touch: set to prompt a message to remind the user to touch the device.

* touch_prompt=your prompt here: set individual prompt message for the cue
  option. Default is: “Please touch the device."

An example prompt interaction can look like: ::

    Insert your Passkey device, then press ENTER.
    < ENTER >
    Enter PIN: 1234
    Please touch the device.

User verification
+++++++++++++++++
The user verification can be set in various places:

* In the IPA passkey configuration
* In the local sssd.conf

IPA passkey configuration user verification requirement overrides local
sssd.conf.

Registration process
--------------------

sssctl
******

Each passkey needs to be registered before it can be used for authentication.
This registration process is quite simple; the user connects the hardware
token to the computer, and then, executes the
``sssctl passkey-exec  --register`` command.

The command contains several parameters that slightly change its behaviour or
its output. The following is a list of the mandatory options:

* domain: LDAP domain name. Also know as
  `Relying Party <https://www.w3.org/TR/webauthn-2/#webauthn-relying-party>`__
  in the WebAuthn standard.

List of optional parameters:

* username: this is the username as registered in the LDAP server.

* type: public key cryptography. There are three possible types: es256, rs256
  and EdDSA. The default is es256.

* user-verification: requires user verification (i.e. PIN, fingerprint).

* cred-type: credential type (server-side or discoverable).

* debug-libfido2: flag to print libfido2 library messages.

The most basic example of a registration would be the following: ::

    # sssctl passkey-exec --register --username=USERNAME --domain=DOMAIN

This outputs the key mapping data (
``passkey:credentialId,pemPublicKey,userId``) that is used as the input for the
registration in the LDAP server. In AD and other LDAP servers the output is
copied to the LDAP attribute. In FreeIPA, the key mapping can copied to the
WebUI or to a command:
``ipa user-add-passkey USERNAME KEY_MAPPING``, or you can use the FreeIPA's
`user-add-passkey` command to do it in a single step.

FreeIPA
*******
FreeIPA has an additional more direct approach for the key registration. The
user connects the hardware token to the computer, and then, executes the
``ipa user-add-passkey USERNAME --register`` command on the machine where the
device is inserted. This takes care of registering the key and copying the
output to the corresponding LDAP attribute automatically.

Authors
-------
 * Iker Pedrosa <ipedrosa@redhat.com>
 * Justin Stephenson <jstephen@redhat.com>
 * Sumit Bose <sbose@redhat.com>
