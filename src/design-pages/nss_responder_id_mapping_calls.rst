ID Mapping calls for the NSS responder
--------------------------------------

Related tickets:

-  `RFE Integrate SSSD with CIFS
   client <https://pagure.io/SSSD/sssd/issue/1534>`__
-  `RFE Use the Global Catalog in SSSD for the AD
   provider <https://pagure.io/SSSD/sssd/issue/1557>`__
-  `RFE Use the getpwnam()/getgrnam() interface as a gateway to resolve
   SID to Names <https://pagure.io/SSSD/sssd/issue/1559>`__

Related design documents:

-  `Integrate SSSD with CIFS
   Client <https://docs.pagure.org/SSSD.sssd/design_pages/integrate_sssd_with_cifs_client.html>`__
-  `Global Catalog Lookups in
   SSSD <https://docs.pagure.org/SSSD.sssd/design_pages/global_catalog_lookups.html>`__

Problem Statement
~~~~~~~~~~~~~~~~~

When SSSD is used in environments with AD, either as a member of the AD
domain or as a member of a trusted IPA domain, it has to map users and
groups managed by AD to a POSIX ID. The AD user and groups are
identified by

-  a name which may change
-  a unique SID which never changes, i.e. new SID == new object

Applications interacting tightly with users and groups from AD domains
e.g.

-  samba
-  cifs-client
-  FreeIPA

need to know which SID relates to which POSIX ID or name.

Mapping a SID to a user or group would be possible with the current
interfaces as described in ticket
`#1559 <https://pagure.io/SSSD/sssd/issue/1559>`__. But getting a SID
for a user or a group would be at least hard and ugly if not impossible.
I think the solution proposed in ticket
`#1559 <https://pagure.io/SSSD/sssd/issue/1559>`__ is a good and
useful shortcut. But by making the \*bySID lookups also available via a
new calls applications will have a more reliable interface, e.g. by
allowing more specific error codes (see details below).

Overview of the solution
~~~~~~~~~~~~~~~~~~~~~~~~

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

The NSS responder will be extended with four new calls: ::

    SSS_NSS_GETSIDBYNAME = 0x0111, /**< Takes a zero terminated fully qualified name
                                        and returns the zero terminated string representation
                                        of the SID of the object with the given name.
                                    */
    SSS_NSS_GETSIDBYID   = 0x0112, /**< Takes an unsigned 32bit integer (POSIX ID)
                                        and returns the zero terminated string representation
                                        of the SID of the object with the given ID.
                                    */
    SSS_NSS_GETNAMEBYSID = 0x0113, /**< Takes the zero terminated string representation
                                        of a SID and returns the zero terminated fully
                                        qualified name of the related object.
                                    */
    SSS_NSS_GETIDBYSID   = 0x0114, /**< Takes the zero terminated string representation
                                        of a SID and returns and returns the POSIX ID of
                                        the related object as unsigned 32bit integer value
                                        and another unsigned 32bit integer value indicating
                                        the type (unknown, user, group, both) of the object.
                                    */

Alternatively SSS\_NSS\_GETSIDBYID and SSS\_NSS\_GETIDBYSID could be
implemented to take an return arrays SIDs and POSIX IDs respectively as
the related cifs\_idmap API calls (see `Integrate SSSD with CIFS
Client <https://docs.pagure.org/SSSD.sssd/design_pages/integrate_sssd_with_cifs_client.html>`__).
I took the approach mentioned above because it better matches the other
NSS responder calls and additionally I do not like the implicit required
ordering in the input and output array.

After receiving the request the NSS responder will first check if it can
create the response from cached data. If not the request is forwarded to
the providers. For the \*byName and \*byID calls the corresponding
existing interface can be used. For the \*bySID call a new call must be
added to the providers. Currently only the IPA and AD provider will
support the new calls. If the provider cannot handle the requests it
will return an appropriate error code which it return to the client via
the NSS responder.

Additionally on the provider side it must be ensured that the string
representation of the SID is saved in the cache. It looks that this is
already the case for the AD provider. But I think this is currently not
the case for the IPA provider for both IPA and trusted users. Also the
PAC responder should add the SID to the cache object.

The sid2name extended operation on the FreeIPA server should get a new
request type and corresponding response types so that the SID is
returned with the user and group data. (A ticket for this should be
opened for FreeIPA if this design is approved.)

