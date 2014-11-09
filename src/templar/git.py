'''
Module that will run git tasks for you
'''

import subprocess # for check_call, DEVNULL

''' git clean -xdf > /dev/null '''
def clean():
	subprocess.check_call(['git', 'clean', '-xdf'], stdout=subprocess.DEVNULL)
