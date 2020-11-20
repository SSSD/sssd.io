GPO-Based Access Control
========================

Problem Statement
-----------------

A common use case for managing computer-based access control in an AD
environment is through the use of GPO policy settings related to Windows
Logon Rights. This design page proposes adding support for this use case
by enhancing the SSSD AD provider to include the GPO support necessary
for this access control use case. We are not currently planning on
supporting other GPO-based use cases.

Use Cases
---------

Administrator, who maintains a heterogenous AD and RHEL network is able
to define login policies in one central place -- on the AD DC. The same
policies will be then honored by his RHEL clients and Windows clients
alike. Mapping between interactive or remote Windows logon methods and
RHEL PAM services has sensible defaults and can be customized further.

Proposed Solution
-----------------

.. FIXME: GPO Overview hasn't been migrated yet.
.. This link should be fixed whenever it happens.

.. For a general overview of GPO technology, visit `GPO
.. Overview <link here>`__

For a general overview of Windows Logon Rights, visit
`http://technet.microsoft.com/en-us/library/cc976701.aspx <http://technet.microsoft.com/en-us/library/cc976701.aspx>`__

GPO policy settings can be used to centrally configure several sets of
Windows Logon Rights, with each set classified by its logon method (e.g.
interactive, remote interactive) and consisting of a whitelist [and
blacklist] of users and groups that are allowed [or denied] access to
the computer using the set's logon method. In order to integrate Windows
Logon Rights into a GNU/Linux environment, we allow pam service names to be
mapped to a specific Logon Right. We provide default mappings for all of
the commonly used pam service names, but we also allow the admin to
add/remove mappings as needed (to support custom pam service names, for
example). The latter is done by using a new set of config options of the
form "gpo\_map\_<logon\_right>" (i.e. gpo\_map\_interactive,
gpo\_map\_network, etc), each of which consists of a comma-separated
list of entries beginning either with a '+' (for adding to default set)
or a '-' (for removing from default set). For example, since the
RemoteInteractive logon right maps to a single pam service name ("sshd")
by default, an admin could map their own pam service name
("my\_pam\_service") and remove the "sshd" mapping with the following
sssd.conf line: "gpo\_map\_remote\_interactive = +my\_pam\_service,
-sshd"

For this project, the following options can be used to configure the
corresponding Logon Right (default values are also given):

-  ad\_gpo\_map\_interactive (default: login, su, su-l, gdm-fingerprint,
   gdm-password, gdm-smartcard, kdm)
-  ad\_gpo\_map\_remote\_interactive (default: sshd)
-  ad\_gpo\_map\_network (default: ftp, samba)
-  ad\_gpo\_map\_batch (default: crond)
-  ad\_gpo\_map\_service (default: <not set>)
-  ad\_gpo\_map\_permit (default: sudo, sudo-i)
-  ad\_gpo\_map\_deny (default: <not set>)
-  ad\_gpo\_map\_default\_right (default: deny)

The first five options are used to associate specific pam service names
with each logon right. The ad\_gpo\_map\_permit [and ad\_gpo\_map\_deny]
is used to specify pam service names for which GPO-based access is
always [or never] granted. Unlike the other options, the
ad\_gpo\_map\_default\_right does not specify pam service names. Rather,
it allows the admin to specify a default logon right (or the special
permit/deny values)for pam service names that are not explicitly mapped
to any of the logon rights. Note that, in many cases, we do not expect
the admin will need to specify any of these config options, b/c the
defaults have been chosen carefully to cover the most commonly used pam
service names (with deny as the default for unmapped service names).

The semantics of each whitelist and blacklist are as follows:

-  whitelist ("allow"): When this policy setting is not defined, any
   user can logon to the computer. When it is defined, only the users
   and groups specified in the whitelist are allowed to logon to the
   computer. In other words, by defining this setting, the semantics go
   from "everyone allowed access to this computer" to "no one allowed
   access to this computer, except principals on the whitelist".
