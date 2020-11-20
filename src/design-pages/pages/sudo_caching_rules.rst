SUDO caching rules
******************

Important sudo attributes
=========================

-  **sudoHost** - to what host does the rule apply

   -  *ALL* - all hostnames
   -  *hostname*
   -  *IP address*
   -  *+netgroup*
   -  *regular expression* - contains one of "\\?\*[]"

-  **sudoUser** - to what user does the rule apply

   -  *username*
   -  *#uid*
   -  *%group*
   -  *+netgroup*

-  **sudoOrder** - rules ordering
-  **sudoNotBefore** and **sudoNotAfter** - time constraints

Complete LDAP schema can be found
`here <http://www.gratisoft.us/sudo/man/1.8.4/sudoers.ldap.man.html>`__.

Common
======

Per host update
---------------

Per host update returns all rules that:

-  sudoHost equals to ALL
-  direct match with sudoHost (by hostname or address)
-  contains regular expression (will be filtered by sudo)
-  contains netgroup (will be filtered by sudo)

Hostname match is performed in sudo source in
*plugin/sudoers/ldap.c/sudo\_ldap\_check\_host()*.

Per user update
---------------

Per user update returns all rules that:

-  sudoUser equals to ALL
-  direct match with username, #uid or %group names
-  contains +netgroup (will be filtered by sudo)

Username match is performed via LADP filter in sudo source in
*plugin/sudoers/ldap.c/sudo\_ldap\_result\_get()*.

Smart refresh
-------------

Download only rules that were modified or newly created since the last
refresh.

Implementation
==============

We will be looking for modified and newly created rules in short
intervals. Expiration of the rules is handled per user during the
execution time of *sudo*. We will also do periodical full refresh to
ensure consistency even if the *sudo* command is not used.

SysDB attributes
----------------

| **sudoLastSmartRefreshTime** on *ou=SUDOers* - when the last smart
  refresh was performed
| **sudoLastFullRefreshTime** on *ou=SUDOers* - when the last full
  refresh was performed
| **sudoNextFullRefreshTime** on *ou=SUDOers* - when the next full is
  scheduled
| **dataExpireTimestamp** on each rule - when the rule will be
  considered as expired

Data provider
-------------

Data provider will be performing following actions:

A. Periodical download of changed or newly created rules (per host smart refresh)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Interval is configurable via
  **ldap\_sudo\_changed\_refresh\_interval** (default: 15 minutes)
| Enable *modifyTimestamp* with
  **ldap\_sudo\_modify\_timestamp\_enabled** (default: false)

#. **if** server has changed **then** do **C**
#. **else if** *entryUSN* is available **then**

   #. refresh rules per host, where entryUSN > currentHighestUSN
   #. **goto** 3.2.

#. **else if** *modifyTimestamp* is enabled **then**

   #. refresh rules per host, where entryUSN > currentHighestUSN
   #. *sudoLastSmartRefreshTime* := current time
   #. nextrefresh := (current time +
      *ldap\_sudo\_changed\_refresh\_interval*)
   #. **if** nextrefresh >= *sudoNextFullRefreshTime* AND nextrefresh <
      (*sudoNextFullRefreshTime* +
      *ldap\_sudo\_changed\_refresh\_interval*) **then**

      #. nextrefresh := (*sudoNextFullRefreshTime* +
         *ldap\_sudo\_changed\_refresh\_interval*)

   #. schedule next smart refresh

#. **else** do nothing

B. Periodical full refresh of all rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configurable via **ldap\_sudo\_full\_refresh\_interval** (default: 360
minutes)

#. do **C**
#. *sudoLastFullRefreshTime* := current time
#. *sudoNextFullRefreshTime* := (current time +
   *ldap\_sudo\_full\_refresh\_interval*)
#. schedule next full refresh

C. On demand full refresh of all rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Download all rules per host
#. Deletes all rules from the sysdb
#. Store downloaded rule in the sysdb

D. On demand refresh of specific rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Download the rules
#. Delete them from the sysdb
#. Store downloaded rule in the sysdb

Responder
---------

**sudo\_timed** (default: false) - filter rules by time constraints?

#. search sysdb per user
#. refresh all expired rules
#. **if** any rule was deleted **then**

   #. schedule **C** (out of band)
   #. search sysdb per user

#. **if** *sudo\_timed* = false **then** filter rules by time
   constraints
#. sort rules
#. return rules to sudo

Questions
=========

#. Should we also do per user smart updates when the user runs *sudo*?
#. Should we create a tool to force full refresh of the rules
   immediately?
