'''
A module which wraps subprocess

Why do we need this?
This is a single place where activation of processes takes place and so we could
centrally debug everything that is going on.
'''

import subprocess # for check_call, DEVNULL
import templar.debug # for process

# do we want to see stdout and stderr?
opt_debug=False

'''check_call wrapper'''
def check_call(l):
	templar.debug.process(l)
	if opt_debug:
		subprocess.check_call(l)
	else:
		subprocess.check_call(l, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

