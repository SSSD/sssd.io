Joining AD Domain Manually
##########################

The manual process of joining the GNU/Linux client to the AD domain consists of several steps:

* Acquiring the host keytab with Samba or create it using ``ktpass`` on the AD controller
* Configuring ``sssd.conf``
* Configuring the system to use the SSSD for identity information and authentication

Creating Host Keytab with Samba
*******************************

On the GNU/Linux client with properly configured ``/etc/krb5.conf`` (see below) and suitable ``/etc/samba/smb.conf``, replacing your REALM/Domain name:

.. code-block:: ini
   :caption: /etc/krb5.conf

    [logging]
    default = FILE:/var/log/krb5libs.log

    [libdefaults]
    default_realm = AD.EXAMPLE.COM
    dns_lookup_realm = true
    dns_lookup_kdc = true
    ticket_lifetime = 24h
    renew_lifetime = 7d
    forwardable = true
    rdns = false

    # You may also want either of:
    # allow_weak_crypto = true
    # default_tkt_enctypes = arcfour-hmac

    [realms]
    # Define only if DNS lookups are not working
    # AD.EXAMPLE.COM = {
    # kdc = server.ad.example.com
    # master_kdc = server.ad.example.com
    # admin_server = server.ad.example.com
    # }

    [domain_realm]
    # Define only if DNS lookups are not working
    # .ad.example.com = AD.EXAMPLE.COM
    # ad.example.com = AD.EXAMPLE.COM

Make sure ``kinit aduser@AD.EXAMPLE.COM`` works properly. If not, using ``KRB5_TRACE`` usually provides helpful information:

.. code-block:: bash

    KRB5_TRACE=/dev/stdout kinit -V aduser@AD.EXAMPLE.COM.

Update ``/etc/samba/smb.conf``, replacing the sample domain/realm name with yours:

.. code-block:: ini
   :caption: /etc/samba/smb.conf

    [global]
    security = ads
    realm = AD.EXAMPLE.COM
    workgroup = EXAMPLE

    log file = /var/log/samba/%m.log

    kerberos method = secrets and keytab

    client signing = yes
    client use spnego = yes

Now join the client with:

.. code-block:: bash

    kinit Administrator
    net ads join -k

Alternatively, without using the Kerberos ticket:

.. code-block:: bash

    net ads join -U Administrator

Additional principals can be created later with ``net ads keytab add`` if needed.

You don't need a Domain Administrator account to do this, you just need an account with sufficient rights to join a machine to the domain. This is a notable advantage of this approach over generating the keytab directly on the AD controller.

Creating Service Keytab on AD
*****************************

Do not do this step if you've already created a keytab using Samba. This part of the guide might be useful if the password for Administrator or another user who is able to enroll computers can't be shared.

On the Windows server:

* Open Users & Computers snap-in
* Create a new Computer object named ``client`` (i.e., the name of the host running SSSD)
* On the command prompt

.. code-block:: bash

    setspn -A host/client.ad.example.com@AD.EXAMPLE.COM client
    setspn -L client
    ktpass /princ host/client.ad.example.com@AD.EXAMPLE.COM /out client-host.keytab /crypto all
    /ptype KRB5_NT_PRINCIPAL -desonly /mapuser AD\client$ +setupn +rndPass +setpass +answer

* This sets the machine account password and UPN for the principal
* If you create additional keytabs for the host add ``-setpass -setupn`` for the above command to prevent resetting the machine password (thus changing kvno) and to prevent overwriting the UPN
* Transfer the keytab created in a secure manner to the client as ``/etc/krb5.keytab`` and make sure its permissions are correct:

.. code-block:: bash

    chown root:root /etc/krb5.keytab
    chmod 0600 /etc/krb5.keytab
    restorecon /etc/krb5.keytab

See the next section for verifying the keytab file and the example ``sssd.conf`` below for the needed SSSD configuration.

Pre-flight check
****************

To verify the keytab was acquired correctly and can be used to access AD:

.. code-block:: bash

    net ads join -U Administrator

    klist -ke
    kinit -k CLIENT\$@AD.EXAMPLE.COM

Now using this credential you've just created try fetching data from the server with ``ldapsearch`` (in case of issues make sure ``/etc/openldap/ldap.conf`` does not contain any unwanted settings):

.. code-block:: bash

    net ads join -U Administrator

    /usr/bin/ldapsearch -H ldap://server.ad.example.com/ -Y GSSAPI -N -b "dc=ad,dc=example,dc=com"
    "(&(objectClass=user)(sAMAccountName=aduser))"

By using the credential from the keytab, you've verified that this credential has sufficient rights to retrieve user information.

