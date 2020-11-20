Require Smartcard authentication (for local users)
==================================================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/3650

Problem statement
-----------------
By default SSSD tries to determine what authentication methods are available
for a user and prompts accordingly. This is primarily done by figuring out the
supported authentication methods on the server. E.g. the ``krb5`` provider will
use the available pre-authentication methods to determine how the user can
authenticate. If a user should only and always use Smartcard authentication the
long term password can be removed on the server side so that the user can only
user PKINIT for authentication. For FreeIPA domains there are `authentication
indicators`_ to requires specific authentication methods for services.

.. _authentication indicators: https://www.freeipa.org/page/V4/Authentication_Indicators

Currently SSSD does not handle the general authentication of local user because
this is still done by ``pam_unix``. However SSSD offers the support for
Smartcard authentication for local user. To be flexible and offer the user the
most suitable prompting during authentication SSSD currently only prompt for a
Smartcard PIN if a Smartcard is inserted with certificates which can mapped to
the user trying to log in. This means that local users cannot easily be forced
to use Smartcard authentication where the user is prompted to insert a
Smartcard and SSSD waits until a suitable card is inserted.

Use cases
---------
Local users
^^^^^^^^^^^
Force local users to use Smartcard authentication

Active Directory
^^^^^^^^^^^^^^^^
Although Active Directory offers the 'Smart card is required for interactive
logon' option it might not be suitable for all use cases because it disables
password based authentication which might still be needed for certain services.
Having an option on the client to require Smartcard authentication for specific
services would help here as well.

Overview of the solution
------------------------
There are two places where an option to enforce Smartcard authentication can be
set, the SSSD configuration file ``sssd.conf`` or the option list of the
``pam_sss`` PAM module.

In general we try to avoid adding options to the PAM module to keep the PAM
module as dumb and simple as possible and do all processing in SSSD's PAM
responder and the backends. But in the given case options for the PAM module
offer greater flexibility with a less complex configuration. To keep the
``pam_sss`` PAM module still simple, it will forward the provided option to
SSSD and check the reply if Smartcard authentication is possible or return an
error.

Besides and option to require Smartcard authentication and option to only check
if Smartcard authentication is available will be added as well to allow more
flexible PAM configurations.

Implementation details
----------------------
``p11_child``
^^^^^^^^^^^^^
``p11_child`` needs a new option to wait until a card is available if no
suitable card is available. Since the PAM responder will kill ``p11_child`` if
a timeout expires an option is needed to let the PAM responder wait longer to
allow the child to wait longer.

If a slot with with the ``CKF_REMOVABLE_DEVICE`` flag was found ``p11_child``
can check if the PKCS#11 call ``C_WaitForSlotEvent`` is implemented and use it.
If the PKCS#11 does not implement this call ``p11_child`` can call
``C_GetSlotInfo`` in regular interval until a token is present or it is kill by
the PAM responder. NSS provides the ``PK11_WaitForTokenEvent`` call to handle
this.

If there is no slot with the ``CKF_REMOVABLE_DEVICE`` flag set ``p11_child``
has to run ``C_Finalize``-``C_Initialize`` cycles to be able to discover new
slots. This is e.g. needed for Yubikey USB devices which are from the PKCS#11
perspective Smartcard (tokens) and reader (slot) in a single device.

``pam_sss``
^^^^^^^^^^^
The PAM module ``pam_sss`` will get two new flag options:

``try_cert_auth``
                        Try to use certificate based authentication, i.e.
                        authentication with a Smartcard or similar devices. If a
                        Smartcard is available and the service is allowed for
                        Smartcard authentication the use will be prompted for a
                        PIN and the certificate based authentication will
                        continue.

                        If no Smartcard is available or certificate based
                        authentication is not allowed for the current service
                        ``PAM_AUTHINFO_UNAVAIL`` is returned.

``require_cert_auth``
                        Wait until a Smartcard suitable for authentication is
                        available and ask the user to insert a Smartcard.

                        If no Smartcard is available or certificate based
                        authentication is not allowed for the current service
                        ``PAM_AUTHINFO_UNAVAIL`` is returned.

The PAM module will forward the flags to the PAM responder in a 32bit integer
which will handled the request accordingly. If the reply of the PAM responder
does not contain the needed information to prompt the user for a Smartcard PIN
the PAM module will return ``PAM_AUTHINFO_UNAVAIL``.

PAM responder
^^^^^^^^^^^^^
The PAM responder will get a new option to increase the waiting time for
``p11_child`` if the ``require_cert_auth`` flag was received from the client.
To receive the flags the PAM responder must be prepared to handle to 32bit
integer send by the client containing the flags. 

Configuration changes
---------------------
``p11_child``
^^^^^^^^^^^^^
``p11_child`` is mentioned here for completeness, since it is an internal helper this change is not directly relevant for users.

New option:

``--wait_for_card``
      Wait until a Smartcard (token) is available in a reader (slot)

``pam_sss``
^^^^^^^^^^^
New options:

``try_cert_auth``
      see above

``require_cert_auth``
      see above

PAM responder:
^^^^^^^^^^^^^^
New option:

``p11_wait_for_card_timeout``
     If Smartcard authentication is required how many                                         
     extra seconds in addition to p11_child_timeout                                           
     should the PAM responder wait until a Smartcard is                                       
     inserted.                                                                                

     Default: 60 (seconds)
 

How to test
-----------
To test the feature the PAM configuration had to be modified and ``pam_sss`` has to be added with the ``require_cert_auth`` or ``try_cert_auth`` option at a suitable place.

Allow Smartcard authentication for local users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To allow Smartcard authentication for local user but use password authentication as a fallback if no Smartcard is available the following snippet might be added to the PAM configuration::

    ....
    auth        [default=2 success=ok] pam_localuser.so
    auth        sufficient    pam_sss.so try_cert_auth
    auth        [success=done ignore=ignore default=die] pam_unix.so try_first_pass
    ....

Require Smartcard authentication for local users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To require Smartcard authentication for local user the following snippet might be added to the PAM configuration::

    ....
    auth        [default=2 success=ok] pam_localuser.so
    auth        required    pam_sss.so require_cert_auth
    auth        required    pam_deny.so
    ....

Authors
-------
 * Sumit Bose ``<sbose@redhat.com>``
