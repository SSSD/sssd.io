SUDO-RS Integration
###################

Problem Statement
*****************
Starting at version 0.2.14, ``sudo-rs`` is able to read the sudoers rules from
a socket in text format. We need to be able to provide this client with the sudoers
rules, using a mechanism separated from the one used for ``sudo`` which uses
a binary protocol.

Solution Overview
*****************
``sudo-rs`` opens a dedicated socket (the path can be configured) and expects to
receive all the sudoers rules formatted as in the sudoers file. No filtering is
considered at this moment.

Four option were analyzed for this:

1. Use a plugin in ``sudo-rs`` to communicate with SSSD.
2. Use a separate, intermediate daemon to convert from our protocol to text.
   This daemon could be socket-activated with systemd.
3. Configure ``sssd_sudo`` to use the current protocol or simply text (as ``sudo-rs``
   expects) with a selector in ``sssd.conf``. The downside is that ``sudo`` and
   ``sudo-rs`` cannot be used together.
4. Make ``sssd_sudo`` open a second, separated socket to be used by ``sudo-rs``.

Option 1 was refused by the ``sudo-rs`` developers because they want to keep ``sudo-rs``
simple and minimize the attack surface. Option 2 is not that different from option 4,
but requires an extra daemon and the filtering is yet unresolved. The third option
was discarded because of the mentioned downside.

We decided to go with the **fourth option**.

Implementation Details
**********************
The ``sudo`` responder will keep serving the *sudo* plugin on its usual socket,
``/var/lib/sss/pipes/sudo``, with the usual binary protocol, and will
additionally listen on a second socket, ``/var/lib/sss/pipes/sudoers``, in the
same directory, where it will write out the cached rules as *sudoers* text.

The socket name will be defined at build time, next to the other responder
sockets, as ``SSS_SUDOERS_SOCKET_NAME`` in ``Makefile.am``.

Several Sockets per Responder
=============================
Currently a responder has exactly one socket, created (or inherited from
*systemd*, when socket activated) by ``sss_process_init()`` and kept in
``rctx->lfd`` / ``rctx->lfde``. A new function in
``src/responder/common/responder_common.c`` will let a responder listen on more
than one socket:

.. code-block:: c

    errno_t sss_responder_add_socket(struct resp_ctx *rctx,
                                     const char *sock_name,
                                     mode_t umaskval,
                                     connection_setup_t conn_setup);

An additional socket will be handled exactly like the main one with respect to
peer credentials, ``allowed_uids`` and the idle timers; what will differ is the
``connection_setup_t`` callback, which installs the protocol handling of the
connection. This is what will let a single responder speak a different
protocol on each of its sockets.

To make this possible, the listening file descriptor and its ``tevent_fd`` will
be tracked in ``struct accept_fd_ctx``, which already exists per listening
socket, rather than being read from ``rctx``. The accept handler and the
file-descriptor-exhaustion backoff will use the per-context values, so that
running out of file descriptors pauses ``accept()`` only on the socket where it
happened.

An additional socket will differ from the main one in that it will be owned by
its ``accept_fd_ctx``: a destructor will close the listening file descriptor
and, when SSSD created the socket itself, unlink it, so that an orderly
shutdown does not leave behind a socket that clients could still connect to.

Finally, ``cctx->ev`` and ``cctx->rctx`` will be set in ``accept_fd_handler()``
*before* the connection setup callback runs. The *sudoers* protocol has to
reach the responder context from the setup callback, because it starts sending
without waiting for a request from the client.

Socket Activation
=================
The *sudoers* socket will be activatable in its own right, by a new
``sssd-sudoers.socket`` unit that points at ``sssd-sudo.service`` with
``Service=``; the service will list it in ``Sockets=``, since only the socket
unit sharing its name is inherited implicitly. Connecting to either socket will
start the sudo responder, and *systemd* will hand it both listening file
descriptors at once.

This is what the single socket assumption in ``activate_unix_sockets()``
currently rules out: it rejects a second descriptor with ``E2BIG`` and
hardcodes ``rctx->lfd = SD_LISTEN_FDS_START``. Instead, all the passed
descriptors will be collected by a new ``responder_setup_activated_fds()`` into
``rctx->activated_fds``, each with the name *systemd* gave it and the path it
is bound to, and each listener will claim its own with
``responder_claim_activated_fd()``.

A socket will be matched by the ``FileDescriptorName=`` of its unit, which by
convention is the basename of the socket path, ``sudo`` and ``sudoers`` here.
Matching will fall back to the bound path, so a unit that does not set the name
still works, and finally to "a single unnamed descriptor is the main socket",
which is how every other responder is activated, leaving their units
unchanged.

``sd_listen_fds_with_names()`` is available since *systemd* 227, so ``systemd.m4``
will be changed to ask for that version. 227 is also well past 209, where the
``libsystemd-{login,journal,daemon,id128}`` libraries were merged into a single
``libsystemd``, so the fallbacks to the split libraries can be dropped with it.

Which side created the socket will decide who must remove it. A socket SSSD
created will be unlinked when the responder stops; one created by *systemd*
belongs to its socket unit and will deliberately be left in place.

