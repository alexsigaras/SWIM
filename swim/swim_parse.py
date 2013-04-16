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

#-----------------------------------------------------------------------------#
#                   2. External Library Import                                #
#-----------------------------------------------------------------------------#

# Parsing
from pyquery import PyQuery as pq
import urllib, getpass
import re

# PDF
from fpdf import fpdf as pdf

# Error handling
from swim_exception import *

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                          3.  External Functions                             #
#-----------------------------------------------------------------------------#

def stripe_quotation(string):
    result = string.replace("'","") if string.startswith("'") else string.replace('"', "")
    return result

#-----------------------------------------------------------------------------#

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
	        if result is not None:
	        	print(result)
        except Error as e:
        	#print 1
        	#print e
            print(t[1].traverse())
            pass
        	#print "[Line :" + str(e.lineno) + "] " + e.msg 
    
    # Saving mode for function and class definition
    ''' TO DO '''

#----------------------------------------------------#

#--------------------------------------------------------------#
#                       5.2 Statements                         #
#--------------------------------------------------------------#

def p_statements(t):
    '''statements : statement statements
                  | statement'''
    try:
        t[0] = Node ("statements", [t[1], t[2]], "statements")    

        def do(self):
            self.children[0].do()
            self.children[1].do()

    except:
        t[0] = Node ("statement", t[1], "statement")

        def do(self):
            self.children.do()
    t[0].do = MethodType(do, t[0], Node)

# def p_statement(t):
#     '''statement :

# Single Statement
#                  | statement_expression
#                  | statement_assign
#                  | statement_increment
#                  | statement_decrement
#                  | statement_list
#                  | statement_dictionary

# Compound Statement
#                  | statement_if
#                  | statement_while
#                  | statement_for
#                  | statement_function


#----------------------------------------------------#

def p_statement_expr(t):
    'statement : expression'
    
    t[0] = Node("expr", t[1], 'expr')
    def do(self):
        return self.children.do()
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#                  5.2. Assignment                   #
#----------------------------------------------------#
    
def p_statement_assign(t):
    'statement : ID ASSIGN expression SEMICOLON'
    t[0] = Node("assign", [t[1], t[3]], t[2])
    def do(self):
        ''' Need to check ID !'''       
        identifiers[self.children[0]] = self.children[1].do()
        return identifiers[self.children[0]]
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#

#----------------------------------------------------#
#                5.2. Auto Increment                 #
#----------------------------------------------------# 

def p_statement_increment(t):
    'statement : expression PLUS PLUS SEMICOLON'
    t[0] = Node("increment", t[1], "++")
    def do(self):
        identifiers[self.children.children] = self.children.do() + 1
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#

#----------------------------------------------------#
#                5.2. Auto Decrement                 #
#----------------------------------------------------# 

def p_statement_decrement(t):
    'statement : expression MINUS MINUS SEMICOLON'
    t[0] = Node("decrement", t[1], "--")
    def do(self):
        identifiers[self.children.children] = self.children.do() - 1
    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#

#--------------------------------------------------------------#
#                       5.3 Expressions                        #
#--------------------------------------------------------------#

def p_expression(t):
    '''expression : simple_expr
                  | compound_expr'''
    
    t[0] = Node("expr", t[1], 'expr')
    def do(self):
        return self.children.do()
    t[0].do = MethodType(do, t[0], Node)

def p_simple_expr(t):
    '''simple_expr : boolean_expr
                   | not_expr
                   | number_expr
                   | id_expr
                   | string_expr
                   | list_expr
                   | parse_text_expr
                   | group_expr
                   | uplus_expr
                   | uminus_expr'''

    t[0] = Node("expr", t[1], 'expr')
    def do(self):
        return self.children.do()
    t[0].do = MethodType(do, t[0], Node)

