Periodic task API
=================

Related ticket(s):

-  `unite periodic refresh
   API <https://pagure.io/SSSD/sssd/issue/1891>`__

Problem Statement
-----------------

SSSD contains several periodic tasks that implements custom periodic
API. These APIs are more or less sophisticated but it does the same
thing.

Current periodic tasks are:

-  Enumeration
-  Dynamic DNS updates
-  SUDO - full and smart refresh
-  Refresh of expired NSS entries

We want to replace these individual implementation with one back end
wise API.

Implementation details
----------------------

::

    New error code:
    - ERR_STOP_PERIODIC_TASK

    struct be_ptask;

    typedef struct tevent_req *
    (*be_ptask_send_t)(TALLOC_CTX *mem_ctx,
                       struct be_ctx *be_ctx,
                       struct be_ptask *be_ptask,
                       void *pvt);

    typedef errno_t
    (*be_ptask_recv_t)(struct tevent_req *req);

    enum be_ptask_offline {
        BE_PTASK_OFFLINE_SKIP,
        BE_PTASK_OFFLINE_DISABLE,
        BE_PTASK_OFFLINE_EXECUTE
    };

    errno_t be_ptask_create(TALLOC_CTX *mem_ctx,
                            struct be_ctx *be_ctx,
                            time_t period,
                            time_t first_delay,
                            time_t enabled_delay,
                            time_t timeout,
                            enum be_ptask_offline offline,
                            be_ptask_send_t send,
                            be_ptask_recv_t recv,
                            void *pvt,
                            const char *name,
                            struct be_ptask **_task);

    void be_ptask_enable(struct be_ptask *task);
    void be_ptask_disable(struct be_ptask *task);
    void be_ptask_destroy(struct be_ptask **task);

Terminology
~~~~~~~~~~~

-  task: object of type be\_ptask
-  request: tevent request that is fired periodically and is managed by
   task

API
~~~

-  *struct be\_ptask\_task* is encapsulated.
-  *be\_ptask\_create()* creates and starts new periodic task
-  *be\_ptask\_enable(task)* enable *task* and schedule next execution
   *enabled\_delay* from now
-  *be\_ptask\_disable(task)* disable *task*, cancel current timer and
   wait until it is enabled again
-  *be\_ptask\_destroy(task)* destroys *task* and sets it to *NULL*

Schedule rules
~~~~~~~~~~~~~~

-  the first execution is scheduled *first\_delay* seconds after the
   task is created
-  if request returns EOK, it will be scheduled again to
   'last\_execution\_time + period'
-  if request returns ERR\_STOP\_PERIODIC\_TASK, the task will be
   terminated
-  if request returns other error code (i.e. non fatal failure), it will
   be rescheduled to 'now + period'
-  if request does not complete in *timeout* seconds, it will be
   cancelled and rescheduled to 'now + period'
-  if the task is reenabled, it will be scheduled again to 'now +
   enabled\_delay'

When offline
~~~~~~~~~~~~

Offline behaviour is controlled by *offline* parameter.

-  If *offline* is *BE\_PTASK\_OFFLINE\_EXECUTE* and back end is
   offline, current request will be executed as planned.
-  If *offline* is *BE\_PTASK\_OFFLINE\_SKIP* and back end is offline,
   current request will be skipped and rescheduled to 'now + period'.
-  If *offline* is *BE\_PTASK\_OFFLINE\_DISABLE*, an offline and online
   callback is registered. The task is disabled immediately when back
   end goes offline and then enabled again when back end goes back
   online.

Debugging
~~~~~~~~~

Task will provide enough debugging information so we can know exactly
when a task is created and destroy, when it is executed and finished and
when it will be executed in the future.

Author(s)
---------

Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
