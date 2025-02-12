Passwordless-GDM authentication integration
=======================================================

Related ticket(s):
------------------
 * https://github.com/SSSD/sssd/issues/7069

Problem statement
-----------------
Passwordless authentication is becoming increasingly popular. SSSD and FreeIPA
already provide several authentication mechanisms which make use of it:
`Smart Cards <https://sssd.io/design-pages/smartcards.html>`__,
`External Identity Providers
<https://freeipa.readthedocs.io/en/latest/designs/external-idp/external-idp.html>`__
(EIdP) and `Passkeys <https://sssd.io/design-pages/passkey_kerberos.html>`__.
Unfortunately, the integration of these mechanisms into the graphical interface
leaves much to be desired. Some of them may work in a degraded mode, while
others can’t be used at all.

SSSD and the GUI should be better integrated to make all these authentication
mechanisms effortless for the user. This would increase the overall security of
the system, by providing the benefits of these authentication mechanisms, i.e.
passwordless, MFA, etc.

SSSD and `GDM <https://wiki.gnome.org/Projects/GDM>`__ are working together to
provide a set of interfaces that can be used to enable these authentication
mechanisms in Linux’s GUI. While the initial work targets SSSD-GDM integration,
the objective is that these interfaces can be used by any other desktop
environment.

Use cases
---------
* As a centrally managed user, I want to choose the authentication mechanism
  to login from the graphical interface so that I can select the one that best
  suits my needs.

* As a centrally managed user, I want to use an external identity provider
  (IdP) to login from the graphical interface so that the user interface is
  easy to use and consistent across all authentication mechanisms in the
  distribution.

* As a centrally managed user, I want to select the smart card identity to
  login from the graphical interface so that the authentication is performed
  with the correct credentials.

* As a centrally managed user, I want to use a passkey to login from the
  graphical interface so that the user interface is easy to use and consistent
  across all authentication mechanisms in the distribution.

* As a centrally managed user, I want to get notified when the passkey
  authentication has been performed locally so that I am aware that the user
  experience might be affected.

Solution overview
-----------------
The objective is to provide usable workflows for users to authenticate in the
graphical interface using passwordless authentication mechanisms. To do this,
we first need to design a communication protocol between SSSD and GDM.

The APIs can be implemented in two ways, either by implementing them in
`D-BUS <https://www.freedesktop.org/wiki/Software/dbus/>`__, or by extending
the PAM conversation to include the new authentication mechanisms. There
doesn’t seem to be any advantage in using D-BUS, whereas a PAM-level API would
give other desktop environments the ability to offer similar features. For this
reason, the GDM PAM extension has been selected.

GDM already provides an interface in ``/usr/include/gdm/gdm-pam-extensions.h``
that SSSD supports. Unfortunately extending this binary interface is hard, so
a JSON based protocol is used. It’s easier to extend and manage, making it
easier to adapt the different packages involved. The previous implementation
will continue to be maintained for backward compatibility.

As for the workflows, they have to provide the user with a way to interact
(i.e. insert the hardware token or enter the PIN), while allowing communication
with the device or the external provider. Each authentication mechanism needs
its own sequence diagram definition, which will be explained later in this
document.

Implementation details
----------------------

Sequence diagram
****************
The communication between SSSD and GDM is explained in the following sequence
diagram.

.. uml:: ../diagrams/passwordless-gdm-auth.pu

* GDM prompts the user for their username.

* The user initiates the login procedure by entering their username.

* GDM starts the PAM conversation.

* GDM starts the authentication process in SSSD.

* pam_sss communicates with the PAM responder to resolve the user.

* PAM responder resolves the username and obtains, among other things, the
  available authentication methods and the prompting strings.

* PAM responder prepares the JSON message with the available authentication
  mechanisms, the prompts and the user credentials to be requested
  (check format in :ref:`data`).

* PAM responder returns this information to pam_sss.

* pam_sss wraps the JSON message in the PAM conversation using the macros
  provided by GDM in ``/usr/include/gdm/gdm-custom-json-pam-extension.h``.

