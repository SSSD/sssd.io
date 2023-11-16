Quick Start Guide
#################

This page provides brief instructions to configure SSSD with FreeIPA, AD, and LDAP.

Quick Start IPA
***************

Before starting, make sure you have the following information.

- Administrator credentials *e.g. admin*
- FreeIPA domain name *e.g. sssd.io*
- FreeIPA server hostname *e.g. ipa1.sssd.io*
- FreeIPA server IP *e.g. 1.2.3.4*

Install the necessary packages, for RHEL and clones the package is named ``ipa-client``, and for Fedora it’s ``freeipa-client``.

.. code-tabs::

    .. fedora-tab::

         dnf install -y freeipa-client

    .. rhel-tab::

        yum install -y ipa-client

Make sure DNS is pointing to your IPA server(s) by checking ``/etc/resolv.conf`` and it having it contain an entry with the IPA server IP, if it’s missing go ahead and add it, as the first entry.

.. code-block:: text
  :caption: /etc/resolv.conf

    search sssd.io
    nameserver 1.2.3.4
    nameserver 1.1.1.1

Now the ``ipa-client-install`` command will work. Run the command ``ipa-client-install`` and follow the prompts asking for your domain and server and then a user that can join the domain, which will be the administrator user.

.. code-block:: text

    ipa-client-install

After it’s finished, test to see if the users in IPA show up on the system, by running ``getent`` or ``id <IPA_USER>``

.. code-block:: text

    id admin

If you have auto mounts configured, run ``ipa-client-automount`` to enable that feature. Use the -U flag for unattended.

.. code-block:: text

    ipa-client-automount -U


Quick Start AD
**************

Before starting make sure you have the following information:

- Domain user credentials *e.g. Administrator*
- AD Domain name *e.g. sssd.io*
- AD Server IP *e.g. 1.2.3.4*
- AD Server hostname *e.g. ad1.sssd.io*

Install the necessary packages, for RHEL and clones the packages are ``sssd, adcli, realmd, oddjob`` and ``oddjob-mkhomedir``

.. code-tabs::

    .. fedora-tab::

        dnf install -y sssd adcli realmd oddjob oddjob-mkhomedir

    .. rhel-tab::

        yum install -y sssd adcli realmd oddjob oddjob-mkhomedir

Make sure DNS is pointing to your AD server(s) by checking ``/etc/resolv.conf`` and it having it contain an entry with an AD server IP, if it’s missing go ahead and add it, as the first entry.

.. code-block:: text

    search sssd.io
    nameserver 1.2.3.4
    nameserver 1.1.1.1

Now you can issue the ``realm join`` command with the domain name in order to join the domain.

.. code-block:: text

    realm join sssd.io

It will default and use the *Administrator* user, add the -u flag to specify a different user account to join the domain.

.. code-block:: text

    realm join -u jsmith sssd.io

Now see if it works, and issue an id command.

.. code-block:: text

    id administrator@sssd.io

If you want to use short names, edit ``sssd.conf`` and set ``use_fully_qualified_names`` to ``false``.

.. note::

    In the event of user name conflict, jsmith@sssd.io, jsmith@child.sssd.io for example, you can configure a domain resolution order using shortnames. :doc:`short names <../design-pages/shortnames>`. If that does not work, checkout ``sss_overide`` which is part of the ``sssd_tools`` package to create a local override. Of course it's best to resolve the conflict.

.. code-block:: text

    id administrator

The following command and logins should now work. For more detail please refer to :doc:ad/ad-provider .

Quick Start LDAP
****************

Before starting make sure you have the following information:

- LDAP domain *e.g. sssd.io*
- LDAP suffix *e.g. DC=sssd,DC=io*
- LDAP bind user *e.g. UID=bind_user,OU=people,DC=sssd,DC=io*
- LDAP bind password *e.g. password123*
- LDAP server hostname *e.g. ldap1.sssd.io*
- LDAP server IP *e.g. 1.2.3.4*
- LDAP server CA certificate *e.g. /etc/openldap/cacerts/ca.crt*

.. note::

    The bind user and the bind password are only necessary if the LDAP server you are connecting does not permit anonymous binds.

First install the necessary package, sssd.

.. code-tabs::

    .. fedora-tab::

        dnf install -y sssd

    .. rhel-tab::

        yum install -y sssd

Edit ``/etc/sssd/sssd.conf`` and add a new domain section. The section should look like the following without a bind user. Unlike the other providers, ``sssd.conf`` needs to be edited manually.

.. code-block:: ini
   :caption: /etc/sssd/sssd.conf

    [sssd]
    domains = LDAP_DOMAIN

    [domain/LDAP_DOMAIN]
    id_provider = ldap
    auth_provider = ldap

    ldap_uri = ldap://ldap1.sssd.io
    ldap_search_base = DC=sssd,DC=io

    ldap_id_use_start_tls = true
    ldap_tls_reqcert = demand
    ldap_tls_cacert = /etc/openldap/cacerts/ca.crt

.. note::

    CA certificates are usually kept in ``/etc/openldap/cacert``, and ``start_tls`` or ``ldaps`` should be used, **DO NOT** use both at the same time.

If anonymous queries are not enabled on the server, the following section is required for the bind account.

.. code-block:: text

    ldap_default_bind_dn = uid=bind_user,ou=people,dc=sssd,dc=io
    ldap_default_authtok_type = password
    ldap_default_authtok = password123

In RHEL8 and clones you should use ``authselect`` to configure the rest of the configuration, on older versions like RHEL7 use ``authconfig``.

.. code-tabs::

    .. fedora-tab::

        authselect select sssd

    .. rhel-tab::
        :version: 8+

        authselect select sssd

    .. rhel-tab::
        :version: 7

        authconfig --enablesssd --update


Now restart SSSD and test looking up a user.

.. code-block:: text

   service sssd start
   id jsmith
