.. highlight:: none

"Files" data provider to serve contents of ``/etc/passwd`` and ``/etc/group``
=============================================================================

Related ticket(s):

-  The umbrella tracking ticket:
   `https://pagure.io/SSSD/sssd/issue/2228 <https://pagure.io/SSSD/sssd/issue/2228>`__

which includes the following sub-tasks:

-  Ship an immutable recovery mode config for local accounts -
   `https://pagure.io/SSSD/sssd/issue/2229 <https://pagure.io/SSSD/sssd/issue/2229>`__
-  [RFE] Support UID/GID changes -
   `https://pagure.io/SSSD/sssd/issue/2244 <https://pagure.io/SSSD/sssd/issue/2244>`__
-  Provide a "writable" D-Bus management API for local users -
   `https://pagure.io/SSSD/sssd/issue/3242 <https://pagure.io/SSSD/sssd/issue/3242>`__

Problem statement
~~~~~~~~~~~~~~~~~

SSSD does not behave well with nscd, so we recommend that it be
disabled. However, this comes with a price in the form of every
nameservice lookup hitting the disk for ``/etc/passwd`` and friends
every time. SSSD should be able to read and monitor these files and
serve them from its cache, allowing ``sss`` to sort before ``files`` in
``/etc/nsswitch.conf``

In addition, SSSD provides some useful interfaces, such as `the dbus
interface <https://docs.pagure.org/SSSD.sssd/design_pages/dbus_users_and_groups.html>`__
which only work for users and groups SSSD knows about.

Use cases
~~~~~~~~~

Use Case: Default Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SSSD (and its useful APIs) should always be available. This means that
SSSD must ship with a default configuration that works (and requires no
manual configuration or joining a domain). This default configuration
should provide a fast in-memory cache for all user and group information
that SSSD can support, including those traditionally stored in
``/etc/passwd`` and friends.

Use Case: Programatically managing POSIX attributes of a user or a group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently the available ways to manage users and groups is either spawn
and call shadow-utils binaries like ``useradd`` or libuser. SSSD already
has a D-Bus API used to provide custom attributes of domain users. This
interface should be be extended to provide 'writable' methods to manage
users and groups from files. This is tracked by `ticket #3242
<https://pagure.io/SSSD/sssd/issue/3242>`__

Use Case: Manage extended attributes of users and groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some applications (such as desktop environments) additional attributes
(such as keyboard layout) should be stored along with the user. Since
the passwd file has only a fixed number of fields, it might make sense
to allow additional attributes to be stored in SSSD database and
retrieved with sssd's D-Bus interface. Again, this is tracked by
`ticket #3242 <https://pagure.io/SSSD/sssd/issue/3242>`__

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

.. FIXME: Add a link to the INI config merge design page in line 78

SSSD should ship a ``files`` provider as part of its required minimal
package. Absent any user modifications, SSSD should be configured to
start at boot and use this provider to serve local identity information.

