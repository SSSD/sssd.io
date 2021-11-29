Log Analyzer
############

The SSSD 2.6.0 release includes a new log parsing tool for SSSD debug log
analysis. This analyzer tool can be called using the ``sssctl analyze`` command, the log analysis tool primarily acts as a grep front-end.

Use Case
********
Identifying SSSD failures can be a difficult task without knowledge of SSSD internal components. If an administrator or SSSD user doesn't know what to look for, it may become a very slow and time consuming process. The ``sssctl analyze`` tool improves the overall troubleshooting workflow for administrators, users, and anyone needing to review SSSD debug logs. The initial use case is to extract and print SSSD logs pertaining only to certain client requests across responder and backend sssd processes.

A `Pull request <https://github.com/SSSD/sssd/pull/5863>`_ is in review upstream to enable functionality for the analyzer tool to print logs across all responders, and SSSD child processes.

Command line
************
The ``sssctl analyze`` command uses git-like subcommand invocation.

.. code-block:: bash

    # sssctl analyze MODULE [ARGS]

The only supported module currently is the **request** module. The request module is used to print logs associated with client requests made to SSSD.

.. note::

    Additional modules to be added contingent on future SSSD development plans

.. code-block:: bash

    # sssctl analyze request
    Usage: sss_analyze.py request [OPTIONS] COMMAND [ARGS]...

    Request module

    Options:
    --help  Show this message and exit.

    Commands:
    list
    show

Request Tracking
****************

``sssctl analyze request`` operates in two different primary modes shown in the table below. ``list`` mode is intended to use first, to find the client ID which can then be passed to the ``show`` command. The client ID can also be found in the log files (search for **[CID #]** tag).

+----------------+---------------------------+--------------------------------------------------------------------------------------------------------+
| mode           | mode functionality        | additional options                                                                                     |
+================+===========================+========================================================================================================+
| list           | Output list of recent     | -v, --verbose             Enables verbose output                                                       |
|                | client requests made to   | --pam                     Filter only PAM requests                                                     |
|                | sssd                      |                                                                                                        |
+----------------+---------------------------+--------------------------------------------------------------------------------------------------------+
| show           | Print logs pertaining to  | --merge                   Merge logs together sorted by timestamp (requires debug_microseconds = True) |
|                | a provided client ID      | --cachereq                Include cache request logs                                                   |
|                | number                    | --pam                     Track only PAM requests                                                      |
|                |                           |                                                                                                        |
+----------------+---------------------------+--------------------------------------------------------------------------------------------------------+


Command examples
****************

.. warning::
    Requests which return from the SSSD memory cache will not be logged, and therefore not tracked by the analyzer

Print client command request list, NSS (default), or PAM

.. code-block:: bash

    # sssctl analyze request list
    # sssctl analyze request list --pam

Verbose list output

.. code-block:: bash

   # sssctl analyze request list -v

Track individual NSS request id number 20

.. code-block:: bash

    # sssctl analyze request show 20

Track individual NSS request including cache request logs

.. code-block:: bash

    # sssctl analyze request show 20 --cachereq

Track individual PAM request

.. code-block:: bash

    # sssctl analyze request show 20 --pam

Supports ``--logger=journald`` configurations

.. code-block:: bash

    # sssctl analyze --source=journald request list

Analyze logs extracted, or sent from another user.

.. note::
    Logs must be from compatible SSSD version built with tevent chain ID support.

.. code-block:: bash

    # sssctl analyze --logdir=/path/to/var/log/sssd request list

Feedback
********

SSSD development would appreciate any positive, or negative, `feedback <https://github.com/SSSD/sssd/issues/new>`_ on the log analyzer tool. One reason the log analyzer tool is written in python is to encourage contributions. Improvement suggestions and :doc:`Pull Requests </contrib/introduction>` are welcome!