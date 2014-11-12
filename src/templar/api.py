'''
This is the API that templar exposes to python scripts who want
to get access to all the variables.
'''

###########
# imports #
###########
import pkgutil # for iter_modules
import os # for environ

###########
# globals #
###########
override_var_name='TEMPLAR_OVERRIDE'

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
	for m in get_mod_list():
		m.populate(d)

	# environment override
	if override_var_name in os.environ:
		values=os.environ[override_var_name].split(';')
		for value in values:
			k,v=value.strip().split('=')
			d[k]=v

	return d

def get_all_deps():
	for m in get_mod_list():
		for d in m.getdeps():
			yield d
