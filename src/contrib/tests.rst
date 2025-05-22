
Tests
============

SSSD is a complex piece of software with a long development history. Therefore, several layers of tests have been
created with different goals and using various frameworks. We are currently in the process of reworking our
integration and multihost tests into system tests. Unit and system tests are actively maintained and used.

Test Types
^^^^^^^^^^

Historically, we have had four different test types on other frameworks. The integration and multi-host test cases are being rewritten as system tests using the `SSSD Test Framework <https://tests.sssd.io/en/latest/>`_.

.. toctree::
    :maxdepth: 0
    :titlesonly:

    tests/unit-tests
    tests/system-tests
    tests/integration-tests
    tests/multihost-tests

Running tests
^^^^^^^^^^^^^

To get started contributing to system tests, the first step is to set up your test environment. Please visit `Running
Tests <https://tests.sssd.io/en/latest/running-tests.html>`_ page in the `SSSD Test Framework <https://tests.sssd.io/en/latest/>`_ wiki and start following the instructions provided.
