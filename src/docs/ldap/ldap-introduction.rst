Introduction to LDAP Integration
################################

The LDAP Protocol is a well known cross platform protocol implemented in various LDAP server software components in small to enterprise level environments. SSSD on Linux clients is able to consume LDAP information with LDAP servers on Linux clients using the traditional SSSD LDAP provider. SSSD can use LDAP information for identity and authentication operations.

SSSD strives to work well with multiple RFC-conforming (*rfc2307bis*, *rfc2307*) LDAP server implementations such as 389-ds-base, OpenLDAP, Windows Active Directory, and several others. LDAP provider features include, not limited to

* SASL/SSL/TLS suport
* LDAP Service discovery
* Control search behavior with search base customization and nesting level
* Paging configurable options
* LDAP Access filters
* SUDO LDAP support
* Password policy support

.. note::

    Client side support for features is dependent on server side support.

To read more about how SSSD is used in LDAP integration at a high level, refer to the following links:

* `Understanding SSSD and its benefits <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel>`_


* `Configuring SSSD to use LDAP and require TLS authentication <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/configuring-sssd-to-use-ldap-and-require-tls-authentication_configuring-authentication-and-authorization-in-rhel>`_

Or on the terminal to read about SSSD's LDAP provider

.. code-block:: console

    $ man sssd-ldap