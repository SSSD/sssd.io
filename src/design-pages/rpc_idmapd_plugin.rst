SSS NFS Client (rpc.idmapd plugin)
==================================

The client is named "**sss\_nfs**" (although "sss\_idmap" or "idmap"
might have been better names, the term "idmap" is already occupied in
the SSSD world).

rpc.idmapd - background
~~~~~~~~~~~~~~~~~~~~~~~

rpc.idmapd runs on NFSv4 servers as a userspace daemon (part of
nfs-utils). Its role is to assist knfsd by providing the following 6
mapping functions:

#. (user) name to UID
#. (group) name to GID
#. UID to (user) name
#. GID to (group) name
#. principal (user) name to ids (UID + GID)
#. principal (user) name to grouplist (groups which user are member of)

.. FIXME: The last two items had the following note below them
.. :sup:`(`(1) <https://fedorahosted.org/sssd#krbnote>`__)`
.. What's this about?

rpc.idmapd provides API for developing plugins (loaded by ``dlopen(3)``)
which implements the actual mapping process.

On the kernel level, there's a caching mechanism for the responses from
the userspace daemon.

\ :sup:`(1)` Items 5 + 6 are only relevant for kerberized NFSv4 servers.
At the first stage only there won't be kerberos support.

SSSD - Responder
~~~~~~~~~~~~~~~~

The functionality required from the Responder side is a subset of the
functionality provided by existing NSS Responder's commands.

As you can see below (on the client part of the design) - no changes are
needed in the NSS Responder.

SSSD - NFS Client
~~~~~~~~~~~~~~~~~

Responder-Facing Interactions (existing NSS Responder commands)

-  ``SSS_NSS_GETPWNAM`` - map (user) name to UID requests
-  ``SSS_NSS_GETGRNAM`` - map (group) name to GID requests
-  ``SSS_NSS_GETPWUID`` - map UID to (user) name requests
-  ``SSS_NSS_GETGRGID`` - map GID to (group) name requests

The request & reply sent to & from the responder is "standard" in terms
of the NSS Responder.

The client only needs a portion of the reply. Only this portion will be
extracted from the packet (i.e. UID/GID/user name/group name).

Optimisation Techniques
~~~~~~~~~~~~~~~~~~~~~~~

The optimisation techniques used for the NSS client will be used here as
well. i.e. Fast Cache (memcache) & negative-cache.

It will be possible for the user to disable Fast Cache from the
configuration file. (see below)

Configuration File
~~~~~~~~~~~~~~~~~~

The configuration of the client will be part of rpc.idmap config file
(``/etc/idmapd.conf``).
