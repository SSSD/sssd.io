Coding Style
############

SSSD is a large open source project and as such it is crucial for all authors to
follow a single coding style to improve maintainability and readability of the
code. The SSSD is written in C and it follows a `Kernighan & Ritchie Style`_ (or
perhaps `The One True Brace Style`_) with slight modifications that fit well
into the project.

.. _Kernighan & Ritchie Style: https://en.wikipedia.org/wiki/Indentation_style#K&R_style
.. _The One True Brace Style: https://en.wikipedia.org/wiki/Indentation_style#Variant:_1TBS_(OTBS)


.. note::

    Most of the SSSD is written in the ``C`` language, however we also use some
    other languages when necessary, mostly Python which is used for code
    generators and integration tests. We have adopted the `PEP8`_ style for Python
    code.

.. _PEP8: https://www.python.org/dev/peps/pep-0008/

General rules
*************

* Use 4 spaces instead of one tab and do not use tabs at all
* Add copy of the license to all source and header files
* Limit line length to 80 characters (120 characters in justified cases)
* Use variable length arrays with caution and only for smaller arrays
* Do not use C99 line comments (``// line comment``)
* Avoid comments that do not add value to the code

The coding style
****************

If you are an experienced programmer, it should be sufficient to look at the
following code snippet to tell you enough about our coding style to get you
started. There is a more detailed description available bellow the example to
note things that may not be obvious.

.. code-block:: c

    /* - Headers should be grouped properly (system, project, etc.).
     * - Files inside the groups should be sorted alphabetically, unless a
     *   specific order is required.
     * - Header groups should be separated by a blank line.
     */

    #include "config.h"

    #include <stdio.h>
    #include <stdlib.h>
    #include <sring.h>

    #include "util/util.h"

    int my_func(int arg1, int arg2, int *_output_argument)
    {
        /* Prefer one declaration per line. */
        int meaningful_name;
        int simple_initialization = 0;
        int complex_initialization;
        const char *pointer;
        int i, j;

        /* Avoid complex initialization in declarations. */
        complex_initialization = get_the_value();

        /* Do not use !pointer */
        if (pointer == NULL) {
            pointer = "Always use brackets, even for one liner"
        }

        /* One liner is allowed for very simple things. */
        if (pointer == NULL) return EINVAL;

        if (condition) {
            /* Do stuff. */
        } else {
            /* Do stuff. */
        }

        switch (value) {
        case 1:
            /* Do stuff. */
            break;
        case 2:
            /* Do stuff. */
            break;
        default:
            /* Do stuff. */
            break;
        }

        for (i = 0; i < 10; i++) {
            for (j = 0; j < 10; j++) {
                /* Do stuff. */
            }
        }

        while (condition) {
            /* Loop body */
        }

        do {
            /* Loop body */
        } while (condition)

        return 0;
    }

Additional notes
================

Naming conventions
    * We use lower cased names with words separated by underscores
    * Use meaningful variable names
    * Do not use Hungarian notation
    * Use uppercase for constants (``#define``, ``enum``)

Comments
    * Avoid C++ style line comments ``// comment``
    * Always use ``/* comment */``
    * Avoid useless comments that do not add value to the code (i.e. do not
      describe code, but try to describe intentions or knowledge that is not
      clear from the code)

Definitions
    * When defining structure or union try make it easy to read. You may use
      some form of alignment if you see that this might make it more readable.
    * Avoid using ``typedefs``, they obscure structures and make it harder
      to understand and debug

Variables
    * Always declare variables at the top of the function or a block, one
      declaration per line is preferred
    * Initialize local variables at declaration when possible
    * Avoid complex initializations (e.g. calling functions) at declaration
    * Don’t initialize static or global variables to ``0`` or ``NULL``
    * Avoid using global variables when possible

Functions
    * Add underscore prefix to output arguments, e.g. ``_output``
    * Put input arguments before output arguments
    * Put arguments that are both input and output in the middle

Strings
    * Use index  format specifiers if a string is internationalized
      (e.g. ``_("item %1$s has %2$s value")``

Including headers
    * Headers should be grouped properly (system, project, etc.)
    * Files inside the groups should be sorted alphabetically, unless a
      specific order is required
    * Header groups should be separated by a blank line

Header guards
    .. code-block:: c

        #ifndef _HEADER_H_
        #define _HEADER_H_

        /* Some important code here */

        #endif /* !_HEADER_H_ */

Wrapping lines
    * Try to fit inside 80 characters limit when possible
    * Try to break the line at common place: after a comma, before an operator
    * Align the new line with the beginning of the expression at the same level
      in the previous line
    * Keep the code readable

    .. code-block:: c

      ret = wrapped_arguments(arg1, arg2,
                              arg3, arg4,
                              arg5);

      ret = unbreakable_argument_name(arg1,
                        real_long_argument_name_that_wont_fit_the_line);

      if (operand1 && operand2
              && operand3) {
          /* Do stuff. */
      }

Goto usage
    * We use ``goto`` to simplify cleanup
    * Never use ``goto`` to  jump backwards in the code
    * Do not use more than one ``goto`` label per function
    * We use ``done`` and ``fail`` labels

      done
          Label ``done`` is used as jump target before exit. Clean-up
          operations, such as freeing local talloc context, usually follow the
          ``done`` label. Both successful and unsuccessful function executions
          pass this label.

      fail
          Used as special exit path when function fails. Successful function
          execution typically does not execute statements after this label.

    .. code-block:: c

        errno_t done_example()
        {
            errno_t ret;

            ret = do_stuff();
            if (ret != EOK) {
                goto done;
            }

            ret = EOK;

        done:
            /* Cleanup. */
            return ret;
        }

        char *fail_example()
        {
            char *output;
            errno_t ret;

            output = strdup("show me the usage");
            if (output == NULL) {
                return NULL;
            }

            ret = do_stuff();
            if (ret != EOK) {
                goto fail;
            }

            return output;

        fail:
            free(output)
            return NULL;
        }

Localization and Internationalization
*************************************

Our development policy for the SSSD requires that any code that generates
a user-facing message should be wrapped by GNU ``gettext`` macros so that they
can eventually be translated.
