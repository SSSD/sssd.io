Internal D-Bus communication
############################

`D-Bus`_ is a lightweight system for inter-process communication. We use it heavily in SSSD
to send messages between different SSSD processes,
especially between the :doc:`responders and backends <architecture>`. SSSD uses the referral
C implementation of the D-Bus protocol `libdbus`_, however it is wrapped in
our own API that is called ``sbus`` which integrates ``libdbus`` with
:doc:`talloc <talloc>` and :doc:`tevent <tevent>`.

.. _D-Bus: https://dbus.freedesktop.org/doc/dbus-specification.html
.. _libdbus: https://dbus.freedesktop.org/doc/api/html/index.html

D-Bus 101
*********

D-Bus operates over a client-server architecture. The server is commonly known
as a ``message bus``. Clients connect to the message bus and acquire a name.
The name is used as an address for exchanging messages between the clients over
the message bus. The main purpose of the message bus is to route incoming
messages to the target clients.

D-Bus Message bus
=================

There are two public message buses that are automatically started on modern
Linux distributions. These can be used to communicate with unrelated process and
publish information. They are called the  ``system bus`` and the ``session
bus``.

system bus
  There is only one system bus on the system. It is run on a well-known,
  publicly accessible address and everyone can connect to it. It is available to
  all users and every process can communicate with everyone.

session bus
  Session bus exists only for the lifetime of a user session. Only the logged-in
  user who started the session can connect to it and it can be therefore used
  only by processes that are owned by the user and thus has access to the
  socket.

.. seealso::

    The reality is little bit more complicated as there are mechanisms that can
    define D-Bus policy and restrict the communication on the message bus. See
    `dbus-daemon (1) <https://dbus.freedesktop.org/doc/dbus-daemon.1.html>`__
    "CONFIGURATION FILE" section for more information.

D-Bus Messages
==============

D-Bus distinguishes between four different message types:

method call
    Unicast message with a specific destination (it is sent to a single specific
    target) and expects a reply in return. The reply is either a ``method
    return`` or ``error``. A method call can have one or more arguments
    marshalled into the message.

method return
    Used to send a reply to a ``method call``. It can also contain arguments
    that are send to the original sender.

error
    Used as a reply to a ``method call``, similar to ``method return``. However,
    as the name suggest, it is used to send an error code and error message back
    to the sender. It can not have any arguments.

signal
    Signals are broadcast messages. Once a signal is emitted by a client, it is
    then retransmitted to anyone who listens to it. Message bus therefore
    maintains a list of event listeners and clients must explicitly register and
    start listening to the signal.

.. note::

    In fact, signals can be unicast messages as well as they may contain
    a destination. If the destination field is set, it is only sent to the
    destination address and only if the destination client listens to the
    signal.

Each message consist of the following information:

* message type
* sender name
* destination name
* target interface and method
* target object path
* arguments

D-Bus Interfaces
================

The D-Bus protocol is quite object oriented. Each service defines interfaces and
object paths that it provides. The interface defines methods, signals and
properties that available on the given object path. An interface consists of
words separated by dots, object paths are words separated by slash.

There are some standard interfaces that should be always available, such as
``org.freedesktop.DBus``. Others are defined by services through an
xml-formatted introspection, which can be obtained by calling
``org.freedesktop.DBus.Introspectable.Introspect`` method on given object.

.. seealso::

    The standard interface and introspection format are well described in the
    `D-Bus specification`_. You can also look at SSSD internal
    `introspection`_ file.

.. _D-Bus specification: https://dbus.freedesktop.org/doc/dbus-specification.html
.. _introspection: https://github.com/SSSD/sssd/blob/master/src/sss_iface/sss_iface.xml

D-Bus in SSSD
*************

SSSD uses its own API called ``sbus`` which is a wrapper around ``libdbus`` that
integrates it with :doc:`talloc <talloc>` and :doc:`tevent <tevent>` so it can
be used asynchronously with defined memory hierarchy.

The ``sbus`` library provides a code generator that generates both asynchronous
and synchronous C code out of an introspection file. Therefore calling a method
and emitting a signal is as easy as calling a single C function (or a tevent
request) with full compile-time type safety. The user does not have to know all
D-Bus details and does not have to understand ``libdbus`` at all, only
understanding of interfaces and object paths is required. It also makes it
possible to unit test the IPC interface.

Defining a method handler
=========================

A method handler is a function or tevent request that is called once a specific
method call (or signal) is received. The ``sbus`` uses extensive macro magic to
allow declaring handlers in declarative style with compile-time type safety of
parameters and private data. It is quite cumbersome to debug typos, but the
compile-time type safety is a huge benefit.

The declarative macros are defined and explained in `sbus_interface.h`_. They
declare a new D-Bus interfaces and setup methods and properties handlers and
defines what signals can be emitted. This interface is later registered on a
given object path and it is also used to construct and online introspection that
is returned as a reply for the
``org.freedesktop.DBus.Introspectable.Introspect`` method. See the following
code snippet from `dp_init_interface()`_ to get the idea.

