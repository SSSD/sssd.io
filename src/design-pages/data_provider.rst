.. highlight:: none

Data Provider Refactoring
=========================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/385 <https://pagure.io/SSSD/sssd/issue/385>`__

Problem statement
-----------------

Current state of data provider interface is not extensible enough to
fulfill needs of planned SSSD features such as `SSSD Status Tool
<https://docs.pagure.org/SSSD.sssd/design_pages/sssctl.html>`__.
The main flaw that we aim to solve is to simplify adding of new methods,
properties and possibly signals using our *sbus* interface. As a side
effect we will also solve the following issues that are in current code:

-  encapsulate data provider from the rest of the code
-  fix poor memory hierarchy which creates occasional race condition on
   shutdown
-  convert method handlers to *simple* tevent requests that are not
   aware of data provider
-  handle D-Bus message reply automatically in data provider code

Terminology
~~~~~~~~~~~

This section clarifies the terminology that is used in this document.

-  **Backend**: Implementation of a domain (periodic tasks,
   online/offline callbacks, online check, ...)
-  **Data Provider**: Interface between backend and responders
-  **Module**: library implementing data provider interface (LDAP, IPA,
   AD, KRB5, PROXY)
-  **Target**: functionality implemented in modules (id, auth, chpass,
   selinux, autofs, sudo, hostid)

A general overview of the communication process is as follows.

#. Responder issues a method call with Data Provider through DP D-Bus
   API
#. Data Provider calls a method handler registered by configured module
#. Method handler is finished
#. Reply is sent to responder

Current state
-------------

This is just a brief summarization, please refer to the code to get the
whole picture.

At this moment each target can have only one method specified. The
method is defined by providing bet\_ops data in
sssm\_$module\_$target\_init function. Structure bet\_ops contains
*handler* that defines a method handler in addition with *check\_online*
which defines a method that should be called when SSSD is trying to
check if it can reestablish a connection and it is used only in
connection with ID provider. Field *finalize* was probably introduced as
a clean up function, however it is not used at all at the moment.

Even though it is not possible with current code to have different
private data for different methods, it is possible to extend this
structure to allow more methods. However, it would be nice to have it in
more automated and controlled way and we still can't use properties and
signals this way though. ::

    struct bet_ops {
        be_req_fn_t check_online;
        be_req_fn_t handler;
        be_req_fn_t finalize;
    };

Each target is defined in *struct bet\_data*. ::

    static struct bet_data bet_data[] = {
        {BET_NULL, NULL, NULL},
        {BET_ID, CONFDB_DOMAIN_ID_PROVIDER, "sssm_%s_id_init"},
        [...]
        {BET_MAX, NULL, NULL}
    };

Initialization function assigns the bet\_ops structure together with
private data. The private data are attached to *be\_ctx* in talloc
memory hierarchy which results in race conditions during shutdown
process. This is currently solved by *be\_spy* which basically forces
the desired order of freeing data, however we have seen some crashes on
shutdown which we were unable to figure out so far even with spies. ::

    /* Auth Handler */
    struct bet_ops sdap_auth_ops = {
        .handler = sdap_pam_auth_handler,
        .finalize = sdap_shutdown
    };

    int sssm_ldap_auth_init(struct be_ctx *bectx,
                            struct bet_ops **ops,
                            void **pvt_data)
    {
        struct sdap_auth_ctx *ctx;
        int ret;

        [...]

            *ops = &sdap_auth_ops;
            *pvt_data = ctx;
        }

        return ret;
    }

Goals to achieve
~~~~~~~~~~~~~~~~

-  make adding a new client automated and error proof
-  make adding a new target automated and error proof
-  make adding a new method automated and error proof
-  create a proper talloc hierarchy so we can control clean up process
-  support module's constructor and private data shared across target's
   initialization functions
-  make method handlers pure tevent requests that returns single error
   code
-  make method handlers not aware of reply process
-  improve debugging capabilities

   -  keep track of active requests
   -  make each request clearly visible in logs

-  allow methods with different output parameters
-  allow D-Bus objects, properties and signals
-  properly terminate all requests on clean up

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

A responder sends a *D-Bus method* to the data provider which is handled
by a D-Bus method handler. Depending on the introspect file this handler
may be called directly with *automatically parsed parameters or the
parsing may be left to handler implementation*. In the handler, we
process parameters and *create a data provider request*. This request
will call a data provider method handler which is a basic **tevent
request**. When the request is finished, data provider tevent callback
is invoked and it send a reply back to the responder. Depending on the
request result the reply message may be either error, sending an error
code and message, or success where a default or *custom \_recv* function
may be called to obtain and send additional attributes.

