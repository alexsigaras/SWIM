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
from pyquery import PyQuery as pq
import urllib, getpass
import re

# PDF
from fpdf import fpdf as pdf

# Error handling
from swim_exception import *





#-----------------------------------------------------------------------------#
#                          3.  External Functions                             #
#-----------------------------------------------------------------------------#

def stripe_quotation(string):
    result = string.replace("'","") if string.startswith("'") else string.replace('"', "")
    return result

#-----------------------------------------------------------------------------#
#                          4.  Built-in Functions                             #
#-----------------------------------------------------------------------------#
def builtin_print(result, color=None):
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

        if color is None:
            print result
        else:    
            print "\033[" + color + "m" + result + "\033[0m"     
    else:
        if color is None:
            print result
        else:
            print "\033[" + color + "m" + str(result) + "\033[0m"


def builtin_pdf(expr):
    try:
        #print stripe_quotation(t[3][0])
        f = pdf.FPDF()
        f.add_page()
        f.set_font('Arial','B',16)          
        f.multi_cell(w=200,h=5,txt = stripe_quotation(expr[0])) 
        
        # for our user test
        filename = stripe_quotation(self.children.do()[1])
        filename = filename.split('.')[0] + '_' + getpass.getuser() + '.' + filename.split('.')[1]
        
        f.output(os.path.join("..","doc",filename),'F')
    except:
        print("Mismatch grammar for pdf output!")
        raise Exception    

def builtin_abs(number):
    try:
        return abs(number)
    except:
        print("Mismatch grammar for abs")
        raise Exception

         		
# def p_function(t):
#     '''function_stmt : ID LPAREN statement RPAREN SEMICOLON'''
#     t[0] = Node("function", t[3], t[1])

#     def do(self):   
#         result = self.children.do() 
#         if self.leaf == "print" :
#             if isinstance(result, StringType):
#                 # Escaped sequence handling
#                 escaped_sequences = (r"\newline", r"\\", r"\'", r'\"', r"\a", r"\b", r"\f", r"\n", r"\r", r"\t", r"\v")
                
#                 for seq in escaped_sequences:
#                     if result.find(seq) != -1:      
#                         result = result.decode('string-escape')
                    
#                 # string containing ""              
#                 # 2 byte unicode with unicode characters
#                 if re.match(r'u"\\u', result):
#                     result = unichr(int(result[4:8], 16))
#                 # 2 byte unicode with strings
#                 elif re.match(r'^u"', result):
#                     result =  result.replace('"','')[1:].decode("utf-8")
                    
#                 # string containing ''          
#                 elif re.match(r"u'\\u", result):
#                     result = unichr(int(result[4:8], 16))
#                 # 2 byte unicode with strings
#                 elif re.match(r"^u'", result):
#                     result = result.replace("'",'')[1:].decode("utf-8")         
#                 else:
#                     result = result.replace("'",'')            

#                 print result       
#             else:
#                 print result        
     
#         elif self.leaf == "pdf":
#             try:
#                 #print stripe_quotation(t[3][0])
#                 f = pdf.FPDF()
#                 f.add_page()
#                 f.set_font('Arial','B',16)          
#                 f.multi_cell(w=200,h=5,txt = stripe_quotation(self.children.do()[0])) 
                
#                 # for our user test
#                 filename = stripe_quotation(self.children.do()[1])
#                 filename = filename.split('.')[0] + '_' + getpass.getuser() + '.' + filename.split('.')[1]
                
#                 f.output(os.path.join("..","doc",filename),'F')
#             except:
#                 print("Mismatch grammar for pdf output!")
#                 raise Exception     
        
#     t[0].do = MethodType(do, t[0], Node)     




