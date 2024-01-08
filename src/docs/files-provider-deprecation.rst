Files Provider Removal
######################

The SSSD team has announced the `removal of the files provider <https://pagure.io/fesco/issue/3107>`_ feature in recent versions of SSSD in Fedora/CentOS Stream/RHEL. This document describes how to switch to using the SSSD 'proxy' provider to replace files provider functionality.

Practically, there are only two use cases that currently justify usage of the files provider feature:

* smart card authentication of local users
* session recording for local users

For both cases the proxy provider is a viable substitute. Otherwise, there is no benefit in SSSD handling local users. The SSSD proxy provider is just a relay, an intermediary configuration. SSSD connects to its proxy service, and then that proxy loads the specified libraries. This allows SSSD to use some resources that it otherwise would not be able to use.

Follow the steps below based on the use case you are using.

Smartcard Authentication for Local Users
****************************************

An example of the old `files provider` smartcard configuration which will no longer function properly is:

.. code-block:: console

    [pam]
    pam_cert_auth = True

    [domain/shadowutils]
    id_provider = files

Now let's look at the steps to setup the proxy provider replacement. First, make sure to install the ``sssd-proxy`` package.

.. code-block:: console

    $ dnf install sssd-proxy

Configure SSSD for smart card authentication as below:

.. code-block:: console

    [domain/myproxy]
    id_provider = proxy
    proxy_lib_name = files
    local_auth_policy = only

.. note:: An explicit **proxy_pam_target** is only needed if you want Smartcard authentication be an additional method besides the method provided by the **proxy_pam_target** (in this case you should also use **local_auth_policy = enable:smartcard**). This is typically not needed for password authentication because pam_unix should be present in the PAM configuration to handle this.

.. note:: The domain name in the `certmap` rule needs to be updated if the domain name was modified from the previous configuration, **shadowutils** to **myproxy** as shown here.

Choose one of the following authselect profiles and run the appropriate command:

.. code-block:: bash

    authselect select sssd with-smartcard
    authselect select sssd with-smartcard-lock-on-removal
    authselect select sssd with-smartcard-required

Now you are done!

Session Recording for Local Users
*********************************

Configure SSSD for session recording as below:

.. code-block:: console

    [sssd]
    services=nss, pam
    domains=nssfiles

    [domain/nssfiles]
    id_provider=proxy
    proxy_lib_name=files
    proxy_pam_target=sssd-shadowutils

The ``proxy_lib_name`` option specifies which existing NSS library to proxy identity requests through.

The ``proxy_pam_target`` specifies the target to which PAM must proxy as an authentication provider. This PAM target is a file containing PAM stack information in the default PAM directory, ``/etc/pam.d/``. The file `sssd-shadowutils <https://github.com/SSSD/sssd/blob/master/src/examples/sssd-shadowutils>`_ is packaged with upstream SSSD and shipped in Fedora.

.. note:: Ensure that the proxy PAM target stack does not recursively include pam_sss.so.

.. code-block:: console

    ~# cat /etc/pam.d/sssd-shadowutils
    #%PAM-1.0
    auth        [success=done ignore=ignore default=die] pam_unix.so nullok try_first_pass
    auth        required      pam_deny.so

    account     required      pam_unix.so
    account     required      pam_permit.so

Add SSSD session recording configuration, refer to `man sssd-session-recording` for more details:

.. code-block:: console

        [session_recording]
        scope = some
        users = contractor1, contractor2
        groups = students

Next it is required to set the `sss` module as the first module in the list for the `passwd` and `group` databases of ``/etc/nsswitch.conf``. On systems managed by authselect, the following command should be run:

.. code-block:: bash

    authselect select sssd with-tlog