def p_compound_expr(t):
    '''compound_expr : arithmetic_expr
                     | conditional_expr'''
    
    t[0] = Node("expr", t[1], 'expr')
    def do(self):
        return self.children.do()
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
        def do(self):
            try:        
                return self.children[0].do() + self.children[1].do()
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do())) 
    elif t[2] == '-':
        #t[0] = t[1] - t[3]  # subtract
        
        def do(self):
            try:
                return self.children[0].do() - self.children[1].do()        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '*':
        #t[0] = t[1] * t[3]  # multiply
        def do(self):
            try:
                return self.children[0].do() * self.children[1].do()        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '/':
        #t[0] = t[1] / t[3]  # divide
        def do(self):
            try:
                return self.children[0].do() / self.children[1].do()        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '^': 
        #t[0] = t[1] ** t[3] # power
        def do(self):
            try:
                return self.children[0].do() ** self.children[1].do()        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '%': 
        #t[0] = t[1] % t[3]  # remainder
        def do(self):
            try:
                return self.children[0].do() % self.children[1].do()        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
                    
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

    t[0] = Node("conditional_op", [t[1], t[3]], t[2])
                    
    if (t[2] == 'and' or t[2] =='&&'):
        #t[0] = t[1] and t[3]
        def do(self):
            try:
                return self.children[0].do() and self.children[1].do()        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif (t[2] == 'or' or t[2] =='||'):
        #t[0] = t[1] or t[3]
        def do(self):
            try:
                return self.children[0].do() or self.children[1].do()        
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == 'xor':
        #t[0] = (t[1] and not t[3]) or (not t[1] and t[3])
        def do(self):
            try:
                return (self.children[0].do() and not self.children[1].do()) or (not self.children[0].do() and tself.children[1].do())
            except:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '==':
        #t[0] = t[1] == t[3] # equal?
        def do(self):
            try:
                return self.children[0].do() == self.children[1].do()
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '!=':
        #t[0] = t[1] != t[3] # not equal?
        def do(self):
            try:
                return self.children[0].do() != self.children[1].do()
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '>':
        #t[0] = t[1] > t[3] # greater than?
        def do(self):
            try:
                return self.children[0].do() > self.children[1].do()
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '<':
        #t[0] = t[1] < t[3] # less than?
        def do(self):
            try:
                return self.children[0].do() < self.children[1].do()                              
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '>=':
        #t[0] = t[1] >= t[3] # greater than or equal?
        def do(self):
            try:
                return self.children[0].do() >= self.children[1].do()
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
    elif t[2] == '<=':
        #t[0] = t[1] <= t[3] # less than or equal?
        def do(self):
            try:
                return self.children[0].do() <= self.children[1].do()
            except TypeError:
                raise TypeException(t.lexer.lineno, str(self.children[0].do()) + " " + self.leaf + " " + str(self.children[1].do()))
                    
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#--------------------------------------------------------------#
          
def p_expression_not_op(t):
    '''not_expr : NOT expression'''
    
    t[0] = Node("logop", t[2], t[1])
    def do(self):
        return not self.children.do()
        
    t[0].do = MethodType(do, t[0], Node)    
    
def p_expression_boolean(t):
    '''boolean_expr : TRUE
                    | FALSE'''
                  
    t[0] = Node("boolean", t[1], 'boolean')
    
    if t[1] == "True":
        def do(self):
            return True
    elif t[1] == "False":
        def do(self):
            return False
    t[0].do = MethodType(do, t[0], Node)
                        
def p_expression_uminus(t):
    'uminus_expr : MINUS expression %prec UMINUS'
    
    t[0] = Node("uminus", t[2], 'uminus')
    def do(self):
        try:
            return -self.children.do()
        except:
            raise Exception
        
    t[0].do = MethodType(do, t[0], Node) 

def p_expression_uplus(t):
    'uplus_expr : PLUS expression %prec UPLUS'
    
    t[0] = Node("uplus", t[2], 'uplus')
    def do(self):
        try:
            return self.children.do()
        except:
            raise Exception
        
    t[0].do = MethodType(do, t[0], Node) 

def p_expression_group(t):
    'group_expr : LPAREN expression RPAREN'
    
    t[0] = Node("group", t[2], 'group')
    def do(self):
        return self.children.do()    
        
    t[0].do = MethodType(do, t[0], Node)    

def p_expression_parse_text(t):
    'parse_text_expr : SELECTOR LPAREN elements RPAREN'
    
    t[0] = Node("selector", t[3], t[1])
    def do(self):
        try:
            raw_selector = self.children.do()[0]
            selector = stripe_quotation(raw_selector)
            raw_url = self.children.do()[1]

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

def p_expression_list(t):
    'list_expr : LSBRACKET elements RSBRACKET'

    t[0] = Node("list", t[2], "list")

    def do(self):
        return list( self.children.do() )
    t[0].do = MethodType(do, t[0], Node)
        
def p_expression_number(t):
    'number_expr : NUMBER'

    t[0] = Node("number", t[1], 'number')
    def do(self):
        return self.children
    t[0].do = MethodType(do, t[0], Node) 

