Enhanced NSS (Name Service Switch) API
======================================

Related ticket(s):
------------------
    https://pagure.io/SSSD/sssd/issue/2478

Problem statement
-----------------
The system-wide NSS API provided by glibc with calls like ``getpwnam`` etc.
might be a bottleneck for applications which are only interested in the data
provided by the SSSD backends.

It would be possible to load SSSD's NSS plugin ``libnss_sss.so`` with
``dlopen`` and call the provided functions directly. But besides being a bit
cumbersome the API defined by NSS is limited and does not offer an option to
control the behavior of the plugin. Hence a new API provider by SSSD to lookup
objects managed by SSSD would be beneficial.

Use cases
---------
The first users of the new API would be the FreeIPA ``extdom`` and
``slapi-nis`` plugins. Both are used to make information about users and groups
from trusted domains available and hence are only interested in results from SSSD.

Both plugins are run in threads of the 389ds directory server and to work
efficiently the current mutex based locking of the connection of SSSD should be
improved.

Additionally ``slapi-nis`` caches results for performance reasons. Being a part
of 389ds it will be notified if 389ds objects like e.g. id-overrides are
modified and can drop the cached object. But since SSSD caches results as well
a new lookup of the modified object via ``slapi-nis`` might still return the old
result which will then stay in the cache of ``slapi-nis`` because no new
modification is detected. As a result ``slapi-nis`` should be able to
invalidate objects in the caches of SSSD to allow a refresh. The ``sss_cache``
is only of limited use here because it requires root privileges and currently
invalidates the whole memory cache.

Overview of the solution
------------------------
Additional use cases should be supported by the new API. It should offer a timeout option so that an
individual thread does not have to wait until the request is completely handled
by SSSD but can abandon from the request and maybe check later if a result is
available.

Additionally an option to invalidate the cached entries of an individual object
is needed. It would be possible to use a set of new calls for this but since
most of the processing of such request and similar to the lookup requests it
would be more straight forward to use a flag to indicate that the cached entry
of the found object should be invalidated.

This gives us an API with two new options, a timeout and the bit-field for
flags. The flags might be useful for future use cases as well. And the flag to
invalidate cached entries of individual objects might be used in future by the
``sss_cache`` utility to make the code simpler and to avoid to completely
remove the memory cache.


Implementation details
----------------------

Client side
~~~~~~~~~~~
Some of the flags might have influence on the client behavior. E.g. the flag to
invalidate the cached entries of an object would tell the client to bypass the
memory cache. This is needed because the memory cache will only contain the
data of object which were directly requested. But the SSSD on-disk cache might
already contain data of objects which are looked up indirectly, e.g. groups
during an initgroups request or users while looking up group members. So a
missing entry in the memory cache does not indicate that the entry is missing
in the on-disk cache as well. Additionally memory cache and on-disk cache have
different timeouts which would require the request to go directly to the SSSD
responder as well.

For the timeout it has to be kept in mind that in a threaded environment there
are two major steps where time might be spend. First is of course the
communication with the SSSD responder. But the second is waiting on the mutex.
Currently SSSD's NSS plugin ``libnss_sss.so`` uses ``pthread_mutex_lock`` which
waits without limits until the mutex can be locked. The reason is that
``libnss_sss.so`` should restrict itself to only use glibc and not libpthread
and currently glibc only implements ``pthread_mutex_lock`` (see discussion in
https://bugzilla.redhat.com/show_bug.cgi?id=1369130 for details about this
requirement).

To wait only a limited amount of time libpthread offers
``pthread_mutex_timedlock`` but due to the restriction mentioned above this
should be implemented independently of the NSS plugin code.
``libsss_nss_idmap`` looks like the most suitable place for this.

