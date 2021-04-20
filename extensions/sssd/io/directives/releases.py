import textwrap

import docutils
import sphinx.util.docutils

from .utils import HTMLDirective, nodes_to_html


class ReleaseContainer(HTMLDirective):
    has_content = True

    def run(self):
        node = docutils.nodes.table(classes=['release-list'])
        node.append(docutils.nodes.raw(format='html', text='<tr><th>Release date</th><th>Version</th><th>Links</th></tr>'))
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class ReleaseElement(HTMLDirective):
    has_content = True

    option_spec = {
        'date': docutils.parsers.rst.directives.unchanged,
        'download': docutils.parsers.rst.directives.uri,
    }

    def run(self):
        html = '''
            <tr>
                <td>{date}</td>
                <td>{version}</td>
                <td><a href="{download}" title="{version} GitHub Release Page">Download</a> | <a href="{notes}" title="{version} release notes">Release Notes</a></td>
            </tr>
        '''

        version = self.content[0].strip()
        return [docutils.nodes.raw(
            format='html',
            text=textwrap.dedent(html).format(**{
                'version': version,
                'date': self.options.get('date', ''),
                'download': self.options.get('download', ''),
                'notes': self.env.app.builder.get_relative_uri(self.env.docname, f'release-notes/{version}'),
            })
        )]


def setup(app):
    app.add_directive("releases", ReleaseContainer)
    app.add_directive("release", ReleaseElement)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
