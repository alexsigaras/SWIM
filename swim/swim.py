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
from lex import *

# Import Parse Analyzer
from parse import *

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                                 2. Yacc                                     #
#-----------------------------------------------------------------------------#

import ply.yacc as yacc

def main(file=None, mode=2):

    yacc.yacc(optimize=0, write_tables=0)
    
    if file:
        yacc.yacc(debug=0, errorlog=yacc.NullLogger())
        f = open(file)
        s = f.read().replace('\n',' ')
        yacc.parse(s)
        f.close()
    else:

        if mode == 1:
            s = raw_input("SWIM REPL> ")   
            lex.input(s)
        if mode == 3:
            s = 'print("good");/* comment; 1 \n + - hahaha */'
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
                s = fn.read()
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

if __name__ == "__main__":
    main()
    
#-----------------------------------------------------------------------------#