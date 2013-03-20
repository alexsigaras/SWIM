#-----------------------------------------------------------------------------#
#                                                                             #
#           COLUMBIA UNIVERSITY - FU FOUNDATION SCHOOL OF ENGINEERING         #
#                             COMPUTER SCIENCE DEPARTMENT                     #
#                                                                             #
# COMS W4115 - PROGRAMMING LANGUAGES AND TRANSLATORS                          #
# Professor A. Aho                                                            #
#                                                                             #
# Team 3 Final Project: "SWIM"                                                #
# Team Mentor: A. Aho                                                         #
#                                                                             #
# Team members:                                                               #
#                                                                             #
#    Name                    Role                         UNI                 #
# Morris Hopkins        Project Manager                 mah2250               #
# Seungwoo Lee          Language Guru                   sl3492                #
# Lev Brie              System Architect                ldb2001               #
# Alexandros Sigaras    System Integrator               as4161                #
# Michal Wolski         Verification and Validation     mtw2135               #
#                                                                             #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                            1. Library Import                                #
#-----------------------------------------------------------------------------#

import sys
sys.path.insert(0,"..")

if sys.version_info[0] >= 3:
    raw_input = input

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                           2. Token Declaration                              #
#-----------------------------------------------------------------------------#

# Declare tokens table

# Rebuild it
tokens = (
	'SINGLE_LINE_COMMENT', 'MULTI_LINE_COMMENT_START', 'MULTI_LINE_COMMENT_END',
	'LPAREN', 'RPAREN',
	'TRUE', 'FALSE', 'ID', 'STRING', 'NUMBER',
	'CONTINUE', 'BREAK', 'RETURN', 'IS', 'IF', 'ELSE', 'DO', 'WHILE', 'FOR', 'EACH', 'TRY', 'CATCH',
	'AND', 'OR', 'NOT', 'XOR', 'ASSIGN',
    'EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_OR_EQUAL', 'GREATER_THAN_OR_EQUAL',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'POW', 'MOD',
    )

#---------------------------------#
#          Comment Tokens         #
#---------------------------------#

t_SINGLE_LINE_COMMENT      = '//'
t_MULTI_LINE_COMMENT_START = '/*'
t_MULTI_LINE_COMMENT_END   = '/*'

#---------------------------------#

#---------------------------------#
#        Identifier Tokens        #
#---------------------------------#

t_LPAREN  = r'\('
t_RPAREN  = r'\)'

#---------------------------------#

#---------------------------------#
#         Keyword Tokens          #
#---------------------------------#

t_TRUE    = r'True'
t_FALSE   = r'False'
t_ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_STRING  = r'"[a-zA-Z0-9_ ]*"'

def t_NUMBER(t):
    r'[0-9]*\.?[0-9]+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %s" % t.value)
        t.value = 0
    return t

t_CONTINUE 	= r'continue'
t_BREAK 	= r'break'
t_RETURN 	= r'return'
t_IS 		= r'is'
t_IF      	= r'if'
t_ELSE    	= r'else'
t_DO      	= r'do'
t_WHILE   	= r'while'
t_FOR     	= r'for'
t_EACH 	  	= r'each'
t_TRY 		= r'try'
t_CATCH 	= r'catch'

#---------------------------------#

#---------------------------------#
#         Operator Tokens         #
#---------------------------------#

# Logical Operators
t_AND       			= r'and|&&'
t_OR       				= r'or|\|\|'
t_NOT       			= r'not|!'
t_XOR       			= r'xor'
t_ASSIGN   				= r'='

# Comparison Operators
t_EQUALS                = r'=='
t_NOT_EQUALS            = r'!='
t_LESS_THAN             = r'<'
t_GREATER_THAN          = r'>'
t_LESS_THAN_OR_EQUAL    = r'<='
t_GREATER_THAN_OR_EQUAL = r'<='

# Arithmetic Operators
t_PLUS      			= r'\+'
t_MINUS    				= r'-'
t_MULTIPLY  			= r'\*'
t_DIVIDE    			= r'/'
t_POW       			= r'\^'
t_MOD       			= r'\%'

#---------------------------------#

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                                 3. Lex                                      #
#-----------------------------------------------------------------------------#
    
import ply.lex as lex
lex.lex(optimize=1)

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                            4. Parsing Rules                                 #
#-----------------------------------------------------------------------------#

precedence = (
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY','DIVIDE', 'MOD'),
    ('right','UMINUS','POW'),
    )



#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                                5. Yacc                                      #
#-----------------------------------------------------------------------------#

import ply.yacc as yacc
yacc.yacc(optimize=1)
mode = 2
if mode == 1:
    s = raw_input("SWIM REPL> ")
    lex.input(s)
while 1:
    if mode == 1:
        tok = lex.token()
        print tok
        if not tok:
            break
    else:
        try:
            s = raw_input('SWIM REPL> ')
        except EOFError:
            break
        yacc.parse(s)

#-----------------------------------------------------------------------------#