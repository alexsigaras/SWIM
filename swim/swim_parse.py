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
# File: swim_parse.py                                                         #
# Description: Swim Parse Analyzer                                            #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                     1. Common Library Import                                #
#-----------------------------------------------------------------------------#

from core import *
from namespace import Namespace
from types import *

#-----------------------------------------------------------------------------#
#                   2. External Library Import                                #
#-----------------------------------------------------------------------------#

# Parsing
import re
# simplified arithmetic expressions
import operator

# Error handling
from swim_exception import *

# Builtin functions
from swim_builtin import *

#-----------------------------------------------------------------------------#
#                          3.  External Functions                             #
#-----------------------------------------------------------------------------#

def stripe_quotation(string):
    result = string.replace("'","") if string.startswith("'") else string.replace('"', "")
    return result

class swimClass():
    pass
#-----------------------------------------------------------------------------#
#                           4.  Tables & Dictionaries                         #
#-----------------------------------------------------------------------------#

# Precedence Table
precedence = (
    ('nonassoc', 'LESS_THAN', 'LESS_THAN_OR_EQUAL', 'EQUALS', 'NOT_EQUALS', 'GREATER_THAN', 'GREATER_THAN_OR_EQUAL'),
    ('left', 'PLUS', 'MINUS', 'COMMA', 'AND', 'OR', 'XOR'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MOD'),
    ('right', 'NOT'),
    ('right', 'POW'),
    ('left', 'UPLUS', 'UMINUS'),
)

# Namespace stack
identifiers = Namespace() 

# Operators Dictionary
ops = { "+":    operator.add, 
        "-":    operator.sub, 
        "*":    operator.mul, 
        "%":    operator.mod, 
        "/":    operator.div, 
        "^":    operator.pow,
        "<":    operator.lt,
        "<=":   operator.le,
        ">":    operator.gt,
        ">=":   operator.ge,
        "!=":   operator.ne,
        "==":   operator.eq,
        "and":  operator.and_,
        "&&":   operator.and_,
        "or":   operator.or_,
        "||":   operator.or_,
        "xor":  operator.xor
        }

# Colors Table
# Right now this is only used for error codes but it can be used 
# to easily extend printing to other colors.
colorCodes = {
    'black':    '0;30',     'bright gray':  '0;37',
    'blue':     '0;34',     'white':        '1;37',
    'green':    '0;32',     'bright blue':  '1;34',
    'cyan':     '0;36',     'bright green': '1;32',
    'red':      '0;31',     'bright cyan':  '1;36',
    'purple':   '0;35',     'bright red':   '1;31',
    'yellow':   '0;33',     'bright purple':'1;35',
    'dark gray':'1;30',     'bright yellow':'1;33',
    'normal':   '0'
}

#-----------------------------------------------------------------------------#
#                                 5. Grammar                                  #
#-----------------------------------------------------------------------------# 

#----------------------------------------------------#
#                   5.1 Starting                     #
#----------------------------------------------------#

def p_start(t):
    '''start : statements
             | '''
    
    try:
        # Normal mode
        showNodeTree = False
        if(showNodeTree):
            print(t[1].traverse())
        else:
            try:
                result = t[1].do()
                # print result                
                if result is not None and result.__doc__ != "Simple Node":                
                	print(result)
            except Error as e:
            	#print 1
            	#print e
                printErr(t[1].traverse())
                pass
            	#print "[Line :" + str(e.lineno) + "] " + e.msg 
        
        # Saving mode for function and class definition
        ''' TO DO '''
    except:
        pass

#--------------------------------------------------------------#
#                       5.2 Statements                         #
#--------------------------------------------------------------#

import traceback
def p_statements(t):
    '''statements : statement statements
                  | statement'''

    try:
        t[0] = Node ("statements", [t[1], t[2]], "statements")    

        def do(self, id = None, object_name = None):
            try:
                firstResult = self.children[0].do(id = id, object_name = object_name)                         
                if isinstance(firstResult, dict):
                    if firstResult.keys()[0] == "break" or firstResult.keys()[0] == "return":
                        return firstResult
                else: 
                    secondResult = self.children[1].do(id = id, object_name = object_name)
                    if isinstance(secondResult, dict):
                        if secondResult.keys()[0] == "break" or secondResult.keys()[0] == "return":
                            return secondResult              
            except:
                print("Error in statements")
                #print traceback.format_exc()
    except:
        t[0] = Node ("statement", t[1], "statement")

        def do(self, id = None, object_name = None):
            try:                
                return self.children.do(id = id, object_name = object_name)
            except:
                print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_statement(t):
    '''statement : simple_stmt
                 | compound_stmt'''
    super_do(t, 'stmt')


def p_simple_stmt(t):
    '''simple_stmt : expression_stmt
                   | assign_stmt
                   | assign_global_stmt
                   | assign_this_stmt
                   | increment_stmt
                   | decrement_stmt
                   | return_stmt
                   | break_stmt
                   | class_instantiation_stmt
                   | class_setAttribute_stmt
                   | include_stmt'''
    super_do(t, 'simple_stmt')
    #                   | list_stmt
                       # | dictionary_stmt

def p_compound_stmt(t):
    '''compound_stmt : if_stmt
                     | while_stmt
                     | for_stmt                 
                     | function_decl
                     | class_decl_stmt '''
    super_do(t, 'compound_stmt')


# This statement do refactors duplicate code
# that existed in the various statement functions.
# 
#  Currently serves statements and expressions
# 
def super_do(t, typestring):
    t[0] = Node(typestring, t[1], typestring)
    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)
        except:
            print("Error in super do")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)


