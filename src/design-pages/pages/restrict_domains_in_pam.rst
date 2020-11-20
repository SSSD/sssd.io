Restricting the domains a PAM service can auth against
======================================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/1021 <https://pagure.io/SSSD/sssd/issue/1021>`__

Problem statement
~~~~~~~~~~~~~~~~~

Some environments require that different PAM applications can use a
different set of SSSD domains. The legacy PAM modules, such as
``pam_ldap`` were able to use a different configuration file altogether
as a parameter for the PAM module. This wiki page describes a similar
feature for the SSSD.

Use case
~~~~~~~~

An example use-case is an environment that allows external users to
authenticate to an FTP server. This server is running as a separate
non-privileged user and should only be able to authenticate to a
selected SSSD domain, separate from the internal company accounts. The
administrator is able to leverage this new feature to mark allow the FTP
user to only authenticate against one of the domains in the FTP PAM
config file.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

On the PAM client side, the PAM module should receive a new option that
specifies the SSSD domains to authenticate against. However, the SSSD
daemon can't fully trust all PAM services. We can't rely on the PAM
service fields either, as the data the PAM client sends to the PAM
application can be faked by the client, especially by users who posses
shell access or can start custom applications. Instead, there needs to
be a list of users who we trust. Typically, this would be a list of
users who run the PAM aware applications we wish to restrict (such as
``vsftpd`` or ``openvpn``). This list would default to ``root`` only.

These trusted users would be allowed to authenticate against any domain
and would also be able to restrict the domains further using a new
pam\_sss option. For the untrusted users, we need to keep a list of
domains allowed to authenticate against, too. Since by default there are
no restrictions on the allowed domains, this list would default to "all
domains are allowed".

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

This section breaks down the Overview of the solution into consumable
pieces.

Add a new option ``pam_trusted_users``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A new option must be added to the PAM responder. This option will be a
list of numerical UIDs or group names that are trusted or a special
keyword "ALL". This list will be parsed during PAM responder
initialization (``pam_process_init`` call) using the
``csv_string_to_uid_array`` function and stored in the PAM responder
context (``struct pam_ctx``). The PAC responder does pretty much the
same in the ``pac_process_init`` function.

In the responder, we already have the credentials of the client stored
in the ``cli_ctx`` structure. When a new request comes into the
``pam_forwarder`` function, we will match the client UID against the
list of trusted IDs and determine whether the client is trusted or not.

The default will be the special keyword ALL, meaning all users are
trusted. This is in line with the current behaviour where any user can
access any domain.

Add a option to limit the domains for untrusted users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another option, called ``pam_allowed_auth_domains`` shall be added to
the PAM responder. This option will list the SSSD domains an untrusted
client can authenticate against. The option will accept either a
comma-separated list of SSSD domains or any of two special values
``all`` and ``none``. The default value will be ``none`` to make sure
the administrator is required to spell out the domains that can be
contacted by an untrusted client when he starts differentiating trusted
and untrusted domains.

The option will be parsed during ``pam_process_init`` and stored in the
``pam_ctx`` structure. An untrusted client will only be allowed to send
a request to a domain that matches the list of allowed domains.

In order to keep the implementation simple, the ``all`` keyword would
copy all domain names into ``pam_ctx`` and the ``none`` keyword would
set the variable holding the names to NULL. Then the check would be a
simple loop for all cases.

Care must be taken to ensure a sensible PAM error code for cases where
the domain wouldn't match.

Add a new pam module option to limit the domains
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The PAM module will gain a new option, called ``domains`` that will
allow the administrator to use a list of domains to authenticate this
PAM service against. In the PAM responder, this option will only be in
effect for trusted clients. If the client is trusted, only domains
listed in this PAM option will be considered for authentication.

Please note that a patch implementing most of the functionality of this
PAM module option was contributed to the sssd-devel mailing list by
Daniel Gollub already.

Password Changes
^^^^^^^^^^^^^^^^

Password changes should be allowed against all domains, meaning that a
user A (recognized via getpeercred) will be allow to perform a password
change, i.e. implicitly allowed to access its own domain even if it is
untrusted. Arbitrary password changes for other users should not be
allowed.

Configuration Changes
~~~~~~~~~~~~~~~~~~~~~

Several new options, described in details in the previous section, will
be introduced. No existing options will change defaults or gain new
option values.

How To Test
~~~~~~~~~~~

#. Prepare an SSSD installation with at least two domains A and B.
#. Pick a PAM service that is running by a trusted user. One example
   might be VPN service ran by the openvpn user or similar. Add this
   user as a value of ``pam_trusted_users`` option in the ``[pam]``
   section.
#. Add one of the domains (domain A) as a ``domain=`` parameter into the
   ``auth`` section of your service's PAM config file
#. Authenticate using the selected PAM service as a user from domain A.
   The authentication should succeed.
#. Authenticate using the same service as a user from domain B. The
   authentication should fail and there should be a reasonable (i.e. not
   System Error) return code returned to the application
#. Authenticate using a different PAM service. Make sure this service is
   ran by an untrusted user (not root!). Logins against both A and B
   should fail.
#. Set the value of ``pam_allowed_auth_domains`` to A. Login against A
   should succeed from a service running as untrusted user.
#. Change the value of ``pam_allowed_auth_domains`` to all. Login
   against both domains should succeed from a service running as
   untrusted user.
#. Remove the ``domains=`` option from the PAM config file. The trusted
   service should now be able to log in against both SSSD domains.
#. Perform a password change as an untrusted user against a domain that
   he should not normally be allowed to use. The password change must
   succeed.

Authors
~~~~~~~

-  Daniel Gollub <`dgollub@brocade.com <mailto:dgollub@brocade.com>`__>
-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
-  Simo Sorce <`simo@redhat.com <mailto:simo@redhat.com>`__>
