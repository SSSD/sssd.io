Secrets Service
===============

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2913 <https://pagure.io/SSSD/sssd/issue/2913>`__

Problem statement
~~~~~~~~~~~~~~~~~

Many system and user applications need to store secrets such as
passwords or service keys and have no good way to properly deal with
them. The simple approach is to embed these secrets into configuration
files potentially ending up exposing sensitive key material to backups,
config management system and in general making it harder to secure data.

The `custodia <https://github.com/simo5/custodia>`__ project was born
to deal with this problem in cloud like environments, but we found the
idea compelling even at a single system level. As a security service
sssd is ideal to host this capability while offering the same
`API <https://github.com/simo5/custodia/blob/master/API.md>`__ via a
UNIX Socket. This will make it possible to use local calls and have them
transparently routed to a local or a remote key management store like
`IPA Vault <http://www.freeipa.org/page/V4/Password_Vault_1.0>`__ or
`HashiCorp's Vault <https://www.vaultproject.io>`__ for storage, escrow
and recovery.

Use cases
~~~~~~~~~

This feature can be used to keep secrets safe in an encrypted database
and yet make it easy for application to have access to the clear text
form, at the same time protecting access to the secrets by using
targeted system policies. Also when remote providers are implemented it
will become possible to synchronize application secrets across multiple
machines either for system applications like clusters or for user's
passwords by providing a simple network keyring that can be shared by
multiple clients.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

This feature will be implemented by creating a new responder process
that handles the REST API over a UNIX Socket, and will route requests
either to a local database separate from the generic ldb caches or to a
provider that can implement remote backends like IPA Vault to store some
or all the secrets of a user or a system application.

The new responder daemon will be called sssd-secrets and will be socket
activated in the default configuration on systemd based environments.

Additionally a client library will be provided with a very simple basic
API for simple application needs. The full Custodia API will be provided
over the socket and will be accessible via curl or a similar tool.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

TBD

Request flow: application -> libsss-secrets.so ---unix socket--->
sssd-secrets -> local store

Or alternatively, for an application that can speak REST itself:
application ---unix socket---> sssd-secrets -> local store

The latter would be probably used by applications written in higher
level languages such as Java or Python, the former would be better
suited for C/C++ applications without requiring additional dependencies.

unix socket in /var/run/secrets.socket local store in
/var/lib/sss/secrets/secrets.ldb encrypted using master secret
(potentially uses TPM where available ?)

Helper libraries
^^^^^^^^^^^^^^^^

The Custodia REST API uses JSON to encode requests and replies,
{provisionally} the `​Jansson <http://www.digip.org/jansson/>`__ library
will be used behind a talloc base wrapper and insulated to allow easy
replacement, and encoding/decoding into specific API objects.

The REST API uses HTTP 1.1 as transport so we'll need to parse HTTP
Requests in the server, {provisionally} the
`​http-parser <https://github.com/nodejs/http-parser>`__ library will be
used in a tevent wrapper to handle these requests. The library seem to
be particularly suitable for use in callback based systems like tevent,
and does not handle memory on it's own allowing use to use fully talloc
backed objects natively.

Client Library
^^^^^^^^^^^^^^

A simple client library is build to provide easy access to secrets from
C applications (or other languages via bindings) by concealing all the
communication into a simple API.

The API should be as follow: ::

        struct secrets_context;

        struct secrets_data {
            uint8_t *data;
            size_t *length;
        };

        struct secrets_list {
            struct secret_data *elements;
            int count;
        }

        int secrets_init(const char *appname,
                         struct secrets_context **ctx);
        int secrets_get(struct secrets_context *ctx, const char *name,
                        struct secrets_data *data);
        int secrets_put(struct secrets_context *ctx, const char *name,
                        struct secrets_data *data);
        int secrets_list(struct secrets_context *ctx, const char *path,
                         struct secrets_list *list);

        void secrets_context_free(struct secrets_context **ctx);
        void secrets_list_contents_free(struct secrets_list *list);
        void secrets_data_contents_free(struct secrets_data *data);

The API uses exclusively the "simple" secret type.

Resource Considerations
^^^^^^^^^^^^^^^^^^^^^^^

TBD user quotas

Security Considerations
^^^^^^^^^^^^^^^^^^^^^^^

Access Control SO\_PEERCRED and SELinux.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

A new type of configuration section called "secrets" will be introduced.
Like the "domain" sections, secrets session names include a secret name
in the section name.

A typical section name to override where an application like the Apache
web server will have its secrets stored looks like this: ::

     [secrets/system/httpd]
     provider = xyz

The global secrets configuration will be held in the `` [secrets] `` (no
path components) section. Providers may deliver overrides in
configuration snippets, use of additional, dynamic configuration
snippets will be the primary method to configure overrides and remote
backends.

How To Test
~~~~~~~~~~~

A test/example binary that implement the functions of the client library
will be provided, additional the curl binary should be used to test the
wider API, especially once we have a proxy backend to talk to a real
custodia server on the network.

Authors
~~~~~~~

Simo Sorce <`simo@redhat.com <mailto:simo@redhat.com>`__>
