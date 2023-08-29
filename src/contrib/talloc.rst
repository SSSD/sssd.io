Memory allocator: talloc
########################

`Talloc`_ is a hierarchical memory allocator which is used heavily inside SSSD
instead of ``malloc``. It allows you to manage memory of complex data structures
more naturally *by defining an oriented graph of memory context* and its
descendants and thus simplifying the data flow and error management. It also
extends the allocator with runtime type safety and destructors.

.. seealso::

    The talloc library provides many useful features and mastering it will help
    you to simplify the code and its logic a lot. However, this document
    provides only a basic description of talloc and its use cases and patterns
    inside the SSSD project. It is recommended for you to :tag:`strong` read the
    official `Talloc Tutorial`_ and `API Reference`_ to learn more about its
    features. :end-tag:`strong`

.. _Talloc: https://talloc.samba.org
.. _Talloc Tutorial: https://talloc.samba.org/talloc/doc/html/libtalloc__tutorial.html
.. _API Reference: https://talloc.samba.org/talloc/doc/html/group__talloc.html

Memory hierarchy
****************

Talloc organizes allocated memory into an oriented graph. This makes it very
easy to free complex data structures. See the following example to get the idea:

.. code-tabs::

    .. code-tab:: c
        :label: talloc

        struct record {
            char *name;
            char *value;
        };

        struct record *r;

        r = talloc_zero(NULL, struct record);
        r->name = talloc_strdup(r, "Hello");
        r->value = talloc_strdup(r, "World");

        talloc_free(r);

    .. code-tab:: c
        :label: malloc

        struct record {
            char *name;
            char *value;
        };

        struct record *r;

        r = malloc(sizeof(struct record));
        r->name = strdup("Hello");
        r->value = strdup("World");

        free(r->name);
        free(r->value);
        free(r);

We create a simple hierarchy of memory contexts by associating ``name`` and
``value`` with the record ``r``. This allows us to free the whole structure with
a single call to ``talloc_free(r)`` whereas we have to free each field if we do
not use talloc.

.. mermaid::

    graph TD
        r((r))
        n(name)
        v(value)

        linkStyle default interpolate basis
        style r fill:green,stroke:green,stroke-width:1px,fill-opacity:0.2

        r --> n
        r --> v

.. note::

    There are many functions that can create a new talloc memory context. These
    functions always take an existing talloc context as an argument that is used
    as the parent context. The newly allocated memory context becomes a child of
    the existing context and will be automatically freed when the parent is
    freed.

    For example ``talloc_new``, ``talloc_zero``,
    ``talloc_zero_array``, ``talloc_strdup``, ``talloc_strndup`` and
    ``talloc_asprintf``.

The example above is very simple for the demonstration purpose. But we often
have to use very complex and nested data structures in the real world and all of
them can be freed with a single call to ``talloc_free`` if we maintain the
correct memory hierarchy. We can look at ``struct sss_domain_info`` in
`confdb.h`_ to see an example of such complex structure. If we create a correct
hierarchy, we get the following graph *(heavily simplified for demonstration
purpose)*. Imagine how difficult it would be to create a function that would
free all the content. With talloc, it is as simple as calling
``talloc_free(domain)``.

.. mermaid::

    graph TD
        domain(domain)
        sysdb(sysdb)
        name(name)
        provider(provider)
        ldb(ldb)
        file(file)
        modules(modules)
        modules_child(...)
        rules(rules)
        rules_child(...)
        names(names)
        pattern(pattern)
        fmt(fmt)
        re(re)
        data(data)
        data_child(...)
        string(string)

        classDef struct fill:green,stroke:green,stroke-width:1px,fill-opacity:0.2
        linkStyle default interpolate basis
        class domain,sysdb,ldb,modules,rules,names,re,data struct

        domain --> name
        domain --> provider
        domain --> sysdb
        domain --> names
        sysdb --> ldb
        sysdb --> file
        ldb --> modules --> modules_child
        ldb --> rules --> rules_child
        names --> pattern
        names --> fmt
        names --> re
        re --> data --> data_child
        re --> string

