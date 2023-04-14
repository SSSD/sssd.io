SSSD Errors
###########

SSSD process is terminated by own WATCHDOG
******************************************

  .. code-block:: sssd-log

      (Fri Apr 14 15:07:19 2023) system1 sssd[sssd]: Child [1277] ('SSSDdomain':'%BE_SSSDdomain') was terminated by own WATCHDOG. Consult corresponding logs to figure out the reason.

The above log indicates that the sssd_be process was blocked too long on something that was longer than ``3*10`` seconds(the default value of ``timeout`` is 10 sec). In order to find which operation is blocking sssd_be, enable sssd debugging by adding ``debug_level = 9`` under all sections of the ``/etc/sssd/sssd.conf`` file, especially under the ``[$domain]`` section, and wait for the issue to reoccur. Once the issue is observed, take the timestamp of the ``... was terminated by own WATCHDOG`` message and then spot the last operation before the timestamp in ``/var/log/sssd/sssd_$domain.log``. In the above example, sssd_be is getting killed, but there could be some other situation where ``sssd_nss`` or ``sssd_pam`` processes could get killed by watchdog. In this case, the troubleshooting process will be the same, but the respective sssd log needs to be checked instead of the ``/var/log/sssd/sssd_$domain.log`` file. Increasing the ``timeout`` values may serve as a workaround, however finding the root cause of the watchdog termination may be important. On a side note if the processing of group membership is very slow then also we can observe ``sssd_be killed by watchdog``.

  
sdap_async_sys_connect request failed
*************************************

  .. code-block:: sssd-log

      (Fri Apr 14 16:07:19 2023) [sssd[be[example.com]]] [sssd_async_socket_init_done] (0x0020): sdap_async_sys_connect request failed: [110]: Connection timed out.

