Coding Style
############

Introduction
============
This manual contains coding standards and guidelines for SSSD contributors.
All new code should adhere to these standards. These rules do not apply to
existing legacy code. Please do not go back and apply formatting changes to
the old code. It just confuses things and is generally a waste of time.

Why we are using coding guidelines?
-----------------------------------
The Coding Guidelines are necessary to improve maintainability and readability
of the code. It allows contributors from all over the world to stick to one
code convention making collaboration much easier.

Improved readability
--------------------
Code is not only for compilers, it is for people also.
Coding style and consistency means that if you go from one part of the code
to another you don’t spend time having to re-adjust from one style to another.
Blocks are consistent and readable and the flow of the code is apparent.
Coding style adds value for people reading your code after you’ve been
hit by a `bus <https://en.wikipedia.org/wiki/Bus_factor>`_.
Remember that.

Easier maintanance
------------------
If you’re merging changes from a patch it’s much easier if everyone is using
the same coding style. This isn’t the reality for a lot of our code,
but we’re trying to get to the point where most of it uses the same style.
The less time maintainers will spend on adjusting to the new coding style,
the more of that time will be spend on ensuring code quality.


General rules
=============
Most of our coding guidelines are based on K&R (Kernighan & Ritchie Style)
C coding style.

Compiler
--------
- We compile code with -std=gnu99 flag. It is OK to use C99 features supported by
  GCC and Clang.
- Using variable length arrays should be done with caution and only be used for
  smaller arrays.
- Don’t add extra dependencies unless they are needed.

Code structure
---------------
- All source and header files should include a copy of the license.
- For best readability line length should be 80 characters, in justified cases
  maximum line length can be up to 120 characters.

.. code-block:: c

    /* Below situation is common and accepted */
    ret = friendly_function_with_meaningful_name(arg1,
                                                 arg2,
                                                 arg3)

    /* Below situation is accepted but should be avoided */
    ret = this_is_some_function_with_very_long_name_from_external_library_and_cant_fit_80_characters(arg1,
                                                                                                     arg2,
                                                                                                     arg3)

- When wrapping lines try to break it in a common place:

  - after a comma
  - before an operator
  - align the new line with the beginning of the expression at the same level in the previous line
  - if all above fails, indent 8 spaces

.. code-block:: c

    ret = some_random_function_wrapped_right_way(arg1,
                                                 arg2 + HEAD_OFFSET,
                                                 arg3);

    ret = some_random_function_wrapped_wrong_way(
          arg1, arg2 +
          HEAD_OFFSET,
          arg3);

Comments
--------
- C++ style line comments "// ......" should be avoided. Avoid useless comments
  that do not add value to the code.

.. code-block:: c

    // I am a bad multi line comment
    // and should not look like this
    // so please avoid doing something like me
    void fun(int arg1, int arg2, int arg3); // I also should not be here

    /*
     * I am a bad multi line comment
     * which is pretty and well formatted.
     * Be like me.
     */
    void fun(int arg1, int arg2, int arg3); /* I am a nice comment too */

- Our code is used internationally, so use simple english in messages.
- Keep messages short, direct, and offer direction.

