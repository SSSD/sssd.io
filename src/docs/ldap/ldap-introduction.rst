Introduction to LDAP
####################

`LDAP`_ (Lightweight Directory Access Protocol) is a protocol that is used to
communicate with directory servers. Directory is a sort of a database that is
used heavily for identity management use cases. The terms "LDAP", "LDAP
database" and "directory server" are usually used interchangeably.

Unlike relational SQL databases, the LDAP database is not organized into tables,
rows and columns but it is organized into a hierarchical directory structure --
into containers, entries and attributes.

.. note::

    Examples of LDAP servers that are often used in Linux environments are
    `OpenLDAP`_ and `389ds`_.

SSSD and LDAP integration
*************************

SSSD can connect to any LDAP server to lookup POSIX accounts and other
information such as sudo rules and autofs maps using an SSSD LDAP provider. It
also provides various mechanisms of access controls and password policies. LDAP
provider features include (but they are not limited to):

* SASL/SSL/TLS support
* LDAP service auto discovery
* Limit search behavior using multiple search bases
* Password changing and password policy support
* RFC2307 and RFC2307bis support
* POSIX users and groups support
* sudo rules support
* autofs maps support
* LDAP-based access control
* Simple access control

.. seealso::

    To read more about how SSSD is used in LDAP integration at a high level, refer to the following links:

        * `Understanding SSSD and its benefits <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel>`_
        * `Configuring SSSD to use LDAP and require TLS authentication <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/configuring-sssd-to-use-ldap-and-require-tls-authentication_configuring-authentication-and-authorization-in-rhel>`_

LDAP Basics
***********

The rest of the page is dedicated to readers that are not yet familiar with
directory servers. It explains the very basics that will help you dive into the
LDAP world. Please lookup and visit external resources such as `ldap.com
<https://ldap.com>`__ to gain more thorough information.

Directory structure
*******************

Each directory entry consists of a *distinguished name*, *object class* and
*attributes*.

Distinguished name (DN)
    The distinguished name is a unique name that identifies the object in the
    database. It is created out of set of attributes that have unique value to
    the object (also called relative distinguished name or RDN) and the parent's
    DN. It basically resembles a hierarchical path to the entry (for example.
    ``name=John,cn=users,dc=mydomain`` where ``name`` is the entry's attribute
    with unique value and ``cn=users,dc=mydomain`` is the parent's DN.

Object class (OC)
    An object class is a special attribute that specifies what mandatory and
    optional attributes can be set on the entry. Object classes are defined in
    schemas that are installed on the LDAP server.

Attributes
    Attributes are single or multi-valued properties of the entry. Their format
    and functions (e.g. date, string, case sensitiveness, comparison schema,
    limits, etc.) are defined by schema and object classes. Some standard and
    common attributes are:

    * **dc**: domain component -- used to identify the directory domain
    * **ou**: organizational unit -- used to split entries into named containers
    * **cn**: canonical name -- used to provide name to an object

LDIF
====

Directory entries can be exported into an `LDIF`_ (LDAP Data Interchange Format)
format which is a text representation of the directory contents. Here is a
simple example:

.. code-block:: text

    dn: dc=ldap,dc=vm
    objectClass: domain
    objectClass: top
    dc: ldap

    dn: ou=users,dc=ldap,dc=vm
    objectClass: organizationalUnit
    objectClass: top
    ou: users

    dn: cn=user-1,ou=users,dc=ldap,dc=vm
    objectClass: posixAccount
    objectClass: top
    cn: user-1
    gidNumber: 10001
    homeDirectory: /home/user-1
    uid: user-1
    uidNumber: 10001
    userPassword: {SHA}98O8HYCOBHMq32eZZczDTKeuNEE=

This represents the following entries:

.. mermaid::

    graph LR
        dc(dc=ldap,dc=vm)
        ou(ou=users)
        cn(cn=user-1)

        dc --> ou --> cn

Filtering LDAP entries
======================

LDAP filters are expressed using a tree that consist of attribute-value pairs
and operators. The whole tree is then collapsed using parentheses. The filters
are well explained `here <https://ldap.com/ldap-filters>`__ and `here
<http://www.ldapexplorer.com/en/manual/109010000-ldap-filter-syntax.htm>`__, but
here is an example for a quick introduction and basic idea. The following filter
will search for all objects that have ``objectClass`` equal to ``posixAccount``
and canonical name set either to John or Alice. The filter also requires that an
``uidNumber`` attribute is set (it may have any arbitrary value but it must have
a value).

.. code-block:: text

    (&(objectClass=posixAccount)(uidNumber=*)(|(cn=John)(cn=Alice)))

We can also expand this filter into an indented tree so the operators and their
operands can be easily understood.

.. code-block:: text

    (&
        (objectClass=posixAccount)
        (uidNumber=*)
        (|
            (cn=John)
            (cn=Alice)
        )
    )

Scope and search base
=====================

When querying LDAP, we usually also specify a search base and scope which tells
the server from which object and how far in the hierarchy it should start
searching. A search base is simply a DN, scope can be one of ``base``,
``subtree`` or ``onelevel``.

base
    The search base itself it matched against the filter. If the filter matches,
    the search base entry is returned. Otherwise an empty result is returned.

subtree
    All entries below the search base are filtered.

onelevel
    Similar to ``subtree`` but only one level below the search base is searched.


Tools
=====

You can use OpenLDAP tools to work with an LDAP server. Especially
``ldapsearch``, ``ldapadd``, ``ldapdelete`` and ``ldapmodify``. To install
these tools, run:

.. code-tabs::

    .. fedora-tab::

        dnf install openldap-clients

    .. rhel-tab::

        yum install openldap-clients

    .. ubuntu-tab::

        apt install slapd ldap-utils

The following code shows an example of looking up an entry using the filter
above and a simple bind with a combination of account and password:

.. code-block::

    ldapsearch -x -D "cn=Directory Manager" -w "$password" -H ldap://ldap.example.com -b dc=example,dc=com -s sub '(&(objectClass=posixAccount)(uidNumber=*)(|(cn=John)(cn=Alice)))'

You can also choose from a variety of graphical LDAP tools such as the `Apache
Directory Studio`_.

.. _LDAP: https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol
.. _LDIF: https://en.wikipedia.org/wiki/LDAP_Data_Interchange_Format
.. _OpenLDAP: https://www.openldap.org/
.. _389ds: https://directory.fedoraproject.org/
.. _Apache Directory Studio: https://directory.apache.org/studio
