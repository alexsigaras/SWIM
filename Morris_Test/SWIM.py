#
# This is a test file to create a hello world file.
#

import sys
sys.path.insert(0,"..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'ID','NUMBER', 
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'STRING'
    )

# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ID    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_STRING= r'\"[a-zA-Z_][a-zA-Z0-9_ ]*\"'
    

t_ignore = " \t"
xvar = ''
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


    
# Build the lexer
import ply.lex as lex
lex.lex()



# Yacc



def p_function(t):
    '''function : ID LPAREN STRING RPAREN'''
    if t[1] == "print" : print t[3]
    xvar = t[3]
    print "done function"



def p_error(t):
    if t:
        print("Syntax error at '%s'" % t.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc(optimize=1)
mode = 2
if mode == 1:
    s = raw_input('SWIM REPL > ')
    lex.input(s)

while 1:

    if mode == 1:   
        tok = lex.token()

        if not tok:
            break
        print tok
        print xvar
    else:
        try:
            s = raw_input('SWIM REPL > ')
        except EOFError:
            break
        yacc.parse(s) 
        print xvar       
             
