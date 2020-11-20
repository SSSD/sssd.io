Sudo Plugin Wire Protocol
=========================

Sudo v1.8 supports a plugin API that can be used to extend features of
SUDO. These pluggable modules can be of two types

#. Policy Plugin
#. I/O log Plugin

Policy plugin can determine whether the user is allowed run the
specified command as specified user. Only one policy plugin may be
loaded at a time. Where as the I/O log plugin logs the session to local
file including the tty input/output, stdin, stdout, stderr etc. Through
this policy plugin the user can different security policies that can be
plugged into action. In the forwarder plugin we are not using I/O plugin
to log data.


Policy Plugin
-------------

open()
~~~~~~

::

    int (*open)(unsigned int version, sudo_conv_t conversation,
                     sudo_printf_t plugin_printf, char * const settings[],
                     char * const user_info[], char * const user_env[]);

This function opens the connection between plugin and SUDO

**Input**

@param[in] version - The major and minor version number of the plugin
API

@param[in] conversation - A pointer to the conversation function that
can be used by the plugin to interact with the user (see below). Returns
0 on success and -1 on failure.

@param[in] plugin\_printf - A pointer to a printf-style function that
may be used to display informational or error messages

@param[in] user\_info - A vector of user-supplied sudo settings in the
form of "name=value" strings. The vector is terminated by a NULL
pointer.

@param[in] user\_env - A vector of information about the user running
the command in the form of "name=value" strings. The vector is
terminated by a NULL pointer.

**Output**

@return 1 success

@return 0 failure

@return -1 general error

@return -2 usage error,

If an error occurs, the plugin may optionally call the conversation or
plugin\_printf function with SUDO\_CONF\_ERROR\_MSG to present
additional error information to the user.

close()
~~~~~~~

::

    void (*close)(int exit_status, int error);

The close function is called when the command being run by sudo
finishes.

**Input**

@param[in] exit\_status - The command's exit status, as returned by the
wait system call. The value of exit\_status is undefined if error is
non-zero.

@param[out] error - If the command could not be executed, this is set to
the value of errno set by the execve system call. If the command was
successfully executed, the value of error is 0.

check\_policy()
~~~~~~~~~~~~~~~

::

    int (*check_policy)(int argc, char * const argv[]
                         char *env_add[], char **command_info[],
                         char **argv_out[], char **user_env_out[]);

The check\_policy function is called by sudo to determine whether the
user is allowed to run the specified commands.

**Input**

@param[in] argc - The number of elements in argv, not counting the final
NULL pointer.

@param[in] argv - The argument vector describing the command the user
wishes to run, in the same form as what would be passed to the execve()
system call which is terminated by a NULL pointer.

@param[in] env\_add - Additional environment variables specified by the
user on the command line in the form of a NULL-terminated vector of
"name=value" strings.

@param[in] command\_info - Information about the command being run in
the form of "name=value" strings.

@param[out] argv\_out - The NULL-terminated argument vector to pass to
the execve() system call when executing the command.

@param[in] user\_env\_out - The NULL-terminated environment vector to
use when executing the command.

**Output**

@return 1 - Command is allowed

@return -1 - general error

@return -2 - usage error

If an error occurs, the plugin may optionally call the conversation or
plugin\_printf function with SUDO\_CONF\_ERROR\_MSG to present
additional error information to the user.

validate()
~~~~~~~~~~

::

    int (*validate)(void);

The validate function is called when sudo is run with the -v flag. For
policy plugins such as sudoers that cache authentication credentials,
this function will validate and cache the credentials. i.e, sudo will
update the user's cached credentials, authenticating the user's password
if necessary. The default sudoers plugin caches the user credential for
a timeout of 5 minutes. The invocation of validate function through
'sudo -v' flag extends the timeout of the user credentials after
authentication if necessary.

No Input

**Output**

@return 1 - success

@return 0 - failure

@return -1 - error

On error, the plugin may optionally call the conversation or
plugin\_printf function with SUDO\_CONF\_ERROR\_MSG to present
additional error information to the user.

invalidate()
~~~~~~~~~~~~

::

    void (*invalidate)(int remove);

The invalidate function is called when sudo is called with the -k or -K
flag. This function will invalidate the credentials. i.e, the user
credentials will be marked as invalid so that on the nest invocation of
sudo user will be forcefully prompted undergo the authentication
procedures. The invalidate function should be NULL if the plugin does
not support credential caching.

**Input**

@param[in] remove - If the remove flag is set, the plugin may remove the
credentials instead of simply invalidating them.

