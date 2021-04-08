**Nothing on this page truly exists. It contains only ramblings on what
SSSD might become in the future.** These are mostly unordered notes.

SSSD 2.0
========

Major themes

-  Powered by systemd wherever possible
-  Eliminate the monitor process
-  Support socket activation and idle termination
-  Simplify configuration
-  Fast support for local users

systemd
~~~~~~~

This init system supports many powerful features that could make large
parts of SSSD *infrastructure* irrelevant.

-  Supports process monitoring and automatic restart
-  Can support chaining multiple child processes together
-  Manages socket-activation for registered processes
-  Supports kdbus for secure and fast D-BUS communication between
   processes

Process start-up
~~~~~~~~~~~~~~~~

-  Use the ``sssd`` process (formerly the monitor) solely to parse
   sssd.conf and convert it to the config LDB, which the other processes
   will be able to read at startup.
-  Eliminate the services= line. All supported responders should simply
   be invoked (socket-activated) when their client asks for them and
   then proceed according to the config LDB (which may just tell it to
   terminate again with an appropriate error reply)
-  We may want to load different providers as separate processes to make
   it easier to decide when to terminate them. It would be better to
   rethink whether it makes more sense to have one process per domain as
   opposed to one process per configured provider back-end.
-  systemd now has a D-BUS method for setting up persistent or
   non-persistent units (such as service units), so we can take
   advantage of this to start up only the processes we really need.

idle termination
~~~~~~~~~~~~~~~~

Shutting down any SSSD process that is not actively doing work would be
advantageous for several reasons (most notably memory and CPU resource
reduction during idle periods). Designing for this would also force us
to optimize for making SSSD operations stateless (or at least tracking
in-progress operations more carefully).

Some random thoughts on provider implementations:

-  LDAP provider (and derivatives) should auto-terminate once the the
   ldap\_connection\_expire\_timeout is reached, since we can then
   assume that nothing has been happening on the connection for quite
   some time (15 minutes by default).
-  Other providers should terminate after a similar reasonable amount of
   time.
-  Providers that have computationally-rare periodic tasks (such as
   cache cleanup or kerberos ticket renewal) should be stored in a
   persistent manner between process startups and should automatically
   be invoked if their period has passed. We can take advantage of
   systemd timer units to have the process periodically woken up to
   process these events, rather than simply holding the process alive
   and idle for long periods.

Local users
~~~~~~~~~~~

-  We need to rework the local provider to behave more similarly to the
   other providers (even if this just means a provider backend that
   always returns "offline"). This way, the local id\_provider can be
   configured with other providers like kerberos.
-  We need to optimize the local user behavior such that it is
   acceptable to have ``sss`` first in the nsswitch.conf lines
   everywhere. This will solve the performance problem caused by
   disabling nscd for local users (which results in disk reads for all
   lookups prior to trying sssd)
-  We need to work on
   `​https://sourceware.org/glibc/wiki/Proposals/GroupMerging <https://sourceware.org/glibc/wiki/Proposals/GroupMerging>`__
   and finish it.

Enumeration
~~~~~~~~~~~

Enumeration mode should be deprecated in SSSD 2.0 with a strong
recommendation being placed on a D-BUS API for doing enumeration that
supports paging and filtering. Most uses of enumeration are for
presenting a user/group list in a UI, so this will be a better fit for
that anyway.

SBUS
~~~~

The original point-to-point SBUS should be retired. Now that SSSD
supports running as non-root, we should instead set up a session bus and
use that (which will also be advantageous as we get into the
kdbus-enabled world).
