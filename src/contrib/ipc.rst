Inter-process Communication
###########################

This document describes the inter-process communication mechanism that is used
between various SSSD components.

Architecture overview
*********************

The SSSD consists of several processes, each of them has its own
function. The SSSD processes can be one of the following:

Monitor
    The purpose of the monitor process is to spawn the other processes and to
    make sure they are restarted if they exit unexpectedly. There is only one
    instance of the monitor process at a given time.

Backend
    The backend process communicates with the remote server (e.g. queries the
    remote server for a user) and updates the cache (e.g. writes the user
    entry). There is one backend process per domain.

Responder
    The system libraries (such as the Name Service Switch module or the PAM
    module) communicate with the corresponding responder process. When the
    responder process receives a query, it checks the cache first and attempts
    to return the requested data from cache. If the data is not cached (or is
    expired), the responder sends a message to the backend requesting the cache
    to be updated. When the backend is done updating the cache, the responder
    process checks the cache again and returns the updated data. It is important
    to note that the responder process never returns the data directly from the
    server, the data is always written to the cache by the backend process and
    returned to the calling library in the responder process.

Helpers
    SSSD runs in asynchronous mode so it is able to serve multiple requests in
    parallel. However, this is not achieved by threads but by event driven
    programming. Therefore operations that cannot be executed in a non-blocking
    way are run in a special helper process. The helper process is spawned so it
    can perform an otherwise blocking operation (e.g. ``kinit``). Example of
    such process are ``krb5_child`` and ``ldap_child``.

Clients and client libraries
    A client is an external process that talks to SSSD responders through their
    relevant client libraries. For example the application that wants to
    authenticate the user via PAM is a client that talks through ``pam_sss.so``
    client library with the SSSD's PAM responder.

IPC Methods
***********

SSSD uses three kinds of inter-process communication methods.

D-Bus
    The D-Bus protocol is used for communication between core SSSD components --
    monitor, backends and responders.

Client wire protocol
    SSSD implements a custom wire protocol over well known sockets for
    communication between client libraries and responders.

UNIX signals
    SSSD processes also listen to various UNIX signals.

D-Bus and sbus
==============

SSSD uses the `D-Bus protocol`_ for inter-process communication between its
components. However, it does not use the public system bus, but rather runs a
private D-Bus server.

D-Bus is not used directly but SSSD implements a wrapper around ``libdbus``
called ``sbus`` which integrates D-Bus with ``tevent`` and ``talloc`` -- the
event and memory managements libraries that are heavily used inside SSSD. The
terms ``D-Bus`` and ``sbus`` are used interchangeably in the developers
terminology.

.. _D-Bus protocol: https://www.freedesktop.org/wiki/Software/dbus


Basic D-Bus concepts
--------------------

The D-Bus protocol consists of several primary components:

D-Bus server
    The server accepts connections and routes communication (messages) between
    two or more endpoints. Each connection to the server is associated with one
    or more well-known or anonymous names and can send and also receive
    messages from another connection.

D-Bus message
    The message is a key communication component that is transmitted between two
    or more connections. There are three types of messages -- method call,
    signal and error.

    * The method call is a unicast message that can be replied to.
    * The error message is a possible reply to the method call.
    * The signal is a broadcast message that is sent to every one that listens
      to it.

System bus
    The system bus is a well-known instance of a D-Bus server. There is one
    system bus that can be accessed by all users.

Session bus
    The session bus is another well-known instance of a D-Bus server. There is
    one session bus per user session and it can be accessed only by the user.

Client wire protocol
====================

SSSD creates several local ``AF_UNIX`` sockets. These sockets are used for
communication between clients (e.g. ``nss_sss``) and SSSD responders (e.g. the
NSS responder).

All clients employ a request/response protocol using their own TLV-encoding.
Note that the clients only support synchronous I/O so sending a request to
the SSSD responder is a blocking operation -- it will await the response on
the client side. The responder itself supports asynchronous I/O using `tevent`
event library so it can serve multiple client's requests in parallel.

UNIX Signals
============

All SSSD components listen to several standard signals. It is usually enough
to send the signal to the main monitor process, which will then propagate it
to other components.

SIGTERM
    Terminates a process gracefully.

SIGKILL
    In cases where an unresponsive worker process does not terminate
    after receiving SIGTERM, the monitor forcibly kills it with SIGKILL.

SIGUSR1
    Switch SSSD to offline state. This signal is mostly useful for testing. It
    can be send to a single backend or to the monitor process. If it is recieved
    by the monitor process then all backends are moved to the offline state.

SIGUSR2
    This is similar to ``SIGUSR1``. It will reset the offline state, making
    SSSD to reconnect to the remote server on next request.

SIGHUP
    This signal can be send to the monitor only. It will cause log files
    rotation and clearing in-memory caches. Please note that this signal is
    commonly used to re-read service configuration, but SSSD does not support
    this. To reload the configuration you must restart the service.
