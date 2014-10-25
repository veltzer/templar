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
import mako # for exceptions
import mako.exceptions # for RickTraceback
import mako.template # for Template
import mako.lookup # for TemplateLookup
import os # for chmod, unlink
import os.path # for isfile
import argparse # for ArgumentParser, ArgumentDefaultsHelpFormatter

#############
# functions #
#############
def cmdline(clsdict):
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
	subparser_process.add_argument('--chmod', help='chmod the output?', default=True, action='store_false')

	subparser_print=subparsers.add_parser(
		'printmake',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)

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
		'''
		if there is any error, remove the output to prevent having
		bad output...
		'''
		try:
			'''
			We really need the unlink, even though we have *open a file
			for writing* later on which is supposed to truncate the file to 0
			since we chmod the output to be unwritable which means that the
			*open a file for writing* later would fail...
			'''
			if os.path.isfile(args.output):
				os.unlink(args.output)
			mylookup=mako.lookup.TemplateLookup(
				directories=['.'],
				input_encoding=args.inputencoding,
				output_encoding=args.outputencoding,
			)
			template=mako.template.Template(
				filename=args.input,
				lookup=mylookup,
				input_encoding=args.inputencoding,
				output_encoding=args.outputencoding,
			)
			file=open(args.output,'wb')
			for name, cls in clsdict.items():
				cls.init()
			file.write(template.render(**clsdict))
			file.close()
			if args.chmod:
				os.chmod(args.output,0o0444)
		except Exception as e:
			if os.path.isfile(args.output):
				os.unlink(args.output)
			found=False
			traceback=mako.exceptions.RichTraceback()
			for (filename, lineno, function, line) in traceback.traceback:
				if filename==args.input:
					print('{0}: error {1} in {2}, line {3}'.format(sys.argv[0], str(e), filename, lineno, function))
					print('{0}'.format(line))
					found=True
			if not found:
				for (filename, lineno, function, line) in traceback.traceback:
					print('File {0}, line {1}, in {2}'.format(filename, lineno, function))
					print(line)
				print('{0}: {1}'.format(str(traceback.error.__class__.__name__), traceback.error))
			sys.exit(1)

	if args.subcommand=='printmake':
		for name, cls in clsdict.items():
			cls.init()
			for k in sorted(cls.__dict__.keys()):
				v=cls.__dict__[k]
				if not k.startswith('__') and type(v)==str:
					print('{0}.{1}:={2}'.format(name, k, v))

	if args.subcommand=='printall':
		for name, cls in clsdict.items():
			cls.init()
			for k in sorted(cls.__dict__.keys()):
				v=cls.__dict__[k]
				print('{0}.{1}={2}'.format(name, k, v))

	if args.subcommand=='getdeps':
		print(' '.join([cls.getdeps() for cls in clsdict.values()]))
