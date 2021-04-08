Prompting For Multiple Authentication Types
===========================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2988 <https://pagure.io/SSSD/sssd/issue/2988>`__

Problem statement
-----------------

Currently FreeIPA only allows one authentication type at a given time
for a user. Even if both authentication types 'password' and 'otp' were
configured for the user only 'otp' was allowed in that case. Because of
this SSSD only had to prompt for either 'Password' or 'First factor' and
'Second factor'.

New version of FreeIPA will allow that the sue can authentication with
different authentication types at the same time
(`https://pagure.io/freeipa/issue/433 <https://pagure.io/freeipa/issue/433>`__).
SSSD now must prompt the user differently to make clear which
authentication types are available for the user ideally without making
the login process more complicated.

Use cases
---------

(taken from
`http://www.freeipa.org/page/V4/Authentication\_Indicators <http://www.freeipa.org/page/V4/Authentication_Indicators>`__)

Strong Authentication on Selected System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

User story
''''''''''

As an Administrator, I want to setup authentication to a critical system
in my infrastructure (gateway VPN, accounting system) to only allow IdM
users authenticated via strong authentication methods (2FA). I do not
want to require strong authentication on other systems.

Description
'''''''''''

A realm has two servers configured for ssh which use the following
principals configured with authentication indicators: ::

        host/lowsecurity.example.com []
        host/highesecurity.example.com [otp radius]

When the administrator logs in using both his password and an OTP token,
he can access both systems via ssh. However, when the administrator logs
in using just a password, he can only access lowsecurity.example.com.

Overview of the solution
------------------------

Depending on the available authentication types SSSD will show different
login prompts:

+------------------------+------------------------------------------------------------+
| Authentication types   | Login Prompt                                               |
+========================+============================================================+
| password               | Password:                                                  |
+------------------------+------------------------------------------------------------+
| otp                    | First factor:                                              |
|                        | Second factor:                                             |
+------------------------+------------------------------------------------------------+
| password + otp         | First factor or password:                                  |
|                        | Second factor, press return for Password authentication:   |
+------------------------+------------------------------------------------------------+

If Smartcard authentication is enabled (*pam\_cert\_auth = True*) and a
Smartcard is inserted in a reader with a certificate matching the user
who wants to login the login prompt will ask for the Smartcard PIN for
local authentication.
(`https://docs.pagure.org/SSSD.sssd/design_pages/smartcard_authentication_step1 <https://docs.pagure.org/SSSD.sssd/design_pages/smartcard_authentication_step1.html>`__).
Upcoming support for pkinit might lead to another extension of the
prompting scheme.

Implementation details
----------------------

First it has to be noted that this feature is related to Kerberos
authentication because here the available authentication types are
indicated by the server during the authentication request. Other
authentication schemes like e.g. LDAP bind based authentication do
support multiple different methods as well, e.g. you can bind to the
FreeIPA LDAP server with password and 2FA authentication if the user is
configured accordingly. But here the client either has to try which
authentication might work or figure out possible authentication methods
by other means which might be unreliable.

Kerberos indicates the available authentication methods via the
available pre-authentication methods listed in the 'Additional
pre-authentication required' response. The different pre-authentication
methods are implemented as plugins and there are two ways for the
plugins to interact with a user. The first one is a prompter callback
which can be given as argument to e.g.
krb5\_get\_init\_creds\_password(). The second, newer and more advanced
method, are responders which can be set with
krb5\_get\_init\_creds\_opt\_set\_responder() which is available since
version 1.11 of MIT Kerberos.

For older versions of Kerberos where
krb5\_get\_init\_creds\_opt\_set\_responder() is not available nothing
changes because those versions do not support OTP either, so only
password authentication will be available here.

For builds with a newer version of MIT Kerberos all authentication
decision will be moved to the responder. This means that calls like
krb5\_get\_init\_creds\_password() will not get the password as an
argument anymore but the password is set inside of the responder if
password based authentication is chosen.

The responder will check which authentication types are available by
calling krb5\_responder\_list\_questions(). If password authentication
is available, indicated by the value of
KRB5\_RESPONDER\_QUESTION\_PASSWORD and the provided authentication
token is of type password as well the password is set as answer to the
password authentication and no further methods are considered.

If password authentication is not available or the provided
authentication token is of type SSS\_AUTHTOK\_TYPE\_2FA the existing OTP
responder component is called.

During the SSSD pre-authentication request a new pam response is added
which indicate that password authentication is available. Based on this
and the OTP related response the pam\_sss PAM modules can choose the
right set of prompts.

Configuration changes
---------------------

No configuration changes are needed on the client the available
authentication types are determined based the the responses of the
server.

How To Test
-----------

First create an IPA user and assign an OTP token to the user, see
`http://www.freeipa.org/page/V4/OTP#How\_to\_Test <http://www.freeipa.org/page/V4/OTP#How_to_Test>`__
for details. Additionally two services with different authentication
indicator requirements are useful to test the returned credentials but
are not necessary to test the prompting. ::

    $ ipa service-add ANY/ipa-client.example.com
    $ ipa-getkeytab -p ANY/ipa-client.example.com -k /tmp/any.keytab

    $ ipa service-add OTP/ipa-client.example.com --auth-ind=otp
    $ ipa-getkeytab -p OTP/ipa-client.example.com -k /tmp/otp.keytab

