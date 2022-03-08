Using AutoFS with Active Directory
##################################

This article shows how to use AutoFS and Kerberos to automatically mount shared
folders on a Microsoft Windows Server via `Common Internet File System (CIFS)
<https://cifs.com>`__.

Creating a shared folder
************************

First, we need to create a shared folder on the Windows Server. As a Windows
administrator you probably already know how to do that, but for the sake of this
article you can use the following PowerShell script as an example.

It will create a folder at ``C:\_shared`` and enable sharing on it for the
groups ``Administrator`` (full access) and ``Users`` (read only access). This
means that it requires an authenticated user to access the share.

.. code-block:: powershell

    # Create a directory that we want to share
    New-Item 'C:\_shared' -ItemType Directory

    # Share the directory
    New-SMBShare -Name _shared -Path C:\_shared -FullAccess Administrators -ReadAccess Users

Mounting a CIFS share with Kerberos manually
********************************************

First, install CIFS dependencies:

.. code-tabs::

    .. fedora-tab::

        $ sudo dnf install -y cifs-utils

    .. rhel-tab::

        $ sudo yum install -y cifs-utils

    .. ubuntu-tab::

        $ sudo apt-get install -y cifs-utils

Now make sure you have a valid ticket-granting ticket for your user:

.. code-block:: console

    $ kinit Administrator@AD.VM
    Password for Administrator@AD.VM:
    $ klist
    Ticket cache: KCM:1730800500:40268
    Default principal: Administrator@AD.VM

    Valid starting       Expires              Service principal
    03/08/2022 13:06:07  03/08/2022 23:06:07  krbtgt/AD.VM@AD.VM
        renew until 03/15/2022 13:06:07

When we have all prerequisites in place, we can move forward by creating the
target folder and finally mounting the shared directory.

.. code-block:: console

    $ mkdir _shared
    $ sudo mount -t cifs -o "user=Administrator@AD.VM,cruid=Administrator@ad.vm,sec=krb5,vers=3,multiuser" //root-dc.ad.vm/_shared _shared

Parameters explanation:

* ``sec=krb5`` simply says that we want to use Kerberos protocol to authenticate the user against the CIFS share
* ``user`` defines the user that we want to authenticate as
* ``cruid`` is the user whose credential cache will be used for authentication
* ``vers=3`` tells the cifs module to use Window's SMB protocol v3 or later
* ``multiuser`` means that the credentials of the user who is currently
  accessing the share will be used to control access

.. seealso::

    You can read man mount.cifs(8) for more information.


Mounting CIFS share with AutoFS
*******************************

In order to let autofs mount the folder automatically, we need to use a Kerberos
keytab. Lets create a new user ``cifs`` that would be used to mount the CIFS
share. We need to generate a keytab for this user and copy it to
``/etc/krb5.keytab`` on the Linux machine.

.. code-block:: powershell

    Import-Module ActiveDirectory

    $password = "Secret123" | ConvertTo-SecureString -AsPlainText -Force
    New-AdUser -Name "cifs" -UserPrincipalName "cifs@ad.vm" -AccountPassword $password -Enabled $true -PasswordNeverExpires $true -CannotChangePassword $true
    ktpass -mapuser "cifs@ad.vm" -princ "cifs@AD.VM" -pass "Secret123" -ptype KRB5_NT_PRINCIPAL -crypto ALL -out C:\krb5.keytab

Once the keytab is created and present on the hosts, we can create a new autofs
map. It will create a new mount point at ``/_shared``.

.. code-tabs::

    .. code-tab:: powershell
        :label: powershell

        Import-Module ActiveDirectory

        New-ADOrganizationalUnit -Name "autofs" -Path "dc=ad,dc=vm"

        New-ADObject -Name auto.master -Path 'ou=autofs,dc=ad,dc=vm' -Type nisMap -OtherAttributes @{'nisMapName'='auto.master'}
        New-ADObject -Name '/-' -Path 'cn=auto.master,ou=autofs,dc=ad,dc=vm' -Type nisObject -OtherAttributes @{'nisMapName'='/-'; 'nisMapEntry'='auto.direct'}

        New-ADObject -Name auto.direct -Path 'ou=autofs,dc=ad,dc=vm' -Type nisMap -OtherAttributes @{'nisMapName'='auto.direct'}
        New-ADObject -Name /_shared -Path 'cn=auto.direct,ou=autofs,dc=ad,dc=vm' -Type nisObject -OtherAttributes @{'nisMapName'='/_shared'; 'nisMapEntry'='-fstype=cifs,sec=krb5,user=cifs@AD.VM,vers=3,multiuser ://root-dc.ad.vm/_shared'}

    .. code-tab:: ldif
        :label: ldif

        dn: ou=autofs,dc=ad,dc=vm
        objectClass: top
        objectClass: organizationalUnit
        ou: autofs

        dn: cn=auto.master,ou=autofs,dc=ad,dc=vm
        objectClass: top
        objectClass: automountMap
        cn: auto.master
        nisMapName: auto.master

        dn: cn=/-,cn=auto.master,ou=autofs,dc=ad,dc=vm
        objectClass: top
        objectClass: automount
        nisMapName: /-
        nisMapEntry: auto.direct
        cn: /-

        dn: cn=auto.direct,ou=autofs,dc=ad,dc=vm
        objectClass: top
        objectClass: automountMap
        cn: auto.direct
        nisMapName: auto.direct

        dn: cn=/_shared,cn=auto.direct,ou=autofs,dc=ad,dc=vm
        objectClass: top
        objectClass: automount
        nisMapName: /_shared
        nisMapEntry: -fstype=cifs,sec=krb5,user=cifs@AD.VM,vers=3,multiuser ://root-dc.ad.vm/_shared
        cn: /_shared

Then we need to restart autofs, access the mount point and check that it has
been successfully mounted.

.. code-block:: console

    $ sudo systemctl enable autofs
    $ sudo systemctl restart autofs
    $ cd /_shared
    $ mount
    ...
    auto.direct on /_shared type autofs (rw,relatime,fd=5,pgrp=36940,timeout=300,minproto=5,maxproto=5,direct,pipe_ino=72103)
    //root-dc.ad.vm/_shared on /_shared type cifs (rw,relatime,vers=3.1.1,sec=krb5,cruid=0,cache=strict,multiuser,uid=0,noforceuid,gid=0,noforcegid,addr=192.168.100.110,file_mode=0755,dir_mode=0755,soft,nounix,serverino,mapposix,noperm,rsize=4194304,wsize=4194304,bsize=1048576,echo_interval=60,actimeo=1,user=cifs@AD.VM)
