SSSD 2.8.1 Release Notes
========================

Highlights
----------

Important fixes
~~~~~~~~~~~~~~~

* A regression when running sss_cache when no SSSD domain is enabled would produce a syslog critical message was fixed.

Tickets Fixed
-------------

* `#6360 <https://github.com/SSSD/sssd/issues/6360>`__ - [D-Bus] ``ListByName()`` returns several times the same entry
* `#6361 <https://github.com/SSSD/sssd/issues/6361>`__ - [D-Bus] ``ListByName()`` fails when not using wildcards
* `#6387 <https://github.com/SSSD/sssd/issues/6387>`__ - Fatal errors in log during Anaconda installation: "CRIT sss_cache:No domains configured, fatal error!"
* `#6398 <https://github.com/SSSD/sssd/issues/6398>`__ - [D-Bus] ``Groups.ListByName()`` and ``Groups.ListByDomainAndName()`` not working


Detailed Changelog
------------------

.. code-block:: release-notes-shortlog

    $ git shortlog --pretty=format:"%h  %s" -w0,4 2.8.0..2.8.1

    Alejandro López (8):
        6d7f1fba2  CACHE_REQ: Do not use timestamp optimization on "files" provider.
        129979a38  Cache: String has to be duplicated instead of copied
        1377bca97  CACHE_REQ: Initialize domain with NULL
        1562df030  CACHE_REQ: Do not return duplicated values.
        82c69b7f6  TESTS: Correct ListByAttr()'s test
        13e841de7  CACHE_REQ: Consider the domain when looking names in the cache
        7f583fad9  TESTS: New test for D-Bus' ListByName()
        0f670188c  CACHE_REQ: Use a const struct in cache_req_data_create()

    Alexey Tikhonov (3):
        e6f94e252  IPA: "trusted user not found" isn't an error
        cfaa06b0e  CFG RULES: allow 'fallback_to_nss' option
        e0026e38c  SYSDB: pre-existence of MPG group in the cache isn't an error

    Justin Stephenson (2):
        587fe9682  CI: Build srpm fix for illegal version tag '-'
        c61e10987  Analyzer: Optimize list verbose output

    Pavel Březina (10):
        a6d521458  confdb: avoid syslog message when no domains are enabled
        1df029470  monitor: read all enabled domains in add_implicit_services
        a6312c46d  sss_cache: use ERR_NO_DOMAIN_ENABLED instead of ENOENT
        ab7cbb5f0  confdb: chande debug level when no domain are found in confdb_get_domains
        7bf97190e  ci: enable ci for sssd-2-8 branch
        40ccfd6c7  ci: switch to actions/checkout@v3
        9aee8164e  ci: use GITHUB_OUTPUT instead of set-output
        a7853d51c  ci: switch to actions/upload-artifact@v3
        59973c0b8  pot: update translations
        a18ef88ed  Release sssd-2.8.1

    Shridhar Gadekar (1):
        59685cff0  Tests: GSSAPI ssh login failing due to a missing directive

    aborah-sudo (1):
        62276737f  Tests: port proxy_provider/rfc2307

    김인수 (1):
        cfa112948  po: update translations