-  blacklist ("deny"): When this policy setting is not defined, it has
   no effect. When it is defined, the users and groups specified in the
   blacklist are blocked from performing logons. For a particular Logon
   Right (e.g. Interactive), if a user/group is specified in both the
   whitelist and the blacklist, then the blacklist takes precedence.

In summary, if a user is trying to login to a computer (e.g.
pam\_service\_name = "login"), we first find which Logon Right the
"login" service maps to (i.e. Interactive, by default), and then process
only the corresponding policy settings found in GptTmpl.inf (which
contains policy settings for the "Security Settings" extension, of which
Logon Rights are a part). In the case of Interactive Logon Right, those
policy settings are named *SeInteractiveLogonRight* and
*SeDenyInteractiveLogonRight* in the GptTmpl.inf file.

A client-side implementation consists of the following components:

-  LDAP Engine: determines which GPOs are applicable for the computer
   account from which the user is attempting to log in, filters those on
   various criteria, and ultimately produces a set of cse\_filtered GPOs
   that contain the "Security Settings" CSE, which it feeds, one by one,
   to the SMB/CIFS Engine
-  SMB/CIFS Engine: makes blocking libsmbclient calls to retrieve each
   GPO's GPT.INI and GptTmpl.inf files, and stores the files in the GPO
   cache (/var/lib/sss/gpo\_cache), from which the GPO Enforcement
   Engine will retrieve them
-  GPO Enforcement Engine: enforces GPO-based access control by
   retrieving each GPO's policy file (GptTmpl.inf) from the GPO cache,
   parsing it, and making an access control decision by comparing the
   user/groups against the whitelist/blacklist of the Logon Right of
   interest (which is based on the pam service name)

For the sake of clarity, the above description ignores some features,
such as GPO version caching/comparing, and offline support.

Implementation Details
----------------------

Packaging
^^^^^^^^^

Since the GPO-based access control feature will only be used by the AD
provider, it will be included as part of the sssd-ad package. The source
files for the feature would be included as part of libsss\_ad.so. In
order to ensure that existing configurations do not see changes in
behavior when upgrading, this feature will not be enabled by default.
Rather, a new "ad\_gpo\_access\_control" config option is provided which
can be set to "disabled" (neither evaluated nor enforced), "enforcing"
(evaluated and enforced), or "permissive" (evaluated, but not
enforced).The "permissive" value is the default, primarily to facilitate
a smooth transition for administrators; it evaluates the GPO-based access
control rules and outputs a syslog message if access would have been
denied. By examining the logs, administrators can then make the
necessary changes before setting the mode to "enforcing".

In addition to the new ad\_gpo\_access\_control and ad\_gpo\_map\_\*
config options, there is also a new config option named
ad\_gpo\_cache\_timeout, which can be used to specify the interval
during which subsequent access control requests can re-use the files
stored in the gpo\_cache (rather than retrieving them from the DC).

GPO Retrieval
^^^^^^^^^^^^^

-  LDAP Engine (running in backend): This component runs as part of the
   AD access provider. It does the following:

   -  Determines which GPOs are applicable to the computer account from
      which the user is attempting to log in. This is based on:

      -  whether the GPO is linked to the site/domain/ou under which the
         computer account is stored
      -  whether the GPO is enabled or disabled
      -  whether the GPO is enforced or unenforced
      -  whether or not the GPO is allowed to be inherited from parent
         containers
      -  whether the user has the ApplyGroupPolicy permission on the
         GPO's DACL

   -  Retrieves relevant attributes of applicable GPOs (e.g. cse-guids,
      file\_system\_paths, etc)
   -  Extracts supported GPOs (i.e. those with "Security Settings" cse)
      from the applicable GPOs
   -  For each supported GPO

      -  Retrieves the GPO's version and timeout from the sysdb cache
         (from a previous transaction, if any)
      -  If timeout is greater than current time, then skips to GPO
         Enforcement
      -  Else, sends to the gpo\_child the supported GPO, as well as the
         cached GPO version (if any)