.. code-tabs::

    .. code-tab:: c
        :label: talloc

        talloc_free(domain);

    .. code-tab:: c
        :label: malloc

        /* ... */

        void free_sysdb(struct struct sysdb_ctx *sysdb)
        {
            free(sysdb->file);
            free_ldb(sysdb->ldb);
            free(sysdb);
        }

        void free_domain(struct sss_domain_info *domain)
        {
            free(domain->name);
            free(domain->provider);
            free_sysdb(domain->sysdb);
            free_names(domain->names)
            free(domain);
        }

        free_domain(domain);

.. _confdb.h: https://github.com/SSSD/sssd/blob/master/src/confdb/confdb.h#L353

.. note::

    Every pointer created by talloc is a memory context on its own.

Changing the hierarchy
======================

Ideally, what you want to create is a nice oriented graph where nodes are
structures and leaves are non-structure elements (e.g. strings). The path must
follow the natural ordering that comes from the structure definition -- that is
structures are the parent memory contexts and their fields are their children as
you can see from previous examples.

Sometimes (e.g. when your function produces an output values) you want to change
the parent context. You can use ``talloc_steal`` or ``talloc_move`` for this
operation.

.. code-block:: c

    struct record {
        char *name;
        char *value;
    };

    char *value = talloc_strdup(NULL, "Hello world!");
    struct record *r;

    r = talloc_zero(NULL, struct record);
    r->name = talloc_strdup(r, "Hello");
    r->value = talloc_steal(r, value)

Destructors
***********

It is possible to assign a destructor on a memory context. The destructor is a
function that takes the context as an argument and is executed when the context
is freed before any of its children are freed. This can be used to perform
additional clean up when simple memory free is not sufficient.

.. code-block:: c

    int record_destructor(struct record *r)
    {
        printf("Removing %s\n", r->name);

        return 0;
    }


    r = talloc_zero(NULL, struct record);
    r->name = talloc_strdup(r, "Hello");
    r->value = talloc_strdup(r, "World");

    talloc_set_destructor(r, record_destructor);

.. seealso::

    Checkout the example from the official `Tutorial
    <https://talloc.samba.org/talloc/doc/html/libtalloc__destructors.html>`_.

Identifying memory leaks
************************

Talloc has the ability to produce dump of the complete tree from the first top
level context down to the leaves. This information is very useful for debugging
a memory leak since it can help you identify the talloc context that was not
freed properly. Use the following snippet to produce the talloc report from a
running process:

.. code-tabs::

    .. plain-tab::
        :label: sssd-2.9.3+

        .. code-block::

            PROCESS=$(pidof sssd_nss)
            FILE=/tmp/talloc.$PROCESS
            sudo gdb -quiet -batch -p $PROCESS \
                -ex "set \$file = (FILE*)fopen(\"$FILE\", \"w+\")" \
                -ex 'call (void) talloc_report_full(0, $file)' \
                -ex 'detach' \
                -ex 'quit' &> /dev/null

        Since sssd-2.9.3 ``talloc_enable_null_tracking()`` is called when
        starting long running processes. As a result all allocations are
        reported by ``talloc_report_full()`` when used on
        NULL(``0``).

    .. plain-tab::
        :label: sssd-2.6 - sssd-2.9.2

        .. code-block::

            PROCESS=$(pidof sssd_nss)
            FILE=/tmp/talloc.$PROCESS
            sudo gdb -quiet -batch -p $PROCESS \
                -ex "set \$file = (FILE*)fopen(\"$FILE\", \"w+\")" \
                -ex 'call (void) talloc_report_full(autofree_ctx, $file)' \
                -ex 'detach' \
                -ex 'quit' &> /dev/null

        Since ssssd-2.6 the dedicated local context ``autofree_ctx`` is used
        instead of the deprecated ``talloc_autofree_context()``.

    .. plain-tab::
        :label: sssd-2.5 and older

        .. code-block::

            PROCESS=$(pidof sssd_nss)
            FILE=/tmp/talloc.$PROCESS
            sudo gdb -quiet -batch -p $PROCESS \
                -ex "set \$file = (FILE*)fopen(\"$FILE\", \"w+\")" \
                -ex 'call (void) talloc_enable_null_tracking()' \
                -ex 'call (void) talloc_report_full(0, $file)' \
                -ex 'detach' \
                -ex 'quit' &> /dev/null

        SSSD versions older than SSSD-2.6.0 use the deprecated
        ``talloc_autofree_context()`` main context instead of the dedicated
        local context ``autofree_ctx``.

