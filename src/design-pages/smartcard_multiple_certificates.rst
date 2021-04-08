Smartcard authentication - Multiple Certificates on a Smartcard
===============================================================

Related ticket(s):
------------------
 * https://pagure.io/SSSD/sssd/issue/3050
 * https://pagure.io/SSSD/sssd/issue/3560

Problem statement
-----------------
Smartcard can contain multiple certificates valid for authentication. Currently
SSSD uses only the first valid one returned by the configured PKCS#11 module.

SSSD should allow the user to choose the certificate which should be used for
authentication at login time.

Use cases
---------
A Smartcard might contain different certificates which can be used by a single
person to authenticate as different roles (different accounts). At login time
the user should be able to choose the certificate so that he can login with the
expected role.

A Smartcard might contain certificates for different purposes which will all
match the configured criteria for login (matching and mapping rules) but only
one is accepted on the server side for login. At login time the user must be
able to select the certificate which is accepted on the server side to login
successfully.

Overview of the solution
------------------------
The primary way to login to a desktop with a connected Smartcard reader is via
GDM. GDM has a special plugin which can detect the insertion of a Smartcard in
the reader and start the login process based on this. Recently an extension for
a special type of PAM conversation was added
(https://bugzilla.gnome.org/show_bug.cgi?id=788851) which allows to easily
select from a list of options.

SSSD should support the GDM PAM extensions in pam_sss. As a fallback a text
based interface which displays a numbered list of options should be used. The
user can then enter the number of the certificate which should be used.

To make it easy to the user to choose the right certificate the Subject-DNs of
the different certificates found on the card should be shown together with the
label of the certificate. It would be possible to make this configurable in a
later version.

Implementation details
----------------------
Currently in the communication between the SSSD components (``pam_sss``, PAM
responder, ``p11_child`` and backend) there are already attributes used to
uniquely identify a certificate on a Smartcard. This was added with the PKINIT
support to make sure the certificate matched by SSSD to the user is the same
used by the MIT Kerberos PKINIT plugin. This means that the initial part of the
communication between pam_sss and the PAM responders has to be refactored to
not only support one set of attributes but multiple. Additionally a user prompt
for each certificate (Subject-DN and label) has to be added to the attributes.

As mentioned above ``pam_sss`` should support the GDM PAM extension for an
option list besides a simple text based interface. Luckily all internal details
of this extension are hidden in macros which are provider by recent version of
gdm in the ``/usr/include/gdm/gdm-pam-extensions.h`` header file. This means
that there is no additional runtime requirement.

On the PAM responder side the code has to be adopted to make sure the user name
mapped to the selected certificate is determined before the actual
authentication starts, i.e. the authentication request is sent to the backend.

Configuration changes
---------------------
No configuration changes are needed. If p11_child detects multiple certificate
suitable for authentication SSSD should allow the user to select one.

How To Test
-----------
To test this feature a Smartcard with  multiple different certificate (together
with the matching private keys) should be created. For different use cases

* the certificates can be all mapped to single user

* the certificates can be all mapped to different users

* only some certificates are mapped while the other are not suitable for
  authentication

* no certificate is mapped to a user

How To Debug
------------
All debug data can be found in the usual SSSD log files. For Smartcard
authentication ``sssd_pam.log``, ``p11_child.log`` and the backend log file
``sssd_domain.name.log`` are the most important ones.

Authors
-------
 * Sumit Bose <sbose@redhat.com>
