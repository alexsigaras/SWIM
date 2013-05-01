import os
os.system("cp -r *.py *.swim ../SWIM-Executables/Unix/pyinstaller-2.0/swim3/")
os.system("python ../SWIM-Executables/Unix/pyinstaller-2.0/pyinstaller.py --onefile ../SWIM-Executables/Unix/pyinstaller-2.0/swim3/swim.py")
os.system("cp dist/swim ./")
os.system("rm -r build dist")
#os.system("cp -r ../pyinstaller-2.0/swim/dist/swim ../bin/")