Blank Feature Template
======================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/XYZ

Problem statement
-----------------
Short overview (up to a couple of sentences) of the change being
designed. Might include pointers to reference materials (such as MSDN
articles when designing an AD integration feature) or other information
required to understand what the change is about.

Use cases
---------
Walk through one or more full examples of how the feature will be used. If
this is an internal change only (refactoring, perhaps), include a sentence
saying so.

Overview of the solution
------------------------
Describe, without going too low into technical details, what changes need to
happen in SSSD during implementation of this feature. This section should
be understood by a person with understanding of how SSSD works internally
but doesn't have an in-depth understanding of the code. For example, it's
fine to say that we implement a new option foo with a default value bar,
but don't talk about how is foo processed internally and which structure
stores the value of foo. In some cases (internal APIs, refactoring,
...) this section might blend with the next one.

Implementation details
----------------------
A more technical extension of the previous section. Might include low-level
details, such as C structures, function synopsis etc. In case of very
trivial features (e.g. a new option), this section can be merged with the
previous one.

Configuration changes
---------------------
Does your feature involve changes to configuration, like new options or
options changing values? Summarize them here. There's no need to go into
too many details, that's what man pages are for.

How To Test
-----------
This section should explain to a person with admin-level of SSSD
understanding how this change affects run time behaviour of SSSD and how
can an SSSD user test this change. If the feature is internal-only, please
list what areas of SSSD are affected so that testers know where to focus.

How To Debug
------------
Explain how to debug this feature if something goes wrong. This section
might include examples of additional commands the user might run (such as
keytab or certificate sanity checks) or explain what message to look for.

Authors
-------
Give credit to authors of the design in this section.
