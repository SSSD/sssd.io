Introduction to Kerberos Integration
####################################

The Kerberos Protocol is a commonly used network authentication protocol to secure logins and communication between linux services. SSSD on Linux clients can be configured to authenticate against Kerberos servers (or *KDCs*), allowing kerberos communication to be handled by SSSD and providing Kerberos tickets to the user or service at login.

SSSD is often used as a client to communicate with Red Hat MIT Kerberos KDC, :doc:`FreeIPA <../ipa/ipa-introduction>` or the built-in Windows Active Directory KDC. Features of the SSSD *KRB5* provider include* 

* Automatic renewal of tickets
* Ticket lifetime configurable options
* FAST support
* Map User
* Backup KDC server support

.. note::

    Client side support for features is dependent on Kerberos server side support.

To read more about how SSSD is used in Kerberos integration at a high level, refer to the following links:

* `Understanding SSSD and its benefits <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel>`_


* `Using Kerberos <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system-level_authentication_guide/using_kerberos>`_

Or on the terminal to read about SSSD's Kerberos provider

.. code-block:: console

    $ man sssd-krb5

Setting up a Red Hat Kerberos Server has its own documentation:

* `Configuring the Kerberos KDC <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system-level_authentication_guide/configuring_a_kerberos_5_server>`_
