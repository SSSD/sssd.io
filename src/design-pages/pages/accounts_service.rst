Note well: this is at the *spitballing* stage, so it can all get shot
down.

AccountsService takeover
========================

What we're suggesting as the point of focus for integration is to have
SSSD provide a superset of the *org.freedesktop.Accounts* D-Bus API.

The org.freedesktop.Accounts D-Bus API as currently implemented by *accountsservice*
------------------------------------------------------------------------------------

`The current
API <https://live.gnome.org/ThreePointThree/Features/UserPanel/Service>`__
offers:

-  Creation/removal of user accounts.
-  Enumeration of user accounts which are known to the service.

   -  Currently this resolves to a subset of the local system's
      accounts.

-  Signals broadcast when a user account is added/removed/modified.
-  Ability to mark the user user account as a "Standard" user or an
   "Administrator".

   -  Under the covers, the user is added to or removed from the *wheel*
      group, but UID=0 is always considered to be an administrator.

-  Ability to lock or unlock the user's account and query its lock
   status.
-  Ability to check, set, or reset that the user must change password at
   next login.
-  Password can be changed to a new **hashed** value, as returned by
   *crypt(3)* or it can be removed, after which no password is required
   for login.
-  Attributes exposed via specific get/set methods and the properties
   interface:

   -  login name
   -  full name
   -  email
   -  preferred locale
   -  preferred X session name
   -  physical location
   -  home directory pathname
   -  login shell
   -  login frequency
   -  icon/thumbnail filename

      -  the contents of this file are copied to
         /var/lib/AccountsService/icons/$user

   -  autologin
   -  password hint

The org.freedesktop.Accounts D-Bus API as it would be provided by *SSSD*
------------------------------------------------------------------------

-  Local users live in the SSSD *local* provider's domain, full
   creation/removal support.
-  Local **groups** are now exposed and managed.

   -  Groups can contain users and other groups.

-  Enumeration of users defaults to returning those known to the *local*
   domain and all identities from other domains that are in SSSD's
   cache.
-  Signals broadcast when a user account or group is added to the
   *local* domain's database, or an entry is added to SSSD's cache for
   any other domains. Likewise, signals emitted when knowledge of a user
   or group is updated or removed from either location.
-  *Local* users can be marked as *Standard* or *Administrator*
   accounts, and this information can be retrieved.

   -  [STRIKEOUT:This will add or remove the user from the *local*
      *wheel* group. Some POSIX applications may be confused by this.]
   -  [STRIKEOUT:Users from other domains may also be added or removed
      from the *local* *wheel* group.]

-  *Local* user accounts can be locked or unlocked, and their account
   lock status can be checked.
-  *Local* user accounts can have their account flagged to require a
   password change at the next login.

   -  When the user is part of a non-\ *local* domain, this may be known
      up-front, or it may be discovered as a side-effect of performing
      an authentication attempt.

-  *Local* user accounts can have their password changed to a new
   **clear** or **hashed** value, or removed.

   -  User accounts in non-\ *local* domains can have their password
      changed to a new **clear** value if the old value is also
      provided.

-  *Local* user accounts have their attributes stored in the database as
   entry attributes along with the already-kept POSIX attributes, and
   can be modified.

   -  For user accounts in non-\ *local* domains, if an attribute is
      configured to be writable, its value is fetched from the identity
      provider only if there is no value for it, for the user, already
      present in the cache. Because SSSD does not know how to push
      updated information to identity providers, if the attribute is
      writable, only the cached value is updated.

API additions useful to non-desktop cases
-----------------------------------------

Some of these look like reasonable extensions to the existing D-Bus
APIs, others won't.

-  A new method for obtaining a list of SSSD's domains.

   -  The answer can depend on who's asking, as reported by the bus.

-  New methods for creating and deleting *local* groups, and for adding
   or removing a *local* user or group from the list of a *local*
   group's members.
-  A new method for enumerating the groups known to the *local* domain
   and any identities from other domains that are in SSSD's cache.

   -  [STRIKEOUT:A variation on this method] [STRIKEOUT:An optional
      argument for this method] A variation on this method which narrows
      the scope to a specified domain.

-  [STRIKEOUT:A variation on] [STRIKEOUT:An optional argument for the]
   An additional user enumeration method which narrows the scope to a
   specified domain.
