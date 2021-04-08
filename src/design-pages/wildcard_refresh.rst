Wildcard refresh through InfoPipe
=================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2553 <https://pagure.io/SSSD/sssd/issue/2553>`__

Problem statement
~~~~~~~~~~~~~~~~~

The InfoPipe responder adds a listing capability to the frontend code,
allowing the user to list users matching a very simple filter. To
implement the back end part of this feature properly, we need to add the
possibility to retrieve multiple, but not all entries with a single DP
request.

For details of the InfoPipe API, please see the `DBus responder design
page <https://docs.pagure.org/SSSD.sssd/design_pages/dbus_users_and_groups.html>`__.

Use cases
~~~~~~~~~

A web application, using the InfoPipe interface requests all users
starting with the letter 'a' so the users can be displayed in the
application UI on a single page. The SSSD must fetch and return all
matching user entries, but without requiring enumeration, which would
pull down too many users.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

Currently, the input that Data Provider receives can only be a single
user or group name. Wildcards are not supported at all, the back end
actively sanitizes the input to escape any characters that have a
special meaning in LDAP. Therefore, we need to add functionality to the
Data Provider to mark the request as a wildcard.

Only requests by name will support wildcards, not i.e. requests by SID,
mostly because there would be no consumer of this functionality.
Technically we could allow wildcard searches on any attribute with the
same code, though. Also, only requests for users and groups will support
wildcards.

When the wildcard request is received by the back end, sanitization will
be done, but modified in order to avoid escaping the wildcard. After the
request finishes, a search-and-delete operation must be run in order to
remove entries that matched the wildcard search previously but were
removed from the server.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

The wildcard request will only be used by the InfoPipe responder, but
will be implemented in the common responder code, in particular the new
``cache_req`` request.

The following sub-sections document the changes explained earlier in
more detail.

Responder lookup changes
^^^^^^^^^^^^^^^^^^^^^^^^

The responder code changes will be done only in the new cache lookup
code (``src/responder/common/responder_cache_req.c``). Since the NSS
responder wouldn't initially expose the functionality of wildcard
lookups, we don't need to update the lookup code currently in use by the
NSS responder.

The ``cache_req_input_create()`` function should be extended to denote
that the ``name`` input contains a wildcard to make sure the caller
really intends to left the asterisk unsanitized. Internally, the
``cache_req_type`` would add a new value as well.

We might add a new user function and a group function that would grab
all entries by sysdb filter, which can be more or less a wrapper around
``sysdb_search_entry``, just setting the right search bases and default
attributes. This new function must be able to handle views.

These responder changes should be developed as a first phase of the work
as they can be initially tested with enumeration enabled on the back end
side.

Responder <-> Data Provider communication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The request between the responders and the Data Provider is driven by a
string filter, formatted as follows: ::

        type:value:extra

Where ``type`` can be one of ``name``, ``idnumer`` or ``secid``. The
``value`` field is the username, ID number or SID value and extra
currently denotes either lookup with views or lookup by UPN instead of
name.

To support the wildcard lookups, we have two options here - add a new
``type`` option (perhaps ``wildcard_name``) or add another
``extra_value``.

Adding a new ``type`` would be easier since it's just addition of new
code, not changing existing code. On the backend side, the ``type``
would be typically handled together with ``name`` lookups, just sanitize
the input differently. The downside is that if we wanted to ever allow
wildcard lookups for anything else, we'd have to add yet another type.
Code-wise, adding a new type would translate to adding new values for
the ``sss_dp_acct_type`` enum which would then print the new type value
when formatting the sbus message.

The other option would be to allow multivalued ``extra`` field: ::

        type:value:extra1:extra2:...:extraN

However, that would involve changing how we currently handle the
``extra`` field, which is higher risk of regressions. Also, the back
ends can technically be developed by a third party, so we should be
extremely careful about changing the protocol between DP and providers.
Since we don't expect to allow any other wildcard requests than by name
yet, I'm proposing to go with the first option and add a comment to the
code to change to using the extra field if we need wildcard lookups by
another attribute.

Relax the ``sss_filter_sanitize`` function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a wildcard request is received, we still need to sanitize the input
and escape special LDAP characters, but we must not escape the asterisk
(``*``).

As a part of the patchset we need to add a parameter that will denote
characters that should be skipped during sanitization.

Delete cached entries removed from the server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After a request finishes, the back end needs to remove entries that are
cached from a previous lookup using the same filter, but no longer
present on the server.

Because wildcard requests can match multiple entries, we need to save
the time of the backend request start and delete all entries that match
a sysdb filter analogous to the LDAP filter, but were last updated prior
to the start of the request.