def p_expression_name(t):
    'id_expr : ID'
    
    t[0] = Node("name", str(t[1]), 'name')
    def do(self):
        try:
            return identifiers[self.children]
        except LookupError:
            print(str(t.lexer.lineno) + ":\nexpression could not be recognized as stored value.\n")
            raise NameException(t.lexer.lineno, str(self.children))
    t[0].do = MethodType(do, t[0], Node)     
    
def p_expression_string(t):
    '''string_expr : STRING1
                  | STRING2''' 
    t[0] = Node("string", stripe_quotation(t[1]), 'string')
    def do(self):
        return self.children
    t[0].do = MethodType(do, t[0], Node)

#-----------------------------------------------------#


#---------------------------------------------------------#


# def p_expression_unistring(t):
#     'expression : ID expression'
    
#     t[0] = Node("unistring", [t[1] , t[2]], 'unistring')
#     def do(self):
#         try:
#             # u is ID, not node
#             if self.children[0] == 'u':
#                 return self.children[0] + self.children[1].do()
#             else:
#                 raise Exception()
#         except LookupError:
#             print("Undefined name '%s'" % self.children[0])
#             raise Exception
            
#     t[0].do = MethodType(do, t[0], Node)  

#--------------------------------------------------------------#

#----------------------------------------------------#
#               5.4  If Statement                    #
#----------------------------------------------------#

def p_statement_if(t):
    'statement : IF expression DO statements elif_blocks END'

    t[0] = Node ("if", [t[2],t[4],t[5]])

    def do(self):
        if self.children[0].do():
            return self.children[1].do()
        else:
            return self.children[2].do()

    t[0].do = MethodType(do, t[0], Node)

def p_statement_elif_blocks(t):
    '''elif_blocks : elif_block elif_blocks
                   | else_block 
                   | '''
    try:     
        t[0] = Node ("elifs", [t[1], t[2]], "elifs")

        def do(self):
            if self.children[0].do():
                return self.children[0].do()
            else:
                return self.children[1].do()

    except:
        try:
            t[0] = Node ("else", t[1], "else")

            def do(self):
                return self.children.do()
        except:
            t[0] = Node ("else", None, "else")
            def do(self):
                return None
    t[0].do = MethodType(do, t[0], Node)                   

def p_statement_elif_block(t):
    'elif_block : ELIF expression DO statements'

    t[0] = Node ("elif", [t[2], t[4]])

    def do(self):
        if self.children[0].do():
            return self.children[1].do
        else:
            return False
    
    t[0].do = MethodType(do, t[0], Node)

def p_statement_else_block(t):
    'else_block : ELSE statements'

    t[0] = Node ("else", t[2])

    def do(self):
        return self.children.do()

    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
    
#----------------------------------------------------#
#                 5.5 While Statement                #
#----------------------------------------------------#

def p_statement_while(t):
    'statement : WHILE expression DO statements END'

    t[0] = Node("while", [t[2],t[4],t[1]])

    def do(self):
        while self.children[0].do(): 
            self.children[1].do()
            self.do()
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#

#----------------------------------------------------#
#                 5.6 For Statement                  #
#----------------------------------------------------#

def p_statement_for(t):
    'statement : FOR EACH ID IN element DO statements END'
    t[0] = Node("for", [t[3], t[5], t[7]] , "for")
    def do(self):
        for temp in self.children[1].do():
            identifiers[self.children[0]] = temp
            self.children[2].do()
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#

#----------------------------------------------------#
#                  5.7 List                          #
#----------------------------------------------------#

def p_list(t):
    'statement : ID ASSIGN LSBRACKET elements RSBRACKET SEMICOLON'

    t[0] = Node("list", [t[1],t[4]], "elements")
    def do(self):
        ''' Need to check ID !'''       
        identifiers[self.children[0]] = self.children[1].do()
        return identifiers[self.children[0]]
    t[0].do = MethodType(do, t[0], Node)

def p_elements(t):
    '''elements : element COMMA elements
                | element'''
    try:
        t[0] = Node ("elements", [t[1], t[3]], "elements")    

        def do(self):
            return list([self.children[0].do()] + self.children[1].do())

    except:
        t[0] = Node ("element", t[1], "element")

        def do(self):
            return [self.children.do()]
    t[0].do = MethodType(do, t[0], Node)

def p_element(t):
    '''element : expression'''
    
    t[0] = Node("expr", t[1], 'expr')
    def do(self):
        return self.children.do()
    t[0].do = MethodType(do, t[0], Node) 

