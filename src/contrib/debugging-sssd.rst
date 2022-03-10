Debugging SSSD
##############

SSSD consists of multiple processes, namely:

The monitor
    This is the main ``sssd`` process.

Responders
    There is one process for each responder with distinguishable name, for
    example ``sssd_nss``, ``sssd_pam``, etc.

Backends
    There is one process for each configured SSSD domain. Each process is named
    ``sssd_be`` and the domain is determined by the ``--domain`` parameter.

Child processes
    These are special processes that are usually invoked from backends to
    perform individual tasks such as Kerberos authentication or reading GPO
    data. They are located in ``/usr/libexec/sssd`` and suffixed with
    ``_child``, for example ``krb5_child``, ``ldap_child`` or ``gpo_child``.

The following snippet shows a list of running SSSD process with three responders
(nss, pam and pac) and three different domains (ldap.test, samba.test and
ipa.test).

.. code-block:: console

    # ps aux | grep sssd
    root  44  0.4  0.0  29248 11308 ?  Ss  10:51  0:00 /usr/sbin/sssd -i --logger=files
    root  57  0.2  0.0  24728 11412 ?  S   10:51  0:00 /usr/libexec/sssd/sssd_be --domain ldap.test --uid 0 --gid 0 --logger=files
    root  58  0.3  0.1  88920 20748 ?  S   10:51  0:00 /usr/libexec/sssd/sssd_be --domain samba.test --uid 0 --gid 0 --logger=files
    root  59  0.3  0.1  73300 19872 ?  S   10:51  0:00 /usr/libexec/sssd/sssd_be --domain ipa.test --uid 0 --gid 0 --logger=files
    root  60  0.3  0.2  54408 37984 ?  S   10:51  0:00 /usr/libexec/sssd/sssd_nss --uid 0 --gid 0 --logger=files
    root  61  0.0  0.0  28416  9864 ?  S   10:51  0:00 /usr/libexec/sssd/sssd_pam --uid 0 --gid 0 --logger=files
    root  62  0.1  0.0  74416 16220 ?  S   10:51  0:00 /usr/libexec/sssd/sssd_pac --uid 0 --gid 0 --logger=files

    # ll /usr/libexec/sssd
    -rwxr-xr-x. 1 root root  32584 Jan 25 12:03 gpo_child
    -rwxr-xr-x. 1 root root     71 Mar 10 12:03 krb5_child
    -rwxr-x---. 1 root root 119344 Jan 25 12:03 krb5_child.exe
    -rwxr-x---. 1 root root  53136 Jan 25 12:03 ldap_child
    -rwxr-xr-x. 1 root root  69416 Jan 25 12:03 p11_child
    -rwxr-x---. 1 root root  28424 Jan 25 12:03 proxy_child
    -rwxr-x---. 1 root root  32544 Jan 25 12:03 selinux_child
    -rwxr-xr-x. 1 root root     72 Jan 25 10:44 sss_analyze
    -rwxr-xr-x. 1 root root  15960 Jan 25 12:03 sss_signal
    -rwxr-xr-x. 1 root root 208088 Jan 25 12:03 sssd_autofs
    -rwxr-xr-x. 1 root root 245728 Jan 25 12:03 sssd_be
    -rwxr-xr-x. 1 root root  15992 Jan 25 12:03 sssd_check_socket_activated_responders
    -rwxr-xr-x. 1 root root 303048 Jan 25 12:03 sssd_ifp
    -rwxr-xr-x. 1 root root 212160 Jan 25 12:03 sssd_kcm
    -rwxr-xr-x. 1 root root 287696 Jan 25 12:03 sssd_nss
    -rwxr-xr-x. 1 root root 203848 Jan 25 12:03 sssd_pac
    -rwxr-xr-x. 1 root root 278368 Jan 25 12:03 sssd_pam
    -rwxr-xr-x. 1 root root 216096 Jan 25 12:03 sssd_ssh
    -rwxr-xr-x. 1 root root 216336 Jan 25 12:03 sssd_sudo

.. seealso::

    See the :doc:`./architecture` for more information about the different
    processes that makes SSSD.

Disabling the watchdog
**********************

There is a special deadlock guard called the `watchdog`_ that runs inside each
SSSD process. Its purpose is to make sure that the process is still responsive
and kill it if it is not so it can be restarted again by the monitor.

