SUDO integration proposal using sudo policy plugin
==================================================

SUDO plugin API
---------------

Since version 1.8 SUDO supports replacing standard policy behaviour
using plugins.

Referral plugin API documentation can be found here:
`http://www.gratisoft.us/sudo/man/1.8.2/sudo\_plugin.man.html <http://www.gratisoft.us/sudo/man/1.8.2/sudo_plugin.man.html>`__

Basically to create a policy plugin, one must define a policy\_plugin
structure: ::

    struct policy_plugin {
     #define SUDO_POLICY_PLUGIN    1
         unsigned int type; /* always SUDO_POLICY_PLUGIN */
         unsigned int version; /* always SUDO_API_VERSION */
         int (*open)(unsigned int version, sudo_conv_t conversation,
                     sudo_printf_t plugin_printf, char * const settings[],
                     char * const user_info[], char * const user_env[]);
         void (*close)(int exit_status, int error);
         int (*show_version)(int verbose);
         int (*check_policy)(int argc, char * const argv[],
                             char *env_add[], char **command_info[],
                             char **argv_out[], char **user_env_out[]);
         int (*list)(int argc, char * const argv[], int verbose,
                     const char *list_user);
         int (*validate)(void);
         void (*invalidate)(int remove);
         int (*init_session)(struct passwd *pwd);
     };

To use the plugin, just edit /etc/sudo.conf: ::

    Plugin policy_struct_name plugin.so

Only one policy plugin may be configured.

The most important functions are open(), close() and check\_policy().

open()
~~~~~~

Initializes plugin with data passed by SUDO as arguments of this
function.

close()
~~~~~~~

Does a data clean up and checks a return code of the command.

check\_policy()
~~~~~~~~~~~~~~~

Determines whether the user can run the command or not.

Integration in SSSD
-------------------

.. FIXME:  Missing "high level view of integration" image

SSSD SUDO plugin
----------------

All decision logic is done by responder and therefore this plugin should
be as light weight as possible.

Communication with responder is done by SSS CLI sockets interface.

.. FIXME: Missing "SSSD Sudo plugin" image

SSSD SUDO responder
-------------------

Plugin <=> responder protocol
-----------------------------

Query
~~~~~

Byte array with format: ::

    qualified_command_path\0argv[0]\0argv[i]\0\0env_add\0\0user_env\0\0settings\0\0user_info\0\0

where env\_add, user\_env, settings and user\_info are in the form of
NAME=VALUE pairs.

All fields are interpreted as char\*.

**qualified\_command\_path** is a full name of executed command
(/bin/ls, ./my-program)

**argv[]** arguments passed to executed programs

**env\_add** environment variables that user wants to add

**user\_env** current environment variables (provided in open() function
by SUDO)

**settings** provided in open() function by SUDO (see plugin API open())

**user\_info** provided in open() function by SUDO (see plugin API
open())

Response
~~~~~~~~

Byte array with format: ::

    (result)argv\0\0command_info\0\0user_env\0\0

where command\_info and user\_env are in the form of NAME=VALUE pairs.

All fields except result are interpreted as char\*.

**result** interpreted as an integer value

**argv[]** arguments passed to executed programs

**command\_info** information about the command (see plugin API
check\_policy())

**user\_env** environment variables that should be kept / added.
