import textwrap

import docutils
import sphinx.util.docutils

from .utils import HTMLDirective


class Poster(HTMLDirective):
    has_content = True

    option_spec = {
        'first-line': docutils.parsers.rst.directives.unchanged,
        'second-line': docutils.parsers.rst.directives.unchanged,
        'project': docutils.parsers.rst.directives.unchanged,
        'download-uri':  docutils.parsers.rst.directives.uri,
        'github-uri':  docutils.parsers.rst.directives.uri
    }

    def run(self):
        return [docutils.nodes.raw(format='html', text=textwrap.dedent(
            '''
            <header>
                <h1>
                    <span><span>{first-line}</span> <span>{second-line}</span></span>
                </h1>
                <p class="f-title">
                    {content}
                </p>
            </header>
            <section id="links">
                <h2>Get {project}</h2>
                <ul class="clear-list">
                    <li><a href="{download-uri}">Download {project}</a></li>
                    <li><a href="{github-uri}">{project} on GitHub</a></li>
                </ul>
            </section>
            '''.format(**{
                'first-line': self.options.get('first-line', ''),
                'second-line': self.options.get('second-line', ''),
                'project': self.options.get('project', ''),
                'github-uri': self.options.get('github-uri', ''),
                'content': '\n'.join(self.content) if self.content else '',
                'download-uri': self.env.app.builder.get_relative_uri(
                    self.env.docname, self.options.get('download-uri', '')
                ),
            })
        ))]


class PosterHintsContainer(sphinx.util.docutils.SphinxDirective):
    has_content = True

    def run(self):
        node = docutils.nodes.container(ids=['hints'])
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class PosterHintElement(HTMLDirective):
    has_content = True

    option_spec = {
        'icon': docutils.parsers.rst.directives.unchanged,
        'title': docutils.parsers.rst.directives.unchanged,
        'link': docutils.parsers.rst.directives.uri,
        'link-title': docutils.parsers.rst.directives.unchanged,
    }

    def run(self):
        return [docutils.nodes.raw(format='html', text=textwrap.dedent(
            '''
            <section>
                <a href="{link}" title="{link-title}" style="background-image: url('{icon}');">
                    <h2>{title}</h2>
                    <p>
                        {content}
                    </p>
                </a>
            </section>
            '''.format(**{
                'icon': self.options.get('icon', ''),
                'link': self.env.app.builder.get_relative_uri(self.env.docname, self.options.get('link', '')),
                'link-title': self.options.get('link-title', ''),
                'title': self.options.get('title', ''),
                'content': '\n'.join(self.content) if self.content else '',
            })
        ))]


def setup(app):
    app.add_directive("poster", Poster)
    app.add_directive("poster-hints", PosterHintsContainer)
    app.add_directive("poster-hint", PosterHintElement)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
