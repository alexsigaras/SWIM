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

import sys, os
import re
import types
from types import MethodType

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
#                             External Functions                              #
#-----------------------------------------------------------------------------#
def stripe_quotation(string):
	result = string.replace("'","") if string.startswith("'") else string.replace('"', "")
	return result
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                               Declare tokens                                #
#-----------------------------------------------------------------------------#

reserved = {
	'if'       : 'IF',
	'else'     : 'ELSE',
	'do'       : 'DO',
	'True'     : 'TRUE',
	'False'    : 'FALSE',
	'while'    : 'WHILE',
	'for'      : 'FOR',
	'foreach'  : 'FOREACH',
	'and'      : 'AND',
	'or'       : 'OR',
	'xor'      : 'XOR',
	'not'      : 'NOT',
}

tokens = [
    'STRING1', 'STRING2', 'SELECTOR', 'ID','NUMBER', 'AND', 'OR', 'XOR', 'NOT', 'COMMA',
    'PLUS','MINUS','MULTIPLY','DIVIDE','ASSIGN', 'EQUALS','POW','MOD',
    'LPAREN','RPAREN'
    ] + list(reserved.values())

# Tokens

# Operator Tokens

t_AND     = r'&&'
t_OR      = r'\|\|'
t_NOT     = r'!'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULTIPLY   = r'\*'
t_DIVIDE  = r'/'
t_ASSIGN  = r'='
t_EQUALS  = r'=='
t_POW     = r'\^'
t_MOD     = r'\%'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'


# Keywords
'''
t_WHILE   = r'while'
t_FOR     = r'for'
t_FOREACH = r'foreach'
'''

t_STRING1 = r'u?"\\?[^"]*"'
t_STRING2 = r"u?'\\?[^']*'"
t_SELECTOR = r'@'
t_COMMA   = r','

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


t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
#                                    Lex                                      #
#-----------------------------------------------------------------------------#
    
import ply.lex as lex
lex.lex(optimize=1)

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                               Parsing Rules                                 #
#-----------------------------------------------------------------------------#

precedence = (
    ('left','PLUS','MINUS', 'COMMA'),
    ('left','MULTIPLY','DIVIDE', 'MOD'),
    ('right', 'POW'),
    )

# dictionary of names
names = { } 

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                            Abstract Syntax Tree                             #
#-----------------------------------------------------------------------------#
class Node:
	'Simple Node'
	
	def __init__(self, type, children = None, leaf = None):
		'''	Atttribute is composed of type, children, and leaf. 
			
		 	1) a + b              => type : binop     ,  leaf : +         ,  children = [node a, node b]    (Here, if a is number, node a is 5) form. If string, 6))
			2) if s do e1 else e2 => type : ifelse    ,  leaf : if        ,  children = [node s, node e1, node e2]
			3) a = 2              => type : assign    ,  leaf : =         ,  children = [node a, node 2]
			4) print(e)           => type : function  ,  leaf : print     ,  children = node e
			5) 1                  => type : number    ,  leaf : number    ,  children = node 1
			6) a                  => type : name      ,  leaf : name      ,  children = node a
			
			* Note that leaf should be string and children can be list or string according to whether it is the last tree or not. You should make
			take care of children is list or not to make "do" method.
		'''
		
		self.type = type
		
		# make children list or object
		if children:
			self.children = children
		else:
			self.children = []
			
		self.leaf = leaf
	
	# This method is called when we type just object on console. For test
	def __str__(self):
		return str([self.leaf, self.children])
		
	# To test the node tree. If you want to see node tree structure, make showNodeTree True
	def traverse(self):
		childTree = []
		if isinstance(self.children, types.ListType):
			for child in self.children:
				if child.__doc__ == "Simple Node":
					childTree.append(child.traverse())
				else:
					childTree.append(child)
		else:
			if self.children.__doc__ == "Simple Node":
				childTree = self.children.traverse()
			else:
				childTree = self.children
		#return str([self.type, self.leaf, childTree])
		return [self.leaf, childTree]		
		#print str([self.type, self.leaf]
	
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                                    Grammar                                  #
#-----------------------------------------------------------------------------#	
def p_start(t):
    '''start : statement'''
    
    # Normal mode
    showNodeTree = False
    if(showNodeTree):
    	print(t[1].traverse())
    else:
	    result = t[1].do()
	    if result is not None:
    		print(result)
    
    # Saving mode for function and class definition
    ''' TO DO '''
   
def p_function(t):
    '''expression : ID LPAREN expression RPAREN'''
    t[0] = Node("function", t[3], t[1])

    def do(self):   
	    result = self.children.do() 
	    if self.leaf == "print" :
	    	
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

	        return result	            
     
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
    
def p_statement_assign(t):
    'statement : ID ASSIGN expression'
    
    t[0] = Node("assign", [t[1], t[3]], t[2])
    def do(self):
	    ''' Need to check ID !'''	    
	    names[self.children[0]] = self.children[1].do()
    t[0].do = MethodType(do, t[0], Node) 
    

def p_statement_if_else(t):
    'statement : IF expression DO expression ELSE expression'
    
    t[0] = Node("ifelse", [t[2], t[4], t[6]], t[1])

    def do(self):
    	if self.children[0].do():
    		return self.children[1].do()
    	else:
    		return self.children[2].do()
    		
    t[0].do = MethodType(do, t[0], Node)  
       
