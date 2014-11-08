'''
This module captures all output from a process.
It exports a generator like interface.
See my demos-python repository to see how this works.
'''

import sys # for stderr, exit
import pty # for fork
import os # for execv, fdopen

def capture_all(args):
	(pid, fd)=pty.fork()
	if pid==0:
		os.execv(args[0], args)
		print('execv didnt work', sys.stderr)
		sys.exit(1)
	else:
		try:
			for line in os.fdopen(fd):
				yield line
		except OSError as e:
			pass
