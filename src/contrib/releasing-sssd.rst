Releasing SSSD
##############

This is a step by step guide for core developers on releasing a new SSSD
version.

#. Find all `opened Weblate pull requests <https://github.com/SSSD/sssd/pulls?q=is%3Apr+is%3Aopen+weblate>`__ (translations)

   #. Make sure SSSD builds (PR CI build job), sometimes new translations introduce errors
   #. If not, fix the translations at
      https://translate.fedoraproject.org/projects/sssd
   #. Merge them

#. If this is a new major release, make sure the master branch PR CI is green
   and create a branch sssd-X-Y (e.g. sssd-2-12) and push it to SSSD repository.
   If this is a minor release and the branch already exist, make sure PR CI is
   green.
#. Go to https://github.com/SSSD/sssd/actions/workflows/release.yml
#. Click on "Run workflow" and provide parameters:

   * Target branch to release from: sssd-X-Y, e.g. sssd-2-12
   * Release version: X.Y.Z, e.g. 2.12.6
   * Previous version: X.Y.Z-1, e.g. 2.12.5

The workflow will create a new GitHub draft release and a pull request with
release notes at sssd.io repository. Review, edit and merge the release notes,
then publish the release on GitHub.

Packit will automatically create pull requests against active Fedora versions in
Fedora sources. When the pull request is pushed, packit automatically creates
koji build and bodhi update.

.. note::

    We generate large release notes between two major releases to avoid issues,
    since the new release branch and old release branch diverged. If the last
    release is 2.12.6 and you are releasing a new major release 2.13.0 provide
    2.12.0 as the previous version. Release notes will be generated between
    ``2.12.0..2.13.0``.