Conversation API & Printf-style functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

     typedef int (*sudo_conv_t)(int num_msgs,
                  const struct sudo_conv_message msgs[],
                  struct sudo_conv_reply replies[]);

     typedef int (*sudo_printf_t)(int msg_type, const char *fmt, ...);

If the plugin needs to interact with the user or display informational
or error messages, it may do so via the conversation function. The
caller must include a trailing newline in msg if one is to be printed.
The messages are passed in the the msg[] array of sudo\_conv\_messages
and the replies are received in the array sudo\_conv\_reply structures.

The format of sudo\_conv\_messages and sudo\_conv\_reply are

::

     struct sudo_conv_message {
         int msg_type;
         int timeout;
         const char *msg;
     };

     struct sudo_conv_reply {
         char *reply;
     };

A printf-style function is also available that can be used to
display informational or error messages to the user, which is
usually more convenient for simple messages where no use input is
required.

The msg\_type can be any one of these

::

     SUDO_CONV_PROMPT_ECHO_OFF    /* do not echo user input */
     SUDO_CONV_PROMPT_ECHO_ON     /* echo user input */
     SUDO_CONV_ERROR_MSG          /* error message */
     SUDO_CONV_INFO_MSG           /* informational message */
     SUDO_CONV_PROMPT_MASK        /* mask user input */
     SUDO_CONV_PROMPT_ECHO_OK     /* flag: allow echo if no tty */

The formatted string given in the printf-style function is printed to
the screen.

THE PLUGIN WIRE PROTOCOL
------------------------

This is the structure of message packet that is sent from plugin to
SSSD responder for getting the authentication result.

The structure is as shown below.

Each string message is grouped into a container of format: ::

    message_type +(uint32_t) message_size + message_string

and each integer messages are grouped into container as: ::

    message_type+ sizeof( uint32_t ) + (uint32_t)integer_value

So that string message occupies a space of { 2\*(sizeof
uint32\_t)+sizeof string } and integer type takes a space of {
3\*(sizeof uint32\_t) }

message\_type : is defined at "sss\_sudo\_cli.h" as **enum
sudo\_item\_type**

The message format will be: ::

    start_header + message_container1 + message_container2 + ........ + message_containerN + stop_header.

where: ::

    start\_header : SSS\_START\_OF\_SUDO\_REQUEST
    end\_header : SSS\_END\_OF\_SUDO\_REQUEST

The messages are: ::

    MESSAGE                            MESSAGE TYPE                     DESCRIPTION


    uid                                SSS_SUDO_ITEM_UID                UID of the user

    Current directory                  SSS_SUDO_ITEM_CWD                Current working directory of the user

    tty                                SSS_SUDO_ITEM_TTY                tty used by the user

    Run as user                        SSS_SUDO_ITEM_RUSER              User name to run the command as

    run as group                       SSS_SUDO_ITEM_RGROUP             group name to run the command as

    prompt to be used                  SSS_SUDO_ITEM_PROMPT             Prompt to be used when credentials are requested

    network address                    SSS_SUDO_ITEM_NETADDR            Network address of user

    Use sudo edit                      SSS_SUDO_ITEM_USE_SUDOEDIT       Use sudo edit instead of sudo

    set HOME to target user's home     SSS_SUDO_ITEM_USE_SETHOME        set HOME env variable to target user's home

    preserve environment               SSS_SUDO_ITEM_USE_PRESERV_ENV    Preserve the environment to be used

    implied shell support              SSS_SUDO_ITEM_USE_IMPLIED_SHELL  use sudo without any command

    Use login shell                    SSS_SUDO_ITEM_USE_LOGIN_SHELL    indicates that user want to run a login shell

    Run a shell                        SSS_SUDO_ITEM_USE_RUN_SHELL      Want to run a shell instead of command

    preserve groups                    SSS_SUDO_ITEM_USE_PRE_GROUPS     Preserve group information

    ignore cached results              SSS_SUDO_ITEM_USE_IGNORE_TICKET  Ignore the cached credentials

    be noninteractive                  SSS_SUDO_ITEM_USE_NON_INTERACTIVE die when user input is needed

    debug level                        SSS_SUDO_ITEM_DEBUG_LEVEL        debug level

    command                            SSS_SUDO_ITEM_COMMAND            command with its arguments to be executed

    user's environment variables       SSS_SUDO_ITEM_USER_ENV           null terminated list of environment variables

    client pid                         SSS_SUDO_ITEM_CLI_PID            client's pid
