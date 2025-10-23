Introduction to SSSD's Identity Provider (IdP) support
######################################################

OAuth2.0/OIDC based Identity Providers (IdPs) such as Keycloak, EntraID, and
Okta are the preferred solutions for Identity Management of web-based
applications and services.

If an IdP infrastructure is already available and used for web applications
SSSD's IdP provider can be used to allow user-management and authentication on
the system level as well. Given the main use case of IdPs, to authenticate a
single user against a web service, the integration with often terminal-based
multi-user systems requires some compromises. E.g. the authentication requires
an interaction with the IdP with the help of a web-browser. In a terminal-based
environment this would require an additional device with a web-browser.

For authentication SSSD is using the `OAuth 2.0 Device Authorization Grant flow
<https://datatracker.ietf.org/doc/html/rfc8628>`_ . To look up users and
groups, independent of an authenticated user, SSSD will use the different REST
APIs provided by the IdPs and a dedicated IdP client to authenticate against
the REST endpoint. Since there is no standard for the REST APIs, SSSD has to
support them individually, currently Keycloak and EntraID are supported.

There is a `short video with a demo
<https://sbose.fedorapeople.org/sssd-idp-demo/sssd-idp-demo.mp4>`_ and an
extended demo with more details on `Youtube
<https://www.youtube.com/watch?v=kclXwGuCGGE>`_. There are also `slides and
recordings of a presentation of this feature at the FOSDEM conference
<https://archive.fosdem.org/2025/schedule/event/fosdem-2025-4756-sssd-and-idps/>`_.

Basic setup
***********
After installing the packages, especially the `sssd-idp` package, create a
`sssd.conf` file, for example:

.. code-block:: text

    [sssd]
    services = nss, pam
    domains = entra_id, keycloak

    [domain/entra_id]
    id_provider = idp
    idp_type = entra_id
    idp_client_id = 12345678-abcd-0101-efef-ba9876543210
    idp_client_secret = YOUR-CLIENT-SECRET
    idp_token_endpoint = https://login.microsoftonline.com/TENANT-ID/oauth2/v2.0/token
    idp_userinfo_endpoint = https://graph.microsoft.com/v1.0/me
    idp_device_auth_endpoint = https://login.microsoftonline.com/TENANT-ID/oauth2/v2.0/devicecode
    idp_id_scope = https%3A%2F%2Fgraph.microsoft.com%2F.default
    idp_auth_scope = openid profile email

    [domain/keycloak]
    idp_type = keycloak:https://master.keycloak.test:8443/auth/admin/realms/master/
    id_provider = idp
    idp_client_id = myclient
    idp_client_secret = YOUR-CLIENT-SECRET
    idp_token_endpoint = https://master.keycloak.test:8443/auth/realms/master/protocol/openid-connect/token
    idp_userinfo_endpoint = https://master.keycloak.test:8443/auth/realms/master/protocol/openid-connect/userinfo
    idp_device_auth_endpoint = https://master.keycloak.test:8443/auth/realms/master/protocol/openid-connect/auth/device
    idp_id_scope = profile
    idp_auth_scope = openid profile email


    [nss]
    default_shell = /bin/bash
    fallback_homedir = /home/%f

Please note that the IdP clients must have the permissions to read user and
group attributes. More details about the new configuration options can be found
in the ``sssd-idp(5)`` man page.

Since IdP providers typically do not provide home directories or default shell
reasonable defaults are added to the  sample configuration.
