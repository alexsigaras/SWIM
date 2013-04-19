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

#-----------------------------------------------------------------------------#
#                           4.  Precedence                                    #
#-----------------------------------------------------------------------------#

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

#-----------------------------------------------------------------------------#
#                                 5. Grammar                                  #
#-----------------------------------------------------------------------------# 

#----------------------------------------------------#
#                   5.1 Starting                     #
#----------------------------------------------------#

def p_start(t):
    '''start : statements'''
    
    # Normal mode
    showNodeTree = False
    if(showNodeTree):
        print(t[1].traverse())
    else:
        try:
            result = t[1].do()
            #if result is not None:                
            #	print(result)
        except Error as e:
        	#print 1
        	#print e
            print(t[1].traverse())
            pass
        	#print "[Line :" + str(e.lineno) + "] " + e.msg 
    
    # Saving mode for function and class definition
    ''' TO DO '''

#--------------------------------------------------------------#
#                       5.2 Statements                         #
#--------------------------------------------------------------#

def p_statements(t):
    '''statements : statement statements
                  | statement'''
    try:
        t[0] = Node ("statements", [t[1], t[2]], "statements")    

        def do(self, id = None):
            try:
                firstResult = self.children[0].do(id)
                if firstResult == "break":
                    return "break"
                elif firstResult == "return":
                    return "return"
                else: 
                    secondResult = self.children[1].do(id)
                    if secondResult == "break":
                        return "break"
                    elif secondResult == "return":
                        return "return"                    
            except:
                raise Exception

    except:
        t[0] = Node ("statement", t[1], "statement")

        def do(self, id = None):
            try:                
                return self.children.do()
            except:
                raise Exception
    t[0].do = MethodType(do, t[0], Node)

def p_statement(t):
    '''statement : simple_stmt
                 | compound_stmt'''

    t[0] = Node("stmt", t[1], 'stmt')
    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
                raise Exception
    t[0].do = MethodType(do, t[0], Node)

def p_simple_stmt(t):
    '''simple_stmt : expression_stmt
                   | assign_stmt
                   | increment_stmt
                   | decrement_stmt
                   | list_stmt
                   | dictionary_stmt
                   | function_call_stmt
                   | return_stmt
                   | break_stmt
                   '''
#
    t[0] = Node("stmt", t[1], 'stmt')
    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
                raise Exception
    t[0].do = MethodType(do, t[0], Node)

def p_compound_stmt(t):
    '''compound_stmt : if_stmt
                     | while_stmt
                     | for_stmt                 
                     | function_decl'''
    
    t[0] = Node("stmt", t[1], 'stmt')
    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
                raise Exception
    t[0].do = MethodType(do, t[0], Node)

#--------------------------------------------------------------#
#                 5.2.1 Simple Statements                      #
#--------------------------------------------------------------#

#----------------------------------------------------#
#               5.2.1.1 Expression                   #
#----------------------------------------------------#

def p_statement_expr(t):
    'expression_stmt : expression'
    
    t[0] = Node("expr", t[1], 'expr')
    def do(self, id = None):
        return self.children.do(id)
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#               5.2.1.2 Assignment                   #
#----------------------------------------------------#
    
def p_statement_assign(t):
    '''assign_stmt : ID ASSIGN expression SEMICOLON
                   | ID ASSIGN function_call_stmt SEMICOLON'''

    t[0] = Node("assign", [t[1], t[3]], t[2])
    def do(self, id = None):
        ''' Need to check ID !'''       
        identifiers[self.children[0]] = self.children[1].do()
        return identifiers[self.children[0]]
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#                5.2.1.3 Auto Increment              #
#----------------------------------------------------# 

def p_statement_increment(t):
    'increment_stmt : expression PLUS PLUS SEMICOLON'
    t[0] = Node("increment", t[1], "++")
    def do(self, id = None):
        identifiers[self.children.do(True)] = self.children.do() + 1
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#                5.2.1.4 Auto Decrement              #
#----------------------------------------------------# 

def p_statement_decrement(t):
    'decrement_stmt : expression MINUS MINUS SEMICOLON'
    t[0] = Node("decrement", t[1], "--")
    def do(self, id = None):
        identifiers[self.children.do(True)] = self.children.do() - 1
    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#
#                  5.2.1.5 List                      #
#----------------------------------------------------#

def p_list(t):
    'list_stmt : ID ASSIGN LSBRACKET elements RSBRACKET SEMICOLON'

    t[0] = Node("list", [t[1],t[4]], "elements")
    def do(self, id = None):
        ''' Need to check ID !'''
        try:
            identifiers[self.children[0]] = self.children[1].do(id)
            return identifiers[self.children[0]]
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)

def p_elements(t):
    '''elements : element COMMA elements
                | element
                |'''
    try:
        t[0] = Node ("elements", [t[1], t[3]], "elements")    

        def do(self, id = None):
            try:
                return list([self.children[0].do(id)] + self.children[1].do(id))
            except:
                raise Exception

    except:
        try:
            t[0] = Node ("element", t[1], "element")

            def do(self, id = None):
                try:
                    return [self.children.do(id)]
                except:
                    raise Exception
        except:
            t[0] = Node ("empty_element", None, "empty_element")
            def do(self, id = None):
                try:
                    return []
                except:
                    raise Exception
    t[0].do = MethodType(do, t[0], Node)

def p_element(t):
    '''element : expression'''
    
    t[0] = Node("expr", t[1], 'expr')
    def do(self, id = None):
        try:
            return self.children.do(id)
        except:  
            raise Exception
    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#
#                 5.2.1.6 Dictionary                 #
#----------------------------------------------------#

def p_dictionary(t):
    '''dictionary_stmt : ID ASSIGN LCBRACKET dictionary_objects RCBRACKET SEMICOLON'''
    t[0] = Node("dictionary", [t[1],t[4]], "dictionary")
    def do(self, id = None):
        ''' Need to check ID !'''
        try:       
            identifiers[self.children[0]] = self.children[1].do(id)
            return identifiers[self.children[0]]
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)


def p_dictionary_objects(t):
    '''dictionary_objects : dictionary_object COMMA dictionary_objects
                          | dictionary_object
                          |'''
    try:
        t[0] = Node ("dictionary_objects", [t[1], t[3]], "dictionary_objects")

        def do(self, id = None):
            try:
                temp  = self.children[0].do(id)
                temp.update(self.children[1].do(id))
                return temp
            except:
                raise Exception

    except:
        try:
            t[0] = Node ("dictionary_object", t[1], "dictionary_object")
            def do(self, id = None):
                try:
                    return self.children.do(id)
                except:
                    raise Exception
        except:
            t[0] = Node ("empty_dictionary_object", None, "empty_dictionary_object")
            def do(self, id = None):
                try:
                    return {}
                except:
                    raise Exception
    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_object(t):
    'dictionary_object : key COLON value'
    t[0] = Node("dictionary_object", [t[1], t[3]], "dictionary_object")
    def do(self, id = None):
        try:
            return {self.children[0].do(id) : self.children[1].do(id)}
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_key(t):
    '''key : STRING1
           | STRING2'''

    t[0] = Node("key", stripe_quotation(t[1]), 'key')
    def do(self, id = None):
        try:
            return self.children
        except:
            raise Exception

    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_value(t):
    'value : expression'
    t[0] = Node("value", t[1], 'value')
    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
            raise Exception
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

    def do(self, id = None):
        if self.children[0].do(id):
            try:
                return self.children[1].do(id)
            except:
                raise Exception
        else:
            try:
                return self.children[2].do(id)
            except:
                raise Exception

    t[0].do = MethodType(do, t[0], Node)

def p_statement_elif_blocks(t):
    '''elif_blocks : elif_block elif_blocks
                   | else_block 
                   | '''
    try:     
        t[0] = Node ("elifs", [t[1], t[2]], "elifs")

        def do(self, id = None):
            if self.children[0].do(id):
                try:
                    return self.children[0].do(id)
                except:
                    raise Exception
            else:
                try:
                    return self.children[1].do(id)
                except:
                    raise Exception
    except:
        try:
            t[0] = Node ("else", t[1], "else")

            def do(self, id = None):
                try:
                    return self.children.do(id)
                except:
                    raise Exception
        except:
            t[0] = Node ("else", None, "else")
            def do(self, id = None):
                try:
                    return None
                except:
                    raise Exception
    t[0].do = MethodType(do, t[0], Node)                   

def p_statement_elif_block(t):
    'elif_block : ELIF expression DO statements'

    t[0] = Node ("elif", [t[2], t[4]])

    def do(self, id = None):
        if self.children[0].do(id):
            try:
                return self.children[1].do
            except:
                raise Exception
        else:
            try:
                return False
            except:
                raise Exception
    
    t[0].do = MethodType(do, t[0], Node)

def p_statement_else_block(t):
    'else_block : ELSE statements'

    t[0] = Node ("else", t[2])

    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
            raise Exception

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#              5.2.2.2 While Statement               #
#----------------------------------------------------#

def p_statement_while(t):
    'while_stmt : WHILE expression DO statements END'

    t[0] = Node("while", [t[2],t[4],t[1]])

    def do(self, id = None):
        try:            
            while self.children[0].do(): 
                self.children[1].do()
                self.do()
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#             5.2.2.3 For Statement                  #
#----------------------------------------------------#

def p_statement_for(t):
    'for_stmt : FOR EACH ID IN element DO statements END'
    t[0] = Node("for", [t[3], t[5], t[7]] , "for")
    def do(self, id = None):
        try:
            for temp in self.children[1].do():
                identifiers[self.children[0]] = temp
                result  = self.children[2].do()
                if result == "break":
                    break
                elif result == "return":
                    return "return"
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#              5.2.2.4 Functions                     #
#----------------------------------------------------#

def p_function_decl(t):
    '''function_decl : FUN ID LPAREN elements RPAREN DO statements END'''
    t[0] = Node('fundef', [t[2],t[4],t[7]], 'fundef')
    def do(self, id = None):
        identifiers[self.children[0]] = self  # child 0 is id, adds tree to id ref in symbol table
        return self
    t[0].do = MethodType(do, t[0], Node)      # adds the method do dynamically to function_declaration method

def p_function_call(t):
    '''function_call_stmt : ID LPAREN elements RPAREN SEMICOLON'''
    t[0] = Node("funcall", [t[1],t[3]], 'funcall')
  

    if t[1] == "print":
        def do(self, id = None):
            return builtin_print(self.children[1].do()[0])
    elif t[1] == "pdf":
        def do(self, id = None):
            return buildtin_pdf(self.children[1].do())
    else:      
        @identifiers.scope
        def do(self, id = None):
            func = identifiers[self.children[0]]
            try:
                cnt = 0
                # set to true so it returns name and not variable
                for name in func.children[1].do(True):
                    # take the name and assign it into the new namespace
                    # pass by ref via python
                    identifiers[name] = self.children[1].do()[cnt]
                    cnt += 1
            except:
                print "Function parameter error!"
                return None 
            result = identifiers[self.children[0]].children[2].do() 
            if result == "return":
                return "return"
            return result 
    t[0].do = MethodType(do, t[0], Node)

# def p_function_statements(t):
#     '''function_stmt : statement RETURN statements
#                      | statement
#                      |'''
#     try:
#             t[0] = Node ("function_stms", [t[1], t[3]], "function_stms")    

#             def do(self, id = None):
#                 try:
#                     return list([self.children[0].do(id)] + self.children[1].do(id))
#                 except:
#                     raise Exception

#         except:
#             try:
#                 t[0] = Node ("function_stm", t[1], "function_stm")

#                 def do(self, id = None):
#                     try:
#                         return [self.children.do(id)]
#                     except:
#                         raise Exception
#             except:
#                 t[0] = Node ("empty_function_stmt", None, "empty_function_stmt")
#                 def do(self, id = None):
#                     try:
#                         return []
#                     except:
#                         raise Exception
#         t[0].do = MethodType(do, t[0], Node)
    
#----------------------------------------------------#
#                    5.2.2.5 Return                  #
#----------------------------------------------------#

def p_return(t):
    '''return_stmt : RETURN elements SEMICOLON'''
    
    t[0] = Node('return', t[2], 'return')    
    def do(self, id = None):
        # return self.children.do()[0]
        return "return"
    t[0].do = MethodType(do, t[0], Node)      # adds the method do dynamically to function_declaration method

#----------------------------------------------------#
#                    5.2.2.5 Break                   #
#----------------------------------------------------#

def p_break(t):
    '''break_stmt : BREAK SEMICOLON'''
    
    t[0] = Node('break', t[0], 'break')    
    def do(self, id = None):
        #print "Entered Break"
        return "break"
    t[0].do = MethodType(do, t[0], Node)      # adds the method do dynamically to function_declaration method

#--------------------------------------------------------------#
#                       5.3 Expressions                        #
#--------------------------------------------------------------#

def p_expression(t):
    '''expression : unary_expr
                  | binary_expr'''
    
    t[0] = Node("expr", t[1], 'expr')
    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
            raise Exception
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
                  | uminus_expr'''

    t[0] = Node("expr", t[1], 'expr')
    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)

def p_binary_expr(t):
    '''binary_expr : arithmetic_expr
                   | conditional_expr'''
    
    t[0] = Node("expr", t[1], 'expr')
    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)

#--------------------------------------------------------------#
#                   5.3.1 Simple Expressions                   #
#--------------------------------------------------------------#

#----------------------------------------------------#
#               5.3.1.1 Boolean                      #
#----------------------------------------------------#
def p_expression_boolean(t):
    '''boolean_expr : TRUE
                    | FALSE'''
                  
    t[0] = Node("boolean", t[1], 'boolean')
    
    if t[1] == "True":
        def do(self, id = None):
            try:
                return True
            except:
                raise Exception
    elif t[1] == "False":
        def do(self, id = None):
            try:
                return False
            except:
                raise Exception
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#               5.3.1.2 Not                          #
#----------------------------------------------------#

def p_expression_not_op(t):
    '''not_expr : NOT expression'''
    
    t[0] = Node("logop", t[2], t[1])
    def do(self, id = None):
        try:
            return not self.children.do(id)
        except:
            raise Exception
        
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#              5.3.1.3 Number                        #
#----------------------------------------------------#

def p_expression_number(t):
    'number_expr : NUMBER'

    t[0] = Node("number", t[1], 'number')
    def do(self, id = None):
        try:
            return self.children
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#
#              5.3.1.4 ID                            #
#----------------------------------------------------#

def p_expression_name(t):
    'id_expr : ID'
    
    t[0] = Node("name", str(t[1]), 'name')
    def do(self, id = None):
        try:
            if id is not None:
                return self.children
            else:
                return identifiers[self.children]
        except LookupError:
            print(str(t.lexer.lineno) + ":\nexpression could not be recognized as stored value.\n")
            raise NameException(t.lexer.lineno, str(self.children))
    t[0].do = MethodType(do, t[0], Node)     

#----------------------------------------------------#
#              5.3.1.4 String                        #
#----------------------------------------------------#

def p_expression_string(t):
    '''string_expr : STRING1
                   | STRING2''' 
    t[0] = Node("string", stripe_quotation(t[1]), 'string')
    def do(self, id = None):
        try:
            return self.children
        except:
            raise Exception

    t[0].do = MethodType(do, t[0], Node)  

#----------------------------------------------------#
#               5.3.1.5 List                         #
#----------------------------------------------------#

def p_expression_list(t):
    'list_expr : LSBRACKET elements RSBRACKET'

    t[0] = Node("list", t[2], "list")

    def do(self, id = None):
        try:
            return list( self.children.do(id) )
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#               5.3.1.5 Dictionary                   #
#----------------------------------------------------#

def p_expression_dictionary(t):
    'dictionary_expr : LCBRACKET dictionary_objects RCBRACKET'

    t[0] = Node("dictionary", t[2], "dictionary")

    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#               5.3.1.6 Parse                        #
#----------------------------------------------------#

def p_expression_parse_text(t):
    'parse_text_expr : SELECTOR LPAREN elements RPAREN'
    
    t[0] = Node("selector", t[3], t[1])
    def do(self, id = None):
        try:
            raw_selector = self.children.do(id)[0]
            selector = stripe_quotation(raw_selector)
            raw_url = self.children.do(id)[1]

            if type(raw_url) == str:
                url = stripe_quotation(raw_url)
                d = pq(url=url, opener=lambda url: urllib.urlopen(url).read())
                return d(selector)
            else:
                return raw_url(selector)
        except Exception:
            print("Mismatch grammar for parsing!")
            raise Exception
                
    t[0].do = MethodType(do, t[0], Node)      

#----------------------------------------------------#
#               5.3.1.7 Group                        #
#----------------------------------------------------#

def p_expression_group(t):
    'group_expr : LPAREN expression RPAREN'
    
    t[0] = Node("group", t[2], 'group')
    def do(self, id = None):
        try:
            return self.children.do(id)    
        except:
            raise Exception
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#               5.3.1.8 Unary Plus                   #
#----------------------------------------------------#

def p_expression_uplus(t):
    'uplus_expr : PLUS expression %prec UPLUS'
    
    t[0] = Node("uplus", t[2], 'uplus')
    def do(self, id = None):
        try:
            return self.children.do(id)
        except:
            print("There was an error in the unary plus expression")
        
    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#
#              5.3.1.9 Unary Minus                   #
#----------------------------------------------------#

def p_expression_uminus(t):
    'uminus_expr : MINUS expression %prec UMINUS'
    
    t[0] = Node("uminus", t[2], 'uminus')
    def do(self, id = None):
        try:
            return -self.children.do(id)
        except:
            print("There was an error in the unary minus expression")
        
    t[0].do = MethodType(do, t[0], Node) 
    
#--------------------------------------------------------------#
#                   5.3.1 Compound Expressions                 #
#--------------------------------------------------------------#

#----------------------------------------------------#
#            5.3.1.1 Arithemtic Operations           #
#----------------------------------------------------#

def p_expression_arithmetic_op(t):
    '''arithmetic_expr : expression PLUS expression 
                       | expression MINUS expression 
                       | expression MULTIPLY expression 
                       | expression DIVIDE expression
                       | expression POW expression 
                       | expression MOD expression'''
    
    t[0] = Node("arithmetic_op", [t[1], t[3]], t[2])
                    
    if t[2] == '+':
        #t[0] = t[1] + t[3]  # add
        def do(self, id = None):
            try:        
                return self.children[0].do(id) + self.children[1].do(id)
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id))) 
    elif t[2] == '-':
        #t[0] = t[1] - t[3]  # subtract
        
        def do(self, id = None):
            try:
                return self.children[0].do(id) - self.children[1].do(id)        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '*':
        #t[0] = t[1] * t[3]  # multiply
        def do(self, id = None):
            try:
                return self.children[0].do(id) * self.children[1].do(id)        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '/':
        #t[0] = t[1] / t[3]  # divide
        def do(self, id = None):
            try:
                return self.children[0].do(id) / self.children[1].do(id)        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '^': 
        #t[0] = t[1] ** t[3] # power
        def do(self, id = None):
            try:
                return self.children[0].do(id) ** self.children[1].do(id)        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '%': 
        #t[0] = t[1] % t[3]  # remainder
        def do(self, id = None):
            try:
                return self.children[0].do(id) % self.children[1].do(id)        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
                    
    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#

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
                    
    if (t[2] == 'and' or t[2] =='&&'):
        #t[0] = t[1] and t[3]
        def do(self, id = None):
            try:
                return self.children[0].do(id) and self.children[1].do(id)        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif (t[2] == 'or' or t[2] =='||'):
        #t[0] = t[1] or t[3]
        def do(self, id = None):
            try:
                return self.children[0].do(id) or self.children[1].do(id)        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == 'xor':
        #t[0] = (t[1] and not t[3]) or (not t[1] and t[3])
        def do(self, id = None):
            try:
                return (self.children[0].do(id) and not self.children[1].do(id)) or (not self.children[0].do(id) and tself.children[1].do(id))
            except:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '==':
        #t[0] = t[1] == t[3] # equal?
        def do(self, id = None):
            try:
                return self.children[0].do(id) == self.children[1].do(id)
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '!=':
        #t[0] = t[1] != t[3] # not equal?
        def do(self, id = None):
            try:
                return self.children[0].do(id) != self.children[1].do(id)
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '>':
        #t[0] = t[1] > t[3] # greater than?
        def do(self, id = None):
            try:
                return self.children[0].do(id) > self.children[1].do(id)
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '<':
        #t[0] = t[1] < t[3] # less than?
        def do(self, id = None):
            try:
                return self.children[0].do(id) < self.children[1].do(id)                              
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '>=':
        #t[0] = t[1] >= t[3] # greater than or equal?
        def do(self, id = None):
            try:
                return self.children[0].do(id) >= self.children[1].do(id)
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
    elif t[2] == '<=':
        #t[0] = t[1] <= t[3] # less than or equal?
        def do(self, id = None):
            try:
                return self.children[0].do(id) <= self.children[1].do(id)
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do(id)) + " " + self.leaf + " " + str(self.children[1].do(id)))
                    
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
# def p_expression_unistring(t):
#     'expression : ID expression'
    
#     t[0] = Node("unistring", [t[1] , t[2]], 'unistring')
#     def do(self, id = None):
#         try:
#             # u is ID, not node
#             if self.children[0] == 'u':
#                 return self.children[0] + self.children[1].do(id)
#             else:
#                 raise Exception()
#         except LookupError:
#             print("Undefined name '%s'" % self.children[0])
#             raise Exception
#     t[0].do = MethodType(do, t[0], Node)  
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