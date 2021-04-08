Proposal to redesign the memberOf plugin (v2)
=============================================

Let us start with the following setup:

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