New calls
~~~~~~~~~
The API of the new calls will be defined in ``sss_nss_idmap.h``::

    /**
     * Flags to control the behavior and the results for sss_*_ex() calls
     */

    #define SSS_NSS_EX_FLAG_NO_FLAGS 0

    /** Always request data from the server side, client must be privileged to do
     *  so, see nss_trusted_users option in man sssd.conf for details.
     *  This flag cannot be used together with SSS_NSS_EX_FLAG_INVALIDATE_CACHE */
    #define SSS_NSS_EX_FLAG_NO_CACHE (1 << 0)

    /** Invalidate the data in the caches, client must be privileged to do
     *  so, see nss_trusted_users option in man sssd.conf for details.
     *  This flag cannot be used together with SSS_NSS_EX_FLAG_NO_CACHE */
    #define SSS_NSS_EX_FLAG_INVALIDATE_CACHE (1 << 1)

    #ifdef IPA_389DS_PLUGIN_HELPER_CALLS

    /**
     * @brief Return user information based on the user name
     *
     * @param[in]  name       same as for getpwnam_r(3)
     * @param[in]  pwd        same as for getpwnam_r(3)
     * @param[in]  buffer     same as for getpwnam_r(3)
     * @param[in]  buflen     same as for getpwnam_r(3)
     * @param[out] result     same as for getpwnam_r(3)
     * @param[in]  flags      flags to control the behavior and the results of the
     *                        call
     * @param[in]  timeout    timeout in milliseconds
     *
     * @return
     *  - 0:
     *  - ENOENT:    no user with the given name found
     *  - ERANGE:    Insufficient buffer space supplied
     *  - ETIME:     request timed out but was send to SSSD
     *  - ETIMEDOUT: request timed out but was not send to SSSD
     */
    int sss_nss_getpwnam_timeout(const char *name, struct passwd *pwd,
                                 char *buffer, size_t buflen,
                                 struct passwd **result,
                                 uint32_t flags, unsigned int timeout);

    /**
     * @brief Return user information based on the user uid
     *
     * @param[in]  uid        same as for getpwuid_r(3)
     * @param[in]  pwd        same as for getpwuid_r(3)
     * @param[in]  buffer     same as for getpwuid_r(3)
     * @param[in]  buflen     same as for getpwuid_r(3)
     * @param[out] result     same as for getpwuid_r(3)
     * @param[in]  flags      flags to control the behavior and the results of the
     *                        call
     * @param[in]  timeout    timeout in milliseconds
     *
     * @return
     *  - 0:
     *  - ENOENT:    no user with the given uid found
     *  - ERANGE:    Insufficient buffer space supplied
     *  - ETIME:     request timed out but was send to SSSD
     *  - ETIMEDOUT: request timed out but was not send to SSSD
     */
    int sss_nss_getpwuid_timeout(uid_t uid, struct passwd *pwd,
                                 char *buffer, size_t buflen,
                                 struct passwd **result,
                                 uint32_t flags, unsigned int timeout);

    /**
     * @brief Return group information based on the group name
     *
     * @param[in]  name       same as for getgrnam_r(3)
     * @param[in]  pwd        same as for getgrnam_r(3)
     * @param[in]  buffer     same as for getgrnam_r(3)
     * @param[in]  buflen     same as for getgrnam_r(3)
     * @param[out] result     same as for getgrnam_r(3)
     * @param[in]  flags      flags to control the behavior and the results of the
     *                        call
     * @param[in]  timeout    timeout in milliseconds
     *
     * @return
     *  - 0:
     *  - ENOENT:    no group with the given name found
     *  - ERANGE:    Insufficient buffer space supplied
     *  - ETIME:     request timed out but was send to SSSD
     *  - ETIMEDOUT: request timed out but was not send to SSSD
     */
    int sss_nss_getgrnam_timeout(const char *name, struct group *grp,
                                 char *buffer, size_t buflen, struct group **result,
                                 uint32_t flags, unsigned int timeout);

    /**
     * @brief Return group information based on the group gid
     *
     * @param[in]  gid        same as for getgrgid_r(3)
     * @param[in]  pwd        same as for getgrgid_r(3)
     * @param[in]  buffer     same as for getgrgid_r(3)
     * @param[in]  buflen     same as for getgrgid_r(3)
     * @param[out] result     same as for getgrgid_r(3)
     * @param[in]  flags      flags to control the behavior and the results of the
     *                        call
     * @param[in]  timeout    timeout in milliseconds
     *
     * @return
     *  - 0:
     *  - ENOENT:    no group with the given gid found
     *  - ERANGE:    Insufficient buffer space supplied
     *  - ETIME:     request timed out but was send to SSSD
     *  - ETIMEDOUT: request timed out but was not send to SSSD
     */
    int sss_nss_getgrgid_timeout(gid_t gid, struct group *grp,
                                 char *buffer, size_t buflen, struct group **result,
                                 uint32_t flags, unsigned int timeout);

    /**
     * @brief Return a list of groups to which a user belongs
     *
     * @param[in]      name       name of the user
     * @param[in]      group      same as second argument of getgrouplist(3)
     * @param[in]      groups     array of gid_t of size ngroups, will be filled
     *                            with GIDs of groups the user belongs to
     * @param[in,out]  ngroups    size of the groups array on input. On output it
     *                            will contain the actual number of groups the
     *                            user belongs to. With a return value of 0 the
     *                            groups array was large enough to hold all group.
     *                            With a return value of ERANGE the array was not
     *                            large enough and ngroups will have the needed
     *                            size.
     * @param[in]  flags          flags to control the behavior and the results of
     *                            the call
     * @param[in]  timeout        timeout in milliseconds
     *
     * @return
     *  - 0:         success
     *  - ENOENT:    no user with the given name found
     *  - ERANGE:    Insufficient buffer space supplied
     *  - ETIME:     request timed out but was send to SSSD
     *  - ETIMEDOUT: request timed out but was not send to SSSD
     */
    int sss_nss_getgrouplist_timeout(const char *name, gid_t group,
                                     gid_t *groups, int *ngroups,
                                     uint32_t flags, unsigned int timeout);
    /**
     * @brief Find SID by fully qualified name with timeout
     *
     * @param[in] fq_name  Fully qualified name of a user or a group
     * @param[in] timeout  timeout in milliseconds
     * @param[out] sid     String representation of the SID of the requested user
     *                     or group, must be freed by the caller
     * @param[out] type    Type of the object related to the given name
     *
     * @return
     *  - 0 (EOK): success, sid contains the requested SID
     *  - ENOENT: requested object was not found in the domain extracted from the given name
     *  - ENETUNREACH: SSSD does not know how to handle the domain extracted from the given name
     *  - ENOSYS: this call is not supported by the configured provider
     *  - EINVAL: input cannot be parsed
     *  - EIO: remote servers cannot be reached
     *  - EFAULT: any other error
     *  - ETIME:     request timed out but was send to SSSD
     *  - ETIMEDOUT: request timed out but was not send to SSSD
     */
    int sss_nss_getsidbyname_timeout(const char *fq_name, unsigned int timeout,
                                     char **sid, enum sss_id_type *type);

    /**
     * @brief Find SID by a POSIX UID or GID with timeout
     *
     * @param[in] id       POSIX UID or GID
     * @param[in] timeout  timeout in milliseconds
     * @param[out] sid     String representation of the SID of the requested user
     *                     or group, must be freed by the caller
     * @param[out] type    Type of the object related to the given ID
     *
     * @return
     *  - see #sss_nss_getsidbyname_timeout
     */
    int sss_nss_getsidbyid_timeout(uint32_t id, unsigned int timeout,
                                   char **sid, enum sss_id_type *type);

    /**
     * @brief Return the fully qualified name for the given SID with timeout
     *
     * @param[in] sid      String representation of the SID
     * @param[in] timeout  timeout in milliseconds
     * @param[out] fq_name Fully qualified name of a user or a group,
     *                     must be freed by the caller
     * @param[out] type    Type of the object related to the SID
     *
     * @return
     *  - see #sss_nss_getsidbyname_timeout
     */
    int sss_nss_getnamebysid_timeout(const char *sid, unsigned int timeout,
                                     char **fq_name, enum sss_id_type *type);

    /**
     * @brief Return the POSIX ID for the given SID with timeout
     *
     * @param[in] sid      String representation of the SID
     * @param[in] timeout  timeout in milliseconds
     * @param[out] id      POSIX ID related to the SID
     * @param[out] id_type Type of the object related to the SID
     *
     * @return
     *  - see #sss_nss_getsidbyname_timeout
     */
    int sss_nss_getidbysid_timeout(const char *sid, unsigned int timeout,
                                   uint32_t *id, enum sss_id_type *id_type);

    /**
     * @brief Find original data by fully qualified name with timeout
     *
     * @param[in] fq_name  Fully qualified name of a user or a group
     * @param[in] timeout  timeout in milliseconds
     * @param[out] kv_list A NULL terminate list of key-value pairs where the key
     *                     is the attribute name in the cache of SSSD,
     *                     must be freed by the caller with sss_nss_free_kv()
     * @param[out] type    Type of the object related to the given name
     *
     * @return
     *  - 0 (EOK): success, sid contains the requested SID
     *  - ENOENT: requested object was not found in the domain extracted from the given name
     *  - ENETUNREACH: SSSD does not know how to handle the domain extracted from the given name
     *  - ENOSYS: this call is not supported by the configured provider
     *  - EINVAL: input cannot be parsed
     *  - EIO: remote servers cannot be reached
     *  - EFAULT: any other error
     *  - ETIME:     request timed out but was send to SSSD
     *  - ETIMEDOUT: request timed out but was not send to SSSD
     */
    int sss_nss_getorigbyname_timeout(const char *fq_name, unsigned int timeout,
                                      struct sss_nss_kv **kv_list,
                                      enum sss_id_type *type);

    /**
     * @brief Return the fully qualified name for the given base64 encoded
     * X.509 certificate in DER format with timeout
     *
     * @param[in] cert     base64 encoded certificate
     * @param[in] timeout  timeout in milliseconds
     * @param[out] fq_name Fully qualified name of a user or a group,
     *                     must be freed by the caller
     * @param[out] type    Type of the object related to the cert
     *
     * @return
     *  - see #sss_nss_getsidbyname_timeout
     */
    int sss_nss_getnamebycert_timeout(const char *cert, unsigned int timeout,
                                      char **fq_name, enum sss_id_type *type);

    /**
     * @brief Return a list of fully qualified names for the given base64 encoded
     * X.509 certificate in DER format with timeout
     *
     * @param[in] cert     base64 encoded certificate
     * @param[in] timeout  timeout in milliseconds
     * @param[out] fq_name List of fully qualified name of users or groups,
     *                     must be freed by the caller
     * @param[out] type    List of types of the objects related to the cert
     *
     * @return
     *  - see #sss_nss_getsidbyname_timeout
     */
    int sss_nss_getlistbycert_timeout(const char *cert, unsigned int timeout,
                                      char ***fq_name, enum sss_id_type **type);

    #endif /* IPA_389DS_PLUGIN_HELPER_CALLS */

