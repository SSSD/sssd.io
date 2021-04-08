Integrate SSSD with CIFS Client
-------------------------------

Related tickets:

-  `RFE Integrate SSSD with CIFS
   client <https://pagure.io/SSSD/sssd/issue/1534>`__
-  `RFE Allow SSSD to be used with smbd
   shares <https://pagure.io/SSSD/sssd/issue/1588>`__

Designs and tickets this design (might) depend:

-  `ID Mapping calls for the NSS
   responder <https://docs.pagure.org/SSSD.sssd/design_pages/nss_responder_id_mapping_calls.html>`__
-  `Global Catalog Lookups in
   SSSD <https://docs.pagure.org/SSSD.sssd/design_pages/global_catalog_lookups.html>`__
-  `RFE Use the getpwnam()/getgrnam() interface as a gateway to resolve
   SID to Names <https://pagure.io/SSSD/sssd/issue/1559>`__

Problem Statement
~~~~~~~~~~~~~~~~~

Although mapping of POSIX UIDs and SIDs is not needed mounting a CIFS
share it might become necessary when working with files on the share,
e.g. when modifying ACLs. Up to version 5.8 the cifs-utils package uses
Winbind for this exclusively and the following binaries were linked
against libwbclient:

-  /usr/bin/getcifsacl
-  /usr/bin/setcifsacl
-  /usr/sbin/cifs.idmap

With version 5.9 of cifs-utils a plugin interface was introduced by Jeff
Layton (Thank you very much Jeff) to allow services other than winbind
to handle the mapping of POSIX UIDs and SIDs. SSSD will provide a plugin
to allow the cifs-utils to ask SSSD to map the ID. With this plugin an
SSSD client can access a CIFS share with the same functionality as a
client running Winbind.

Use Case
~~~~~~~~

Environment where FreeIPA and AD trusts are used already, but also Samba
file server should be used. It's important that UNIX IDs are mapped the
same way in all utilities, then and all IDs are consistent.

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

There are two parts of this feature - a plugin for cifs-utils and a
library implementing the winbind API, but with SSSD calls. Both these
parts are fairly self-contained and do not touch the SSSD internals. See
the next section for the implementation details.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

The plugin interface is defined in cifsidmap.h which can be found in the
cifs-utils-devel package. For easier reference a copy of the relevant
section is included below.

-  From the 6 expected functions, cifs\_idmap\_init\_plugin() and
   cifs\_idmap\_exit\_plugin() are obvious.

-  cifs\_idmap\_sid\_to\_str() and cifs\_idmap\_str\_to\_sid() are
   SID-to-Name and Name-to-SID mappings as discussed in
   NSSResponderIDMappingCalls. I think the new libsss\_nss\_idmap.so
   mentioned there can be used here, too.