-  A new method for performing authentication checks.

   -  Conceptually similar to the application's part of a PAM
      conversation, but explicitly includes the concept of an
      authentication domain and enough context to tell if we're asking
      for a password, an OTP, a smart card PIN, etc.
   -  Can be multi-step.
   -  RHEV-M would likely use this instead of nsswitch+PAM because its
      users wouldn't be (and wouldn't need to be) complete POSIX users.
   -  A user's secondary identities, if serviced by a mechanism that
      SSSD can/will/does support, *can* also be authenticated here,
      though it would generally only be useful to do so if
      authentication provided some sort of SSO credential for SSSD to
      manage on the user's behalf.

-  A new method for performing password changes.

   -  [STRIKEOUT:As above, conceptually similar to the application's
      part of a PAM conversation, again including the concept of an
      authentication domain.]
   -  [STRIKEOUT:Add a flag to the existing password change method to
      indicate that an unhashed password is being provided, and allow
      password change to fail if the flag is not set.]
   -  Calling signature is similar to the authentication API, except
      that the caller is told when it will be supplying the new
      password.

-  A new method for obtaining a list of groups to which a user belongs.
   These wouldn't necessarily be POSIX groups, as the accounts service
   is uninterested in groups in the general case (the main exception
   being that it maps Administatorness to membership in the *wheel*
   group), but they'd be whatever the domain considered to be groups.
-  A new method or three for determining which users are in a group,
   which groups are in a group, and which users are in a group by way of
   being in other groups.
-  A new signal broadcast when a user's password or equivalent is about
   to expire, along with how much time is left, if we can know that.

   -  Would need something running in the user's session to catch them
      and offer to initiate a password change via the above
      password-changing method. Not provided by SSSD.

-  A new signal broadcast when a user's SSO credentials (e.g. Kerberos
   TGT) are about to expire.

   -  Would need something running in the user's session to catch them
      and offer to reinitialize them by calling the above authentication
      method. Not provided by SSSD.

-  A new signal broadcast when a user's SSO credentials are
   reinitialized.

   -  Would want something running in the user's session to catch them
      and rescind offers to reinitialize them that aren't in-progress.
      Not provided by SSSD.

-  The ability to fetch and manage more string attributes than the
   current accountsService API offers.

   -  This may just take the form of more properties, perhaps without
      friendly get/set methods, particularly if
   -  The set would be configured in SSSD on a per-domain basis.

Breaking It Down To The API Level
---------------------------------

We're talking about providing a superset of the D-Bus API currently
offered by the *accountsservice* package.

The APIs themselves are advertised to clients via D-Bus introspection,
so they can be browsed using tools such as *d-feet*, and what follows is
heavily based on that information and the introspection information
included with the package.

The very, very, very short D-Bus Primer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The D-Bus service model is a tree of objects. Each object has a path
name (an *object path*) which resembles a filesystem path, and can both
emit broadcast notifications referred to as *signals* and provide
callable functions referred to as *method call*\ s, as well as
possessing data members called *properties*. When a process connects to
a bus, it is given a connection-specific name (typically of the form
":1.121") which is used to route replies back to it. A process which
intends to offer services typically also registers a name (of a form
such as "org.freedesktop.Accounts") which clients can use to specify the
destination for *method call*\ s that they intend to make use of. The
names of methods can be namespaced using *interface* names, but in many
cases, unless necessary for disambiguation, they are optional.

The Singleton Management Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *accountsservice* package currently provides a service which can be
reached using the name *org.freedesktop.Accounts*, which provides one
singleton object of note: */org/freedesktop/Accounts*, which provides
five methods, two signals, and one property, all as part of an interface
named *org.freedesktop.Accounts*. Methods and properties that we add
that are specific to SSSD should grouped as part of an SSSD-specific
interface name.

-  **method** CreateUser(String name, String fullname, Int accountType)

   -  *name*: the user's login name
   -  *fullname*: the user's real name
   -  *accountType*: an enumerated value which flags the account as a
      *Standard* or *Administrator* account
   -  returns: Path *user*: the path for the user's object
   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure
   -  Creates a user with a given name in the default local provider
      domain. Note that the UID is not specified by the caller, as it is
      allocated by the provider. The caller can retrieve it from the
      user's entry if the call succeeds. The meaning of account types is
      not specified, but in the current implementation the difference
      between a *Standard* user and an *Administrator* is whether or not
      the user is a member of the *wheel* group.

