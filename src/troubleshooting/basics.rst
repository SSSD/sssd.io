Troubleshooting Basics
######################

SSSD provides two major features - obtaining information about users and authenticating users. Each of these hook into different system APIs and should be viewed separately. However, a successful authentication can only be performed when the information about a user can be retrieved, so if authentication doesn't work in your case, please make sure you can at least obtain info from about the user with ``getent passwd $user`` and ``id``.

SSSD debug logs
***************

Each SSSD process is represented by a section in the ``sssd.conf`` config file. To enable debugging persistently across SSSD service restarts, put the directive ``debug_level=N``, where N typically stands for a number between 1 and 10 into the particular section. Debug levels up to 3 should log mostly failures and anything above level 8 provides a large number of log messages. Level 6 might be a good starting point for debugging problems. You can also use the ``sss_debuglevel(8)`` tool to enable debugging on the fly without having to restart the daemon.

On Fedora/RHEL, debug logs are stored under ``/var/log/sssd``. There is one log file per SSSD process. The services (also called responders) log into a log file called ``sssd_$service``, for example NSS responder logs to ``/var/log/sssd/sssd_nss.log``. Domain sections log to files called ``sssd_$domainname.log``. The short-lived helper processes also log to their own log files, such as ``ldap_child.log`` or ``krb5_child.log``.

.. note::

    Enabling `debug_level` in the `[sssd]` section only enables debugging of the sssd process itself, not all the worker processes!

Troubleshooting Identity Information
************************************

Before diving into the SSSD logs and config files it is very beneficial to know what the :doc:`../contrib/architecture` looks like. Please note the examples of the ``DEBUG`` messages are subject to change in future SSSD versions.

General tips
============

* To avoid SSSD caching, it is often useful to reproduce the bugs with an empty cache or at least invalid cache. However, keep in mind that also the cached credentials are stored in the cache! Do not remove the cache files if your system is offline and it relies on SSSD authentication!
* Before sending the logs and/or config files to a publicly-accessible space, such as mailing lists or bug trackers, check the files for any sensitive information.
* Please only send log files relevant to the occurrence of the issue. Issues in log files that are mega- or gigabytes large are more likely to be skipped
* Unless the problem you're trying to diagnose is related to enumeration, always reproduce the issue with ``enumerate=false``. Triaging logs with enumeration enabled obfuscates the normal data flow..

Getent or id commands don't print the user or group at all
==========================================================

Follow the usual name-service request flow:

#. Is sssd running at all? On most recent systems, running the below command would display the service status. Alternatively, check for the sssd processes with ``ps -ef | grep sssd`` or similar.

   .. code-block:: bash

        # systemctl status sssd

#. Is the ``sss`` module present in ``/etc/nsswitch.conf`` for all databases?

   * If there is a separate initgroups database configured, make sure it either contains the ``sss`` module as well or comment the ``initgroups`` line completely

#. Does the request reach the SSSD responder processes? Enable debugging by putting ``debug_level=6`` (or higher) into the ``[nss]`` section. Restart SSSD and check the nss log for incoming requests with the matching timestamp to your ``getent`` or ``id`` command. Here is how an incoming request looks like with SSSD-1.15:

   .. code-block:: sssd-log

        [sssd[nss]] [get_client_cred] (0x4000): Client creds: euid[10327] egid[10327] pid[18144].
        [sssd[nss]] [setup_client_idle_timer] (0x4000): Idle timer re-set for client [0x13c9960][22]
        [sssd[nss]] [accept_fd_handler] (0x0400): Client connected!
        [sssd[nss]] [sss_cmd_get_version] (0x0200): Received client version [1].
        [sssd[nss]] [sss_cmd_get_version] (0x0200): Offered version [1].
        [sssd[nss]] [nss_getby_name] (0x0400): Input name: admin