Care must be taken about case sensitivity. Since the LDAP servers are
typically case-insensitive, but sysdb (and POSIX systems) are
case-sensitive, we will default to matching only case-sensitive ``name``
attribute by default as well. With case-insensitive back ends, the
search function must match also the ``nameAlias`` attribute.

LDAP provider changes
^^^^^^^^^^^^^^^^^^^^^

The LDAP provider is the lowest common denominator of other providers
and hence it would contain the low-level changes related to this
feature.

In the LDAP provider, we need to use the relaxed version of the input
sanitizing and the wildcard method to delete matched entries. These
changes will be contained to the ``users_get_send()`` and
``groups_get_send()`` requests.

The requests that fetch and store the users or groups from LDAP
currently have a parameter called ``enumerate`` that is used to check
whether it's OK to receive multiple results or not. We should rename the
parameter or even invert it along with renaming (i.e change the name to
``direct_lookup`` or similar).

We also need to limit the number of entries returned from the server,
otherwise the wildcard request might easily turn into a full
enumeration. To this end, we will add a new configuration option
``wildcard_search_limit``. Internally, we would change the boolean
parameter of ``sdap_get_users_send`` to a tri-state that would control
whether we expect only a single entry (i.e. don't use the paging control),
multiple entries with a search limit (wildcard request) or multiple
entries with no limit (enumeration). We need to make sure during
implementation that it is discoverable via DEBUG messages that the upper
limit was reached.

IPA provider changes
^^^^^^^^^^^^^^^^^^^^

The tricky part about IPA provider are the views. The lookups with views
have two branches - either an override object matches the input and then
we look up the corresponding original object or the other way around.
The code must be changed to support multiple matches for both overrides
and original objects in the first pass. We might end up fetching more
entries than needed because the resulting object wouldn't match in the
responder after applying the override, but the merging on the responder
side will only filter out the appropriate entries.

Currently, the request handles all account lookups in a single tevent
request, with branches for special cases, such as initgroup lookups or
resolving ghost members during group lookups. We might need to refactor
the single request a bit into per-object tevent lookups to keep the code
readable.

Please keep in mind that each tevent request has a bit of performance
overhead, so adding new request is always a trade-off. Care must be
taken to not regression performance of the default case unless
necessary.

If the first override lookup matches, then we must loop over all
returned overrides and find matching originals. The current code re-uses
the state->ar structure, which is single-valued, we need to add another
multi-valued structure instead (``state->override_ar``) and perhaps even
split the lookup of original objects into a separate request, depending
on the complexity.

Conversely, when the original objects match first, we need to loop over
the original matches and fetch overrides for each of the objects found.
Here, the ``get_object_from_cache()`` function needs to be able to
return multiple results and the following code must be turned into a
loop.

When looking up the overrides, the ``be_acct_req_to_override_filter()``
must be enhanced to be able to construct a wildcard filter. The
``ipa_get_ad_override_done`` must also return all matched objects if
needed, not just the first array entry. The rest of the
``ipa_get_ad_override_send()`` request is generic enough already.

IPA subdomain lookups via the extdom plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently the extdom plugin only supports direct entry lookups, even on
the server side. We could add a new request that accepts a filter with
asterisk and returns a list of matching DNs or names, but because of the
complexity of the changes, this part of implementation should be
deferred until requested specifically.

If the IPA subdomain would receive a wildcard request, it would reply
with an error code that would make it clear this request is not
supported.

Making sure the IPA provider in server mode is capable of returning
wildcard entries and adding a wildcard-enabled function for the
``libnss_sss_idmap`` library would be a prerequisite so that the extop
plugin can request multiple entries from the SSSD running in the server
mode.

AD provider changes
^^^^^^^^^^^^^^^^^^^

No changes seem to be required for the AD provider, since the AD
provider mostly just passes around the original ``ar`` request to a
Global Catalog lookup or an LDAP lookup. However, testing must be
performed in an environment where some users have POSIX attributes but
those attributes are not replicated to the Global Catalog to make sure
we handle the fallback between connections well.

Other providers
^^^^^^^^^^^^^^^

Proxy provider support is not realistic, since the proxy provider only
uses the NSS functions of the wrapped module which means it would rely
on enumeration anyway. With enumeration enabled, the responders would be
able to return the required matching entries already. The local provider
is not a real back end, so it should get the wildcard support for free,
just with the changes to the responder.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

A new option ``wildcard_search_limit`` will be added. The default value
would be 1000, which is also typically the size of one page.

How To Test
~~~~~~~~~~~

When the InfoPipe API is ready, then testing will be done using the
methods such as ListByName. Until then, the feature is not exposed or
used anyway, so developers can test using a special command-line tool
that would send the DP request directly. This tool wouldn't be committed
to the git tree.

Authors
~~~~~~~

-  Jakub Hrozek <`jhrozek@redhat.com <mailto:jhrozek@redhat.com>`__>
