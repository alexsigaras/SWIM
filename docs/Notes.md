# Semantic Analysis

AST + Symbol Table -> semantic consistency/errors, type information

>Type checking is an important part of semantic analysis. During type checking the compiler checks that each operator has compatible operands.

>Uses made of semantic information for a variable x:

>What kind of value is stored in x?

>How big is x?

>Who is responsible for allocating space for x?

>Who is responsible for initializing x?

>How long must the value of x be kept?

>If x is a procedure, what kinds of arguments does it take and what kind of return value does it have?

>Storage layout for local names

Type system/check/inference
--------------------
### equivalence
+ name
+ structural

### compatibility
+ type checker must check for type compatibility

### inference


1. Type Inference Templates:

>We can apply the type-inference templates by making a bottom-up traversal 
>of the AST. We determine the types of the leaves using information from the 
>symbol table. We can then move up the tree determining the type of the interior
>nodes from the types of their children by applying the inference rule for the 
>operator at a given interior node

```template == hash on (operator, n.type, n2.type)
	if keyerror on lookup then type error```

2. Symbol Table:

Procedures:
-----------

+ choice of parameter-passing mechanism
+ storage allocation for local variables: static or dynamic
+ can procedure declarations nest
+ can procedures be passed as parameters, returned as values
+ can procedure names be overloaded
+ generic procedures, ones whose computations can be done on different types
+ does language have closures (encapsulations of procedures with their runtime context)

1. Parameter-Passing Mechanisms

+ call by value
+ call by reference

2. Evaluation Strategies for the Arguments of a Procedure

+ applicative-order evaluation
+ normal-order evaluation