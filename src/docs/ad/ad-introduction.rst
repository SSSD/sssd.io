Introduction to Active Directory Integration
############################################

Direct Active Directory integration
-----------------------------------

Heterogeneous IT environments often contain various domains and operating systems that need to be able to seamlessly communicate. SSSD offers integration with Active Directory on Linux clients by taking advantage of the SSSD AD provider. In addition to retrieving and caching user and group information from Active Directory, SSSD can:


* Perform automatic objectSID -> UID/GID Mapping, or use existing POSIX attributes
* Auto-discover trusted AD domains
* Utilize sudo rules stored in AD
* Enable linux systems to act as a GPO client
* Set customized access controls based on user/group membership, or GPO rules
* Dynamic DNS updates
* Offline support
* AD Site discovery
* Automatically renew linux host computer object

To read more about how SSSD is used in AD integration at a high level, refer to the following links:

* `Understanding SSSD and its benefits <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel>`_


* `Why Use SSSD Instead of a Direct LDAP Configuration for Applications?  <https://www.redhat.com/en/blog/why-use-sssd-instead-direct-ldap-configuration-applications>`_

Or on the terminal to read about SSSD's AD provider

.. code-block:: console

    $ man sssd-ad

Active Directory integration through FreeIPA
--------------------------------------------

SSSD can also retrieve information and perform authentication against Active Directory Domain Controllers through IPA servers, this is done via IPA - AD Trust - also called *Indirect AD* integration. Red Hat documentation gives more information about how this works.

* `Planning a cross-forest trust between IdM and AD and Installing a trust between IdM and AD. <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/planning_identity_management/index?lb_target=production#planning-a-cross-forest-trust-between-idm-and-ad_planning-dns-and-host-names>`_

* `Integrating IdM and AD. <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/installing_identity_management/index?lb_target=production#installing-trust-between-idm-and-ad_installing-identity-management>`_