* GDM prompts the user for the user credentials, and at the bottom of the
  screen it shows the available authentication mechanisms. If the user selects
  another method, GDM already has all the information needed to request the
  user credentials for this authentication mechanism.
 
* The authentication workflow continues, but varies depending on the selected
  authentication mechanism. This will be explained separately for each
  mechanism.

.. _data:

Data
****
In addition, the messages exchanged follow the JSON standard. SSSD provides the
available authentication mechanisms in the following message:

..  code-block:: json

    {
      "auth-selection": {
        "mechanisms": {
          "$mech1": {
            "name": "$name1",
            "role": "$role1",
            "selectable": true,
            "msg1": "$msg1"
          },
          "$mech2": {
            "name": "$name2",
            "role": "$role2",
            "selectable": true,
            "msg1": "$msg2",
            "msg2": "$msg3"
          }
        },
        "priority": [
          "$role2",
          "$role1"
        ]
      }
    }

The field meaning is as follows:

* name: the mechanism name that will be shown in the login screen.
* role: the authentication mechanism. It can be password, EIdP, smartcard or
  passkey.
* selectable: whether the authentication mechanism should be shown up in the
  login screen as an explicitly selectable option. By default it is set to
  ``true``.

GDM answers with the result for the previous JSON message processing:

..  code-block:: json

    {
      "auth-selection": {
        "status": "$status",
        "mech": {
          "data1": "$data1",
          "data2": "$data2"
        }
      }
    }

For clarification, there are two different types of user interaction messages:
`prompt` and `instruction`. The first one asks the user to enter something on
the screen, e.g. the PIN. The second type prompts the user to follow
instructions, e.g. to enter the PIN into the reader.

The JSON request and reply messages for different authentication mechanisms are
defined in the next sections.

Password
++++++++
SSSD provides the available authentication mechanisms:

..  code-block:: json

    {
      "auth-selection": {
        "mechanisms": {
          "password": {
            "name": "Password",
            "role": "password",
            "selectable": true,
            "prompt": "Password:"
          }
        },
        "priority": [
          "password"
        ]
      }
    }

GDM replies with the selection:

..  code-block:: json

    {
      "auth-selection": {
        "status": "Ok",
        "password": {
          "password": "ThePassword"
        }
      }
    }

EIdP
++++
SSSD provides the available authentication mechanisms:

..  code-block:: json

    {
      "auth-selection": {
        "mechanisms": {
          "eidp": {
            "name": "Web Login",
            "role": "eidp",
            "selectable": true,
            "init_prompt": "Login",
            "link_prompt": "Log in online with another device",
            "uri": "https://short.url.com/1234",
            "code": "1234",
            "timeout": 300
          }
        },
        "priority": [
          "eidp"
        ]
      }
    }

GDM replies with the selection:

..  code-block:: json

    {
      "auth-selection": {
        "status": "Ok",
        "eidp": {}
      }
    }

Smart card
++++++++++
SSSD provides the available authentication mechanisms:

..  code-block:: json

    {
      "auth-selection": {
        "mechanisms": {
          "smartcard:1": {
            "name": "sc1",
            "role": "smartcard",
            "selectable": true,
            "init_instruction": "Insert smartcard",
            "cert_instruction": "Certificate for PIV Authentication\nCN=sc1,O=GDM.TEST",
            "pin_prompt": "PIN",
            "module_name": "/usr/lib64/pkcs11/opensc-pkcs11.so",
            "key_id": "01",
            "label": "Certificate for PIV Authentication"
          },
          "smartcard:2": {
            "name": "sc2",
            "role": "smartcard",
            "selectable": true,
            "init_instruction": "Insert smartcard",
            "cert_instruction": "Certificate for PIV Authentication\nCN=sc2,O=GDM.TEST",
            "pin_instruction": "Enter PIN in reader",
            "module_name": "/usr/lib64/pkcs11/opensc-pkcs11.so",
            "key_id": "02",
            "label": "Certificate for PIV Authentication"
          }
        },
        "priority": [
          "smartcard:1",
          "smartcard:2"
        ]
      }
    }

