Recognize trusted domains in AD provider
----------------------------------------

Related tickets:

-  `RFE Recognize trusted domains in AD
   provider <https://pagure.io/SSSD/sssd/issue/364>`__

Problem Statement
~~~~~~~~~~~~~~~~~

With the current LDAP lookups the SSSD AD provider can only find users
and groups in the local domain. With Global Catalog lookups (`Design
page <https://docs.pagure.org/SSSD.sssd/design_pages/global_catalog_lookups.html>`__)
this will be extended to all users and groups of the local forest. Using
the PAC helps to avoid group membership lookups (`RFE Use MS-PAC to
retrieve user's group
list <https://pagure.io/SSSD/sssd/issue/1558>`__).

What is missing are lookups of users and groups in trusted forests and
password based authentication of users from trusted forests. For this
the names of the trusted forests and additional suffixes managed by the
forest are needed. The names the

Overview view of the solution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

How to test
~~~~~~~~~~~

Author(s)
~~~~~~~~~

Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
