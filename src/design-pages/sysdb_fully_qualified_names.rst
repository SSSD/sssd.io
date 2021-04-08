Change format of SYSDB\_NAME attribute for users and groups
===========================================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2011 <https://pagure.io/SSSD/sssd/issue/2011>`__

Problem statement
~~~~~~~~~~~~~~~~~

Currently the "name" (SYSDB\_NAME) attribute for users and groups can be
stored in different formats depending on domain configuration, in
particular the ``full_name_format`` option. If the domain does not
require fully-qualified domain names (FQDN), the name in SYSDB\_NAME is
stored without the domain portion (for example ``joe``). If FQDN is
required in the domain, then the domain portion is stored in the
SYSDB\_NAME attribute (for example ``joe@example.com``). The format in
which the FQDN is stored is stored is also configurable in sssd.conf.

There are two major problems with this approach:

-  For admins - The format of data in sysdb is dependent on SSSD
   configuration. Changes in sssd.conf may render the cached data
   invalid, so admins have to remove the cache. In general, allowing an
   option that should purely control the output format to also control
   the database layout is a very bad idea.

-  For code maintainers - The code that deals with SYSDB\_NAME attribute
   often contains conditions and multiple branches to treat the
   FQDN/non-FQDN names differently. This makes the code less readable
   and more fragile.

In addition, some features such as using only the name part for
subdomain users are very hard to implement with the current code.

Use cases
~~~~~~~~~

As an Administrator, I would like an option to only output the short
names of trusted AD users without the domain component.

As an Administrator, I would like to change the output name format
without having the flush the whole database.

As a code maintainer, I need a predictable way to store user and group
entries without special casing the name formats.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

Always store SYSDB\_NAME attribute for users and groups in special
internal FQDN format that is not configuration dependent. The options
``use_fully_qualified_names`` and ``full_name_format`` should only be
relevant for code that prepares data for user output. Internally, only
the internal FQDN should be used.

Using a fully qualified name (as opposed to a non-qualified name) for
all users is better to make it possible to use the ``memberUid`` and
``ghost`` attributes in our ldb cache for cases where a group stores
members from multiple domains.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

The new internal FQDN will have the following format: ``name@domain``.
The name portion will retain the original case, while the domain portion
will be normalized as lower-case. The SYSDB\_ALIAS attribute will have
the same format, but lowercased. The database will not store the
shortname for users and groups at all, but the code would parse the
shortname if needed. This is acceptable because the shortname would only
be needed during interaction with outside of SSSD, such as creating
filters or during output.

The name that SSSD receives from the client libraries would be converted
to the internal format when a responder loops over a domain, much like
we normalize the case at the moment. The back end would receive the
qualified name as part of the ``be_req`` structure already and
internally would work with the qualified name only except places where
we need to use the name portion only (such as when constructing an LDAP
filter).

All functions that work with user and/or group names should be modified
to accept this format.

When working on the conversion, care must be taken to not tie the code
to any particular format, but always use functions to create or parse
the internal name. This could be tested by changing the functions to
create and parse the format to create the FQDN in a different format and
making sure all tests still pass.

A sysdb version upgrade will be necessary. The changes in sysdb will be
following:

-  Change the SYSDB\_NAME attribute for users and groups to use the new
   internal format.
-  Use the new internal format for SYSDB\_GHOST and SYSDB\_MEMBERUID
   attributes.
-  The member and memberof attributes will have to be changed to use the

sysdb upgrade
^^^^^^^^^^^^^

The sysdb upgrade is tricky for two reasons:

#. the amount of data we'll have to change and write can potentially be
   huge if the database contains many users and groups. To mitigate the
   performance impact, we will open the database in a nosync mode,
   perform all the writes at once and flush when we are done.
#. the memberof plugin normally prevents the ldb user to write the
   SYSDB\_MEMBERUID, SYSDB\_GHOST and SYSDB\_MEMBEROF attributes
   directly. Because there is no way to selectively disable one module
   when connecting to ldb, we will have to add a way to the memberof
   plugin to allow the user to bypass the module (maybe when an
   environment variable is set)

Additionally, because this update is risky, we should perform the update
on a copy of the database and only rename the copy when the upgrade
finishes successfully. This would allow the admin to downgrade sssd back
and still use the original database in the previous format.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

No configuration changes required, this is internal change only.

How To Test
~~~~~~~~~~~

All available tests should still pass. The tests should also pass if the
format of the database was changed.

Authors
~~~~~~~

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
-  Michal Židek <`mzidek@redhat.com <mailto:mzidek@redhat.com>`__>
