.. contents:: Table of Contents
    :local:

Troubleshooting SUDO
####################

Is SSSD and sudo cooperation configured correctly?
**************************************************

To check whether the basic configuration of sudo and SSSD is correct,
see ``/etc/nsswitch.conf`` and ``/etc/sssd/sssd.conf`` files.

- ``/etc/nsswitch.conf`` must say that ``sss`` module is used for sudo
  service. Look for line like ``"sudoers: sss"`` (only SSSD is used),
  ``"sudoers: files sss"`` (local rules first, then SSSD) or similar.
- ``/etc/sssd/sssd.conf`` must say that ``sudo responder is enabled``.
  Look at ``[sssd]`` section and search for line ``services: nss, pam,
  sudo`` or similar.
- In ``/etc/sssd/sssd.conf`` check that ``sudo provider is enabled``.
  Look at ``[domain]`` section, sudo provider is always enabled for ldap,
  ad and ipa providers, unless this section contains
  ``sudo_provider = none``.

Obtaining logs
**************

Logs can provide useful information to find a solution when troubleshooting an
issue with sudo.

How do I get sudo logs?
=======================

#. Open ``/etc/sudo.conf`` and add the following lines:

   .. code-block:: text

      Debug sudo /var/log/sudo_debug all@debug
      Debug sudoers.so /var/log/sudo_debug all@debug

#. Run ``sudo``
#. File ``/var/log/sudo_debug`` contains sudo logs

How do I get SSSD logs?
=======================

#. Open ``/etc/sssd/sssd.conf`` and enable logging by setting a debug
   level in ``[sudo]`` and ``[domain/$NAME]`` section: ``debug_level = 0x3ff0``

   .. code-block:: ini

       [sudo]
       debug_level = 0x3ff0

       [domain/$NAME]
       debug_level = 0x3ff0

#. Restart SSSD
#. Run sudo
#. Log files are stored in ``/var/log/sssd/sssd_$NAME.log`` (domain log)
   and ``/var/log/sssd/sssd_sudo.log`` (sudo responder log)

What to look for in the logs
****************************

SSSD sudo responder -- sssd_sudo.log
====================================

- Was a rule returned to sudo at all?

  .. code-block:: sssd-log

      [sssd[sudo]] [sudosrv_get_sudorules_from_cache] (0x0400): Returning $num-rules rules for [user-1@LDAP.PB]

