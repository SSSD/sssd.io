LDAP provider with AD domain
############################

This describes how to configure SSSD to setup an Active Directory domain using
``id_provider = ldap``.

.. note::

    The recommended way to join into an Active Directory domain is to use the
    integrated AD provider (``id_provider = ad``). See :doc:`ad-provider` for
    more information.

    The only reason to use the ``ldap`` provider is if you do not want to
    explicitly join the client into the Active Directory domain (you do not want
    to have the computer account created etc.).

Prerequisites
*************

This document uses the following setup as an example:

.. table::
    :align: left
    :widths: 1, 3
    :width: 100%

    =========================== =========================
    Domain name                 ``ad.example.com``
    Kerberos realm              ``AD.EXAMPLE.COM``
    Active Directory server DNS ``dc.ad.example.com``
    Client DNS                  ``client.ad.example.com``
    =========================== =========================

Enabling LDAP Searches
**********************

SSSD must be configured to bind with SASL/GSSAPI or DN/password in order to
allow SSSD to do LDAP searches for user information against AD. GSSAPI is
recommended for security reasons. However, using GSSAPI probably mean that the
computer is already joined into the domain thus it probably makes sense to use
the AD provider instead.

Using SASL/GSSAPI Binds for LDAP Searches
=========================================

Create the service keytab for the host running SSSD on AD. Either do
this with Samba or using Windows. Samba is recommended.

Creating Service Keytab with Samba
----------------------------------

The service keytab can be created from the client computer using Samba tools.

#.  Configure Kerberos and Samba

    .. code-tabs::

        .. code-tab:: ini
            :label: /etc/krb5.conf

            [logging]
            default = FILE:/var/log/krb5libs.log

            [libdefaults]
            default_realm = AD.EXAMPLE.COM
            dns_lookup_realm = true
            dns_lookup_kdc = true
            ticket_lifetime = 24h
            renew_lifetime = 7d
            rdns = false
            forwardable = yes

            # You may also want either of:
            # allow_weak_crypto = true
            # default_tkt_enctypes = arcfour-hmac

            [realms]
            # Define only if DNS lookups are not working
            # AD.EXAMPLE.COM = {
            #  kdc = server.ad.example.com
            #  admin_server = server.ad.example.com
            # }

            [domain_realm]
            # Define only if DNS lookups are not working
            # .ad.example.com = AD.EXAMPLE.COM
            # ad.example.com = AD.EXAMPLE.COM

        .. code-tab:: ini
            :label: /etc/samba/smb.conf

            [global]
            workgroup = EXAMPLE
            client signing = yes
            client use spnego = yes
            kerberos method = secrets and keytab
            log file = /var/log/samba/%m.log
            password server = AD.EXAMPLE.COM
            realm = EXAMPLE.COM
            security = ads

#.  Join the machine to the realm

    .. code-block:: bash

        net ads join -U Administrator

#.  Additional principals can be created later with ``net ads keytab add`` if needed
#.  Check that the keytab works correctly

    .. code-block:: console

        # klist -ke
        # kinit -k CLIENT$@AD.EXAMPLE.COM

.. note::

    You don't need a Domain Administrator account to do this, you just need an
    account with sufficient rights to join a machine to the domain. This is a
    notable advantage of this approach over generating the keytab directly on
    the AD controller. If you're using NFS you may want to specify a different
    ``createupn`` argument here. This does not cause any problems for SSSD. For
    example:

    .. code-block:: bash

        net ads join createupn="nfs/client.ad.example.com@AD.EXAMPLE.COM" -U Administrator

Creating Service Keytab on AD
-----------------------------

.. warning::

    Do not do this step if you've already created a keytab using Samba.

On the Windows server:

#.  Open ``Users & Computers`` snap-in -  Create a new ``Computer`` object
    named ``client`` (the name of the host running SSSD)