#--------------------------------------------------------------#
#                 5.2.1 Simple Statements                      #
#--------------------------------------------------------------#

#----------------------------------------------------#
#               5.2.1.1 Expression                   #
#----------------------------------------------------#

def p_statement_expr(t):
    'expression_stmt : expression SEMICOLON'
    super_do(t, 'expr')

#----------------------------------------------------#
#               5.2.1.2 Assignment                   #
#----------------------------------------------------#

def p_statement_assign(t):
    'assign_stmt : ID ASSIGN expression SEMICOLON'

    t[0] = Node("assign", [t[1], t[3]], t[2])

    def do(self, id = None, object_name = None):
        ''' Need to check ID !'''
        try:
            element = self.children[1].do(id = id, object_name = object_name)
            if isinstance(element, list):
                # If the expr is a list
                identifiers.scope_in()
                identifiers["List"].children[1].do(id = id, object_name = object_name)    
                class_attributes = identifiers.getAllItems()
                identifiers.scope_out()
                identifiers[self.children[0]] = Namespace(class_attributes)
                identifiers[self.children[0]]["val"] = element                
            elif isinstance(element, dict):
                #If the expr is a dictionary
                identifiers.scope_in()
                identifiers["Dict"].children[1].do(id = id, object_name = object_name)   
                class_attributes = identifiers.getAllItems()
                identifiers.scope_out()
                identifiers[self.children[0]] = Namespace(class_attributes)
                identifiers[self.children[0]]["val"] = element                   
            else:
                if object_name is not None:
                    identifiers[object_name][self.children[0]] = element
                    return identifiers[object_name][self.children[0]]
                else:
                    identifiers[self.children[0]] = element
                    return identifiers[self.children[0]]
            return identifiers[self.children[0]]        
        except:
            print("Error in assignment statement")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_statement_global_assign(t):
    'assign_global_stmt : GLOBAL ID ASSIGN expression SEMICOLON'
                          
    t[0] = Node("global_assign", [t[2], t[4]], t[3])

    def do(self, id = None, object_name = None):
        ''' Need to check ID !'''
        try:
            element = self.children[1].do(id = id, object_name = object_name)
            identifiers.assign_global(self.children[0], element)
            return identifiers.access_global(self.children[0])
        except:
            print("Error in global assignment statement")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_statement_this_assign(t):
    'assign_this_stmt : THIS DOT ID ASSIGN expression SEMICOLON'
                          
    t[0] = Node("this_assign", [t[3], t[5]], t[4])

    def do(self, id = None, object_name = None):
        ''' Need to check ID !'''
        try:
            element = self.children[1].do(object_name = object_name)
            identifiers[object_name].assign_global(self.children[0], element)
            return identifiers[object_name].access_global(self.children[0])
        except:
            print("Error in this. assignment statement")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#                5.2.1.3 Auto Increment              #
