'''
centralized debugging module
'''

import sys # for stderr

# do you want to see the commands?
opt_show_commands=True

def process(l):
	if opt_show_commands:
		print('executing [{0}]...'.format(l), file=sys.stderr)

def debug(s):
	if opt_show_commands:
		print(s, file=sys.stderr)