#----------------------------------------------------#
#----------------------------------------------------#
#                  5.8 Dictionary                    #
#----------------------------------------------------#

def p_dictionary(t):
    '''statement : ID ASSIGN LCBRACKET dictionary_objects RCBRACKET SEMICOLON'''
    t[0] = Node("dictionary", [t[1],t[4]], "dictionary")
    def do(self):
        ''' Need to check ID !'''       
        identifiers[self.children[0]] = self.children[1].do()
        return identifiers[self.children[0]]
    t[0].do = MethodType(do, t[0], Node)


def p_dictionary_objects(t):
    '''dictionary_objects : dictionary_object COMMA dictionary_objects
                          | dictionary_object'''
    try:
        t[0] = Node ("dictionary_objects", [t[1], t[3]], "dictionary_objects")

        def do(self):
            temp  = self.children[0].do()
            temp.update(self.children[1].do())
            return temp

    except:
        t[0] = Node ("dictionary_object", t[1], "dictionary_object")
        def do(self):
            return self.children.do()
    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_object(t):
    'dictionary_object : key COLON value'
    t[0] = Node("dictionary_object", [t[1], t[3]], "dictionary_object")
    def do(self):
        return {self.children[0].do() : self.children[1].do()}
    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_key(t):
    '''key : STRING1
           | STRING2'''
    t[0] = Node("key", stripe_quotation(t[1]), 'key')
    def do(self):
        return self.children
    t[0].do = MethodType(do, t[0], Node)

def p_dictionary_value(t):
    'value : expression'
    t[0] = Node("value", t[1], 'value')
    def do(self):
        return self.children.do()
    t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#

#----------------------------------------------------#
#                  5.9 Functions                     #
#----------------------------------------------------#

def p_function(t):
    '''statement : ID LPAREN statement RPAREN SEMICOLON'''
    t[0] = Node("function", t[3], t[1])

    def do(self):   
        result = self.children.do() 
        if self.leaf == "print" :
            if isinstance(result, StringType):
                # Escaped sequence handling
                escaped_sequences = (r"\newline", r"\\", r"\'", r'\"', r"\a", r"\b", r"\f", r"\n", r"\r", r"\t", r"\v")
                
                for seq in escaped_sequences:
                    if result.find(seq) != -1:      
                        result = result.decode('string-escape')
                    
                # string containing ""              
                # 2 byte unicode with unicode characters
                if re.match(r'u"\\u', result):
                    result = unichr(int(result[4:8], 16))
                # 2 byte unicode with strings
                elif re.match(r'^u"', result):
                    result =  result.replace('"','')[1:].decode("utf-8")
                    
                # string containing ''          
                elif re.match(r"u'\\u", result):
                    result = unichr(int(result[4:8], 16))
                # 2 byte unicode with strings
                elif re.match(r"^u'", result):
                    result = result.replace("'",'')[1:].decode("utf-8")         
                else:
                    result = result.replace("'",'')            

                print result       
            else:
                print result        
     
        elif self.leaf == "pdf":
            try:
                #print stripe_quotation(t[3][0])
                f = pdf.FPDF()
                f.add_page()
                f.set_font('Arial','B',16)          
                f.multi_cell(w=200,h=5,txt = stripe_quotation(self.children.do()[0])) 
                
                # for our user test
                filename = stripe_quotation(self.children.do()[1])
                filename = filename.split('.')[0] + '_' + getpass.getuser() + '.' + filename.split('.')[1]
                
                f.output(os.path.join("..","doc",filename),'F')
            except:
                print("Mismatch grammar for pdf output!")
                raise Exception     
        
    t[0].do = MethodType(do, t[0], Node)     

#----------------------------------------------------#

# def p_param_statement(t):
#     'param_statement : ID ASSIGN expression'
#     t[0] = Node("param_statement", [t[1], t[3]], t[2])
#     def do(self):
#         ''' Need to check ID !'''       
#         identifiers[self.children[0]] = self.children[1].do()
#         return identifiers[self.children[0]]
#     t[0].do = MethodType(do, t[0], Node)

#----------------------------------------------------#
#                    5.10 Error                      #
#----------------------------------------------------#

def p_error(t):
    if t:
        print("Syntax error at '%s'" % t.value)
    else:
        print("Syntax error at EOF")

#----------------------------------------------------#

#-----------------------------------------------------------------------------#