.. code-block:: c

    /* Bad message */
    LOG_DEBUG("Error!!!");

    /* Better message */
    LOG_DEBUG("An error occured processing client request");

    /* Great message */
    LOG_DEBUG("An error occured processing client request: <ID>, result: <RET>");

    /* Too long of a message */
    LOG_DEBUG("An error occured processing client request: <ID>, result: <RET>
               caused by potential timeout in backend connection to LDAP
               server or backend server malfunction. This may be issue unrelated
               to SSSD. Please check your backend connection and try again");

- Instead of tabs use spaces. Most editors should figure this out automatically
  based on existing code. In some rare usecases it may require manual adjustment.

Preprocesor
===========

Includes
--------
- Headers should be grouped properly (system headers, project headers etc.)
- Files inside the groups should be sorted alphabetically, unless a specific
  order is required
- Standard headers and local headers should be separated by a blank line

.. code-block:: c

    #include "config.h"

    #include <stdio.h>
    #include <stdarg.h>
    #include <stdlib.h>
    #include <fcntl.h>

    #include <sys/types.h>
    #include <sys/stat.h>
    #include <sys/time.h>

Compilation guards
------------------
When using compilation guards always remember to add comment to closing guard
explaining to which code section it is related.

.. code-block:: c

    #ifndef _HEADER_H_
    #define _HEADER_H_

    /* Some important code here */

    #endif /* !_HEADER_H_ */

.. code-block:: c

    #ifdef HAVE_PTHREADS

    /* Some code here */

    #else /* !HAVE_PTHREADS */

    /* Some other code here */

    #endif /* HAVE_PTHREADS */

Defines
-------
Constant values can be declared globally as #define. In such case capital letters
should be used for the define name. This is frequently used for things
like error codes definitions:

.. code-block:: c

    #define SSSDBG_FATAL_FAILURE  0x0010   /* level 0 */
    #define SSSDBG_CRIT_FAILURE   0x0020   /* level 1 */
    #define SSSDBG_OP_FAILURE     0x0040   /* level 2 */
    #define SSSDBG_MINOR_FAILURE  0x0080   /* level 3 */
    #define SSSDBG_CONF_SETTINGS  0x0100   /* level 4 */
    #define SSSDBG_FUNC_DATA      0x0200   /* level 5 */
    #define SSSDBG_TRACE_FUNC     0x0400   /* level 6 */
    #define SSSDBG_TRACE_LIBS     0x1000   /* level 7 */
    #define SSSDBG_TRACE_INTERNAL 0x2000   /* level 8 */
    #define SSSDBG_TRACE_ALL      0x4000   /* level 9 */
    #define SSSDBG_BE_FO          0x8000   /* level 9 */
    #define SSSDBG_TRACE_LDB     0x10000   /* level 10 */
    #define SSSDBG_IMPORTANT_INFO SSSDBG_OP_FAILURE

Macros
------
If a macro is safe (for example a simple wrapping function), then the case
can be lower-case. Macros that are unsafe should be in upper-case.
This also applies to macros that span multiple lines:

.. code-block:: c

    #define MY_MACRO(a, b) do {   \
    foo((a) + (b));           \
    bar(a);                   \
    } while (0)

Notice that arguments should be in parentheses if there’s a risk. Also notice
that a is referenced two times, and hence the macro is dangerous. Wrapping the
body in do { } while (0) makes it safe to use it like this:

.. code-block:: c

    if (expr)
        MY_MACRO(x, y);

Notice the semicolon is used after the invocation, not in the macro definition.

goto
====
We use goto to simplify cleanup operations and some other tasks that need
to be done before leaving the function. Never use goto to jump backwards
in the code. Do not use more than one goto label per function.

Common goto labels we are using are:

- done:
    Label done is used as jump target before exit. Clean-up operations, such as
    freeing local talloc context, usually follow the done label. Both successful
    and unsuccessful function executions pass this label.

- fail:
    Used as special exit path when function fails. Successful function execution
    typically does not execute statements after this label.

- immediate:
    The immediate label is used in tevent’s _send functions.
    The typical usage would look like this:

.. code-block:: c

    if (ret != EOK) {
        DEBUG(...);
        goto immediate;
    }

    immediate:
    if (ret == EOK) {
        tevent_req_done(req);
    } else {
        tevent_req_error(req, ret);
    }

    tevent_req_post(req, ev);
    return req;

Variables
=========
- Never use Hungarian notation when naming variables.
- Use lower case multi word underscore separated notation for naming variables.
- Make variable name meaningful.
- Always declare variables at the top of the function or block. If you find
  yourself declaring many variables inside inner block or loop, consider
  refactoring the block into helper function.
- One declaration per line is preferred.
- Initialize local variables at declaration time when possible.
- Avoid complex variable initializations (like calling functions) when declaring
  variables
- Don’t initialize static or global variables to 0 or NULL.

.. code-block:: c

    /* Bad example */
    int foo, bar;
    int car = some_complicated_function();

    /* Good example */
    int foo = 0;
    int bar = 0;
    int car = 0;
    car = some_complicated_function();

- Avoid using typedefs. Typedefs obscure structures and make it harder
  to understand and debug.
- When defining structure or union try make it easy to read. You may use some
  form of alignment if you see that this might make it more readable.
- Avoid using global variables. They make for very poor code. Should be used
  only if no other way can be found or strong reason is presented.
  They tend to be not thread/async safe.

Functions
=========
- Do not reinvent the wheel. Creating lists and queues was already done
  a lot of times. When possible, use some common functions for manipulating
  these to avoid mistakes.
- Each public API function should be preceded with a block comment describing
  what the function is supposed to do.
- It is not required to document internal APIs, although use your discretion
  and feel free to document internal functions as well.
- It up to the developer to define the order of the functions in the module and
  thus declare functions at the top or use a native flow of the module
  and avoid forward function declarations.
