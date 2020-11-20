Make authentication prompting configurable
==========================================

Related ticket(s):
------------------
    - https://pagure.io/SSSD/sssd/issue/3264
    - https://pagure.io/SSSD/sssd/issue/3856
    - https://bugzilla.redhat.com/show_bug.cgi?id=1623624

Problem statement
-----------------
Although SSSD tries to use the most suitable prompting depending on which
authentication options (password, two-factor authentication, smartcard
authentication) are available for the user it does not fit in all cases.  It
should be possible with the help of configuration options to tune the prompting
during authentication.

Use cases
---------
General prompting
^^^^^^^^^^^^^^^^^
Sometimes just asking ``Password:`` is not sufficient because different
authentication domains are used and something like ``Enter your AD Password:``
is more suitable.

Another example is SSSD's default prompting for two-factor authentication if
both plain password and two-factor authentication is available for the user. In
this case an ``(optional)`` is shown with the prompt for the second factor.
This might be irritating on systems where two-factor authentication is
required.

Two-Factor Authentication Prompting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are two ways how the two factors can be entered. Either each factor in a
separate prompt and both chained together in a single prompt.

The `PAM Conversation of OTP`_ design page explains some details why using two
separate prompts is useful from the SSSD point of view. However there are
services which cannot handle PAM conversations and ask the user directly to
enter the needed credentials. On the PAM level those application can put the
user input in both prompts or only in the first one. Instead of adding
heuristics to SSSD to figure out what is meant by which application it would be
easier and more reliable to be able to configure the expected behavior for each
service individually if needed.

.. _PAM Conversation of OTP: https://docs.pagure.org/SSSD.sssd/design_pages/pam_conversation_for_otp.html

What has to be noted here is that SSSD must know somehow if the user entered a
single password or or two-factor credentials in a single string. The reason is
that both types of authentication might be treated differently on the server
side. This can e.g. be seen with Kerberos where a special pre-authentication
scheme described in `RFC6560`_ is used. If here the plain password is used
authentication will fail and if the two-factor string is used with plain
Kerberos authentication not using the OTP pre-auth method authentication will
fail as well. Since a failed authentication might increment a bad-password
count and cause a user lock, try-and-error is not an option here.

.. _RFC6560: https://tools.ietf.org/html/rfc6560.html

Alternative authentication principal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Typically during authentication the user name of the POSIX user trying to
authenticate is entered and SSSD tries to figure out to which account in the
authentication domain the POSIX user relates. If the account cannot be found,
e.g. because the backend simply does not support such lookup, and there is a
strict 1:1 mapping the `krb5_map_user` option might be used. But this might
become cumbersome if many users have to be managed or if multiple users from an
authentication domain should be allowed to authenticate as a single POSIX user.

To cover those cases and additional prompt for a user name which should be used
for authentication would be helpful. Of course it has to be noted that a
suitable access control scheme has to be used to make sure that only expected
accounts from the authentication domain can login in as a given POSIX user.

Additionally this can only work properly with services which offer full PAM
conversation functionality so that the prompt for the alternative name is shown
to the user.

Asking for missing user name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There is also the case of `gdm-smartcard` where typically no user name is
prompted at all because it is expected that the user name can be derived from
the certificate found on the Smartcard. But there are cases where this is not
possible as described in `Smartcards and Multiple Identities`_. Here is would
be useful to have a configurable extra prompt for a user name hint.

.. _Smartcards and Multiple Identities: https://docs.pagure.org/SSSD.sssd/design_pages/smartcards_and_multiple_identities.html

Using specific authentication methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Currently SSSD tries to determine on its own what would be the most suitable
prompting if multiple authentication methods are available. E.g. if a Smartcard
with a certificate suitable to authenticate the current user is available SSSD
will prompt for a Smartcard PIN even if password authentication would be
available for the user as well. To see a password prompt the Smartcard has to
be removed first. But there might be cases where password or two-factor
authentication should be preferred and having to remove the Smartcard might be
irritating.

Another use case would be to only ask for two-factor authentication even if
password authentication would be available for the user as well.

An option where the prompting types can be ordered by preference would be
useful here.

Overview of the solution
------------------------
On one hand it can be seen from the use cases above that it should be possible
to set the options for each PAM service individually. On the other hand it
should be easy to set e.g. a global welcome/warning message for all services.
For this a hierarchical configuration scheme, which SSSD already uses e.g. to
configure sub-domains, would be suitable.

The hierarchy would start with a `[prompting]` section valid for all
authentication types and services. The next level would be
`[prompting/password]`, `[prompting/2fa]` and `[prompting/cert_auth]` for
password, two-factor and Smartcard authentication respectively. Finally there
will be a level for the PAM service specific options like e.g.
`[prompting/2fa/sshd]`. Lower level, i.e. more specific, options will of course
overwrite higher level, i.e. more general, options.

All those options will be evaluated by SSSD's PAM responder. It would be
possible to have all those options in `[pam/prompting/....]` sections. But
always having the `pam/` prefix looks redundant and the section names are
already long enough.

Currently the prompting for the different authentication schemes and the
selection is basically hardcoded in the `pam_sss.so` PAM module. Since the PAM
responder will control the prompting if any option is set below `[prompting]`
the PAM responder must set `/var/lib/sss/pubconf/pam_preauth_available` in this
case to make sure `pam_sss.so` tries to call the PAM responder before prompting
the user.