.. _watchdog: https://github.com/SSSD/sssd/blob/master/src/util/util_watchdog.c

The watchdog uses timers and signals mechanisms therefore it interrupts the
process every now and then which makes it difficult to debug the process in the
debugger, not to mention that the process will be killed if you keep it hanging
on a breakpoint for a longer time.

You could tell the debugger to don't react on the ``SIG34`` signal so it is
passed directly to the process.

.. code-block:: console

    $ sudo gdb program $(pidof sssd_nss) -ex 'handle SIG34 nostop noprint'

This however will not solve the problem when the process is waiting on a
breakpoint and therefore it eventually gets terminated by the watchdog. To solve
this, it is recommended to set a long watchdog interval using the ``timeout``
option in ``sssd.conf``, for example to 30000 seconds.

.. code-block:: ini

    [sssd]
    config_file_version = 2
    services = nss, pam
    domains = ldap.test, samba.test, ipa.test
    user = root

    [nss]
    timeout=30000
    ...

    [pam]
    timeout=30000
    ...

    [domain/ldap.test]
    timeout=30000
    ...

    [domain/samba.test]
    timeout=30000
    ...

    [domain/ipa.test]
    timeout=30000
    ...

Attaching debugger to a running process
***************************************

There is only one process for each responder that can be distinguished by name,
therefore it is simple to attach a debugger to the running process. For example:

.. code-block::

    $ sudo gdb program `pgrep sssd_nss`

There can be multiple backend ``sssd_be`` processes and we need to use the
``--domain`` parameter to distinguish between them. Therefore we want to use the
``-f/--full`` option of the ``pgrep`` command to make it match the whole command
line and not only the process name. The following snippet shows how to attach
the debugger to ``ldap.test`` domain:

.. code-block::

    $ sudo gdb program `pgrep -f "sssd_be.+ldap.test"`

.. seealso::

    We created set of `gdb extensions <https://github.com/SSSD/sssd-gdb>`__ for
    SSSD that provides pretty printers to some difficult SSSD structures.

Debugging forked process from its start
***************************************

Usually, you will suffice with attaching debugger to a running process. But
sometimes, you want to debug the process from the very beginning. This applies
especially to the different child processes that are forked from ``sssd_be`` to
perform various stuff like Kerberos authentication.

We can use `gdbserver`_ for that which provides a remote access for ``gdb``. It
can either listen on given device or a TCP connection which we will use in our
examples. To install it, run:

.. _gdbserver: https://sourceware.org/gdb/onlinedocs/gdb/gdbserver-man.html

.. code-tabs::

    .. fedora-tab::

        $ sudo dnf install -y gdb-gdbserver

    .. rhel-tab::

        $ sudo yum install -y gdb-gdbserver

    .. ubuntu-tab::

        $ sudo apt-get install -y gdbserver

Now, we need to create a wrapper that would execute the process in the gdbserver
that will listen on a specific port.

.. code-block:: console

    $ process=/usr/libexec/sssd/krb5_child
    $ sudo mv "$process" "$process.exe"
    $ sudo cat << 'EOF' > $process
    #!/bin/bash
    exec gdbserver :1234 /usr/libexec/sssd/krb5_child.exe "$@"
    EOF
    $ sudo chmod +x "$process"

Now we need to increase timeout of the child process in order to avoid its
termination during the debugging session. We'll use the ``krb5_auth_timeout``
for that.

.. code-block:: ini

    [domain/ipa.test]
    timeout=30000
    krb5_auth_timeout=30000

Now you can start SSSD and let it get to the process that you want to debug, it
is the ``krb5_child`` in our example so we can try authenticate as some user,
i.e. ``su admin@ipa.test``. Then start gdb and attach it to the server:

.. code-block:: console

    $ sudo gdb /usr/libexec/sssd/krb5_child.exe -ex "target remote :1234" -ex "b main" -ex "c"

.. seealso::

    Another way of debugging a child process is to use ``set follow-fork-mode
    child`` when debugging the parent process. It will tell ``gdb`` to start
    debugging the child once it is forked off the parent. See `gdb manual
    <https://sourceware.org/gdb/onlinedocs/gdb/Forks.html>`__ for more
    information.
