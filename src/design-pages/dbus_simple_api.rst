.. highlight:: none

Simple D-Bus API wrapper library
================================

Related ticket(s):

-  `Create a library to simplify usage of D-Bus
   responder <https://pagure.io/SSSD/sssd/issue/2254>`__

Problem Statement
-----------------

Using D-Bus requires a significant amount of knowledge of D-Bus and its
underlying library API. Libraries like libdbus or libdbus\_glib are
quite complex and requires a lot of code to do even the simplest things.
The purpose of this document is to describe a new public API to access
most fundamental parts of SSSD's D-Bus responder in a simple way so that
a user doesn't have to deal with D-Bus at all.

Prerequisites
-------------

-  Each attribute of every D-Bus object accessible via this API is
   represented as string.
-  Naming convention of D-Bus methods:

   -  **List<class><condition>(arg1, ...)** returning array of object
      paths

      -  ListUsers()
      -  ListDomains()
      -  ListUsersByName(filter)
      -  ListGroupsByName(filter)

   -  **Find<class><condition>(arg1, ...)** returning single object path

      -  FindUserById(id)
      -  FindDomainByName(name)

The API
-------

 ::

    /**
     * @defgroup sss_dbus Simple interface to SSSD InfoPipe responder.
     * Libsss_dbus provides a synchronous interface to simplify basic communication
     * with SSSD InfoPipe responder.
     * @{
     */

    /** SSSD InfoPipe bus address */
    #define SSS_DBUS_IFP "org.freedesktop.sssd.infopipe"

    /** SSSD InfoPipe interface */
    #define SSS_DBUS_IFACE_IFP SSS_DBUS_IFP
    #define SSS_DBUS_IFACE_COMPONENTS "org.freedesktop.sssd.infopipe.Components"
    #define SSS_DBUS_IFACE_SERVICES "org.freedesktop.sssd.infopipe.Services"
    #define SSS_DBUS_IFACE_DOMAINS "org.freedesktop.sssd.infopipe.Domains"
    #define SSS_DBUS_IFACE_USERS "org.freedesktop.sssd.infopipe.Users"
    #define SSS_DBUS_IFACE_GROUPS "org.freedesktop.sssd.infopipe.Groups"

    /**
     * Opaque libsss_dbus context. One context shall not be used by multiple
     * threads. Each thread needs to create and use its own context.
     *
     * @see sss_dbus_init
     * @see sss_dbus_init_ex
     */
    typedef struct sss_dbus_ctx sss_dbus_ctx;

    /**
     * Typedef for memory allocation functions
     */
    typedef void (sss_dbus_free_func)(void *ptr, void *pvt);
    typedef void *(sss_dbus_alloc_func)(size_t size, void *pvt);

    /**
     * Error codes used by libsss_dbus
     */
    typedef enum sss_dbus_error {
        /** Success */
        SSS_DBUS_OK = 0,

        /** Ran out of memory during processing */
        SSS_DBUS_OUT_OF_MEMORY,

        /** Invalid argument */
        SSS_DBUS_INVALID_ARGUMENT,

        /**
         * Input/output error
         *
         * @see sss_dbus_get_last_io_error() to get more information
         */
        SSS_DBUS_IO_ERROR,

        /** Internal error */
        SSS_DBUS_INTERNAL_ERROR,

        /** Operation not supported */
        SSS_DBUS_NOT_SUPPORTED,

        /** Attribute does not exist */
        SSS_DBUS_ATTR_MISSING,

        /** Attribute does not have any value set */
        SSS_DBUS_ATTR_NULL,

        /** Incorrect attribute type */
        SSS_DBUS_INCORRECT_TYPE,

        /** Always last */
        SSS_DBUS_ERROR_SENTINEL
    } sss_dbus_error;

    /**
     * Boolean type
     */
    typedef uint32_t sss_dbus_bool;

    /**
     * D-Bus object attribute
     */
    typedef struct sss_dbus_attr sss_dbus_attr;

    /**
     * String dictionary
     */
    typedef struct {
        char *key;
        char **values;
        unsigned int num_values;
    } sss_dbus_str_dict;

    /**
     * D-Bus object
     */
    typedef struct sss_dbus_object {
        char *name;
        char *object_path;
        char *interface;
        sss_dbus_attr **attrs;
    } sss_dbus_object;

    /**
     * @brief Initialize sss_dbus context using default allocator (malloc)
     *
     * @param[out] _ctx sss_dbus context
     */
    sss_dbus_error
    sss_dbus_init(sss_dbus_ctx **_ctx);

    /**
     * @brief Initialize sss_dbus context
     *
     * @param[in] alloc_pvt  Private data for allocation routine
     * @param[in] alloc_func Function to allocate memory for the context, if
     *                       NULL malloc() is used
     * @param[in] free_func  Function to free the memory of the context, if
     *                       NULL free() is used
     * @param[out] _ctx      sss_dbus context
     */
    sss_dbus_error
    sss_dbus_init_ex(void *alloc_pvt,
                     sss_dbus_alloc_func *alloc_func,
                     sss_dbus_free_func *free_func,
                     sss_dbus_ctx **_ctx);

    /**
     * @brief Return last error message from underlying D-Bus communication
     *
     * @param[in] ctx sss_dbus context
     * @return Error message or NULL if no error occurred during last D-Bus call.
     */
    const char *
    sss_dbus_get_last_io_error(sss_dbus_ctx *ctx);

    /**
     * @brief Return default interface for object with path @object_path.
     *
     * @param[in] ctx object_path D-Bus object path
     * @return Interface name or NULL if the object path is unknown.
     */
    const char *
    sss_dbus_get_iface_for_object(const char *object_path);

    /**
     * @brief Create message for SSSD InfoPipe bus.
     *
     * @param[in] object_path D-Bus object path
     * @param[in] interface   D-Bus interface
     * @param[in] method      D-Bus method
     *
     * @return D-Bus message.
     */
    DBusMessage *
    sss_dbus_create_message(const char *object_path,
                            const char *interface,
                            const char *method);

    /**
     * @brief Send D-Bus message to SSSD InfoPipe bus.
     *
     * @param[in] ctx         sss_dbus context
     * @param[in] interface   D-Bus interface
     * @param[in] object_path D-Bus object path
     * @param[in] method      D-Bus method
     *
     * @return D-Bus message.
     */
    sss_dbus_error
    sss_dbus_send_message(sss_dbus_ctx *ctx,
                          DBusMessage *msg,
                          DBusMessage **_reply);

    /**
     * @brief Fetch selected attributes of given object.
     *
     * @param[in] ctx         sss_dbus context
     * @param[in] object_path D-Bus object path
     * @param[in] interface   D-Bus interface
     * @param[in] name        Name of desired attribute
     * @param[out] _attrs     List of acquired attributes
     */
    sss_dbus_error
    sss_dbus_fetch_attr(sss_dbus_ctx *ctx,
                        const char *object_path,
                        const char *name,
                        const char *interface,
                        sss_dbus_attr ***_attrs);

    /**
     * @brief Fetch all attributes of given object.
     *
     * @param[in] ctx         sss_dbus context
     * @param[in] object_path D-Bus object path
     * @param[in] interface   D-Bus interface
     * @param[out] _attrs     Acquired attributes
     */
    sss_dbus_error
    sss_dbus_fetch_all_attrs(sss_dbus_ctx *ctx,
                             const char *object_path,
                             const char *interface,
                             sss_dbus_attr ***_attrs);

    /**
     * @brief Fetch D-Bus object.
     *
     * @param[in] ctx         sss_dbus context
     * @param[in] object_path D-Bus object path
     * @param[in] interface   D-Bus interface
     * @param[out] _object    Object and its attributes
     */
    sss_dbus_error
    sss_dbus_fetch_object(sss_dbus_ctx *ctx,
                          const char *object_path,
                          const char *interface,
                          sss_dbus_object **_object);

    /**
     * @brief List objects that satisfies given conditions. This routine will
     * invoke List<method> D-Bus method on SSSD InfoPipe interface. Arguments
     * to this method are given as standard variadic D-Bus arguments.
     *
     * @param[in] ctx            sss_dbus context
     * @param[in] method         D-Bus method to call without the 'List' prefix
     * @param[out] _object_paths List of object paths
     * @param[in] first_arg_type Type of the first D-Bus argument
     * @param[in] ...            D-Bus arguments
     */
    sss_dbus_error
    sss_dbus_invoke_list(sss_dbus_ctx *ctx,
                         const char *method,
                         char ***_object_paths,
                         int first_arg_type,
                         ...);

    /**
     * @brief Find single object that satisfies given conditions. This routine will
     * invoke Find<method> D-Bus method on SSSD InfoPipe interface. Arguments
     * to this method are given as standard variadic D-Bus arguments.
     *
     * @param[in] ctx            sss_dbus context
     * @param[in] method         D-Bus method to call without the 'Find' prefix
     * @param[out] _object_path Object path
     * @param[in] first_arg_type Type of the first D-Bus argument
     * @param[in] ...            D-Bus arguments
     */
    sss_dbus_error
    sss_dbus_invoke_find(sss_dbus_ctx *ctx,
                         const char *method,
                         char **_object_path,
                         int first_arg_type,
                         ...);

    /**
     * @brief Find attribute in list and return its value.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _value Output value
     */
    sss_dbus_error
    sss_dbus_find_attr_as_bool(sss_dbus_attr **attrs,
                               const char *name,
                               sss_dbus_bool *_value);

    /**
     * @brief Find attribute in list and return its value.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _value Output value
     */
    sss_dbus_error
    sss_dbus_find_attr_as_int16(sss_dbus_attr **attrs,
                                const char *name,
                                int16_t *_value);

    /**
     * @brief Find attribute in list and return its value.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _value Output value
     */
    sss_dbus_error
    sss_dbus_find_attr_as_uint16(sss_dbus_attr **attrs,
                                 const char *name,
                                 uint16_t *_value);

    /**
     * @brief Find attribute in list and return its value.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _value Output value
     */
    sss_dbus_error
    sss_dbus_find_attr_as_int32(sss_dbus_attr **attrs,
                                const char *name,
                                int32_t *_value);

    /**
     * @brief Find attribute in list and return its value.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _value Output value
     */
    sss_dbus_error
    sss_dbus_find_attr_as_uint32(sss_dbus_attr **attrs,
                                 const char *name,
                                 uint32_t *_value);

    /**
     * @brief Find attribute in list and return its value.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _value Output value
     */
    sss_dbus_error
    sss_dbus_find_attr_as_int64(sss_dbus_attr **attrs,
                                const char *name,
                                int64_t *_value);

    /**
     * @brief Find attribute in list and return its value.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _value Output value
     */
    sss_dbus_error
    sss_dbus_find_attr_as_uint64(sss_dbus_attr **attrs,
                                 const char *name,
                                 uint64_t *_value);

    /**
     * @brief Find attribute in list and return its value.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _value Output value
     */
    sss_dbus_error
    sss_dbus_find_attr_as_string(sss_dbus_attr **attrs,
                                 const char *name,
                                 const char **_value);

    /**
     * @brief Find attribute in list and return its value.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _value Output value
     */
    sss_dbus_error
    sss_dbus_find_attr_as_string_dict(sss_dbus_attr **attrs,
                                      const char *name,
                                      sss_dbus_str_dict *_value);

    /**
     * @brief Find attribute in list and return its values.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _num_values Number of values in the array
     * @param[out] _values Output array
     */
    sss_dbus_error
    sss_dbus_find_attr_as_bool_array(sss_dbus_attr **attrs,
                                     const char *name,
                                     unsigned int *_num_values,
                                     sss_dbus_bool **_value);

    /**
     * @brief Find attribute in list and return its values.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _num_values Number of values in the array
     * @param[out] _values Output array
     */
    sss_dbus_error
    sss_dbus_find_attr_as_int16_array(sss_dbus_attr **attrs,
                                      const char *name,
                                      unsigned int *_num_values,
                                      int16_t **_value);

    /**
     * @brief Find attribute in list and return its values.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _num_values Number of values in the array
     * @param[out] _values Output array
     */
    sss_dbus_error
    sss_dbus_find_attr_as_uint16_array(sss_dbus_attr **attrs,
                                       const char *name,
                                       unsigned int *_num_values,
                                       uint16_t **_value);

    /**
     * @brief Find attribute in list and return its values.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _num_values Number of values in the array
     * @param[out] _values Output array
     */
    sss_dbus_error
    sss_dbus_find_attr_as_int32_array(sss_dbus_attr **attrs,
                                      const char *name,
                                      unsigned int *_num_values,
                                      int32_t **_value);

    /**
     * @brief Find attribute in list and return its values.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _num_values Number of values in the array
     * @param[out] _values Output array
     */
    sss_dbus_error
    sss_dbus_find_attr_as_uint32_array(sss_dbus_attr **attrs,
                                       const char *name,
                                       unsigned int *_num_values,
                                       uint32_t **_value);

    /**
     * @brief Find attribute in list and return its values.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _num_values Number of values in the array
     * @param[out] _values Output array
     */
    sss_dbus_error
    sss_dbus_find_attr_as_int64_array(sss_dbus_attr **attrs,
                                      const char *name,
                                      unsigned int *_num_values,
                                      int64_t **_value);

    /**
     * @brief Find attribute in list and return its values.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _num_values Number of values in the array
     * @param[out] _values Output array
     */
    sss_dbus_error
    sss_dbus_find_attr_as_uint64_array(sss_dbus_attr **attrs,
                                       const char *name,
                                       unsigned int *_num_values,
                                       uint64_t **_value);

    /**
     * @brief Find attribute in list and return its values.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _num_values Number of values in the array
     * @param[out] _values Output array
     */
    sss_dbus_error
    sss_dbus_find_attr_as_string_array(sss_dbus_attr **attrs,
                                       const char *name,
                                       unsigned int *_num_values,
                                       const char * const **_value);

    /**
     * @brief Find attribute in list and return its values.
     *
     * @param[in] attrs Attributes
     * @param[in] name Name of the attribute to find
     * @param[out] _num_values Number of values in the array
     * @param[out] _values Output array
     */
    sss_dbus_error
    sss_dbus_find_attr_as_string_dict_array(sss_dbus_attr **attrs,
                                            const char *name,
                                            unsigned int *_num_values,
                                            sss_dbus_str_dict **_value);

    /**
     * @brief Free sss_dbus context and set it to NULL.
     *
     * @param[in,out] _ctx sss_dbus context
     */
    void
    sss_dbus_free(sss_dbus_ctx **_ctx);

    /**
     * @brief Free attribute list and set it to NULL.
     *
     * @param[in,out] _attrs Attributes
     */
    void
    sss_dbus_free_attrs(sss_dbus_ctx *ctx,
                        sss_dbus_attr ***_attrs);

    /**
     * @brief Free sss_dbus object and set it to NULL.
     *
     * @param[in,out] _object Object
     */
    void
    sss_dbus_free_object(sss_dbus_ctx *ctx,
                         sss_dbus_object **_object);

    /**
     * @brief Free string and set it to NULL.
     *
     * @param[in,out] _str String
     */
    void
    sss_dbus_free_string(sss_dbus_ctx *ctx,
                         char **_str);

    /**
     * @brief Free array of strings and set it to NULL.
     *
     * @param[in,out] _str_array Array of strings
     */
    void
    sss_dbus_free_string_array(sss_dbus_ctx *ctx,
                               char ***_str_array);

    /**
     * @}
     */

    /**
     * @defgroup common Most common use cases of SSSD InfoPipe responder.
     * @{
     */

    /**
     * @brief List names of available domains.
     *
     * @param[in] ctx       sss_dbus context
     * @param[out] _domains List of domain names
     */
    sss_dbus_error
    sss_dbus_list_domains(sss_dbus_ctx *ctx,
                          char ***_domains);

    /**
     * @brief Fetch all information about domain by name.
     *
     * @param[in] ctx      sss_dbus context
     * @param[in] name     Domain name
     * @param[out] _domain Domain object
     */
    sss_dbus_error
    sss_dbus_fetch_domain_by_name(sss_dbus_ctx *ctx,
                                  const char *name,
                                  sss_dbus_object **_domain);

    /**
     * @brief Fetch all information about user by uid.
     *
     * @param[in] ctx    sss_dbus context
     * @param[in] uid    User ID
     * @param[out] _user User object
     */
    sss_dbus_error
    sss_dbus_fetch_user_by_uid(sss_dbus_ctx *ctx,
                               uid_t uid,
                               sss_dbus_object **_user);

    /**
     * @brief Fetch all information about user by name.
     *
     * @param[in] ctx    sss_dbus context
     * @param[in] name   User name
     * @param[out] _user User object
     */
    sss_dbus_error
    sss_dbus_fetch_user_by_name(sss_dbus_ctx *ctx,
                                const char *name,
                                sss_dbus_object **_user);

    /**
     * @}
     */

Authors
-------

-  Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>
