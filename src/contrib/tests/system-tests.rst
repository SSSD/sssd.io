.. _system-tests:

============
System Tests
============

Eventually all the integration and multihost tests will be re-worked and moved to system tests. Like the current multihost the system tests are the closest to using SSSD in the real world. The differences between multihost tests and the system tests is the approach.

To start, we are taking everything we have learned from before. The SSSD system tests now have an emphasis on documentation and coding standards. Specifying what the test is suppose to do and why. We are standardizing all the tests to use our `SSSD Test Framework <https://tests.sssd.io/en/latest/>`_ and `pytest-mh pytest plugin <https://github.com/next-actions/pytest-mh>`_.

Unlike the multihost tests, specific provider calls are abstracted allowing us to use one test for all topologies. Greatly reducing the amount of test code and administrative overhead when maintaining these tests. To learn more, please visit `SSSD Test Framework <https://tests.sssd.io/en/latest/>`_ page.
