.. highlight:: none

Change password on LDAP server that does not support Password Mofify Extended Operation
=======================================================================================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/1314


Problem statement
-----------------
Some directory servers either do not support Password Modify Extended Operation
(OID 1.3.6.1.4.1.4203.1.11.1, RFC 3062) for password change or this feature is
disabled by default. SSSD is unable to perform password change on such servers.
Even though we recommend to upgrade to servers that supports this feature,
there are still users that will benefit from SSSD being able to change
password without it.

Two example servers are IBM Tivoli Directory Server that does not support
this operation and Oracle Directory Server that may not have it enabled
by default.

Use cases
---------
 * A user wants to change his/her password against LDAP that does not support
   Password Modify Extended Operation.

Overview of the solution
------------------------
Provide new configuration option ``ldap_pwmodify_mode``. This option can be
set to one of two values: ``exop``, ``ldap_modify`` having ``exop`` to be the
default value. This will give us the ability to extend SSSD with another method
for password change in the future if it is ever needed.

If this option is set to ``exop`` then SSSD use Password Modify extended
operation to change the password as it does now. If the value is ``ldap_modify``
then ldap_modify operation will be used to change the password.

Even though the ldap_modify operation uses a plain text password, the servers
typically hashes the userPassword attribute.

`Quote from IBM Tivoli DS documentation <https://www.ibm.com/support/knowledgecenter/en/ssw_ibm_i_71/rzahy/rzahypwdencrypt.htm>`_:
"After the server is configured, any new passwords (for new
users) or modified passwords (for existing users) are encrypted before
they are stored in the directory database. Subsequent LDAP searches will
return a tagged and encrypted value."

Implementation details
----------------------
When a password change is requested, ``sdap_pam_chpass_handler_send`` is called.
This request first authenticates the user with current password and then in
``sdap_pam_chpass_handler_auth_done`` tries to change it with extended operation
by calling ``sdap_exop_modify_passwd_send``. At this point we should check
the value of ``ldap_pwmodify_exop`` option and decide whether to continue with
extended operation or use ``ldap_modify_ext`` instead.

Both operations use the connection that verified the current password not
connection that is used for ID lookups. Therefore the user that wants to change
his/her password must be allowed to write to the userPassword attribute of
their object.

Information on how to change the password using simple LDAP modify operation
can be found `here <https://www.ibm.com/support/knowledgecenter/SSVJJU_6.3.0/com.ibm.IBMDS.doc/admin_gd202.htm>`_

Configuration changes
---------------------
* New option: ``ldap_pwmodify_mode`` with possible values ``exop`` (default)
  and ``ldap_modify``.

How To Test
-----------
* Set ``ldap_pwmodify_mode`` to ``ldap_modify`` and try to change user's password.

Authors
-------
 * Pavel Březina <pbrezina@redhat.com>