-  cifs\_idmap\_sids\_to\_ids() and cifs\_idmap\_ids\_to\_sids() are the
   ID mapping calls. Although it might be possible possible to map IDs
   algorithmically without talking to SSSD I think those calls should
   also reach out to SSSD to do the mapping. The main reason is to allow
   other kind of mappings (e.g. using POSIX attributes if available in
   AD). ::

      57 /*
      58  * Plugins should implement the following functions:
      59  */
      60
      61 /**
      62  * cifs_idmap_init_plugin - Initialize the plugin interface
      63  * @handle - return pointer for an opaque handle
      64  * @errmsg - pointer to error message pointer
      65  *
      66  * This function should do whatever is required to establish a context
      67  * for later ID mapping operations. The "handle" is an opaque context
      68  * cookie that will be passed in on subsequent ID mapping operations.
      69  * The errmsg is used to pass back an error string both during the init
      70  * and in subsequent idmapping functions. On any error, the plugin
      71  * should point *errmsg at a string describing that error. Returns 0
      72  * on success and non-zero on error.
      73  *
      74  * int cifs_idmap_init_plugin(void **handle, const char **errmsg);
      75  */
      76
      77 /**
      78  * cifs_idmap_exit_plugin - Destroy an idmapping context
      79  * @handle - context handle that should be destroyed
      80  *
      81  * When programs are finished with the idmapping plugin, they'll call
      82  * this function to destroy any context that was created during the
      83  * init_plugin. The handle passed back in was the one given by the init
      84  * routine.
      85  *
      86  * void cifs_idmap_exit_plugin(void *handle);
      87  */
      88
      89 /**
      90  * cifs_idmap_sid_to_str - convert cifs_sid to a string
      91  * @handle - context handle
      92  * @sid    - pointer to a cifs_sid
      93  * @name   - return pointer for the name
      94  *
      95  * This function should convert the given cifs_sid to a string
      96  * representation or mapped name in a heap-allocated buffer. The caller
      97  * of this function is expected to free "name" on success. Returns 0 on
      98  * success and non-zero on error. On error, the errmsg pointer passed
      99  * in to the init_plugin function should point to an error string. The
     100  * caller will not free the error string.
     101  *
     102  * int cifs_idmap_sid_to_str(void *handle, const struct cifs_sid *sid,
     103  *                              char **name);
     104  */
     105
     106 /**
     107  * cifs_idmap_str_to_sid - convert string to struct cifs_sid
     108  * @handle - context handle
     109  * @name   - pointer to name string to be converted
     110  * @sid    - pointer to struct cifs_sid where result should go
     111  *
     112  * This function converts a name string or string representation of
     113  * a SID to a struct cifs_sid. The cifs_sid should already be
     114  * allocated. Returns 0 on success and non-zero on error. On error, the
     115  * plugin should reset the errmsg pointer passed to the init_plugin
     116  * function to an error string. The caller will not free the error string.
     117  *
     118  * int cifs_idmap_str_to_sid(void *handle, const char *name,
     119  *                              struct cifs_sid *sid);
     120  */
     121
     122 /**
     123  * cifs_idmap_sids_to_ids - convert struct cifs_sids to struct cifs_uxids
     124  * @handle - context handle
     125  * @sid    - pointer to array of struct cifs_sids to be converted
     126  * @num    - number of SIDs to be converted
     127  * @cuxid  - pointer to preallocated array of struct cifs_uxids for return
     128  *
     129  * This function should map an array of struct cifs_sids to an array of
     130  * struct cifs_uxids.
     131  *
     132  * Returns 0 if at least one conversion was successful and non-zero on error.
     133  * Any that were not successfully converted will have a cuxid->type of
     134  * CIFS_UXID_TYPE_UNKNOWN.
     135  *
     136  * On any error, the plugin should reset the errmsg pointer passed to the
     137  * init_plugin function to an error string. The caller will not free the error
     138  * string.
     139  *
     140  * int cifs_idmap_sids_to_ids(void *handle, const struct cifs_sid *sid,
     141  *                              const size_t num, struct cifs_uxid *cuxid);
     142  */
     143
     144 /**
     145  * cifs_idmap_ids_to_sids - convert uid to struct cifs_sid
     146  * @handle - context handle
     147  * @cuxid  - pointer to array of struct cifs_uxid to be converted to SIDs
     148  * @num    - number of cifs_uxids to be converted to SIDs
     149  * @sid    - pointer to preallocated array of struct cifs_sid where results
     150  *           should be stored
     151  *
     152  * This function should map an array of cifs_uxids an array of struct cifs_sids.
     153  * Returns 0 if at least one conversion was successful and non-zero on error.
     154  * Any SIDs that were not successfully converted should have their revision
     155  * number set to 0.
     156  *
     157  * On any error, the plugin should reset the errmsg pointer passed to the
     158  * init_plugin function to an error string. The caller will not free the error
     159  * string.
     160  *
     161  * int cifs_idmap_ids_to_sids(void *handle, const struct cifs_uxid *cuxid,
     162  *                              const size_t num, struct cifs_sid *sid);
     163  */

