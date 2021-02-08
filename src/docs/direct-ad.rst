Direct AD Integration
#####################

This page describes how to configure SSSD to authenticate with a Windows 2008 or later Domain Server using the Active Directory provider (``id_provider=ad``). The AD provider was introduced with SSSD 1.9.0. Follow :doc:`manual-ad` to join AD manually without realmd.

Joining the GNU/Linux client using realmd (Recommended)
*******************************************************

The realmd (Realm Discovery) project is a system service that manages discovery and enrolment to several centralized domains including AD or IPA. realmd is included in several popular GNU/Linux distributions including:

* Red Hat Enterprise Linux 7.0 and later
* Fedora 19 and later
* Ubuntu 13.04 and later
* Debian 8.0 and later

Run ``realm discover`` to see what domains realmd can find. Note that this functionality relies on NetworkManager being up and running in order to read the DHCP domain:

.. code-block:: bash

    realm discover
    realm discover AD.EXAMPLE.COM

Finally, joining the Active Directory domain is as easy as:

.. code-block:: bash

    realm join AD.EXAMPLE.COM

You will be prompted for Administrator password. However, realmd supports more enrolment options, including using a one-time password or selecting a custom OU. Refer to the `realmd documentation <https://www.freedesktop.org/software/realmd/docs/>`_ for more details.

Note that the ``realm permit`` command configures the simple access provider.

Additional reading
******************

The following sections are optional reading, it contains information which may be useful to administrators using SSSD with the AD Provider.

Testing with a clean cache
==========================

You may have made iterative changes to your setup while learning about SSSD. To make sure that your setup actually works, and you're not relying on cached credentials, or cached LDAP information, you may want to clear out the local cache. Obviously this will erase local credentials, and all cached user information, so you should only do this for testing, and while on the network with network access to the AD servers:

.. code-block:: bash

    sssctl cache-remove
    getent passwd administrator@ad.example.com

If all looks well on your system after this, you know that sssd is able to use the kerberos and ldap services you've configured.

Configuring Active Directory to use POSIX attributes
====================================================

The Active Directory provider is able to either map the Windows Security Identifiers (SIDs) into POSIX IDs or use the POSIX IDs that are set on the AD server. By default, the AD provider uses the automatic ID mapping method. In order to use the POSIX IDs, you need to set up `Identity Management for UNIX <https://technet.microsoft.com/en-us/library/cc731178.aspx>`_. Note that starting with Windows Server 2016, the `Identity Management for UNIX UI is deprecated <https://blogs.technet.microsoft.com/activedirectoryua/2016/02/09/identity-management-for-unix-idmu-is-deprecated-in-windows-server/>`_. However, it is still possible to set the POSIX attributes. For managing POSIX attributes in environments with IPA-AD trusts (Indirect AD integration) deployed, the `ID views <https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Linux_Domain_Identity_Authentication_and_Policy_Guide/id-views.html>`_ feature of IDM might also be interesting.

When working with multiple trusted domains, SSSD often reads the data from the Global Catalog first. However, POSIX attributes such as UIDs or GIDs are not replicated to the Global Catalog by default. For performance reasons, it might be a good idea to set them to be replicated manually. This recommendation applies to setups that do not use automatic ID mapping and use ``ldap_id_mapping=False`` instead.

* Install the Identity Management for UNIX Components

  * Follow this `technet article <https://technet.microsoft.com/en-us/library/cc731178.aspx>`_ to install Identity Management for UNIX on primary and child domains controllers
  * After the installation has finished, you'll be able to assign POSIX UID, GID and other attributes using a tab called UNIX Attributes in the Properties menu
* Add Schema Snap-in

  * To enable new attributes to replicate to the GC we need an Active Directory Schema snap-in. Use `these steps <https://serverfault.com/questions/609592/where-is-active-directory-snap-in-for-server-2012-r2>`_ to install the Schema Snap-In if you are having trouble.
* Modify Attributes for replication

  * The `article <https://docs.microsoft.com/en-us/windows/win32/ad/attributes-included-in-the-global-catalog>`_ explains how to select any attribute for replication
  * In our case, select ``uidNumber``, ``gidNumber``, ``unixHomeDirectory`` and ``loginShell``
* Verifying Attributes replication to Global Catalog

  * In general, search for a user entry that has the POSIX attributes set on port 3268 of a Domain Controller
  * You can use the Windows ``LDP`` tool or after the GNU/Linux machine is joined, simply ``ldapsearch``

DNS validation
==============

It is recommended that the GNU/Linux client you are enrolling is able to resolve the SRV records the Active directory publishes. In order to do so, the clients would typically point at the AD DCs in ``/etc/resolv.conf``. You can verify this using dig:

.. code-block:: bash

    dig -t SRV _ldap._tcp.ad.example.com @server.ad.example.com

Unreachable AD servers/domains
==============================

If any DNS-advertised (see dig command above) AD servers are unreachable (usually for firewall reasons), you need to list the reachable servers using the ``ad_server`` configuration option. The same is true for AD domains, SSSD auto-discovers all domains in the forest by default, so if any of the DCs in other domains are not reachable, either exclude that domain with ``ad_enabled_domains`` or, if only some DCs from that trusted domain are reachable, define a per-subdomain section in the config file (see below for an example).

Fully qualified names
=====================
The AD provider sets the option ``use_fully_qualified_names`` to false, manually setting this option to ``true`` forces all lookups to contain the domain name as well, either the full domain name as specified in sssd.conf (``getent passwd administrator@ad.example.com``) or the short NetBIOS name (``getent passwd AD\\Administrator``). This restriction helps separate users from different domains, especially in setups with multiple domains in a trusted environment, or in cases where local UNIX users might have the same user names as AD users.

Access control options
======================

There is a number of access control options available to a directly-enrolled AD client machine.

+----------------+---------------------------+-------------------------------------------------------+-------------------------------------------------------------------------------+
| access provider| simple                    | ad                                                    | ad_access_filter                                                              |
+================+===========================+=======================================================+===============================================================================+
| Pros           | Very simple,              | Supports fully centralized environments by using GPOs | Very expressive,                                                              |
|                | supports nested groups    |                                                       | can be used to allow/deny based on any properties of the LDAP user object.    |
+----------------+---------------------------+-------------------------------------------------------+-------------------------------------------------------------------------------+
| Cons           | Only supports allow/deny  | Not supported with older releases,                    | Cumbersome to write                                                           |
|                | user or group             | may not be desirable in a mixed GNU/Linux and         |                                                                               |
|                |                           | Windows environment                                   |                                                                               |
+----------------+---------------------------+-------------------------------------------------------+-------------------------------------------------------------------------------+

It is also possible to use completely external means of access control, such as ``pam_access.so``. Those might be useful when supporting legacy stack alongside SSSD or when defining access control by means SSSD doesn't support (such as per netgroup).

Other documentation
===================

Red Hat maintains a very in-depth `guide about SSSD and Windows integration <https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Windows_Integration_Guide/index.html>`_. Some of the commands such as setting up the PAM stack or installing packages are specific to RHEL, CentOS or Fedora, but the general information are useful for all distributions.

See the `following article on Technet site <http://technet.microsoft.com/en-us/library/cc772815%28WS.10%29.aspx>`_ for more in-depth Kerberos understanding

If there is a specific document for your distribution or environment, such as the RHEL guide below, please let us know so that we can include it\!
