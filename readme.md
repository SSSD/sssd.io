# SSSD Documentation Sources (work in progress)

The documentation is written in [reStructuredText] format and can be build
with [Sphinx] documentation generator.

[reStructuredText]: https://docutils.sourceforge.io/rst.html
[Sphinx]: https://www.sphinx-doc.org

## Install Python dependencies

It is recommended to install Python dependencies in virtual environment.

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip3 install -r requirements.txt
```

Note: To step out of the virtual environment, run `$ deactivate`.

## Build it

```console
(.venv) $ make html
```

## View it

```console
$ firefox _build/html/index.html
```

## Example page

There is a [sample page] that can get you started with reStructuredText. You
can view it after the build is finished with:

```console
$ firefox _build/html/example.html
```

[sample page]: src/example.rst

## Add new content

1. Create a new page in reStructuredText format and include in somewhere in
   [src] folder.
2. Every new page needs to be part of a page table of content (ToC) tree. To
   add a page to the ToC tree, either include it in `toc` directive in an
   existing document or add it to the top level navigation in the [contents]
   document.
3. Build the documentation with `make html` and navigation to your page to check
   that everything display as intended.
4. Open a Pull Request against this repository with your change.

[src]: src
[contents]: src/contents.rst
