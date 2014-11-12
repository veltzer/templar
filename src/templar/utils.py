import configparser # for ConfigParser
import os.path # for isfile
import glob # for glob

def read_full_ini_cls(cls, filename):
	assert os.path.isfile(filename)
	ini_config=configparser.ConfigParser()
	ini_config.read(filename)
	for section in ini_config.sections():
		for k,v in ini_config.items(section):
			setattr(cls, '{0}_{1}'.format(section, k), v)

def read_ini_cls(cls, filename, sections):
	assert os.path.isfile(filename)
	ini_config=configparser.ConfigParser()
	ini_config.read(filename)
	for section in sections:
		for k,v in ini_config.items(section):
			setattr(cls, '{0}_{1}'.format(section, k), v)

def read_full_ini_dict(d, filename):
	assert os.path.isfile(filename)
	ini_config=configparser.ConfigParser()
	ini_config.read(filename)
	for section in ini_config.sections():
		for k,v in ini_config.items(section):
			d['{0}_{1}'.format(section, k)]=v

def read_ini_cls_dict(d, filename, sections):
	assert os.path.isfile(filename)
	ini_config=configparser.ConfigParser()
	ini_config.read(filename)
	for section in sections:
		for k,v in ini_config.items(section):
			d['{0}_{1}'.format(section, k)]=v

def hlp_files_under(dest_folder, pat):
	return (dest_folder, sorted([ x for x in glob.glob(pat) if os.path.isfile(x)]))
