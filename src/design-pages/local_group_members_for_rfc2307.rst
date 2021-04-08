Supporting Local Users as members of LDAP Groups for RRFc2307 servers
---------------------------------------------------------------------

Related Tickets:

-  `SSSD does not list local user's group membership defined in
   LDAP <https://pagure.io/SSSD/sssd/issue/1020>`__

Problem Statement
~~~~~~~~~~~~~~~~~

SSSD Has been built around the concept of self-contained Identity
Domains. Because of this all users of a domain must be present in the
domain itself to be available as members of the domain groups.

Historically identity providers like nss\_ldap has allowed to include
local users in remote LDAP servers that use the RFC2307 (not bis)
schema. With that schema group members are identified by the simple user
name. So if a user by the same name happened to exist on the local
workstation the LDAP group would end up being assigned to the user
during operations like initgroups.

This is technically a violation of the Identity domain and works mostly
by accident. However in order to keep compatibility with existing
deployments it has been requested to allow sssd to honor initgroups
request for local users that happen to be referenced in RFC2307 LDAP
servers.

Solution
~~~~~~~~

New Option
^^^^^^^^^^

We introduce a new boolean option named
ldap\_rfc2307\_fallback\_to\_local\_users This option enables or
disables the compatibility behavior. The option is set to 'false' by
default.

Behavior
^^^^^^^^

When the above option is enabled the LDAP provider will perform
additional local lookups for users only if the schema in use is RFC2307.
A simple getpwnam() or getpwuid() call is performed when looking up
users if the LDAP server returns no entry. If the a local user by the
same name or id exists it is stored in the cache like if it were an LDAP
user. The same is done for initgroups calls.

Details
^^^^^^^

Calls like initgroups will not fail anymore if the user is not found in
LDAP like they normally would do and groups this user 'belongs to' are
returned. The groups returned are the ones found in LDAP that have this
user's name in the memberUid attribute.

SSSD backends disable by default recursion from nsswitch calls into SSSD
itself. It is therefore safe to call functions like getpwnam() or
getpwuid() from within a backend. These functions will not enter the nss
client and will return all users from any other backend listed in
nsswitch.conf for the 'passwd' database.
