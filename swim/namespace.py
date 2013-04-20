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
		for table in reversed(self.stack):
			if table.has_key(var):
				return table[var]
		raise KeyError

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


class ScopeError(Exception):
	def __init__(self, msg):
		self.msg = 'ScopeError: ' + msg