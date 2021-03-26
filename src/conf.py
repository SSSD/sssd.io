# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath('../extensions'))


def setup(app):
    ''' Setup local extensions. '''
    import sssd.io
    sssd.io.setup(app)


# -- Project information -----------------------------------------------------
project = 'sssd.io'
copyright = '2020, SSSD Team'
author = 'SSSD Team'


# -- General configuration ---------------------------------------------------

master_doc = 'contents'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_gitstamp',
    'sphinx.ext.graphviz',
    'sssd.io.directives.codetabs',
    'sssd.io.directives.mermaid',
    'sssd.io.directives.poster',
    'sssd.io.directives.toctree',
    'sssd.io.lexers',
    'sssd.io.roles.tag',
]

graphviz_output_format = 'svg'

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title = 'sssd.io'
html_theme = 'sssd.io'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

toc_contrib = [
    'Contribution',
    'Fundamentals',
    'Under the hood'
]

html_theme_options = {
    'toc_pattern': {
        'contrib/*': toc_contrib,
        '*': [f'!{x}' for x in toc_contrib],
    },
    'design_page_path': 'design-pages/pages'
}