As can be seen the existing calls from ``libsss_nss_idmap.so`` got a
``*_timeout`` variant as well.

SSSD responder side
~~~~~~~~~~~~~~~~~~~
The SSSD NSS responder has to be prepared to accept the flags in the request.
Currently only a name or an ID are expected. To handle this new request types:

 * SSS_NSS_GETPWNAM_EX
 * SSS_NSS_GETPWUID_EX
 * SSS_NSS_GETGRNAM_EX
 * SSS_NSS_GETGRGID_EX
 * SSS_NSS_INITGR_EX

will be added. If the flags are not set, will behave as the non-EX calls.

If ``SSS_NSS_EX_FLAG_NO_CACHE`` is set, ``cache_req_data_set_bypass_cache()``
will be called so that the cache-request framework will directly request new
data from the backend.

If ``SSS_NSS_EX_FLAG_INVALIDATE_CACHE`` is set,
``cache_req_data_set_bypass_dp()`` (which will be implemented with this
feature) will be called to only search the requested object in the cache. If it
was found, the cached entry will be invalidated in both on-disk and memory cache.
If ``SSS_NSS_EX_FLAG_INVALIDATE_CACHE`` was sent with SSS_NSS_INITGR_EX, both
the groupmembership data and the plain user data will be invalidated.

The flags ``SSS_NSS_EX_FLAG_NO_CACHE`` and ``SSS_NSS_EX_FLAG_INVALIDATE_CACHE``
cannot be used at the same time.

Configuration changes
---------------------
There are no configuration changes needed to use the new library calls.

How To Test
-----------
To test the new calls they should be used in C-programs.

How To Debug
------------
``libsss_nss_idmap`` currently does not has any logging infrastructure so only
the debug logs of the SSSD responder are available.

If the ``SSS_NSS_EX_FLAG_NO_CACHE`` or ``SSS_NSS_EX_FLAG_INVALIDATE_CACHE`` are
used on the client side, ``strace`` can be used to see whether the client skips the
memory cache as expected.

Authors
-------
 * Sumit Bose <sbose@redhat.com>