C-API
^^^^^

The C-API for those calls will be made available in a new library
libsss\_nss\_idmap (other names are welcome). Like the other client
libraries this library will just offer an easy way to send the requests
to SSSD and receive the responses, all processing is done by SSSD not by
the library. In contrast to libnss\_sss loaded via glibc into client
programs the new library can be linked with other programs. The new
calls will be declared in a header sss\_nss\_idmap.h and can have
reasonable return values to make error detection an reporting easier for
the clients using the new API.

::

    /**
     * @brief Find SID by fully qualified name
     *
     * @param[in] fq_name Fully qualified name of a user or a group
     * @param[out] sid    String representation of the SID of the requested user or group,
                          must be freed by the caller
     *
     * @return
     *  - 0 (EOK): success, sid contains the requested SID
     *  - ENOENT: requested object was not found in the domain extracted from the given name
     *  - ENETUNREACH: SSSD does not know how to handle the domain extracted from the given name
     *  - ENOSYS: this call is not supported by the configured provider
     *  - EINVAL: input cannot be parsed
     *  - EIO: remote servers cannot be reached
     *  - EFAULT: any other error
     */
    int sss_nss_getsidbyname(const char *fq_name, char **sid);

    /**
     * @brief Find SID by a POSIX UID or GID
     *
     * @param[in] id   POSIX UID or GID
     * @param[out] sid String representation of the SID of the requested user or group,
                       must be freed by the caller
     *
     * @return
     *  - see #sss_nss_getsidbyname
     */
    int sss_nss_getsidbyid(uint32_t id, char **sid);

    /**
     * @brief Return the fully qualified name for the given SID
     *
     * @param[in] sid      String representation of the SID
     * @param[out] fq_name Fully qualified name of a user or a group,
                           must be freed by the caller
     *
     * @return
     *  - see #sss_nss_getsidbyname
     */
    int sss_nss_getnamebysid(const char *sid, char **fq_name);

    /**
     * @brief Return the POSIX ID for the given SID
     *
     * @param[in] sid      String representation of the SID
     * @param[out] id      POSIX ID related to the SID
     * @param[out] id_type Type of the object related to the ID
     *
     * @return
     *  - see #sss_nss_getsidbyname
     */
    int sss_nss_getidbysid(const char *sid, uint32_t *id, enum id_type id_type);

Currently I do not see a strong requirement to allow different kind of
memory allocators (e.g. talloc).

I think it is not necessary to add special set of return values/error
code but the standard ones are sufficient. Maybe ENETUNREACH it indicate
that SSSD could not find the right domain for the request could be
replaced by a better one. (EDOM would be a candidate, but IMO it should
be reserved for mathematical operations.)

Python bindings
^^^^^^^^^^^^^^^

To allow easy usage of the new calls by the FreeIPA python framework,
python binding would be useful.

Lookup utility
^^^^^^^^^^^^^^

A small utility sss\_idmap (other names are welcome) will be added which
offers access to the new calls via libsss\_nss\_idmap. This utility will
make testing easier and might help user and administrators as well.

::

    # sss_idmap --help
    Usage: sss_idmap [OPTION...]
      -n, --name-to-sid=NAME      Converts name to SID
      -s, --sid-to-name=SID       Converts SID to name
      -S, --sid-to-id=SID         Converts SID to POSIX ID
      -i, --id-to-sid=ID          Converts POSIX ID to SID

    Help options:
      -?, --help                  Show this help message
      --usage                     Display brief usage message

The following diagram illustrates the data flow and the communication
between the different components (Dmitri Pal kindly provided the
diagram).

How to test
~~~~~~~~~~~

The sss\_idmap utility or the python bindings can be used to create
tests, e.g.

::

    # sss_idmap --sid-to-name=S-1-5-21-111111-222222-333333-1234
    DOM\user
    # sss_idmap --name-to-sid=DOM\user
    S-1-5-21-111111-222222-333333-1234
    # sss_idmap --sid-to-name=abcdefg
    Usage: sss_idmap .......
    Invalid SID

Author(s)
~~~~~~~~~

Sumit Bose <`sbose@redhat.com <mailto:sbose@redhat.com>`__>