-  **ADD** **method** CreateUserInDomain(String domain, String name,
   String fullname, Int accountType)

   -  *domain*: the domain in which the caller wants the account to be
      created, can be left empty or unspecified to implicitly select the
      default local provider domain, to which the caller must already be
      allowed access
   -  *name*: the user's login name
   -  *fullname*: the user's real name
   -  *accountType*: an enumerated value which flags the account as a
      *Standard* or *Administrator* account
   -  returns: Path *user*: the path for the user's object
   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure
   -  Creates a user with a given name. Note that the UID is not
      specified by the caller, as it is allocated by the provider. The
      caller can retrieve it from the user's entry if the call succeeds.
      The meaning of account types is not specified, but in the current
      implementation the difference between a *Standard* user and an
      *Administrator* is whether or not the user is a member of the
      *wheel* group.

-  **method** DeleteUser(Int64 user, Boolean removeFiles)

   -  *user*: the user ID of the user to be removed
   -  *removeFiles*: whether or not to remove the user's home directory
   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure
   -  Deletes the user with the given UID.

-  **ADD** **method** DeleteUserInDomain(String domain, Int64 user,
   Boolean removeFiles)

   -  *domain*: the domain to which the user belongs
   -  *user*: the user ID of the user to be removed
   -  *removeFiles*: whether or not to remove the user's home directory
   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure
   -  Deletes the user with the given UID if a matching user exists in
      the named domain.

-  **method** FindUserById(Int64 id)

   -  *id*: the user's UID
   -  returns: Path *user*: the path for the user's object. All
      configured domains are searched.
   -  Error *org.freedesktop.Accounts.Error.Failed*: no such user exists

-  **ADD** **method** FindUserByIdInDomain(String domain, Int64 id)

   -  *id*: the user's UID
   -  *domain*: the name of the domain to search
   -  returns: Path *user*: the path for the user's object, if a
      matching user exists in the domain.
   -  Error *org.freedesktop.Accounts.Error.Failed*: no such user exists

-  **method** FindUserByName(String name)

   -  *name*: the user's login name
   -  returns: Path *user*: the path for the user's object. The search
      is performed over all configured domains.
   -  Error *org.freedesktop.Accounts.Error.Failed*: no such user exists

-  **ADD** **method** FindUserByNameInDomain(String domain, String name)

   -  *domain*: the name of the domain to search
   -  *name*: the user's login name
   -  returns: Path *user*: the path for the user's object
   -  Error *org.freedesktop.Accounts.Error.Failed*: no such user exists

-  **method** ListCachedUsers()

   -  returns: *users*: an array of paths for the user objects
   -  Returns a subset of the users who exist, typically those who have
      logged in recently, for populating chooser lists such as those
      used by GDM's greeter.
   -  Currently the *accountsservice* process scans /etc/passwd for
      users, filters out those with UID values which are below a
      threshold point to screen out system users, and sorts the rest by
      the number of times the users in question appear in /var/log/wtmp.
      Above a certain length, it's expected that the caller will
      disregard the list and present only an entry field. The entry
      field always needs to be available because we know that some
      results may be missing from this list.

-  **ADD** **method** ListDomainUsers(String domain)

   -  *domain*: the domain name in which the caller is interested
   -  returns: *users*: an array of paths for all known user objects
   -  Returns all of the objects for users about which SSSD is aware.
      This may be a very large list, particularly if enumeration is
      enabled for the domain.

-  **signal** UserAdded(Path user)

   -  *path*: the path for the user's object
   -  **MODIFY** this signal is emitted when a user is created or
      appears in the cache for a remote domain

-  **signal** UserDeleted(Path user)

   -  *path*: the path for the user's object
   -  **MODIFY** this signal is emitted when a user is deleted or
      disappears from the cache for a remote domain, though the latter
      is not expected to happen often

-  **property** String DaemonVersion

   -  The version of the running daemon.

-  **ADD** **method** CreateGroup(String name)

   -  *name*: the group's name
   -  returns: Path *group*: the path for the new group object
   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure
   -  Creates a group with the given name in the default local provider
      domain. As with users, the GID is allocated by the provider, and
      the caller can retrieve it from the group's entry if the call
      succeeds.

