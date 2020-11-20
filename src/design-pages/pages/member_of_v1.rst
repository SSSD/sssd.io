Proposal to redesign the memberOf plugin (v1)
=============================================

Let us start with the following setup:

.. FIXME: This page is missing a image representing nestedgroups

::

    dn: name=Group A, cn=Groups, cn=default, cn=sysdb
    objectClass: group
    member: name=Group D, cn=Groups, cn=default, cn=sysdb
    member: name=User 1, cn=Users, cn=default, cn=sysdb
    member: name=User 2, cn=Users, cn=default, cn=sysdb
    member: name=User 3, cn=Users, cn=default, cn=sysdb
    member: name=User 4, cn=Users, cn=default, cn=sysdb
    member: name=User 5, cn=Users, cn=default, cn=sysdb
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb

    dn: name=Group B, cn=Groups, cn=default, cn=sysdb
    objectClass: group
    member: name=Group D, cn=Groups, cn=default, cn=sysdb
    member: name=User 1, cn=Users, cn=default, cn=sysdb
    member: name=User 2, cn=Users, cn=default, cn=sysdb
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb

    dn: name=Group C, cn=Groups, cn=default, cn=sysdb
    objectClass: group
    member: name=Group A, cn=Groups, cn=default, cn=sysdb
    member: name=Group B, cn=Groups, cn=default, cn=sysdb
    member: name=Group F, cn=Groups, cn=default, cn=sysdb
    member: name=User 3, cn=Users, cn=default, cn=sysdb

    dn: name=Group D, cn=Groups, cn=default, cn=sysdb
    objectClass: group
    member: name=User 4, cn=Users, cn=default, cn=sysdb
    memberOf: name=Group A, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group B, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb

    dn: name=Group E, cn=Groups, cn=default, cn=sysdb
    objectClass: group
    member: name=User 5, cn=Users, cn=default, cn=sysdb
    memberOf: name=Group B, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group F, cn=Groups, cn=default, cn=sysdb

    dn: name=Group F, cn=Groups, cn=default, cn=sysdb
    objectClass: group
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb


    dn: name=User 1, cn=Users, cn=default, cn=sysdb
    objectClass: user
    memberOf: name=Group A, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group B, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb

    dn: name=User 2, cn=Users, cn=default, cn=sysdb
    objectClass: user
    memberOf: name=Group A, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group B, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb

    dn: name=User 3, cn=Users, cn=default, cn=sysdb
    objectClass: user
    memberOf: name=Group A, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb

    dn: name=User 4, cn=Users, cn=default, cn=sysdb
    objectClass: user
    memberOf: name=Group A, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group B, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group D, cn=Groups, cn=default, cn=sysdb

    dn: name=User 5, cn=Users, cn=default, cn=sysdb
    objectClass: user
    memberOf: name=Group A, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group B, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group C, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group E, cn=Groups, cn=default, cn=sysdb
    memberOf: name=Group F, cn=Groups, cn=default, cn=sysdb

Actions
-------

Add new member to a group with no parents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We send an ldb message to add "User 4" to "Group C"

#. Check whether the member attribute matches the DN of Group C (it does
   not)
#. Examine "Group C" for memberOf attributes.
#. No memberOf attributes exist
#. Add memberOf(Group C) to "User 4"

Add new member to a group with parents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We send an ldb message to add "User 5" to "Group B"

#. Check whether the member attribute matches the DN of Group C (it does
   not)
#. Examine "Group B" for memberOf attributes.
#. "Group B" has memberOf attributes: "Group C"
#. Check whether any of these memberOf values match "User 5" (none do)
#. Add memberOf(Group B) and memberOf(Group C) to "User 4" and return

.. Add new group to a group with no parents (no loops)
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
..
.. .. |image0| image:: https://fedorahosted.org/sssd/raw-attachment/wiki/DesignDocs/MemberOfv2/nestedgroups.png
..    :target: https://fedorahosted.org/sssd/attachment/wiki/DesignDocs/MemberOfv2/nestedgroups.png