- What filter was used to fetch rules from cache?

  .. code-block:: sssd-log

      [sudosrv_get_sudorules_query_cache] (0x0200): Searching sysdb with [(&(objectClass=sudoRule)(|(sudoUser=ALL)(sudoUser=user-1)(sudoUser=#10001)(sudoUser=%group-1)(sudoUser=%user-1)(sudoUser=+*)))]

- You can then use this filter to search in the SSSD cache to see what
  rules were returned

  .. code-tabs::

      .. fedora-tab::

          $ dnf install ldb-tools
          $ ldbsearch -H /var/lib/sss/db/cache_$domain.ldb -b cn=sysdb '$filter'

      .. rhel-tab::

          $ yum install ldb-tools
          $ ldbsearch -H /var/lib/sss/db/cache_$domain.ldb -b cn=sysdb '$filter'

- SSSD cache uses a LDAP-like format equivalent to the sudo format described in
  `man sudoers.ldap <https://www.sudo.ws/man/1.8.15/sudoers.ldap.man.html>`__

SSSD domain -- sssd_$domain.log
===============================

-  How many rules were found?

   .. code-block:: sssd-log

       [sdap_sudo_refresh_load_done] (0x0400): Received $num-rules rules

-  What sudo rules were downloaded from server?

   .. code-block:: sssd-log

       [sssd[be[LDAP.PB]]] [sysdb_save_sudorule] (0x0400): Adding sudo rule $rule-name

-  Were all matching rules stored?

   .. code-block:: sssd-log

       [sdap_sudo_refresh_load_done] (0x0400): Sudoers is successfully stored in cache

-  What filter was used to fetch rules from server?

   .. code-block:: sssd-log

       [sdap_get_generic_ext_step] (0x0400): calling ldap_search_ext with [(&(objectClass=sudoRole)(|(!(sudoHost=*))(sudoHost=ALL)(sudoHost=client.sssd.pb)(sudoHost=client)(sudoHost=10.34.78.77)(sudoHost=10.34.78.0/24)(sudoHost=2620:52:0:224e:21a:4aff:fe23:1394)(sudoHost=2620:52:0:224e::/64)(sudoHost=fe80::21a:4aff:fe23:1394)(sudoHost=fe80::/64)(sudoHost=+*)(|(sudoHost=*\\*)(sudoHost=*?*)(sudoHost=*\2A*)(sudoHost=*[*]*))))][dc=ldap,dc=pb]

-  You can then use ldapsearch with this exact filter to see what rules
   were downloaded

   .. code-tabs::

       .. code-tab::
           :label: Anonymous bind

           $ ldapsearch -x -H ldap://ldap.example.com -b dc=ldap,dc=example,dc=com '$filter'

       .. code-tab::
           :label: Simple bind

           $ ldapsearch -x -D "cn=Directory Manager" -w "$password" -H ldap://ldap.example.com -b dc=ldap,dc=example,dc=com '$filter'

       .. code-tab::
           :label: GSSAPI

           $ ldapsearch -Y GSSAPI -H ldap://ldap.example.com -b dc=ldap,dc=example,dc=com '$filter'

sudo debug logs -- sudo_debug
=============================

-  Information about the user that is attempting to run sudo

   .. code-block:: text

       Mar 31 16:11:15 sudo[22259] settings: debug_flags=all@debug
       Mar 31 16:11:15 sudo[22259] settings: run_shell=true
       Mar 31 16:11:15 sudo[22259] settings: progname=sudo
       Mar 31 16:11:15 sudo[22259] settings: network_addrs=10.71.4.192/255.255.255.0 fe80::250:56ff:feb9:7d6/ffff:ffff:ffff:ffff::
       Mar 31 16:11:15 sudo[22259] user_info: user=$username
       Mar 31 16:11:15 sudo[22259] user_info: pid=22259
       Mar 31 16:11:15 sudo[22259] user_info: ppid=22172
       Mar 31 16:11:15 sudo[22259] user_info: pgid=22259
       Mar 31 16:11:15 sudo[22259] user_info: tcpgid=22259
       Mar 31 16:11:15 sudo[22259] user_info: sid=22172
       Mar 31 16:11:15 sudo[22259] user_info: uid=$uid
       Mar 31 16:11:15 sudo[22259] user_info: euid=0
       Mar 31 16:11:15 sudo[22259] user_info: gid=554801393
       Mar 31 16:11:15 sudo[22259] user_info: egid=554801393
       Mar 31 16:11:15 sudo[22259] user_info: groups=498,6004,6005,7001,106501,554800513,554801107,554801108,554801393,554801503,554802131,554802244,554807670
       Mar 31 16:11:15 sudo[22259] user_info: cwd=/
       Mar 31 16:11:15 sudo[22259] user_info: tty=/dev/pts/1
       Mar 31 16:11:15 sudo[22259] user_info: host=$hostname
       Mar 31 16:11:15 sudo[22259] user_info: lines=31
       Mar 31 16:11:15 sudo[22259] user_info: cols=237

-  What data sources are used to fetch sudo rules

   .. code-block:: text

       Mar 31 16:11:15 sudo[22259] <- sudo_parseln @ ./fileops.c:178 := sudoers: files sss

-  SSSD plugin starts here

   .. code-block:: text

       Mar 31 16:11:15 sudo[22259] <- sudo_sss_open @ ./sssd.c:305 := 0

-  Here is sudo looking for ``cn=defaults``

   .. code-block:: text

       Mar 31 16:11:15 sudo[22259] Looking for cn=defaults

-  SSSD is returning rules

   .. code-block:: text

       Mar 31 16:11:15 sudo[22259] Received 3 rule(s)

-  ...and sudo is evaluating them by matching sudoHost, sudoUser, ...
   attributes to current user (the hostname is matched in this example)

   .. code-block:: text

       Mar 31 16:11:15 sudo[22259] sssd/ldap sudoHost 'ALL' ... MATCH!

-  if something does not match, you will see line ending ``:= false;`` you
   need to guess the test from function name

   .. code-block:: text

       Mar 31 16:11:15 sudo[22259] <- user_in_group @ ./pwutil.c:1010 := false

Common questions
****************

Setting global options with cn=defaults when sudo rules are stored on an IPA server
===================================================================================

To imitate global options, create a rule named ``cn=defaults`` in LDAP tree
or rule named ``defaults`` in IPA and ``set`` sudoOption attribute as you wish.

!authenticate does not work
===========================

A common problem is when you set ``!authenticate`` option to a specific rule
but ``sudo -l`` command that lists all rules still requires
authentication. If you want ``sudo -l`` to be password-less you need to
set ``!authenticate`` also in ``cn=defaults``.

It takes too long to update rules
=================================

Look at ``man sssd-sudo`` to see how sudo rules are cached in SSSD.

Alternative to options in command definition in sudoers
===============================================================

In sudoers, you can define an allowed command together with many
options, such as:

.. code-block:: text

    %wheel  ALL=(ALL) ROLE=unconfined_r TYPE=unconfined_t ALL
    john    ALL=(ALL) NOPASSWD: ALL

These all have their equivalent as a sudo option that can be placed in
``sudoOption`` attribute. Usually it is only lower cased value of this
command option, with an exception of ``NOPASSWD`` which is referenced as
``authenticate``. See ``SUDOERS OPTIONS`` section of ``sudoers.5`` manual page
for more information.

Known issues
************

**Problems with IPA-AD trust when fully qualified names are required for
IPA**

**Fixed in 1.14.0**:
`https://pagure.io/SSSD/sssd/issue/2919 <https://pagure.io/SSSD/sssd/issue/2919>`__

In configurations that requires IPA users and groups to use fully
qualified names (i.e. ``username@IPA.DOMAIN`` and ``groupname@IPA.DOMAIN``) sudo
is not able to resolve the users or groups in sudo rules correctly.

Example configuration:

.. code-block:: ini

    [sssd]
    domains = IPA.DOMAIN
    default_domain_suffix = AD.DOMAIN

Or:

.. code-block:: ini

    [domain/IPA.DOMAIN]
    use_fully_qualified_names = True

**Sudo rule won't work since 1.13.4 if it contains non-POSIX group with
IPA provider**

**Won't fix, intentional**:
`https://pagure.io/SSSD/sssd/issue/3046 <https://pagure.io/SSSD/sssd/issue/3046>`__

We switched to IPA sudo rules schema stored at ``cn=sudo`` in SSSD 1.13.4.
The slapi-nis plugin that is used to generate the compat tree
``ou=sudoers`` unfold members of non-POSIX group and stores each as
``sudoUser: member`` value. This makes sudo rules work even with non-POSIX
group if the compat tree is used.

To re-enable this functionality, you can switch SSSD to fetch sudo rules
from the compat tree again by setting ``ldap_sudo_search_base`` to
``ou=sudoers,dc=example,dc=com``

The correct way to reference a non-POSIX group in sudo rule is to
include it by a POSIX one which is referenced by sudo as:

* ``sudorule ---> POSIX group <--- non-POSIX group``

Ask for help
************

Most of the sudo related user cases that we have in past years was
actually only a misconfiguration of sudo rule or the client system. If
you are not able to track down the issue yourself, feel free to ask one
of the developers on `SSSD mailing list`_ or `#sssd IRC channel`_ on
`libera.chat`_. To speed things up, please prepare the following information:

-  Description of the problem and what have you found out. You should at
   least know whether the issue lies on sudo (rules are send to sudo but
   it unexpectedly rejects access) or sssd (the rule is not even send to
   sudo) side with the use of previous debugging information.
-  sudo and SSSD logs
-  LDIF of rules that are expected to work but don't
-  Any additional information you deemed helpful -- e.g. group
   membership, output of the following commands:

.. _SSSD mailing list: https://lists.fedorahosted.org/archives/list/sssd-devel@lists.fedorahosted.org
.. _#sssd IRC channel: irc://irc.libera.chat/sssd
.. _libera.chat: https://libera.chat

.. code-block:: bash

    id $user
    getent group $group
    getent netgroup $netgroup

Supported versions
******************

Sudo integration is supported since version 1.8.6 of sudo itself and
version 1.9 of sssd.