-  SMB/CIFS Engine (gpo\_child): This component is used to make blocking
   SMB/CIFS calls. It does the following:

   -  Retrieves the GPO's corresponding GPT.INI file (from which it
      extracts the fresh version)
   -  If the fresh version is greater than the cached version (or if
      there is no cached version)

      -  Retrieves the policy file corresponding to the GPO
         (GptTmpl.inf) and saves it to the GPO cache
         (/var/lib/sss/gpo\_cache)
      -  Returns the fresh version to the backend, which stores it in
         the cache

GPO Enforcement
^^^^^^^^^^^^^^^

-  GPO Enforcement Engine: enforces GPO-based access control (note that
   this will take place after existing AD access provider mechanisms,
   such as account lockout, LDAP filter)

   -  For each GPO

      -  Retrieves GPO's corresponding policy file (i.e. GptTmpl.inf)
         file from GPO cache
      -  Parses policy file, extracting entries corresponding to the
         Logon Right of interest (determined by the pam service name)
      -  Enforces access control policy settings

Cache Schema
^^^^^^^^^^^^

The Cache stores entries for individual GPOs in a new container
"cn=gpos, cn=ad, cn=custom, cn=<domain>, cn=sysdb" ::

      // GPOs
      dn: "name=<gpo-guid1>,cn=gpos,cn=ad,cn=custom,cn=<domain>,cn=sysdb"
      gpoGUID: <gpo-guid1>            (string)
      gpoVersion: <version>           (integer)
      objectClass: "gpo"
      gpoPolicyFileTimeout: <timeout> (integer)

Refresh Interval Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Microsoft specifies that there be separate configurable refresh
intervals (one for computer-based GPOs and one for user-based GPOs),
with each having a default of 90 minutes. If 0 minutes are specified,
Microsoft uses a 7-second refresh interval. Additionally, in order to
avoid performance degradation that could occur if several computers
perform a group policy refresh simultaneously, Microsoft also specifies
that a random offset interval be added to the refresh interval, with the
maximum offset interval having a default of 30 minutes. As such, there
are four settings (computer-based refresh interval, computer-based
maximum offset interval, user-based refresh interval, user-based maximum
offset interval). Additionally, Microsoft specifies a boolean
configuration setting that disables refresh altogether (in which case
none of the previous four configuration settings would be relevant). If
refresh is completely disabled, then GPOs would only be retrieved at
computer startup (or user login). One final note: the GPO mechanism
itself can be used to uniformly set these refresh configuration options
for a set of computers; namely, Microsoft specifies standard GPO policy
settings that can used to centrally specify the various refresh
parameters. Of course, these would not apply until after they had been
retrieved.

Although we are only implementing a computer-based GPO in the first
implementation, we should keep in mind that user-based GPOs could have a
different refresh interval. As such, we would need to add a new
configuration option ("computer\_gpo\_refresh\_interval") to the
existing AD access provider that would specify the GPO retrieval refresh
interval in seconds. This would specify the period to use in the
periodic task API to determine how often to call the GPO retrieval code.
By default, Microsoft sets this value to 90 minutes. It is an open issue
as to whether we want to support the random offset interval or the
ability to disable refresh altogether.

Unresolved Issues
-----------------

When should GPO retrieval take place? It could happen at one or more of
the following times:

-  If we follow the Microsoft spec, since "Allow / Deny Logon Locally"
   are computer-based policy settings, GPO retrieval should take place
   when the system boots and at regular refresh intervals. If we assume
   system boot effectively coincides with sssd initialization (for our
   purposes), we can retrieve the policy settings during ad\_init and
   kick off a periodic task (similar to what we do for enumeration).
   However, this will likely have an adverse performance impact on
   system startup.
