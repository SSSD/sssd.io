User Account Management Consolidation
-------------------------------------

Related ticket(s):

-  N/A

The following proposal is the result of the understanding reached at the
February 22nd, 2013 meeting held at the Red Hat offices in Brno.

Problem Statement
~~~~~~~~~~~~~~~~~

User management is currently fragmented throughout our system. The only
unifying interface is nsswitch, provided by glibc. However, this
interface is minimal, provides only POSIX information and is a querying
interface only.

An interface used for limited editing of account data is provided
through libuser. This library can be used to modify data in local files
or LDAP servers. However the libuser interface is not generic and does
not allow to dynamically select the target database nor add additional
user data.

Desktop tools augment user information by storing additional data in a
separate database.

Legacy aspects of user management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Local files
^^^^^^^^^^^

Even today, many tools may still have direct dependencies on the files
even tough the
`nsswitch <https://www.gnu.org/software/libc/manual/html_node/Name-Service-Switch.html>`__
interface has been around for a long time. Also some administrators are
used to vipw password files or use scripts that directly manipulate
them. For these reasons it is not advisable to stop using the
traditional files for local accounts completely.

The only option to augment the files with non-POSIX information is to
access them through a common interface and store additional information
in a separate database. Legacy files would still remain authoritative.

Managing remote accounts
^^^^^^^^^^^^^^^^^^^^^^^^

For accessing remote information, nsswitch became the de facto standard.
Red Hat is standardizing on the SSSD daemon for accessing remote user
information and perform authentication for remote users.

Remote directories often provide more flexibility, so additional data
will pushed there when possible. However in some cases additional
information may need to be stored locally if the remote server can't
hold it. The directory remains authoritative.

Unified interface through SSSD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The proposal is to leverage SSSD to unify account management. The pros
and cons of this approach are listed below:

-  Pros:

   -  Provides all the infrastructure needed to cache remote data and to
      store locally additional information.
   -  SSSD's database is easily extensible (LDAP -like)
   -  Already provide PAM and nsswitch interfaces

-  Cons:

   -  Misses an interface to directly manage users, however already has
      infrastructure in place to make it easy to build this interface.

Changing authentication and user lookup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The system will continue to use the classic PAM and nsswitch interfaces
for authentication and account lookups.

However we will probably change the PAM stack to try pam\_sss before
pam\_unix so that sssd is consulted first and pam\_unix is only used as
a fallback to directly access files.

Similarly for the nsswitch interface we will probably switch passwd and
group (and potentially other) database to use the sss target first and
only later fall back to the files target

Action Items
~~~~~~~~~~~~

-  Develop dbus interface specification to satisfy desktop requirements
   (design doc for SSSD)
-  Open tickets in SSSD to:

   -  Build Files provider in SSSD
   -  Build Rich API/dbus responder
   -  Insure additional information pins cache contents

-  Modify libuser to become a compatibility layer on top of the Rich
   API/dbus responder
-  Test and implement Root only access to files, and channel all access
   through sssd

   -  Needed for OpenShift and similar containerized envs.

Authors
~~~~~~~

-  Simo Sorce <`ssorce@redhat.com <mailto:ssorce@redhat.com>`__>