#.  Create the keytab

    .. code-block:: PowerShell

        setspn -A host/client.ad.example.com@AD.EXAMPLE.COM client
        setspn -L client
        ktpass /princ host/client.ad.example.com@AD.EXAMPLE.COM /out client-host.keytab /crypto all /ptype KRB5_NT_PRINCIPAL -desonly /mapuser AD\\client$ /pass \*

    * This sets the machine account password and UPN for the principal
    * If you create additional keytabs for the host add ``-setpass -setupn`` for
      the above command to prevent resetting the machine password (thus changing
      kvno) and to prevent overwriting the UPN

#.  Transfer the keytab created in a secure manner to the client as
    ``/etc/krb5.keytab`` and make sure its permissions are correct:

    .. code-block:: bash

        chown root:root /etc/krb5.keytab
        chmod 0600 /etc/krb5.keytab
        restorecon /etc/krb5.keytab

#.  Check that the keytab works correctly

    .. code-block:: console

        # klist -ke
        # kinit -k CLIENT$@AD.EXAMPLE.COM

Using DN/Password Binds for LDAP Searches
=========================================

This method allows you to use SSSD against AD without joining the domain. Please
note that this is not generally recommended. See the options
``ldap_default_bind_dn``, ``ldap_default_authtok_type`` and
``ldap_default_authtok`` in the example configuration below.

Setup the Client
****************

#.  Configure SSSD and Kerberos and start the SSSD service

    .. code-tabs::

        .. code-tab:: ini
            :label: /etc/krb5.conf

            [logging]
            default = FILE:/var/log/krb5libs.log

            [libdefaults]
            default_realm = AD.EXAMPLE.COM
            dns_lookup_realm = true
            dns_lookup_kdc = true
            ticket_lifetime = 24h
            renew_lifetime = 7d
            rdns = false
            forwardable = yes

            # You may also want either of:
            # allow_weak_crypto = true
            # default_tkt_enctypes = arcfour-hmac

            [realms]
            # Define only if DNS lookups are not working
            # AD.EXAMPLE.COM = {
            #  kdc = server.ad.example.com
            #  admin_server = server.ad.example.com
            # }

            [domain_realm]
            # Define only if DNS lookups are not working
            # .ad.example.com = AD.EXAMPLE.COM
            # ad.example.com = AD.EXAMPLE.COM

        .. code-tab:: ini
            :label: /etc/sssd/sssd.conf

            [sssd]
            domains = ad.example.com
            services = nss, pam

            [nss]

            [pam]

            [domain/ad.example.com]
            # Unless you know you need referrals, turn them off
            ldap_referrals = false
            # Uncomment if you need offline logins
            # cache_credentials = true
            enumerate = false

            id_provider = ldap
            auth_provider = krb5
            chpass_provider = krb5
            access_provider = ldap

            # Uncomment if service discovery is not working
            #ldap_uri = ldap://server.ad.example.com/

            # Comment out if not using SASL/GSSAPI to bind
            ldap_sasl_mech = GSSAPI
            # Uncomment and adjust if the default principal host/fqdn@REALM is not available
            #ldap_sasl_authid = nfs/client.ad.example.com@AD.EXAMPLE.COM

            # Define these only if anonymous binds are not allowed and no keytab is available
            # Enabling use_start_tls is very important, otherwise the bind password is transmitted
            # over the network in the clear
            #ldap_id_use_start_tls = True
            #ldap_default_bind_dn = CN=binduser,OU=user accounts,DC=ad,DC=example,DC=com
            #ldap_default_authtok_type = password
            #ldap_default_authtok = bindpass

            ldap_schema = rfc2307bis

            ldap_user_search_base = ou=user accounts,dc=ad,dc=example,dc=com
            ldap_user_object_class = user

            ldap_user_home_directory = unixHomeDirectory
            ldap_user_principal = userPrincipalName

            ldap_group_search_base = ou=groups,dc=ad,dc=example,dc=com
            ldap_group_object_class = group

            ldap_access_order = expire
            ldap_account_expire_policy = ad
            ldap_force_upper_case_realm = true

            # Uncomment if dns discovery of your AD servers isn't working.
            #krb5_server = server.ad.example.com
            krb5_realm = AD.EXAMPLE.COM

            # Probably required with sssd 1.8.x and newer
            krb5_canonicalize = false

            # Perhaps you need to redirect to certain attributes?
            # ldap_user_object_class = user
            # ldap_user_name = sAMAccountName
            # ldap_user_uid_number = msSFU30UidNumber
            # ldap_user_gid_number = msSFU30GidNumber
            # ldap_user_gecos = displayName
            # ldap_user_home_directory = msSFU30HomeDirectory
            # ldap_user_shell = msSFU30LoginShell
            # ldap_user_principal = userPrincipalName
            # ldap_group_object_class = group
            # ldap_group_name = cn
            # ldap_group_gid_number = msSFU30GidNumber

