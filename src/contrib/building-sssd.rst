Building SSSD
=============

Starting with SSSD 1.10 beta, we now include a set of helper aliases and
environment variables in SSSD to simplify building development versions of
SSSD on Fedora. To take advantage of them, use the following command:

.. code-block:: bash

    . /path/to/sssd-source/contrib/fedora/bashrc_sssd

To build SSSD from source, follow these steps:

- Install necessary tools:

.. code-block:: bash

    # When using yum
    sudo yum -y install rpm-build yum-utils libldb-devel

    # When using dnf
    sudo dnf -y install rpm-build dnf-plugins-core libldb-devel

- Create source rpm (run from git root directory):

.. code-block:: bash

    contrib/fedora/make_srpm.sh

- Install SSSD dependencies:

.. code-block:: bash

    # When using yum
    sudo yum-builddep rpmbuild/SRPMS/sssd-*.src.rpm

    # When using dnf
    sudo dnf builddep rpmbuild/SRPMS/sssd-*.src.rpm

In rare cases SSSD dependencies packages may exist in system repository under
different name. Sometimes additional repository needs to be added to the system
for full SSSD dependencies resolution. In those rare cases autoconf script
output will suggest package name developer should search for.

Sidenote: If you plan on working with the SSSD source often, you may want to
add the following to your ~/.bashrc file:

.. code-block:: bash

    if [ -f /path/to/sssd-source/contrib/fedora/bashrc_sssd ]; then
        . /path/to/sssd-source/contrib/fedora/bashrc_sssd
    fi

- Produce a Debug build of SSSD (run from git root directory):

.. code-block:: bash

    reconfig && chmake

- Install fresh build of SSSD into the system (this operation assumes that user
  has "sudo" privilege). To install SSSD "sssinstall" alias is used:

.. code-block:: bash

    sssinstall && echo "Build install successful"

Installation on other distributions is possible via standard autotools combo:

.. code-block:: bash

    autoreconf -i -f
    ./configure --enable-nsslibdir=/lib64 --enable-pammoddir=/lib64/security
    make
    sudo make install

Sidenote: By default autotools install prefix is "/usr/local". Default location
for "nsslibdir" and "pammoddir" will be "/usr/local/lib64".
32bit machines will search for SSSD libraries by default in "/usr/local/lib"
which will result in broken NSS and PAM linking with SSSD. Advice here is to
double check if SSSD install location will be visible for system linker.

- Build RPM packages out of fresh build if needed

.. code-block:: bash

    make rpms

    # For generating prerelease RPMs with date and git hash in package release
    # we prepared special make target:
    make prerelease-rpms
