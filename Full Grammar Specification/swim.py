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

import sys, os
import re
sys.path.insert(0,os.path.join("..", "include"))

if sys.version_info[0] >= 3:
    raw_input = input

# Parsing
from pyquery import PyQuery as pq
import urllib, getpass

# PDF
from fpdf import fpdf as pdf

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                           2.  External Functions                            #
#-----------------------------------------------------------------------------#

def stripe_quotation(string):
    result = string.replace("'","") if string.startswith("'") else string.replace('"', "")
    return result

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                           3. Token Declaration                              #
#-----------------------------------------------------------------------------#

# Reserved Tokens
reserved = {
    'if'       : 'IF',
    'else'     : 'ELSE',
    'do'       : 'DO',
    'True'     : 'TRUE',
    'False'    : 'FALSE',
    'while'    : 'WHILE',
    'for_each' : 'FOREACH',
}

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
t_MULTI_LINE_COMMENT_START = '/\*'
t_MULTI_LINE_COMMENT_END   = '/\*'

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
t_STRING  = '"[a-zA-Z_][a-zA-Z0-9_]*"'

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

#---------------------------------#
#           Other Tokens          #
#---------------------------------#

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#---------------------------------#

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                                 4. Lex                                      #
#-----------------------------------------------------------------------------#
    
import ply.lex as lex
lex.lex(optimize=1)

def t_error(t): 
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                            5. Parsing Rules                                 #
#-----------------------------------------------------------------------------#

precedence = (
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY','DIVIDE', 'MOD'),
    ('right','POW'),
    )

# dictionary of names
names = { }

# Parsing Starts from here.
def p_start(t):
    # '''start : statement
    #          | function'''
    '''start : statement'''

# Handling Errors
def p_error(t):
    if t:
        print("Syntax error at '%s'" % t.value)
    else:
        print("Syntax error at EOF")

def p_statement_true(t):
    'statement : TRUE'
    print True

def p_statement_false(t):
    'statement : FALSE'
    print False


# # Statement parsing rules
# def p_statement_assign(t):
#     'statement : ID ASSIGN expression'
#     names[t[1]] = t[3]

# def p_statement_equals(t):
#     'statement : expression EQUALS expression'
#     print t[1] == t[3]

# def p_statement_if_else(t):
#     'statement : IF expression DO expression ELSE expression'
#     if t[2] : t[4] 
#     else    : t[6]

# def p_statement_expr(t):
#     'statement : expression'
#     print t[1]

# # Function parsing rules
# def p_function(t):
#     '''function : ID LPAREN STRING RPAREN
#                 | ID LPAREN expression RPAREN'''

#     if t[1] == "print" : print t[3]
#     xvar = t[3]
#     print "done function"

# def p_expression_binop(t):
#     '''expression : expression PLUS expression
#                   | expression MINUS expression
#                   | expression MULTIPLY expression
#                   | expression DIVIDE expression
#                   | expression POW expression
#                   | expression MOD expression
#                   | expression AND expression
#                   | expression OR expression
#                   | expression XOR expression
#                   | NOT expression
#                   | TRUE
#                   | FALSE'''
#     if t[2] == '+':
#         t[0] = t[1] + t[3]  # add
#     elif t[2] == '-':
#         t[0] = t[1] - t[3]  # subtract
#     elif t[2] == '*':
#         t[0] = t[1] * t[3]  # multiply
#     elif t[2] == '/':
#         t[0] = t[1] / t[3]  # divide
#     elif t[2] == '^': 
#         t[0] = t[1] ** t[3] # power
#     elif t[2] == '%': 
#         t[0] = t[1] % t[3]  # remainder3
#     elif (t[2] == 'and' or t[2] =='&&'):
#         t[0] = t[1] and t[3]
#     elif (t[2] == 'or' or t[2] =='||'):
#         t[0] = t[1] or t[3]
#     elif t[2] == 'xor':
#         t[0] = (t[1] and not t[3]) or (not t[1] and t[3])
#     elif t[1] == 'not':
#         t[0] = not t[2]
#     elif t[1] == 'True':
#         t[0] = True
#     elif t[1] == 'False':
#         t[0] = False
#     elif t[2] == '<': t[0] = t[1] < t[3]

# # def p_expression_uminus(t):
# #     'expression : MINUS expression %prec UMINUS'
# #     print "uminus"#t[0] = -t[2]

# def p_expression_group(t):
#     'expression : LPAREN expression RPAREN'
#     t[0] = t[2]

# def p_expression_number(t):
#     'expression : NUMBER'
#     #print "push " + str(t[1])#t[0] = t[1]
#     t[0] = t[1]

# def p_expression_name(t):
#     'expression : ID'
#     try:
#         t[0] = names[t[1]]
#     except LookupError:
#         print("Undefined name '%s'" % t[1])
#         t[0] = 0

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                                6. Yacc                                      #
#-----------------------------------------------------------------------------#

import ply.yacc as yacc
yacc.yacc(optimize=1)
mode = 2
if mode == 1:
    s = raw_input("SWIM REPL> ")
    lex.input(s)
    
if len(sys.argv) > 1:
    fn = open(sys.argv[1])
    for line in fn.readlines():
        if line == "\n": continue
        if mode == 1:
            lex.input(line)
            while 1:
                tok = lex.token()
                print tok
                if not tok:
                    break
        else:
            yacc.parse(line)
    fn.close()  
else:
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