#----------------------------------------------------# 

def p_statement_increment(t):
    'increment_stmt : expression PLUS PLUS SEMICOLON'

    t[0] = Node("increment", t[1], "++")

    def do(self, id = None, object_name = None):
        try:
            if object_name is not None:
                identifiers[object_name][self.children.do(id = True, object_name = object_name)] = self.children.do(id = id, object_name = object_name) + 1
                return identifiers[object_name][self.children.do(id = True, object_name = object_name)]                
            else:
                identifiers[self.children.do(id = True, object_name = object_name)] = self.children.do(id = id, object_name = object_name) + 1
                return identifiers[self.children.do(id = True, object_name = object_name)]
        except:
            print("Error in auto increment statement")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#                5.2.1.4 Auto Decrement              #
#----------------------------------------------------# 

def p_statement_decrement(t):
    'decrement_stmt : expression MINUS MINUS SEMICOLON'

    t[0] = Node("decrement", t[1], "--")

    def do(self, id = None, object_name = None):
        try:
            if object_name is not None:
                identifiers[object_name][self.children.do(id = True, object_name = object_name)] = self.children.do(id = id, object_name = object_name) - 1
                return identifiers[object_name][self.children.do(id = True, object_name = object_name)]                                
            else:
                identifiers[self.children.do(id = True, object_name = object_name)] = self.children.do(id = id, object_name = object_name) - 1
                return identifiers[self.children.do(id = True, object_name = object_name)]
        except:
            print("Error in auto decrement statement")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node) 

#--------------------------------------------------------------#
#                   5.2.2 Compound Statements                  #
#--------------------------------------------------------------#

#----------------------------------------------------#
#               5.2.2.1  If Statement                #
#----------------------------------------------------#

def p_statement_if(t):
    'if_stmt : IF expression DO statements elif_blocks END'

    t[0] = Node ("if", [t[2],t[4],t[5]])

    def do(self, id = None, object_name = None):
        if self.children[0].do(id = id, object_name = object_name):
            try:
                return self.children[1].do(id = id, object_name = object_name)
            except:
                print("Error in if statement")
                print traceback.format_exc()
        else:
            try:
                return self.children[2].do(id = id, object_name = object_name)
            except:
                print("Error in if statement")
                print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_statement_elif_blocks(t):
    '''elif_blocks : elif_block elif_blocks
                   | else_block 
                   | '''
    try:     
        t[0] = Node ("elifs", [t[1], t[2]], "elifs")

        def do(self, id = None, object_name = None):
            if self.children[0].do(id = id, object_name = object_name):
                try:
                    return self.children[0].do(id = id, object_name = object_name)
                except:
                    print traceback.format_exc()
            else:
                try:
                    return self.children[1].do(id = id, object_name = object_name)
                except:
                    print("Error in elif blocks")
                    print traceback.format_exc()
    except:
        try:
            t[0] = Node ("else", t[1], "else")

            def do(self, id = None, object_name = None):
                try:
                    return self.children.do(id = id, object_name = object_name)
                except:
                    print("Error in elif blocks")
                    print traceback.format_exc()
        except:
            t[0] = Node ("else", None, "else")
            def do(self, id = None, object_name = None):
                try:
                    return None
                except:
                    print("Error in elif blocks")
                    print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)                   

def p_statement_elif_block(t):
    'elif_block : ELIF expression DO statements'

    t[0] = Node ("elif", [t[2], t[4]])

    def do(self, id = None, object_name = None):
        if self.children[0].do(id = id, object_name = object_name):
            try:
                return self.children[1].do
            except:
                print("Error in elif block")
                print traceback.format_exc()
        else:
            try:
                return False
            except:
                print("Error in elif block")
                print traceback.format_exc()
    
    t[0].do = MethodType(do, t[0], Node)