**Note**: name field might have multiple lines.

GDM replies with the selection:

..  code-block:: json

    {
      "auth-selection": {
        "status": "Ok",
        "smartcard:1": {
          "pin": "ThePIN",
          "name": "sc1",
          "module_name": "/usr/lib64/pkcs11/opensc-pkcs11.so",
          "key_id": "01",
          "label": "Certificate for PIV Authentication"
        }
      }
    }

Passkey
+++++++
SSSD provides the available authentication mechanisms:

..  code-block:: json

    {
      "auth-selection": {
        "mechanisms": {
          "passkey": {
            "name": "passkey",
            "role": "passkey",
            "selectable": true,
            "init_instruction": "Insert security key",
            "pin_request": true,
            "pin_attempts": 8,
            "pin_prompt": "Security key PIN",
            "touch_instruction": "Touch security key",
            "kerberos": true,
            "crypto_challenge": "6uDMvRKj3W5xJV3HaQjZrtXMNmUUAjRGklFG2MIhN5s="
          }
        },
        "priority": [
          "passkey"
        ]
      }
    }

GDM replies with the selection:

..  code-block:: json

    {
      "auth-selection": {
        "status": "Ok",
        "passkey": {
          "pin": "ThePIN",
          "kerberos": true,
          "crypto_challenge": "6uDMvRKj3W5xJV3HaQjZrtXMNmUUAjRGklFG2MIhN5s="
        }
      }
    }

All authentication mechanisms
+++++++++++++++++++++++++++++
SSSD provides the available authentication mechanisms:

..  code-block:: json

    {
      "auth-selection": {
        "mechanisms": {
          "password": {
            "name": "Password",
            "role": "password",
            "selectable": true,
            "prompt": "Password:"
          },
          "eidp": {
            "name": "Web Login",
            "role": "eidp",
            "selectable": true,
            "init_prompt": "Login",
            "link_prompt": "Login online with another device",
            "uri": "https://short.url.com/tmp",
            "code": "1234"
          },
          "smartcard:1": {
            "name": "sc1",
            "role": "smartcard",
            "selectable": true,
            "init_instruction": "Insert smartcard",
            "cert_instruction": "Certificate for PIV Authentication\nCN=sc1,O=GDM.TEST",
            "pin_prompt": "PIN",
            "module_name": "/usr/lib64/pkcs11/opensc-pkcs11.so",
            "key_id": "01",
            "label": "Certificate for PIV Authentication"
          },
          "passkey": {
            "name": "passkey",
            "role": "passkey",
            "selectable": true,
            "init_instruction": "Insert security key",
            "pin_request": true,
            "pin_attempts": 8,
            "pin_prompt": "Security key PIN",
            "touch_instruction": "Touch security key",
            "kerberos": true,
            "crypto_challenge": "6uDMvRKj3W5xJV3HaQjZrtXMNmUUAjRGklFG2MIhN5s="
          }
        },
        "priority": [
          "passkey",
          "eidp",
          "smartcard:1",
          "password"
        ]
      }
    }

GDM replies with the selection, as explained in the preceding sections.

Authentication mechanisms priority
**********************************

The priority for the authentication mechanisms set in the JSON message is a
hardcoded value. This priority is only used the first time the user tries to
login as there are no saved methods. Once the user authenticates with a method
GDM will remember it and the next time the same user tries to login this method
will be provided. The priority is as follows:

* Passkey
* EIdP
* Smartcard
* Password

Configuration options
*********************

PAM responder options
+++++++++++++++++++++

PAM responder provides the new ``pam_json_services`` option to enable the
aforementioned authentication method selection mechanism. This is a list of all
PAM service files allowed to use it. Application maintainers can use it to let
SSSD know they support the json protocol, and that SSSD should provide the
available authentication methods using it.

Authors
-------
 * Iker Pedrosa <ipedrosa@redhat.com>
 * Ray Strode <halfline@redhat.com>
