SUDO Responder Cache Behaviour
==============================

Before we go into the caching its better to know some useful
information about sudo schema.

1. As the document at
   `http://www.gratisoft.us/sudo/man/1.8.1/sudoers.ldap.man.html <http://www.gratisoft.us/sudo/man/1.8.1/sudoers.ldap.man.html>`__
   indicates the sudo rules are contained in a ldap server inside
   the SUDOers container.

2. The SUDOers container contains the sudoRole objects.
   Where each object indicates a a sudorule.

3. Each sudoRole object supports following attributes:

    | **sudoUser** - A user name, uid (prefixed with '#'), UNIX group
      (prefixed with a '%') or user netgroup (prefixed with a '+').

    | **sudoHost** - A host name, IP address, IP network, or host
      netgroup (prefixed with a '+'). The special value ALL will match
      any host.

    | **sudoCommand** - A UNIX command with optional command line
      arguments and wild chars.

    | **sudoOption** – Specifies options to be enabled or disabled as in
      the sudoers file.

    | **sudoRunAsUser** - A user name or uid (prefixed with '#') that
      commands may be run as or a UNIX group (prefixed with a '%') or
      user netgroup (prefixed with a '+') that contains a list of users
      that commands may be run as. The special value ALL will match any
      user.

    | **sudoRunAsGroup** - A UNIX group or gid (prefixed with '#') that
      commands may be run as. The special value ALL will match any
      group.

    | **sudoNotBefore** - A time-stamp in the form yyyymmddHHMMZ that
      can be used to provide a start date/time for when the sudoRole
      will be valid. If multiplesudoNotBefore entries are present, the
      earliest is used. Note that timestamps must be in Coordinated
      Universal Time (UTC), not the local timezone.

    | **sudoNotAfter** - A time stamp in the form yyyymmddHHMMZ that
      indicates an expiration date/time,after which the sudoRole will no
      longer be valid. If multiplesudoNotBefore entries are present, the
      last one is used. Note that time-stamps must be in Coordinated
      Universal Time (UTC), not the local timezone

    **\*To use SudoNotBefore and SudoNotAfter the user should enable the
    SUDOERS\_TIMED option in the config file.**\ \*

    |   **sudoOrder** - The sudoRole entries retrieved from the LDAP
        directory have no inherent order. The sudoOrder attribute is an
        integer (or floating point value for LDAP servers that support
        it) that is used to sort the matching entries. This allows
        LDAP-based sudoers entries to more closely mimic the behaviour
        of the sudoers file, where the of the entries influences the
        result. If multiple entries match, the entry with the highest
        sudoOrder attribute is chosen.

    **\*A sudoRole must contain at least one sudoUser, sudoHost and
    sudoCommand.**\ \*

4. The sudoRole that have ``'''cn=Defaults'''`` will be applied
   (if specified) over all the rules before applying any other
   rules. This mimics the default statements in the sudoers file.

Now we have the necessary information to move on.

Q1). **What should we cache for offline sudo authentication???**

    The anatomy of sudo is as follows:

    when you type 'sudo cmd' sudo is going to lookup in ldap to try and
    find the user POSIX groups and the user/host Nisnetgroup where the
    user is a member. Then it is going to do an ldap search in the
    ou=SUDOers container looking for any rule that matches that user or
    his usergroups. when it matches some rules, it goes down that list
    to see if the hostname OR a netgroup that the host is a member of is
    in that same rule, then finally it determines if the command 'less'
    is allowed.

    This is how it works in a ldap server client. But in order to
    incorporate the netgroups we have to do some hack in the order of
    this anatomy.

    For the successful validation we need to know the nisnetgroups and
    POSIX groups that a user/host is a member of. So that we need to
    cache the host/user-> nisgroup and user->posixgroups along with all
    sudoRole objects inside the SUDOers container that references to the
    specified command.

    The simple solution for this problem is to enumerate all groups and
    netgroup information and check it with sudorules. But this approach
    less efficient and costly. Instead of enumerating all the rules, the
    procedure goes like this.

    - First we need to find the groups and user/host netgroups in which
      the user is a member of. That is the first step. We can do the
      search in DN: cn=accounts,dc=example,dc=com. Here we can use
      memberof plugin to resolve the user groups and the host groups. This
      step is already implemented inside the sssd. In order to include the
      support for NIS net groups we can add one more filter to the query
      that searches for the user groups. The query is ::

        (|
           (nisNetgroupTriple=\28*,username,*\29)
           (nisNetgroupTriple=\28hostname,*,*\29)
        )

      This will give you the netgroup that the user/host is a member of.

    - In the second phase we apply the search to filter the rules
      that applies to the user/host POSIX groups and netgroups found
      in step1. Search returns ::

        (\|(sudoBaseCommand=cmd)(sudoCommand=ALL)) where the
        sudoBaseCommand is JUST the command (not including args).

      The skeleton of the filter will be: ::

        (&
            (objectClass=sudoRole)
            (|
                (sudoUser=username)
                (sudoUser=#uid)
                (sudoUser=%usergroup1)
                (sudoUser=%usergroupN)
                (sudoUser=+userNetgroup1)
                (sudoUser=+userNetgroupN)
                (sudoUser=ALL)
            )
            (|
                (sudoHost=ipa.example.com)
                (sudoHost=+sample_host_group)
                (sudoHost=ALL)
            )
            (|
                (sudoBaseCommand=!cmd*)
                (sudoCommand=ALL)
            )
         )

    - From these rules the evaluation is done.

    **Performance Considerations**

    1. Within a sudoRole, The sudoCommand attribute with an command
       negation is executed first, then sudoCommand with exact command
       is evaluated, at last the sudoCommands with 'all' is evaluated.
    2. To incorporate the sudoOrder attribute we can do the sorting
       AFTER our search filter. So we'll limit the number of rules to
       sort first.

Q2) **How to store cached data?**
    The cached data is in the LDAP format.
    So that the simple option available is to store it in the ldb file.