def p_statement_else_block(t):
    'else_block : ELSE statements'

    t[0] = Node ("else", t[2])

    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)
        except:
            print("Error in else block")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#              5.2.2.2 While Statement               #
#----------------------------------------------------#

def p_statement_while(t):
    'while_stmt : WHILE expression DO statements END'

    t[0] = Node("while", [t[2],t[4],t[1]])

    def do(self, id = None, object_name = None):
        try:            
            while self.children[0].do(id = id, object_name = object_name): 
                result = self.children[1].do(id = id, object_name = object_name)
                if isinstance(result, dict):
                    if result.keys()[0] == "break":
                        break
                    elif result.keys()[0] == "return":
                        return result
        except:
            print("Error in while statement")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#             5.2.2.3 For Statement                  #
#----------------------------------------------------#

def p_statement_for(t):
    'for_stmt : FOR EACH ID IN element DO statements END'

    t[0] = Node("for", [t[3], t[5], t[7]] , "for")

    def do(self, id = None, object_name = None):
        try:
            # val = self.children[1].do(id = id, object_name = object_name)[0].attr['val']
            for temp in self.children[1].do(id = id, object_name = object_name):
                if object_name is not None:
                    identifiers[object_name][self.children[0]] = temp
                else:
                    identifiers[self.children[0]] = temp
                result  = self.children[2].do(id = id, object_name = object_name)

                if isinstance(result, dict):
                    if result.keys()[0] == "break":
                        break
                    elif result.keys()[0] == "return":
                        return result
        except:
            print("Error in for statement")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#             5.2.2.4 Include                        #
#----------------------------------------------------#
import sys
import os
sys.path.insert(0,os.path.join("..", "include"))

import ply.yacc as yacc

def p_statement_include(t):
    'include_stmt : INCLUDE ID SEMICOLON'

    t[0] = Node("include", t[2] , "include")

    def do(self, id = None, object_name = None):
        try:
            fn = open( os.path.join( "lib", self.children + ".swim"))
            s = fn.read()
            yacc.parse(s)
            fn.close()              
        except:
            print("Error in include")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)
#----------------------------------------------------#
#              5.2.2.4 Classes                       #
#----------------------------------------------------#

def p_class_decl(t):
    'class_decl_stmt : CLASS ID DO statements END'

    t[0] = Node("class", [t[2], t[4]], t[2])

    def do(self, id=None, object_name = None):
        try:
            identifiers[self.children[0]] = self # child 0 is id, adds tree to id ref in symbol table
            return self
        except:
            print("Error in Class declaration")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node) # adds the method do dynamically to class_declaration method

def p_class_instantiation(t):
    'class_instantiation_stmt : ID ASSIGN NEW ID LPAREN RPAREN SEMICOLON '

    t[0] = Node("class_instantiation", [t[1],t[4]], "class_instantiation")

    def do(self, id = None, object_name = None):
        try:
            identifiers.scope_in()
            identifiers[self.children[1]].children[1].do(id = id, object_name = object_name)            
            class_attributes = identifiers.getAllItems()
            identifiers.scope_out()
            identifiers[self.children[0]] = Namespace(class_attributes)
        except:
            print("Error in class instantiation")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_class_getAttribute(t):
    '''class_getAttribute_expr : ID DOT ID
                               | ID DOT function_call_expr'''

    t[0] = Node("classAttribute", [t[1],t[3]], "classAttribute")

    def do(self, id = None, object_name = None):
        try:
            return identifiers[self.children[0]][self.children[1]]
        except:
            try:       
                return self.children[1].do(object_name = self.children[0])
            except:
                print("Error in class get Child")
                print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_class_setAttribute(t):
    '''class_setAttribute_stmt : ID DOT ID ASSIGN expression SEMICOLON'''
    t[0] = Node("classAttribute", [t[1],t[3],t[5]], "classAttribute")

    def do(self, id = None, object_name = None):
        try:
            identifiers[self.children[0]][self.children[1]] = self.children[2].do(id = id, object_name = object_name)
            return identifiers[self.children[0]][self.children[1]]
        except:
            print("Error in class get Child")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#              5.2.2.4 Functions                     #
