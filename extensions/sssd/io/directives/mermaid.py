import textwrap

import docutils.nodes

from .utils import HTMLDirective


class Mermaid(HTMLDirective):
    has_content = True

    def run(self):
        return [docutils.nodes.raw(format='html', text=textwrap.dedent(
            '''
            <div class="mermaid">
                {content}
            </div>
            '''.format(**{
                'content': '\n'.join(self.content) if self.content else '',
            })
        ))]


def setup(app):
    app.add_directive("mermaid", Mermaid)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
