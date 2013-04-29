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
# File: namespace.py                                                     	  #
# Description: Swim namespace 	                                              #
#-----------------------------------------------------------------------------#

class Namespace:
	'''Namespaces implemented as a stack of hash tables
		add "@namespace.scope" before function definition to automatically
		scope in before the procedure and scope out after'''
	
	level = 0

	def __init__(self, globl = {}, debug=False):
		self.stack = [globl]
		self.debug = debug

	def __str__(self):
		return str(self.stack)

	def __setitem__(self, var, val):
		'assign value to variable in innermost scope'
		self.stack[-1][var] = val

	def __getitem__(self, var):
		'access the variable in innermost scope that it was defined in'
		# try:
		for table in reversed(self.stack):
			if table.has_key(var):
				return table[var]
		raise KeyError
		# except Exception:
		# 	# print("Error: Identifier '%s' is not defined" % var)
		# 	raise Exception

	def __contains__(self, var):
		for table in self.stack:
			if table.has_key(var):
				return True
		return False

	def __delitem__(self, var):
		'delete the innermost instance of the variable'
		for table in reversed(self.stack):
			if table.has_key(var):
				del table[var]

	def getAllItems(self):
		'return all items on current namespace scope'
		return self.stack[-1]

	def scope_in(self):
		'pushes a new namespace on top of the stack'
		self.stack.append({})
		if self.debug:
			self.level += 1
			print "Namespace on start of level " + str(self.level) + ": "+ str(self)

	def scope_out(self):
		'removes the top namespace from the stack'

		if self.debug:
			print "Namespace at end of level " + str(self.level) + ": " + str(self)
			self.level -= 1

		try:
			if len(self.stack) <= 1:
				raise ScopeError('Attempted to drop global scope')
			self.stack.pop()
		except ScopeError as e:
			print e.msg

	def scope(self, func):
		def decorated(*args, **kwargs):
			self.scope_in()
			func(*args, **kwargs)
			self.scope_out()
		return decorated

	def assign_global(self, var, val):
		'assign variable to global scope'
		self.stack[0][var] = val

	def access_global(self, var):
		'access variable to global scope'
		return self.stack[0][var]

class ScopeError(Exception):
	def __init__(self, msg):
		self.msg = 'ScopeError: ' + msg

#-----------------------------------------------------------------------------#