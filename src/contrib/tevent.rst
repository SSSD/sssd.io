Asynchronous programming: tevent
################################

SSSD can handle many user requests in parallel. However, the project does not
use threads to serve the incoming requests but it uses a `talloc`_-based `event
loop`_ implementation called `tevent`_. Using tevent allows us to neatly avoid
blocking during communication with remote servers and other processes but at the
same time we do not have to deal with complicated thread management and locks
since all the code run in a single thread.

.. seealso::

    The tevent library provides many useful features and mastering it will help
    you to simplify the code and its logic a lot. However, this document
    provides only a basic description of tevent and its use cases and patterns
    inside the SSSD project. It is recommended for you to :tag:`strong` read the
    official `Tevent Tutorial`_ and `API Reference`_ to learn more about its
    features. :end-tag:`strong`

.. _event loop: https://en.wikipedia.org/wiki/Event_loop
.. _talloc: talloc.rst
.. _tevent: https://tevent.samba.org/
.. _Tevent Tutorial: https://tevent.samba.org/tevent_tutorial.html
.. _API Reference: https://tevent.samba.org/group__tevent.html

Event loop
**********

Event loop is an infinite cycle that awaits an event and executes the registered
event handler when the event is received. The program goes back to the event
loop when the handler is done. The event loop uses various mechanisms to receive
different event types, you may be already familiar with `select`_ or `epoll`_
that deals with asynchronous input and output operations (read and write to a
socket).

.. _select: https://man7.org/linux/man-pages/man2/select.2.html
.. _epoll: https://man7.org/linux/man-pages/man7/epoll.7.html

.. mermaid::

    graph LR
        loop((Event<br>loop))
        handler(Event handler)
        io(Start asynchronous I/O)

        linkStyle default interpolate basis
        classDef handler fill:green,stroke:green,stroke-width:1px,fill-opacity:0.2
        style loop fill:red,stroke:red,stroke-width:1px,fill-opacity:0.2,font-weight:bold
        class handler,io handler

        loop -. await event .-> loop
        loop -- event received ---> handler
        handler -- register new event handler ---> io
        io --> loop

Event types
===========

The tevent library has support for various event types.

Signals
    `Signals`_ are a basic IPC mechanism. Tevent provides its own implementation
    of signal handlers. SSSD listens to various standard signals to manage its
    components. See `tevent_add_signal`_ for more details.

File descriptor events
    These events implement a non-blocking input and output operations. They are
    triggered when a file descriptor is readable or writable. SSSD uses this for
    communication with remote server as well as for inter-process communication
    between SSSD's components. See `tevent_add_fd`_ for more details.

Timer events
    This can setup a delay task that is fired after a given amount of time.
    Timers are heavily used inside SSSD to perform different kinds of periodic
    tasks such as background cache refresh. See `tevent_add_timer`_ for more
    details.

Immediate events
    When an immediate event is created, it is executed immediately when the
    control gets back to the event loop. This kind of events can be used to
    postpone an operation and sometimes to simplify the code logic. SSSD
    sometimes utilize immediate events to free shared resources. See
    `tevent_create_immediate`_ and `tevent_schedule_immediate`_ for more
    details.

Requests
    Tevent requests are a special event type that helps you keep asynchronous
    code readable with a neat request flow supported by a well defined coding
    pattern. These are the backbone of SSSD and they are explained in more
    details in `Tevent requests`_.

.. _Signals: https://man7.org/linux/man-pages/man7/signal.7.html
.. _tevent_add_signal: https://tevent.samba.org/group__tevent.html#ga3e144d31421b0443ca6925d3d9516323
.. _tevent_add_fd: https://tevent.samba.org/group__tevent.html#gadc52787f3daf49e589066d37a5cdb18c
.. _tevent_add_timer: https://tevent.samba.org/group__tevent.html#gaf3a67ff624c7a12ff2bd413820580676
.. _tevent_create_immediate: https://tevent.samba.org/group__tevent.html#gade7648af3185bf1171a65aae5c72d776
.. _tevent_schedule_immediate: https://tevent.samba.org/group__tevent.html#gaa7d3a489b21813b60abe322b3e8b407e

