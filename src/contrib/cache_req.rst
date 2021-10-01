.. contents:: Table of Contents
    :local:

Unified Cache Interface
#######################

The unified cache interface (``cache_req``) is an integral component of the SSSD data flow, consumed by most SSSD responders including NSS, PAM, InfoPipe, autofs and ssh.

The ``cache req`` component implements a generic interface for SSSD requests. The interface is responsible for handling the logic for domain selection, cache lookups, and sending requests to the backend. ``cache_req`` implements a plugin architecture where a plugin exists for each object request type. The plugin dictates the behavior of cache request, which attributes should be used to lookup the object in the cache, etc. Each request follows similar logic through the cache request interface, making it easier to understand and debug.

.. mermaid::

    graph LR
        app(Application)
        gnss(glibc-NSS)
        snss(sssd_nss)
        cache_req(cache_req)
        lcache(local cache)
        be(backend)

        style gnss fill:green,stroke:green,stroke-width:1px,fill-opacity:0.2
        style snss fill:green,stroke:green,stroke-width:1px,fill-opacity:0.2
        style cache_req fill:blue,stroke:blue,stroke-width:1px,fill-opacity:0.2
        style lcache fill:yellow,stroke:yellow,stroke-width:1px,fill-opacity:0.2
        style be fill:purple,stroke:purple,stroke-width:1px,fill-opacity:0.2
        
        app --> gnss
        gnss --> snss
        snss --> cache_req
        cache_req --> lcache
        lcache <--> be
        be --> lcache


How to use the cache_req API
****************************

Initiating a cache request is done by calling the tevent request input function ``cache_req_send``

.. code-block:: c

    struct tevent_req *cache_req_send(TALLOC_CTX *mem_ctx,
                                      struct tevent_context *ev,
                                      struct resp_ctx *rctx,
                                      struct sss_nc_ctx *ncache,
                                      int midpoint,
                                      enum cache_req_dom_type req_dom_type,
                                      const char *domain,
                                      struct cache_req_data *data);

Arguments
=========

midpoint
    Handle background (out of band) object refreshes. It is used to enable the ``entry_cache_nowait_percentage`` configuration option in the NSS responder. Set this argument to 0 for non-NSS responder callers.

.. note::

    A **midpoint** refresh is a cache performance optimization implemented in cache req code, it is used to avoid a blocking call when refreshing an entry after the entry has expired. This allows SSSD to refresh cached entries in the background prior to a cached object/entry expiration, based on a configurable (``entry_cache_nowait_percentage``) percentage. The entry is returned from the cache immediately, but also a request to refresh the object in the backend is performed. The end result is that no delay is seen on the client side.

req_dom_type
    Limit the request type lookups to only POSIX Domains (``CACHE_REQ_POSIX_DOM``), only ``CACHE_REQ_APPLICATION_DOM`` or any domain type (``CACHE_REQ_ANY_DOM``). POSIX domains are reachable by all services. Application domains are only reachable from the InfoPipe responder and the PAM responder. Only objects from POSIX domains are available to the operating system interfaces (NSS) and utilities.

domain
    Request searching an explicit domain, NULL otherwise. When ``domain`` is NULL we delegate the logic of domain selection to ``cache req``.

data
    Must be a ``struct cache_req_data`` formatted data. Several helper functions exist to create this cache_req_data (See ``cache_req_data_*`` in `cache_req.h <https://github.com/SSSD/sssd/blob/master/src/responder/common/cache_req/cache_req.h>`_) based on the type of input data.

Retrieving the output from the cache request is done with either of the two ``_recv`` functions:

.. code-block:: c

    errno_t cache_req_recv(TALLOC_CTX *mem_ctx,
                           struct tevent_req *req,
                           struct cache_req_result ***_results);

    errno_t cache_req_single_domain_recv(TALLOC_CTX *mem_ctx,
                           struct tevent_req *req,
                           struct cache_req_result **_result);

You may want to only skip searching the local cache, or the data provider. The public functions in ``cache_req.h`` can be used to tune the behavior of the request lookups. See ``lookup_behavior``

.. code-block:: c

    void
    cache_req_data_set_bypass_cache(struct cache_req_data *data,
                                    bool bypass_cache)

    void
    cache_req_data_set_bypass_dp(struct cache_req_data *data,
                                 bool bypass_dp)

    void
    cache_req_data_set_requested_domains(struct cache_req_data *data,
                                         char **requested_domains)

