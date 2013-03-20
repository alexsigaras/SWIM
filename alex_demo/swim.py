<<<<<<< HEAD
# -----------------------------------------------------------------------------
# COLUMBIA UNIVERSITY - FU FOUNDATION SCHOOL OF ENGINEERING
# COMPUTER SCIENCE DEPARTMENT
#
# COMS W4115 - PROGRAMMING LANGUAGES AND TRANSLATORS
# Professor A. Aho
#
# Team 3 Final Project: "SWIM"
# Team Mentor: A. Aho
#
# Team members:
#
#    Name                    Role                         UNI
# Morris Hopkins        Project Manager                 mah2250
# Seungwoo Lee          Language Guru                   sl3492
# Lev Brie              System Architect                ldb2001
# Alexandros Sigaras    System Integrator               as4161
# Michal Wolski         Verification and Validation     mtw2135
#
# Programming and Translational language 
# Prof.Aho
# -----------------------------------------------------------------------------
=======
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
#                               Library Import                                #
#-----------------------------------------------------------------------------#
>>>>>>> Added AND, OR, XOR, NOT

import sys
sys.path.insert(0,"..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'ID','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS','POW','MOD',
    'LPAREN','RPAREN', 'STRING',
    )

# Tokens
t_AND     = r'and|&&'
t_OR      = r'or|\|\|'
t_XOR     = r'xor'
t_NOT     = r'not|!'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
<<<<<<< HEAD
t_ASSIGN  = r'='
t_EQUALS  = r'=='
<<<<<<< HEAD
=======
t_EQUALS  = r'='
>>>>>>> Revert "Updated Styling and added stuff for future expansion"
=======
>>>>>>> Added AND, OR, XOR, NOT
t_POW     = r'\^'
t_MOD     = r'\%'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
<<<<<<< HEAD
t_STRING  = r'\"[a-zA-Z_][a-zA-Z0-9_ ]*\"'

# def t_NUMBER(t):
#     r'\d+'
#     try:
#         t.value = int(t.value)
#     except ValueError:
#         print("Integer value too large %s" % t.value)
#         t.value = 0
#     return t
=======
t_STRING  = r'"[a-zA-Z0-9_ ]*"'
t_IF      = r'if'
t_ELSE    = r'else'
t_DO      = r'do'
t_TRUE    = r'True'
t_FALSE   = r'False'
t_WHILE   = r'while'
t_FOR     = r'for'
t_FOREACH = r'foreach'
>>>>>>> Added AND, OR, XOR, NOT

def t_NUMBER(t):
    r'[0-9]*\.?[0-9]+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %s" % t.value)
        t.value = 0
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex(optimize=1)

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MOD'),
    ('right','UMINUS','POW'),
    )

# dictionary of names
names = { }	

def p_start(t):
    '''start : function
             | statement'''

def p_function(t):
    '''function : ID LPAREN STRING RPAREN
                | ID LPAREN expression RPAREN'''
    if t[1] == "print" : print t[3]
    xvar = t[3]
    print "done function"

def p_statement_assign(t):
    'statement : ID EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print t[1]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POW expression
<<<<<<< HEAD
                  | expression MOD expression'''
    if t[2]   == '+':
=======
                  | expression MOD expression
                  | expression AND expression
                  | expression OR expression
                  | expression XOR expression
                  | NOT expression
                  | TRUE
                  | FALSE'''
    if t[2] == '+':
>>>>>>> Added AND, OR, XOR, NOT
        t[0] = t[1] + t[3]  # add
    elif t[2] == '-':
        t[0] = t[1] - t[3]  # subtract
    elif t[2] == '*':
        t[0] = t[1] * t[3]  # multiply
    elif t[2] == '/':
        t[0] = t[1] / t[3]  # divide
    elif t[2] == '^': 
        t[0] = t[1] ** t[3] # power
    elif t[2] == '%': 
        t[0] = t[1] % t[3]  # remainder3
<<<<<<< HEAD
=======
    elif (t[2] == 'and' or t[2] =='&&'):
        t[0] = t[1] and t[3]
    elif (t[2] == 'or' or t[2] =='||'):
        t[0] = t[1] or t[3]
    elif t[2] == 'xor':
        t[0] = (t[1] and not t[3]) or (not t[1] and t[3])
    elif t[1] == 'not':
        t[0] = not t[2]
    elif t[1] == 'True':
        t[0] = True
    elif t[1] == 'False':
        t[0] = False
>>>>>>> Added AND, OR, XOR, NOT
    elif t[2] == '<': t[0] = t[1] < t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    print "uminus"#t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    #print "push " + str(t[1])#t[0] = t[1]
    t[0] = t[1]

def p_expression_name(t):
    'expression : ID'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    if t:
        print("Syntax error at '%s'" % t.value)
    else:
        print("Syntax error at EOF")

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
