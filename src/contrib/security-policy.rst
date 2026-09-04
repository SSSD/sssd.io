SSSD Security Policy
####################

Our Commitment
**************

SSSD takes security seriously. We are committed to maintaining the highest
level of security and trust for our users. We appreciate the security research
community's efforts in helping us identify and address vulnerabilities
responsibly.

Supported Versions
******************

Only the latest release of SSSD receives regular security patches. Earlier
versions may receive critical fixes on a best-effort basis, but we cannot
guarantee back-porting to unsupported versions.

Security Model
**************

Security assumptions and threat model
=====================================

SSSD is designed to read information about users, groups and other resources
from trusted servers. This data is written into a cache file for offline usage
and is made available to system services via various interfaces.

The data received from the server is in general trusted and only sanity checks
or similar are done. This means that SSSD should be configured to use encrypted
connection (typically used by default) and the server should be verified
(typically done by default). To do this properly SSSD has to trust system
resources like e.g the system central Certificate Authority (CA) certificate
store for TLS connections.

It is expected that the cache file is used only by SSSD and that only a
dedicated SSSD system user or the root user can access it. It is expected that
there is always sufficient disk space for operations on the cache file, if e.g.
the disk is full some functionality of SSSD might be degraded.


Reporting a Vulnerability
*************************

Please see SSSD's `SECURITY.md file on GitHub
<https://github.com/SSSD/sssd/blob/master/SECURITY.md>`_ as well.

How to Report
=============

Please report security vulnerabilities privately through one of these channels:

 - Email
   - Send to: secalert@redhat.com

Do NOT report security vulnerabilities through:

 - Public GitHub issues
 - Pull requests
 - Public forums or social media

What to Include
===============

Please provide the following information:

 - Title: Clear, descriptive summary
 - Reporter details: Your name/handle and affiliation (optional)
 - Vulnerability description: Technical details of the issue
 - Affected versions: Mandatory: known, affected version; Good to have: identification of all affected versions
 - Reproduction steps: Minimal example to reproduce the issue
 - Impact assessment: Potential exploit scenarios and severity
 - Suggested fix: If you have recommendations (optional)
 - Disclosure status: Whether this has been shared elsewhere

What to Report
==============

Please report if you have:
 - Discovered a potential security vulnerability
 - Found an issue but are uncertain about its security impact
 - Identified vulnerabilities in dependencies not yet addressed

What NOT to Report
==================

The following do not qualify as security vulnerabilities:
 - Automated scanner output without analysis or reproduction steps
 - General support or usage questions
 - Requests for help updating to newer versions
 - Bugs without security implications

Response Process
****************

Please see Red Hat's `Security Contacts and Procedures
<https://access.redhat.com/security/team/contact>`_.

Disclosure Policy
*****************

 - We follow coordinated disclosure practices
 - Fixes are typically included in the next planned release
 - Critical vulnerabilities may warrant out-of-band releases
 - Public disclosure occurs via Red Hat Security Advisories
 - Reporters are credited unless they prefer anonymity

Security Advisories
*******************

Published advisories are available at:
Red Hat CVE database: `https://access.redhat.com/security/security-updates/cve?q=sssd <https://access.redhat.com/security/security-updates/cve?q=sssd>`_

Safe Usage Guidelines
*********************

To use SSSD securely:
 - Keep updated: Always use supported versions
 - Always use encrypted connections and verify the server with e.g. TLS or
   SASL/GSSAPI

Scope
*****

In Scope
========

 - SSSD codebase
 - Documentation that could lead to insecure usage

Out of Scope
============

- Third-party plugins or extensions
- User-implemented code
- Issues requiring physical access
- Social engineering attacks
- Denial of service through exhaustion of external resources



Recognition
***********

We thank security researchers who help improve SSSD. Contributors are acknowledged in:
 - Security advisories

Policy Updates
**************

This policy may be updated periodically. Suggestions for improvement can be submitted via issues or pull requests.
