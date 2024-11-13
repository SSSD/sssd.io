Performance tuning in SSSD
##########################

Slow id lookup
**************

``id`` lookup may become slow if the LDAP or AD user is a member of large groups (viz., 500+ groups). ``id`` is very heavy. ``id`` does a lot under the hood.
Behind the scenes, when the ``id $user`` command is executed, it triggers the following:
 
1] Get user information - getpwnam() for the user.
 
2] Get primary group information - getgrgid() for the primary group of the user.
 
3] Get list of groups - getgrouplist() for the user.
 
4] Get group information for each group returned from step 3 - getgrid() for all GIDs returned from the getgrouplist() call.
 
We can identify from the above 4 steps which step is actually slow. In order to collect detailed information, we need to add ``debug_level = 9`` under the ``[$domain]`` section of the ``/etc/sssd/sssd.conf" file, followed by a ``sssd`` restart. We often notice that step 4 is the step where ``sssd`` takes most of its time because the most data-intensive operation is downloading the groups, including their members, and by default this feature is enabled. We can turn this off by setting ``ignore_group_members = true``.
Usually, we are interested in what groups a user is a member of. Setting the ``ignore_group_members`` option to True makes all groups appear as empty, thus downloading only information about the group objects themselves and not their members, providing a significant performance boost. Please note that id aduser@ad_domain would still return all the correct groups.
 
- Pros: getgrnam/getgrgid calls are significantly faster.
- Cons: getgrnam/getgrgid calls only return the group information, not the members.
 
**WARNING! If the compat tree is used, DO NOT SET ignore_group_members = true because it breaks the compatibility logic.**

If after disabling group_members the id lookup is still slow, in that case we can get into the sssd debug logs and verify how long the ``Initgroups`` call is taking. This can be done by grepping the ``CR`` no. of that id lookup request. In this example, "sssd_nss`` is taking ``1 sec`` to process the user group membership. In the below example, we have only 39 groups associated with the AD user. If the count is large, for an example, 500-600 and the ``ignore_group_members`` is not set to true, then it is expected that the id lookup will take some time with the cold cache.

.. code-block:: sssd-log

        $ grep 'CR #3\:' /var/log/sssd/sssd_nss.log
	(2023-06-08 12:21:31): [nss] [cache_req_set_plugin] (0x2000): CR #3: Setting "Initgroups by name" plugin
	(2023-06-08 12:21:31): [nss] [cache_req_send] (0x0400): CR #3: New request 'Initgroups by name'
	(2023-06-08 12:21:31): [nss] [cache_req_process_input] (0x0400): CR #3: Parsing input name [roy]
	(2023-06-08 12:21:31): [nss] [cache_req_set_name] (0x0400): CR #3: Setting name [roy]
	(2023-06-08 12:21:31): [nss] [cache_req_select_domains] (0x0400): CR #3: Performing a multi-domain search
	(2023-06-08 12:21:31): [nss] [cache_req_search_domains] (0x0400): CR #3: Search will check the cache and check the data provider
	(2023-06-08 12:21:31): [nss] [cache_req_set_domain] (0x0400): CR #3: Using domain [redhat.com]
	(2023-06-08 12:21:31): [nss] [cache_req_prepare_domain_data] (0x0400): CR #3: Preparing input data for domain [redhat.com] rules
	(2023-06-08 12:21:31): [nss] [cache_req_search_send] (0x0400): CR #3: Looking up roy@redhat.com
	(2023-06-08 12:21:31): [nss] [cache_req_search_ncache] (0x0400): CR #3: Checking negative cache for [roy@redhat.com]
	(2023-06-08 12:21:31): [nss] [cache_req_search_ncache] (0x0400): CR #3: [roy@redhat.com] is not present in negative cache
	(2023-06-08 12:21:31): [nss] [cache_req_search_cache] (0x0400): CR #3: Looking up [roy@redhat.com] in cache
	(2023-06-08 12:21:31): [nss] [cache_req_search_send] (0x0400): CR #3: Object found, but needs to be refreshed.
	(2023-06-08 12:21:31): [nss] [cache_req_search_dp] (0x0400): CR #3: Looking up [roy@redhat.com] in data provider
	(2023-06-08 12:21:32): [nss] [cache_req_search_cache] (0x0400): CR #3: Looking up [roy@redhat.com] in cache
	(2023-06-08 12:21:32): [nss] [cache_req_search_ncache_filter] (0x0400): CR #3: This request type does not support filtering result by negative cache
	(2023-06-08 12:21:32): [nss] [cache_req_search_done] (0x0400): CR #3: Returning updated object [roy@redhat.com]
	(2023-06-08 12:21:32): [nss] [cache_req_create_and_add_result] (0x0400): CR #3: Found 39 entries in domain redhat.com <---------
	(2023-06-08 12:21:32): [nss] [cache_req_done] (0x0400): CR #3: Finished: Success

