from sphinx.highlighting import lexers

from .SSSDLogLexer import SSSDLogLexer


def setup(app):
    lexers['sssd-log'] = SSSDLogLexer()
