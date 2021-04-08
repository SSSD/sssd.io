Periodical refresh of expired entries
=====================================

Related ticket(s):

-  `Add a task to the SSSD to periodically refresh cached
   entries <https://pagure.io/SSSD/sssd/issue/1713>`__

Problem Statement
-----------------

Large deployments may suffer from latency when refreshing a big number
of expired entries, for instance during logins that involve refreshing
netgroups.

Overview of the solution
------------------------

We will create a back end task, that will periodically search and update
all expired NSS entries. The periodic task it self is provider
independent and it leverage new `periodic tasks
API <https://docs.pagure.org/SSSD.sssd/design_pages/periodic_tasks.html>`__.
The task will fetch all expired entries and invoke a provider specific
callback to update those entries.

Implementation details
----------------------

::

    typedef struct tevent_req *
    (*nss_refresh_records_send_t)(TALLOC_CTX *mem_ctx,
                                  struct be_ctx *be_ctx,
                                  const char **dn,
                                  void *pvt);

    typedef errno_t
    (*nss_refresh_records_recv_t)(struct tevent_req *req);

    struct nss_refresh_records_cb {
        bool enabled;
        nss_refresh_records_send_t send;
        nss_refresh_records_recv_t recv;
        void *pvt;
    }

    enum nss_refresh_type {
        NSS_REFRESH_TYPE_USERS,
        NSS_REFRESH_TYPE_GROUPS,
        ... for all NSS objects

        NSS_REFRESH_TYPE_SENTINEL
    };

    struct nss_refresh_records_ctx {
        struct nss_refresh_records_cb callbacks[NSS_REFRESH_TYPE_SENTINEL];
    };

    struct nss_refresh_records_init();

    errno_t
    nss_refresh_records_add_cb(struct nss_refresh_records_ctx *ctx,
                               enum nss_refresh_type type,
                               nss_refresh_records_send_t send,
                               nss_refresh_records_recv_t recv,
                               void *pvt);

    struct tevent_req *
    nss_refresh_records_send(TALLOC_CTX *mem_ctx,
                             struct be_ctx *be_ctx,
                             void *pvt /* struct nss_refresh_records_ctx */

    errno_t
    nss_refresh_records_recv(struct tevent_req *req);

A new nss\_refresh\_records\_ctx is created during back end start up and
it is made a member of be\_ctx. Every ID provider can install an update
function during its initialization via
*nss\_refresh\_records\_add\_cb()*. Every callback can be installed only
once. After all providers are initialized, back end creates a new
periodic task for refreshing NSS expired entries.

*nss\_refresh\_records\_send()* will go through the callback list. When
a callback is enabled it will acquire a list of all expired entries
distinguish names and call the provider-specific request to refresh
them.

Author(s)
---------

Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