Moreover, if the initgroups call is taking time, then add ``debug_microseconds = true`` under the ``[$domain]`` section of the ``/etc/sssd/sssd.conf`` and try to check the details in ``sssd_nss.log`` and ``sssd_$domain.log`` where the initgroup call is taking time. In ''sssd_$domain_.log'', start checking from ``[BE_USER]``; it will show you if sssd can retrieve the user. After that, sssd will start processing the groups of the respective user, which can be seen in the ``[Initgroups]`` call in ``sssd_$domain.log``. By looking at this call, you will be able to confirm if the user lookup and processing of membership are done properly. Here you will be able to see where the lookup is taking time or if there is any failure. Also, we can look at ``ltrace -r`` this will tell us which library call is taking time. In the below example, sssd is spending 26 sec in ``getgrouplist()``.

.. code-block:: sssd-log

  0.000976 strrchr("id", '/')                                                                                 = nil
  ….
  0.000383 __printf_chk(1, 0x557407f39a3c, 0x55740813d0ba, 0)                                                 = 14
  0.000175 getpwuid(0x6be2724d, 14, 0x7f9996950860, 0)                                                        = 0x7f99969514e0
  0.000860 __printf_chk(1, 0x557407f39a2d, 0x557409bb81b0, 0)                                                 = 9
  0.000119 dcgettext(0, 0x557407f39a32, 5, 0x55740813d09a)                                                    = 0x557407f39a32
  0.000119 __printf_chk(1, 0x557407f39a32, 0x55740813d09a, 0)                                                 = 15
  0.000117 getgrgid(0x6be26a81, 15, 0x7f9996950860, 0)                                                        = 0x7f9996951340
  0.290352 __printf_chk(1, 0x557407f39a2d, 0x557409bb9780, 0)                                                 = 14
  0.000174 realloc(nil, 40)                                                                                   = 0x557409bb9b90
  26.000152 getgrouplist(0x557409bb85c0, 0x6be26a81, 0x557409bb9b90, 0x7ffc51b78934)                           = 0xffffffff
  6.450594 realloc(0x557409bb9b90, 360)

On a side note, we can try to reduce the time spent in id lookup to some extent by reducing the ``ldap_group_nesting_level`` to 0. The default value is 2. This will be valid if we have a large number of groups from nesting level 1, in which case reducing the nesting level will probably help.

Slow ssh/login
**************

In order to troubleshoot slow ssh, we should basically look at both ssh and sshd. We can enable ssh debugging or collect strace in order to check why ssh is slow. But here we will check from the sssd perspective if sssd is playing any role in slow ssh. In order to do that, we will first verify if the ``id`` lookup is slow because at the time of ssh, ``initgroup`` calls will be executed.
If the ``id`` lookup is fast, then we need to check the SSSD debug logs. Go to the ``/var/log/sssd/sssd_$domain.log`` search for ``PAM_AUTH`` section this is the first phase of authentication, and we need to validate if this has been passed properly or if we are noticing any issues here. As a common example, we often notice ``[krb5_child_timeout] (0x0040): Timeout for child [23514] reached`` this indicates the KDC server is responding very slowly due to some reason. One of them could be an issue with the firewall or a slow network. As a workaround, consider increasing the value of ``krb5_auth_timeout`` which is 6 seconds by default. For detail please refer to :doc:`errors`

Another common example is ``pam_id_timeout`` user group membership is set for processes during login time. Therefore, during PAM conversation, SSSD has to prefer precision over speed and contact the server for accurate information. However, a single login can span over multiple PAM requests as PAM processing is split into several stages – for example, there might be a request for authentication and a separate request for account check (HBAC). It’s not beneficial to contact the server separately for both requests, therefore we set a very short timeout for the PAM responder during which the requests will be answered from in-memory cache. The default value of 5 seconds might not be enough in cases where complex group memberships are populated on server and client side. The recommended value of this option is as long as a single un-cached login takes. Add ``pam_id_timeout = n `` under the ``[pam]`` section of the ``/etc/sssd/sssd.conf`` followed by a ``sssd`` restart.

With respect to ``id_provider = ad`` you could also notice ``sdap_async_sys_connect request failed: [110]: Connection timed out.`` sdap_async_sys_connect request failed occurs if sssd is not able to connect to the LDAP server within 6 seconds. This could be an issue with DNS or the network. Validate the DNS SRV records; if SRV records are not working, hardcoding the AD/LDAP server may help here. For example, if id_provider = ad is being used, then hardcoding of AD servers can be done as: add ``ad_server = ad1.example.com, ad2.example.com`` under the ``[$domain]`` section of the ``/etc/sssd/sssd.conf``. If the network is slow or ldap_network_timeout is reached, then consider increasing the value of ``ldap_network_timeout`` which is set to 6 seconds by default.

.. code-block:: sssd-log

      (Fri Apr 14 16:07:19 2023) [sssd[be[example.com]]] [sssd_async_socket_init_done] (0x0020): sdap_async_sys_connect request failed: [110]: Connection timed out.

If the ``PAM_AUTH`` section has passed successfully without any errors, then ``sssd`` jumps into the authorization section, i.e: ``PAM_ACC``. In this section, sssd checks for ``GPO`` access control or any other authorization set by the user. Example: ``simple_allow_groups``, ``simple_allow_user`` or ``access_filter``. Go to the ``/var/log/sssd/sssd_$domain.log`` section and search for ``PAM_ACC`` section and check if we notice any error or delay here. Sometimes we have noticed GPO processing is slow if the user has a very large policy.
