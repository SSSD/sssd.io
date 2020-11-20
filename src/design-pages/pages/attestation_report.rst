Generate an access control report for IPA domains
=================================================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/2840

Problem statement
-----------------
Some environments require, for auditing reasons, to generate an access
control report on the IPA client itself. While it can be argued that
generating these reports on the IPA servers instead would provide a nicer
experience, the audits requirement sometimes need a tool to be run on the
host.

Use cases
---------
As an owner of an IPA client I need to know which users have access to
this client. I want to run a tool on the host and get a report who can
access it.

The reports must contain information about HBAC rules. In future, SUDO
rules would be nice to have as well.

Overview of the solution
------------------------
A new ``sssctl`` command called ``access-report``. will be added. This
command will only be implemented for IPA domains for now, other domain
types will just return an error.

In this version, only a human-readable output will be provided.

Configuration changes
---------------------
None, only the new tool will be implemented.

Implementation details
----------------------
In order to trigger the refresh of rules by ``sssd_be`` process,
the Data Provider will be enhanced with a new sbus method
``org.freedesktop.sssd.DataProvider.AccessControl``.

This method will trigger the same async requests that PAM access phase
normally calls which fetch and save the IPA HBAC rules. This means that
the same rate-limiting with the ``ipa_hbac_refresh`` applies to this
request as if it was called via PAM access phase. Additionally, this
method will be exposed over the public D-Bus InfoPipe responder via a new
``RefreshAccessRules`` method. As with all methods, only root can call
it by default.

Finally, this new D-Bus method will be called from the ``sssctl
access-report`` command when it's ran in order to populate the ldb cache
with fresh HBAC rules

For printing the rules, the tool will simply call ``ldb_search``,
retrieve all objects of objectclass ``ipaHbacRule`` and then print the RDN
value of ``memberUser`` (for users and user groups), ``memberService``
(for services and service groups) and ``category``. By default, groups
will not be unrolled, because the ``getgrnam`` interface limits the group
nesting by default, therefore it is better to just print the group name,
not all the group members.

Future enhancements
-------------------
In future, the tool should also print the output in both human-readable
and machine-readable formats. For machine readable output, JSON is the
best choice, since the KCM responder already depends on ``libjansson.``
This enhancement is tracked in ticket `#3581 <https://pagure.io/SSSD/sssd/issue/3581>`_.

Additionally, for HBAC rules which are linked to a group, it might
be handy to unroll the group members and print them if the administrator
wishes. This enhancement is tracked with ticket `#3580 <https://pagure.io/SSSD/sssd/issue/3580>`_

How To Test
-----------
Run ``sssctl access-report`` on an IPA client with different HBAC rules
stored in the cache. Make sure all options produce the desired results.


How To Debug
------------
Debug messages will be added to the tool itself. To compare the output
with the cache contents, the ``ldbsearch`` tool can be used. The ``ipa``
administration tool can be used to display the server-side HBAC rules.

Authors
-------
    * Jakub Hrozek <jhrozek@redhat.com>
