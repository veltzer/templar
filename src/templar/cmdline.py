'''
This script is a wrapper for the mako templating system to be used from the command line,
build system or whatever.

It has command line parsing and ability to import your own variable definitions.
- It can process a single file, in the future this may change.
- It work in utf.
- It chmods the output file to be read only (to avoid accidentaly editing it).
- On any exception no output file is produced.
- You can specify encodings from the command line.
TODO:
- make this module create the folder for the output file if that folder does not exist.
'''

###########
# imports #
###########
import sys # for argv, getdefaultencoding, exit
import argparse # for ArgumentParser, ArgumentDefaultsHelpFormatter
import templar.api # for load_and_populate, process, print_exception

def cmdline():
	parser=argparse.ArgumentParser(
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	subparsers=parser.add_subparsers(
		title='subcommands',
		dest='subcommand',
	)

	subparser_process=subparsers.add_parser(
		'process',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	subparser_process.add_argument('--input', help='input file')
	subparser_process.add_argument('--inputencoding', help='specify input encoding', default=sys.getdefaultencoding())
	subparser_process.add_argument('--output', help='output file')
	subparser_process.add_argument('--outputencoding', help='specify output encoding', default=sys.getdefaultencoding())
	subparser_process.add_argument('--nochmod', help='dont chmod the output to readonly', default=False, action='store_true')

	subparser_print=subparsers.add_parser(
		'printmake',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	subparser_print.add_argument('--nosec', help='dont do security', default=False, action='store_true')

	subparser_print=subparsers.add_parser(
		'printall',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)

	subparser_print=subparsers.add_parser(
		'getdeps',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)

	args=parser.parse_args()

	if args.subcommand=='process':
		d=templar.api.load_and_populate()
		try:
			templar.api.process(
				d,
				args.input,
				args.output,
				args.inputencoding,
				args.outputencoding,
				args.nochmod,
			)
		except Exception as e:
			print_exception(e, args.input)
			sys.exit(1)

	if args.subcommand=='printmake':
		d=templar.api.load_and_populate()
		for k in sorted(d.keys()):
			v=d[k]
			if type(v)!=str:
				continue
			if v.find('\n')!=-1:
				continue
			if not args.nosec and ( k.find('password')!=-1 or k.find('secret')!=-1 ):
				continue
			print('{0}.{1}:={2}'.format('tdefs', k, v))

	if args.subcommand=='printall':
		d=templar.api.load_and_populate()
		for k in sorted(d.keys()):
			v=d[k]
			print('{0}.{1}={2}'.format('tdefs', k, v))

	if args.subcommand=='getdeps':
		print(' '.join(templar.api.get_all_deps()))