#----------------------------------------------------#

def p_function_decl(t):
    'function_decl : FUN ID LPAREN elements RPAREN DO statements END'

    t[0] = Node('fundef', [t[2],t[4],t[7]], 'fundef')

    def do(self, id = None, object_name = None):
        try:
            identifiers[self.children[0]] = self  # child 0 is id, adds tree to id ref in symbol table
            return self
        except:
            print("Error in Function declaration")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)      # adds the method do dynamically to function_declaration method

def p_function_call_expr(t):
    '''function_call_expr : ID LPAREN elements RPAREN'''

    t[0] = Node("funcallexpr", [t[1],t[3]], 'funcallexpr')

    if t[1] == "print":
        def do(self, id = None, object_name = None):
            try:
                if self.children[1].do(id = id, object_name = object_name)[0]["type"] == 'List' or self.children[1].do(id = id, object_name = object_name)[0]["type"] == 'Dict' or self.children[1].do(id = id, object_name = object_name)[0]["type"] == 'Str':
                    val = self.children[1].do(id = id, object_name = object_name)[0]['val']
                else:
                    val = self.children[1].do(id = id, object_name = object_name)[0]
                return builtin_print(val)
            except:
                try:
                    val = self.children[1].do(id = id, object_name = object_name)[0]
                    return builtin_print(val) 
                except:
                    print("Error in builtin print")
    elif t[1] == "printErr":
        def do(self, id = None, object_name = None):            
            try:
                return builtin_print(self.children[1].do(id = id, object_name = object_name)[0], colorCodes['red'])
            except:
                print("Error in builtin printErr")
    elif t[1] == "pdf":
        def do(self, id = None, object_name = None):
            try: 
                return buildtin_pdf(self.children[1].do(id = id, object_name = object_name))
            except:
                print("Error in builtin pdf")
                print traceback.format_exc()
    else:      
        def do(self, id = None, object_name = None):
            #class method"
            if object_name is not None:
                identifiers[object_name].scope_in()
                try:
                    func = identifiers[object_name][self.children[0]]
                except:
                    print "Namespce does not have the function!"
                    identifiers[object_name].scope_out()
                    return None
                try:
                    cnt = 0
                    # set to true so it returns name and not variable
                    for name in func.children[1].do(True):
                        # take the name and assign it into the new namespace
                        # pass by ref via python
                        identifiers[object_name][name] = self.children[1].do(id = id, object_name = object_name)[cnt]
                        cnt += 1
                except:
                    print "Function parameter error!"
                    return None             
                try:
                    result = func.children[2].do(id = id, object_name = object_name)
                except:
                    print "function call error"
                    identifiers[object_name].scope_out()
                    return None
                try:
                    if result.keys()[0] == "return":
                        identifiers[object_name].scope_out()
                        return result.values()[0]
                except:
                    identifiers[object_name].scope_out()
                    return result 

            
            #function
            else:
                identifiers.scope_in()
                func = identifiers[self.children[0]]

                try:
                    cnt = 0
                    for name in func.children[1].do(True):
                        # take the name and assign it into the new namespace
                        # pass by ref via python
                        identifiers[name] = self.children[1].do(id = id, object_name = object_name)[cnt]
                        cnt += 1
                except:
                    print "Function parameter error!"
                    return None 
                result = func.children[2].do(id = id, object_name = object_name)
                try:
                    if result.keys()[0] == "return":
                        identifiers.scope_out()
                        return result.values()[0]
                except:
                    identifiers.scope_out()
                    return result 

    t[0].do = MethodType(do, t[0], Node)
    
#----------------------------------------------------#
#                    5.2.2.5 Return                  #
#----------------------------------------------------#

