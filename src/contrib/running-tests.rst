Running Tests
=============

SSSD is a complex piece of software with a long development history. Therefore, there are several layers of tests with different goals and using different frameworks. This page shows how to run the tests and how to add new ones or modify the existing tests.

Existing test types
-------------------

Each test is different. Sometimes, you want to test the whole system end-to-end, sometimes the test should exercise some corner case for which special input and environment must be simulated. This section should give you a better idea what kind of tests already exist in SSSD so that you can choose where to add a new test and also provides a general overview.

.. toctree::
    :maxdepth: 0
    :titlesonly:

    tests/unit-tests
    tests/integration-tests
    tests/multihost-tests

Virtual Test Suite for SSSD
---------------------------

Developing and testing SSSD features may require Active Directory/FreeIPA/LDAP systems that can be easily provisioned and destroyed. The `SSSD Test Suite <https://github.com/SSSD/sssd-test-suite/>`_ is a set of Vagrant and Ansible scripts that will automatically setup and provision several virtual machines that you can use to test SSSD.

It creates an out of the box working virtual environment with 389 Directory Server, IPA and Active Directory servers. It also creates an SSSD client machine enrolled to those servers, ready to build and debug your code.
