from sphinx.highlighting import lexers

from .NSSwitchLexer import NSSwitchLexer
from .PAMLexer import PAMLexer
from .SSSDLogLexer import SSSDLogLexer


def setup(app):
    lexers['nsswitch'] = NSSwitchLexer()
    lexers['pam'] = PAMLexer()
    lexers['sssd-log'] = SSSDLogLexer()
