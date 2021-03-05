Getting the source
==================

For the SSSD project, we use the Git source control system.
Hosted on `GitHub <https://github.com/sssd/sssd>`_ are the
`documentation <https://sssd.io>`_, the
`issue tracker <https://github.com/sssd/sssd/issues>`_ tracker,
and the referential repository:

.. code-block:: bash

    https://github.com/SSSD/sssd

The preferred way for sending patches is to create pull requests on GitHub.
You can also e-mail your patch as an attachment to the
`sssd-devel <https://sssd.io/docs/developers/contribute.html#contribute>`_
mailing list.

Setting up an environment for development
-----------------------------------------

Development of SSSD can be done on any Linux - based machine.
If you do not want to install development related packages on your host
virtual machine based setup is the right way to go.

There are several ways to do so, but the one recommended by the author
of this document is by simply using the
`SSSD Test Suite <https://github.com/SSSD/sssd-test-suite>`_.

Just check out the project’s
`readme <https://github.com/SSSD/sssd-test-suite/blob/master/readme.md>`_
on the GitHub for setup details.
