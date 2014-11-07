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
import os # for chmod, unlink, makedirs
import os.path # for isfile, dirname, isdir
import argparse # for ArgumentParser, ArgumentDefaultsHelpFormatter
import templar.tdefs # for populate, getdeps
import pkgutil # for iter_modules

###########
# classes #
###########
'''
class that looks like a dictionary but also like a namespace to allow the end users
namespace like access (easy) and also non namespace like access.
'''
class D(dict):
	def __init__(self):
		pass
	def __getattr__(self,name):
		return self[name]
	def __setattr__(self, name, val):
		self[name]=val

#############
# functions #
#############
def get_mod_list():
	for (module_loader, name, ispkg) in pkgutil.iter_modules(path=['templardefs']):
		if ispkg:
			continue
		ml=module_loader.find_module(name)
		m=ml.load_module()
		yield m

def load_and_populate():
	d=D()
	templar.tdefs.populate(d)
	for m in get_mod_list():
		m.populate(d)
	return d

def get_all_deps():
	for d in templar.tdefs.getdeps():
		yield d
	for m in get_mod_list():
		for d in m.getdeps():
			yield d

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
			output_folder=os.path.dirname(args.output)
			if output_folder!='' and not os.path.isdir(output_folder):
				os.makedirs(output_folder)
			file=open(args.output, 'wb')
			tdefs=load_and_populate()
			file.write(template.render(tdefs=tdefs))
			file.close()
			if not args.nochmod:
				# FIXME: only remove the w from user group and all
				os.chmod(args.output, 0o0444)
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
		tdefs=load_and_populate()
		for k in sorted(tdefs.keys()):
			v=tdefs[k]
			if v.find('\n')!=-1:
				continue
			if not args.nosec and ( k.find('password')!=-1 or k.find('secret')!=-1 ):
				continue
			print('{0}.{1}:={2}'.format('tdefs', k, v))

	if args.subcommand=='printall':
		tdefs=load_and_populate()
		for k in sorted(tdefs.keys()):
			v=tdefs[k]
			print('{0}.{1}={2}'.format('tdefs', k, v))

	if args.subcommand=='getdeps':
		print(' '.join(get_all_deps()))
