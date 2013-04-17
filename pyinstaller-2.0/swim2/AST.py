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
# File: AST.py 		                                                          #
# Description: Abstract Syntax Tree                                           #
#-----------------------------------------------------------------------------#
import types

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
			self.children = 0.0
			
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
		return [self.leaf, childTree]


#     def accept(self, visitor):
#         visitor(self)
#         for field in self.fields:
#             value = getattr(self, field)
#             if isinstance(value, Node):
#                 value.accept(visitor)
#             elif isinstance(value, list):
#                 for item in value:
#                     if isinstance(item, Node):
#                         item.accept(visitor)

# def node(name, fields):
#     attrs = {'fields': fields}
#     return type(name, (Node,), attrs)

# Class = node('Class', ['name', 'type', 'extends', 'implements', 'nodes'])
# Function = node('Function', ['name', 'params', 'nodes', 'is_ref'])
# FunctionCall = node('FunctionCall', ['name', 'params'])
# MagicConstant = node('MagicConstant', ['name', 'value'])
# Namespace = node('Namespace', ['name', 'nodes'])

# def resolve_magic_constants(nodes):
#     current = {}
#     def visitor(node):
#         if isinstance(node, Namespace):
#             current['namespace'] = node.name
#         elif isinstance(node, Class):
#             current['class'] = node.name
#         elif isinstance(node, Function):
#             current['function'] = node.name
#         elif isinstance(node, MagicConstant):
#             if node.name == '__NAMESPACE__':
#                 node.value = current.get('namespace')
#             elif node.name == '__CLASS__':
#                 node.value = current.get('class')
#                 if current.get('namespace'):
#                     node.value = '%s\\%s' % (current.get('namespace'),
#                                              node.value)
#             elif node.name == '__FUNCTION__':
#                 node.value = current.get('function')
#                 if current.get('namespace'):
#                     node.value = '%s\\%s' % (current.get('namespace'),
#                                              node.value)
#                 if current.get('namespace'):
#                     node.value = '%s\\%s' % (current.get('namespace'),
#                                              node.value)
#     for node in nodes:
#         if isinstance(node, Node):
#             node.accept(visitor)
#-----------------------------------------------------------------------------#		