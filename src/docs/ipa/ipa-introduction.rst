Introduction to FreeIPA
#######################

`FreeIPA`_ is an open source product that combines multiple technologies and
protocols into a single complex identity management solution. It provides a much
richer experience when compared to native LDAP solutions including features such
as:

* Support for two factor and smartcard-based authentication
* Host-Based Access Control (HBAC)
* Host groups
* SELinux user maps
* Integrated DNS server
* Dynamic DNS updates
* Site locations
* ... and much more ...

.. note::

    SSSD is the main FreeIPA client therefore it provides the full experience
    and always supports every new feature at the same time when it becomes
    available on the server.

FreeIPA can be managed either through a command line interface with the ``ipa``
command or through rich web interface. You can try it right away using an online
`demo <https://www.freeipa.org/page/Demo>`__.

.. lightbox::

    images/ipa-introduction-1.png FreeIPA Web User Interface
    images/ipa-introduction-2.png FreeIPA Web User Interface
    images/ipa-introduction-3.png FreeIPA Web User Interface
    images/ipa-introduction-4.png FreeIPA Web User Interface

Active Directory Integration
****************************

One of the main FreeIPA features is its ability to seamlessly integrate with
`Active Directory`_. The integration is achieved through creating a trust with
existing Active Directory domains. Users and groups from trusted domains are
then available on FreeIPA enrolled hosts (which also means that Active Directory
users and log into the Linux host) and all policies and rules (such as HBAC or
sudo) are applied on them as well.

FreeIPA in combination with SSSD also provides additional functionality that
further enhance the integration with Active Directory such as:

* No POSIX attributes are required on Active Directory objects
* SIDs are automatically mapped to user and groups IDs within an ID Range
* POSIX attributes can be overwritten through ID Views
* ... and much more ...

.. seealso::

    The following documents provide more information on the Active Directory
    integration:

    * `Planning a cross-forest trust between IdM and AD <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/planning_identity_management/index?lb_target=production#planning-a-cross-forest-trust-between-idm-and-ad_planning-dns-and-host-names>`__
    * `Installing trust between IdM and AD <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/installing_identity_management/index?lb_target=production#installing-trust-between-idm-and-ad_installing-identity-management>`__

.. _FreeIPA: https://www.freeipa.org
.. _Active Directory: https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview
