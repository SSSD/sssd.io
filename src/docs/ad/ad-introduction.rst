Introduction to Active Directory
################################

`Active Directory Domain Services`_ is Microsoft's product for enterprise
identity management. It contains multiple services such as LDAP (database),
Kerberos (authentication), Group Object Policies (access control and policy),
DNS and more. Even though it only has official support on Microsoft Windows,
SSSD provides seamless integration of Linux clients with Active Directory
through the ``ad`` provider, including automatic SID to uid/gid translation.

The following features are supported in SSSD Active Directory integration:

* Full support of Active Directory users and groups
* Kerberos authentication
* Access control via Group Policy Objects
* Auto-discovery of trusted domains (subdomains in SSSD terminology)
* Auto-discovery of Active Directory site and forest
* Automatic SID to uid and gid translation
* Dynamic DNS records updates
* No POSIX attributes are required on Active Directory objects
* ID views to support migration effort
* Automount maps and sudo rules support
* Support for offline authentication
* ... and more

.. _Active Directory Domain Services: https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview

.. seealso::

  * `Understanding SSSD and its benefits <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel>`_
  * `Why Use SSSD Instead of a Direct LDAP Configuration for Applications? <https://www.redhat.com/en/blog/why-use-sssd-instead-direct-ldap-configuration-applications>`_

.. note::

  There are multiple ways to join a host into an Active Directory domain. We
  recommend using ``realmd`` which provides automatic domain discovery and
  enrollment. It is also possible to perform required steps manually.

  * :doc:`ad-provider` (realmd)
  * :doc:`ad-provider-manual`

  If you want to avoid enrolling to the Active Directory domain explicitly, you
  may also use the ``ldap`` provider (:doc:`ad-ldap-provider`). This requires
  deeper understanding of SSSD configuration and does not provide all the
  features and benefits of the ``ad`` provider, therefore it is not generally
  recommended.

Integrating Active Directory through FreeIPA
********************************************

If you need to manage large numbers of both Windows and Linux machines, you may
want to consider using FreeIPA for Linux systems and establish a trust between
FreeIPA and Active Directory domains. This will keep all the benefits of direct
Active Directory integration but also grants you better control over the Linux
system through a Linux-specific identity management product. Visit
:doc:`../ipa/ipa-introduction` for more information.
