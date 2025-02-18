Profiling SSSD
##############

Getting Ready
*************

There are several tools allowing us to profile an application. We will focus on
perf_ which seems to be the one that works best with SSSD.

.. _perf: https://perf.wiki.kernel.org

First you need to install the ``perf`` tool:

.. code-tabs::

    .. fedora-tab::

        # dnf -y install perf js-d3-flame-graph

    .. ubuntu-tab::

        $ sudo apt install linux-tools-common linux-tools-generic


Make sure the debug information is available for SSSD and all its dependencies
either by using ``debuginfod``, or by manually installing the debug information
packages:

.. code-tabs::

    .. fedora-tab::

        # dnf debuginfo-install -y sssd* libsss_* samba-client-libs libsmbclient \
        libldb libtevent libtalloc libini_config c-ares glibc

    .. ubuntu-tab::

        $ sudo apt install sssd-ad-common-dbgsym sssd-ad-dbgsym sssd-common-dbgsym \
        sssd-dbus-dbgsym sssd-ipa-dbgsym sssd-kcm-dbgsym sssd-krb5-common-dbgsym \
        sssd-krb5-dbgsym sssd-ldap-dbgsym sssd-proxy-dbgsym sssd-tools-dbgsym \
        libsss-certmap0-dbgsym libsss-idmap0-dbgsym libsss-nss-idmap0-dbgsym \
        libsss-simpleifp0-dbgsym libsss-sudo-dbgsym libldb2-dbgsym libtdb1-dbgsym \
        libtalloc2-dbgsym libtevent0-dbgsym libc6-dbgsym

.. seealso::

    More information on `Debug Symbol Packages`_ for Ubuntu.

.. _`Debug Symbol Packages`: https://documentation.ubuntu.com/server/reference/debugging/debug-symbol-packages/

.. note::

    If you are using SELinux, the shipped targeted policy may prevent ``perf``
    from interacting with the SSSD process. You can put SELinux into permissive
    mode to confirm or look at the audit logs and add the required rules. Rules
    can be added using ``audit2allow``. 

Profiling
*********

The simplest way to profile one of the SSSD's daemons is to attach the profiler
to the process while it is running.

Once SSSD is running and ready to be profiled, identify the PID of the process
you want to monitor (``sssd_ssh``, ``sssd_nss``, ``sssd_be``, etc.), start the
``perf`` command in the background, launch the command you want to profile
and stop the profiling after the command completes:

.. code-block:: console
    :caption: `Profiling the LDAP domain daemon during the id command`

    # PID=$(pgrep -f 'sssd_be --domain LDAP')
    # perf record --pid=$PID --call-graph=dwarf -e cycles:u &
    # id user1002@LDAP
    # kill %%

.. code-block:: console
    :caption: `Profiling the sssd_nss daemon during the ls command`

    # perf record --pid=$(pgrep -f 'sssd_nss') --call-graph=dwarf -e cycles:u &
    # ls -l /tmp
    # kill %%


This will create a ``perf.data`` file in your current directory. It is
recommended to process this file in the same machine, so that the debug
information matches perfectly the installed binaries. You can later move the
results to another host.

The ``-e cycles:u`` argument tells ``perf`` to only monitor the CPU cycles the
application consumes in user space. The kernel will not be profiled. Check the 
``perf-record(1)`` man page for more options that might be useful in you
particular case.

Generating the Reports
**********************

We will create two types of reports: a text report and a flame graph to be seen
in a web browser:

.. code-block:: console

    # perf report -g > report.txt
    # perf script report flamegraph

The files ``report.txt`` and ``flamegraph.html`` contain the reports, are
self-contained, and can safely be moved to another host.

.. seealso::

    Other reports are available. You can learn about them in the
    ``perf-report(1)`` and ``perf-script(1)`` man pages.

