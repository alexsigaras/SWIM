# lextab.py. This file automatically created by PLY (version 3.4). Don't edit!
_tabversion   = '3.4'
_lextokens    = {'DO': 1, 'LESS_THAN_OR_EQUAL': 1, 'NUMBER': 1, 'SELECTOR': 1, 'WHILE': 1, 'MULTIPLY': 1, 'END': 1, 'LESS_THAN': 1, 'TRUE': 1, 'MINUS': 1, 'RPAREN': 1, 'SEMICOLON': 1, 'NOT_EQUALS': 1, 'POW': 1, 'PLUS': 1, 'COMMA': 1, 'STRING2': 1, 'ASSIGN': 1, 'STRING1': 1, 'XOR': 1, 'DIVIDE': 1, 'FOR': 1, 'EQUALS': 1, 'ELSE': 1, 'FOREACH': 1, 'LPAREN': 1, 'GREATER_THAN': 1, 'ID': 1, 'IF': 1, 'AND': 1, 'FALSE': 1, 'GREATER_THAN_OR_EQUAL': 1, 'NOT': 1, 'OR': 1, 'MOD': 1}
_lexreflags   = 0
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_NUMBER>[0-9]*\\.?[0-9]+)|(?P<t_ID>[a-zA-Z_][a-zA-Z_0-9]*)|(?P<t_newline>\\n+)|(?P<t_COMMENT>\\#.*|//.*|/\\*(.*[^\\*/]|\\n|\\t)*\\*/)|(?P<t_STRING1>u?"\\\\?[^"]*")|(?P<t_STRING2>u?\'\\\\?[^\']*\')|(?P<t_OR>\\|\\|)|(?P<t_LESS_THAN_OR_EQUAL><=)|(?P<t_LPAREN>\\()|(?P<t_PLUS>\\+)|(?P<t_POW>\\^)|(?P<t_MULTIPLY>\\*)|(?P<t_NOT_EQUALS>!=)|(?P<t_GREATER_THAN_OR_EQUAL>>=)|(?P<t_MOD>\\%)|(?P<t_EQUALS>==)|(?P<t_RPAREN>\\))|(?P<t_AND>&&)|(?P<t_SELECTOR>@)|(?P<t_LESS_THAN><)|(?P<t_NOT>!)|(?P<t_COMMA>,)|(?P<t_DIVIDE>/)|(?P<t_ASSIGN>=)|(?P<t_MINUS>-)|(?P<t_SEMICOLON>;)|(?P<t_GREATER_THAN>>)', [None, ('t_NUMBER', 'NUMBER'), ('t_ID', 'ID'), ('t_newline', 'newline'), ('t_COMMENT', 'COMMENT'), None, (None, 'STRING1'), (None, 'STRING2'), (None, 'OR'), (None, 'LESS_THAN_OR_EQUAL'), (None, 'LPAREN'), (None, 'PLUS'), (None, 'POW'), (None, 'MULTIPLY'), (None, 'NOT_EQUALS'), (None, 'GREATER_THAN_OR_EQUAL'), (None, 'MOD'), (None, 'EQUALS'), (None, 'RPAREN'), (None, 'AND'), (None, 'SELECTOR'), (None, 'LESS_THAN'), (None, 'NOT'), (None, 'COMMA'), (None, 'DIVIDE'), (None, 'ASSIGN'), (None, 'MINUS'), (None, 'SEMICOLON'), (None, 'GREATER_THAN')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