You can also check if searching the Global Catalog works and whether the attributes your environment depends on are replicated to the Global Catalog:

.. code-block:: bash

    net ads join -U Administrator

    /usr/bin/ldapsearch -H ldap://server.ad.example.com:3268 -Y GSSAPI -N -b "dc=ad,dc=example,dc=com"
    "(&(objectClass=user)(sAMAccountName=aduser))"

After both ``kinit`` and ``ldapsearch`` work properly proceed to actual SSSD configuration.

SSSD setup
**********

Configuring SSSD consists of several steps:

* Install the ``sssd-ad`` package on the GNU/Linux client machine
* Make configuration changes to the files below
* Start the ``sssd`` service

Copy the following sssd.conf, additional options can be added as needed

.. code-block:: ini
   :caption: /etc/sssd/sssd.conf

    [sssd]
    config_file_version = 2
    domains = ad.example.com
    services = nss, pam

    [domain/ad.example.com]
    # Uncomment if you need offline logins
    # cache_credentials = true

    id_provider = ad
    auth_provider = ad
    access_provider = ad

    # Uncomment if service discovery is not working
    # ad_server = server.ad.example.com

    # Uncomment if you want to use POSIX UIDs and GIDs set on the AD side
    # ldap_id_mapping = False

    # Uncomment if the trusted domains are not reachable
    #ad_enabled_domains = ad.example.com

    # Comment out if the users have the shell and home dir set on the AD side
    default_shell = /bin/bash
    fallback_homedir = /home/%d/%u

    # Uncomment and adjust if the default principal SHORTNAME$@REALM is not available
    # ldap_sasl_authid = host/client.ad.example.com@AD.EXAMPLE.COM

    # Comment out if you prefer to use shortnames.
    use_fully_qualified_names = True

    # Uncomment if the child domain is reachable, but only using a specific DC
    # [domain/ad.example.com/child.example.com]
    # ad_server = dc.child.example.com

Set the file ownership and permissions

.. code-block:: bash

    chown root:root /etc/sssd/sssd.conf
    chmod 0600 /etc/sssd/sssd.conf
    restorecon /etc/sssd/sssd.conf

NSS/PAM Configuration
*********************

Depending on your distribution you have different options how to enable SSSD.

.. code-tabs::
    :caption: Configure identity/authentication files

    .. fedora-tab::

        dnf install oddjob-mkhomedir
        authselect select sssd with-mkhomedir
        systemctl enable --now oddjobd.service

    .. rhel-tab::

        dnf install oddjob-mkhomedir
        authselect select sssd with-mkhomedir
        systemctl enable --now oddjobd.service

    .. ubuntu-tab::

        apt install libnss-sss libpam-sss

On Debian/Ubuntu, add ``pam_mkhomedir.so`` to the PAM session configuration manually and restart SSSD.

Configure NSS/PAM manually
--------------------------

Manual configuration can be done with the following changes. The file paths for PAM in the example below are from Debian/Ubuntu, in Fedora/RHEL corresponding manual configuration should be done in ``/etc/pam.d/system-auth`` and ``/etc/pam.d/password-auth``. See the sample
nsswitch.conf below, it is expected to contain other modules.

.. code-block:: nsswitch
   :caption: /etc/nsswitch.conf

    passwd: files sss
    shadow: files sss
    group: files sss

    hosts: files dns

    bootparams: files

    ethers: files
    netmasks: files
    networks: files
    protocols: files
    rpc: files
    services: files sss

    netgroup: files sss

    publickey: files

    automount: files sss
    aliases: files
    sudoers : files sss


in the ``/etc/pam.d/common-auth file``, Right after the ``pam_unix.so`` line, add:

.. code-block:: pam
   :caption: /etc/pam.d/common-auth

    auth sufficient pam_sss.so use_first_pass

in the ``/etc/pam.d/common-account`` file, Right after the ``pam_unix.so`` line, add:

.. code-block:: pam
   :caption: /etc/pam.d/common-account

    account [default=bad success=ok user_unknown=ignore] pam_sss.so

in the ``/etc/pam.d/common-password`` file, Right after the ``pam_unix.so`` line, add:

.. code-block:: pam
   :caption: /etc/pam.d/common-password

    password sufficient pam_sss.so use_authtok

In the ``/etc/pam.d/common-session`` file. Just before the ``pam_unix.so`` line, add:

.. code-block:: pam
   :caption: /etc/pam.d/common-session

    session optional pam_mkhomedir.so

Also in this file right after the ``pam_unix.so`` line, add:

.. code-block:: pam
   :caption: /etc/pam.d/common-session

    session optional pam_sss.so