The whole data provider lifetime is controlled by a tevent request.
There is only one way in *(\_send)* and one way out *(\_recv)* from the
request. The data provider method handler has no knowledge about D-Bus
or data provider at all. The data flow looks like this: ::

    Responder -> (dbus) -> DP D-Bus method handler -> DP Request -> (tevent) -> DP method handler

    ... asynchronous processing ...

    (tevent done) -> (dp request done) -> (error detected) -> (dbus error) -> Responder
                                       -> (success)        -> (receive callback) -> (dbus) -> Responder

Data Provider Initialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section describes what is needed to initialize data provider. It
talks only about sections that may change in the future in order to
extend SSSD's functionality, it does not describe how it works under the
hood. The initialization basically consist of these steps:

**1. Initialization of data provider modules and targets**

Each modules and target needs to be initialized through it's initializer
functions in **src/providers/$modname/$modname\_init.c**. The whole
module can contain a constructor that may create data shared across all
or multiple modules, it is not required though. The functions names are
generated as follows:

A constructor is named **sssm\_$modname\_init** and has header: ::

    errno_t sssm_$modname_init(TALLOC_CTX *mem_ctx, struct be_ctx *be_ctx, void **shared_data);

A target initializer is named **sssm\_$modname\_$target\_init** and has
header: ::

    errno_t sssm_$modname_$target_init(TALLOC_CTX *mem_ctx, struct be_ctx *be_ctx, void *shared_data, struct dp_method *dp_methods);

Target initializer will at the end set all methods that are implemented
by this target via dp\_set\_method() example: ::

    errno_t sssm_ipa_sudo_init(TALLOC_CTX *mem_ctx,
                               struct be_ctx *be_ctx,
                               void *module_data,
                               struct dp_method *dp_methods)
    {
        struct ipa_sudo_ctx *sudo_ctx;

        /* ... */

        dp_set_method(dp_methods, DPM_SUDO_FULL_REFRESH, dp_ipa_sudo_full_refresh_send, dp_ipa_sudo_full_refresh_recv, sudo_ctx);
        dp_set_method(dp_methods, DPM_SUDO_SMART_REFRESH, dp_ipa_sudo_smart_refresh_send, dp_ipa_sudo_smart_refresh_recv, sudo_ctx);
        dp_set_method(dp_methods, DPM_SUDO_RULES_REFRESH, dp_ipa_sudo_rules_refresh_send, dp_ipa_sudo_rules_refresh_recv, sudo_ctx);
    }

**2. Registering a data provider client -- responders**

When a responder wants to establish D-Bus connection with data provider
it needs to send a Register method to handshake with the provider. Here
we test that the client is known and setup D-Bus method handlers. Each
client is monitored and when the connection is dropped we remove active
requests of this client. Internally, we actually only remove sbus
connection from the request but try to finish the request otherwise so
we can completely save data that were already downloaded into the sysdb
for further usage.

To add a new well-known client just add it into **enum dp\_clients** in
*dp\_private.h* and alter **dp\_client\_to\_string()** in
*dp\_client.c*.

**3. Registering D-Bus methods**

When the D-Bus service is created a D-Bus method handlers needs to be
registered. The following steps are needed to add a new method or
interface into the data provider.

#. Add new method (or interface) into data provider introspection file
   **dp\_iface.xml**
#. Register this interface or method in **dp\_iface.c** by providing the
   interface structure generated from the introspection file and
   amending **dp\_map** array
#. (optionally if needed) Add new data provider method and/or target
   into **enum dp\_methods** and **enum dp\_targets** respectively
#. Implement the method handler

D-Bus method handlers
^^^^^^^^^^^^^^^^^^^^^

The purpose of a D-Bus method handler is to parse parameters from a
D-Bus message (if they are not parsed automatically) and to create data
specific to the method called. Then the handler issues a new data
provider request through dp\_file\_request(). For example: ::

    int dp_sudo_full_refresh(struct sbus_request *sbus_req,
                             void *dp_cli,
                             uint32_t dp_flags)
    {
        dp_file_request(dp_cli, "SUDO Full Refresh", sbus_req,
                        dp_req_reply_default,
                        DPT_SUDO, DPM_SUDO_FULL_REFRESH, dp_flags, NULL);

        return EOK;
    }