.. _dp_init_interface(): https://github.com/SSSD/sssd/blob/11c7f6a65da28e8802d992d4d07682a500dc6350/src/providers/data_provider/dp.c#L32
.. _sbus_interface.h: https://github.com/SSSD/sssd/blob/master/src/sbus/sbus_interface.h

.. code-block:: c

    SBUS_INTERFACE(iface_dp_failover,
        sssd_DataProvider_Failover,
        SBUS_METHODS(
            SBUS_SYNC(METHOD, sssd_DataProvider_Failover, ListServices, dp_failover_list_services, provider->be_ctx),
            SBUS_SYNC(METHOD, sssd_DataProvider_Failover, ListServers, dp_failover_list_servers, provider->be_ctx),
            SBUS_SYNC(METHOD, sssd_DataProvider_Failover, ActiveServer, dp_failover_active_server, provider->be_ctx)
        ),
        SBUS_SIGNALS(SBUS_NO_SIGNALS),
        SBUS_PROPERTIES(SBUS_NO_PROPERTIES)
    );

    SBUS_INTERFACE(iface_dp_access,
        sssd_DataProvider_AccessControl,
        SBUS_METHODS(
            SBUS_ASYNC(METHOD, sssd_DataProvider_AccessControl, RefreshRules, dp_access_control_refresh_rules_send, dp_access_control_refresh_rules_recv, provider)
        ),
        SBUS_SIGNALS(SBUS_NO_SIGNALS),
        SBUS_PROPERTIES(SBUS_NO_PROPERTIES)
    );

Changing the interface
======================

If you need to change the interface (e.g. add a new method), you need to modify
the `introspection`_ file and rebuild SSSD. Rebuilding the project will generate
the new code for your changes. The generated code should be committed to the git
repository as well to keep tools such as static analyzers functional.

Calling D-Bus method
====================

In order to call a D-Bus method, you need to include either:

* ``sss_iface/sss_iface_async.h`` for asynchronous calls via tevent in main SSSD processes
* ``sss_iface/sss_iface_sync.h`` for direct synchronous calls in SSSD tools

These headers will make generated code accessible for your use. For example:

.. code-tabs::
    :short:

    .. code-tab:: c
        :label: Asynchronous code

        struct tevent_req *
        sbus_call_dp_autofs_Enumerate_send
            (TALLOC_CTX *mem_ctx,
            struct sbus_connection *conn,
            const char *busname,
            const char *object_path,
            uint32_t arg_dp_flags,
            const char * arg_mapname,
            uint32_t arg_cli_id);

        errno_t
        sbus_call_dp_autofs_Enumerate_recv
            (struct tevent_req *req);

        struct tevent_req *
        sbus_call_dp_backend_IsOnline_send
            (TALLOC_CTX *mem_ctx,
            struct sbus_connection *conn,
            const char *busname,
            const char *object_path,
            const char * arg_domain_name);

        errno_t
        sbus_call_dp_backend_IsOnline_recv
            (struct tevent_req *req,
            bool* _status);

    .. code-tab:: c
        :label: Synchronous code

        errno_t
        sbus_call_systemd_RestartUnit
            (TALLOC_CTX *mem_ctx,
            struct sbus_sync_connection *conn,
            const char *busname,
            const char *object_path,
            const char * arg_name,
            const char * arg_mode,
            const char ** _arg_job);

        errno_t
        sbus_call_systemd_StartUnit
            (TALLOC_CTX *mem_ctx,
            struct sbus_sync_connection *conn,
            const char *busname,
            const char *object_path,
            const char * arg_name,
            const char * arg_mode,
            const char ** _arg_job);

        errno_t
        sbus_call_systemd_StopUnit
            (TALLOC_CTX *mem_ctx,
            struct sbus_sync_connection *conn,
            const char *busname,
            const char *object_path,
            const char * arg_name,
            const char * arg_mode,
            const char ** _arg_job);

Custom data types
=================

Another benefit over pure ``libdbus`` is the support for custom data types.
D-Bus supports all standard scalar types (numbers, strings) and non-scalar types
(dictionary entry, arrays). However, it is often necessary to exchange a complex
structure. The ``sbus`` library makes it possible to define a custom data type
so the caller does not have to deal with marshalling it into the D-Bus protocol.

In order to add a new data type, you need to change three files:

1. `The code generator <https://github.com/SSSD/sssd/blob/11c7f6a65da28e8802d992d4d07682a500dc6350/src/sbus/codegen/sbus_CodeGen.py#L221>`__

   * You need to register the new data type in the code generator by associating
     a specific D-Bus signature with C data type and new name.

2. `The header file <https://github.com/SSSD/sssd/blob/master/src/sss_iface/sss_iface_types.h>`__

   * Add reader and writer declaration to the header file.

3. `The source file <https://github.com/SSSD/sssd/blob/master/src/sss_iface/sss_iface_types.c>`__

   * Implement the reader and writer for the new data type. It is possible to
     reuse already existing readers and writers.