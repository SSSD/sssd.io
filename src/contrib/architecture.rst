SSSD Architecture
#################

Simply put, the main SSSD purpose is to store data from the remote database in a
local cache and then serve this data to the target user (application). Keeping
the cache up to date and valid is a difficult task and to do that SSSD consists
of multiple components (processes and libraries) that talk to each other through
various inter-process communication techniques. The following diagram gives you
a basic understanding about the components and their relations. The components
are described in more detail below the diagram.

.. image:: /contrib/architecture.svg
    :height: 700px
    :align: center

Backends
    The goal of the backend is to keep the cache up to date. To do so, it talks
    to the remote server, requests required data and then stores the data in the
    cache. There are multiple mechanisms that keeps the cache valid and
    consistent, some of them are triggered by a user request (e.g. user
    authentication) and some of them happens automatically on the background.

    Each backend represents one SSSD domain that is configured in the
    ``[domain/$name]`` section of the SSSD configuration and it is started as
    its own instance of ``sssd_be`` process. It consist of modules called the
    *data providers* that implements specific functionality such as:

    * id provider: identity of users, groups, services, ...
    * auth provider: user authentication
    * access provider: grants or denies user access to the machine
    * sudo provider: provides sudo rules from remote server
    * and many more

Responders
    A responder serves as a middle man between the target application and the
    local cache. When the application requests data (e.g. search user by id),
    the responder looks into the cache. If the requested data is valid it just
    returns it. If the data is missing or expired, it asks the backend to query
    the server first and then the responder returns the result.

    There are many responders that serve many different purpose, such as the
    NSS responder that provides data to the `Name Service Switch`_ (nsswitch, nss)
    service (do not confuse it with `Network Security Services`_) or the PAM
    responder that implements authentication via `Pluggable Authentication
    Modules`_ (PAM).

    Each responder lives in its own process such as:

    * ``sssd_nss``: The NSS responder
    * ``sssd_pam``: The PAM responder
    * ``sssd_sudo``: The sudo responder
    * ... and so on

Client libraries
    These libraries are part of the SSSD project. They implement an interface
    that is used by the target applications. Their mission is to arrange a
    communication between the application and a responder in order to retrieve
    desired data. Example of such libraries are ``nss_sss.so``, ``pam_sss.so``
    and ``sss_sudo.so``

Clients
    Clients are not part of SSSD, they are the applications used by users. These
    applications talk to SSSD using the interface implemented in the client
    libraries. We can state ``id``, ``getent``, ``su`` and ``sudo`` as
    examples of such applications or ``glibc`` and its nsswitch or PAM libraries
    that talks with SSSD on behalf of the application.

Monitor
    The monitor is the main SSSD process ``sssd``. It's purpose is to start and
    stop requested backends and responders and as the name suggest, it also
    monitors their state and restarts them if they suddenly stops.

Tools
    These are utility tools that can be used to monitor SSSD's status and
    manipulate the cache from command line.

.. _Name Service Switch: https://www.gnu.org/software/libc/manual/html_node/Name-Service-Switch.html
.. _Network Security Services: https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS
.. _Pluggable Authentication Modules: http://www.linux-pam.org

.. note::

    Backend is the only component the writes to the local cache.

Cache levels
************

Local cache (cache)
    Local cache is the main and *persistent* storage. It is stored on the disk
    using the `ldb database`_ (an LDAP-like embedded database) and it contains
    all data that is currently cached and known to SSSD.

    Every object stored in the cache has its own *expiration time*. The object
    is considered valid within this time and invalid or expired when the
    expiration time was reached. If the object is valid, it is returned
    immediately when requested. If the object is expired then SSSD tries to
    refresh it before returning the data. Staled data may be returned if the
    backend is not reachable in the moment of the refresh process.

Negative cache (ncache)
    A negative cache is a *non-persistent* cache for negative lookups stored
    inside each SSSD responder. It contains information about objects that are
    known to not exist (user does not exist) to prevent multiple subsequent
    queries to the remote database.

In-memory cache (memcache)
    This is a small *volatile* memory mapped cache of selected objects (user,
    groups and initgroups). The NSS responder stores objects in this cache after
    a successful lookup. This cache is then searched by the ``nss_sss.so``
    library to avoid contacting the NSS responder in the case when the object
    was already resolved moments ago.

.. _ldb database: https://ldb.samba.org

Cache lookup
************

SSSD is capable of caching many object types such as users and groups but also
autofs maps, sudo rules, SSH keys and many more. A cache lookup is performed
when data is requested. The lookup is performed through a unified cache
interface therefore all lookups share the basic algorithm regardless of the
object type. The following diagram can give you a basic understanding of how the
lookup is performed.

.. image:: /contrib/architecture-lookup.svg
    :height: 700px
    :align: center

.. note::

    In reality, the lookup is more difficult than what is shown on the diagram
    and more operations and checks are performed. Some of them implements
    shortcuts (e.g. we already know what domain is the user from) and some
    implements subtle differences that are specific to the requested object
    type. But the diagram is sufficient to get the idea as it catches all the
    fundamental steps.

User lookup example
*******************

The following diagram show the example of looking up a user named *Alice*. This
happens every time you log in to your computer, list directories, use ``id``,
``getent``, ``su`` or ``sudo`` commands and so on.

This diagram starts with a call to ``getpwnam`` POSIX function which
responsibility is to resolve the user name (Alice) to a user object which holds
the user id, group id, gecos an similar data. This function is internally called
from the processes and commands mentioned above.

.. mermaid::
    :style: margin-left: 0; margin-right: 0;

    sequenceDiagram
    participant getpwnam
    participant nss_sss.so
    participant memcache
    participant sssd_nss
    participant cache
    participant sssd_be
    participant LDAP

    getpwnam->>nss_sss.so: Search Alice!
    nss_sss.so->>memcache: Is Alice here?
    memcache->>nss_sss.so: No.
    nss_sss.so->>sssd_nss: Search Alice
    sssd_nss->>cache: Is Alice here?
    cache->>sssd_nss: No.
    sssd_nss->>sssd_be: Search Alice!
    sssd_be->>LDAP: Get me Alice!
    LDAP->>sssd_be: Here: [Alice].
    sssd_be->>cache: Store [Alice]!
    sssd_be->>sssd_nss: Done.
    sssd_nss->>cache: Is Alice here?
    cache->>sssd_nss: Yes: [Alice].
    sssd_nss->>memcache: Store [Alice]!
    sssd_nss->>nss_sss.so: Here: [Alice].
    nss_sss.so->>getpwnam: Here: [Alice].
