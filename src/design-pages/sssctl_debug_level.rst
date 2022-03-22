Get and Set per-Component Debug-Level
#####################################

Related Tickets
***************

* https://github.com/SSSD/sssd/issues/6019

Problem statement
*****************
The debug level can currently be set using the sssctl tool, but it cannot be
retrieved except by grepping the log file.

In addition, each component can have its own debug level, but the tool sets
it for all of them and there is no way to limit it to a given component.

Solution overview
*****************
Extend the behavior of ``sssctl``’s ``debug-level`` command to:

1. Print the current debug level if no value is provided. Because each
   component can have a separate debug level, a list will be printed,
   not just a single, global value.

2. Allow the user to select which component(s) to target. That applies both
   to setting a new level and to getting the current level. If no particular
   component is targeted, the command is applied to all of them.

For compatibility’s sake, the old behavior remains unmodified.

::

  # sssctl debug-level 0x1000         # Same old behavior
  # sssctl debug-level                # Get all the current debug-levels
  sssd                      0x1000
  nss                       0x1000
  pac                       0x1000
  pam                       0x1000
  domain/ldap               0x1000
  domain/samba              0x1000
  domain/ipa                0x1000
  # sssctl debug-level --pam --nss 0x0270   # Set only sssd_pam and sssd_nss
  # sssctl debug-level --domain=ldap 0x0070 # Set only the ldap domain
  # sssctl debug-level --pam --domain=ldap  # Get only sssd_pam and the ldap domain
  pam                       0x0270
  domain/ldap               0x0070
  # sssctl debug-level --autofs --domain=wrong --nss # Wrong components
  nss                       0x0270
  autofs                    Unreachable service
  domain/wrong              Unknown domain

Implementation details
**********************
Only ``sssctl``'s public interface is affected by this solution.
No change to the configuration.

Currently, the new debug level the user requests is mandatory. It won’t be
any more. When not provided, the tool will display the current debug levels
for the targeted components.

``sssctl`` will accept new options to determine which component to target.
Those components could be the services (nss, pam, etc.) which have predefined
names, but also the different domains with names defined by the user.
For services, dedicated options will be created using their names:
``--nss`` , ``--autofs``, etc.; while for domains the ``--domain`` option
with the domain name as argument will be used: ``--domain=domain/mydomain``. The
``domain/`` string is optional, making ``--domain=mydomain`` also valid.
The tool will accept several of these options to target multiple components.

To achieve this, the function ``sssctl_debug_level()`` in ``sssctl_logs.c``
will be modified to handle the missing debug level (get) and the new options.
Then ``set_debug_level()`` will be replaced by ``sssctl_do_debug_level()``. It
will receive a flag (``ACTION_GET`` or ``ACTION_SET``) indicating the action to
take about the debug level, depending on whether a debug level was provided by
the user or not. This function will first establish a connection to ``D-Bus``
and then loop on the received target list getting or setting each debug level
by calling the ``do_debug_level()`` function. If no target is provided by the
user, ``confdb`` will be used to retrieve the whole list of components. On
``ACTION_GET``, the retrieved debug level will be printed to ``STDOUT``.

``sssctl_do_debug_level()`` will call ``do_debug_level()`` to set or get the a
component's debug level. Again, this function will receive the ``ACTION_GET``
or ``ACTION_SET`` flag, will compute the bus name for the given component and
get or set the component's debug level.

``D-Bus`` will be accessed using the ``sbus`` library. The read-write
``debug_level`` property will be added to the ``sssd.service`` interface.
Responders, backends and the ``monitor`` will have to implement this interface
(if not already done) and this property's getter and setter.

The function ``sss_tool_popt_ex()`` is used by ``sssctl_do_debug_level()`` to
retrieve the command line arguments, in particular the debug level. This
function considers today that the free option is required if the caller
requested it. A new parameter called ``fopt_require`` will be added for the
caller to tell whether the free option is optional or required, even if it was
requested. All the existing calls to this function will be updated to provide
this new parameter.

``sssctl`` will exit with code 1 on user errors. Those errors could be that the
user requested a domain that does not exist, or a service which is not started.
Valid components will still be displayed. When asked to show the debug level,
on both error cases, a message will explain what happened.

The man page does not need to be updated as it does not go into these details
and recommends using the command's ``--help`` option.

A new test called ``test_debug_level_sanity`` will be added to the
``test_sssctl.py`` test suite. It will test the expected behavior is respected
and that error cases are correctly treated.

Authors
*******
- Alejandro López <allopez@redhat.com>
- Pavel Březina <pbrezina@redhat.com>