def p_return(t):
    '''return_stmt : RETURN elements SEMICOLON'''
    
    t[0] = Node('return', t[2], 'return')    
    def do(self, id = None, object_name = None):
        try: 
            return {"return" :  self.children.do(id = id, object_name = object_name)[0]}
        except:
            print("Error in return statement")

    t[0].do = MethodType(do, t[0], Node)      # adds the method do dynamically to function_declaration method

#----------------------------------------------------#
#                    5.2.2.5 Break                   #
#----------------------------------------------------#

def p_break(t):
    '''break_stmt : BREAK SEMICOLON'''
    
    t[0] = Node('break', t[0], 'break') 

    def do(self, id = None, object_name = None):
        try:
            return {"break" : None}
        except:
            print("Error in break statement")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)      # adds the method do dynamically to function_declaration method

#--------------------------------------------------------------#
#                       5.3 Expressions                        #
#--------------------------------------------------------------#

def p_expression(t):
    '''expression : unary_expr
                  | binary_expr'''
    
    t[0] = Node("expr", t[1], 'expr')

    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)
        except:
            print("Error in expression")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_unary_expr(t):
    '''unary_expr : boolean_expr
                  | not_expr
                  | number_expr
                  | id_expr
                  | string_expr
                  | list_expr
                  | dictionary_expr
                  | parse_text_expr
                  | group_expr
                  | uplus_expr
                  | uminus_expr
                  | class_getAttribute_expr
                  | function_call_expr'''

    t[0] = Node("expr", t[1], 'expr')

    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)
        except:
            print("Error in unary expression")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_binary_expr(t):
    '''binary_expr : arithmetic_expr
                   | conditional_expr'''
    
    t[0] = Node("expr", t[1], 'expr')

    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)
        except:
            print("Error in binary expression")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#--------------------------------------------------------------#
#                   5.3.1 Simple Expressions                   #
#--------------------------------------------------------------#

#----------------------------------------------------#
#               5.3.1.1 Boolean                      #
#----------------------------------------------------#
def p_expression_boolean(t):
    '''boolean_expr : TRUE
                    | TRUELOWERCASE
                    | FALSE
                    | FALSELOWERCASE'''
                  
    t[0] = Node("boolean", t[1], 'boolean')
    
    # if t[1] == "True" or t[1] == "true":
    if t[1] in ["True","true"]:
        def do(self, id = None, object_name = None):
            try:
                return True
            except:
                print("Error in True boolean expression")
                print traceback.format_exc()
    elif t[1] in ["False", "false"]:
        def do(self, id = None, object_name = None):
            try:
                return False
            except:
                print("Error in False boolean expression")
                print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#               5.3.1.2 Not                          #
#----------------------------------------------------#

def p_expression_not_op(t):
    '''not_expr : NOT expression'''
    
    t[0] = Node("logop", t[2], t[1])
    def do(self, id = None, object_name = None):
        try:
            return not self.children.do(id = id, object_name = object_name)
        except:
            print("Error in not expression")
            print traceback.format_exc()
        
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#              5.3.1.3 Number                        #
#----------------------------------------------------#

def p_expression_number(t):
    'number_expr : NUMBER'

    t[0] = Node("number", t[1], 'number')

    def do(self, id = None, object_name = None):
        try:
            return self.children
        except:
            print("Error in number expression")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#
#              5.3.1.4 ID                            #
#----------------------------------------------------#

def p_expression_name(t):
    'id_expr : ID'
    
    t[0] = Node("name", str(t[1]), 'name')

    def do(self, id = None, object_name = None):
        try:
            if id is not None:
                return self.children
            else:
                if object_name is not None:
                    return identifiers[object_name][self.children]
                else:
                    return identifiers[self.children]
        except LookupError:
            print(str(t.lexer.lineno) + ":\nexpression could not be recognized as stored value.\n")
            raise NameException(t.lexer.lineno, str(self.children))

    t[0].do = MethodType(do, t[0], Node)     

#----------------------------------------------------#
#              5.3.1.5 String                        #
#----------------------------------------------------#

