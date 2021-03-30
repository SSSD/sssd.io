Introduction to FreeIPA Integration
###################################

SSSD is a key client-side component of the FreeIPA (also known as Red Hat Identity Management in RHEL, or simply **IPA**) architecture. SSSD is running on both IPA servers and IPA clients and is used to

* Retrieve and cache data stored in IPA LDAP database, including

   * User and group identity information
   * Sudo rules
   * HBAC (Host-Based Access Rules)
   * SSH Keys
   * Automount maps
   * SELinux user maps
   * Netgroups

* Perform authentication with IPA services like IPA's embedded Kerberos server/KDC
* Allow IPA user authentication though ``pam_sss`` PAM module
* Automated Client Service discovery and failover
* Dynamic DNS Updates

To read more about how SSSD is used in FreeIPA integration at a high level, refer to the following links:

* `Understanding SSSD and its benefits <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel>`_


* `FreeIPA Client <https://www.freeipa.org/page/Client>`_

Or on the terminal to read about SSSD's IPA provider

.. code-block:: console

    $ man sssd-ipa

Active Directory integration through FreeIPA
--------------------------------------------

SSSD can also retrieve information and perform authentication against Active Directory Domain Controllers through IPA servers, this is done via IPA - AD Trust - also called *Indirect AD* integration. Red Hat documentation gives more information about how this works.

* `Planning a cross-forest trust between IdM and AD and Installing a trust between IdM and AD. <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/planning_identity_management/index?lb_target=production#planning-a-cross-forest-trust-between-idm-and-ad_planning-dns-and-host-names>`_

* `Integrating IdM and AD. <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/installing_identity_management/index?lb_target=production#installing-trust-between-idm-and-ad_installing-identity-management>`_