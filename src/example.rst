:orphan:

.. contents:: Table of Contents
    :local:

Level one headline
##################

Level two headline
******************

Third headline
==============

Fourth headline
---------------

Fifth headline
^^^^^^^^^^^^^^

Sixth headline
""""""""""""""

This is a paragraph. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Morbi commodo laoreet viverra. Duis cursus risus quam, vel tempor eros fringilla
nec. Curabitur sed tincidunt urna, eu sagittis ante. Etiam tempor risus vitae
dapibus placerat.

This is new paragraph. *Italic* **Bold**.

* Item in an unordered list.
* Item in an unordered list.

#. Item in an ordered list.
#. Item in an ordered list.

Links
*****

* External: `ReST cheatsheet
  <https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_
* Internal: :doc:`index`

Tables
******

======== ======== ======== ========
Header 1 Header 2 Header 3 Header 4
======== ======== ======== ========
Column 1 Column 2 Column 3 Column 4
Column 1 Column 2 Column 3 Column 4
Column 1 Column 2 Column 3 Column 4
Column 1 Column 2 Column 3 Column 4
======== ======== ======== ========

Side content
************

.. note::

    A note paragraph.

.. warning::

    A warning paragrapgh.

.. seealso::

    A see also paragrapgh.

Code snippets
*************

.. code-tabs::
    :caption: Distribution specific snippets

    .. fedora-tab::

        $ echo "fedora"

    .. fedora-tab::
        :version: 33

        $ echo "fedora 33"

    .. rhel-tab::

        $ echo "rhel"

    .. ubuntu-tab::

        $ echo "ubuntu"

.. code-block:: c
    :caption: Example code snippet, line numbers can be disabled
    :linenos:
    :emphasize-lines: 6,7

    #include <stdio.h>
    int main() {

        int number1, number2, sum;

        printf("Enter two integers: ");
        scanf("%d %d", &number1, &number2);

        // calculating sum
        sum = number1 + number2;

        printf("%d + %d = %d", number1, number2, sum);
        return 0;
    }

Images
******

.. image:: ../extensions/sssd/io/themes/sssd.io/static/images/logo.svg
    :width: 200
    :align: center

Diagrams
********

Graphviz
========

You can use `graphviz <https://graphviz.org>`_ to render diagrams. Graphviz is
an old and well known tool that can create pretty much any image. There are also
bunch of GUI applications to help you design what you need.

* Online editor: https://dreampuf.github.io/GraphvizOnline

.. graphviz::
    :align: center

    digraph {
        center=true;
        rankdir=LR;

        a->b->c
        a  [shape=ellipse,label="Start"]
        b  [shape=box,label="Task"]
        c  [shape=ellipse,label="End"]
    }

Mermaid
=======

`Mermaid <https://mermaid-js.github.io>`_ is a javascript diagram library. It is
probably not as generic and powerful as graphviz but it is more then sufficient
for most use cases and much easier to use. It also looks better without any
additional effort.

* Online editor: https://mermaid-js.github.io/mermaid-live-editor

.. mermaid::

    graph LR
        s((Start)) --> Task --> e((End))
