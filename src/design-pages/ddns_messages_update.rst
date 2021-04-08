DDNS - specify which server to update DNS with
==============================================

Related ticket(s):

-  `https://pagure.io/SSSD/sssd/issue/2495 <https://pagure.io/SSSD/sssd/issue/2495>`__

Problem statement
~~~~~~~~~~~~~~~~~

SSSD provides input to nsupdate that's redundant and might actually
impair proper resolution using DNS. Further, format of messages pasted
to nsupdate is grouped by command type - deleting and adding addresses
are two separate batches which is not optimal as update of one of
address families might be prohibited to be changed on server.

Use cases
~~~~~~~~~

If DNS system is broken using dyndns\_server option might be a
workaround

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

-  Allow SSSD to add a new option that would specify which server to
   update DNS with ('dyndns\_server')
-  In first attempt to perform DDNS **do not specify zone/server/realm**
   commands in input for nsupdate (nsupdate will then utilize DNS)
-  As fallback (if first attempt fails) specify realm command and if
   'dyndns\_server' option is specified then also add server command
   with value of 'dyndns\_server'
-  Bulk deleting and adding addresses from the same address family into
   one batch rather then grouping by command type

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

-  Remove servername and dns\_zone parameters from
   sdap\_dyndns\_update\_send() as they are no longer used. Remove code
   from AD and IPA provider which was passing this data to
   sdap\_dyndns\_update\_send().
-  Remove dns\_zone field from struct sdap\_dyndns\_update\_state and
   remove all code relating to it.
-  In sdap\_dyndns\_update\_done() make setting command realm
   conditional same way as command server is.
-  Update nsupdate\_msg\_add\_fwd() to group commands by address family
   processed IP belongs to.

Configuration changes
~~~~~~~~~~~~~~~~~~~~~

New option dyndns\_server

How To Test
~~~~~~~~~~~

Check that IP addresses get changed in IPA and on AD. Break DNS
resolving to force first attempt of DDNS to fail. Check that messages
generated as input for nsupdate in domain logs are matching the
expectation.

Example of expected format of messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**First attempt**

 ::

    update delete husker.human.bs. in A
    update add husker.human.bs. 1200 in A 192.168.122.180
    send
    update delete husker.human.bs. in AAAA
    update add husker.human.bs. 1200 in AAAA 2001:cdba::666
    send

**Fallback attempt**

 ::

    ;sever is present only if option dyndns_server is set in sssd.conf
    server 192.168.122.20
    ;realm is used always in fallback message
    realm IPA.WORK
    update delete husker.human.bs. in A
    update add husker.human.bs. 1200 in A 192.168.122.180
    send
    ;sever is present only if option dyndns_server is set in sssd.conf
    server 192.168.122.20
    ;realm is used always in fallback message
    realm IPA.WORK
    update delete husker.human.bs. in AAAA
    update add husker.human.bs. 1200 in AAAA 2001:cdba::666
    send

Authors
~~~~~~~

`preichl@redhat.com <mailto:preichl@redhat.com>`__
