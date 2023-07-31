Performance tuning SSSD
#######################

Slow id lookup
**************
This has been noticed id lookup become slow if the LDAP/AD user is a member of large groups say for example user is a member of 300+ groups. ``id`` is very heavy. ``id`` does a lot under its hood.
Behind the scenes, when the 'id $user' command is executed it triggers the following:

- Get user information - getpwnam() for the user

- Get primary group information - getgrgid() for the primary group of the user

- Get list of groups - getgrouplist() for the user

- Get group information for each group returned from step 3 - getgrid() for all GIDs returned from getgrouplist() call.

We need to identify out of the above 4 steps which step is actually slow. In order to collect detailed infromation we need to add ``debug_level = 9`` under the ``[$domain]`` section of the ``/etc/sssd/sssd.conf`` followed by a ``sssd`` restart. We often noticed step 4 is the step where sssd takes most of its time because the most data-intensive operation is downloading the groups including their members and by default this feature is enabled we can turn this off by setting ``ignore_group_members = true``. 
Usually, we are interested in what groups a user is a member of (id aduser@ad_domain) as the initial step rather than what members do specific groups include (getent group adgroup@ad_domain). Setting the ignore_group_members option to True makes all groups appear as empty, thus downloading only information about the group objects themselves and not their members, providing a significant performance boost. Please note that id aduser@ad_domain would still return all the correct groups.

- Pros: getgrnam/getgrgid calls are significantly faster.
- Cons: getgrnam/getgrgid calls only return the group information, not the members

**WARNING! If the compat tree is used, DO NOT SET ignore_group_members = true because it breaks the compatibility logic.