-  **ADD** **method** CreateGroupInDomain(String domain, String name)

   -  *domain*: the domain name in which the caller wants the group to
      be created
   -  *name*: the group's name
   -  returns: Path *group*: the path for the new group object
   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure
   -  Creates a group with the given name in the given domain. As with
      users, the GID is allocated by the provider, and the caller can
      retrieve it from the group's entry if the call succeeds.

-  **ADD** **method** DeleteGroup(Int group)

   -  *group*: the group ID of the group to be removed
   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure
   -  Deletes the group with the given GID.

-  **ADD** **method** DeleteGroupInDomain(String domain, Int group)

   -  *domain*: the name of the domain to which the group belongs
   -  *group*: the group ID of the group to be removed
   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure
   -  Deletes the group with the given GID.

-  **ADD** **method** ListCachedGroups()

   -  returns: *groups*: a subset of the known group objects
   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure

-  **ADD** **method** ListDomainGroups(String domain)

   -  *domain*: the domain name in which the caller is interested
   -  returns: *groups*: an array of paths for the group objects
      representing all of the groups of which SSSD is aware in the named
      domain

-  **ADD** **method** FindGroupById(Int64 id)

   -  *id*: the group's GID
   -  returns: Path *group*: the path for the group object
   -  Error *org.freedesktop.Accounts.Error.Failed*: no such group
      exists

-  **ADD** **method** FindGroupByIdInDomain(String domain, Int64 id)

   -  *id*: the group's GID
   -  *domain*: the group's domain name
   -  returns: Path *group*: the path for the group object
   -  Error *org.freedesktop.Accounts.Error.Failed*: no such group
      exists

-  **ADD** **method** FindGroupByName(String name)

   -  *name*: the group's name
   -  returns: Path *group*: the path for the group object
   -  Error *org.freedesktop.Accounts.Error.Failed*: no such group
      exists

-  **ADD** **method** FindGroupByNameInDomain(String domain, String
   name)

   -  *name*: the group's name
   -  *domain*: the group's domain name.
   -  returns: Path *group*: the path for the group object
   -  Error *org.freedesktop.Accounts.Error.Failed*: no such group
      exists

-  **ADD** **signal** GroupAdded(Path group)

   -  *path*: the path for the group's object
   -  this signal is emitted when a group is created or appears in the
      cache for a remote domain

-  **ADD** **signal** GroupDeleted(Path group)

   -  *path*: the path for the group's object
   -  this signal is emitted when a group is deleted or disappears from
      the cache for a remote domain, though the latter is not expected
      to happen often

-  **ADD** **method** ListDomains()

   -  returns: *domains*: a list of domain name strings

User Objects
^^^^^^^^^^^^

Users are represented by objects as well. The object path name used for
an object need not contain any identifying information about the user,
so no assumptions should be made about it. That all said, a typical user
object path is currently */org/freedesktop/Accounts/User500*.

User objects typically provide several properties, methods for setting
the properties which can be written to, and one signal, all grouped as
part of the *org.fredesktop.Accounts.User* interface:

-  **property** Boolean AutomaticLogin, **method**
   SetAutomaticLogin(Boolean enabled)

   -  Whether the user should be logged in automatically at boot.

-  **property** Boolean Locked, **method** SetLocked(Boolean locked)

   -  Whether the user's account is locked.

-  **property** Int AccountType, **method** SetAccountType(Int type)

   -  The type of the account. 0 is a *Standard* user, while 1 indicates
      an *Administrator*.

-  **property** Int PasswordMode, **method** SetPasswordMode(Int mode)

   -  Password flags. 0 is normal, 1 indicates that the password must be
      changed at next login, and 2 indicates that no password is
      necessary.

-  **property** Boolean SystemAccount

   -  Whether or not the account is a system account, such as *adm*.
      System accounts aren't returned by *ListCachedUsers* and should
      generally be ignored.

-  **property** String Email, **method** SetEmail(String email)

   -  The user's email address.

-  **property** String HomeDirectory, **method** SetHomeDirectory(String
   homedir)

   -  The user's home directory. If changed, the user's files are moved.

