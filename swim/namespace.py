class Namespace:
	'''Namespaces implemented as a stack of hash tables
		use push() on entrance into new scope
		use pop() on exit out of the scope'''
	

	def __init__(self, globl = {}):
		self.stack = [globl]

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

	def push(self):
		'pushes a new namespace on top of the stack'
		self.stack.append({})

	def pop(self):
		'removes the top namespace from the stack'
		try:
			self.stack.pop()
		except IndexError:
			print "stack is empty, no namespace to pop" 

	def assign_global(self, var, val):
		'assign variable to global scope'
		self.stack[0][var] = val