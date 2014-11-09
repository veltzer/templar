'''
this is a specific wrapper written for debuild since it does not have "warnings as errors"
and produces copious amounts of junk as output.
'''
import sys # for exit
import templar.capture_all # for capture_all

warning_patterns_to_ignore=set([
	'binary-without-manpage',
])

def run(args):
	seen_error=False
	do_errors=True
	do_always_print=False
	do_print_naked=True
	for line in templar.capture_all.capture_all(args):
		do_print=False
		if line.find('warning')!=-1:
			do_print=True
			seen_error=True
		if line.find('error')!=-1:
			do_print=True
			seen_error=True
		if line.startswith('W: '):
			for pat in warning_patterns_to_ignore:
				if line.find(pat)!=-1:
					break
			else:
				do_print=True
				seen_error=True
		if do_print or do_always_print:
			if do_print_naked:
				print(line, end='')
			else:
				print('got bad line [{0}]'.format(line.rstrip()))
	if seen_error and do_errors:
		sys.exit(1)