(the keytab files are not needed for further testing).

Password only
^^^^^^^^^^^^^

To test plain password authentication call ::

    $ ipa user-mod test_user --user-auth-type=password

and then as an un-privileged user ::

    $ su - test_user
    Password:

after login you can test by calling ::

    $ kvno ANY/ipa-client.example.com@EXAMPLE.COM
    ANY/ipa-client.example.com@EXAMPLE.COM: kvno = 1
    $ kvno OTP/ipa-client.example.com@EXAMPLE.COM
    kvno: KDC policy rejects request while getting credentials for OTP/ipa-client.example.com@EXAMPLE.COM

that only a ticket for the ANY service can be requested but not for the
OTP service because only the password was used for authentication.
Entering Password+TokenValue in a single string at the *Password:* prompt
will cause an authentication failure.

OTP only
^^^^^^^^

The second test is for OTP only authentication ::

    $ ipa user-mod test_user --user-auth-type=otp

and then as an un-privileged user call ::

    $ su - test_user
    First Factor:
    Second Factor:

after login you can test by calling ::

    $ kvno ANY/ipa-client.example.com@EXAMPLE.COM
    ANY/ipa-client.example.com@EXAMPLE.COM: kvno = 1
    $ kvno OTP/ipa-client.example.com@EXAMPLE.COM
    OTP/ipa-client.example.com@EXAMPLE.COM: kvno = 1

that tickets for both services can be request successfully because now
2-Factor authentication was used to log in.
Entering Password+TokenValue in a single string at the *First Factor:*
prompt will authenticate the user successfully as well but features
like off-line authentication or unlocking of the user's keyring might
not be available.

Password and OTP
''''''''''''''''

Finally both authentication methods are enabled on the server: ::

    $ ipa user-mod test_user --user-auth-type=otp --user-auth-type=password

If now call *su* as an un-privileged user ::

    $ su - test_user
    First Factor or Password:
    Second Factor, press return for Password authentication:

you can either just enter the password and press enter at the second
prompt or enter the password and the OTP token value at the respective
prompt. In the first case only a ticket for the ANY service can be
requested: ::

    $ kvno ANY/ipa-client.example.com@EXAMPLE.COM
    ANY/ipa-client.example.com@EXAMPLE.COML: kvno = 1
    $ kvno OTP/ipa-client.example.com@EXAMPLE.COM
    kvno: KDC policy rejects request while getting credentials for OTP/ipa-client.example.com@EXAMPLE.COM

If both factor are given tickets for both services can be requested
successfully: ::

    $ kvno ANY/ipa-client.example.com@EXAMPLE.COM
    ANY/ipa-client.example.com@EXAMPLE.COM: kvno = 1
    $ kvno OTP/ipa-client.example.com@EXAMPLE.COM
    OTP/ipa-client.example.com@EXAMPLE.COM: kvno = 1

Entering Password+TokenValue in a single string at the
*First Factor or Password:* prompt will cause an authentication
failure.

How To Debug
------------

If password authentication is not working when both password and OTP
authentication are enabled you might hit
`https://bugzilla.redhat.com//show\_bug.cgi?id=1340304 <https://bugzilla.redhat.com//show_bug.cgi?id=1340304>`__
and should update the Kerberos packages.

Inspecting log files
^^^^^^^^^^^^^^^^^^^^

Setting *debug\_level = 9* in the *[domain/...]* section of *sssd.conf*
will add libkrb5 trace messages to the krb5\_child.log file which e.g.
will show the pre-authentication methods offered by the KDC. Based on
this SSSD will determine which authentication methods are available. In
the *Processing preauth types:* line of the trace output *141*
represents the OTP authentication while *2* (without FAST) or *138*
(with FAST) stand for password authentication.

Manual testing with kinit
^^^^^^^^^^^^^^^^^^^^^^^^^

If only password authentication or password and OTP authentication are
configured for a user kinit should ask for the password: ::

    $ kinit test_user
    Password for test_user@EXAMPLE.COM

OTP authentication is only available if FAST is enabled. The needed
armor credential cache must be requested with kinit as well: ::

    $ kinit -c ./armor.ccache -k

which will use the default keytab (/etc/krb5.keytab) which is accessible
only by root to get a TGT. For easier testing you can create a special
service and give suitable permissions to the service keytab. To use it
with kinit use the -t option ::

    $ kinit -c ./armor.ccache -k -t ./service.keytab

Now you can call ::

    $ kinit -T ./armor.ccache test_user
    Enter OTP Token Value:

If OTP is not enable for the user you should see the password prompt.

As usual, setting *KRB5\_TRACE=/dev/stdout* before calling *kinit* or
*kvno* will produce some extra output which might be useful.

Authors
-------

-  Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