This provider may or may not be optional. For example, we might decide
that it always exists as the first domain in the list, even if not
explicitly specified. Alternatively, distributions that wish to always
include the files provider will be able (starting with SSSD 1.14 and its
config merging feature to drop a definition of the files provider into
``/etc/sssd/conf.d``. In order for this functionality to work, we would
have to deprecate the ``domains`` line and instead load all
``[domain/XXXX]`` sections from all available sources, unless the
``domains`` line is specified for backwards-compatibility.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

Upon SSSD startup, the ``files`` provider will always run a complete
enumeration pass on the ``/etc/passwd``, ``/etc/group`` and other files
as appropriate. The provider will then configure an appropriate set of
file monitors (using ``inotify()``) and will re-run the enumeration if
any of those files are modified or replaced. The implementation of
enumeration would use the ``nss_files`` module interface - we would
``dlopen`` the module and ``dlsym`` the appropriate functions like
``__nss_files_getpwent``.

The fast-cache must also be flushed any time the enumeration is run, to
ensure that stale data is cleaned up. We should also consider turning
off the fast memory cache while we are performing the update.

In addition, the nscd cache (if applicable) should also be flushed
during an update. The updates to the files should be sufficiently rare
so the performance impact would be negligible.

The ``files`` provider in its first incarnation is expected to be a
read-only tool, making no direct modifications to local passwords. In
future enhancements, the Infopipe may grow the capability to serve the
AccountsServices API and make changes.

When a change in the files is detected, we should also flush the
negative cache - either only the changes or just flush it whole. This
would prevent scenarios like: ::

        getent passwd foo # see that there is no user foo
        useradd foo       # OK, let's add it then
        getent passwd foo # still no user returned until the negative cache expires

from confusing admins.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

We may need the ability to choose non-default locations for files. This
can be a hidden (undocumented) option in the first version and if there
is a need to actually configure a non-default location, we can later
expose these configuration options.

We may also need to set a configurable number of seconds between
detecting a change and running enumerations. This could be implemented
in waiting a short time (2-3 seconds perhaps?) before detecting the
change and running the enumeration to avoid excessive enumerations and
invalidating the fastacache during subsequent shadow-utils invocations.

Performance impact
~~~~~~~~~~~~~~~~~~

For measuring performance impact, we have developed a simple project
called `nssbench <https://github.com/jhrozek/nssbench>`__ which
measures the time spent in NSS with systemtap. For each case, results
are included for a single lookup which simulate the simplest case of an
application that is spawned and exists and a case where an application
performs several lookup and is able to benefit from the memory cache
which is opened once per application. For single lookups, we ran the
tests 10 times and averaged the Below are test results from different
scenarios:

#. Base-line: Looking up a local user directly from ``nss_files``

   -  Single lookup ::

          nss operation getpwnam(jhrozek) took 226 us
          _nss_files_getpwnam cnt:1 avg:30 min:30 max:30 sum:30 us
          _nss_sss_getpwnam cnt:0 avg:0 min:0 max:0 sum:0 us

   -  100 lookups ::

          nss operation getpwnam(jhrozek) took 2717 us
          _nss_files_getpwnam cnt:100 avg:21 min:14 max:524 sum:2159 us
          _nss_sss_getpwnam cnt:0 avg:0 min:0 max:0 sum:0 us

#. Failover from ``sss`` to ``files`` when SSSD is not running - this is
   the 'worst' case where ``sss`` is enabled in ``nsswitch.conf`` but
   the daemon is not running at all, so the system falls back from
   ``sss`` to ``files`` for user lookups.

   -  Single lookup ::

          nss operation getpwnam(jhrozek) took 549 us
          _nss_files_getpwnam cnt:1 avg:32 min:32 max:32 sum:32 us
          _nss_sss_getpwnam cnt:1 avg:72 min:72 max:72 sum:72 us

   -  100 lookups ::

          nss operation getpwnam(jhrozek) took 6078 us
          _nss_files_getpwnam cnt:100 avg:19 min:16 max:42 sum:1907 us
          _nss_sss_getpwnam cnt:100 avg:22 min:19 max:74 sum:2248 us

#. Round-trip between SSSD daemon's populated cache and OS when the
   memory cache is not used or not populated

   -  Single lookup ::

          nss operation getpwnam(jhrozek) took 755 us
          _nss_files_getpwnam cnt:0 avg:0 min:0 max:0 sum:0 us
          _nss_sss_getpwnam cnt:1 avg:384 min:384 max:384 sum:384 us

   -  100 lookups ::

          nss operation getpwnam(jhrozek) took 97831 us
          _nss_files_getpwnam cnt:0 avg:0 min:0 max:0 sum:0 us
          _nss_sss_getpwnam cnt:100 avg:968 min:115 max:22153 sum:96812 us

#. Performance benefit from using the memory cache

   -  Single lookup ::

          nss operation getpwnam(jhrozek) took 373 us
          _nss_files_getpwnam cnt:0 avg:0 min:0 max:0 sum:0 us
          _nss_sss_getpwnam cnt:1 avg:37 min:37 max:37 sum:37 us

   -  100 lookups ::

          nss operation getpwnam(jhrozek) took 1355 us
          _nss_files_getpwnam cnt:0 avg:0 min:0 max:0 sum:0 us
          _nss_sss_getpwnam cnt:100 avg:4 min:3 max:42 sum:408 us

The testing shows substantial benefit from SSSD cache for applications
that perform several lookup. The first lookup, which opens the memory
cache file takes about as much time as lookup against files. However,
subsequent lookups are almost an order of magnitude faster.

For setups that do not run SSSD by default, there is a performance hit
by failover from ``sss`` to ``files``. During testing, the failover took
up to 300us, about ~70us was spent in the ``sss`` module and about ~200
us seems to be the failover in libc itself.

Compatibility issues
~~~~~~~~~~~~~~~~~~~~

Unless the ordering is specified, the files provider should be loaded
first.

Other distributions should be involved as well - we should work with
Ubuntu as well.

abrt and coredumpd must be run with ``SSS_LOOPS=no`` in order to avoid
looping when analyzing a crash. We need to test this by reverting the
order of modules, attaching a debugger and crashing SSSD on purpose.

Packaging issues
~~~~~~~~~~~~~~~~

We need to add conflicts between glibc an an sssd version that doesn't
provide the files provider.

How To Test
~~~~~~~~~~~

When properly configured, SSSD should be able to serve local users and
groups. Testing this could be as simple as ::

    getent -s sss passwd localuser

Of course, testing on the distribution level could be more involved. For
the first phase, of just adding the files provider, nothing should break
and the only thing the user should notice is improved performance.
Corner cases like running ``sssd_nss`` under gdb or corefile generation
with setup where ``sss`` is set first in nsswitch.conf must be done as
well.

How To Debug
~~~~~~~~~~~~

A simple way of checking is some issue is caused by this new setup is to
revert the order of NSS modules back to read ``files sss``.

Authors
~~~~~~~

-  Stephen Gallagher <`sgallagh@redhat.com <mailto:sgallagh@redhat.com>`__>
-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