-  **property** String IconFile, **method** SetIconFile(String path)

   -  The user's icon file. Its contents are copied from the specified
      location to a location managed by the service, and when the value
      is read, the location of the service's copy is returned.

-  **property** String Language, **method** SetLanguage(String locale)

   -  The user's preferred language.

-  **property** String Location, **method** SetLocation(String where)

   -  The user's location, as a free-form string.

-  **property** String RealName, **method** SetRealName(String fullname)

   -  The user's real, full name.

-  **property** String Shell, **method** SetShell(String path)

   -  The user's login shell.

-  **property** String UserName, **method** SetUserName(String name)

   -  The user's login name.

-  **property** String XSession, **method** SetXSession(String session)

   -  The user's preferred graphical session, e.g. *gnome-fallback*.

-  **property** Int64 Uid

   -  The user's UID. Note that it is read-only.
   -  **MODIFY** this is allowed to not be set.

-  **property** Int64 LoginFrequency

   -  The user's login frequency. Currently this is the number of times
      the user appears in lastlog (or maybe utmp).

-  **property** String PasswordHint

   -  The user's password hint.

-  **ADD** **property** String Domain

   -  The user's domain.

-  **ADD** **property** Int CredentialLifetime

   -  The number of seconds left before the user's credentials expire,
      if the service is managing and monitoring some on the user's
      behalf.

-  **method** SetPassword(String crypted, String hint)

   -  Resets the password mode to normal.
   -  Unlocks the account.
   -  Currently takes a **crypt** string as a parameter.
   -  **ADD** Error
      *org.fedorahosted.SSSD.Error.PasswordMustBePlaintext*: this user's
      password must be set as plaintext by calling *SetAuthenticator*.

-  **ADD** **method** FindGroups(Boolean direct, Boolean indirect)

   -  *direct*: return groups which explicitly list the user as a member
   -  *indirect*: return groups which have the user as a member by
      virtue of having, as a member, a group which lists the user as a
      member
   -  returns: *groups*: an array of paths for the matched group objects

-  **signal** Changed()

   -  Emitted when the user's properties change.

-  Any attempt to change a property value can result in these errors:

   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure

