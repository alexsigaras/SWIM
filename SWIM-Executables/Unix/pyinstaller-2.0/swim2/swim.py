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
# File: swim.py                                                               #
# Description: Swim Main File                                                 #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                            1. Library Import                                #
#-----------------------------------------------------------------------------#

import sys, os
import re
import types

sys.path.insert(0,os.path.join("..", "include"))

if sys.version_info[0] >= 3:
    raw_input = input

# Import Lexical Analyzer
from swim_lex import *

# Import Parse Analyzer
from swim_parse import *

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                                 2. Yacc                                     #
#-----------------------------------------------------------------------------#

import ply.yacc as yacc
yacc.yacc(optimize=0, write_tables=0)
mode = 2
if mode == 1:
    s = raw_input("SWIM REPL> ")   
    lex.input(s)
if mode == 3:
    s = 'print("good");/* comment; 1 \n bullshit + - hahaha */'
    #yacc.parse(s)
    lex.input(s)
    while 1:
        tok = lex.token()
        print tok
        if not tok:
            break
else:

    if len(sys.argv) > 1:
        fn = open(sys.argv[1])
        # for line in fn.readlines():
        #     if line == "\n": continue
        #     if mode == 1:
        #         lex.input(line)
        #         while 1:
        #             tok = lex.token()
        #             print tok
        #             if not tok:
        #                 break
        #     else:
        #         yacc.parse(line)
        s = fn.read()
        #s = re.sub(r'\#.*|/\*(.*[^\*/]|\n|\t)*\*/', '', s)
        s = s.replace('\n',' ')
        #print s
        #print s
        yacc.parse(s)
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