The current handler rewritten to the new data provider interface may
look like: ::

    int dp_sudo_handler(struct sbus_request *sbus_req, void *dp_cli)
    {
        struct dp_sudo_data *data;
        uint32_t dp_flags;
        errno_t ret;

        data = talloc_zero(sbus_req, struct dp_sudo_data);
        if (data == NULL) {
            return ENOMEM;
        }

        ret = dp_sudo_parse_message(data, sbus_req->message, &dp_flags,
                                    &data->type, &data->rules);
        if (ret != EOK) {
            return ret;
        }

        dp_file_request(dp_cli, "sudo", sbus_req, dp_req_reply_std,
                        DPT_SUDO, DPM_SUDO_HANDLER, dp_flags, data);

        return EOK;
    }

If dp\_flags are provider the data provider will check the flags and act
accordingly. Currently only DP\_FAST\_REPLY is available which if set
sends
*org.freedesktop.sssd.Error.DataProvider.Offline*
immediately without calling the request handler.

Data Provider Request Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Data provider request handler is a tevent request implementing the
following headers: ::

    struct dp_req_params {
        struct tevent_context *ev;
        struct be_ctx *be_ctx;
        struct sss_domain_info *domain;
        enum dp_methods method;
        void *method_data;
        void *req_data;
    };

    typedef struct tevent_req *
    (*dp_req_send_fn)(TALLOC_CTX *mem_ctx, struct dp_req_params *params);

    typedef errno_t
    (*dp_req_recv_fn)(TALLOC_CTX *mem_ctx, struct tevent_req *req, void *data);

All parameters except memory context are combined into one structure to
simplify possible future extensions (thus when a new parameter needs to
be added we don't have to modify existing handler). The *data* in
receive function may be used to pass output parameters into the D-Bus
reply. For example, the following reply callback simulates current reply
message which returns major and minor error together with error message. ::

    void dp_req_reply_std(const char *req_name,
                          struct sbus_request *sbus_req,
                          struct tevent_req *handler_req,
                          dp_req_recv_fn recv_fn,
                          void *pvt)
    {
        struct dp_reply_data reply;
        const char *safe_err_msg;
        errno_t ret;

        ret = recv_fn(sbus_req, handler_req, &reply);
        if (ret != EOK) {
            DEBUG(SSSDBG_CRIT_FAILURE, "Bug: !EOK code returned?\n");
            talloc_free(sbus_req);
            return;
        }

        safe_err_msg = safe_be_req_err_msg(reply.message, reply.dp_error);

        DP_REQ_DEBUG(SSSDBG_TRACE_LIBS, req_name, "Returning [%s]: %d,%d,%s",
                     dp_err_to_string(reply.dp_error), reply.dp_error,
                     reply.error, reply.message);

        sbus_request_return_and_finish(sbus_req,
                                       DBUS_TYPE_UINT16, &reply.dp_error,
                                       DBUS_TYPE_UINT32, &reply.error,
                                       DBUS_TYPE_STRING, &safe_err_msg,
                                       DBUS_TYPE_INVALID);
    }

On memory hierarchy
~~~~~~~~~~~~~~~~~~~

The memory hierarchy is known strictly specified and should not be
broken. It gives us the ability to clearly clean up all data provider
data on SSSD exit. ::

                                   struct be_ctx
                                         |
                                struct data_provider
                            /            |              \
          struct dp_module[]      struct dp_target[]     struct dp_req [...]
                           |             |                |
                  module_data     struct dp_methods[]    req_data,tevent_req state,...
                                         |
                                    method_data

A destructor on data\_provider is set to ensure that all DP requests are
correctly terminated (sending a proper error message back to responder)
prior its private data is freed.

Implementation steps
~~~~~~~~~~~~~~~~~~~~

#. (done) Implement the new data provider interface
#. (wip) Convert modules init functions
#. (wip) Convert existing handlers into tevent requests
#. Switch to the new interface
#. Add new methods and interfaces as needed

Responders
~~~~~~~~~~

In the first stage no change to the responders needs to be done. All
existing data provider methods will always succeed and return three
output parameters (major error, minor error, error message) as the
current code does. New methods that return error or some output
parameters may be added without affecting the current responder data
provider code. When the new code is thoroughly tested we can change the
existing methods to return either error or success but this requires
also changes in responders. I would like to write something similar to
cache\_req but I don't have any specific plan so far.

Questions
~~~~~~~~~

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

No configuration changes.

How To Test
~~~~~~~~~~~

All existing test must pass and no functionality is broken.

How To Debug
~~~~~~~~~~~~

Each data provider request life cycle can be tracked in debug logs with
a special message prefix: **DP Request [$name #$index]**. The $name is
the name of the request (i.e. which method was called), $index is a
cyclic number assigned to the request. When we run out of number we
simply start from 1 again.

In the debugger we can monitor active data provider request, clients,
modules and targets in **be\_ctx->provider**.

Authors
~~~~~~~

Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
