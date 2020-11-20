from .fixbody import filter_js, fixbody, fixindex
from .picktoc import picktoc, picktoptoc


def register_filters(app):
    if app.builder.name != 'html':
        return

    filters = [
        filter_js,
        fixbody,
        fixindex,
        picktoc,
        picktoptoc
    ]

    for f in filters:
        app.builder.templates.environment.filters[f.__name__] = f


def setup(app):
    app.connect("builder-inited", register_filters)
