.. _multihost-tests:

===============
Multihost tests
===============

SSSD multihost tests are the closest our tests get to running SSSD in the real world. The multihost tests utilize a VM the tests are ran at, so no part of the setup is faked. This is also the test's biggest advantage, as long as you can prepare the test environment, the tests can then be used to test even Active Directory or FreeIPA integration. Also, unlike the cwrap tests or the unit tests, the multihost tests are typically good enough for distribution QE teams, so the multihost tests allow a collaboration between the team that typically just develops SSSD and the team that tests it.

The disadvantage of the tests is that setting up the environment can be complex and the development loop (the time between modifying test, modifying the SSSD sources, deploying them to the test environment and running the tests) is much longer than with the cwrap based tests.

Running multihost tests
-----------------------

First, the infrastructure does not yet concern itself with provisioning at all. You need to set up an environment to run the tests on yourself, we recommend using the `SSSD CI Containers <https://github.com/sssd/sssd-ci-containers>`_ to handle the provisioning. The **tests will modify the machine** so use something disposable.

Clone and cd into the SSSD github repository:

.. code-block:: bash

    git clone https://github.com/SSSD/sssd.git
    cd sssd

You may choose to run the tests inside a python virtual environment, but it is not required.

.. code-block:: bash

    dnf install python3-pip python3-virtualenv
    virtualenv .mh-venv
    source .mh-venv/bin/activate

The file ``src/tests/multihost/basic/mhc.yaml`` is already configured properly if you are using the SSSD Test Suite, run the tests with:

.. code-block:: bash

    pip3 install -r src/tests/multihost/requirements.txt
    pytest-3 -s --multihost-config=src/tests/multihost/basic/mhc.yaml src/tests/multihost/basic

When running multihost tests, you may see the following error:

.. code-block:: bash

     sssd.testlib.common.exceptions.DirSrvException: fail to setup Directory Server instance

The test setup code automatically sets up a directory server instance, but if the test
cleanup code does not execute cleanly, or fully, then some manual cleanup is needed on
the non-controller system(s).

.. code-block:: bash

     remove-ds.pl -i slapd-example-1

If you use a more recent version of 389ds you might have to call

.. code-block:: bash

     dsctl slapd-localhost remove --do-it

instead.

And possibly

.. code-block:: bash

     kdb5_util destroy -f EXAMPLE.TEST


