import textwrap

import docutils
import os.path

from sphinx.util.osutil import relative_uri

from .utils import HTMLDirective, nodes_to_html


class Lightbox(HTMLDirective):
    has_content = True

    option_spec = {
        'group': docutils.parsers.rst.directives.unchanged,
    }

    def run(self):
        html = ''
        images = self.content
        for image in images:
            (src, title) = image.split(' ', 1)

            # Make sure the image is copied over
            # TODO This is quite a hack, there is certainly a more proper way.
            self.env.app.builder.images[src] = os.path.basename(src)
            dest = relative_uri(
                self.env.app.builder.get_target_uri(self.env.docname),
                f'{self.env.app.builder.imagedir}/{os.path.basename(src)}'
            )

            html += '<a href="{src}" data-lightbox="{group}" data-title="{title}"><img src="{src}"></a>\n'.format(
                src=dest,
                title=title,
                group=self.options.get('group', 'default')
            )

        return [docutils.nodes.raw(format='html', text=textwrap.dedent(
            '''
            <div class="lightbox-container">
                {html}
            </div>
            '''.format(html=html)
        ))]



def setup(app):
    app.add_directive("lightbox", Lightbox)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
