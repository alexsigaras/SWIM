import re
s = '''websites = ["http://www.cs.columbia.edu/~aho", "http://www.cs.columbia.edu/"]; #single comment
tags = ["h1", "h4"]; 
/* ads
fa
dsf */
for each website in websites do
// iterative loop
	for each tag in tags do
	// iterative loop
c = a + b;
print(c);

 /* ads
fa
dsf */

 seungwoo'''
print "here0"
s = re.sub(r'\#.*|/\*(.*[^\*/]|\n|\t)*\*/', '', s)
print s