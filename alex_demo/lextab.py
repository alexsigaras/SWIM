# lextab.py. This file automatically created by PLY (version 3.4). Don't edit!
_tabversion   = '3.4'
_lextokens    = {'RPAREN': 1, 'DIVIDE': 1, 'POW': 1, 'NUMBER': 1, 'TIMES': 1, 'EQUALS': 1, 'PLUS': 1, 'LPAREN': 1, 'STRING': 1, 'MINUS': 1, 'ID': 1, 'MOD': 1}
_lexreflags   = 0
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_NUMBER>\\d+)|(?P<t_newline>\\n+)|(?P<t_STRING>\\"[a-zA-Z_][a-zA-Z0-9_ ]*\\")|(?P<t_ID>[a-zA-Z_][a-zA-Z0-9_]*)|(?P<t_LPAREN>\\()|(?P<t_PLUS>\\+)|(?P<t_POW>\\^)|(?P<t_RPAREN>\\))|(?P<t_MOD>\\%)|(?P<t_TIMES>\\*)|(?P<t_MINUS>-)|(?P<t_EQUALS>=)|(?P<t_DIVIDE>/)', [None, ('t_NUMBER', 'NUMBER'), ('t_newline', 'newline'), (None, 'STRING'), (None, 'ID'), (None, 'LPAREN'), (None, 'PLUS'), (None, 'POW'), (None, 'RPAREN'), (None, 'MOD'), (None, 'TIMES'), (None, 'MINUS'), (None, 'EQUALS'), (None, 'DIVIDE')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
