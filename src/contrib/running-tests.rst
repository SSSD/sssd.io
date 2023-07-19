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

SSSD CI Containers
------------------

Developing and testing SSSD features may require Active Directory/FreeIPA/LDAP systems that can be easily provisioned and destroyed. The `SSSD CI Containers <https://github.com/sssd/sssd-ci-containers/>`_ containers and images are intended to be used in SSSD CI and they should not be used in production. However, you can use them during SSSD local testing and development.

It creates an out of the box working container environment with 389 Directory Server, IPA and Samba Active Directory servers. It also creates an SSSD client container enrolled to those servers, ready to build and debug your code.
