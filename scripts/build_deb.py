#!/usr/bin/python3

'''
This script will build a package and will move all the results to ~/packages
'''

import subprocess # for check_call
import os # for system

subprocess.check_call([
	'debuild',
])
os.system('mv ../templar_* ~/packages')
