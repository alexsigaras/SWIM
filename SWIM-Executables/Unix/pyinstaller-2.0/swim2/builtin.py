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
# File: builtin.py                                                            #
# Description: Swim Built in libraries                                        #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                     1. Common Library Import                                #
#-----------------------------------------------------------------------------#

# Abstract Syntax Tree
from AST import Node

from namespace import Namespace
from types import *

#-----------------------------------------------------------------------------#
#                   2. External Library Import                                #
#-----------------------------------------------------------------------------#

# Parsing
from pyquery import PyQuery as pq
import urllib, getpass
import re
import math

# PDF
from fpdf import fpdf as pdf

# Error handling
from exception import *

#-----------------------------------------------------------------------------#
#                          3.  External Functions                             #
#-----------------------------------------------------------------------------#

def stripe_quotation(string):
    result = string.replace("'","") if string.startswith("'") else string.replace('"', "")
    return result

#-----------------------------------------------------------------------------#
#                          4.  Built-in Functions                             #
#-----------------------------------------------------------------------------#

#----------------------------------------------------#
#           4.1  Mathematical Functions              #
#----------------------------------------------------#

def builtin_abs(number):
    try:
        return abs(number)
    except:
        print("Mismatch grammar for abs")
        raise Exception

def builtin_sin(number):
    try:
        return math.sin(math.pi*number/180)
    except:
        print("Mismatch grammar for sin")
        raise Exception

def builtin_cos(number):
    try:
        return math.cos(math.pi*number/180)
    except:
        print("Mismatch grammar for cos")
        raise Exception

def builtin_tan(number):
    try:
        return math.tan(math.pi*number/180)
    except:
        print("Mismatch grammar for tan")
        raise Exception

def builtin_sqrt(number):
    try:
        return math.sqrt(number)
    except:
        print("Mismatch grammar for sqrt")
        raise Exception
def builtin_log(number):
    try:
        return math.log10(number)
    except:
        print("Mismatch grammar for log10")
        raise Exception
def builtin_factorial(number):
    try:
        return math.factorial(number)
    except:
        print("Mismatch grammar for factorial")
        raise Exception

#----------------------------------------------------#
#            4.2  Print Function                     #
#----------------------------------------------------#

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

#----------------------------------------------------#
#             4.2  PDF Function                      #
#----------------------------------------------------#

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

#----------------------------------------------------#
#             4.3  String Functions                  #
#----------------------------------------------------#

def builtin_lowercase(string):
    try:
        return string.lower()
    except Exception, e:
        print ("Mismatch grammar for lowercase")
        raise Exception

def builtin_uppercase(string):
    try:
        return string.upper()
    except Exception, e:
        print ("Mismatch grammar for uppercase")
        raise Exception

def builtin_length(string):
    try:
        return len(string)
    except Exception, e:
        print ("Mismatch grammar for length")
        raise Exception

def builtin_split(string, string1):
    try:
        return string.split(string1)
    except Exception, e:
        print ("Mismatch grammar for split")
        raise Exception

def builtin_replace(string, string1, string2):
    try:
        return string.replace(string1,string2)
    except Exception, e:
        print ("Mismatch grammar for replace")
        raise Exception

def builtin_contains(string, string1):
    try:
        return string1 in string
    except Exception, e:
        print ("Mismatch grammar for contains")
        raise Exception

def builtin_startswith(string, string1):
    try:
        return string.startswith(string1)
    except Exception, e:
        print ("Mismatch grammar for starts with")
        raise Exception

def builtin_endswith(string, string1):
    try:
        return string.endswith(string1)
    except Exception, e:
        print ("Mismatch grammar for ends with")
        raise Exception
def builtin_matches(string, string1):
    try:
        return bool(re.match(string1, string))
    except Exception, e:
        print ("Mismatch grammar for ends with")
        raise Exception

def builtin_ToString(obj):
    try:
        return str(obj)
    except Exception, e:
        print ("Mismatch grammar for ToString")
        raise Exception

#-----------------------------------------------------------------------------#