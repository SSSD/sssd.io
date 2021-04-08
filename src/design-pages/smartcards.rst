Smart Cards
===========

For Fedora 20 (ended up in 21), we proposed adding `support for smart
cards <https://fedoraproject.org/wiki/Changes/SSSD_Smart_Card_Support>`__
to SSSD. This is where we work out how to do it, or try to, anyway.

Multi-step Authentication
-------------------------

Considerations
~~~~~~~~~~~~~~

-  Current sequence of events when a client authenticates:

   -  pam\_sss sends a request to the PAM responder, containing
      parameters:

      -  PAM\_USER (the login name)
      -  PAM\_SERVICE
      -  PAM\_TTY
      -  PAM\_RUSER
      -  PAM\_RHOST
      -  client PID
      -  PAM\_AUTHTOK (supplied password)
      -  PAM\_NEWAUTHTOK (new password, if changing)

   -  PAM responder sends a D-Bus method call over a private bus to the
      domain's provider, containing:

      -  user
      -  domain
      -  service
      -  tty
      -  ruser
      -  rhost
      -  authtok\_type (enumerated, one of {password, ccfilename,
         empty})
      -  authtok\_data
      -  newauthtok\_type (enumerated, one of {password, ccfilename,
         empty})
      -  newauthtok\_data
      -  1 if client is on privileged pipe, else 0
      -  client PID

   -  domain provider sends a method reply to the PAM responder

      -  PAM status code
      -  empty array of response messages

   -  PAM responder replies to pam\_sss

      -  PAM status code

-  PAM modules can prompt for an arbitrary number of answers at once.

   -  Sometimes this is a password.
   -  Sometimes this is a non-password one-off secret.
   -  Both tend to be stored as the PAM\_AUTHTOK item, without
      indication of what's been stored there.

-  An LDAP simple bind transmits the user's DN and current password to
   server; nothing else is required.

   -  Conclusion: multi-step needs to be a superset of single-step.

-  An LDAP OTP bind requires a fresh OTP value.

   -  Conclusion: we need to be able to distinguish between a cacheable
      password and a not-cacheable not-a-password.

-  Kerberos can prompt for current password, and/or one of several OTP
   values, and/or one of several smart card PINs.

   -  Conclusion: multi-step is sometimes going to mean having multiple
      questions at a given each step, only some of which will need to be
      answered before proceeding.

-  The set of things the user can provide may change during an
   authentication attempt, for example if the user inserts a smart card
   or swipes a finger over a scanner.
-  The model for the dialog between components should cover these cases.

Proposal
~~~~~~~~

-  Modify request/reply messages from pam\_sss to responder to backends.
-  Request and reply messages passed between pam\_sss and responder need
   to add an identifier to distinguish one ongoing authentication
   attempt from another.

   -  This value is under control of a possibly-not-trustworthy
      pam\_sss, so if it isn't the value that we designate for
      requesting a new attempt (either 0 or -1), it should be checked
      for correspondence with an ongoing authentication attempt before
      we do anything else for it.

-  Request and reply messages passed between responder and data provider
   need to add an identifier to distinguish one ongoing authentication
   attempt from another.

   -  Because the responder is multiplexing requests from multiple
      pam\_sss instances, this identifier should be not be the same as
      the one received from pam\_sss in a request message.

-  Reply messages over both connections (pam\_sss-to-responder, and
   responder-to-provider) need to be able to carry multiple questions
   back to a requester. A request message needs to be able to supply
   answers for any subset of those questions.
