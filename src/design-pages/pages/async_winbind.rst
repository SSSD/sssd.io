.. highlight:: none

.. FIXME: Add a link to WinBind internal documentation on all "WinBind"
..        references in this document!

Async WinBind
=============

The WinBind provider uses *libwbclient* library for communication with
WinBind to satisfy NSS and PAM requests. However this library doesn't
provide an asynchronous interface. We had a choice between creating this
interface or use synchronous calls in auxiliary processes running in
parallel to the main provider process.

General Approach
----------------

There should always be at least one auxiliary process running. This
process will receive requests from the main provider process, handle
them as they come in and send back responses. The communication protocol
used should be DBus as it is used in other providers and therefor
doesn't require any extra dependencies or writing additional code. DBus
should also take care of request buffering.

Splitting the load
------------------

If the host needs to process a huge amount of NSS and PAM requests in
short periods of time, it should be possible to setup more than one
auxiliary process to handle them. One should always be available before
hand, because starting it just before it's required adds extra overhead
and delay. A maximum (and maybe a minimum too) number of auxiliary
process should be configurable along with a threshold expressing when a
new process should be created or a spare process killed. The main
provider process need to keep track of this and send it's requests to
the least busy auxiliary process.

Implementation steps
--------------------

#. Have one auxiliary process started when the provider starts. It will
   handle all requests.

2. Add the possibility to have a pre-configured number of processes
   (maximum=minimum) and split requests between them.

3. Add the ability to spawn/kill processes based on load.\*

-  This needs more thinking: e.g. how long do we keep a spare process
   alive? how is the threshold going to work?


Update
------

.. FIXME: Do we have access to these diagrams?
..        For now I'm commenting out this part.

.. Here are some diagrams that show how the solution is going to be
.. implemented. Inspiration has been taken from Apache process pool as
.. Jakub suggested in ticket discussion.
..
.. Sorry for the poor quality of diagrams, but Dia just sucks. :-/

The main process of the WinBind  provider will send requests to spare
processes in the pool. These processes will be allocated automatically
based on the number of spare processes available at any given time.

Requests from NSS and PAM will be forwarded to spare processes in the
pool if there are any available. If not, a new process will be created
unless the maximum number of processes has been reached. After the
request has been forwarded, the number of available spare processes is
checked and a new process is created if there are not enough. Note that
the pool is first populated with a minimum number of processes (spare or
not) when the WinBind provider starts.

In other words, there will be 3 settings:

**Minimum** number of worker processes **running**.

**Maximum** number of worker processes **running**.

**Minimum** number of **spare** worker processes **running**.
