'''
centralized file operations
'''

import os # for unlink, mkdir, chmod
import shutil # for move
import sys # for stderr

# do you want to see ops?
opt_debug=True

def unlink(f):
	if opt_debug:
		print('unlinking [{0}]'.format(f), file=sys.stderr)
	return os.unlink(f)

def mkdir(f):
	if opt_debug:
		print('mkdir [{0}]'.format(f), file=sys.stderr)
	return os.mkdir(f)

def chmod(f, mod):
	if opt_debug:
		print('chmod [{0}] to [{1}]'.format(f, mod), file=sys.stderr)
	return os.chmod(f, mod)

def move(a, b):
	if opt_debug:
		print('moving [{0}] to [{1}]'.format(a, b), file=sys.stderr)
	return shutil.move(a, b)
