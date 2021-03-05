GitHub workflow
===============

There are a lots of good git
`tutorials <http://www.kernel.org/pub/software/scm/git/docs/gittutorial.html>`_
on the internet, in this chapter we will focus on some basics related to setting
up git environment, managing changes and generating pull request on GitHub.

Setting up git
--------------
To check out the latest SSSD sources, install git on your system
(Instructions are for Fedora, you may need to use a platform-specific
installation mechanism for other OSes):

.. code-block:: bash

    sudo dnf -y install git

The first time, you will want to configure git with your name and email address
for patch attribution:

.. code-block:: bash

    git config --global user.name "JOHN SMITH"
    git config --global user.email "john.smith@home.com"

Usefull thing is to enable syntax highlighting at the console (for git commands
such as ‘git status’ and ‘git diff’) by setting:

.. code-block:: bash

    git config --global color.ui auto

If you prefer to have graphical tool for handling merge conflicts ``Meld`` may
be a good choice:

.. code-block:: bash

    sudo dnf -y install meld
    git config --global merge.tool meld

You can also setup you favourite code editor to work with git commit:

.. code-block:: bash

    git config --global core.editor vim
    git config --global diff.tool vimdiff


Usefull thing is commit template which speeds up the proces of commit message
crafting. Template is a simple text file which will be used every time after
``git commit`` command will be called:

.. code-block:: bash

    git config commit.template <commit_template_file_path>

Downloading the code
--------------------

To clone upstream SSSD git repository use command:

.. code-block:: bash

    git clone https://github.com/SSSD/sssd.git

This will create a new subdirectory ‘sssd’ in the current directory which will
contain the current master sources. All development should be done first against
the master branch, then backported to one of the stable branches if necessary.

Making changes
--------------

At first fork our GitHub repository. In order to do so, go to the SSSD GitHub
page, log in with your GitHub account and click on the ``Fork`` button.
It will create a fork in your own GitHub account. Once it’s done:

- Clone your own SSSD fork: ``$ git clone git@github.com:<your_username>/sssd.git``

- Add SSSD’s GitHub repo as a remote repo: ``$ git remote add github https://github.com/SSSD/sssd``

Using https:// will ensure you don’t push to SSSD’s GitHub repo by mistake.
Once those two steps are done, you’re good to go and start hacking on your task.
We strongly recommend to do that in local branches!

- Create your local branch: ``$ git checkout -b wip/meaningful_name``

Now it is the time to make changes in the code. There are few options here.
You can have you own idea for contribution to add some new functions to the SSSD.
Or maybe something is broken and you already know how to fix it?
If you run out of ideas always feel free to pick something from pending
`issues <https://github.com/sssd/sssd/issues>`_ list and try to fix it.

Creating a patch
----------------

When working with the code be sure your changes follows our official coding
style rules. Breaking a coding style rules may be reason for patch refuse
upstream even if logic behind the patch changes is correct.

It is a good practice to run spell-checker before code submission. This allows
to avoid most of the misstypes of language errors in the code / messages.
Most of the modern IDEs have spell-checking enabled by default, if not feel
free to use any 3rd party tools (LibreOffice Writter etc.).

- Make your changes and then add any new or modified files to a change-set
  with the command:

.. code-block:: bash

    # Check what files changed
    git status

    # See what changed in file
    git diff <path_do_modified_file>

    # Add modified files and submit change to git tree
    git add <path_to_modified_file>
    git commit

    # Show last patch in git tree
    git show

- Before submitting a patch, always make sure it doesn’t break SSSD tests and
  applies to the latest upstream master branch. You will want to rebase to this
  branch and fix any merge conflicts (in case someone else changed the same code).

.. code-block:: bash

    git remote update
    git rebase -i origin/master

- If this rebase has a merge conflict, you will need to resolve the conflict
  before you continue. When you resolve conflicts in files add add them as
  resolved and continue rebase:

.. code-block:: bash

    git add <path_to_modified_file>
    git rebase --continue

- If you get stuck or make a mistake, you can abort rebase process and come
  back to original commit you did:

.. code-block:: bash

    git rebase --abort

