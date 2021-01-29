.. _unit-tests:

=============
Unit tests
=============

Unit tests typically run a function or a tevent request without running the full deamon. The unit tests in SSSD are developed using either the `check <https://libcheck.github.io/check>`_ library or the `cmocka <https://cmocka.org>`_ library. Cmocka should be used for any new unit tests added to SSSD.

The unit tests are fast to execute and in general this is where corner cases are typically easiest to test as you can provide false or unexpected input to the code under test. Unit tests are also often used to test a library's API.

An important part of many tests using cmocka is wrapping a function provided by an external library using the ``ld`` linker's ``--wrap`` feature. You can learn more about cmocka and this feature in a `lwn.net article the cmocka developers contributed <https://lwn.net/Articles/558106/>`_. In the SSSD source tree, the unit tests reside under ``src/tests/*.c`` (check-based tests) and ``src/tests/cmocka/*.c``.

To run the tests, make sure both the cmocka and check libraries are installed on your system. On Fedora/RHEL, the package names are ``libcmocka-devel`` and ``check-devel``. Running ``make check`` from your build directory will then execute all the unit tests.

Testing for talloc context memory growth
----------------------------------------

Talloc can be a double-edged sword sometimes. On the one hand, talloc greatly simplifies memory management, on the other hand, using talloc creates a risk that a memory related to some operation is allocated using a top-level memory context and outlives the lifetime of the related request. To make sure we catch errors like this, our tests contain several useful functions that record the amount of memory a talloc context takes before an operation begins and compares that amount of memory after the operation finishes. The functions to set up and tear down the memory leak detection are called ``leak_check_setup`` and ``leak_check_teardown.`` Record the amount of memory taken before an operation with ``check_leaks_push`` and then check the amount of memory taken after the operation with ``check_leaks_pop``.

Examples of what can be tested by unit tests
--------------------------------------------

A typical use-case is the sysdb API tests at e.g. ``src/tests/sysdb-tests.c``.

A less typical use-case is testing of the NSS or PAM responders in isolation. The NSS responder test is located at ``src/tests/cmocka/test_nss_srv.c``. Normally, the NSS responder would require a client such as getent to talk to it through the nss_sss module and would send requests to and receive replies from a back end. In unit tests, the NSS client's input is simulatd by calling the ``sss_cmd_execute`` directly, but with mocked input (see e.g. ``mock_input_user_or_group``). The test even fakes communication to the Data Provider by mocking the ``sss_dp_get_account_send`` and ``sss_dp_get_account_recv`` request that normally talks to the Data Provider over D-Bus (see e.g. the ``test_nss_getpwnam_search`` test).
