#
# This is a test file to create a hello world file.
#

import sys
sys.path.insert(0,"..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
	'EXPR', 'STAT', 'LINE_COMMENT', 'COMMENT'

    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    )

# Tokens
t_EXPR	  = 
t_STAT	  = 
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ID    = r'[a-zA-Z_][a-zA-Z0-9_]*'


COMMENT
    :   '/*' .*? '*/'    -> channel(HIDDEN) // match anything between /* and */
    ;
WS  :   [ \r\t\u000C\n]+ -> channel(HIDDEN)
    ;

LINE_COMMENT
    : '//' ~[\r\n]* '\r'? '\n' -> channel(HIDDEN)
    ;