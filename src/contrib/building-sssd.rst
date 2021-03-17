Building SSSD
#############

SSSD is using `autoconf`_ and `automake`_ build systems. If you are not familiar
with these tools, below are the commands you need to execute in order to
configure and build the project.

.. _autoconf: https://www.gnu.org/software/autoconf
.. _automake: https://www.gnu.org/software/automake

.. code-block:: console

    [sssd]$ autoreconf -if
    [sssd]$ ./configure --enable-nsslibdir=/lib64 --enable-pammoddir=/lib64/security --enable-silent-rules
    [sssd]$ make

The ``autoreconf`` command will create a ``configure`` script. This script
allows you to modify the resulting build with several flags, it also makes sure
that all required dependencies are available. SSSD requires lots of build
dependencies that helps us integrate with the identity and authentication
systems. Your system may not have all necessary dependencies installed. In such
case, the ``configure`` script will end up with error that will tell you what is
missing. Re-run the script after you install the dependency.

.. note::

    Run ``./configure --help`` to list all available ``configure`` options.

Some distributions provide a way to quickly install a package's build
dependencies with a single command. If your distributions supports it, you can
install them all at once with:

.. code-tabs::

    .. fedora-tab::

        dnf builddep sssd

    .. ubuntu-tab::

        apt-get build-dep sssd

There are additional `make` targets available, such as `rpms` or
`prerelease-rpms` that you may find useful.

.. code-block:: bash

    # Build RPM packages
    make rpms

    # Build RPM packages with prerelease version tag (date and git hash)
    make prerelease-rpms

Development scripts
===================

SSSD provide a set of helper aliases and scripts to simplify building of
developments versions. These scripts are currently only available for Fedora.
You can start using them by sourcing the `bashrc_sssd`.

.. code-block:: console

    [sssd]$ source ./contrib/fedora/bashrc_sssd

.. note::

    If you plan to work on SSSD regularly, you may want to include the script
    in your `~/.bashrc` file:

    .. code-block:: bash

        if [ -f /path/to/sssd-source/contrib/fedora/bashrc_sssd ]; then
            . /path/to/sssd-source/contrib/fedora/bashrc_sssd
        fi

Usage
*****

* Produce a debug build of SSSD and run unit tests (run from git root
  directory):

.. code-block:: console

    [sssd]$ reconfig && chmake

* Install fresh build of SSSD into the system (this operation assumes that user
  has "sudo" privilege). To install SSSD "sssinstall" alias is used:

.. code-block:: console

    [sssd]$ sssinstall && echo "Build install successful"