#. If the command is reaching the NSS responder, does it get forwarded to the Data Provider? Does the Data Provider request end successfully? An unsuccessful request would look like this:

   .. code-block:: sssd-log

        [sssd[nss]] [cache_req_search_dp] (0x0400): CR #3: Looking up [admin@ipa.test] in data provider
        [sssd[nss]] [sss_dp_issue_request] (0x0400): Issuing request for [0x41e51c:1:admin@ipa.test@ipa.test]
        [sssd[nss]] [sss_dp_get_account_msg] (0x0400): Creating request for [ipa.test][0x1][BE_REQ_USER][name=admin@ipa.test:-]
        [sssd[nss]] [sss_dp_internal_get_send] (0x0400): Entering request [0x41e51c:1:admin@ipa.test@ipa.test]
        [sssd[nss]] [sss_dp_req_destructor] (0x0400): Deleting request: [0x41e51c:1:admin@win.trust.test@win.trust.test]
        [sssd[nss]] [sss_dp_get_reply] (0x0010): The Data Provider returned an error [org.freedesktop.sssd.Error.DataProvider.Offline]
        [sssd[nss]] [cache_req_common_dp_recv] (0x0040): CR #3: Data Provider Error: 3, 5, Failed to get reply from Data Provider
        [sssd[nss]] [cache_req_common_dp_recv] (0x0400): CR #3: Due to an error we will return cached data

In contrast, a request that ran into completion would look like this:

   .. code-block:: sssd-log

        [sssd[nss]] [cache_req_search_dp] (0x0400): CR #3: Looking up [admin@ipa.test] in data provider
        [sssd[nss]] [sss_dp_issue_request] (0x0400): Issuing request for [0x41e51c:1:admin@ipa.test@ipa.test]
        [sssd[nss]] [sss_dp_get_account_msg] (0x0400): Creating request for [ipa.test][0x1][BE_REQ_USER][name=admin@ipa.test:-]
        [sssd[nss]] [sss_dp_get_reply] (0x1000): Got reply from Data Provider - DP error code: 0 errno: 0 error message: Success
        [sssd[nss]] [cache_req_search_cache] (0x0400): CR #3: Looking up [admin@ipa.test] in cache

If the Data Provider request had finished completely, but you're still not seeing any data, then chances are the search didn't match any object. Either, way, the next step is to look into the logs from the ``[domain]`` section. Put ``debug_level=6`` or higher into the appropriate [domain] section, restart SSSD, re-run the lookup and continue debugging in the next section.

Troubleshooting general sssd_be problems
========================================

* The back end performs several different operations, so it might be difficult to see where the problem is at first. At the highest level, the back end performs these steps, in this order

  #. The request is received from the responder
  #. The back end resolves the server to connect to. This step might involve locating the client site or resolving a SRV query
  #. The back end establishes connection to the server. In case the connection is authenticated, then a proper keytab or a certificate might be required
  #. Once connection is established, the back end runs the search. You should see the LDAP filter, search base and requested attributes.
  #. After the search finishes, the entries that matched are stored to the cache
  #. When the request ends (correctly or not), the status code is returned to the responder

* Make sure the back end is in "neutral" or "online" state when you run the search.

  * With some responder/provider combinations, SSSD might run a search immediately after startup, which, in case of misconfiguration, might mark the back end offline even before the first request by the user arrives.
  * You can forcibly set SSSD into offline or online state using the ``SIGUSR1`` and ``SIGUSR2`` signals, see the ``sssd(8)`` man page for details.

* Can the remote server be resolved? Check if the DNS servers in ``/etc/resolv.conf`` are correct. With AD or IPA back ends, you generally want them to point to the AD or IPA server directly.
  * Use the ``dig`` utility to test SRV queries, for instance:

  .. code-block:: bash

            dig -t SRV _ldap._tcp.ad.example.com @127.0.0.1