- For function names use multi word underscore separate naming convention.
- Never use Hungarian notation when naming functions.
- Put opening “{“ of the function body on the beginning of the new line
  after the function declaration.
- Do not put spaces before or after parenthesis in the declaration
  of the parameters.

.. code-block:: c

    /* Bad example */
    int foo ( arg1, arg2 ) {
        /* Function body */
    }

    /* Good example */
    int foo(arg1, arg2)
    {
        /* Function body */
    }

- Try to always put “input” arguments before “output” arguments, if you have
  arguments that provide both input an output put them between the pure-input
  and the pure-output ones. Add underscore prefix “_” to output arguments.
- If appropriate, always use the const modifier for pointers passed
  to the function. This makes the intentions of the function more clearer,
  plus allows the compiler to catch more bugs and make some optimizations.
- Try to return status code from function to be able to handle errors.

.. code-block:: c

    /* Good example */
    int foo(int in1, const char *in2, chr **_out1);

Decision blocks
===============
- Use the full condition syntax like (str == NULL) rather than (!str).

.. code-block:: c

    /* Incorrect way */
    if (!str) {
        ;
    }

    /* Correct way */
    if (str = NULL) {
        ;
    }

- Use braces even if there is just one line in the if statement. You can avoid
  the braces if entire if statement is on one line.
- Always use braces when there is "else" part.

.. code-block:: c

    /* Correct code */
    if (condition) {
        /* Do something */
    }

    if (condition) {
        /* Do something */
    } else {
        /* Do something else */
    }

    if (condition) foo();

    /* Incorrect code */
    if (condition)
        foo();

    if (condition)
        foo();
    else {
        bar();
    }

- Avoid last-return-in-else problem

.. code-block:: c

    /* Correct code */
    int foo(int bar)
    {
        if (something) {
            return 1;
        }

        return 0;
    }

    /* Incorrect code */
    int foo(int bar)
    {
        if (something) {
            return 1;
        } else {
            return 0;
        }
    }

- Use unsigned types when storing sizes or lengths.
- Conditions with <, <=, >= or == operators should isolate the value being
  checked (untrusted value) on the left hand side of the comparison.
  The right hand side should contain trusted values (thus avoiding
  overflows / underflows).

.. code-block:: c

    uint32_t len;
    uint32_t size;
    uint32_t p;

    /* Program logic here */

    /*
     * variable len - untrusted
     * variable size - trusted
     * variable p - trusted
     */

    /* GOOD */
    if (len / size - p) return EINVAL;

    /* BAD */
    if ((p + len ) / size) return EINVAL;


- Always have default case in switch() statements
- Add comments if a missing break is intentional

.. code-block:: c

    /* Good switch() code style to follow */
    switch (condition) {
    case A:
        /* Do work */
        break;
    case B:
        /* Do work */
        /* Explain why no break here */
    default:
        /* Always have default case */
        break;
    }

Loops
-----
Be sure that you are using similar form as bellow example:

.. code-block:: c

    for (init; condition; update) {
        /* Loop body */
    }

    while (condition) {
        /* Loop body */
    }

    do {
        /* Loop body */
    } while (condition)

Strings
=======
If the string will be internationalized (e.g. is marked with _()) and it has
more than one format substitution you MUST use index format specifiers,
not positional format specifiers. Translators need the option to reorder where
substitutions appear in a string because the ordering of nouns, verbs, phrases,
etc. differ between languages. If conventional positional format conversion
specifiers (e.g. %s %d) are used the string cannot be reordered because
the ordering of the format specifiers must match the ordering of the printf
arguments supplying the substitutions. The fix for this is easy, use indexed
format specifiers. An indexed specifier includes an (1 based) index
to the % character that introduces the format specifier (e.g. %1$ to indicate
the first argument). That index is used to select the matching argument
from the argument list. When indexed specifiers are used all format specifiers
and all * width fields MUST use indexed specifiers. See man 3 printf as well
as section 15.3.1 “C Format Strings” in the GNU gettext manual for more details.

.. code-block:: c

    /* Incerrect usage with positional specifiers */
    printf(_("item %s has %s value"), name, value);

    /* Correct usage with positional specifiers */
    printf(_("item %1$s has %2$s value"), name, value);


Localization and Internationalization
=====================================

Our development policy for the SSSD requires that any code that generates
a user-facing message should be wrapped by GNU ``gettext`` macros so that they
can eventually be translated. We use `zanata <http://zanata.org/>`_ for translating.