-  **ADD** **method** Authenticate((Array of Bytes) handle, (Array of
   String) types, (Array of Struct(Int, Array of Variant)) responses)

   -  (Array of Bytes) *handle*: opaque *handle* returned by a previous
      call to Authenticate(), an empty array or a previously-obtained
      *info.session* value on the first call
   -  (Array of String) *types*: a list of enumerated types of
      information which the caller can supply (see below)
   -  (Array of Struct(Int id, (Array of Variant) data)) *responses*:
      array of responses to request for information returned by a
      previous call to Authenticate()

      -  *id*: an identifier specific to this request which identifiers
         information being provided in response to a particular item
         from a request
      -  *data*: the information being provided in response to a
         particular item requested by a previous call to Authenticate()

   -  returns (Array of Bytes) *handle*: an opaque handle used to track
      an ongoing authentication request
   -  returns Boolean *more*: true if more information is needed; false
      if authentication has succeeded (N.B.: failure is indicated by a
      D-Bus-level error)
   -  returns Int *timer*: amount of time the service is willing to wait
      for answers to its requests for information, in seconds
   -  returns (Array of Struct(Int id, String type, Variant prompt,
      Boolean sensitive, Signature format)) *requests*: information and
      requests for information

      -  *id*: an identifier specific to this request which should be
         used to identify the corresponding response when it is later
         provided
      -  *type*: a label which attempts to catalogue the various kinds
         of information which may be provided or requested

         -  *info.user*: user object (*prompt* is a Path), no input
            requested (*format* is ignored)
         -  *info.text*: user visible feedback (*prompt* is a String),
            no input requested (*format* is ignored)
         -  *input.text*: interactively-obtained string (*prompt* is a
            String, *format*\ =String)

            -  the service attempts to use this as infrequently as
               possible

         -  *input.boolean*: interactively-obtained boolean (*prompt* is
            a String, *format*\ =Boolean)

            -  the service attempts to use this as infrequently as
               possible

         -  *input.password*: current password (*prompt* is a String,
            *format*\ =String)
         -  *input.new-password*: new password value (*prompt* is a
            String, *format*\ =String)
         -  *input.otp*: current OTP value (*prompt* is a String,
            *format*\ =String)
         -  *input.otp-secret*: new OTP secret (*prompt* is a String,
            *format*\ =Array of Byte)
         -  *input.otp-next*: next OTP value (*prompt* is a String,
            *format*\ =String)
         -  *input.otp-new*: new OTP value (*prompt* is a String,
            *format*\ =String)
         -  *authz-data. ...*: authorization data returned on success,
            the portion of the name after *authz-data.* is namespaced
            either as an OID in text form or as a reversed domain name
            (resembling a D-Bus interface name)
         -  *info.cacheable*: an indicator that the calling application
            is willing to accept results based on non-live (i.e. cached)
            data
         -  *info.session*: a handle for any SSO credentials obtained
            during authentication (*prompt* is an Array of Bytes),
            returned only when authentication succeeds, no input
            requested; if the caller doesn't specify that it can accept
            a handle, any SSO credentials which are obtained as a
            side-effect of the authentication process (think: Kerberos
            TGTs) are discarded; if the caller receives a session
            handle, it accepts responsibility for eventually cleaning it
            up
         -  ...

      -  *prompt*: as indicated by and appropriate for *type*

         -  When an (Array of Byte) is expected, the *prompt* is usually
            empty or an (Array of Byte) and the application is expected
            to respond as indicated based only on *type*.

      -  *sensitive*: if the user is supplying the value, if the value
         is sensitive information.

         -  For example, passwords are often considered to be sensitive.

      -  *format*: the D-Bus type of the data which should be returned

         -  usually Boolean, Int64, String, or Array of Byte

      -  The overlap between *input.text* and various other input types
         is intentional, as it should allow applications and the service
         to share contextual information in cases where both support it,
         and to still be able to function (though at a less convenient
         level, programmatically) when one or the other is ignorant of
         the specifics of a particular authentication exchange. If a
         password is needed, for example, applications which advertise
         that they can provide both *input.text* and *input.password*
         will be prompted specifically for the password, while
         applications which only claim to be able to handle *input.text*
         will be prompted via that means. Hopefully this will provide
         some level of compatibility, even if it is less than ideal, as
         input types are added.
      -  As a rule, multiple requests for *input.text* type should not
         be assumed to be multiple requests for the same information,
         and *input.text* values should not be considered appropriate
         for being cached.
      -  The input type mechanism is notionally related to Kerberos
         preauthentication and authorization data, particularly in that
         some *requests* are merely informational, and attempts to
         provide a groundwork for eventually passing through binary
         methods such as GSSAPI.

-  **ADD** **method** CancelAuthentication((Array of Bytes) handle)

   -  (Array of Bytes) *handle*: opaque *handle* returned by a previous
      call to Authenticate()

-  **ADD** **method** ClearSession((Array of Bytes) handle)

   -  (Array of Bytes) *handle*: opaque *info.session* value returned by
      a previous call to Authenticate()
   -  Cleans up any resources being used to maintain the session's
      credentials

-  **ADD** **method** SelectSession((Array of Bytes) handle, (Array of
   String) types)

   -  (Array of Bytes) *handle*: opaque *info.session* value returned by
      a previous call to Authenticate()
   -  (Array of String) *types*: a list of types of returned information
      which the caller is able to usefully consume
   -  returns (Array of Struct(String type, Variant value)) *info*:
      information which the caller will need
   -  Makes previously-obtained SSO credentials available for use by the
      caller. When using Kerberos, the returned array includes an
      *environment* value of type *Array of String*, one of which is a
      KRB5CCNAME value which will be valid until the next time either
      *SelectSession* or *ClearSession* is called, or the
      *SessionCleared* signal is emitted. At this time, the only SSO
      credentials which SSSD "knows" how to obtain are Kerberos
      credentials, so the returned array will typically only contain an
      *environment* member, but this may grow to include other data
      items as additional authentication providers are added to SSSD.

-  **ADD** **method** SetAuthenticator((Array of Bytes) handle, (Array
   of String) types, (Array of Struct(Int, Array of Bytes)) responses)

   -  Same calling setup as *Authenticate*.

-  **ADD** **signal** AuthenticationOperationSucceeded((Array of Bytes)
   handle)

   -  Emitted when authentication or authenticator change succeeds.

-  **ADD** **signal** AuthenticationOperationFailed((Array of Bytes)
   handle)

   -  Emitted when authentication or authenticator change fails.