def p_statement_expr(t):
    'statement : expression'
    
    t[0] = Node("expr", t[1], 'expr')
    def do(self):
	    return self.children.do()
    t[0].do = MethodType(do, t[0], Node) 
    
    #print t[1]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression POW expression
                  | expression MOD expression
                  | expression AND expression
                  | expression OR expression
                  | expression XOR expression
                  | expression EQUALS expression'''
    
    t[0] = Node("binop", [t[1], t[3]], t[2])
                    
    if t[2] == '+':
        #t[0] = t[1] + t[3]  # add
        def do(self):
        	return self.children[0].do() + self.children[1].do()
    elif t[2] == '-':
        #t[0] = t[1] - t[3]  # subtract
        def do(self):
        	return self.children[0].do() - self.children[1].do()        
    elif t[2] == '*':
        #t[0] = t[1] * t[3]  # multiply
        def do(self):
        	return self.children[0].do() * self.children[1].do()        
    elif t[2] == '/':
        #t[0] = t[1] / t[3]  # divide
        def do(self):
        	return self.children[0].do() / self.children[1].do()        
    elif t[2] == '^': 
        #t[0] = t[1] ** t[3] # power
        def do(self):
        	return self.children[0].do() ** self.children[1].do()        
    elif t[2] == '%': 
        #t[0] = t[1] % t[3]  # remainder3
        def do(self):
        	return self.children[0].do() % self.children[1].do()        
    elif (t[2] == 'and' or t[2] =='&&'):
        #t[0] = t[1] and t[3]
        def do(self):
        	return self.children[0].do() and self.children[1].do()        
    elif (t[2] == 'or' or t[2] =='||'):
        #t[0] = t[1] or t[3]
        def do(self):
        	return self.children[0].do() or self.children[1].do()        
    elif t[2] == 'xor':
        #t[0] = (t[1] and not t[3]) or (not t[1] and t[3])
        def do(self):
        	return (self.children[0].do() and not self.children[1].do()) or (not self.children[0].do() and tself.children[1].do())
    elif t[2] == '==':
        #t[0] = t[1] == t[3] # equal?
        def do(self):
        	return self.children[0].do() == self.children[1].do()           	
    
    t[0].do = MethodType(do, t[0], Node) 
          
def p_expression_notop(t):
	'''expression : NOT expression'''
	
	t[0] = Node("logop", t[2], t[1])
	def do(self):
		return not self.children.do()
    	
	t[0].do = MethodType(do, t[0], Node)  	
	
def p_expression_boolean(t):
    '''expression :	TRUE
				  |	FALSE'''
				  
    t[0] = Node("boolean", t[1], 'boolean')
    
    if t[1] == "True":
    	def do(self):
	    	return True
    elif t[1] == "False":
		def do(self):
			return False
    t[0].do = MethodType(do, t[0], Node)
			  		    
def p_expression_uminus(t):
    'expression : MINUS expression'
    
    t[0] = Node("uminus", t[2], 'uminus')
    def do(self):
    	try:
    		return -self.children.do()
    	except:
    		raise Exception
    	
    t[0].do = MethodType(do, t[0], Node) 

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    
    t[0] = Node("group", t[2], 'group')
    def do(self):
    	return self.children.do()    
    	
    t[0].do = MethodType(do, t[0], Node)  
        
def p_expression_parameters(t):
	'expression : expression COMMA expression'	
	
	# Stacking the parameters to the right as list
	t[0] = Node("comma", [t[1], t[3]], 'comma')
	def do(self):
		return [self.children[0].do(), self.children[1].do()]    
    	
	t[0].do = MethodType(do, t[0], Node)  	

def p_expression_parse_text(t):
	'expression : SELECTOR LPAREN expression RPAREN'
	
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
    	
def p_expression_number(t):
    'expression : NUMBER'

    t[0] = Node("number", t[1], 'number')
    def do(self):
	    return self.children
    t[0].do = MethodType(do, t[0], Node) 

def p_expression_name(t):
    'expression : ID'
    
    t[0] = Node("name", str(t[1]), 'name')
    def do(self):
	    try:
	        return names[self.children]
	    except LookupError:
	        print("Undefined name '%s'" % self.children)
	        raise Exception	     

    t[0].do = MethodType(do, t[0], Node)     
    
def p_expression_string(t):
    '''expression : STRING1
    		  	  | STRING2''' 
    t[0] = Node("string", t[1], 'string')
    def do(self):
	    return self.children
    t[0].do = MethodType(do, t[0], Node)     

def p_expression_unistring(t):
    'expression : ID expression'
    
    t[0] = Node("unistring", [t[1] , t[2]], 'unistring')
    def do(self):
	    try:
	    	# u is ID, not node
	    	if self.children[0] == 'u':
	    		return self.children[0] + self.children[1].do()
	    	else:
		    	raise Exception()
	    except LookupError:
	        print("Undefined name '%s'" % self.children[0])
	        raise Exception
	        
    t[0].do = MethodType(do, t[0], Node)        
    
def p_error(t):
    if t:
        print("Syntax error at '%s'" % t.value)
    else:
        print("Syntax error at EOF")

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                                    Yacc                                     #
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
	
