Writing a Design Page
#####################

A design page is a document that describes how a new feature is going to be
implemented. However, the purpose of the design is not to document the feature
itself (we have other channels for that) but rather to document the decision
process behind the final solution. That means, if multiple solutions were
considered, the design page should describe why the final solution was selected
and not the others.

.. note::

    **Writing a design page on a complex feature or change is very beneficial to
    you, the author of these changes.** SSSD, identity management and Linux is a
    huge world and it is not possible to know, anticipate and understand
    everything. Sharing a design page with multiple people before writing the
    code can give you valuable feedback that helps you to avoid errors and
    reinventing the wheel since the reviewers can point you to an existing API
    and catch corner cases that you were not aware of.

Before you start writing a design page, **think about the audience**. It is
important to know the expected audience so you know how thorough you have to be
in your explanations. For SSSD project, we can assume that the audience are
SSSD developers and people that are more or less familiar with SSSD and other
Identity Management products therefore you do not have to go in depth in these
areas and you can mostly focus on the change itself.

We usually start writing design page using Google Docs or similar online
services since it gives the reviewers lots of useful tools such as comments,
assignments, suggestions and revision history. But please, do not forget to
submit a pull request to `sssd.io`_ to include the final revision `here`_ in
ReST format (see :ref:`the ReST template below <design-page-template>`) so it
can remain accessible in the future.

.. _sssd.io: https://github.com/SSSD/sssd.io
.. _here: https://github.com/SSSD/sssd.io/tree/master/src/design-pages

You can use the following template to write a design page, but you can also
modify it as you deem fit.

Feature name
************

Related Tickets
===============

* Link to a upstream ticket
* Link to a upstream ticket
* ...

Problem statement
=================

Describe the problem. The purpose is to give the reader who is not familiar with
the ticket and idea on what and why. It should provide answers to the following
questions:

* What is the current situation?
* What is the problem?
* Why is it a problem?
* Why do we want to change that?
* Why do we want this new feature?
* What does it solve?
* etc.

Use cases
=========

This section contains the problem statement translated into simple use cases
with actors. This helps to quickly identify the target consumers and their
requirements. For example:

* As a user, I want to ...
* As an administrator, I want to ...

Solution overview
=================

High level overview of proposed solution. This section should give the reader an
idea on the solution even without the knowledge of SSSD's internals. Describe
the solution in a way that can be understood but avoid implementation details
such as changes in API or configuration.

This section should also document the decision process on why this solution was
selected over the other considered proposal.

Implementation details
======================

This section should contain all the implementation details of the proposed
solution. The purpose is to describe the changes in configuration and in public
API. It does not have to *(and should not)* describe every single change
and data structures that you are going to introduce but it should highlight the
important parts so the reader can get familiar with it and can provide feedback
and suggestions.

Authors
=======

* Your name <your email>

----

You can start with the following ReST template:

.. _design-page-template:

.. code-block:: rst

    Feature name
    ############

    Related Tickets
    ***************

    * https://github.com/SSSD/sssd/issues/{id}

    Problem statement
    *****************

    Solution overview
    *****************

    Implementation details
    **********************

    Authors
    *******

    * Your name <your email>