* Can the connection be established with the same security properties SSSD uses?

  * Many back ends require the connection to be authenticated. In case of AD and IPA, the connection is authenticated using the system keytab, the LDAP back end often uses certificates.
  * ``ldapsearch -ZZ`` is useful to test problems with certificates, since SSSD uses openldap libraries under the hood.
  * For debugging GSSAPI authentication, ``kinit`` is useful, often together with ``KRB5_TRACE``. Take care to select the correct principal, especially with the AD back end. If you select the highest ``debug_level = 10``, then ``ldap_child.log`` would contain the Kerberos tracing information as well.
  * Are the LDAP search properties correct?

    * Check if all the attributes required by the search are present on the server. This is especially important with the AD provider where the entries might not contain the POSIX attributes at all or might not have the POSIX attributes replicated to Global Catalog, in case SSSD is connecting to the GC.
        * As of SSSD-1.15, try looking for ``DEBUG`` messages from ``sdap_get_generic_ext_step``
    * Is the search base correct, especially with trusted subdomains? Incorrect search base with an AD subdomain would yield a referral.
  * Try running the same search with the ldapsearch utility. Don't forget to use the same authentication method as SSSD uses! For ``id_provider=ad`` or ``ipa`` this means adding ``-Y GSSAPI`` to the ``ldapsearch invocation``.

Troubleshooting Authentication, Password Change and Access Control
******************************************************************

In order for authentication to be successful, the user information must be accurately provided first. Before debugging authentication, please make sure the user information is resolvable with ``getent passwd $user`` or ``id $user``. Failing to retrieve the user info would also manifest in the secure logs or the journal with message such as:

.. code-block:: sssd-log

    pam_sss(sshd:account): Access denied for user admin: 10 (User not known to the underlying authentication module)

Authentication happens from PAM's ``auth`` stack and corresponds to SSSD's ``auth_provider``. Access control takes place in PAM ``account`` phase and is linked with SSSD's ``access_provider``. And lastly, password changes go through the ``password`` stack on the PAM side to SSSD's ``chpass_provider``.

If the user info can be retrieved, but authentication fails, the first place to look into is ``/var/log/secure`` or the system journal. Look for messages from ``pam_sss``. Please note that not all authentication requests come through SSSD. Notably, SSH key authentication and GSSAPI SSH authentication happen directly in SSHD and SSSD is only contacted for the ``account`` phase.

Troubleshooting general authentication problems
===============================================

The PAM authentication flow follows this pattern:

#. The PAM-aware application starts the PAM conversation. Depending on the PAM stack configuration, the ``pam_sss`` module would be contacted. To debug the authentication process, first check in the secure log or journal if ``pam_sss`` is called at all. If you don't see ``pam_sss`` mentioned, chances are your PAM stack is misconfigured. If you see ``pam_sss`` being contacted, enable debugging in pam responder logs

#. SSSD's PAM responder receives the authentication request and in most cases forwards it to the back end. Please note that unlike identity requests, the authentication/access control is typically not cached and always contacts the server. This might manifest as a slowdown in some cases, but it's quite important, because the supplementary groups in GNU/Linux are only set during login time.

   * The PAM responder logs should show the request being received from the pam stack and then forwarded to the back end.

   * If you see the authentication request getting to the PAM responder, but receiving an error from the back end, check the back end logs. An example error output might look like:

   .. code-block:: sssd-log

            [sssd[pam]] [sss_dp_issue_request] (0x0400): Issuing request for [0x411d44:3:admin@ipa.example.com]
            [sssd[pam]] [sss_dp_get_account_msg] (0x0400): Creating request for [ipa.example.com][3][1][name=admin]
            [sssd[pam]] [sss_dp_internal_get_send] (0x0400): Entering request [0x411d44:3:admin@ipa.example.com]
            [sssd[pam]] [sss_dp_get_reply] (0x1000): Got reply from Data Provider - DP error code: 1 errno: 11 error message: Offline
            [sssd[pam]] [pam_check_user_dp_callback] (0x0040): Unable to get information from Data Provider Error: 1, 11, Offline