#.  Make sure that you can obtain Kerberos credentials for an AD user

    .. code-block:: bash

        kinit aduser@AD.EXAMPLE.COM

#.  If you use SASL/GSSAPI to bind to AD also test that the keytab is working
    properly:

    .. code-block:: bash

        klist -ke
        kinit -k CLIENT$@AD.EXAMPLE.COM

#.  Now using this credential you've just created try fetching data from the
    server with ``ldapsearch`` (in case of issues make sure
    ``/etc/openldap/ldap.conf`` does not contain any unwanted settings):

    .. code-block:: bash

        ldapsearch -H ldap://server.ad.example.com -Y GSSAPI -N -b "dc=ad,dc=example,dc=com" "(&(objectClass=user)(sAMAccountName=aduser))"

#.  By using the credential from the keytab, you've verified that this credential
    has sufficient rights to retrieve user information.

PAM and nsswitch Configuration
******************************

You need to add pam_sss.so module into PAM configuration and enable SSSD in
``nsswitch.conf`` to allow user and group lookups and authentication.

.. code-tabs::
    :caption: Configure PAM

    .. fedora-tab::

        # This configures both nsswitch.conf and PAM
        authselect select sssd --force

    .. rhel-tab::

        # This configures both nsswitch.conf and PAM
        authselect select sssd --force

    .. ubuntu-tab::

        # Enable SSSD using the TUI
        pam-auth-update


.. code-block:: nsswitch
    :caption: /etc/nsswitch.conf

    passwd:         files sss
    shadow:         files sss
    group:          files sss
    hosts:          files dns
    bootparams:     files
    ethers:         files
    netmasks:       files
    networks:       files
    protocols:      files
    rpc:            files
    services:       files sss
    netgroup:       files sss
    publickey:      files
    automount:      files sss
    aliases:        files

Understanding Kerberos & Active Directory
*****************************************

It is important to understand that (unlike Linux MIT based KDC) Active Directory
based KDC divides Kerberos principals into two groups:

User Principals
    Usually equals to the ``sAMAccountname`` attribute of the object in AD. In
    short, user principal is entitled to obtain a TGT (Ticket Granting Ticket).
    User principals could be hence used to generate a TGT via ``kinit -k
    <principalname>``

Service Principals
   Represents which Kerberized service can be used on the computer in question.
   Service principals **CANNOT** be used to obtain a TGT therefore they cannot
   be used to grant an access to Active Directory controller for example.

Each user object in Active Directory (understand that a computer object
in AD is de-facto a user object as well) can have:

*  Maximum of 2 User Principal Names (UPN). One is pre-defined by its
   ``sAMAccountName`` LDAP attribute (mentioned above, for computer
   objects it has a form of ``<hostname>$``) and second by its
   ``UserPrincipalName`` string attribute
*  Multiple Service Principal Names (typically one for each Kerberized
   service we want to enable on the computer) defined by the
   ``ServicePrincipalName`` (SPN) list attribute. The attributes can be
   seen/set using the ``ADSIedit`` snap-in for example.

.. seealso::

    See the following `article`_ Technet site for more in-depth Kerberos
    understanding.

    .. _article: http://technet.microsoft.com/en-us/library/cc772815%28WS.10%29.aspx
