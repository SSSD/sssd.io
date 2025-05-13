.. _system-tests:

============
System Tests
============

Eventually all the integration and multihost tests will be re-worked and moved to system tests. Like the current multihost the system tests are the closest to using SSSD in the real world. The differences between multihost tests and the system tests is the approach.

Overview
-------------

Our system tests are written using Pytest and `Pytest Multihost Plug-in <https://github.com/next-actions/pytest-mh>`_ orchestrating the setup, management, execution and teardown of hosts and tests.

All major identity providers, LDAP, Kerberos, FreeIPA, AD, Samba, are provisioned as VMs or containers and are intended to be cleaned for each run. The setup code is in our `SSSD CI Containers Repository <https://github.com/sssd/sssd-ci-containers/>`_.

.. warning::

    These machines are not to be used for production and should only be used in development and testing only.

A comprehensive test run needs several hosts: client, nfs, dns, ipa, krb, samba, ldap, and ad. Emulating several environments and scenarios required by the tests. In local testing and development, all containers use docker or podman, then Vagrant and KVM for virtualization. Networks are created for each virtual computing service and need to be routable to one another. For simplicity documentation assumes everything is running on a single Linux host. Baremetal or a virtual machine with nested virtualization support.

Writing tests
-----------------

Please review the concepts and guidelines before contributing to our tests. Understanding the concepts and adhering to the guidelines and code styles will make this process easier. If any part of this guide can be improved, please do not hesitate to contact us or submit a pull request.

Concepts
^^^^^^^^^^

Formerly, our test cases would have been organized by providers and major features; such as *'ad_provider'*, *'ipa_provider'*, *passkeys*, *sssctl* naming a few. The `SSSD Test Framework <https://tests.sssd.io/en/latest/>`_ allows us to abstract the identity provider, parametrizing a single test to be run against all providers. Since then, we have started to organize our tests by **user stories**, also referred to as **customer scenarios**. To better understand how the customer uses SSSD and emulate their usage as part of a customer-centric approach.

Readability and comprehension
'''''''''''''''''''''''''''''''

* Why the test was written and what scenario it covers must be understood first and foremost.
* Documentation should be short and concise without being overly specific.
* Specific details will be extrapolated from the code.
* When more information is beneficial, avoid duplicating content from other places. Just add a link.

Every test is independent and specific
''''''''''''''''''''''''''''''''''''''''

* Any changes the test makes need to be reverted when the test is finished. This is handled by the test framework, a backup is taken during setup and a restore is performed during teardown.
* Tests must cover a specific configuration, setting, and scenario, not multiple cases.
* Test cases will be less specific when parametrized.

Design, plan, and extend the API
''''''''''''''''''''''''''''''''''

* Extend the test framework making it easier to write and maintain tests. Writing tests needs to be intuitive.
* Design and plan the features when extending the `SSSD Test Framework <https://tests.sssd.io/en/latest/>`_. Build on classes and methods when something similar exists.
* Avoid  too many cumbersome calls to the host and overly complicated test code.

In the below example, several tests use this setup and it makes sense to add it to the``SSSDCommonConfiguration`` class.

.. code-block::
    :caption:  Too many lines

    # Configure SSSD with proxy provider
    client.sssd.common.proxy("ldap", ["id", "auth"], server_hostname=ldap.host.hostname)
    client.sssd.domain["case_sensitive"] = "Preserving"
    client.sssd.svc.restart("nslcd")
    client.sssd.restart()

    client.fs.append(
        "/etc/nslcd.conf",
        "base dc=ldap,dc=test\n"
        "ignorecase yes\n"
        "validnames /^[a-z0-9._@$()]([a-z0-9._@$() ~-]*[a-z:0-9._@$()~-])?$/i\n",
        dedent=False,
    )
    client.sssd.svc.restart("nslcd")
    client.sssd.restart()

A way to approach it, is backwards, decide how we want to write the test code and make the code work.

.. code-block::
    :caption: Ideal test code

    def  test_nslcd(client: Client, provider: GenericProvider):
        client.sssd.common.nslcd(provider.server)
        client.sssd.start()

.. code-block::
    :caption:  Setup added to the framework

    def nslcd(server: str):
        client.sssd.common.proxy("ldap", ["id", "auth"], server_hostname=server)
        client.sssd.domain["case_sensitive"] = "Preserving"
        client.sssd.svc.restart("nslcd")

        client.fs.append(
            "/etc/nslcd.conf",
            "base dc=ldap,dc=test\n"
            "ignorecase yes\n"
            "validnames /^[a-z0-9._@$()]([a-z0-9._@$() ~-]*[a-z:0-9._@$()~-])?$/i\n",
            dedent=False,
        )
        client.sssd.svc.restart("nslcd")

Add test coverage by parametrizing topologies and abstracting methods
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

* Increase test coverage by using multiple `topologies <https://tests.sssd.io/en/latest/writing-tests.html#using-the-topology-marker>`_  and pre-defined topology groups. This makes the tests generic and compatible with multiple providers.
* Extend the `SSSD Test Framework <https://tests.sssd.io/en/latest/>`_ and abstract methods to support multiple providers.