The following samples illustrate the basic usage of file descriptor events as
well as timers, signals and immediate events. Please refer to the `Tevent
Tutorial`_ and `API Reference`_ for more information on registering event
handlers.

.. code-tabs::
    :short:

    .. plain-tab::
        :label: Signal example

        .. code-block:: c

            /**
            * React on SIGUSR1 signal.
            */

            #include <signal.h>
            #include <stdio.h>
            #include <tevent.h>

            static void handler(struct tevent_context *ev,
                                struct tevent_signal *se,
                                int signum,
                                int count,
                                void *siginfo,
                                void *private_data)
            {
                puts("Signal received.");
            }

            int main()
            {
                struct tevent_context *ev;
                struct tevent_signal *sig;
                int i;

                /* Initialize tevent context. */
                ev = tevent_context_init(NULL);
                if (ev == NULL) {
                    return 1;
                }

                sig = tevent_add_signal(ev, NULL, SIGUSR1, 0, handler, NULL);
                if (sig == NULL) {
                    return 2;
                }

                tevent_loop_wait(ev);

                return 0;
            }

        .. code-block:: console

            $  $ gcc ./main.c -ltalloc -ltevent             |
            $ ./a.out                                       |
                                                            |   $ kill -s SIGUSR1 $(pidof a.out)
            Signal received.                                |
                                                            |   $ kill -s SIGUSR1 $(pidof a.out)
            Signal received.                                |

    .. plain-tab::
        :label: File descriptor example

        .. code-block:: c

            /**
            * Read from a remote connection whenever some data is ready.
            */

            #include <arpa/inet.h>
            #include <errno.h>
            #include <netinet/in.h>
            #include <stdio.h>
            #include <string.h>
            #include <sys/socket.h>
            #include <tevent.h>
            #include <unistd.h>

            int open_socket(int *_fd)
            {
                struct sockaddr_in addr;
                int ret;
                int fd;

                fd = socket(AF_INET, SOCK_STREAM, 0);
                if (fd == -1) {
                    fprintf(stderr, "Unable to create socket\n");
                    return EIO;
                }

                addr.sin_family = AF_INET;
                addr.sin_port = htons(3333);
                addr.sin_addr.s_addr = inet_addr("127.0.0.1");

                ret = connect(fd, (struct sockaddr *)&addr, sizeof(struct sockaddr_in));
                if (ret != 0) {
                    ret = errno;
                    fprintf(stderr, "Unable to connect to localhost:3333 [%d]: %s\n",
                            ret, strerror(ret));
                    return ret;
                }

                *_fd = fd;

                return 0;
            }

            static void fd_readable_handler(struct tevent_context *ev,
                                            struct tevent_fd *fde,
                                            uint16_t flags,
                                            void *pvt)
            {
                int fd = *(int*)pvt;
                char buf[255] = {0};
                int ret;

                puts("File descriptor is readable!");
                ret = read(fd, &buf, 254);
                printf("ret = %d, errno = %d\n", ret, errno);
                printf("Data read: %s\n", buf);
            }

            int main()
            {
                struct tevent_context *ev;
                struct tevent_fd *fde;
                int ret;
                int fd;

                /* Initialize tevent context. */
                ev = tevent_context_init(NULL);
                if (ev == NULL) {
                    puts("Unable to create tevent context.");
                    return 1;
                }

                /* Open socket. */
                ret = open_socket(&fd);
                if (ret != 0) {
                    puts("Unable to open socket.");
                    return 1;
                }

                /* Register event handler - executed when the fd is readable */
                fde = tevent_add_fd(ev, NULL, fd, TEVENT_FD_READ, fd_readable_handler, &fd);
                if (fde == NULL) {
                    puts("Unable to create fde.");
                    return 1;
                }

                /* Enter the event loop. */
                while (true) {
                    tevent_loop_wait(ev);
                }
            }

        .. code-block:: console

            $ ncat -v -l 127.0.0.1 3333                     |
            Ncat: Version 7.80 ( https://nmap.org/ncat )    |
            Ncat: Listening on 127.0.0.1:3333               |
                                                            |   $ gcc ./main.c -ltalloc -ltevent
                                                            |   $ ./a.out
            Ncat: Connection from 127.0.0.1.                |
            Ncat: Connection from 127.0.0.1:45900.          |
            hello                                           |
                                                            |   File descriptor is readable!
                                                            |   ret = 6, errno = 0
                                                            |   Data read: hello
            world                                           |
                                                            |   File descriptor is readable!
                                                            |   ret = 6, errno = 0
                                                            |   Data read: world

    .. plain-tab::
        :label: Timer example

        .. code-block:: c

            /**
            * Execute handler after five seconds.
            */

            #include <stdio.h>
            #include <tevent.h>

            static void handler(struct tevent_context *ev,
                                struct tevent_timer *tim,
                                struct timeval current_time,
                                void *private_data)
            {
                puts("I was executed with some delay.");
            }

            int main()
            {
                struct tevent_context *ev;
                struct tevent_timer *te;
                struct timeval delay;

                /* Initialize tevent context. */
                ev = tevent_context_init(NULL);
                if (ev == NULL) {
                    return 1;
                }

                delay = tevent_timeval_current_ofs(5, 0); // Execute handler after 5 seconds
                te = tevent_add_timer(ev, NULL, delay, handler, NULL);
                if (te == NULL) {
                    return 2;
                }

                tevent_loop_wait(ev);

                return 0;
            }

        .. code-block:: console

            $ gcc ./main.c -ltalloc -ltevent
            $ ./a.out
            I was executed with some delay.

    .. plain-tab::
        :label: Immediate event example

        .. code-block:: c

            /**
            * Schedule an immediate event and finish.
            */

            #include <stdio.h>
            #include <tevent.h>

            void handler(struct tevent_context *ctx, struct tevent_immediate *im, void *pvt)
            {
                puts("Hello world.");
            }

            int main()
            {
                struct tevent_context *ev;
                struct tevent_immediate *im;
                int i;

                /* Initialize tevent context. */
                ev = tevent_context_init(NULL);
                if (ev == NULL) {
                    return 1;
                }

                im = tevent_create_immediate(ev);
                if (im == NULL) {
                    return 2;
                }

                tevent_schedule_immediate(im, ev, handler, NULL);
                tevent_loop_wait(ev);

                return 0;
            }

        .. code-block:: console

            $ gcc ./main.c -ltalloc -ltevent
            $ ./a.out
            Hello world.

.. note::

    It is important to understand how these low level events work, however you
    most likely will not need to work with them directly since SSSD already
    provides a higher level API around them that is implemented via tevent
    requests (for example periodic tasks, querying an LDAP server, etc.).

    :tag:`strong` `Tevent requests`_ are fundamental part of SSSD code. They
    provide a high level interface to asynchronous programming and you will work
    with them and even create them all the time. Therefore it is recommended to
    pay extra attention to the following chapter. :end-tag:`strong`

Tevent requests
***************

Tevent requests is a callback-based API. They are an entry point to the low
level asynchronous events (such as non-blocking input and output operations) and
they provide a unified callback interface that helps you write asynchronous code
that reads and feels almost like a synchronous code. The readability and
simplicity of such code is improved dramatically just by following a specific
coding pattern and naming conventions.

The following diagram shows you the basic request flow to give you initial idea
about tevent requests. It share some resemblance with ``async/await`` constructs
of modern languages or Javascript's ``Promise``.

.. mermaid::

    sequenceDiagram
    participant ev     as Event Loop
    participant c      as Caller
    participant req    as Request
    participant subreq as Subrequest
    participant io     as I/O


    ev ->> c: Incoming message
    c ->> req: Send request
    req ->> subreq: Send subrequest
    subreq ->> io: Start async I/O
    io -->> subreq: Register callback
    subreq -->> req: Register callback
    req -->> c: Register callback
    c ->> ev: Return to event loop
    ev ->> ev: Await event
    ev ->> io: I/O done
    io -->> subreq: Execute callback
    subreq ->> io: Receive data
    subreq -->> req: Execute callback
    req ->> subreq: Receive data
    req -->> c: Execute callback
    c ->> req: Receive data
    c ->> ev: Return to event loop

Request components
==================

Each request is associated with its internal state (a structure), it needs to be
named, created, finished and consumed. When the request is created it starts an
asynchronous operation by registering a low level event (fd, timer, immediate).
The request itself does not always have to register the low level event, but
since the requests can be nested it often instantiates a subrequest instead.
However the event handler is always registered at the end of the nested request
chain and the code steps into the asynchronous processing.

The request components are:

state structure (state)
    The request data are always stored in a structure. This data are accessible
    in every part of the requests. It is a talloc memory context that is often
    use as a parent for internal request data.

send function (send)
    This is the entry point to the request. it creates the request using
    ``tevent_req_create()`` and it also either initializes an asynchronous
    operation or sends another subrequest after the request is created.

done function (done)
    This is the request terminator. It finishes the request with
    ``tevent_req_done()``. A callback associated with the request is called once
    it is finished.

step function (step)
    Sometimes the request is more complicated and it requires multiple steps to
    finish. There can be multiple step functions that takes place between send
    and done. For example the request may perform an asynchronous iteration,
    like obtaining multiple objects from LDAP in sequence.

receiver function (recv)
    The output data are consumed by the caller using a receiver.

caller
    Caller is the request consumer. It sends the requests and registers a
    callback that is executed when the request is finished. The callback then
    consumes requests output by calling the receiver.

The following diagram shows you the execution flow of a request:

.. mermaid::

    graph LR
        caller[caller]
        send(send)
        step1(step 1)
        stepN(step N)
        done(done)
        callback[callback]
        recv(recv)

        classDef req fill:green,stroke:green,stroke-width:1px,fill-opacity:0.2
        classDef cb fill:blue,stroke:blue,stroke-width:1px,fill-opacity:0.2
        class send,step1,stepN,done,recv req
        class caller,callback cb

        caller --> send --> step1 -.-> stepN --> done --> callback --> recv

Naming conventions
==================

The naming conventions make it easy to orient in tevent requests code. Let us
assume we have a request named ``fetch_user``. The correct component names are:

.. table::
    :align: left
    :widths: 1, 4
    :width: 100%

    ========= ===================================================
    Component Name
    ========= ===================================================
    state     ``struct fetch_user_state``
    send      ``struct tevent_req *fetch_user_send(...)``
    done      ``void fetch_user_done(...)``
    recv      ``errno_t fetch_user_recv(...)``
    ========= ===================================================

See how the ``_state``, ``_send``, ``_done`` and ``_recv`` suffixes are used.
Additionally, we use variable names ``req`` and ``subreq`` to resemble the
current request and its subrequest.

It is also important to write the components in correct order. The goal is to be
able to read the request code from top to bottom so it can be nicely read as a
synchronous code. The expected and mandatory order is:

.. code-block:: c

    struct fetch_user_state;
    struct tevent_req *fetch_user_send(...);
    void fetch_user_done(...);
    errno_t fetch_user_recv(...);

Example request
===============

Let's implement the request ``fetch_user`` from `Naming conventions`_. The
purpose of this request is to lookup a user by name in an LDAP server. The
example will issue a subrequest instead of implementing asynchronous
communication with the remote server in order to maintain simplicity. The steps
are:

#. Create the request
#. The request will reuse already existing request ``query_ldap`` that handles
   the communication with the LDAP server
#. Once the query is finished we will read the result and store it in the state
#. We will finish the request

.. code-block:: c

    struct fetch_user_state {
        struct ldap_result *result;
    };

    static void fetch_user_done(struct tevent_req *subreq);

    struct tevent_req *fetch_user_send(TALLOC_CTX *mem_ctx,
                                    struct tevent_context *ev,
                                    const char *name)
    {
        struct fetch_user_state *state;
        struct tevent_req *subreq;
        struct tevent_req *req;
        errno_t ret;

        req = tevent_req_create(mem_ctx, &state, struct fetch_user_state);
        if (req == NULL) {
            DEBUG(SSSDBG_CRIT_FAILURE, "tevent_req_create() failed\n");
            return NULL;
        }

        subreq = query_ldap_send(state, ev, "(name=%s)", name);
        if (subreq == NULL) {
            ret = ENOMEM;
            goto done;
        }

        tevent_req_set_callback(subreq, fetch_user_done, req);

        return req;

    done:
        tevent_req_error(req, ret);
        tevent_req_post(req, ev);

        return req;
    }

    static void fetch_user_done(struct tevent_req *subreq)
    {
        struct fetch_user_state *state;
        struct tevent_req *req;
        errno_t ret;

        req = tevent_req_callback_data(subreq, struct tevent_req);
        state = tevent_req_data(req, struct fetch_user_state);

        ret = query_ldap_recv(state, subreq, &state->result);
        talloc_zfree(subreq);
        if (ret != EOK) {
            goto done;
        }

    done:
        if (ret != EOK) {
            tevent_req_error(req, ret);
            return;
        }

        tevent_req_done(req);
    }

    errno_t fetch_user_recv(TALLOC_CTX *mem_ctx,
                            struct tevent_req *req,
                            struct ldap_result **_result)
    {
        struct fetch_user_state *state = NULL;
        state = tevent_req_data(req, struct fetch_user_state);

        TEVENT_REQ_RETURN_ON_ERROR(req);

        *_result = talloc_steal(mem_ctx, state->result);

        return EOK;
    }

.. note::

    If an error occurs before the request had a chance to step into an
    asynchronous processing (that is any error in the send function) before the
    caller had a chance to register a callback, it is necessary to call
    ``tevent_req_post()``. This makes sure that the callback is executed once it
    is registered.

    If the request finished successfully it is terminated with
    ``tevent_req_done``. If it ends with an error then use ``tevent_req_error``.
    Both functions will execute the caller's callback immediately if it is
    available.


Calling the request
===================

The previous chapter showed how the request is created. The following example
shows how it is used.

.. code-block:: c

    errno_t caller(TALLOC_CTX *mem_ctx,
                   struct tevent_context *ev)
    {
        struct tevent_req *req;
        errno_t ret;

        req = fetch_user_send(mem_Ctx, ev, "John Doe");
        if (req == NULL) {
            return ENOMEM;
        }

        tevent_req_set_callback(req, caller_done, /* private data if any */ NULL);
    }

    void caller_done(struct tevent_req *req)
    {
        struct ldap_result *result;

        ret = fetch_user_recv(NULL, req, &result);
        talloc_zfree(req);
        if (ret != EOK) {
            goto done;
        }

        print_result(result);
    }

.. note::

    See how the request is freed immediately after ``fetch_user_recv`` is
    called. This step is an important coding pattern to ensure that no memory is
    leaked.

The caller is usually executed from the event loop as a reaction to an incoming
event, usually when a user requested a specific operation like calling a ``HTTP
GET`` on an HTTP server. The example code can be translated into a sequence
diagram to illustrate the flow further.

.. mermaid::

    sequenceDiagram
    participant ev     as Event Loop
    participant c      as Caller
    participant req    as Request
    participant subreq as Subrequest
    participant io     as I/O


    ev ->> c: Incoming message
    c ->> req: fetch_user_send
    req ->> subreq: query_ldap_send
    subreq ->> io: Start async I/O
    io -->> subreq: Register callback
    subreq -->> req: Register callback
    req -->> c: Register callback
    c ->> ev: Return to event loop
    ev ->> ev: Await event
    ev ->> io: I/O done
    io -->> subreq: query_ldap_done
    subreq ->> io: Receive data
    subreq -->> req: fetch_user_done
    req ->> subreq: query_ldap_recv
    req -->> c: caller_done
    c ->> req: fetch_user_recv
    c ->> ev: Return to event loop

The caller itself does not need to know what happens internally in the
``fetch_user`` request. Therefore the execution flow can be simplified and
translated into the following sequence, which nicely illustrates how an
asynchronous code can be read and written with a synchronous code flow using the
tevent requests.

.. mermaid::

    graph LR
        caller[caller]
        send(fetch_user_send)
        step(...)
        done(fetch_user_done)
        callback[caller_done]
        recv(fetch_user_recv)

        classDef req fill:green,stroke:green,stroke-width:1px,fill-opacity:0.2
        classDef cb fill:blue,stroke:blue,stroke-width:1px,fill-opacity:0.2
        class send,step,done,recv req
        class caller,callback cb

        caller --> send --> step --> done --> callback --> recv