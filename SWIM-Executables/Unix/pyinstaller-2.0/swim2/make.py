import os
os.system("cp -r *.py *.swim ../pyinstaller-2.0/swim2/")
os.system("python ../pyinstaller-2.0/pyinstaller.py --onefile ../pyinstaller-2.0/swim2/swim.py")
os.system("cp dist/swim ./")
os.system("rm -r build dist")
#os.system("cp -r ../pyinstaller-2.0/swim/dist/swim ../bin/")