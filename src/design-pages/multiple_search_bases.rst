Multiple LDAP search bases support
==================================

Purpose
-------

Some deployments use search bases to limit or extend the set of users
and groups visible to a system.

One common example is for applications granting access only to users in
a hard-coded group name. In this case, the group search base would
generally be set differently for each machine running this application.
Other machines running the same application providing access to other
users would receive a different "view" of LDAP through the use of search
bases.

Expected Behaviour
------------------

Individual Lookups
~~~~~~~~~~~~~~~~~~

For targeted lookups (e.g. ``getpwuid()``, ``getgrnam()``) we should try
each of the search bases in order until one of them returns the entry we
are looking for, or we have exhausted all of the search bases. Each
search will be performed with the search scope provided.

Enumeration
~~~~~~~~~~~

For enumeration, we will need to iterate through ALL search bases to
retrieve users, groups, etc. For each search base, we need to examine
each entry retrieved and compare it against the entries received from
earlier search bases. If there are conflicts, we will discard the
conflicting value from the later search base. (Therefore the entry in
the earlier search bases will always win.

Implementation
--------------

We will extend the ``ldap_*_search_base`` options to support behavior
similar to that of ``nss_base_passwd`` and ``nss_base_group`` from
nss-ldapd.

The standard search base (``ldap_search_base`` will be left alone as a
single value with scope "subtree".

The new ``ldap_*_search_base`` options will include a new delimiter,
'``?``'. If this is present, we will divide the string up into triples
as follows: ::

    search_base?scope?filter[?search_base?scope?filter...]

Parsing
~~~~~~~

We will split the input string on the '?' delimiter. If the resulting
array is exactly one, or is a multiple of three, we will continue.
Otherwise it will fail validation.

The scope must be one of 'subtree', 'onelevel' or 'base'
(case-insensitive).

The filter will be optional and may be a zero-length string. The filter
must be pre-sanitized and must pass filter validation with
``ldb_parse_tree()``
