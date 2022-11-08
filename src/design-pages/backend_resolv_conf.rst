Move resolv.conf Watching to the Backends
#########################################

Related Tickets
***************

* https://github.com/SSSD/sssd/issues/6383

Problem statement
*****************
SSSD service starts before the *Network Manager* and misses some changes to
``/etc/resolv.conf``.

The underlying reason for the issue is a race-condition with respect to the
SSSD startup and changes to ``/etc/resolv.conf``. SSSD monitors
``/etc/resolv.conf`` for changes to make sure changes are respected.

This is done here as well, unfortunately the change happens at a time where the
*SSSD monitor* process cannot send a signal to the *SSSD backend* process to
refresh ``/etc/resolv.conf`` because the *backend* is not fully started.

Use Cases
*********
When the host is rebooted and services are starting up, SSSD may miss the
changes initially done to ``/etc/resolv.conf`` by the *Network Manager*.

Solution overview
*****************
Currently the *monitor* is watching for changes to ``/etc/resolv.conf``. When
changes are detected, it uses the D-Bus method ``resInit()`` of the
``sssd.service`` interface to tell each active *backend* and *responder* to
reload this file.

The proposed solution is to stop watching the ``/etc/resolv.conf`` file from
the *monitor* and make each *backend* watch the file. *Responders* do not
really need to monitor this file.

This is also an advantage if it is ever decided to remove the *monitor* and
to rely on a system service manager (such as *systemd*) instead.

Implementation details
**********************
To watch the ``/etc/resolv.conf`` file, the *monitor* can currently do one of
three different things:

1. Use **inotify** to get notified of changes,
2. Polling the file for changes every 5 seconds, or
3. Not watch it at all.

The first case is the default. The *monitor* uses **inotify** to get notified
of changes and, when they happen, it tells each active *backend* to reload the
file thorough ``D-Bus``, by invoking the *backend*’s method ``resInit()``
provided by the ``sssd.service`` interface of the ``/sssd`` object.

If the monitor fails to configure **inotify**, or if the user decided to not
use **inotify** by setting ``try_inotify`` to ``false`` in the *SSSD* section
of the configuration file, it will fall back to polling the file every 5
seconds. For that it uses the timers provided by ``tevent``. This option’s
description in the man pages shall be made conditional to the support for
**inotify**.

The third case happens when the user configures ``monitor_resolv_conf`` to
``false`` in the *SSSD* section, or when all the other methods have failed.

First Phase
-----------
In the first phase we propose to relocate this code, which is tightly coupled
to the *monitor*, to a separate module providing a parametric interface
allowing any component to use it to monitor any file. Initially it will only
be used by the *monitor* in the same way as used today, which will allow us
to verify it is done correctly and we introduced no change in the behavior.

The code will be moved to the ``util/file_watch.c`` and ``util/file_watch.h``
files, and the entry point will be a single function called
``fw_watch_file()``::

    struct file_watch_ctx *fw_watch_file(TALLOC_CTX *mem_ctx,
                                         struct tevent_context *ev,
                                         const char *filename,
                                         bool use_inotify,
                                         void (*fn)(const char *filename, void *arg),
                                         void *fn_arg);


The returned ``file_watch_ctx`` structure will be allocated linked to the
provided ``mem_ctx``. The caller must also provide a ``tevent_context`` to
handle various events, the name of the file to monitor (which was previously
hard-coded), whether to use inotify (this was previously read directly from
the configuration, but to allow each caller to use a different configuration
attribute or section, we let them read it - for the moment the configuration
itself will not be modified), and finally the function, and an argument to pass
it, to be invoked when changes in the file are detected. On error the function
returns ``NULL``.

Internally this will work as before, but most of the previously hard-coded
information (such as the filename, the function to read the file and store it
in some internal structure, the values read from the configuration, etc.) will
be passed as parameters and stored in the ``file_watch_ctx`` context.

No provision is done at this moment to provide a way to stop watching a
watched file as it didn’t exist before. File watching is automatically stopped
when the memory context is freed, which means the caller must not free this
structure while monitoring is needed.

Unit tests will be written for this new module.

Second Phase
------------
The second and final phase will move the call to ``fw_watch_file()``  from
the *monitor* to the *backends* but not to the *responders* as they don’t
actually need to monitor or load this file.

The ``D-Bus`` method ``resInit()`` will be removed from *backends* and
*responders* as it will no longer be used.

Authors
*******
- Alejandro López <allopez@redhat.com>
- Alexey Tikhonov <atikhono@redhat.com>
