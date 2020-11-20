from os import path

from .filters import setup as filters_setup
from .postprocess import setup as postprocess_setup


def setup(app):
    root_dir = path.abspath(path.dirname(__file__))
    themes = [
        'sssd.io'
    ]

    # register themes
    for theme in themes:
        app.add_html_theme(theme, path.join(root_dir, 'themes', theme))

    # register filters
    filters_setup(app)

    # register sass extension required for the theme
    postprocess_setup(app)
