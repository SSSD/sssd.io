import textwrap

import docutils.nodes
from docutils.parsers.rst import directives
from sphinx.directives.code import CodeBlock

from .utils import HTMLDirective, get_unique_id, nodes_to_html


class CustomCodeBlock(CodeBlock):
    """ Wraps code block into a top level contain for better styling. """
    def run(self):
        node = docutils.nodes.container(classes=['code-block'])
        node.extend(super().run())

        return [node]


class CodeTabs(HTMLDirective):
    has_content = True

    option_spec = {
        'name': directives.unchanged,
        'caption': directives.unchanged,
    }

    def run(self):
        node = docutils.nodes.container(classes=['code-tabs'])
        if 'name' in self.options:
            # If 'name' option is set, add it to the node and use it as id.
            self.add_name(node)
            self.state.document.set_id(node)

        if 'caption' in self.options:
            if 'name' in self.options:
                # Use the name as id
                anchor = node['ids'][0]
            else:
                # Generate id out of the caption
                anchor = get_unique_id(self.state.document, self.options['caption'])
                node['ids'] = [anchor]

            caption = docutils.nodes.raw(format='html', text=textwrap.dedent(
                '''
                <div class="code-tabs-caption permalink">
                    <a href="#{id}" title="Permalink to this snippet">{caption}</a>
                </div>
                '''.format(**{
                    'caption': self.options['caption'],
                    'id': anchor
                })
            ))
            node.append(caption)

        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class CodeTab(CustomCodeBlock):
    option_spec = {
        'label': directives.unchanged_required,
        'label-class': directives.unchanged,
        **CodeBlock.option_spec
    }

    def run(self):
        builder = self.env.app.builder
        if builder.name != 'html':
            raise NotImplementedError('Only html builder is supported')

        codeblock = nodes_to_html(self.env.app.builder, super().run())

        return [docutils.nodes.raw(format='html', text=textwrap.dedent(
            '''
            <div class="code-tab" data-label="{label}">
                <div class="code-tab-label {label-class}" data-label="{label}">{label}</div>
                {codeblock}
            </div>
            '''.format(**{
                'codeblock': codeblock,
                'label': self.options.get('label'),
                'label-class': self.options.get('label-class', '')
            })
        ))]


class DistroCodeTab(CodeTab):
    option_spec = {
        'version': directives.unchanged,
        **CodeTab.option_spec
    }

    def __init__(self, name, shortname, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.name = name
        self.shortname = shortname

    def run(self):
        if not self.arguments:
            self.arguments = ['console']

        if 'label-class' not in self.options:
            self.options['label-class'] = f'code-tab-distro code-tab-distro-{self.shortname}'

        if 'label' not in self.options:
            self.options['label'] = self.name
            version = self.options.get('version', '')
            if version:
                self.options['label'] += f' {version}'

        return super().run()


class FedoraCodeTab(DistroCodeTab):
    def __init__(self, *args, **kwargs):
        super().__init__('Fedora', 'fedora', *args, **kwargs)


class RHELCodeTab(DistroCodeTab):
    def __init__(self, *args, **kwargs):
        super().__init__('RHEL', 'rhel', *args, **kwargs)


class UbuntuCodeTab(DistroCodeTab):
    def __init__(self, *args, **kwargs):
        super().__init__('Ubuntu', 'ubuntu', *args, **kwargs)


def setup(app):
    app.add_directive("code-block", CustomCodeBlock, override=True)

    app.add_directive("code-tabs", CodeTabs)
    app.add_directive("code-tab", CodeTab)
    app.add_directive("fedora-tab", FedoraCodeTab)
    app.add_directive("rhel-tab", RHELCodeTab)
    app.add_directive("ubuntu-tab", UbuntuCodeTab)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