- Patches should be split so that every logical change in the large patchset is
  contained in its own patch. In case you want to add new files to existing commit
  and eventually change commit message:

.. code-block:: bash

    git add <path_to_modified_file>

    # Below can be called standalone if you just want to modify commit message
    git commit --amend

- If you need to make changes to earlier patches in your tree, you can use:

.. code-block:: bash

    git rebase -i origin/master

- Finally you can push patches to your GitHub fork to open Pull Request:

.. code-block:: bash

    git push fork HEAD:my-remote-branch

- If you prefer to send changes via mailing list just create .patch files out of
  specified number (N) of last commits:

.. code-block:: bash

    git format-patch -<N> HEAD


Patch metadata
--------------

The description associated with the patch is an important piece of information
that allows other developers or users to see what the change was about,
what bug did the commit fix or what feature did the commit implement.
To structure the information many SSSD developers use the following format:

- One-line short description

- Blank line

- One or more paragraphs that describe the change if it can’t be described
  fully in the one-line description

- Blank line

- Ticket URL / bugzilla URL / GitHub issue URL

These best practices are loosely based on the
`kernel patch submission recommendation <http://www.kernel.org/doc/Documentation/SubmittingPatches>`_.

An example of a patch formatted according to the above guidelines is commit
`925a14d50edf0e3b800ce659b10b771ae1cde293 <https://github.com/SSSD/sssd/commit/925a14d50edf0e3b800ce659b10b771ae1cde293>`_:

.. code-block:: bash

    LDAP: Fix nesting level comparison

    Correct an issue with nesting level comparison of option
    ldap_group_nesting_level to ensure that setting nesting level 0
    will avoid parent group of group searches.

    Resolves:
    https://github.com/SSSD/sssd/issues/4452

Here, I’d like to add some really basic etiquette rules for opening the pull-request:

- The description of your pull-request must be meaningful.

- The message of your pull-request must briefly describe the reason behind
  this pull-request.

- The message of your pull-request should contain the steps to reproduce the
  issue you’re fixing and/or to reproduce the feature you’re implementing.


Opening Pull Request
--------------------

Now is time to open your pull-request, it just requires few steeps:

- Push the changes to your SSSD repo: ``$ git push origin wip/meaningful_name``

- Open the Pull Request either:

  - by using GitHub’s web UI on your GitHub page

  - by using the hub tool: ``$ hub pull-request``

- Click on [Create pull request]. Now your pull-request has been created
  and will be reviewed by one of the core SSSD developers.

Please, keep in mind that the developers may also be quite busy with their
day-to-day job and it may take some time till someone actually reviews your
pull-request. Sending a “ping”/”bump” is totally fine, but only after a week
or so (in other words, not immediately after the pull-request has been created).

Code review process
-------------------

Once your code is reviewed, a few different things may happen.

Pull request accepted
*********************
Your patch is “Accepted”: it means the patch is good enough to be merged
to SSSD’s repo without any changes.

Chenges requested
*****************
Changes are requested: it means that something has to be changed in your
patch before it gets merged to SSSD’s repo. In this case, you’d like to:

- Carefully read and understand the changes required by the reviewer

- In case you did not understand the required changes, comment in the
  pull-request asking your doubts till you have everything crystal clear
  in your mind. Don’t be afraid to do that, the core developers are around
  to help! :-)

- Please, do not privately ping the developers for all your doubts.
  Discussing in the pull-request is a better and more transparent way to do
  so and also doesn’t interrupt the developer from any other task they are doing.

- Make the changes in your patches

- Squash the changes to the original patches

- Rebase your work on top of SSSD’s git master: ``$ git rebase github/master``
  (We are using linear history so please do not merge your branches, use
  fast-forward approach instead)

- Update the pull-request with the new patchset: ``$ git push -f origin wip/meaningful_name``

- Leave a message in GitHub mentioning that your patchset has been updated

Pull request rejected
*********************
Your patch is rejected: it means that your patch was rejected and the reason
for this will be explained in the pull-request.

In case you do not agree with the reviewer, please, feel free to add
another core developer to the discussion. Usually democracy wins! :-)