A simple caller example (user initgroups request) may look as follows:

.. code-block:: c

    /* Prepare the input data */
    data = cache_req_data_name(mem_ctx, CACHE_REQ_INITGROUPS, user_name);

    /* Optional settings */
    cache_req_data_set_bypass_cache(data, false);
    cache_req_data_set_bypass_dp(data, true);
    cache_req_data_set_requested_domains(data, requested_domains);

    /* Initiate the request */
    dpreq = cache_req_send(mem_ctx,
                           ev,
                           rctx,
                           rctx->ncache,
                           0,                  /* Disable midpoint refresh */
                           CACHE_REQ_ANY_DOM,  /* Don't limit domain type */
                           NULL,               /* No explicit domain */
                           data);

    /* Set callback function */
    tevent_req_set_callback(dpreq, sample_user_initgr_done, req);

And inside the callback function:

.. code-block:: c

    static void sample_user_initgr_done(struct tevent_req *subreq)
    {
        struct cache_req_result *result;
        ...  /* Other vars */

        req = tevent_req_callback_data(subreq, struct tevent_req);
        state = tevent_req_data(req, struct sample_user_initgr_state);

        ret = cache_req_single_domain_recv(state, subreq, &result);
        talloc_zfree(subreq);
        if (ret != EOK) {
            tevent_req_error(req, ret);
            return;
        }

        /* Do something with result */

Under the hood
**************

This section is used to describe the cache request interface details, and explain what happens behind the scenes.

Cache request setup
===================

Inside cache request code (``cache_req_send``, ``cache_req_create``, and ``cache_req_process_input``), setup and initialization of cache request plugins, input data and necessary cache request structures is performed.

Lookup Behavior
---------------

Cache request lookup behavior is set here to one of the following 4 modes:

.. code-block:: c

    enum cache_req_behavior {
        CACHE_REQ_NORMAL,
        CACHE_REQ_CACHE_FIRST,
        CACHE_REQ_BYPASS_CACHE,
        CACHE_REQ_BYPASS_PROVIDER,
    };

CACHE_REQ_NORMAL
    Default lookup behavior, described in the :doc:`../contrib/architecture` document.

CACHE_REQ_CACHE_FIRST
    SOn first iteration, the search will only check the cache and will not trigger any request to the data provider/backend. If the requested data is not found then a second lookup will search only in the data provider, not the cache. Set based on the sssd.conf ``cache_first`` option. 

CACHE_REQ_BYPASS_CACHE
    Always contact the data provider before searching the cache. Set with a call to ``cache_req_data_set_bypass_cache``, 

CACHE_REQ_BYPASS_DP
    Always search in the local cache and do **not** perform a lookup to the data provider. Set with a call to ``cache_req_data_set_bypass_dp``

.. note::

    ``CACHE_REQ_BYPASS_CACHE`` does **not** bypass the cache entirely. Data returned from the data provider is always first added into the cache then a local cache lookup will return the refreshed data. It may help to think of bypass cache as **dp_first** instead.

Input name parsing
------------------

All cache request plugins explicitly set the ``parse_name`` and ``ignore_default_domain`` structure members booleans.

.. code-block:: c

    const struct cache_req_plugin cache_req_user_by_name = {
        .name = "User by name",
        ...
        .parse_name = true,
        .ignore_default_domain = false,
        ...

Cache request plugins which accept a name as input will often set the ``parse_name`` boolean to ``true``. The cache request logic will then assume an input name may contain a domain name which needs to be parsed. This domain name parsing also factors in the ``ignore_default_domain`` plugin boolean, determining if the cache request will also append the default domain when no domain component is found during parsing. When ``parse_name`` is ``false``, the input type does not need to be parsed and cache request can assume the input as-is.

An input name may contain a ``name@UPN``, instead of the typical ``name@domain``. ``cache_req`` can automatically detect this when parsing an input name where no matching domain is found.

.. code-block:: c

    const struct cache_req_plugin cache_req_user_by_name = {
        .name = "User by name",
        ...
        .allow_switch_to_upn = true,
        .upn_equivalent = CACHE_REQ_USER_BY_UPN,
        ...

If the plugin sets ``allow_switch_to_upn`` then the plugin ``upn_equivalent`` is set with ``cache_req_set_plugin``

Domain selection
================

Single domain request
---------------------

As mentioned in `How to use the cache_req API`_, the caller of ``cache_req_send()`` can specify a domain argument to tell cache request to perform a single-domain only search.

Restrict to certain domains
---------------------------

The function ``cache_req_data_set_requested_domains`` can be called, providing a list of domain names. This will cause cache_req to search for the object only in those requested domains.

Multi-domain search
-------------------

If no ``domain`` argument is provided to ``cache_req_send``, then a multi-domain search is executed. Here again we take cache_req plugin variables into consideration.

.. code-block:: c

    const struct cache_req_plugin cache_req_group_by_id = {
        ...
        .allow_missing_fqn = true,
        .get_next_domain_flags = SSS_GND_DESCEND,
        ...

If ``allow_missing_fqn`` is set to ``false``, then this multi domain search iterating through domains will skip domains which require fully qualified names.

``get_next_domain_flags`` sets the flags which are passed to ``get_next_domain()`` during iteration. At the time of this writing, cache request plugins set this to ``0`` or ``SSS_GND_DESCEND`` to determine behavior when iterating through multiple domains.

.. table::
    :align: left
    :widths: 1, 3
    :width: 70%

    =========================== ====================================
    Domain Flags                Behavior
    =========================== ====================================
    0                           ``Skip subdomains in iteration``
    SSS_GND_DESCEND             ``Include subdomains in iteration``
    =========================== ====================================

Preparing the domain
--------------------

Before performing the object search inside the domain, the ``prepare_domain_data_fn`` is called, this is used by some plugins to alter lookup data per specific domain rules, such as case sensitivity, fully qualified format, etc.

Domain locator
--------------

The domain locator plugin exists to alleviate performance problems when SSSD must iterate over several domains (e.g. AD forest with multiple domains) for each unqualified name or by-ID lookups. The domain locator can help to find the correct domain to search early on in the lookup flow, instead of iterating through all domains.

The domain locator functionality is set currently only for ``CACHE_REQ_OBJECT_BY_ID``, ``CACHE_REQ_GROUP_BY_ID``, ``CACHE_REQ_USER_BY_ID`` plugins.

.. code-block:: c

    const struct cache_req_plugin cache_req_object_by_id = {
        ...
        .dp_get_domain_check_fn = cache_req_object_by_id_get_domain_check,
        .dp_get_domain_send_fn = cache_req_object_by_id_get_domain_send,
        .dp_get_domain_recv_fn = cache_req_common_get_acct_domain_recv,

A cache-only search is performed first to check if the object already exists in the cache. If not, then we execute the domain locator plugin ``dp_get_domain_check_fn`` function to check if the id exists in the negative cache. If it is not in the negative cache, then we call the ``dp_get_domain_send_fn``

The send function sends an SBUS ``getAccountDomain`` request to the backend, if a domain is reported as containing an object, all domains except that
one are marked with negative cache entries for that request(using the associated ``.ncache_add_fn`` plugin function.

The domain locator plugin code is only executed for unqualified requests with multiple domains or on the second pass of a ``CACHE_REQ_CACHE_FIRST`` lookup.

.. code-block:: c

    if (cr->plugin->dp_get_domain_send_fn != NULL
            && ((state->check_next && cr_domain->next != NULL)
                || ((state->cr->cache_behavior == CACHE_REQ_CACHE_FIRST)
                    && !first_iteration))) {
        /* If the request is not qualified with a domain name AND
         * there are multiple domains to search OR if this is the second
         * pass during the "check-cache-first" schema, it makes sense
         * to try to run the domain-locator plugin
         */
        cache_req_domain_set_locate_flag(cr_domain, cr);
    }


Performing the Search
=====================

.. image:: /contrib/architecture-lookup.svg
    :height: 700px
    :align: center

In a multi-domain search, the below logic repeats for each domain until a result is found, or SSSD searched all available (or requested) domains. Let's assume the normal cache behavior ``CACHE_REQ_NORMAL``, most of the conditional logic in the search code flow is based on the cache behavior type.

* First the search checks the negative cache using the plugin ``ncache_check_fn`` function. If the object exists in the negative cache, and the negative cache timeout has not been reached then ``cache_req`` will return ``ENOENT``.

.. code-block:: c

    .ncache_check_fn = cache_req_user_by_name_ncache_check,

* Next, search the cache to see if the object already exists in the local cache. Here, the plugin-defined ``lookup_fn`` is used to handle the different object types and ``SYSDB`` attributes to search. If the object is found and is not expired, it can be returned successfully.

* If the object is expired, or not found then the plugin ``dp_send_fn`` and ``dp_recv_fn`` are used inside ``cache_req_search_dp`` to trigger a backend search. This backend search will update the cache, then ``cache_req_search_done()`` searches the cache again for the now-existing object.

.. warning::

    If multiple objects are found when the plugin ``only_one_result`` is set to true then ``ERR_MULTIPLE_ENTRIES`` is returned.

.. note::

    When results are found in a multiple domain search, if the plugin **search_all_domains** is true then ``cache_req`` continues to search all domains and merges the results.


Debug ID
========

A cache request contains an ID in ``cr``, used for debugging and allows anyone viewing SSSD logs to follow along a certain request through the life of the cache request. This id is an unsigned integer which increments by 1 for each new request.

.. code-block:: c

    struct cache_req {
    ...

    /* Debug information */
    uint32_t reqid;

Extending cache_req
*******************

Due to the importance of ``cache_req`` in the SSSD data flow, ``cache_req`` will need to be extended going forward to handle additional SSSD use cases.

This may include adding new code paths into cache_req processing logic, see the domain locator feature addition in `Use the domain-locator request to only search domains where the entry was found <https://github.com/SSSD/sssd/commit/f2a5e29f063f9d623c1336d76f4b2bc500c1a5e2>`_ and `Add plugin methods required for the domain-locator request <https://github.com/SSSD/sssd/commit/2856dac5818265a6b4e42d768b73c65e333d14ff>`_

Adding a new plugin
===================

Plugins can be added to expand the functionality of ``cache_req``, for example the commit `add autofs map entries plugin <https://github.com/SSSD/sssd/commit/8b2ab48871758acbd5ab5675b3965a776d0c5457>`_ adds the ``CACHE_REQ_AUTOFS_MAP_ENTRIES`` plugin.

When adding a new plugin you will need to decide which object-specific plugin operations need to be included.

.. code-block:: c

    /* Operations */
    cache_req_is_well_known_result_fn is_well_known_fn;
    cache_req_prepare_domain_data_fn prepare_domain_data_fn;
    cache_req_create_debug_name_fn create_debug_name_fn;
    cache_req_global_ncache_add_fn global_ncache_add_fn;
    cache_req_ncache_check_fn ncache_check_fn;
    cache_req_ncache_add_fn ncache_add_fn;
    cache_req_ncache_filter_fn ncache_filter_fn;
    cache_req_lookup_fn lookup_fn;
    cache_req_dp_send_fn dp_send_fn;
    cache_req_dp_recv_fn dp_recv_fn;
    cache_req_dp_get_domain_check_fn dp_get_domain_check_fn;
    cache_req_dp_get_domain_send_fn dp_get_domain_send_fn;
    cache_req_dp_get_domain_recv_fn dp_get_domain_recv_fn;

At a minimum, you will need to add custom functions into ``src/responder/common/cache_req/plugins/cache_req_new_plugin.c`` for the below operations. The naming scheme below should also be used:

.. code-block:: c

    /* Search for object entries in local cache: lookup_fn */
    cache_req_new_plugin_lookup()

    /* Search for, and retrieve object in the backend: dp_send_fn, dp_recv_fn */
    cache_req_new_plugin_dp_send()
    cache_req_new_plugin_dp_recv()

    /* Create debug name for object */
    cache_req_new_plugin_create_debug_name()

Then you will need to consider if you need to do some domain preparation prior to lookups and define a ``prepare_domain_data_fn``, or add negative cache custom functions in ``ncache_check_fn`` and ``ncache_add_fn`` if the object type supports negative cache entries.

Next you need to decide how your plugin will handle certain cases, these switches have been discussed earlier in this article, but you can see a basic description in ``src/responder/common/cache_req/cache_req_plugin.h``

.. code-block:: c

    .name = "Group by name",
    .attr_expiration = SYSDB_CACHE_EXPIRE,
    .parse_name = true,
    .ignore_default_domain = false,
    .bypass_cache = false,
    .only_one_result = true,
    .search_all_domains = false,
    .require_enumeration = false,
    .allow_missing_fqn = false,
    .allow_switch_to_upn = false,
    .upn_equivalent = CACHE_REQ_SENTINEL,
    .get_next_domain_flags = SSS_GND_DESCEND,
