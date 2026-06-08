Releasing SSSD
##############

This guide outlines the steps for releasing a new SSSD version.

Pre-Release Steps
*****************

1. **Handle Translation PRs**

   * Check all open Weblate pull requests on GitHub
   * Make sure SSSD builds (PR CI build job)
   * If the build fails, fix translations at https://translate.fedoraproject.org/projects/sssd
   * Merge approved PRs

2. **Verify Branch Status**

   * For **major releases from master**: Verify master branch CI is green
   * For **minor/patch releases**: Confirm the existing stable branch
     (`sssd-X-Y`) has green CI

.. warning::

    For major releases, the stable branch `sssd-X-Y` will be created
    automatically by the release workflow. Do NOT create it manually beforehand.

Release Execution
*****************

3. **Trigger Release Workflow**

   * Navigate to https://github.com/SSSD/sssd/actions/workflows/release.yml
   * Click "Run workflow" and configure:

     * **Target branch to release from**:

       * `master` for major releases (e.g., 2.10.0)
       * `sssd-X-Y` for minor/patch releases (e.g., sssd-2-13)

     * **Release version**: `X.Y.Z` format (e.g., `2.13.1`)
     * **Create stable branch**: (optional, default: `auto`)

       * `auto` - Creates stable branch automatically when releasing from master
       * `no` - Skip branch creation (useful for pre-releases like beta/rc)

4. **Finalize Release**

   * Review the draft GitHub release
   * Review the release notes PR at sssd.io
   * Edit both as needed
   * Merge the sssd.io PR with the release notes
   * Publish the GitHub release

.. note::

    The workflow automatically:

    * Computes the previous version for release notes generation
    * Creates and signs the release tag
    * Builds and signs the tarball (with GPG and SHA256)
    * Generates release notes from commit history
    * Pushes the tag to GitHub
    * For master releases (when `create_stable_branch=auto`):

      * Creates the `sssd-X-Y` stable branch from the release tag
      * Creates the `backport-to-sssd-X-Y` GitHub label for backport tracking

    * Creates a draft GitHub release with artifacts
    * Opens a PR to sssd.io with generated release notes

    The workflow automatically computes the previous version (for release notes
    generation):

    * For X.Y.Z releases (Z>0): uses X.Y.(Z-1)
    * For X.Y.0 releases (Y>0): uses X.(Y-1).0
    * For X.0.0 releases: finds the latest stable tag via git history

Post-Release
************

Packit automatically creates pull requests for active Fedora versions,
triggering koji builds and bodhi updates after the pull request is merged.
