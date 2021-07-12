SSSD 2.5.2 Release Notes
========================

Highlights
----------

General information
~~~~~~~~~~~~~~~~~~~

* ``originalADgidNumber`` attribute in the SSSD cache is now indexed

New features
~~~~~~~~~~~~

* Debug messages in data provider include a unique request ID that can be used
  to track the request from its start to its end
  (requires ``libtevent`` >= 0.11.0)

Important fixes
~~~~~~~~~~~~~~~

* Update large files in the files provider in batches to avoid timeouts

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

* Add new config option ``fallback_to_nss``

Tickets Fixed
-------------

- `#4255 <https://github.com/SSSD/sssd/issues/4255>`_ - sssd still showing ipa user after removed from last group
- `#5430 <https://github.com/SSSD/sssd/issues/5430>`_ - Missing search index for ``originalADgidNumber``
- `#5557 <https://github.com/SSSD/sssd/issues/5557>`_ - files_provider: long "blocking" ``sf_enum_files()`` can overrun internal WD timeouts and trigger process restart
- `#5577 <https://github.com/SSSD/sssd/issues/5577>`_ - SSSD Error Msg Improvement: Bad address
- `#5578 <https://github.com/SSSD/sssd/issues/5578>`_ - SSSD Error Msg Improvement: Invalid argument
- `#5649 <https://github.com/SSSD/sssd/issues/5649>`_ - Dead twitter account
- `#5697 <https://github.com/SSSD/sssd/issues/5697>`_ - sss_cache - clarify intended use and limitations

Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.5.1..2.5.2

    Alexey Tikhonov (7):
        c6cd2fe3f  krb5_child: reduce log severity in sss_send_pac() in case PAC responder isn't running.
        0eccee188  secrets: reduce log severity in local_db_create() in case entry already exists since this is expected during normal oprations.
        624e3fe75  KCM: use SSSDBG_MINOR_FAILURE for ERR_KCM_OP_NOT_IMPLEMENTED
        0646917cd  KCM: reduce log severity in sec_get() in case entry not found
        8dba74769  DEBUG: don't reset debug_timestamps/microseconds to DEFAULT in `_sss_debug_init()`.
        71301ccf8  KCM: removed unneeded assignment
        2ebf463fc  CACHE_REQ: fixed covscan issues

    Dan Lavu (2):
        9d576e47e  tests: Adding multihost test for supporting asymmetric nsupdate auth
        ff3f85705  tests: Adding tests to cover ad discovery improvements using cldap

    Deepak Das (2):
        89a40e77a  SSSD Log: invalid_argument msg mod
        7646ac958  SSSD Log: log_bad_address_msg_mod

    Iker Pedrosa (1):
        865330c65  cache_req: parse name to get shortname

    Jakub Vavra (1):
        daad83876  Tests: Add test_innetgr_threads

    Justin Stephenson (2):
        2a3fb3bdb  KCM: Unset _SSS_LOOPS
        ac0c0b000  KCM: Drop unnecessary c-ares linking

    Pavel Březina (8):
        dbd50453b  Update version in version.m4 to track the next release
        4e3e87270  tests: fix pep8 issues
        a6e5d53a3  kcm: terminate client on bad message
        b85984a36  multihost: fix whitespace issues
        75c204ff1  multihost: fix pep8 issues
        f02ac230b  debug: add support for tevent chain id
        881a1a412  debug: enable chain id in backend
        57ac58092  pot: update pot files

    Paweł Poławski (2):
        68ed4d4a2  README: Dead social media link remove
        17e339d58  SYSDB: Add search index "originalADgidNumber"

    Shridhar Gadekar (1):
        5feeb8ac9  Test: sudo rule with runAS set to short-username value

    Sofia Nieves (1):
        e373408a2  Replacing freenode with libera

    Sumit Bose (6):
        b9e60ae06  man: clarify effects of sss_cache on the memory cache
        5288ddaa2  files: split update into batches
        0fbd67404  files: add new option fallback_to_nss
        dd1aa5795  files: delay refresh and not run in parallel
        19b850636  files: queue certmap requests if a refresh is running
        b4ee698ac  cache_req: do not return cached data if domain is inconsistent

    Weblate (1):
        161ff0e88  po: update translations

    Yuri Chornoivan (1):
        b04742485  Fix minor typos in docs