sdap_async_sys_connect request failed occurs if sssd is not able to connect to the LDAP server within 6 seconds. This could be an issue with DNS or the network. Validate the DNS SRV records; if SRV records are not working, hardcoding the AD/LDAP server may help here. For an example, if id_provider = ad is being used then hardcoding of AD servers can be done as: add ``ad_server = ad1.example.com, ad2.example.com`` under the ``[$domain]`` section of the ``/etc/sssd/sssd.conf``. If the network is slow or ldap_network_timeout is reached, then consider increasing the value of ``ldap_network_timeout`` which is set to 6 seconds by default.

  .. code-block:: sssd-log

      (2023-04-20 21:37:10): [be[example.com]] [generic_ext_search_handler] (0x0020): [RID#1434] sdap_get_generic_ext_recv failed: [110]: Connection timed out [ldap_search_timeout]
      (2023-04-20 21:37:16): [be[example.com]] [sssd_async_connect_done] (0x0020): [RID#1434] connect failed [110][Connection timed out].
      (2023-04-20 21:37:16): [be[example.com]] [sssd_async_connect_done] (0x0020): [RID#1434] connect failed [110][Connection timed out].
      (2023-04-20 21:37:16): [be[example.com]] [sssd_async_socket_init_done] (0x0020): [RID#1434] sdap_async_sys_connect request failed: [110]: Connection timed out [ldap_network_timeout].
  
In the above example ``sdap_get_generic_ext_recv failed`` is getting failed due to the network issue we could see ``Connection timed out [ldap_network_timeout]`` and ``connection timed out [ldap_search_timeout]``. As a workaround consider increasing the value of ``ldap_network_timeout`` and ``ldap_search_timeout``. But we should  identify the underlying network issue.

We may notice ``sdap_get_generic_ext_recv failed: [110]: Connection timed out [ldap_search_timeout]`` error msg in case of ``id_provider = ldap`` in such situation it's necessary to check if the ``TLS`` handshake is successful.  

krb5_auth_timeout or krb5_child_timeout reached
***********************************************

  .. code-block:: sssd-log

      (Fri Apr 14 16:37:19 2023) [sssd[be[example.com]]] [krb5_child_timeout] (0x0040): Timeout for child [23514] reached. In case KDC is distant or network is slow you may consider increasing value of krb5_auth_timeout.
  
The above error is self-explanatory when trying to connect to the KDC server, but the KDC server is responding very slowly due to some reason. One of them could be an issue with the firewall or a slow network. As a workaround, consider increasing the value of ``krb5_auth_timeout`` which is 6 seconds by default.

TSIG error with server: tsig verify failure
*******************************************

  .. code-block:: sssd-log

      (Fri Apr 14 16:37:19 2023) example.com sssd[87108]: ; TSIG error with server: tsig verify failure

When SSSD is configured with ``id_provider = ad``, by default, sssd will try to update the DNS record using the nsupdate command. If tsig/nsupdate is failing, sssd will return ``TSIG error with server: tsig verify failure``. This error can be safely ignored if ``Dynamic DNS update`` is not being used. ``Dynamic DNS update`` can be disabled using ``dyndns_update = false`` under the ``[$domain]`` section of the ``/etc/sssd/sssd.conf`` file. If ``Dynamic DNS update`` is being used, then in order to identify the issue, enable sssd debugging using :doc:`basics`

SSSD is offline/Backend is offline
**********************************

   .. code-block:: sssd-log

       (Sat Apr 15 01:07:19 2023) [sssd[be[example.com]] [sbus_issue_request_done] (0x0040): sssd.dataprovider.getAccountInfo: Error [1432158212]: SSSD is offline

SSSD is going offline because it cannot establish a connection to the LDAP server, but the cause could vary. It may be a DNS issue where SRV records are not resolving. It may be a connection issue when the remote server is unreachable because it is behind a firewall, etc. If the DNS or network issue is intermittent then enable authenticate against cache in SSSD. Set ``cache_credentials = True`` under the ``[$domain]`` section of the ``/etc/sssd/sssd.conf`` then user logins should still work if the credentials are already present in the cache. For more details refer to :doc:`../design-pages/cached_authentication`.

s2n exop request failed/ldap_extended_operation failed
******************************************************

  .. code-block:: sssd-log

      (Sat Apr 15 12:07:19 2023): [be[ipa.example.com]] [sdap_call_op_callback] (0x20000): [RID#9] Handling LDAP operation [26][server: [10.23.x.x:389] IPA EXOP] took [10083.267] milliseconds.
      (Sat Apr 15 12:07:19 2023): [be[ipa.example.com]] [ipa_s2n_exop_done] (0x0040): [RID#9] ldap_extended_operation result: Time limit exceeded(3), (null).
      (Sat Apr 15 12:07:19 2023): [be[ipa.example.com]] [ipa_s2n_exop_done] (0x0040): [RID#9] ldap_extended_operation failed, server logs might contain more details.
      (Sat Apr 15 12:07:19 2023): [be[ipa.example.com]] [sdap_op_destructor] (0x2000): [RID#9] Operation 26 finished
      (Sat Apr 15 12:07:19 2023): [be[ipa.example.com]] [ipa_s2n_get_user_done] (0x0040): [RID#9] s2n exop request failed.
      (Sat Apr 15 12:07:19 2023): [be[ipa.example.com]] [sdap_id_op_done] (0x4000): [RID#9] releasing operation connection
      (Sat Apr 15 12:07:19 2023): [be[ipa.example.com]] [ipa_subdomain_account_done] (0x0040): [RID#9] ipa_get_*_acct request failed: [1432158230]: Network I/O Error.
  
ldap_extended_operation failed or s2n exop request failed indicates that the IPA client has sent the request to the IPA server, but connection with the LDAP sevr due to some reason the request has been failed. The IPA server's sssd log will contain more information. Compare the logs between both client and server from the same timeframe. The IPA client s2n request also hits the IPA directory server extdom plugin, investigating IPA 389 directory server access/error logs may be useful here too. For more details, refer to :doc:`IPA common issues <ipa_provider>`.

  .. code-block:: sssd-log

      (Sat Apr 15 01:37:19 2023): [be[ipa.example.com]] [ipa_s2n_exop_done] (0x0040): ldap_extended_operation result: Server is busy(51), Too many extdom instances running.
  
The above log indicates that on the server, the client is currently using 80% of the worker threads of the directory server are busy with requests coming from SSSD clients. To avoid having other important tasks blocked, no further requests will be accepted until more workers are free again. So increasing the number of worker threads on the Directory/IPA server should be a workaround. `Refer to the performance tuning documentation <https://access.redhat.com/documentation/en-us/red_hat_directory_server/12/html-single/tuning_the_performance_of_red_hat_directory_server/index>`_ for more details.

ldap_install_tls failed
***********************

  .. code-block:: sssd-log

      (Sat Apr 15 01:57:19 2023): [be[example.com]] [sss_ldap_init_sys_connect_done] (0x0020): ldap_install_tls failed: [Connect error]

If sssd is not able to create a TLS/SSL connection with the LDAP server due to some reason, then ``ldap_install_tls failed`` is observed. There may be an issue with the certificates or LDAP server. The above error indicates that, the hostname is not matching with subjectAltName in the certificate.

  .. code-block:: sssd-log

      (Sat Apr 15 02:11:19 2023): [be[default]] [sss_ldap_init_sys_connect_done] (0x0020): ldap_install_tls failed: [Connect error] [unknown error]
    ....
      (Sat Apr 15 02:11:19 2023): [be[default]] [sdap_sys_connect_done] (0x0020): sdap_async_connect_call request failed: [1432158304]: TLS handshake was interrupted.

The above error message is a generic message that simply indicates that ldap_install_tls is failing. In order to find the exact reason, enable sssd debugging using :doc:`basics` and add ``ldap_library_debug_level = -1`` under the ``[$domain] section``.

ldap_sasl_interactive_bind_s failed
***********************************

`ldap_sasl_interactive_bind_s failed` as the name suggest the bind is failing here sssd is not able to create SASL bind with the LDAP server.

  .. code-block:: sssd-log

      (2023-04-07 12:41:21): [be[gcr.geg.local]] [ad_sasl_log] (0x0040): SASL: GSSAPI Error: Unspecified GSS failure.  Minor code may provide more information (KDC has no support for encryption type) 
      (2023-04-07 12:41:21): [be[gcr.geg.local]] [sasl_bind_send] (0x0020): ldap_sasl_interactive_bind_s failed (-2)[Local error]

The above log indicates the bind is failing since the KDC's supported encryption type does not match the RHEL encryption type. If this is specific to ``RHEL8.x`` then investigate the enabled crypto policy. By default, SSSD supports ``RC4, AES-128, and AES-256`` Kerberos encryption types. In ``RHEL8`` ``RC4`` encryption has been deprecated and disabled by default, as it is considered less secure than the newer AES-128 and AES-256 encryption types. Without any common encryption types, communication between RHEL hosts and AD domains might not work, or some AD accounts might not be able to authenticate. To remedy this situation, enable ``AES`` encryption support in Active Directory (recommended option) or enable ``RC4`` support in RHEL.

  .. code-block:: sssd-log

      (2023-03-20 15:32:07): [be[example.com]] [sasl_bind_send] (0x0100): [RID#4] Executing sasl bind mech: GSS-SPNEGO, user: RHEL_BOX$
  
      (2023-03-20 15:32:07): [be[example.com]] [sasl_bind_send] (0x0020): [RID#4] ldap_sasl_interactive_bind_s failed (-2)[Local error]
      (2023-03-20 15:32:07): [be[example.com]] [sasl_bind_send] (0x0080): [RID#4] Extended failure message: [SASL(-1): generic failure: GSSAPI Error: Unspecified GSS failure.  Minor code may provide more information (Cannot contact any KDC for realm 'root.example.com')

The above log indicates that the bind is failing since sssd is not able to contact the ``KDC`` server. 
