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
# File: exception.py                                                     	  #
# Description: Swim Exception Handling                                        #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#                          1. Exception Handling                              #
#-----------------------------------------------------------------------------#

class Error(Exception):
	'''Basic exception class'''
	def __init__(self, lineno, msg):
		self.lineno = lineno
		self.msg = msg 

	def __str__(self):
		return "[Line :" + str(self.lineno) + "] " + self.msg 
	
	def addMsg(self, newMsg):
		self.msg += newMsg

class TypeException(Error):
	''' Unsupported value type'''
	def __init__(self, lineno, msg):
		self.msg = "Unsupported value type in expression, " + msg
		self.lineno = lineno
			

class NameException(Error):
	''' Undefined name'''
	def __init__(self, lineno, msg):
		self.msg = "Undefined name is used in expression, " + msg
		self.lineno = lineno
	
class BooleanException(Error):
	''' Boolean Problem'''
	def __init__(self, lineno, msg):
		self.msg = "Boolean is needed in expression, " + msg
		self.lineno = lineno

#-----------------------------------------------------------------------------#