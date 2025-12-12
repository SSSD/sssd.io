import docutils.nodes
import sphinx.util.docutils


class HTMLDirective(sphinx.util.docutils.SphinxDirective):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        builder = self.env.app.builder.name
        if builder != 'html':
            raise Exception(f'Builder {builder} is not supported. HTML builder is required.')


def node_to_html(builder, node):
    rendered = builder.render_partial(node)

    # Handle different Sphinx versions - newer versions use 'fragment', older use 'html_body'
    for key in ('fragment', 'html_body'):
        if key in rendered:
            body = rendered[key]
            break
    else:
        raise KeyError(f"Expected 'fragment' or 'html_body' in render_partial output, got: {list(rendered.keys())}")

    # body is in the form <div class="document">\nbody\n</div>
    # we want to remove the wrapper
    return '\n'.join(body.strip().split('\n')[1:-1]).strip()


def nodes_to_html(builder, nodes):
    return '\n'.join([node_to_html(builder, x) for x in nodes])


def content_to_html(state, builder, content, content_offset):
    node = docutils.nodes.container()
    state.nested_parse(content, content_offset, node)

    body = node_to_html(builder, node).strip()
    # remove the wrapper container
    return '\n'.join(body.strip().split('\n')[1:-1]).strip()


def get_unique_id(document, caption):
    # from docutils.nodes.document.set_id()
    id_prefix = document.settings.id_prefix
    auto_id_prefix = document.settings.auto_id_prefix
    prefix = id_prefix + auto_id_prefix
    uid = document.id_counter[prefix]
    document.id_counter[prefix] += 1

    return f'{docutils.nodes.make_id(caption)}-{prefix}{uid}'