To allow ``gdb`` to handle the ``FILE`` type correctly and the ``autofree_ctx``
symbol debug information should be installed at least for ``glibc`` and SSSD.
You can call

.. code-tabs::

    .. fedora-tab::

        dnf debuginfo-install glibc sssd-common

    .. ubuntu-tab::

        apt install sssd-common-dbgsym libc6-dbg

to install the needed packages.

The report shows the current memory hierarchy that is in the process. When
investigating a memory leak, you want to check for all blocks that are attached
to the top level ``autofree_context`` (or ``null_context``) and for all contexts
that appear more times than what is expected. The following snippet shows an
example output so you can get the idea how the report looks like.

.. code-block:: text

    full talloc report on 'autofree_context' (total  27436 bytes in 362 blocks)
        struct tevent_context          contains  27436 bytes in 360 blocks (ref 0) 0x14f65a0
            struct tevent_fd               contains    112 bytes in   1 blocks (ref 0) 0x15079c0
            struct tevent_timer            contains    104 bytes in   1 blocks (ref 0) 0x15076b0
            struct tevent_fd               contains    112 bytes in   1 blocks (ref 0) 0x1508e20
            struct tevent_signal           contains    112 bytes in   3 blocks (ref 0) 0x14f7830
                reference to: struct tevent_sig_state
                struct tevent_common_signal_list contains     24 bytes in   1 blocks (ref 0) 0x14f78f0
            struct tevent_signal           contains    112 bytes in   3 blocks (ref 0) 0x14f7560
                reference to: struct tevent_sig_state
                struct tevent_common_signal_list contains     24 bytes in   1 blocks (ref 0) 0x14f7620
            struct tevent_fd               contains    112 bytes in   1 blocks (ref 0) 0x14f6940
            struct main_context            contains  26404 bytes in 346 blocks (ref 0) 0x14f68c0
                struct resp_ctx                contains  19908 bytes in 234 blocks (ref 0) 0x1507ff0
                    struct cli_ctx                 contains    512 bytes in   6 blocks (ref 0) 0x1526170
                        struct tevent_timer            contains    104 bytes in   1 blocks (ref 0) 0x151bc90
                        struct tevent_fd               contains    112 bytes in   1 blocks (ref 0) 0x1529f60
                        struct nss_state_ctx           contains     56 bytes in   1 blocks (ref 0) 0x1509310
                        struct cli_protocol            contains     16 bytes in   1 blocks (ref 0) 0x1526af0
                        struct cli_creds               contains     24 bytes in   1 blocks (ref 0) 0x1529ee0

See that it keeps the memory hierarchy with indentation so you can tell what is
the parent context and how much memory does it take. The first line, the
``autofree_context`` (or ``null_context``), is the top level memory context.

Please note that for SSSD versions older than 2.9.3, memory allocated with
``NULL`` given as parent (e.g. ``talloc_new(NULL)``), will not be shown in the
hierarchy by default. For the SSSD versions newer than SSSD-2.6.0 the hierarchy
below SSSD's internal ``autofree_context`` is printed while for older versions
the hierarchy below the deprecated libtalloc internal ``autofree_context``.