def p_expression_string(t):
    '''string_expr : STRING1
                   | STRING2'''

    t[0] = Node("string", stripe_quotation(t[1]), 'string')

    def do(self, id = None, object_name = None):
        try:
            return self.children
        except:
            print("Error in string expressions")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)  

#----------------------------------------------------#
#               5.3.1.6 List                         #
#----------------------------------------------------#

def p_expression_list(t):
    'list_expr : LSBRACKET elements RSBRACKET'

    t[0] = Node("list", t[2], "List")

    def do(self, id = None, object_name = None):
        try:
            return list( self.children.do(id = id, object_name = object_name) )
        except:
            print("Error in list expression")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_elements(t):
    '''elements : element COMMA elements
                | element
                | '''

    try:
        t[0] = Node ("elements", [t[1], t[3]], "elements")    

        def do(self, id = None, object_name = None):
            try:
                return list([self.children[0].do(id = id, object_name = object_name)] + self.children[1].do(id = id, object_name = object_name))
            except:
                print("Error in elements")
                print traceback.format_exc()
    except:
        try:
            t[0] = Node ("element", t[1], "element")

            def do(self, id = None, object_name = None):
                try:
                    return [self.children.do(id = id, object_name = object_name)]
                except:
                    print("Error in element")
                    print traceback.format_exc()
        except:
            t[0] = Node ("empty_element", None, "empty_element")
            def do(self, id = None, object_name = None):
                try:
                    return []
                except:
                    print("Error in empty element")
                    print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_element(t):
    'element : expression'
    
    t[0] = Node("expr", t[1], 'expr')

    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)
        except:  
            print("Error in element")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#
#               5.3.1.7 Dictionary                   #
#----------------------------------------------------#

def p_expression_dictionary(t):
    'dictionary_expr : LCBRACKET dictionary_objects RCBRACKET'

    t[0] = Node("dictionary", t[2], "dictionary")

    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)
        except:
            print("Error in dictionary expression")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_objects(t):
    '''dictionary_objects : dictionary_object COMMA dictionary_objects
                          | dictionary_object
                          | '''
    try:
        t[0] = Node ("dictionary_objects", [t[1], t[3]], "dictionary_objects")

        def do(self, id = None, object_name = None):
            try:
                temp  = self.children[0].do(id = id, object_name = object_name)
                temp.update(self.children[1].do(id =id, object_name = object_name))
                return temp
            except:
                print("Error in empty dictionary objects")
                print traceback.format_exc()

    except:
        try:
            t[0] = Node ("dictionary_object", t[1], "dictionary_object")
            def do(self, id = None, object_name = None):
                try:
                    return self.children.do(id = id, object_name = object_name)
                except:
                    print("Error in dictionary object")
                    print traceback.format_exc()
        except:
            t[0] = Node ("empty_dictionary_object", None, "empty_dictionary_object")
            def do(self, id = None, object_name = None):
                try:
                    return {}
                except:
                    print("Error in empty dictionary object")
                    print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_object(t):
    'dictionary_object : key COLON value'

    t[0] = Node("dictionary_object", [t[1], t[3]], "dictionary_object")

    def do(self, id = None, object_name = None):
        try:
            return {self.children[0].do(id = id, object_name = object_name) : self.children[1].do(id = id, object_name = object_name)}
        except:
            print("Error in dictionary object")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_key(t):
    '''key : STRING1
           | STRING2'''

    t[0] = Node("key", stripe_quotation(t[1]), 'key')

    def do(self, id = None, object_name = None):
        try:
            return self.children
        except:
            print("Error in dictionary key")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_value(t):
    'value : expression'

    t[0] = Node("value", t[1], 'value')

    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)
        except:
            print("Error in dictionary value")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#               5.3.1.8 Parse                        #
#----------------------------------------------------#

