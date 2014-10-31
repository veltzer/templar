#!/usr/bin/python3

'''
Make is really bad at doing text processing. So the idea is to help make out
by supplying a python script which do the heavy lifting and keep the make code
clean and simple.
'''

###########
# imports #
###########
import os.path # splitext
import os # for sep
import argparse # for ArgumentParser, ArgumentDefaultsHelpFormatter, REMAINDER

########
# code #
########
parser=argparse.ArgumentParser(
	formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
subparsers=parser.add_subparsers(
	title='subcommands',
	dest='subcommand',
)

subparser_rmfdas=subparsers.add_parser(
	'rmfdas',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
subparser_rmfdas.add_argument('filenames', nargs=argparse.REMAINDER, action='store')

args=parser.parse_args()

if args.subcommand=='rmfdas':
	result=[]
	for f in args.filenames:
		r=os.path.splitext(os.sep.join(f.split(os.sep)[1:]))[0]
		result.append(r)
	print(' '.join(result), end='')
