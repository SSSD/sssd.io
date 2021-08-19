Common LDAP Provider issues
###########################

* When running ``id user``, no groups are displayed.
* When running ``getent group $groupname``, no group members are displayed

  * In both cases, make sure the selected schema is correct. By default, SSSD will use the more common RFC 2307 schema. The difference between RFC 2307 and RFC 2307bis is the way which group membership is stored in the LDAP server. In an RFC 2307 server, group members are stored as the multi-valued attribute ``memberuid`` which contains the name of the users that are members. In an RFC2307bis server, group members are stored as the multi-valued attribute ``member`` (or sometimes ``uniqueMember``) which contains the DN of the user or group that is a member of this group. RFC2307bis allows nested groups to be maintained as well.
* If using the LDAP provider with Active Directory, the back end randomly goes offline and performs poorly.

  * Make sure the referrals are disabled. See the FAQ page for explanation. Also please consider migrating to the AD provider. The AD provider disabled referral support by default, so there's no need to disable referrals explicitly
* When enumeration is enabled, or when the underlying storage has issues, the ``sssd_be`` process is being killed by ``SIGTERM`` or even ``SIGKILL``

  * With huge directories, the ``sssd_be`` process takes a long time to store the entries to cache. The cache writes are blocking, so when ``sssd_be`` writes to the cache, it might be considered stuck (more on the actual mechanism below) You can increase the heartbeat interval by raising the value of the ``timeout`` option.
* For configuration with ``id_provider=ldap`` and ``auth_provider=ldap``. retrieving user information works, but authentication does not

  * Please note that user information is typically retrieved over unencrypted channel (unless ``ldap_id_use_start_tls`` is enabled), but authentication always happens over an encrypted channel. Checking for certificate errors should be the first step. To test authentication manually, you can perform a base-search against the user entry together with ldapsearch's ``-Z`` option.
