import os, sys

sys.path.insert(0, '../swim')
import swim

for file in os.listdir('.'):
	if file.endswith('.swim'):
		swim.main(file)