To be able to collect information about memory allocated on the parent ``NULL``
``talloc_enable_null_tracking()`` must be called. But only allocations done
after the call will be recorded. Since the script for older version of SSSD is
already calling ``talloc_enable_null_tracking()`` (here to enable the output of
libtalloc's internal ``autofree_context``), calling it a second time would
show allocations with the ``NULL`` parent as well if there were any between
the two runs of the script. In general, if the ``NULL`` parent should be
reported as well, it would be better to call e.g.

.. code-block:: bash

    sudo gdb -quiet -batch -p $(pidof sssd_nss) \
        -ex 'call (void) talloc_enable_null_tracking()' \
        -ex 'detach' \
        -ex 'quit' &> /dev/null

shortly after the start of SSSD, then wait a bit or run some operations which
should trigger allocations on the ``NULL`` parent you are interested in and
then call the report script.

Since sssd-2.9.3 ``talloc_enable_null_tracking()`` is called during the
initialization of long running processes and the allocations on the ``NULL``
context are always reported as well.

Temporary memory context
************************

Talloc can help you simplify memory clean up on both failures and success. When
following the right patterns, it can also help you to detect memory leaks (see
`Identifying memory leaks`_ for details).

A temporary memory context has a lifetime of the function execution. It is
created when entering the function and destroyed when the function returns. It
has to be attached to the top level ``NULL`` context so it is easily visible in
the talloc report if it is not freed properly. Any data that the function
allocates is attached to this temporary context so it can be freed with one call
to ``talloc_free``.

.. note::

    It is very important to use ``NULL`` as the parent for temporary context.
    This makes it visible if you forget to free it. If you use any other parent,
    the temporary context will be freed when the parent is freed and it will
    hide the fact that you forget to free the temporary context explicitly. This
    does not create issues at first glance but the reality is that it creates a
    memory leak for the lifetime of the parent context which may or may not be
    significant.

Using a temporary context is the main pattern that will help you properly clean
up and avoid memory leaks. If the function also produces any output data, this
data is stolen to the desired memory context at the very end. We use ``mem_ctx``
and ``tmp_ctx`` names for the target and temporary contexts.

.. code-block:: c

    struct record *record_init(TALLOC_CTX *mem_ctx,
                               const char *name,
                               const char *value);

    errno_t fetch_records(TALLOC_CTX *mem_ctx,
                          struct record **_r1,
                          struct record **_r2)
    {
        TALLOC_CTX *tmp_ctx;
        struct record *r1;
        struct record *r2;
        errno_t ret;

        /* Create a temporary talloc memory context on the top level context. */
        tmp_ctx = talloc_new(NULL);
        if (tmp_ctx == NULL) {
            return ENOMEM;
        }

        /* Allocate working data on the temporary context. */
        r1 = record_init(tmp_ctx, "name", "John Doe");
        if (r1 == NULL) {
            ret = ENOMEM;
            goto done;
        }

        /* Allocate working data on the temporary context. */
        r2 = record_init(tmp_ctx, "name", "Helen Doe");
        if (r2 == NULL) {
            ret = ENOMEM;
            goto done;
        }

        /* Change parent context to mem_ctx. */
        *_r1 = talloc_steal(mem_ctx, r1);
        *_r2 = talloc_steal(mem_ctx, r2);

        ret = EOK;

    done:
        /* Free all temporary data. */
        talloc_free(tmp_ctx);

        return ret;
    }

It is not always necessary to use a standalone temporary context if the function
does not require any temporary data and we can free everything with one call to
``talloc_free`` in case of failure. This is often the case for constructors.

.. code-block:: c

    struct record *record_init(TALLOC_CTX *mem_ctx,
                               const char *name,
                               const char *value)
    {
        struct record *r;
        errno_t ret;

        r = talloc_zero(NULL, struct record);
        if (r == NULL) {
            return NULL;
        }

        r->name = talloc_strdup(r, name);
        if (r->name == NULL) {
            goto fail;
        }

        r->value = talloc_strdup(r, value);
        if (r->value == NULL) {
            goto fail;
        }

        talloc_steal(mem_ctx, r);

        return r;

    fail:
        talloc_free(r);
        return NULL;
    }
