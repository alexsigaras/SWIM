class Namespace:
	'''Namespaces implemented as a stack of hash tables
		use push() on entrance into new scope
			pop() on exit out of the scope'''
	
	stack = [{}] 

	def __init__(self):
		pass

	def __str__(self):
		return str(self.stack)

	def push(self):
		'pushes a new namespace on top of the stack'
		self.stack.append({})

	def pop(self):
		'removes the top namespace from the stack'
		try:
			self.stack.pop()
		except IndexError:
			print "stack is empty, no namespace to pop"

	def assign(self, var, val):
		'assign val to var in innermost scope'
		self.stack[-1][var] = val

	def access(self, var):
		'access the variable from the innermost scope'
		for table in reversed(self.stack):
			if table.has_key(var):
				return table[var]
		raise KeyError

	def assign_global(self, var, val):
		'assign variable to global scope'
		self.stack[0][var] = val

	def delete(self, var):
		'delete the innermost instance of the variable'
		for table in reversed(self.stack):
			if table.has_key(var):
				del table[var]
