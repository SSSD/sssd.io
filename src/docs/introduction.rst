Introduction
============

SSSD stands for *System Security Services Daemon*, its the client piece
that allows Linux to authenticate to a variety of user directories
such as FreeIPA, 389, Microsoft Active Directory, 389DS, and other
directory servers.

So what does that mean exactly? Did you ever wonder how the same login
worked on all of the computers in the school lab? That’s because they
are joined to a domain that’s part of an identity management solution.
A centralized, redundant, and secure set of servers to manage users,
groups, policies, and more.

This isn’t necessary when you have a handful of machines to manage but
when scaled up to tens, hundreds, and thousands SSSD becomes an important
Linux directory-client component in place. You certainly can force the
new guy to go to each machine to create a user, update their password,
remove a user. However, that’s pretty mean and a waste of time when there
is a much easier way of doing things.

The community project FreeIPA *(Free Identity Policy and Auditing)* is
an Identity Management solution. It’s also known as Red Hat IdM, which
is the downstream name. FreeIPA, Red Hat IdM uses 389DS
*(Directory Server)* for its database.

Directory servers contain objects like a user object, that user object
contains user information stored in LDAP attributes and it is accessible
on the network the LDAP *(Lightweight Directory Access Protocol)*
network protocol.

*Please do not confuse LDAP with 389DS, 389DS is a directory server that
uses the LDAP protocol on port 389.*

Microsoft Windows Server implements a directory service named Microsoft
*ADDS* (Active Directory Domain Services), abbreviated as Microsoft AD.
AD is another identity management solution for Windows. It has
an LDAP server and shares many components with IPA. IPA and AD can have
a trust created between the domain domains. Why? Consider if there was a
company merger or acquisition. There won’t be a need to migrate users but
instead, set up a trust and allow Bob from industry giant "SSSD Corp" to
administer newly acquired small business "LDAP LLC".

It’s not uncommon for companies to have two departments, one that supports
and administers Linux and the other team manages Windows, so each will have
control over its own users and groups. Using SSSD’s ipa_provider,  AD domain
users can then log in to a host managed by IPA because of the established
trust between domains.

SSSD can authenticate directly to AD, using the ad_provider, and they’ll
be no need for IPA servers. Users and groups will be entirely managed by
AD. So why use indirect authentication? IPA is more flexible for managing
Linux hosts than AD since it can manage SUDO rules, SELinux users and
contexts, automount maps, and more. If all users are created in AD, but
the company has two IT teams. The Linux team may have to wait for users
to be created. Hopefully, you can start to see that each solution has its
pros and cons and will not be discussed in this introduction.

For more information about FreeIPA and other compatible directory servers,
please check out the following links.

- `FreeIPA <https://www.freeipa.org/page/Main_Page>`_
- `389DS <https://directory.fedoraproject.org/>`_
- `OpenLDAP <https://www.openldap.org/>`_
- `Kerberos <https://web.mit.edu/kerberos/>`_
- `Microsoft ADDS <https://www.microsoft.com/en-ie/windows-server>`_

The ad_provider and ipa_provider are just some providers that can be used
for authentication or authorization. Other providers is the ldap_provider,
krb_provider, proxy_provider, and local_provider. For more information please
check out the following MAN pages for more information.

- sssd-ldap
- sssd-krb5
- sssd-ipa
- sssd-ad
- sssd-files

What else is important to know about SSSD? We’ve discussed authentication,
verifying the user and that the correct password is being used. We have
not discussed if that user is **allowed** to login, this is what we mean by
authorization. Specific users and, or groups can be authorized to access
the host using centrally managed HBACs *(Host-Based Access Control)* or
filters in the SSSD configuration. For example, web admins don’t need
access to all the servers on the network and only need access to the
Apache and Nginx servers. This level of granular control can easily be
done. The ad_provider can use AD’s GPOs *(Group Policy Objects)* for HBACs.

In addition to access control, SSSD can lookup SUDO rules and roles to
control what users can do and when they can do them on the system. For
example, a web admin only needs access to stop, start, reboot the httpd
service and edit the httpd configuration file. Any failed attempt to
escalate their access will also be logged.

Alright, this sounds great, but what happens when if the directory server
is offline? Or you have a poor wireless signal on your laptop and keep on 
disconnecting? Do I need to log in with a local user? Absolutely not, SSSD
has a cache to improve performance after finding a user. The user’s
password is also stored, as long as the user has logged in before, they
will be able to login if SSSD when it’s unable to communicate to the servers.


Ready to get started? Check out our quick start guide here. :doc:`Quick Start
guide +<quick-start>`


