Common AD Provider issues
#########################

* How do I set up the AD provider?

  * There is a dedicated page about AD provider setup

* Many users can't be displayed at all with ID mapping enabled and SSSD domain logs contain error message such as:

    .. code-block:: sssd-log

        [sdap_idmap_sid_to_unix] (0x0080): Could not convert objectSID [S-1-5-21-101891098-1139187330-4192773280-XXXXXX]

    * If you are running an old (older than 1.13) version and XXXXXX is a number larger than 200000, then check the ``ldap_idmap_range_size`` option. You'll likely want to increase its value. Keep in mind the largest ID value on a POSIX system is 2^32.

    * If you are running a more recent version, check that the ``subdomains_provider`` is set to ``ad`` (which is the default). Some users are setting the ``subdomains_provider`` to ``none`` to work around fail over issues, but this also causes the primary domain SID to be not read and therefore cannot map SIDs from the primary domain. Consider using the ``ad_enabled_domains`` option instead!

* The POSIX attributes disappear randomly after login

  * SSSD looks the user's group membership in the Global Catalog to make sure even the cross-domain memberships are taken into account. Chances are the POSIX attributes are not replicated to the Global Catalog. You can disable the Global catalog lookups by disabling the ``ad_enable_gc`` option, but you'll lose cross-domain memberships. Alternatively, modify the AD schema to replicate the POSIX attribute to the Global Catalog.

* After selecting a custom ``ldap_search_base``, the group membership no longer displays correctly.

  * If you use a non-standard LDAP search bases, please disable the TokenGroups performance enhancement by setting ``ldap_use_tokengroups=False``. Otherwise, the AD provider would receive the group membership via a special call that is not restricted by the custom search base which causes unpredictable results
  * Typically, users configure a custom ``ldap_search_base`` to limit the groups the user is a member of. Please see `this blog post <https://jhrozek.wordpress.com/2016/12/09/restrict-the-set-of-groups-the-user-is-a-member-of-with-sssd/) for more information on the subject>`_.

* SSSD keeps connecting to a trusted domain that is not reachable and the whole daemon switches to offline mode as a result

  * SSSD would connect to the forest root in order to discover all subdomains in the forest in case the SSSD client is enrolled with a member of the forest, not the forest root. This is because only the forest root knows all the subdomains, the forest member only knows about itself and the forest root. Also, SSSD by default tries to resolve all groups the user is a member of, from all domains. In case the SSSD client is behind a firewall preventing connection to a trusted domain, can set the ``ad_enabled_domains`` option to selectively enable only the reachable domains.

* SSSD keeps switching to offline mode with a ``DEBUG`` message saying ``Service resolving timeout reached``

  * This might happen if the service resolution reaches the configured time out before SSSD is able to perform all the steps needed for service resolution in a complex AD forest, such as locating the site or cycling over unreachable DCs. Please check the ``FAILOVER`` section in the man pages Often, increasing the ``dns_resolver_timeout`` option helps to allow more time for the service discovery.

* A group my user is a member of doesn't display in the ``id`` output

  * Cases like this are best debugged from an empty cache. Check if the group GID appears in the output of ``id -G`` first. In case the group is not present in the ``id -G`` output at all, there is something up with the initgroups part. Check the schema and look for anything strange during the initgr operation in SSSD back end logs. If the group is present in ``id -G`` output but not in ``id`` output (or a subsequent id output) then there's something wrong with resolving the group GIDs with ``getgrgid()``.
