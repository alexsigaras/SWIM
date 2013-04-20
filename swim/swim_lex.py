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
# File: swim_lex.pl                                                           #
# Description: Swim language lexical analysis                                 #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                            1. Declare tokens                                #
#-----------------------------------------------------------------------------#

#---------------------------------#
#        1.1 Reserved tokens      #
#---------------------------------#

reserved = {
    'if'       : 'IF',
    'else'     : 'ELSE',
    'elif'     : 'ELIF',
    'do'       : 'DO',
    'True'     : 'TRUE',
    'true'     : 'TRUELOWERCASE',
    'False'    : 'FALSE',
    'false'    : 'FALSELOWERCASE',
    'while'    : 'WHILE',
    'for'      : 'FOR',
    'each'     : 'EACH',
    'in'       : 'IN',
    'return'   : 'RETURN',
    'break'    : 'BREAK',
    'and'      : 'AND',
    'or'       : 'OR',
    'xor'      : 'XOR',
    'not'      : 'NOT',
    'end'      : 'END',
    'fun'      : 'FUN', 
    'class'    : 'CLASS',
}

#---------------------------------#

#---------------------------------#
#     1.2 Reserved Tokens Table   #
#---------------------------------#

tokens = [
    'LPAREN','RPAREN', 'LSBRACKET', 'RSBRACKET', 'LCBRACKET', 'RCBRACKET', 'SELECTOR', 'COMMA', 'SEMICOLON', 'COLON',
    'STRING1', 'STRING2', 'ID','NUMBER',
    'ASSIGN',
    'EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_OR_EQUAL', 'GREATER_THAN_OR_EQUAL',
    'PLUS','MINUS','MULTIPLY','DIVIDE','POW','MOD'
    ] + list(reserved.values())

#---------------------------------#

#---------------------------------#
#     1.3 Identifier Tokens       #
#---------------------------------#

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LSBRACKET  = r'\['
t_RSBRACKET  = r'\]'
t_LCBRACKET = r'\{'
t_RCBRACKET = r'\}'
t_SELECTOR  = r'@'
t_COMMA     = r','
t_COLON     = r':'
t_SEMICOLON = r';'

#---------------------------------#

#---------------------------------#
#      1.4 Operator Tokens        #
#---------------------------------#

# Logical Operators
t_AND                   = r'&&'
t_OR                    = r'\|\|'
t_NOT                   = r'!'
t_ASSIGN                = r'='

# Comparison Operators
t_EQUALS                = r'=='
t_NOT_EQUALS            = r'!='
t_LESS_THAN             = r'<'
t_GREATER_THAN          = r'>'
t_LESS_THAN_OR_EQUAL    = r'<='
t_GREATER_THAN_OR_EQUAL = r'>='

# Arithmetic Operators
t_PLUS                  = r'\+'
t_MINUS                 = r'-'
t_MULTIPLY              = r'\*'
t_DIVIDE                = r'/'
t_POW                   = r'\^'
t_MOD                   = r'\%'

#---------------------------------#

#---------------------------------#
#     1.5 Variable Tokens         #
#---------------------------------#

t_STRING1 = r'u?"\\?[^"]*"'
t_STRING2 = r"u?'\\?[^']*'"


def t_NUMBER(t):
    r'[0-9]*\.?[0-9]+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %s" % t.value)
        t.value = 0
    return t
    
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

#---------------------------------#

#---------------------------------#
#      1.6  Other Tokens          #
#---------------------------------#

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#---------------------------------#

#---------------------------------#
#       1.7 Comment Tokens        #
#---------------------------------#

def t_COMMENT(t):
    r'\#.*|//.*|/\*(.*[^\*/]|\n|\t)*\*/'
    pass
    # No return value. Token Discarded

#---------------------------------#

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                                 2. Lex                                      #
#-----------------------------------------------------------------------------#
    
import ply.lex as lex
lex.lex(optimize=0)

#-----------------------------------------------------------------------------#