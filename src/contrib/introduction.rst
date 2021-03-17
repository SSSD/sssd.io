Introduction to the SSSD development
####################################

Thank you for your interest in contributing to the SSSD project. The development
is happening on the `SSSD GitHub project`_ using the `git`_ version control
system and `GitHub workflow`_. SSSD is a large complex project with many
dependencies. Feel free to reach us on our `community channels`_ to ask for
help.

.. _SSSD GitHub project: https://github.com/SSSD/sssd
.. _GitHub workflow: https://guides.github.com/introduction/git-handbook
.. _git: https://git-scm.com
.. _community channels: ../community

.. seealso::

    Check out also other `GitHub Guides <https://guides.github.com>`_ if you are
    not familiar with GitHub.

Contribution Quick Start
========================

There are plenty of guides available to get you started with git and GitHub
workflow if you are not yet familiar with these, therefore we don't go into
details here. As an example, we suggest reading the `Git Handbook`_ on GitHub.
The following steps describe the process in a nut shell to provide you a basic
template:

.. _Git Handbook: https://guides.github.com/introduction/git-handbook

#. Get familiar with the :doc:`coding-style`
#. Create an account on `GitHub <https://github.com>`_
#. Fork `SSSD repository <https://github.com/SSSD/sssd>`_
#. Clone the SSSD repository
#. Add your fork as an extra remote
#. Setup an SSSD `commit template`_
#. Create a working branch
#. Commit changes
#. Push your changes to your GitHub repository
#. Open a Pull Request against SSSD project (using ``gh``, ``hub`` or web ui)
#. Await our review

.. _commit template: https://github.com/SSSD/sssd/blob/master/.git-commit-template

.. code-block:: console

    [.]$ git clone git@github.com:SSSD/sssd.git
    [.]$ cd sssd
    [sssd]$ git remote add $ghusername git@github.com:$ghusername/sssd.git
    [sssd]$ git config commit.template .git-commit-template
    [sssd]$ git checkout -b my-changes
    [sssd]$ vim change-what-you-need
    [sssd]$ git commit
    [sssd]$ git push $ghusername my-changes --force
    [sssd]$ gh pr create

Additionally, make sure to setup your name contact e-mail that you want to use
for the SSSD development. Run the following commands from the local repository
location:

.. code-block:: console

    [sssd]$ git config user.name "John Smith"
    [sssd]$ git config user.email "john.smith@home.com"

.. note::
    This will setup the user information only for the SSSD repository. You can
    also add ``--global`` switch to the ``git config`` command to setup these
    options globally and thus making them available in every git repository.

.. seealso::

    There are also several SSSD's side projects that you can contribute into.
    Some of these projects can help you with testing and debugging your code so
    we advice you to look at them. Navigate to the `SSSD organization`_ on
    GitHub to see all our projects. The policies, coding style and workflows for
    contributions are the same.

    :tag:`strong` You can also directly contribute to this documentation by
    opening pull requests against `sssd.io <https://github.com/SSSD/sssd.io>`_
    repository. :end-tag:`strong`

.. _SSSD organization: https://github.com/SSSD

Tasks for newcomers
===================

Feel free to pick up any existing ticket from the `issue tracker`_. We try to
mark tickets that don’t require too much existing knowledge with the ``Easy to
fix`` keyword. You can list those tickets with the following `query`_.

.. _issue tracker: https://github.com/sssd/sssd/issues
.. _query: https://github.com/SSSD/sssd/issues?q=is%3Aopen+is%3Aissue+label%3A%22Easy+to+fix%22

Licensing
=========

All source code committed to the SSSD is assumed to be made available under
the GPLv3+ license unless the submitter specifies another license at that time.
The upstream SSSD maintainers reserve the right to refuse a submission
if the license is deemed incompatible with the goals of the project.
