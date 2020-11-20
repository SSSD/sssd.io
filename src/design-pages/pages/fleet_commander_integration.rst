.. highlight:: none

Fleet Commander Integration
===========================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/2995

Problem statement
-----------------
FleetCommander is a service to centrally manage Desktop environments. It
includes a server to define desktop profiles and a client to apply
profile information to the user's desktop session on a specified
machine.

This design document describes the SSSD part of an integration of
FleetCommander with FreeIPA. The integration is done two-fold, the IPA
part of the integration is https://github.com/abbra/freeipa-desktop-profile/blob/master/plugin/Feature.mediawiki

Use cases
---------
As an administrator, I want to manage desktop profiles in a centralized
way

As an administrator, I want to use centrally defined users, groups,
hosts and host groups to specify how desktop profiles should be applied.

As an administrator, I want to make sure desktop profiles associated
with a specific user or user group are downloaded and applied on a
specific FreeIPA client according to the desktop profile rules defined
in FreeIPA.

Overview of the solution
------------------------
FleetCommander consists on two components:
 * a Cockpit plugin that connects to the FreeIPA and sets up profiles
   for different users.
 * a client side component activated by SSSD, which applies all the
   profiles retrieved by the latter.

Since this design page deals with the client side of the whole picture,
this paragraph will focus on the integration of the FC client side
component with SSSD.

The FC profiles will be downloaded by a new ``session_provider`` of IPA.
This provider will be enabled by default and can be disabled by setting
``session_provider = none``.

When a FreeIPA domain user logs in, the IPA provider will download the
Fleet Commander profile and rule objects and drop the resulting JSON
files into a per-user directory. The file names must be normalized and
prepended with priority (please refer to the IPA design page for more
details) and the FC client will be DBus activated by SSSD.

In the future, we would like to link the Fleet Commander profiles with
HBAC rules, but the first implementation will not include this part.

Implementation details
----------------------

Looking up the Fleet Commander profiles and storing the JSON profile data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Similar to how we look up and store sudo and HBAC rules, we will look up
all profiles that apply to this host, with::

    (&(objectclass=ipadeskprofilerule)(|(memberHost=my_fqdn)(memberHost=my_hostgroup1)(memberHost=my_hostgroup2)...(memberUser=group1)(memberUser=group2)...))

All host groups the IPA client is a member of must be included in the
``memberHost`` part of the filter. However, since in the typical
scenario, sessions provider will be called after HBAC or SELinux
processing was done, the host and host groups will be usually already
cached and can be just reused from the cache.

Once all profiles are cached, processing and selection of the profiles
that apply to the user logging in would be done offline. Again, this is
similar to how we process sudo or HBAC rules. The local search's filter
will look for the user and all his groups. For performance reasons, we
need to check if initgroups was performed prior to looking up the
profiles and only issue another initgroups request if the user entry's
initgroup timestamp is expired.

The profiles will also be stored in the cache to allow offline
processing. As an additional enhancement, we can skip writing the
profile data to the cache if the remote data has not changed. We can
take a look at the ``modifyTimestamp`` attribute value to see if any of
the entries need an update in the cache.

The LDAP search will include the Fleet Commander payload data in the
profile's ``data`` attribute. Once the data are known, SSSD will write
them to the disk. Since writing to the disk is typically quite fast

The JSON files will be stored in a new directory owned by the
``sssd-ipa`` subpackage. The top-level directory could be at
``/var/lib/sss/deskprofile/`` with per-user subdirectories. So each
per-user JSON file would be stored at
``/var/lib/sss/deskprofile/<domain>/<username>/<profilename>.json``.
The ``<username>`` directories need to be owned by the user being logged in.

The structure of the the created dirs follow::

    /var/lib/sss/deskprofile/<domain>/<username>/<profilename>.json
                ------------ -------- ---------- ------------------
                     |          |          |            |
                     v          |          |            |
    Created by sssd package as  |          |            |
    root:root (or sssd:sssd)    |          |            |
    and has permissions 0751    |          |            |
                                |          |            |
                                v          |            |
                Owned by user:user_group   |            |
                and has permissions 0751   |            |
                                           |            |
                                           |            |
                                           v            |
                        Owned by user:user_group        |
                        and has permissions 0700        |
                                                        |
                                                        v
                                        Owned by user:user_group
                                        and has permissions 0400

Please, keep in mind that this feature relies on CAP_SETUID and
CAP_SETGID to properly work as expected and relies on SSSD being run
as privileged user (root).

The ``<profilename.json>`` file must include the priority as a number
which is read from the rule's ``prio`` attribute. The Fleet Commander
client component will then process the JSON files in this priority. The
filenames must also be normalized so that characters with a special
meaning in shell are escaped and spaces are converted to another
character such as underscores. Please refer to the IPA design page for
more details.

In the first version, the profiles will always be written again. In the
future, we might want to optimize the process further by only writing
the JSON profiles if they differ from what's already stored on the disk.
This might be doable by storing the modifyTimestamp in the JSON profiles
again, if FC is able to ignore certain JSON key-value pairs that would
be private to SSSD or just storing the largest USN value of the found
profiles in the included directory in a specially-named file.

During implementation, as much code as possible should be reused from
the IPA HBAC access code and/or SELinux rule processing code.

Configuration changes
---------------------
Two new configuration options will be added:

 * ``session_provider`` that will be inherited from the ``id_provider``
   value, so for IPA clients, this provider will default to ``ipa``. A
   default ``session_provider`` for other providers will just shortcut
   and return success.

Disabling the IPA session provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Since searching for the Fleet Commander profiles does not come for free
- at least one LDAP search must be issued, perhaps more unless we cache
the host groups, and this functionality will be enabled by default in
order to have it working "out of the box" for Fleet Commander's users,
we should keep a way to disable the functionality if needed. It can be
easily done by setting ``session_provider = none``, under the
domain's section, in the ``sssd.conf`` file.

How To Test
-----------
Please see the use-cases above.

How To Debug
------------
DEBUG messages will be added to the new session provider so that the
admin can trace if the session provider was invoked at all. An easy way
to debug the integration is to enable the sessions provider and the
FleetCommander integration manually w/o dropping the file by the FC
client side component.

Authors
-------
 * Alexander Bokovoy
 * Jakub Hrozek