-  The initial request also needs to start carrying some flags. If set,
   the client (which, because PAM conversation callbacks are blocking,
   probably won't be pam\_sss) is indicating that it can handle updates
   to the list of questions for a given authentication attempt.

   -  The responder can indicate that a smart card was inserted by
      adding a request for the card's PIN to the list of questions and
      sending the new list of questions to the responder's client.
   -  The responder can similarly indicate that input is no longer
      required if authentication happened out-of-band or has timed out.
   -  The provider will likely emit signals or issue method calls to the
      responder to get the responder to forward updated information to
      the responder's client if that information has been asked for.
   -  If we get the provider and responder talking at each other in an
      unsynchronized manner like this, request identifiers are going to
      have to stay unique over a sufficiently-large period of time that
      simply discarding previously-queued-but-unprocessed updates will
      keep clients of the responder from getting confused by a backlog
      of updates which pertain to a previous authentication attempt.
   -  **TODO** run this by the GDM folks, to make sure it's the sort of
      info they're going to be able to use.

-  Reply messages will need to convey status that isn't just a PAM
   result code: { no-such-auth-attempt-id, got-questions-for-you,
   auth-failed, auth-succeeded }.
-  Suggested prompt layout for reply messages: an array of tuples.
   [(group,questionid,type,details),...]

   -  group: an integer identifier for a group of related questions
   -  questionid: integer identifying a specific question in a group
   -  type: enumeration indicating "kind" of information being requested

      -  password
      -  secret (might not be a password, caching not recommended)
      -  OTP value
      -  insert smart card (unsynchronized only)
      -  scan proximity device (unsynchronized only)
      -  swipe finger (unsynchronized only)
      -  provide smart card PIN out-of-band (if the token has a
         protected authentication path)
      -  smart card PIN (if the token does not have a protected
         authentication path)

   -  detail: structured per-type data:

      -  password → empty
      -  secret → prompt text
      -  OTP value → modeled after
         `​krb5\_responder\_otp\_tokeninfo <https://github.com/krb5/krb5/blob/master/src/include/krb5/krb5.hin#L6626>`__

         -  service name
         -  token index (corresponds to "ti" in the krb5 API)
         -  flags
         -  format
         -  length
         -  vendor
         -  challenge
         -  token ID
         -  algorithm ID

      -  insert smart card -> empty
      -  scan proximity device -> empty
      -  swipe finger -> empty
      -  provide smart card PIN out-of-band or smart card PIN

         -  either broken-out
            `​pkinit\_identities <http://web.mit.edu/Kerberos/krb5-1.9/krb5-1.9.1/doc/krb5-admin.html#pkinit%20identity%20syntax>`__

            -  module name (shared library file name)
            -  slot ID (hex string representing byte array)
            -  token label (string)
            -  certificate ID (hex string representing byte array)
            -  certificate label (string)

         -  or `​p11-kit
            URI <https://datatracker.ietf.org/doc/draft-pechanec-pkcs11uri/>`__
            fields, some of which are:

            -  token label
            -  token manufacturer
            -  token model
            -  token serial number
            -  certificate label

         -  We'll have to go with a common subset of the two to mask the
            differences between what we get when we're doing PKINIT and
            what we have available when we're calling p11-kit/PKCS#11
            directly. Medium-to-longer term, we may need to add to what
            PKINIT provides here.

   -  The responder needs to be able to filter the list of questions it
      gets from the provider to remove questions for kinds of data which
      the administrator does not want to allow to be used for
      authenticating users, passing back to the client only a subset of
      the questions that the provider requested be asked. The list of
      questions could even be pared down to nothing.

-  Suggested answer form for request messages: another tuple array.
   [(group,questionid,answer)...]

   -  For any group, all questionids are expected to have answers.
   -  Answer formats:

      -  password → text string
      -  secret → text string
      -  OTP value → (token index, otp, pin) (or is text string enough?)
      -  insert smart card (never sent by client - out-of-band action)
      -  scan proximity device (never sent by client - out-of-band
         action)
      -  swipe finger (never sent by client - out-of-band action)
      -  provide smart card PIN out-of-band (never sent by client -
         out-of-band action)
      -  smart card PIN → (token label, text string)

Smart Card support, part 1: load the drivers, find the right reader (if we can).
--------------------------------------------------------------------------------

Considerations
~~~~~~~~~~~~~~

-  Readers (*slots* in PKCS#11 jargon), and access to them, haven't
   historically been tied to a console or seat.
-  Cards (*tokens* in PKCS#11 jargon) have therefore been accessible to
   any user on the system for the purposes of logging in to a card and
   using it, or attempting to log in to a card.
-  Some cards self-destruct after a maximum number of failed login
   attempts. Some of these cards can expose a flag in their
   CK\_TOKEN\_INFO to warn that this is about to become a problem.
   Experimentally, some cards which lock the user out after some number
   of failed login attempts, however, don't expose this flag.
-  Multi-user systems, or software which isn't careful about what it
   uses to try to log into a card, can make it very easy for one user to
   destroy someone else's card.

Proposal
~~~~~~~~

-  Use p11-kit to avoid having to tell SSSD specifically about which
   module or modules to use, and to allow us to share the hardware
   configuration which will be used by the user during their login
   session. For PKINIT, this means we'll probably end up using
   p11-kit-proxy.so by default, as it expects the name of a module to
   load when using PKCS#11.
-  Loading the p11-kit-proxy.so module using NSS's APIs gives it access
   to the same set of modules that p11-kit's native API provides, and
   also adds reference counting for module initializations, which should
   avoid at least one known error case that we've seen with the
   soft-pkcs11.so module (wherein calling its initialization function a
   second time nukes any still-being used state).
-  **TODO** We can map from a responder client PID to a unit which might
   have a TTY (before login) or a session with a seat (after login), but
   can we map from a SLOT\_INFO to a anything that lets us avoid using a
   slot if it doesn't belong to the seat on which a particular client
   sits? (This bit has been bugging the author for a while now.)

Smart Card support, part 2: verify the card's contents.
-------------------------------------------------------

Considerations
~~~~~~~~~~~~~~

-  We need to log in to the card as a user.
-  We need to find a certificate on the card for which the card also
   holds the corresponding private key.

   -  Conceptually, the simplest thing is to just sign some data with
      the private key, and verify it using the public key in the
      certificate.
   -  We *could* alternately read the specific public fields from the
      private key, pull the public key out of the certificate, decode
      that public key (in a manner specific to the type of key), and
      compare the two, but we still wouldn't know for sure that the
      private parts of the key were correct. And we'd have extend this
      code for every new type of key pair we wanted to support into the
      future. So we'll just do the sign/verify, like pam\_pkcs11 does.

-  We need to verify that that certificate is issued by an issuer who is
   trusted to issue certificates for login. The set of CAs which we
   trust to do that is almost certainly going to be a much smaller set
   than the full set of commercial CAs that we trust for issuing SSL
   server certificates.
-  We need to verify that that certificate is suitable for login, i.e.,
   not just for signing email and/or visiting web sites. On Windows
   KDCs, and on MIT KDCs by default, this is indicated with a particular
   value in the extendedKeyUsage extension. Large client rollouts may
   have deployed cards with certificates containing one or the other or
   neither, so this needs to be a requirement that we can relax through
   configuration.

Proposal
~~~~~~~~

-  If configured, if a card is not present, wait for card insertion in
   to a suitable slot. Note that the slot and token may show up at the
   same time.
-  Verify that user has access to token in slot.

   -  PIN is accepted for login to card as CKU\_USER.
   -  Find certificate and private key where the pair is marked as
      suitable for signing data.
   -  Generate random to-be-signed data.
   -  Sign generated data with private key.
   -  Verify signature over generated data using public key contained in
      certificate.

-  Verify that the just-used certificate on the token chains up to an
   issuer who is trusted to issue certificates which can be used for
   logging in.

   -  Note that this trusted issuer set is tightly controlled beyond the
      normal set of CAs who are trusted to issue certificates for other
      servers.
   -  **TODO** seek guidance and assistance from the p11-kit
      implementors, who are working on standardizing the storage and
      expression of trust anchor information. PKINIT expects that we
      pass in the names of files containing trusted anchors and known
      intermediates, while p11-kit/PKCS#11 expose the information as
      certificate and CKO\_NSS\_TRUST/??? objects on a token. We're
      going to want to use p11-kit as much as possible cut down on the
      number of places this has to be configured on a given system.

-  Check for either the Windows Smart Card Logon extendedKeyUsage value,
   or the RFC4556 Kerberos Client value, but keep what exactly we look
   for configurable for the sake of existing deployments.

Smart Card support, part 3: check that the card matches the account.
--------------------------------------------------------------------

Considerations
~~~~~~~~~~~~~~

-  A certificate contains a subject field which identifies the owner of
   the public key in the certificate. This is a distinguished name,
   similar in many ways to an LDAP DN, mainly differing in that it's
   encoded as a DER blob, with attribute types represented by OIDs
   rather than by name, and with values encoded as DER strings of one of
   several types.
-  A certificate can also contain one or more subjectAlternativeName
   extension values. If it contains any of these, the subject field
   becomes optional. Each subjectAlternativeName (SAN) value is
   considered equally canonical. SAN values can take multiple forms,
   including but not limited to distinguished names, DNS names, IP
   addresses, email addresses, and Kerberos principal names.
-  Somehow, we have to use this naming information to figure out if the
   certificate belongs to the account.
-  For tech demo situations, we'd like to be able to use this
   information to discover the user account name without requiring that
   it be specified by an end-user. It's a secondary concern, however,
   and some customers legitimately want to be able to turn such a
   feature off.

Proposal
~~~~~~~~

Per-provider check for binding between certificate and account.

-  Kerberos (likely AD and IPA as well): let the KDC decide - if we get
   creds for the account's principal, we're done.

   -  This *should* handle matching using *altSecurityIdentity*
      information for us if we're talking to an AD server.
   -  **TODO** MIT krb5 KDC PKINIT logic currently only accepts a
      client's certificate if it contains the principal name as a SAN
      value. We'll want to be able to extend that.
   -  Don't forget that we need to verify the KDC's certificate, and its
      suitability to be issuing Kerberos tickets for the realm of the
      account.

-  LDAP (possibly AD and IPA as well):

   -  Let the server decide — connect to server using TLS with client
      auth and SASL/EXTERNAL, use whoami EXOP to read our entry DN,
      compare to the account's DN.

      -  With NSS, this *should* only require setting
         LDAP\_OPT\_X\_TLS\_CERTFILE to "tokenname:certnickname",
         preferably after logging in to token.
      -  This *should* get the server to handle *altSecurityIdentity*
         matching for us if we're talking to an AD server.
      -  When we start issuing client certificates in FreeIPA, we'll
         need to make sure that FreeIPA's configuring dirsrv's
         certmap.conf to pull the right attribute from the subject DN
         and construct a search that will match the user's entry.
      -  **TODO** figure out if there's a way to take the
         CK\_FUNCTION\_LIST which p11-kit/PKCS#11 gives us and hand it
         to the copy of NSS that libldap is using under the covers.

   -  Let the server merely hold the info — search for an entry that
      contains a copy of the certificate that's on the token as a
      userCertificate value, check results.
   -  Implement something like certmap.conf logic at the client.
   -  Compare the subject/SAN DN to the user's entry's DN.

      -  This is trickier than it sounds: converting from the binary
         encoding used in the certificate's fields to the text format
         used by LDAP requires that we map the OIDs of attributes to the
         name of the naming attribute used in the LDAP DN. Converting
         the LDAP DN to binary form may work better, but that's just a
         guess.

   -  Don't forget that we need to verify the server's certificate.

-  Local files:

   -  Read certificate Kerberos principal name SAN and perform libkrb5
      *auth\_to\_local* mapping.
   -  Check for the certificate in the user's entry in a local data
      store.
   -  Check for the public key in user's SSH authorized key list.
   -  Check for certificate subject/SAN CN matching user GECOS.
   -  Check for certificate subject/SAN CN matching user name.
   -  Check for certificate subject/SAN UID matching user name.
   -  Check for certificate subject/SAN emailAddress matching user name
      with in a configured email domain.