#. The back end processes the request. This might include the equivalent of ``kinit`` done in the ``krb5_child`` process, an LDAP bind or consulting an access control list. After the back end request finishes, the result is sent back to the PAM responder.

   *  For Kerberos-based (that includes the IPA and AD providers) ``auth_provider``, look into the ``krb5_child.log`` file as well. Setting ``debug_level`` to 10 would also enable low-level Kerberos tracing information in that logfile. You can also simulate the authentication with ``kinit``.

   * If the back end's ``auth_provider`` is LDAP-based, you can simulate the authentication by performing a base-scoped bind as the user who is logging in:

   .. code-block:: bash

            ldapsearch -x -H ldap://master.ipa.example.com -b uid=admin,cn=users,cn=accounts,dc=ipa,dc=example,dc=com -s base -W

#. The PAM responder receives the result and forwards it back to the ``pam_sss`` module. The error or status message is displayed in ``/var/log/secure`` or journal.

General common SSSD problems
****************************

* Logins take too long or the time to execute ``id $username`` takes too long.

  * First, make sure to understand `what does id username do <https://jhrozek.wordpress.com/2014/01/27/why-is-id-so-slow-with-sssd/>`_. Do you really care about its performance? Chances are you're more interested in ``id -G`` performance.
  * Check out the ``ignore_group_members`` options in the ``sssd.conf(5)`` manual page.
  * Some users improved their SSSD performance a lot by mounting the cache into ``tmpfs``
* ``getent passwd`` and ``getent group`` doesn't display any users or groups.

  * Enumeration is disabled by design. See the FAQ page for explanation
* Changes on the server are not reflected on the client for quite some time

  * The SSSD caches identity information for some time. You can force cache refresh on next lookup using the ``sssctl cache-expire`` command.

    * Please note that during login, updated information is always re-read from the server
* After enrolling the same machine to a domain with different users (perhaps a test VM was enrolled to a newly provisioned server), no users can be resolved or log in

  * Probably the new server has different ID values even if the users are named the same (like admin in an IPA domain). Currently UID changes are not supported, caches must be removed.

* How do I enable LDAP authentication over an unsecure connection?

  * Not possible, sorry. SSSD requires the use of either TLS or LDAPS for LDAP authentication. Perimeter security is just not enough.
* There are no messages from ``pam_sss`` at all

  * Your PAM stack is likely misconfigured. Use the ``authselect`` tool if available together with ``sssd`` profile.
  * Alternatively, check that the authentication you are using is PAM-aware, because some authentication methods, like SSH public keys are handled directly in the SSHD and do not use PAM at all.
* I can ``su`` to an SSSD user from root, but not from a regular user, SSH doesn't work either

  * If you su to another user from root, you typically bypass SSSD authentication completely by using the ``pam_rootok.so`` module. Your SSSD setup is likely broken, please log in as an ordinary user and continue debugging in this section
* I'm receiving ``System Error (4)`` in the authentication logs

  * System Error is an "Unhandled Exception" during authentication. It can either be an SSSD bug or a fatal error during authentication. Either way, please bring up your issue on the `sssd-users mailing list <https://lists.fedorahosted.org/admin/lists/sssd-users.lists.fedorahosted.org/>`_

* I'm receiving ``Access denied for user $user: 6 (Permission denied)``

  * Authentication went fine, but the user was denied access to the client machine. You can temporarily disable access control with setting ``access_provider=permit`` temporarily. Don't forget to reset the access provider to a stricter setting after finding out the root cause\!
  * If disabling access control doesn't help, the account might be locked on the server side. Check the SSSD domain logs to find out more.
* I can't get my LDAP-based access control filter right for group access control using the memberOf attribute

  * The LDAP-based access control is really tricky to get right and doesn't typically handle nested groups well. Use the simple access provider ``man sssd-simple`` instead.

