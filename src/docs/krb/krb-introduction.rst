Introduction to Kerberos
########################

`Kerberos`_ is a computer-network authentication protocol. It is based on
symmetric-key cryptography and mutual authentication between client and server
(called Key Distribution Center; KDC) **without sending user's secrets over the
network**. It is commonly used to authenticate users, computers and services in
centralized identity management.

The authentication itself is done by exchanging encrypted messages that contains
encrypted tickets and encryption keys required to decrypt the tickets and
continue the protocol communication. To decrypt the message, one must posses
information (usually a password) that can be used to create the correct
encryption key.

A ticket-granting ticket (TGT) is obtained after a successful authentication and
stored in user's credential cache. This ticket can be used to authenticate the
user against other services without entering user's secrets again. Therefore the
user has to provide the authentication token only once to obtain the
ticket-granting ticket as long as the ticket is valid and not expired. This is
referred to as **single sign-on** (SSO).

.. _Kerberos: https://en.wikipedia.org/wiki/Kerberos_(protocol)

.. seealso::

    Kerberos is a standardized protocol described in `RFC4120
    <https://datatracker.ietf.org/doc/html/rfc4120>`__. Additional, there are
    many standardized extensions that extends the Kerberos protocol with a new
    functionality. For example:

    * `A Generalized Framework for Kerberos Pre-Authentication <https://datatracker.ietf.org/doc/html/rfc6113.html>`__
    * `One-Time Password Pre-Authentication (OTP) <https://datatracker.ietf.org/doc/html/rfc6560>`__
    * `Public-key cryptography for Initial Authentication in Kerberos (PKINIT) <https://datatracker.ietf.org/doc/html/rfc4556>`__

:doc:`FreeIPA <../ipa/ipa-introduction>` and :doc:`Active Directory
<../ad/ad-introduction>` requires Kerberos protocol for authentication. It can
be optionally used with plain :doc:`LDAP <../ldap/ldap-introduction>`. SSSD has
vast Kerberos support, including:

* Automatic ticket renewal
* Offline authentication
* Smartcard authentication
* Two-factor authentication
* FAST channel support
* ``.k5login`` based access control
* ... and more

.. note::

    There are two main open-source Kerberos implementations.

    * `MIT Kerberos <https://web.mit.edu/kerberos>`__
    * `Heimdal <https://github.com/heimdal/heimdal>`__


The Kerberos is fully integrated into identity management solutions
:doc:`FreeIPA <../ipa/ipa-introduction>` and :doc:`Active Directory
<../ad/ad-introduction>` and it is required for authentication. It can be
optionally used with plain :doc:`LDAP <../ldap/ldap-introduction>`. SSSD has
vast Kerberos support, including:

* Automatic ticket renewal
* Smartcard authentication
* Two-factor authentication
* FAST channel support
* ``.k5login`` based access control
* Offline authentication and automatic ticket acquirement upon transition to
  online state
* ... and more

.. seealso::

  * `Understanding SSSD and its benefits <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel>`__
  * `Using Kerberos <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system-level_authentication_guide/using_kerberos>`__
  * `Configuring the Kerberos KDC <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system-level_authentication_guide/configuring_a_kerberos_5_server>`__
