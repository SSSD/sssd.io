Reporting bugs
##############

This document describes how to file an SSSD bug report or an enhancement request. Providing accurate and detailed information will assist SSSD developers in quickly identifying and fixing the bug. A minimal reproducer with explicit steps should be provided in a bug report, or at least a detailed description of your environment if a reproducer is not identifiable.

Navigate to `the new ticket form <https://github.com/SSSD/sssd/issues/new>`_ to file a new issue. Some bugs will be automatically cloned from distribution bug-trackers, such as `BugZilla <http://bugzilla.redhat.com>`_.

Include necessary debugging data
********************************

Always include the following data in a bug report:

* One bug report per ticket. If you think you found multiple problems, file each one in a separate ticket.
* Search the ticket database for possible duplicates. If you find a duplicate, please add a comment saying that you encountered the problem as well.
* Is this a defect or an enhancement? If the ticket you are filing is about adding new functionality and not about a defect in existing functionality, please add the ``RFE`` tag.
* Short problem summary. A good example is: "The LDAP provider segfaults when an invalid TLS certificate is specified".
* CC (optional). If there are other parties interested in a particular bug, please ``@mention`` their GitHub usernames in the ticket.
*  What platform are you on? Please provide the operating system version and architecture.
* The SSSD version. On an RPM-based system, you can just run ``rpm -q sssd``. (If the bug is in the current working tree, please mention that as well)
* The SSSD config file. Typically this would be located at ``/etc/sssd/sssd.conf``
* The SSSD log files with a high debug level. Please see the troubleshooting page on information on how to gather them and other required information. When submitting the logs, it's very helpful to remove the existing log files before running the test case. This ensures the logs only capture the problem and developers don't need to weed out gigabytes of info.
* The steps to reproduce the bug. It's very useful to log the times of the commands that reproduce the bug as you execute them. For instance, if two `id` commands run in sequence would give different information for the admin user, please run them like this:

.. code-block:: bash
    
    $ date; id admin; date; id admin; date

* Describe your network topology and the server types and versions. This is especially important in complex setups with trusted IPA or Active Directory domains.
* What are the results you expect? What were the results you see instead? Please be specific. A bad example is "My logins are slow". A much better example is "When a user who is a member of 100 groups logs in, his login takes 50 seconds even though a kinit and id -G for the same user are fast."

Some data in the SSSD tickets are handled by the SSSD team members. Please leave Priority, Milestone, and Assignee to their defaults.

Providing SSSD crash data
*************************

In addition to the data described above, please also provide the coredump and backtrace along with the bug report.

If you are on a Fedora or RHEL system, ``abrt`` is a great tool for gathering crash info. If abrt is not available, you can retrieve the core file and backtrace manually. First, find out which sssd process is crashing. Please always make sure you have the exact matching debuginfo package version on your system. On Fedora and RHEL, you can easily install the debuginfo packages with ``debuginfo-install sssd``. Then, connect to the faulty process with gdb and resume it:


.. code-block:: bash
    
    # gdb program $(pidof sssd_be)
    (gdb) continue

When the program crashes, save the core file and backtrace:

.. code-block:: bash
    
    (gdb) generate-core-file
    Saved corefile core.7336
    (gdb) bt full
    # lots of output, copy and paste to the bug report

Then attach the core file and the backtrace.

When connecting to an sssd process with ``gdb``, you should increase the ``timeout`` option in the debugged process's section up from its default value, such as:

.. code-block:: ini
    
    [domain/test]
    id_provider=ldap
    ....
    timeout = 300

If you don't do this, chances are that ``gdb`` will be interrupted by SSSD's internal watchdog (which manifests as SSSD receiving ``SIGRT``) before you can catch the error you're debugging.

Alternatively, you can disable the watchdog from inside the gdb session:

.. code-block:: bash
    
    gdb process `pgrep sssd_be` -ex "p teardown_watchdog()"

This has the advantage of not having to restart the sssd, on the other hand, the watchdog is also disabled for the single gdb session only.

Mind your privacy
*****************

Both the SSSD log files and the coredumps might include confidential information. If you don't like them to be exposed in the SSSD bug tracker instance, please contact some of the SSSD developers on the ``#sssd`` channel on FreeNode or on the `sssd-users <https://lists.fedorahosted.org/archives/list/sssd-users@lists.fedorahosted.org>`_ mailing list.

Always test the latest available version
****************************************

SSSD moves at a rapid pace. It's not useful to file a bug report against an old version, please upgrade to the latest release in the branch you're running, if the branch is still active. You can find the tarballs on our releases page. If you're running an Enterprise or Long-Term-Maintenance distribution and can't update to a newer version, consider filing a bug report in your distribution bug tracker instead.

Alternatively, ask on the ``#sssd`` channel on FreeNode. Several SSSD or FreeIPA developers maintain private repositories with custom builds for stable platforms.

Consider if the bug has security consequences
*********************************************

If you think you found a bug that has security impact (allows an unprivileged user to compromise SSSD or elevate privileges for instance), don't file the bug in a public bug tracker. Instead, e-mail any of the SSSD developers instead.
