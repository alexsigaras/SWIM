import sys, os
currentVersion = sys.version_info[1]
#cmd = 'sudo port install py2' + str(currentVersion) + "-lxml"
cmd = '''
	sudo easy_install pip
	STATIC_DEPS=true sudo pip install lxml
	'''
	
if not os.system(cmd):	
	if os.path.exists("/Library/Python/2.6/site-packages/lxml"):
		print "Copy from python2.6 packages into include\n"
		cmd = '''
		sudo cp -r /Library/Python/2.6/site-packages/lxml ./include/lxml
		'''
	elif os.path.exists("/Library/Python/2.7/site-packages/lxml"):
		print "Copy from python2.7 packages into include\n"
		cmd = '''
		sudo cp -r /Library/Python/2.7/site-packages/lxml ./include/lxml
		'''
		
#cmd += "sudo port install py2" + str(currentVersion) + "-pyquery" 
os.system(cmd)