-  Alternatively, we can perform GPO retrieval in the AD access provider
   itself (just before enforcing the policy settings), meaning that
   retrieval would take place at every user login. This would ensure
   that the freshest policy settings were being applied at every logon.
   If we only performed GPO retrieval at this point, then periodic
   refresh would not be needed (at least for the "Allow / Deny Logon
   Locally" policy settings) since we are getting fresh data every time.
-  Additionally, we could register an online callback such that GPO
   retrieval takes place when returning to online mode from offline
   mode. This really depends on what we decide about the first two
   retrieval times above. If we aren't doing periodic refresh, and are
   only retrieving GPOs at login time, then an online callback might
   not be needed. If we are doing periodic refresh, then we can set the
   "offline" parameter of be\_ptask\_create(...) to DISABLE (which means
   the task is disabled immediately when back end goes offline and then
   enabled again when back end goes back online). Or we can play it safe
   and always use DISABLE semantics (regardless of when GPO retrieval
   takes place).

Should we enforce GPO logon policy settings only at user login, or also
at periodic intervals?

-  After a user has logged on successfully using GPO-based access
   control, if new policy settings are retrieved during refresh
   indicating that the user is no longer allowed to log in to this host,
   should sssd log out the user (or should we only enforce the access
   control at login time)? What do our other access control mechanisms
   do here? If we wanted to log out the user, do we have an existing
   mechanism to do this?

If we implement GPO refresh, which of the refresh configuration options
should we implement and how?

-  sssd configuration options

   -  computer\_gpo\_refresh\_interval? If we use sssd configuration, we
      would definitely want this one (although maybe with a shorter
      name).
   -  computer\_gpo\_max\_offset (default 30 minutes)? Do we think this
      random offset adds enough value to be a configurable option?
   -  disable\_gpo\_refresh (default false)? Presumably, this would be
      done so that performance would not be adversely affected during
      the logon session. Alternatively, we could tell admins that wanted
      to disable GPO refresh to set the
      entry\_cache\_computer\_gpo\_timeout to zero (0), although this
      would not be how Microsoft interprets a zero value. Does sssd
      interpret '0' as "disable" elsewhere?

-  GPO refresh interval GPO

   -  if we didn't want to clutter sssd's configuration namespace, we
      could just use the standard Microsoft GPO that allows an admin to
      specify the aforementioned refresh intervals (and distribute a
      consistent configuration to a set of computers)

Options
-------

Option 1: The straightforward option is to only perform GPO retrieval in
the AD access provider itself.

-  Pros

   -  provides just-in-time retrieval (yielding fresh data)
   -  does away with need for periodic refresh and refresh configuration
   -  no performance hit at system startup (and at periodic refresh)

-  Cons

   -  suffers a performance hit on every user login
   -  doesn't allow us to perform user logout (if policy settings no
      longer allow access)

Option 2: The spec-compliant option is to perform GPO retrieval (and
take the performance hit) at system start and then at periodic
intervals.

-  Pros

   -  complies with spec
   -  no performance hit at every user login
   -  allows us to perform user logout (if policy settings no longer
      allow access)

-  Cons

   -  suffers performance hit at initial startup and then periodically
   -  policy data likely to be stale
   -  requires implementation of periodic refresh, including refresh
      configuration (for which we should probably use GPO refresh GPO)

Recommendation
--------------

In order to avoid premature optimization, the team's recommendation is
to start by implementing the straightforward approach (Option 1), and to
address potential performance concerns later (when we will be able to
make actual measurements).

Configuration Changes
---------------------

The following new options are added to the AD access provider. Kindly
see the sssd-ad man page for a complete description.

-  ad\_gpo\_access\_control - describes the operation mode of access
   control (enforcing/permissive/disabled)
-  ad\_gpo\_cache\_timeout - amount of time between lookups of GPO files
   on the AD server
-  ad\_gpo\_map\_interactive - PAM services that map onto
   InteractiveLogonRight and DenyInteractiveLogonRight
   policy settings.
