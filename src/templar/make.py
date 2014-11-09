'''
Module that will run make tasks for you
'''

import subprocess # for check_call

''' make [foo] '''
def make(target):
	subprocess.check_call(['make', target])