One or more new PAM `response_type` should be added to send the needed data for
prompting to `pam_sss.so`.

To handle the alternative authentication principal `enum sss_authtok_type` and
the related methods for `struct sss_auth_token` should be extended.

Implementation details
----------------------

_`sssd.conf` man page section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The details of the expected behavior of the new configuration option are best
documented in a man page. For a start it might look like::

    PROMPTING CONFIGURATION SECTION
       If a special file (/var/lib/sss/pubconf/pam_preauth_available) exists
       SSSD's PAM module pam_sss will ask SSSD to figure out which authentication
       methods are available for the user trying to log in. Based on the results
       pam_sss will prompt the user for appropriate credentials.

       With the growing number of authentication methods and the possibility
       that there are multiple ones for a single user the heuristic used by pam_sss to
       select the prompting might not be suitable for all use cases. To following
       options should provide a better flexibility here.

       Each supported authentication method has it's own configuration
       sub-section under “[prompting/...]”. Currently there are:

       [prompting/password]
           to configure password prompting, allowed options are:

           password_prompt
               to change the string of the password prompt

       [prompting/2fa]
           to configure two-factor authentication prompting, allowed options are:

           first_prompt
               to change the string of the prompt for the first factor

           second_prompt
               to change the string of the prompt for the second factor

           single_prompt
               boolean value, if True there will be only a single prompt using
               the value of first_prompt where it is expected that both factor are entered as
               a single string

       It is possible to add a sub-section for specific PAM services like e.g.
       “[prompting/password/sshd]” to individual change the prompting for this
       service.

Changes to `pam_sss.so`
^^^^^^^^^^^^^^^^^^^^^^^
If there is a `SSS_PAM_PROMPT_CONFIG` item during the pre-auth step in the
response from the PAM responder SSSD's PAM module `pam_sss.so` should act
according to the received configuration. If there is no such item `pam_sss.so`
should just show the current behavior.

The response currently has the following structure:

+-----------------------------------------------+---------------------------+--------------------+-----------------------------------+
| number of prompting configurations (uint32_t) | prompting type (uint32_t) | type specific data | ... additional type-data pairs ...|
+-----------------------------------------------+---------------------------+--------------------+-----------------------------------+

where the type is defined by::

    enum prompt_config_type {
        PC_TYPE_INVALID = 0,
        PC_TYPE_PASSWORD,
        PC_TYPE_2FA,
        PC_TYPE_2FA_SINGLE,
        PC_TYPE_SC_PIN,
        PC_TYPE_LAST
    };

Where the data for `PC_TYPE_PASSWORD` is:

+--------------------------+------------------------+
| string length (uint32_t) | string of given length |
+--------------------------+------------------------+

`PC_TYPE_2FA` obviously has 2 strings:

+---------------------------------------+--------------+------------------------------------+---------------+
| length of the first string (uint32_t) | first string | length of second string (uint32_t) | second string |
+---------------------------------------+--------------+------------------------------------+---------------+

`PC_TYPE_2FA_SINGLE` uses a single prompt hence also only a single string

+--------------------------+------------------------+
| string length (uint32_t) | string of given length |
+--------------------------+------------------------+

Finally `PC_TYPE_SC_PIN` currently has no specific data.

Changes to the PAM responder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
First the PAM responder has to read the new configuration option from
`sssd.conf` and if there are any it should create the pre-auth indicator file
so that the PAM module `pam_sss.so` will run the pre-auth step.  During the
pre-auth step the PAM responder has to check if configured options apply to the
given request and create an appropriate `SSS_PAM_PROMPT_CONFIG` responses if
needed.

Configuration changes
---------------------
See sssd.conf_

How To Test
-----------
Please see sssd.conf_ what options are currently available.

In general testing can start with changing the password prompt for all services by adding::

    [prompting/password]
    password_prompt = My Password Prompt

If now `su` is called as non-root user for an SSSD user::

    $ su sssd_user
    My Password Prompt

    $ su - sssd_user
    My Password Prompt

Next step can be to add a specific prompt for `su-l`::

    [prompting/password/su-l]
    password_prompt = My su-l Prompt

and now calling `su` should show::

    $ su sssd_user
    My Password Prompt

    $ su - sssd_user
    My su-l Prompt

If a FreeIPA setup with users configured for 2-Factor Authentication you can
use `first_prompt` and `second_prompt` in the `[prompting/2fa]` section to
change the 2FA prompting strings for all services. With::

    [prompting/2fa/my_service]
    single_prompt = True
    first_prompt = Please enter password + OTP token value

you can enable single 2FA prompting for the PAM service `my_service` where only
one prompt will be show where the long term password and the one-time password
have to be entered in a single string.

How To Debug
------------
Setting `debug_level` in the `[pam]` section of `sssd.conf` to a sufficiently
high value will show error and debugging information for the processing of the
prompting option.

If you compile `pam_sss.so` with `-DPAM_DEBUG` in the C-compiler flags the PAM
module will write some debug information to `/var/run/pam-debug.log` (or a
similar file depending on the platform). Since this is typically not the case
using `gdb` might help to identify issues in processing the prompting
configuration. Suitable break points are `pc_list_from_response()` where the
response form the PAM responder is translated and `prompt_by_config()` where
the right prompting based on the received configuration is selected.

Authors
-------
Sumit Bose <sbose@redhat.com>