-  ad\_gpo\_map\_remote\_interactive - PAM services that map onto
   RemoteInteractiveLogonRight and DenyRemoteInteractiveLogonRight
   policy settings.
-  ad\_gpo\_map\_network - PAM services that map onto
   NetworkLogonRight and DenyNetworkLogonRight policy settings.
-  ad\_gpo\_map\_batch - PAM services that map onto
   BatchLogonRight and DenyBatchLogonRight policy settings.
-  ad\_gpo\_map\_service - PAM services that map onto
   ServiceLogonRight and DenyServiceLogonRight
   policy settings.
-  ad\_gpo\_map\_permit - PAM service names for which GPO-based access
   is always granted
-  ad\_gpo\_map\_deny - PAM service names for which GPO-based access is
   always denied
-  ad\_gpo\_map\_default\_right - defines how access control is
   evaluated for PAM service names that are not explicitly listed in one
   of the ad\_gpo\_map\_\* options.

How to test
-----------

-  Perform the following tests for each set of Logon Rights (not just
   for Interactive, as shown)

   -  Setup

      -  Create AD users named allowed\_user, denied\_user,
         regular\_user, allowed\_group\_user, denied\_group\_user,
         allowed\_denied\_group\_user
      -  Create AD groups named allowed\_group, denied\_group
      -  Set allowed\_group\_user and allowed\_denied\_group\_user as
         members of allowed\_group
      -  Set denied\_group\_user and allowed\_denied\_group\_user as
         members of denied\_group
      -  Create GPO with two policy settings (in this case, we are using
         Interactive Logon Right as an example)

         -  "Allow Logon Locally" is set to "allowed\_user",
            "allowed\_group"
         -  "Deny Logon Locally" is set to "denied\_user" ,
            "denied\_group"

   -  Link GPO to specific site, domain, or OU node (under which the
      host computer resides in AD)

-  Perform the following "standard test" using each logon method
   (corresponding to each Logon Right). For example, we can use "ssh" to
   test the RemoteInteractive Logon Right on a single computer
   (localhost)

   -  [yelley] $ ssh allowed\_user@foo.com@localhost
   -  Note that "allowed\_user" and "allowed\_group\_user" should be
      granted access
   -  Note that "regular\_user", "denied\_user", "denied\_group\_user",
      and "allowed\_denied\_group\_user" should be denied access

-  Create a new computer account in a location which should have no
   linked GPOs in the AD hierarchy (site, domain, ou)

   -  (Alternatively, use the same computer account, but disable any
      applicable GPOs using GPMC; make sure to re-enable them after this
      step!!)
   -  Perform standard test and make sure that all users are able to log
      in to host (since no GPOs apply to this host)

-  Offline Mode

   -  take the system offline with no files in the gpo\_cache directory;
      perform standard test and make sure it grants access
   -  perform the standard test while online (download some files); then
      take the system offline and make sure it behaves as expected

-  Test ad\_gpo\_access\_control config option

   -  perform standard tests when this option is "permissive" (or
      unspecified), "enforcing", "disabled"

-  Test ad\_gpo\_cache\_timeout config option

   -  perform standard test with a sysdb cache with no GPO entries (or a
      clean sysdb cache)
   -  make a change to a GPO policy setting so that the
      sysvol\_gpt\_version is incremented

      -  perform standard test and make sure that the timestamps on
         GPT.INI and GptTmpl.inf have changed

   -  using a large value for this option (300 seconds), perform
      standard test again within the timeout period; make sure the
      timestamps on GPT.INI and GptTmpl.inf have not changed
   -  using the default value for this option (5 seconds), perform
      standard test again after the timeout period; make sure the
      timestamp on GPT.INI has changed, but not the timestamp on
      GptTmpl.inf (since no policy change was made in AD)

-  Test ad\_gpo\_map\_\* config options

   -  perform standard tests after adding pam service names to default
      set using '+'
   -  perform standard tests after removing pam service names from
      default set using '-'
