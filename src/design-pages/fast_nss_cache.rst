.. highlight:: none

FastNSSCache
============

Problem Statement
-----------------

Currently in SSSD user and group lookups are performed by using a
connection to a named socket. This means each client has to talk to the
sssd\_nss daemon for every lookup it needs to perform.

Although this behaviour works well for normal machines, it has
scalability limits on busy machines with many processes that need to
query the user/group database frequently.

There are 2 factors that cause scalability issues:

#. context switches
#. the responder process is single-threaded (although asynchronous) so
   the amount of processing it can do is limited by the speed of 1 cpu

Each request suffers from at least 2 context switches (and a few copies
of the data in memory) to write() the request in, wait until it is
processed by sssd\_nss, read() the reply back. Because sssd\_nss may be
busy answering many requests a queue may build up and replies be
delayed.

Allowing the clients to directly access SSSD caches is not possible for
various reasons including:

-  sssd uses LDB as caching backend and LDB depends on byte range locks.
   Giving a client read access to the cache would allow DoS, f.e. the
   client locks a record and never unlocks it.
-  sssd stores data not all clients are allowed to get access to
   (password hashes for example) and partitioning access to this data
   within the LDB cache is not feasible.

A method to avoid context switches and the sssd\_nss bottleneck without
compromising th security of the system is therefore desirable.

Overview of FastNSSCache solution
---------------------------------

The FastNSSCache feature addresses both issues.

This is done by creating a specialized cache that have a few properties

-  Contains only public data (the same data available in a public passwd
   or group files)
-  Read only for clients
-  Does not use locking and yet prevents access to inconsistent data
-  Cache has a fixed size and uses a FIFO (for now) method to know which
   entries to purge
-  Fallback to named sockets if entry is not found in the Fast Cache

Implementation details
----------------------

The cache files are opened on the client at the first query and mmaped
in the process memory, all accesses to data are therefore direct access
to memory and do not suffer from any context switch. They also happen in
parallel within each process with synchronization (in order to allow
updates) performed by using memory barriers.

Cache files can only be used for direct lookups (by name or by UID/GID),
enumerations are \_never\_ handled via fast cache lookups by design,
they always fallback to socket communication.

The "maps" currently available are the \_passwd\_ and \_group\_ maps,
each map has a file associated in the /var/lib/sss/mc directory which is
accessible read-only by clients.

Configuration
-------------

At the moment we plan to provide 3 parameters per map that can control
the caches.

-  Per map enablement parameter that allows to activate/deactivate maps
   individually.
-  Per map cache size to fine tune the cache sizes in case space is at a
   premium or the dataset does not fit the default cache.
-  Expiration time for entries.

Cache entries warrant a shorter expiration time than current LDB caches
because access to these entries is undetectable by sssd\_nss which
cannot decide how much an entry is required and whether a midway refresh
is needed. By shortening the FastNSSCache entries life time we incur in
the penalty of using the pipe from time to time but in turn we allow
ssd\_nss to decide whether it is required to refresh the entry or not.

Future Improvements
-------------------

-  Better garbage collection on the server side, at the moment a FIFO is
   used.
-  Handle caching other nsswitch.conf database plugins in order to avoid
   slow access to the files db