-  **ADD** **signal** AuthenticationOperationCanceled((Array of Bytes)
   handle)

   -  Emitted when authentication or authenticator change is canceled or
      times out.

-  **ADD** **signal** SessionExpiring((Array of Bytes) session, Int
   soon)

   -  Emitted when the user's SSO credentials will soon need to be
      refreshed, if the service is hanging on to and monitoring some on
      the user's behalf.
   -  (Array of Bytes) *session*: opaque *info.session* value returned
      by a previous call to Authenticate()
   -  Int *soon*: the amount of time left, in seconds, before the
      credentials expire.

-  **ADD** **signal** SessionCleared(Array of Bytes) session)

   -  (Array of Bytes) *session*: opaque *info.session* value returned
      by a previous call to Authenticate()
   -  Emitted when the user's credentials are either explicitly cleared
      or expire.

-  **ADD** **signal** SessionRefreshed((Array of Bytes) session)

   -  (Array of Bytes) *session*: opaque *info.session* value returned
      by a previous call to Authenticate()
   -  Emitted when the user's credentials are refreshed, if the service
      is managing and monitoring some on the user's behalf.

Group Objects (All New)
^^^^^^^^^^^^^^^^^^^^^^^

Going forward, groups, which were previously not exposed via this API,
will also be represented by objects. The object path name used for an
object need not contain any identifying information about the group, so
no assumptions should be made about it. That all said, a typical group
object path will be */org/freedesktop/Accounts/Domain2/Group500*.

Group objects will typically need to provide a few properties, methods
for setting the properties which can be written to, and one signal, all
grouped as part of the *org.fredesktop.Accounts.Group*, or more likely
an SSSD-specific, interface:

-  **ADD** **property** Boolean SystemGroup

   -  Whether or not the account is a system group, such as *adm*.
      System groups aren't returned by *ListCachedGroups* and should
      generally be ignored.

-  **ADD** **property** String IconFile, **method** SetIconFile(String
   path)

   -  The group's icon file. Its contents are copied from the specified
      location to a location managed by the service, and when the value
      is read, the location of the service's copy is returned.

-  **ADD** **property** String GroupName, **method** SetGroupName(String
   name)

   -  The group's name.

-  **ADD** **property** Int64 Gid

   -  The group's GID. This is read-only, optional, and is allowed to
      not be set.

-  **ADD** **signal** Changed()

   -  Emitted when the group's properties change.

-  **ADD** **property** String Domain

   -  The group's domain.

-  **ADD** **property** (array of Paths) Users

   -  An list of the group's member user objects.

-  **ADD** **property** (array of Paths) Groups

   -  An list of the group's member group objects.

-  **ADD** **method** AddUser(Path user)

   -  *user*: the object path of the user to add to the group's list of
      users
   -  If the user's domain and the group's domain are different, this is
      allowed to fail.

-  **ADD** **method** RemoveUser(Path user)

   -  *user*: the object path of the user to remove from the group's
      list of users

-  **ADD** **method** AddGroup(Path group)

   -  *group*: the object path of the group to add to the group's list
      of groups
   -  If the groups are not in the same domain, this is allowed to fail.
   -  If the domain does not support groups being members of groups,
      this will fail.

-  **ADD** **method** RemoveGroup(Path group)

   -  *group*: the object path of the group to remove from the group's
      list of groups

-  Any attempt to change a property value or alter membership can result
   in these errors:

   -  Error *org.freedesktop.Accounts.Error.PermissionDenied*: caller
      lacks appropriate PolicyKit authorization
   -  Error *org.freedesktop.Accounts.Error.Failed*: generic operation
      failure

Deficiencies
------------

-  No indication of primary group [mvo] (Current assumption: primary
   groups are not exposed.)
-  What are the semantics of system groups [mvo] (Current assumption:
   there is no concept of system groups.)
-  What are the semantics of cached groups [stefw]
-  Why are domains not first class DBus objects [stefw]
-  Does the local domain have a special value/identifier/path? [mvo]
   (Current assumption: empty string, but there is also LocalGroup,
   similar to LocalUser.)
-  We should have FindGroups also on Group objects. [mvo]
-  'direct' argument to FindGroups seems unmotivated. [mvo]
