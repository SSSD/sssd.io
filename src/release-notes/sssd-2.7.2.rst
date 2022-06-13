SSSD 2.7.2 Release Notes
========================

Highlights
----------

Important fixes
~~~~~~~~~~~~~~~

* A serious regression introduced in ``sssd-2.7.1`` that prevented successful authentication of IPA users was fixed.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* Default value of ``pac_check`` changed to ``check_upn, check_upn_dns_info_ex`` (for AD and IPA provider).

Tickets Fixed
-------------

- `#5868 <https://github.com/SSSD/sssd/issues/5868>`__ - Harden kerberos ticket validation
- `#6055 <https://github.com/SSSD/sssd/issues/6055>`__ - Unable to lookup AD user if the AD group contains '@' symbol


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.7.1..2.7.2

    Anuj Borah (1):
        dbb9d62be  Tests: port proxy_provider/misc

    Iker Pedrosa (1):
        eb4a2f3a3  Revert "CI: flake8 move target to pull_request_target"

    Jakub Vavra (1):
        56a158779  Tests: Set FIPS:AD-SUPPORT crypto-policy for AD integration

    Pavel Březina (1):
        ef79966be  Release sssd-2.7.2

    Steeve Goveas (2):
        5f3878052  TEST: Fix the indentation in doctrings
        3fc660492  TEST: Update to search the start string for hostname

    Sumit Bose (2):
        26d8601e9  pac: relax default for pac_check option
        536dc9e4f  names: only check sub-domains for regex match
