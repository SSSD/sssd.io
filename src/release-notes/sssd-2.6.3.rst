SSSD 2.6.3 Release Notes
========================

Highlights
----------

Important fixes
~~~~~~~~~~~~~~~

* A regression introduced in sssd-2.6.2 in the IPA provider that prevented users from login was fixed. Access control always denied access because the selinux_child returned an unexpected reply.
* A critical regression that prevented authentication of users via AD and IPA providers was fixed. LDAP port was reused for Kerberos communication and this provider would send incomprehensible information to this port.
* When authenticating AD users, backtrace was triggered even though everything was working correctly. This was caused by a search in the global catalog. Servers from the global catalog are filtered out of the list before writing the KDC info file. With this fix, SSSD does not attempt to write to the KDC info file when performing a GC lookup.

Tickets Fixed
-------------

- `#5926 <https://github.com/SSSD/sssd/issues/5926>`__ - AD Domain in the AD Forest Missing after sssd latest update
- `#5938 <https://github.com/SSSD/sssd/issues/5938>`__ - sdap_idmap.c/sssd_idmap.c incorrectly calculates rangesize from upper/lower
- `#5939 <https://github.com/SSSD/sssd/issues/5939>`__ - Regression on rawhide with ssh auth using password
- `#5947 <https://github.com/SSSD/sssd/issues/5947>`__ - sssd-ad broken in 2.6.2, 389 used as kerberos port
- `#5956 <https://github.com/SSSD/sssd/issues/5956>`__ - sssd error triggers backtrace : [write_krb5info_file_from_fo_server]

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.6.2..2.6.3

    Alexey Tikhonov (4):
        104f513c4  IPA: get_object_from_cache(): don't touch output arg `_msg` in case object wasn't found (i.e. ENOENT returned)
        e9a25bb0b  IPA: get_object_from_cache(): - reduce log level in case object wasn't found in cache - slightly reduce code duplication
        28af1752a  Removed unused file.
        868f38742  RESPONDER: reduce log level in case files provider in inconsistent state falls back to NSS.

    Anuj Borah (5):
        9ba593e9a  Tests: Fix python-alltests-tier1-2
        b6929c44d  Tests: Fix python-alltests-tier1-2 Add local users
        7e9269412  Tests: Fix yum repoquery --recommends sssd-tools test
        237b99b87  Tests: Fix setup_ipa_client fixture
        4e3385c90  Tests: RFE pass KRB5CCNAME to pam_authenticate environment if available

    Dan Lavu (1):
        244c9f66d  Adding pytest multiforest tests

    Dhairya Parmar (2):
        14c5da6f5  localuser changed to user on line 59
        cf5270a98  indentation of ssh.close() on line 66 corrected

    Iker Pedrosa (1):
        ca8cef0fc  krb5: AD and IPA don't change Kerberos port

    Jakub Vavra (2):
        d5467ad70  Tests: Update AD ssh password change test.
        4897c2874  Tests: Add a test for BZ2004406

    Justin Stephenson (2):
        b76436f88  TESTS: Restrict smartcard in sc auth tests
        e03a2deaf  P11: Increase array size of extra_args

    Madhuri Upadhye (1):
        a8c2e3993  Check default debug level of sssd and corresponding logs

    Pavel Březina (2):
        e58b14afb  pot: update pot files
        2de075879  Release sssd-2.6.3

    Shridhar Gadekar (1):
        58b3233f0  Tests: Health and Support Analyzer - Add request log parsing utility

    Steeve Goveas (1):
        d3424c027  prepend 'r' raw to avoid deprecation errors

    Sumit Bose (3):
        5a2e0ebe8  ipa: fix reply socket of selinux_child
        bf6059eb5  ad: add required 'cn' attribute to subdomain object
        42a3f8fe8  man: clarify ldap_idmap_range_max

    Tomas Halman (1):
        2b0bd0b30  ad: do not write kdc info file for GC lookup

    Weblate (2):
        e7069c532  po: update translations
        d8f558c28  po: update translations
