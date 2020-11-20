.. highlight:: none

LDAP provider integration tests
===============================

Related tickets:

-  `#2541 <https://pagure.io/SSSD/sssd/issue/2541>`__
-  `#2545 <https://pagure.io/SSSD/sssd/issue/2545>`__

Problem statement
-----------------

We'd like to run some sssd/LDAP integration tests during day-to-day
development. They should be low-overhead, completing in under 5 minutes,
and run as part of "make check" and "contrib/ci/run", under a
non-privileged user. They may require special configure options to be
executable, and be skipped if the options are not provided.

Use cases
---------

A developer modifies a part of LDAP-involved data path and wishes to
quickly check sanity of the change. He/she then runs "make check" or
"contrib/ci/run", which include the LDAP integration tests.

A developer submits a change (possibly) affecting the LDAP-involved data
paths and a reviewer wishes to check the sanity of the change before
ACK'ing it. The reviewer then requests a CI job run, which includes the
LDAP integration tests.

Overview of the solution
------------------------

The suite should use pytest test framework.

Tests are executed as part of "make check", which is also included into
"contrib/ci/run". As our Makefiles use Automake's parallel test
execution harness and sssd data and socket directories are compiled-in
currently and cannot be shared, there can only be one Automake-level
integration test suite. Any possible parallelization should be
implemented within.

Because "make check" and "contrib/ci/run" are supposed to be executable
in largely arbitrary environments and under regular users, the sssd
needs to be tricked into believing it is running under a root account
and tests need to be tricked into using libnss\_sss and pam\_sss from
the build instead of the NSS and PAM services specified for the system.
The first two can be done with the help of "cwrap" wrappers. The latter
would require cwrap support for the PAM library, which isn't implemented
yet, but might be in the future. As of now, only libnss\_sss can be
tested.

Because default, compiled-in sssd data and socket locations are not
accessible to regular users, and there is currently no way to change
them after the build, running the tests will require configuring the
build with user-writeable locations. Otherwise the tests will be skipped
during the "make check" run and Automake will report them as such. It is
possible that in the future a way to change them after the build will be
implemented and this requirement will be lifted.

Implementation details
----------------------

All tests are invoked with src/tests/cwrap/cwrap\_test\_setup.sh sourced
into the shell, which sets up NSS and UID wrappers to make tests assume
they're running under root and use libnss\_sss from the build tree.

At the moment, running the tests requires configuring the build to have
data and sockets located in user-writeable directories. The specific
locations might be communicated to the test suite via a
configure-generated Python or Bash module, or a C program outputting
them when invoked. If at least one of these locations is non-writeable,
the test suite will exit to Automake with code 77, indicating SKIPPED
status.

However, a way to change these at startup time might be implemented
later, removing this requirement. E.g. data and socket directories might
be specified in the configuration file for the sssd daemons, and the
socket location might be specified to libnss\_sss and pam\_sss via an
environment variable. See
`#2545 <https://pagure.io/SSSD/sssd/issue/2545>`__.

The OpenLDAP server can be executed with configuration and databases
located under arbitrary (temporary) directories which will be created
during testing. It is unknown yet how to make 389-ds do the same.

The communication with the LDAP server can be left unencrypted at least
for the start, simplifying setup and debugging.

The LDAP server setup/teardown (for either of the servers) will be done
in Bash to simplify initial development and later possibly converted to
(a bit more robust) Python, when all the details are clear. The
setup/teardown scripts will be executed from a pytest fixture
setup/teardown.

The pytest suite will do further setup itself according to specific test
requirements, including: directory population/cleanup, generating sssd
configuration, starting/stopping sssd.

The tests themselves might include listing/retrieving rfc2307(bis) user
and group information, including nested groups, perhaps using the
standard "pwd" and "grp" modules. Some of the tests that can be
implemented initially follow, most useful first.

Sanity
~~~~~~

::

    Fixture rfc2307:
        enumerate = true / false
        ldap_schema = rfc2307
        3 users
        3 user groups
        1 empty group
        1 two-user group

    Fixture rfc2307bis:
        Fixture rfc2307
        ldap_schema = rfc2307bis
        1 group with empty group inside
        1 group with two empty groups inside
        1 group with a single-user group inside
        1 group with a two-user group inside
        1 group with two single-user groups inside
        A basic group membership loop: A->B->A
        A branched group membership loop: A->B, A->D, A->C->A

    Tests:
        List all users/groups with pwd.getpwall/grall()
        Retrieve a user/group by UID/GID with pwd.getpwuid/grgid()
        Retrieve a non-existent user/group by UID/GID with pwd.getpwuid/grgid()
        Retrieve a user/group by name with pwd.getpwnam/grnam()
        Retrieve a non-existent user/group by name with pwd.getpwnam/grnam()

Cache
~~~~~

 ::

    Fixture:
        enumerate = true / false
        enum_cache_timeout = 4s
        ldap_enumeration_refresh_timeout = 0
        3 users
        3 user groups

    Tests:
        Cache refresh
        1. Enumerate users/groups with pwd.getpwall/grall()
        2. Within enum_cache_timeout:
            2.1 Add/remove user/group
            2.2 Enumerate users/groups with pwd.getpwall/grall(),
                check for change absence
        3. After enum_cache_timeout passed from step 1:
           enumerate users/groups with pwd.getpwall/grall(), check for change
        No-wait percentage
        ...
        Negative timeout
        ...

Filter users/groups
~~~~~~~~~~~~~~~~~~~

 ::

    Fixture:
        3 users
        3 user groups
        filter_users/groups: none/one/two

    Tests:
        Enumerate users/groups with pwd.getpwall/grall()
        Retrieve a filtered user/group by UID/GID with pwd.getpwuid/grgid()
        Retrieve a non-filtered user/group by UID/GID with pwd.getpwuid/grgid()

Override homedir
~~~~~~~~~~~~~~~~

 ::

    Fixture:
        1 user with homedir A
        1 user without homedir
        override_homedir = B

    Tests:
        Retrieve the users with pwd.getpwuid/nam/all()

Fallback homedir
~~~~~~~~~~~~~~~~

 ::

    Fixture:
        1 user with homedir A
        1 user without homedir
        fallback_homedir = B

    Tests:
        Retrieve the users using pwd.getpwuid/nam/all()

Override shell
~~~~~~~~~~~~~~

 ::

    Fixture:
        1 user with shell A
        1 user without shell
        override_shell = B

    Tests:
        Retrieve the users using pwd.getpwuid/nam/all()

Vetoed shells / shell fallback
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 ::

    Fixture:
        1 user with shell A
        1 user with shell B
        1 user without shell
        override_shell = C

    Tests:
        Retrieve the users using pwd.getpwuid/nam/all()

Default shell
~~~~~~~~~~~~~

 ::

    Fixture:
        1 user with shell A
        1 user without shell
        default_shell = B

    Tests:
        Retrieve the users using pwd.getpwuid/nam/all()

Configuration changes
---------------------

Sssd, libnss\_sss and pam\_sss might require changes allowing
configuration of data and socket locations.

Authors
-------

Nikolai Kondrashov with help from Martin Kosek, Jakub Hrozek, Lukas
Slebodnik and Simo Sorce.
