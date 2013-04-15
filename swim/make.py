import os
os.system("cp -r AST.py core.py namespace.py swim.py swim_exception.py swim_lex.py swim_parse.py")
os.system("python ../pyinstaller-2.0/pyinstaller.py --onefile swim.py")
os.system("cp -r ../pyinstaller-2.0/swim/dist/swim ../bin/")