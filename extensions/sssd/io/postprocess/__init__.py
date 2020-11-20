from .sass import process_sass
from .search import build_search_index


def setup(app):
    app.connect('build-finished', process_sass)
    app.connect('build-finished', build_search_index)
