.. highlight:: none

Improve config validation
=========================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2247 <https://pagure.io/SSSD/sssd/issue/2247>`__
-  `https://pagure.io/SSSD/sssd/issue/2028 <https://pagure.io/SSSD/sssd/issue/2028>`__
-  `https://pagure.io/SSSD/sssd/issue/1308 <https://pagure.io/SSSD/sssd/issue/1308>`__
-  `https://pagure.io/SSSD/sssd/issue/2249 <https://pagure.io/SSSD/sssd/issue/2249>`__
-  `https://pagure.io/SSSD/sssd/issue/2269 <https://pagure.io/SSSD/sssd/issue/2269>`__
-  `https://pagure.io/SSSD/sssd/issue/2465 <https://pagure.io/SSSD/sssd/issue/2465>`__
-  `https://pagure.io/SSSD/sssd/issue/2687 <https://pagure.io/SSSD/sssd/issue/2687>`__
-  ...and more

Problem statement
-----------------

Admins should be notified if their configuration is not valid Admins
should have an option to still log in to the system if they do an error
in configuration

Use cases
---------

-  Fallback config

   -  With responders, we can use defaults, they are usually paranoid
      enough
   -  With domains, we probably can only fall back to last known good
      (except local domain)
   -  Could we start only responders so that if cached data is
      available, the responders can be used?

-  Last known good (First known good)

   -  For domains
   -  Use-case: admin changes something and wants to still log in

-  Config merging

   -  Deprecate "services" line
   -  Be able to drop domain into /etc/sssd/sssd.conf.d/

-  Config validation

   -  prerequisite: have a common definition of options and autogenerate
      the rest

      -  Autogenerate dp\_opts, man pages and configAPI sources from a
         common location
      -  Look at Samba

   -  ...for that we need to use dp\_opts everywhere

To do
-----

-  Does ding-libs support config validation?

Overview of the solution
------------------------

Describe, without going too low into technical details, what changes
need to happen in SSSD during implementation of this feature. This
section should be understood by a person with understanding of how SSSD
works internally but doesn't have an in-depth understanding of the code.
For example, it's fine to say that we implement a new option ``foo``
with a default value ``bar``, but don't talk about how is ``foo``
processed internally and which structure stores the value of \`foo. In
some cases (internal APIs, refactoring, ...) this section might blend
with the next one.

Implementation details
----------------------

A more technical extension of the previous section. Might include
low-level details, such as C structures, function synopsis etc. In case
of very trivial features (e.g. a new option), this section can be merged
with the previous one.

Configuration changes
---------------------

Does your feature involve changes to configuration, like new options or
options changing values? Summarize them here. There's no need to go into
too many details, that's what man pages are for.

How To Test
-----------

This section should explain to a person with admin-level of SSSD
understanding how this change affects run time behaviour of SSSD and how
can an SSSD user test this change. If the feature is internal-only,
please list what areas of SSSD are affected so that testers know where
to focus.
