IPA sudo schema support
=======================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/1108 <https://pagure.io/SSSD/sssd/issue/1108>`__

Related design document(s)

-  `https://docs.pagure.org/SSSD.sssd/design_pages/sudo_caching_rules <https://docs.pagure.org/SSSD.sssd/design_pages/sudo_caching_rules.html>`__

Problem statement
-----------------

SSSD supports only standard sudo ldap schema at the moment. This has a
drawback of having the need to run compat plugin that converts IPA sudo
schema into the standard one. Once SSSD has support for IPA schema
administrators administrators can disable sudo compat tree which will
result in performance improvement on server side.

Use cases
---------

-  compat plugin may be disabled when using IPA sudo provider

IPA sudo schema
---------------

IPA sudo schema is rather different than the standard one. This section
contains the description of this schema together with ldap containers
where sudo rules are stored. A relevant standard attribute is noted when
possible. **RDN is marked in bold**. Attributes that hold dn are marked
in italic.

cn=sudocmds,cn=sudo,$dc
^^^^^^^^^^^^^^^^^^^^^^^

This container contains definition of single commands that may be
present in sudo rules.

-  objectClass = ipasudocmd
-  **ipaUniqueID**
-  sudoCmd ~ sudoCommand
-  *memberOf* (dn of sudo command group)

cn=sudocmdgroups,cn=sudo,$dc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This container contains definition of command groups that may be present
in sudo rules.

-  objectClass = ipasudocmdgroup
-  ipaUniqueID
-  **cn**
-  *member* (dn of sudo command)

cn=sudorules,cn=sudo,$dc
^^^^^^^^^^^^^^^^^^^^^^^^

This container contains definition of sudo rules.

-  objectClass = ipasudorule
-  **ipaUniqueID**
-  cn
-  ipaEnabledFlag

-  ipaSudoOpt ~ sudoOption
-  *ipaSudoRunAs* ~ sudoRunAsUser (dn of user or group of users)
-  *ipaSudoRunAsGroup* ~ sudoRunAsGroup (dn of group)
-  *memberAllowCmd* (dn of sudo command or command group)
-  *memberDenyCmd* (dn of sudo command or command group)
-  *memberHost* ~ sudoHost (dn of ipa enrolled machine or hostgroup)
-  *memberUser* ~ sudoUser (dn of user or group of users)
-  hostMask (ip/mask)
-  *sudoNotAfter* ~ sudoNotAfter
-  *sudoNotBefore* ~ sudoNotBefore
-  *sudoOption* ~ sudoOption

The following attributes have a special meaning and can contain only
value "all". For example if cmdCategory is present, it is equivalent to
sudoCommand=ALL.

-  cmdCategory ~ sudoCommand
-  hostCategory ~ sudoHost
-  ipaSudoRunAsGroupCategory ~ sudoRunAsGroup
-  ipaSudoRunAsUserCategory ~ sudoRunAsUser
-  userCategory ~ sudoUser

The following attributes are used to contain external objects not known
to IPA nor SSSD. Since SSSD by design provides rules only to users and
groups known to it, we can safely ignore those attributes.

-  externalHost
-  externalUser
-  ipaSudoRunAsExtGroup
-  ipaSudoRunAsExtUser

Overview of the solution
------------------------

We will again use rules, smart and full refresh similar to what we do in
ldap provider. Since we are working with three containers, it is not
very simply to translate everything at once into current standard sudo
schema that we use inside SSSD, because it would make changes in
commands and command groups hard to propagate. Instead we will keep
command and command groups stored separately and translate it into
sudoCommand in responder on the fly.

We will take advantage of using an IPA server and translate dn into
names by parsing dn when possible.

Implementation details
----------------------

Full refresh
^^^^^^^^^^^^

-  download everything under cn=sudo,$dc that applies to this host
-  store only commands and command groups that are present in at least
   one rule
-  convert what possible to sudo schema but leave references to commands
   and command groups for further processing in responder

Smart refresh
^^^^^^^^^^^^^

-  download everything under cn=sudo,$dc that applies to this host newer
   than last USN value
-  if new command or command group is downloaded store it only if it is
   present in changed rule
-  if a rule contains command or command group that is not yet present
   in sysdb, fetch it with dereference or single lookup

Rules refresh
^^^^^^^^^^^^^

-  refresh expired rules and commands and command groups that are
   present in those rules

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

No new options. But we have to provide a way to distinguish between
usage of IPA and ldap schema. By default we will use IPA schema and if
ldap\_sudo\_search\_base is set to anything else then cn=sudo,$dc we
will use the standard sudo ldap schema.

How To Test
~~~~~~~~~~~

-  existing tests can be used, only switching ldap server for IPA

Authors
~~~~~~~

-  Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
