SSSCTL - a CLI tool to control and monitor SSSD
===============================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/385 <https://pagure.io/SSSD/sssd/issue/385>`__
-  `https://pagure.io/SSSD/sssd/issue/1788 <https://pagure.io/SSSD/sssd/issue/1788>`__
-  `https://pagure.io/SSSD/sssd/issue/1828 <https://pagure.io/SSSD/sssd/issue/1828>`__
-  `https://pagure.io/SSSD/sssd/issue/2166 <https://pagure.io/SSSD/sssd/issue/2166>`__
-  `https://pagure.io/SSSD/sssd/issue/2954 <https://pagure.io/SSSD/sssd/issue/2954>`__
-  `https://pagure.io/SSSD/sssd/issue/2957 <https://pagure.io/SSSD/sssd/issue/2957>`__

Problem statement
~~~~~~~~~~~~~~~~~

Main purpose of this task is to make administration & debugging tasks
more user friendly and thus hopefully save time of users, support and
developers.

SSSCTL will be CLI client using the SSSD infopipe as a server that will
be providing necessary data and will perform/delegate commands to the
SSSD providers and responders.

Use cases
~~~~~~~~~

-  online/offline state
   (`https://pagure.io/SSSD/sssd/issue/385 <https://pagure.io/SSSD/sssd/issue/385>`__).
   Users have repeatedly asked for simple mean how to check if data
   provider is offline or online without need to check logs (if logging
   is enabled at all).
-  Report whether the entry is present in SSSD cache
   (`https://pagure.io/SSSD/sssd/issue/2166 <https://pagure.io/SSSD/sssd/issue/2166>`__)
-  Check if the cached entry is valid and refresh if appropriate
   (`https://pagure.io/SSSD/sssd/issue/2166 <https://pagure.io/SSSD/sssd/issue/2166>`__)
-  Measure the time an operation took (useful in performance tuning,
   `https://pagure.io/SSSD/sssd/issue/385 <https://pagure.io/SSSD/sssd/issue/385>`__)
-  Failover status - Current state of failover process
-  Display server to which provider is connected to
   (`https://pagure.io/SSSD/sssd/issue/385 <https://pagure.io/SSSD/sssd/issue/385>`__)
-  Display current debug level of a component
-  Generate memory report - Usually when user is observing a memory leak
   we provide him a special build that generates talloc report which we
   can then analyze. Using this tool customer would simply select SSSD
   component that is supposed to leak memory and generate the talloc
   report immediately.
-  Removing cache - Removing SSSD cache seems to be often misused act
   done by administrators as there are few real needs for that.
   Nevertheless, if administrator decides to remove the cache it would
   be better to do this using the tool instead of crude removing
   directories that might contain other useful data and could lead to
   serious problems. Q: Is this what was requested as 'force reload'? Q:
   Should this rather be part of sss\_cache tool?

Tool interface
~~~~~~~~~~~~~~

The up-to-date list of all available commands can be printed with ::

    # sssctl --help

Domain information
^^^^^^^^^^^^^^^^^^

List of all domain available within SSSD can be obtain with the
following command. ::

    # sssctl domain-list

We can also get more information about specific domain. ::

    # sssctl domain-status $domain [--online, --last-request, --active-server, --servers]
    Online status: Online/Offline
    Active server: $currently-connected-server (server status, port status, resolver status)

    Primary servers:
        first.example.com (server status, port status, resolver status)
        second.example.com (server status, port status, resolver status)

    Backup servers:
        first.example.com (server status, port status, resolver status)
        second.example.com (server status, port status, resolver status)

    10 most recent requests:
    $req-name: started at XXX, finished at XXX, total duration XXX, success/error/...
    ...

If a parameter is present only selected part will be printed.

Information about cached entry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unless we want to use dn, we need to specify whether we want to work
with user/group/sudo/..., interface for user follows, other object may
be done similarly. ::

    # sssctl user-show $objname
    User $objname is not present in cache.

    # sssctl user-show $objname
    Cache entry creation date: XXX
    Cache entry last update date: XXX
    Cache entry expiration date: XXX

To force an update of the cached entry: ::

    # sssctl user-show $objname --update

Debug level
^^^^^^^^^^^

::

    # sssctl logs-level [--monitor --nss --pam ... --domain $domain]
    Monitor: 0x00f0
    NSS responder: 0x3ff0
    ...
    Domain $domain: 0xfff0

Optionally we can provide a debug level to set (taking over
sss\_debuglevel tool, since we already have D-Bus functionality in
place). ::

    # sssctl logs-level [--monitor --nss --pam ... --domain $domain] $new-level
    Monitor: 0x00f0
    NSS responder: 0x3ff0
    ...
    Domain $domain: 0xfff0

If a parameter is present only selected components are shown/changed.

Talloc report
^^^^^^^^^^^^^

::

    # sssctl memory-report [--monitor --nss --pam ... --domain $domain] $file

If a parameter is present memory report is generated only for selected
components.

Cache operations
^^^^^^^^^^^^^^^^

::

    # sssctl client-data-backup [--dir=$outputdir] [--force]

This command will backup all local data that are not present on the
server such as local view and local users. If an *$outputdir* is
specified data will be stored there otherwise */var/lib/sss/backup* will
be used. If *--force* option is specified than the existing backup is
replaced with the new one.

::

    # sssctl client-data-restore [--dir=$outputdir]

Restore local data with the content stored in *$outputdir*.

::

    # sssctl cache-remove

Remove SSSD cache database files, however in a manner that will backup
all local data so it can be restored later. The user is notified that
removing the cache will destroy all cached data and it is therefore not
recommended to do it in offline mode.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

We will create a new administrator tool called **sssctl**. This tool
will communicate with **InfoPipe** responder through its **public D-Bus
interface**. The InfoPipe will then internally forward the messages to
other SSSD components as necessary.

In cases where **sssctl** can be replaces with combination of existing
SSSD or system tools we will just call those tools directly through
system call or through their API if exist. For example the remove cache
operation is a sequence of: *sss\_override user-export
$dir/view\_users.bak && sss\_override group-export $dir/view\_groups.bak
&& rm -f /var/lib/sss/db/\** so we can just call those programs.

Questions
~~~~~~~~~

-  **Q1**: [Domain; Last request] What would be preferred number of
   request to be printed? Do we want a parameter for this in sssd.conf
   or even make it possible to change this value dynamically?

   -  Start with fixed number of 10 request and keep it unless a bigger
      requirement comes.

-  **Q2**: [Domain; Server list] Is it enough to print only active
   server or do we want full list of primary and backup servers as well?

   -  Print full list containing also discovered servers.

-  **Q3**: [Domain; Server list] Do we want to also print IP addresses?

   -  Not needed.

-  **Q4**: [Talloc report] Should we provide parameter $file or should
   we hardcode the path as SSSD logs directory, generating name from
   component and time?

   -  Provide a file parameter but default to log directory.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

No configuration changes.

How To Test
~~~~~~~~~~~

Not at the moment.

How To Debug
~~~~~~~~~~~~

Not at the moment.

Authors
~~~~~~~

Pavel Reichl <`preichl@redhat.com <mailto:preichl@redhat.com>`__>
Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