An example of this is *Active Directory Group Policy Objects*. These tests require different calls to set up GPOs on AD and Samba. Abstracting the methods will extend the test to cover both topologies instead of two sets of tests.

Guidelines
------------

All code must be fully typed and follow the black coding style. All code must be validated using the following tools:

* Check PEP8 compliance with `flake8 <https://flake8.pycqa.org>`__ and `pycodestyle <https://pycodestyle.pycqa.org>`__.
* Sort imports with `isort <https://pycqa.github.io/isort/>`__.
* Convert to `black <https://black.readthedocs.io>`__ style.
* Check types with `mypy <https://mypy.readthedocs.io>`__.

Organizing test cases
^^^^^^^^^^^^^^^^^^^^^

Pytest allows you to write tests inside a class (starts with `Test`) or directly inside a module (a function
starting with `test_`). Even though it might be logical to organize tests inside a class, it does not give you any
benefit over plain function and it create just one more level of organization that must be correctly kept and
maintained.

.. warning::

    **Avoid organizing tests into classes** *unless there is a good reason to use them* .

File header
^^^^^^^^^^^

* The beginning of the file must contain the title and requirements.
* The beginning of the file must provide a summary, not more than a couple of lines, detailing what the test covers.
* A guide must be provided if the tests require additional knowledge to run; a great example is `passkey tests <https://github.com/SSSD/sssd/blob/master/src/tests/system/tests/test_passkey.py>`__.

Naming
^^^^^^^

Test names contain three parts, the **pytest discovery pattern**, **file name**, and **test name**.

* **test**\_ Pytest discovery pattern.
* test\_ **filename**\__ File name, no extension and a double underscore separating the file name from the test name.
* test_filename\__ **name_of_the_test** Test name (see below).

Naming criteria
'''''''''''''''''

* Test names should describe the expected behavior of what you are testing.
* Test names should describe what the code is doing.
* Test names should provide a good idea of what the test does.
* Test names can use the filename to help describe what the test does.

Docstring
'''''''''''

All tests require the following documentation strings.

* **title**: Test name without the_under_scores.
* **description**: Optional, if the name is not clear enough. Any additional information that helps others understand the purpose of the test. If the description is long and requires multiple lines, start the description with a new line and indentation as shown in the example.
* **setup**: All steps leading up to the scope of the test.
* **steps**: Only relevant steps that are described in the test name.
* **expectedresults**: Test results must equal the number of steps.
* **customerscenario**: True, if this is a customer scenario.

The priority of the docstring is to understand the purpose of the test and provide any information that will help future maintainability.
The docstring will provide more of a summary rather than specific details of the test. In a well-written test, the details will be easily readable from the test code.

.. code-block::
    :caption: docstring example

    """
    :title: Feature presence
    :description:
        The parametrization states the distribution name, distribution version, SSSD version and feature
        presence.

        As an example, ("Fedora", 39, 0, 2, 9, "passkey", True) should be read in the following way:
        In a Fedora 39 or higher system with SSSD 2.9 or higher, passkey feature shall be present.

        Another example, (None, None, None, 2, 10, "knownhosts", True):
        In a system with SSSD 2.10 or higher, knownhosts feature shall be present.
    :setup:
        1. Skip if distribution name doesn't match
        2. Skip if distribution version doesn't match
    :steps:
        1. Check SSSD version and feature presence
    :expectedresults:
        1. Depending on the parameterization, the feature shall be present or not
    :customerscenario: False
    """

Code
^^^^^^

While the docstrings contain the emphasis of what and why. The code will contain the how. There is a strong preference making the code readable and efficient over anything else like making the test more comprehensive, elegant or concise. There is no applicable rule but suggestions. If it's complicated, maybe split into a couple of test cases. If reading code feels like a tennis match bouncing back and forth between parts of the code and docstrings, it can be improved. Take the following example.

.. code-block::

    u1 = provider.user("user1").add()
    u2 = provider.user("user2").add()
    u3 = provider.user("user3").add()

    client.sssd.domain["access_provider"] = "simple"
    client.sssd.domain["simple_allow_groups"] = "group1"
    client.sssd.domain["simple_deny_groups"] = "group2"

    provider.group("group1").add().add_members([u1, u3])
    provider.group("group2").add().add_members([u2, u3])

    client.sssd.start()

As a simple example, the difference is pretty inconsequential between asserting by the variable than by the string. The preference is to *hardcode* the  value in the assertions. Looking at the test code, there is no additional step to remember or check what the assertion needs to be in order to pass.

.. code-block::

    assert client.auth.ssh.password("user1", "Secret123"), "User should be able to log in!"
    assert not client.auth.ssh.password("user2", "Secret123"), "User should NOT be able to log in!"
    assert not client.auth.ssh.password("user3", "Secret123"), "User should NOT be able to log in!"

Conclusion
---------------

After everything mentioned, **be consistent**. Always take a few minutes to look at the code around you and match
the style and if they're improvements that can be made, please feel free to contact us by creating a bug on
`Github <https://github.com/SSSD/sssd/issues>`_, start a thread in our mailing lists or chat with us on `IRC <https://sssd.io/community.html>`_.
