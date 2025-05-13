.. _intg-tests:

=================
Integration tests
=================

.. note::

    We are replacing our integration tests, please note that this page is deprecated and may contain out of date information. Please refer to :doc:`system-tests` for the latest information.

SSSD integration tests run the deamon at the same machine you are developing on with the help from the `cwrap <https://cwrap.org>`_. The integration tests are half-way between the unit tests that call APIs or run a single component in isolation and between the multihost tests that run on a dedicated VM. During the integration tests, a build of SSSD is compiled and installed into an environment set up with the help of the ``fakeroot`` program. Then, the cwrap libraries are preloaded into the test environment. The socket_wrapper library provides networking through UNIX pipes, the uid_wrapper library provides the notion of running as root and the nss_wrapper library allows to route requests for users and groups through the NSS module under test.

The advantage over the unit tests is obvious, the full daemon is ran and you can talk to the SSSD using the same interfaces as a user would do in production, e.g. resolve a user with ``getpwnam``. Because the tests are ran on the same machine as the developer works on, it is much faster to compile a new SSSD version for the tests to run and so the develop-test-fix cycle is generally quite fast. The integration tests also offer a simple way to add a "breakpoint" to the tests and connect to the tests using ``screen(1)``. Finally, since the tests run on the same machine, they can trivially run on any OS release or any distribution with little to no changes, even in build systems that typically have no network connectivity as part of the SSSD build.

The disadvantages also stem from running the tests on the local machine. SSSD relies on whatever server it is connecting to to also run in the test environment provided by the cwrap libraries, but in many cases that is so difficult that we even haven't done the work (e.g. FreeIPA) or outright impossible (Active Directory). Even within the tests themselves, we sometimes stretch the limits of the cwrap libraries. As an example, the socket_wrapper library doesn't support faking the client credentials that the SSSD reads using the ``getsockopt`` call with the ``SO_PEERCRED`` parameter.

Integration tests dependencies
------------------------------
Integration tests requires additional packages which are not installed in system by default. One way to solve this is to trigger ``make intgcheck`` in loop and add reported missing packages manually. Alternative option is to install bellow packages which in most cases should satisfy integration test requirements:

.. code-tabs::

    .. fedora-tab::

        sudo dnf builddep sssd
        sudo dnf install -y \
            clang-analyzer \
            curl-devel \
            fakeroot \
            http-parser-devel \
            krb5-server \
            krb5-workstation \
            lcov \
            libcmocka-devel \
            libfaketime \
            mock \
            nss_wrapper \
            openldap-clients \
            openldap-servers \
            pam_wrapper \
            python3-ldap \
            python3-ldb \
            python3-psutil \
            python3-pycodestyle \
            python3-pytest \
            python3-requests \
            redhat-lsb-core \
            rpm-build \
            uid_wrapper \
            valgrind

Running integration tests
-------------------------

The easiest way to run the integration tests is by running: :

.. code-block:: bash

    make intgcheck

This makefile target consists of two targets, actually:

.. code-block:: bash

    make intgcheck-prepare
    make intgcheck-run

The former builds the special SSSD build and creates the environment for tests. The latter actually runs the tests.

Running the complete suite of tests may be overkill for debugging. Running individual tests from the suite can be done according to the following examples: :

.. code-block:: bash

    make intgcheck-prepare
    INTGCHECK_PYTEST_ARGS="-k test_netgroup.py" make intgcheck-run
    INTGCHECK_PYTEST_ARGS="test_netgroup.py -k test_add_empty_netgroup" make intgcheck-run

The `INTGCHECK_PYTEST_ARGS` format can be checked in the `PyTest official documentation <http://doc.pytest.org/en/latest/contents.html>`_.

Sometimes, during test development, you find out that the code needs to be fixed and then you'd like to re-run some tests. ``intgcheck-prepare`` needs to be run only once per debugging session. After you've made the required changes to the SSSD code, cd into the ``intg/bld`` subdirectory in your build directory and recompile and re-install the test build:

.. code-block:: bash

    cd intg/bld
    make
    make -j1 install # Sometimes parallel installation causes issues

Now, re-running make ``intgcheck-run`` (optionally with any parameters, like only a subset of tests) would run your modified code\!

Debugging integration tests
---------------------------

There are three basic ways to debug the integration tests - add print statements to the test, read the SSSD logs from the test directory and insert a breakpoint.

Print statements can be useful to know what's going on in the test code itself, but not the SSSD. Tests remove the logs after a successful run and also suppress stdout during a successful run, so in order to make use of either print statements or the logs, you might need to fail the test on purpose e.g. by adding:

.. code-block:: python

    assert 1 == 0

The debug logs might be useful to get an insight into the SSSD. Let's pretend we want to debug the test called ``test_add_empty_netgroup``. We would add the dummy assert to fail the test first. Then, in the test fixture, we'd locate the function that generates the ``sssd.conf`` (often the function is called ``format_basic_conf`` in many tests) and we'd add the ``debug_level`` parameter:

.. code-block:: python

  --- a/src/tests/intg/test_netgroup.py
    +++ b/src/tests/intg/test_netgroup.py
    @@ -109,6 +109,7 @@ def format_basic_conf(ldap_conn, schema):
            disable_netlink     = true

            [nss]
    +       debug_level = 10

            [domain/LDAP]
            {schema_conf}

Next, we can run the test, expecting it to fail:

.. code-block:: bash

    INTGCHECK_PYTEST_ARGS="-k add_empty_netgroup" make intgcheck-run

In the test output, we locate the test directory which always starts with ``/tmp/sssd-intg-*``. This director contains the fake root and we can then do useful things such as read the logs from outside the build environment:

.. code-block:: bash

    less /tmp/sssd-intg.1ifu0f6n/var/log/sssd/sssd_nss.log

The final option is to insert a breakpoint into the test and jump into the test environment with ``screen(1)``. The breakpoint is inserted by calling the ``run_shell()`` function from the ``util`` package. Again, using the ``test_add_empty_netgroup`` test as an example, we need to first import ``run_shell``:

.. code-block:: python

    from util import run_shell

Next, we call ``run_shell()`` from the test function and invoke ``intgcheck-run`` again. You will see that the test started, but did not finish with either pass or fail, it seemingly hangs. This is when we can check that there is a screen instance running and connect to it:

.. code-block:: bash

    $  screen -ls
    There is a screen on:
            21302.sssd_cwrap_session        (Detached)
    1 Socket in /run/screen/S-jhrozek.
    $  screen -r sssd_cwrap_session

From within the screen session, you can attach ``gdb`` to the SSSD processes, call ``getent`` to resolve users or groups ``ldbsearch`` the cache etc. To finish the debugging session, simply exit all the terminals in the tabs.

Examples
--------

The tests themselves are located under ``src/tests/intg``. Each file corresponds to one "test area", like testing the LDAP provider or testing the KCM responder.

To see an example of adding test cases to existing tests, see commit `76ce965fc3abfdcf3a4a9518e57545ea060033d6 <https://github.com/SSSD/sssd/commit/76ce965fc3abfdcf3a4a9518e57545ea060033d6>`_ or for an example of adding a whole new test, including faking the client library (which should also illustrate the limits of the cwrap testing), see commit `5d838e13351d3062346ca449e00845750b9447da <https://github.com/SSSD/sssd/commit/5d838e13351d3062346ca449e00845750b9447da>`_ and the two preceding it.

