'''
Module that will run git tasks for you
'''

import sys # for stderr
import templar.subprocess # for check_call, check_output

''' git clean -xdf > /dev/null '''
def clean():
	templar.subprocess.check_call(['git', 'clean', '-xdf'])

''' function that reports if all is comitted '''
def is_allcommit():
	out=templar.subprocess.check_output(['git','status','-s']).decode()
	return out==''

''' function that checks that all is committed '''
def check_allcommit():
	if not is_allcommit():
		print('first commit everything, then call me...', file=sys.stderr)
		sys.exit(1)

def commit_all(msg):
	templar.subprocess.check_call(['git','commit','--all','-m',msg])

def push(tags):
	args=['git','push',]
	if tags:
		args.append('--follow-tags')
		#args.append('--tags')
	templar.subprocess.check_call(args)

def tag(tag):
	templar.subprocess.check_call(['git','tag','--annotate','--sign','-m',tag,tag])
