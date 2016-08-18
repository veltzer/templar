'''
This is the API that templar exposes to python scripts who want
to get access to all the variables.
'''

###########
# imports #
###########
import pkgutil # for iter_modules
import os # for environ, chmod, unlink, makedirs, stat
import os.path # for isfile
import mako # for exceptions
import mako.exceptions # for RickTraceback
import mako.template # for Template
import mako.lookup # for TemplateLookup
import stat # for S_IMODE, S_IWRITE
import templar.fileops # for ensure_dir
import sys # for getdefaultencoding
import templar.install_deps # for install_deps

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

def process(d, inputfile, outputfile, inputencoding=sys.getdefaultencoding(), outputencoding=sys.getdefaultencoding(), nochmod=False):
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
        if os.path.isfile(outputfile):
            os.unlink(outputfile)
        mylookup=mako.lookup.TemplateLookup(
            directories=['.'],
            input_encoding=inputencoding,
            output_encoding=outputencoding,
        )
        template=mako.template.Template(
            filename=inputfile,
            lookup=mylookup,
            input_encoding=inputencoding,
            output_encoding=outputencoding,
        )
        templar.fileops.ensure_dir(outputfile)
        f=open(outputfile, 'wb')
        f.write(template.render(tdefs=d))
        f.close()
        if not nochmod:
            # old solution which is no good because of umask
            # and executable scripts
            # os.chmod(output, 0o0444)
            current = stat.S_IMODE(os.stat(inputfile).st_mode)
            current &= ~( stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH )
            os.chmod(outputfile, current)
        else:
            current = stat.S_IMODE(os.stat(inputfile).st_mode)
            os.chmod(outputfile, current)
    except Exception as e:
        if os.path.isfile(outputfile):
            os.unlink(outputfile)
        raise e

def print_full_exception():
    print('printing full exception')
    traceback=mako.exceptions.RichTraceback()
    for (filename, lineno, function, line) in traceback.traceback:
        print('File {0}, line {1}, in {2}'.format(filename, lineno, function))
        print(line)
    print('{0}: {1}'.format(str(traceback.error.__class__.__name__), traceback.error))

def print_exception(e, inputfile):
    found=False
    traceback=mako.exceptions.RichTraceback()
    for (filename, lineno, function, line) in traceback.traceback:
        if filename==inputfile:
            print('{0}: error {1} in {2}, line {3}'.format(sys.argv[0], str(e), filename, lineno, function))
            print('{0}'.format(line))
            found=True
    if not found:
        for (filename, lineno, function, line) in traceback.traceback:
            print('File {0}, line {1}, in {2}'.format(filename, lineno, function))
            print(line)
        print('{0}: {1}'.format(str(traceback.error.__class__.__name__), traceback.error))

def install_deps(d):
    templar.install_deps.install_deps(d)

def git_config(d):
    templar.git.git_config(d)