The Sudoers Protocol
====================
A new file, ``src/responder/sudo/sudosrv_sudoers.c``, will implement the
protocol, which is write-only and has no requests:

1. The client connects. ``sudosrv_sudoers_connection_setup()`` allocates a
   ``struct sudosrv_sudoers_ctx``, sets it as the connection's
   ``protocol_ctx``, installs the file descriptor handler and schedules an
   immediate ``tevent`` timer. The timer is needed because the client's
   ``tevent_fd`` is only registered after the setup callback returns.
2. From that timer, the responder marks the connection as not readable,
   renders the whole reply into a buffer and marks the connection as writable.
   Nothing is ever read from the client; a client that goes away is noticed by
   ``send()`` failing.
3. The write handler sends the buffer, resuming on the next write event on a
   short write or ``EAGAIN``.
4. Once everything has been sent, the client context is freed, which closes
   the connection. The client therefore reads until the end of file.

.. note::

    The reply could be rendered and sent in smaller chunks to reduce the memory
    consumption. Instead, it will be generated all at once, so that the client
    gets a consistent snapshot of the cache and not a mix of rules from before
    and after a refresh that might happen while sending.

Reading the Rules from the Cache
================================
The *sudoers* socket will return every rule currently in the cache of every
enabled domain. Only the cache will be consulted, no lookup against the server
will be triggered, so which rules are returned will depend on the usual refresh
mechanisms of the responder. The code that queries the cache will be shared
with the *sudo* socket.

The function ``sysdb_sudo_filter_all_rules()`` will be added to
``src/db/sysdb_sudo.c``. It will be a filter that matches every cached rule
except the ``cn=defaults`` entry, which is already returned by
``sysdb_sudo_filter_defaults()``.

Per domain, the responder will read the defaults and then all the rules, sort
the rules by ``sudoOrder`` with ``sudosrv_sort_rules()`` honouring
``ldap_sudo_inverse_order``, and run ``sudosrv_format_rules()`` on them, which
rewrites the *run as* user and group names into their output form (fully
qualified or not, ``override_space`` applied). Ordering and name formatting
will therefore be the same ones the *sudo* socket applies. Only top level
domains will be walked, since the rules of a subdomain are stored in the tree
of its parent domain.

Rendering the Rules as Sudoers Text
===================================
Each rule will become one *sudoers* user specification:

.. code-block:: text

    <sudoUser> <sudoHost> = (<sudoRunAsUser> : <sudoRunAsGroup>) <tags>: <sudoCommand>

Multi-valued attributes will be joined with ``", "``. A rule without
``sudoUser`` or ``sudoCommand`` cannot be written out and will be skipped with
a debug message. A rule without ``sudoHost`` will get ``ALL``: according to
``sudoers.ldap(5)`` such a rule matches no host, but SSSD only ever caches
rules that apply to this host. ``sudoRunAs``, the deprecated spelling, will be
used when ``sudoRunAsUser`` is absent. The ``cn=defaults`` entry of a domain
will be rendered as a list of ``Defaults <option>`` lines, before the rules.

``sudoOption`` values that have a per-rule tag equivalent, such as
``!authenticate`` or ``noexec``, will be translated into that tag
(``NOPASSWD:``, ``NOEXEC:``, …) and placed before the command list, by means of
a lookup table.

Nothing that is in the cache will be silently dropped: whatever a *sudoers*
file cannot express on a user specification line will be written out as
comments preceding the rule, namely the rule name, ``sudoOrder``,
``sudoNotBefore``, ``sudoNotAfter`` and the ``sudoOption`` values that have no
tag equivalent. Each domain will also be introduced by a ``# domain: <name>``
comment, and the whole output by a header stating that it was generated by
SSSD.

Security Considerations
=======================
Since the protocol carries no request, it carries no user name either, and the
rules cannot be filtered by the user that connects: every client will receive
every cached rule, which is what ``sudo-rs`` expects, a plain *sudoers* file.

The socket will be public, created with ``SCKT_RSP_UMASK`` like the other
responder sockets, so its mode will be 0666 and any local user will be able to
read the sudo rules of every user. The socket has to be writable to allow the
connection, but the server will close the reception side.

The *sudoers* socket must respect the existing ``client_idle_timeout``.

Documentation
=============
``sssd-sudo(5)`` will get a new section describing the socket, its protocol,
the fact that the output is not filtered per user and the socket is world
accessible, how unrepresentable properties are reported as comments, and the
two ways the socket comes into existence: activated by ``sssd-sudoers.socket``,
where the responder may come and go with ``responder_idle_timeout``, or created
by the responder when "sudo" is listed in ``services``.

Future Work
***********
A huge number of sudoers rules can exist in enterprise environments. This could
introduce some delays both in producing the rules (``sssd-sudo``) as in their
processing by the client (``sudo-rs``). If this happens, we can discuss with the
``sudo-rs`` developers about filtering the rules by user. Because they clearly
stated they want to keep this protocol as simple as possible, we will try to
proceed with this improvement only if we observe these delays.

Authors
*******
* Alejandro López <allopez@redhat.com>
* Claude Code (Opus 5.5 Medium)