def p_expression_parse_text(t):
    'parse_text_expr : SELECTOR LPAREN elements RPAREN'
    
    t[0] = Node("selector", t[3], t[1])
    def do(self, id = None, object_name = None):
        try:
            raw_selector = self.children.do(id = id, object_name = object_name)[0]
            selector = stripe_quotation(raw_selector)
            raw_url = self.children.do(id = id, object_name = object_name)[1]

            if type(raw_url) == str:
                url = stripe_quotation(raw_url)
                d = pq(url=url, opener=lambda url: urllib.urlopen(url).read())
                return d(selector)
            else:
                return raw_url(selector)
        except Exception:
            print("Mismatch grammar for parsing!")
            print traceback.format_exc()
                
    t[0].do = MethodType(do, t[0], Node)      

#----------------------------------------------------#
#               5.3.1.9 Group                        #
#----------------------------------------------------#

def p_expression_group(t):
    'group_expr : LPAREN expression RPAREN'
    
    t[0] = Node("group", t[2], 'group')
    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)    
        except:
            print("There was an error in the group ( ) expression")
            print traceback.format_exc()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#               5.3.1.10 Unary Plus                  #
#----------------------------------------------------#

def p_expression_uplus(t):
    'uplus_expr : PLUS expression %prec UPLUS'
    
    t[0] = Node("uplus", t[2], 'uplus')
    def do(self, id = None, object_name = None):
        try:
            return self.children.do(id = id, object_name = object_name)
        except:
            print("There was an error in the unary plus expression")
            print traceback.format_exc()
        
    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#
#              5.3.1.11 Unary Minus                  #
#----------------------------------------------------#

def p_expression_uminus(t):
    'uminus_expr : MINUS expression %prec UMINUS'
    
    t[0] = Node("uminus", t[2], 'uminus')
    def do(self, id = None, object_name = None):
        try:
            return -self.children.do(id = id, object_name = object_name)
        except:
            print("There was an error in the unary minus expression")
            print traceback.format_exc()
        
    t[0].do = MethodType(do, t[0], Node) 
    
#--------------------------------------------------------------#
#                   5.3.1 Compound Expressions                 #
#--------------------------------------------------------------#

#----------------------------------------------------#
#            5.3.1.1 Arithmetic Operations           #
#----------------------------------------------------#

def p_expression_arithmetic_op(t):
    '''arithmetic_expr : expression PLUS expression 
                       | expression MINUS expression 
                       | expression MULTIPLY expression 
                       | expression DIVIDE expression
                       | expression POW expression 
                       | expression MOD expression'''
    
    t[0] = Node("arithmetic_op", [t[1], t[3]], t[2])
    def do(self, id = None, object_name = None):
            try:        
                return ops[self.leaf](self.children[0].do(id = id, object_name = object_name), self.children[1].do(id = id, object_name = object_name))
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id = id, object_name = object_name)) + " " + self.leaf + " " + str(self.children[1].do(id = id, object_name = object_name))) 

    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#
#        5.3.1.2 Conditional Operations              #
#----------------------------------------------------#

def p_expression_cond_op(t):
    '''conditional_expr : expression AND expression
                        | expression OR expression
                        | expression XOR expression
                        | expression EQUALS expression
                        | expression NOT_EQUALS expression
                        | expression GREATER_THAN expression
                        | expression LESS_THAN expression
                        | expression GREATER_THAN_OR_EQUAL expression
                        | expression LESS_THAN_OR_EQUAL expression'''

    t[0] = Node("conditional_expr", [t[1], t[3]], t[2])
    def do(self, id = None, object_name = None):
            try:
                return ops[self.leaf](self.children[0].do(id = id, object_name = object_name), self.children[1].do(id = id, object_name = object_name))       
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id = id, object_name = object_name)) + " " + self.leaf + " " + str(self.children[1].do(id = id, object_name = object_name)))

    t[0].do = MethodType(do, t[0], Node)

#--------------------------------------------------------------#
 
#----------------------------------------------------#
#                     5.4 Error                      #
#----------------------------------------------------#

def p_error(t):
    if t:
        print("Syntax error at '%s'" % t.value)
    else:
        print("Syntax error at EOF")

#----------------------------------------------------#

#-----------------------------------------------------------------------------#