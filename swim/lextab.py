# lextab.py. This file automatically created by PLY (version 3.4). Don't edit!
_tabversion   = '3.4'
_lextokens    = {'DO': 1, 'NUMBER': 1, 'SELECTOR': 1, 'WHILE': 1, 'MULTIPLY': 1, 'TRUE': 1, 'MINUS': 1, 'RPAREN': 1, 'POW': 1, 'COMMA': 1, 'PLUS': 1, 'STRING2': 1, 'ASSIGN': 1, 'STRING1': 1, 'XOR': 1, 'DIVIDE': 1, 'FOR': 1, 'EQUALS': 1, 'ELSE': 1, 'FOREACH': 1, 'LPAREN': 1, 'ID': 1, 'IF': 1, 'AND': 1, 'FALSE': 1, 'NOT': 1, 'OR': 1, 'MOD': 1}
_lexreflags   = 0
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_NUMBER>[0-9]*\\.?[0-9]+)|(?P<t_ID>[a-zA-Z_][a-zA-Z_0-9]*)|(?P<t_newline>\\n+)|(?P<t_STRING1>u?"\\\\?[^"]*")|(?P<t_STRING2>u?\'\\\\?[^\']*\')|(?P<t_OR>or|\\|\\|)|(?P<t_AND>and|&&)|(?P<t_NOT>not|!)|(?P<t_XOR>xor)|(?P<t_PLUS>\\+)|(?P<t_POW>\\^)|(?P<t_MULTIPLY>\\*)|(?P<t_LPAREN>\\()|(?P<t_MOD>\\%)|(?P<t_EQUALS>==)|(?P<t_RPAREN>\\))|(?P<t_SELECTOR>@)|(?P<t_DIVIDE>/)|(?P<t_ASSIGN>=)|(?P<t_COMMA>,)|(?P<t_MINUS>-)', [None, ('t_NUMBER', 'NUMBER'), ('t_ID', 'ID'), ('t_newline', 'newline'), (None, 'STRING1'), (None, 'STRING2'), (None, 'OR'), (None, 'AND'), (None, 'NOT'), (None, 'XOR'), (None, 'PLUS'), (None, 'POW'), (None, 'MULTIPLY'), (None, 'LPAREN'), (None, 'MOD'), (None, 'EQUALS'), (None, 'RPAREN'), (None, 'SELECTOR'), (None, 'DIVIDE'), (None, 'ASSIGN'), (None, 'COMMA'), (None, 'MINUS')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}