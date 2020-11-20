import copy

from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives.other import TocTree as TocTreeDirective


class CustomTocTree(TocTreeDirective):
    option_spec = {
        'local': directives.flag,
        **TocTreeDirective.option_spec
    }

    """ Exclude TOC tree from the global TOC tree. """
    def run(self):
        ret = super().run()
        ret[0].children[0]['local'] = 'local' in self.options

        return ret

    @staticmethod
    def TocTreeContext(app, pagename, templatename, context, doctree):
        handler = context['toctree']

        def toctree(*args, **kwargs):
            env_tocs = app.env.tocs
            copy_tocs = copy.deepcopy(app.env.tocs)

            # Remove local-only toc tree from global navigation
            for node in copy_tocs.values():
                for toc in node.traverse(addnodes.toctree):
                    if toc.get('local', False):
                        toc.parent.remove(toc)

            app.env.tocs = copy_tocs
            output = handler(*args, **kwargs)
            app.env.tocs = env_tocs

            return output

        context['toctree'] = toctree


def setup(app):
    app.add_directive("toctree", CustomTocTree, override=True)
    app.connect("html-page-context", CustomTocTree.TocTreeContext)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
