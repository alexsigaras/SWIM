Type check/inference
--------------------

	Type Inference Templates:

	>"We can apply the type-inference templates by making a bottom-up traversal 
	>of the AST. We determine the types of the leaves using information from the 
	>symbol table. We can then move up the tree determining the type of the interior
	>nodes from the types of their children by applying the inference rule for the 
	>operator at a given interior node"

		hash on (operator, n.type, n2.type)
			if keyerror on lookup then type error



Symbol Table:

