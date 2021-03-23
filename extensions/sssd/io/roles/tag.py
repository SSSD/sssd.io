import docutils.nodes


def tag(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Sphinx does not support nested markup which is limiting especially during
    string styling, e.g. **`link <path>`_** will not produce a bold link.

    Use:
    :tag:`strong` `link <path>`_link :end-tag:`strong`

    """
    return [docutils.nodes.raw(format='html', text=f'<{text}>')], []


def tag_end(name, rawtext, text, lineno, inliner, options={}, content=[]):
    return [docutils.nodes.raw(format='html', text=f'</{text}>')], []


def setup(app):
    app.add_role('tag', tag)
    app.add_role('end-tag', tag_end)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