SSSD will provide a plugin which will basically act as a wrapper for the
calls in libsss\_nss\_idmap.so.

The libwbclient plugin will include implementation of the following
functions that call into SSSD: ::

    wbcLookupName
    wbcLookupSid
    wbcLookupRids
    wbcSidToUid
    wbcUidToSid
    wbcSidToGid
    wbcGidToSid
    wbcGetpwnam
    wbcGetpwuid
    wbcGetpwsid
    wbcGetgrnam
    wbcGetgrgid

How to test
~~~~~~~~~~~

Testing with getcifsacl
^^^^^^^^^^^^^^^^^^^^^^^

If there is no plugin for the CIFS client utilities or the plugin cannot
resolve the SIDs to names getcifsacl will only show the SID strings in
the output: ::

    # getcifsacl /tmp/bla/Users/Administrator/Desktop/putty.exe
    REVISION:0x1
    CONTROL:0x8004
    OWNER:S-1-5-32-544
    GROUP:S-1-5-21-3090815309-2627318493-3395719201-513
    ACL:S-1-5-18:ALLOWED/0x0/FULL
    ACL:S-1-5-32-544:ALLOWED/0x0/FULL
    ACL:S-1-5-21-3090815309-2627318493-3395719201-500:ALLOWED/0x0/FULL

otherwise the output might look like ::

    # getcifsacl /tmp/bla/Users/Administrator/Desktop/putty.exe
    REVISION:0x1
    CONTROL:0x8004
    OWNER:BUILTIN\Administrators
    GROUP:AD18\Domain Users
    ACL:S-1-5-18:ALLOWED/0x0/FULL
    ACL:BUILTIN\Administrators:ALLOWED/0x0/FULL
    ACL:AD18\Administrator:ALLOWED/0x0/FULL

Testing with cifsacl option to mount.cifs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the cifsacl mount option is used the cifs kernel module will call
cifs.idmap to translate the Windows SIDs into the corresponding
UIDs/GIDs of the client system so that the ownership of the files in the
mounted file system is not mapped to the user how mounted the file
system, but corresponds to the owning user and group of the Windows
domain.

Testing the libwbclient API
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Switching between the Winbind implementation and the SSSD implementation
can be done using alternatives: ::

        alternatives --set libwbclient.so.11 /usr/lib64/sssd/modules/libwbclient.so.0.11.0
        alternatives --list

When SSSD is set as the libwbclient implementation, you can test the
calls using wbinfo: ::

    $ /usr/bin/wbinfo -n 'AD18\Administrator'
    S-1-5-21-3090815309-2627318493-3395719201-500 SID_USER (1)
    $ /usr/bin/wbinfo -S S-1-5-21-3090815309-2627318493-3395719201-500
    1670800500

The following switches can be used to test the functions mentioned in
the implementation section: ::

      -n, --name-to-sid=NAME                Converts name to SID
      -s, --sid-to-name=SID                 Converts SID to name
      -U, --uid-to-sid=UID                  Converts UID to SID
      -G, --gid-to-sid=GID                  Converts GID to SID
      -S, --sid-to-uid=SID                  Converts SID to UID
      -Y, --sid-to-gid=SID                  Converts SID to GID
      -i, --user-info=USER                  Get user info
          --uid-info=UID                    Get user info from UID
          --group-info=GROUP                Get group info
          --user-sidinfo=SID                Get user info from SID
          --gid-info=GID                    Get group info from GID
      -r, --user-groups=USER                Get user groups

Additional links
~~~~~~~~~~~~~~~~

`https://access.redhat.com/documentation/en-US/Red\_Hat\_Enterprise\_Linux/7/html/Windows\_Integration\_Guide/SMB-SSSD.html <https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Windows_Integration_Guide/SMB-SSSD.html>`__

Author(s)
~~~~~~~~~

Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
