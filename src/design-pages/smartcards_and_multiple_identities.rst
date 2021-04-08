Smartcards and Multiple Identities
==================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/3050 <https://pagure.io/SSSD/sssd/issue/3050>`__

Problem statement
~~~~~~~~~~~~~~~~~

Although there are other means like e.g. sudo or policy-kit it is still
common practice to assign multiple accounts with different privileges to
a single person. The typical example is a system administrator who has
an ordinary user account for the daily office work and a privileged
account for the admin duties. Another example are functional accounts
like e.g. a dedicated database administrator account which is used by
more than one person.

In the context of Smartcard authentication there are two cases to
consider

-  multiple certificates valid for authentication on a single Smartcard
-  a single certfificate is mapped to multiple accounts

Use cases
~~~~~~~~~

Multiple certificates on a single Smartcard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To allow to log in to different accounts a user has multiple different
certificates which all match the criteria for authentication on a single
Smartcard. The user must a able to log in to each account by either
giving a user name, selecting a certificate (or both) depending on the
login method.

Single certificate for multiple accounts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To allow to log in to different accounts the certificate on the
Smartcard of the user is mapped to multiple accounts. The user must a
able to log in to each account by giving a user name for the specific
account.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

SSSD will read the the certificates from the Smartcard which matches the
criteria for authentication and will use optional additional
information, like .e.g. the user name, to determine a unique certificate
and a unique user name which can be used for authentication. If there is
not sufficient information SSSD might ask to user to select a
certificate or provider a user name to proceed with authentication.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

In general applications which use PAM for authentication will provide a
user name when calling pam\_start(). In this case SSSD has both the
certificate and a user name which should be sufficient in most cases to
determine if the user can authenticate with the certificate. There are
the following cases

-  if multiple users are found with the same name this is an error even
   without Smartcard authentication
-  if the certificate and the user do not map, SSSD will prompt for a
   password.
-  if the certificate and the user map, SSSD will prompt for a PIN
-  if there are multiple certificates suitable for authentication are on
   the Smartcard and more than one map to the user SSSD will prompt to
   select a certificate before asking for a PIN. **QUESTION: would it be
   an information leak to only show the certificates which relate to the
   user or do we have to display all certificate from the card?**

The first and second case already work. For the third case the check if
a certificate maps only to a single user must be dropped to support the
use case where one certificate is used to log in to different accounts
(which of course are identified by different user names). For the forth
case a new PAM dialog/conversation is needed.

To my knowledge there are currently two cases where a user name is not
available in the first place, InfoPipe lookups by certificate used e.g.
by `mod\_lookup\_identity <https://www.adelton.com/apache/mod_lookup_identity/>`__
and the GDM Smartcard module which calls pam\_start() with an empty user
name if a Smartcard was inserted when the GDM login screen is running.
Here the following cases are possible:

-  the certificate(s) cannot be mapped to any user, SSSD will just
   return a suitable error code
-  there are one or more certificates suitable for authentication on the
   card but only one maps to a user, SSSD will prompt for a PIN
-  there are one or more certificates suitable for authentication on the
   card but only one maps to multiple users, SSSD will prompt for a user
   name before asking for a PIN
-  there are more certificates suitable for authentication on the card
   and more than one map to users, SSSD will prompt to select a
   certificate, if the selected certificate still maps to multiple users
   SSSD will go to case three and asks for a user name before asking for
   a PIN.

Since in the InfoPipe case only one certificate is send to SSSD only the
first three cases are valid here and SSSD can e.g. indicate with an error
code that either none or multiple users match the certificate. In the
latter case the application can ask for a user name.

For the gdm case it might be useful to see how Smartcard authentication
is handled on Windows. To illustrate this I prepare two short screencasts
(sorry for the raw state, if time permits I will improve them).

`The
first <https://sbose.fedorapeople.org/sc/AD_SC_auth_2certs.webm>`__
shows the case where there are two different certificates valid for
authentication on the Smartcard. The Windows utility *certutil* can be
used with the *-SCInfo* option to check the certificates on the card and
if privates keys are available as well. When switching to the logon
screen Windows shows Icons for each certificate together with some data
from the certificate which should help to identify the certificate. In
this example the certificates were generated by the AD CS of the domain
and hence the displayed data matches the AD user name. In general this
does not have to be the case e.g. if certificates are issued by 3rd
party CAs. By selecting a specific certificate and entering the PIN the
mapped user is logged in.

`The
second <https://sbose.fedorapeople.org/sc/AD_SC_auth_2users.webm>`__
shows the case where there is only one certificate on the card but
mapped to two different users. The mapping can be done in AD's 'Users
and Computers' utility after enabling the 'Advanced Features' in the
'View' menu. Now with a right-click 'Name Mappings' can be selected from
the context menu. After switching to the logon screen Smartcard
authentication will fail because Windows does not know which user should
be used for login. To solve this the 'Allow user name hint' policy
setting must be enabled in 'Computer Configuration\\Administrative
Templates\\Windows Components\\Smart Card' (see `'Smart Card Group
Policy and Registry Settings' on
Technet <https://technet.microsoft.com/en-us/library/ff404287%28v=ws.10%29.aspx>`__
for details). Now the logon screen displays a 'Username hint' prompt in
addition to the PIN prompt. If the certificate on the Smartcard is
mapped to multiple users the additional username hint makes
authentication possible. Please note that the 'Username hint' is needed
as well if the user is in a trusted domain.

Coming back to gdm, as long as only a 'Username hint' is needed pam\_sss
can send two messages in the PAM conversation, one for the user name and
the second for the PIN. It would be nice if gdm can display both
messages and prompts at the same time as Windows does to make it more
clear to the user what input is expected and why.

If it is needed to select a certificate the typical PAM service will
display specific data from the certificates, e.g. the value of the most
specific RDN of the subject and the full DN of the issuer, in a numbered
list asking the user to enter the number of the certificate which should
be used for login. If would be nice if gdm can display this list in a
more graphical way and make it possible to select the certificate with a
mouse-click. Since SSSD knows that it is called by gdm because of the
PAM service name, e.g. gdm-smartcard, it would be possible to send the
certificate data with a new messages style, e.g.
PAM\_SELECTON\_LIST\_ITEM like the GNU/Linux specific PAM\_RADIO\_TYPE. Then
gdm would be able to display the certificate selection in a more
suitable way, e.g. similar to the selection of user names.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

Does your feature involve changes to configuration, like new options or
options changing values? Summarize them here. There's no need to go into
too many details, that's what man pages are for.

How To Test
~~~~~~~~~~~

This section should explain to a person with admin-level of SSSD
understanding how this change affects run time behaviour of SSSD and how
can an SSSD user test this change. If the feature is internal-only,
please list what areas of SSSD are affected so that testers know where
to focus.

How To Debug
~~~~~~~~~~~~

Explain how to debug this feature if something goes wrong. This section
might include examples of additional commands the user might run (such
as keytab or certificate sanity checks) or explain what message to look
for.

Authors
~~~~~~~

Give credit to authors of the design in this section.
