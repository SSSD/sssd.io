.. FIXME: Missing "sudo highlevel v2" image.

SUDO integration
****************

Cache format of SUDO rules
==========================

We have decided to use the current schema used by SUDO. The schema is
described
`here <http://www.gratisoft.us/sudo/man/1.8.2/sudoers.ldap.man.html>`__.

The reason is that Sudo can only understand the native schema anyway. We
will have to do a conversion when we implement support for the IPA sudo
schema down the road, but it's simply not needed now.

All rules are store under **cn=sudorules,cn=custom,cn=$domain,cn=sysdb**
subtree.

Communication protocols
=======================

SUDO -> Responder
-----------------

SUDO calls **SSS\_SUDO\_GET\_SUDORULES** command, providing a user name
of the requesting user. ::

    <username(char*)>

Responder -> SUDO
-----------------

Sends all sudo rules entries that contains keyword ALL or matches
requested user name, his groups or netgroups. ::

    <error_code(uint32_t)><num_rules(uint32_t)><rule1><rule2>...
    <ruleN> = <num_attrs(uint32_t)><attr1><attr2>...
    <attrN> = <name(char*)><num_values(uint32_t)><value1(char*)><value2(char*)>...

All strings are terminated with zero character.

If <error\_code> signals an error (i.e. it does not equal to
*SSS\_SUDO\_ERROR\_OK*), the remaining fields are omitted.
