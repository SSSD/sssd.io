Running Tests
=============

SSSD is a complex piece of software with a long development history. Therefore, there has been several layers of tests with different goals and using different frameworks. We are currently in progress of reworking all of our tests and standardizing them using our own `SSSD Test Framework <https://tests.sssd.io/en/latest/>`_.

To get started immediately you can visit `Running Tests <https://tests.sssd.io/en/latest/running-tests.html>`_ page in the `SSSD Test Framework <https://tests.sssd.io/en/latest/>`_ wiki and start following the instructions provided.

Overview
--------

Our system tests are written using Pytest and `Pytest Multihost Plug-in <https://github.com/next-actions/pytest-mh>`_ orchestrating the setup, management, execution and teardown of hosts and tests.

All major identity providers; LDAP, Kerberos, FreeIPA, Microsoft Active Directory, Samba Active Directory are provisioned as VMs or containers and are intended to be provisioned on each run, ensuring the machines are in a clean state. The setup code is in our `SSSD CI Containers Repository <https://github.com/sssd/sssd-ci-containers/>`_. Note, these machines are not to be used for production and should only be used in development and local testing only.

For a comprehensive test run, requires several hosts; client, nfs, dns, ipa, krb, samba, ldap and ad. Emulating several environments and scenarios needed by the tests. In local testing, all containers use podman for containerization then Vagrant and KVM for virtualization. Two networks are created for each virtual computing service and needs to be routable to one another. For simplicity, all documentation assumes that one physical host is used to run the tests.

The tests are designed to be generic, and will run against all supported topologies, but some tests are written to be run against a specific topology or topologies. Topologies also define which hosts are needed by the test. For example, AD topology will require a client host and an AD host, Samba topology will require a client and a Samba host but both can be used by the GenericAD topology group will run against both AD and Samba.

Tests are also written so they can be ran independently, any test setup that is needed by the test, is executed right before the test code and is undone or the host is refreshed for the following test. For example, 389 as an LDAP provider is destroyed and re-installed before every test that, while AD the setup is undone.

Test Types
----------

Historically we have had four different test types on different frameworks. To get started, please reference system tests, because we will be retire-ring the integration and multihost tests.

.. toctree::
    :maxdepth: 0
    :titlesonly:

    tests/unit-tests
    tests/system-tests
    tests/integration-tests
    tests/multihost-tests
