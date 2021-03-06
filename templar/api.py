"""
This is the API that templar exposes to python scripts who want
to get access to all the variables.
"""

import pkgutil
import os
import os.path
import mako
import mako.exceptions
import mako.template
import mako.lookup
import stat
import templar.fileops
import templar.git
import sys
import templar.install_deps

override_var_name = 'TEMPLAR_OVERRIDE'


class D(dict):
    """
    class that looks like a dictionary but also like a namespace to allow the end users
    namespace like access (easy) and also non namespace like access.
    """
    def __init__(self):
        super().__init__(self)

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, val):
        self[name] = val


def get_mod_list():
    for (module_loader, name, is_package) in pkgutil.iter_modules(path=['templardefs']):
        if is_package:
            continue
        ml = module_loader.find_module(name)
        m = ml.load_module()
        yield m


def load_and_populate():
    d = D()
    for m in get_mod_list():
        m.populate(d)

    # environment override
    if override_var_name in os.environ:
        values = os.environ[override_var_name].split(';')
        for value in values:
            k, v = value.strip().split('=')
            d[k] = v

    return d


def get_all_deps():
    for m in get_mod_list():
        for d in m.get_deps():
            yield d


def process(d, input_file, output_file, input_encoding=sys.getdefaultencoding(),
            output_encoding=sys.getdefaultencoding(), no_chmod=False):
    """
    if there is any error, remove the output to prevent having
    bad output...
    """
    try:
        '''
        We really need the unlink, even though we have *open a file
        for writing* later on which is supposed to truncate the file to 0
        since we chmod the output to be non writable which means that the
        *open a file for writing* later would fail...
        '''
        if os.path.isfile(output_file):
            os.unlink(output_file)
        lookup = mako.lookup.TemplateLookup(
            directories=['.'],
            input_encoding=input_encoding,
            output_encoding=output_encoding,
        )
        template = mako.template.Template(
            filename=input_file,
            lookup=lookup,
            input_encoding=input_encoding,
            output_encoding=output_encoding,
        )
        templar.fileops.ensure_dir(output_file)
        f = open(output_file, 'wb')
        f.write(template.render(tdefs=d))
        f.close()
        if not no_chmod:
            # old solution which is no good because of umask
            # and executable scripts
            # os.chmod(output, 0o0444)
            current = stat.S_IMODE(os.stat(input_file).st_mode)
            current &= ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
            os.chmod(output_file, current)
        else:
            current = stat.S_IMODE(os.stat(input_file).st_mode)
            os.chmod(output_file, current)
    except Exception as e:
        if os.path.isfile(output_file):
            os.unlink(output_file)
        raise e


def print_full_exception():
    print('printing full exception')
    traceback = mako.exceptions.RichTraceback()
    for (filename, line_number, function, line) in traceback.traceback:
        print('File {0}, line {1}, in {2}'.format(filename, line_number, function))
        print(line)
    print('{0}: {1}'.format(str(traceback.error.__class__.__name__), traceback.error))


def print_exception(e, input_file):
    found = False
    traceback = mako.exceptions.RichTraceback()
    for (filename, line_number, function, line) in traceback.traceback:
        if filename == input_file:
            print('{0}: error {1} in {2}, line {3}'.format(sys.argv[0], str(e), filename, line_number, function))
            print('{0}'.format(line))
            found = True
    if not found:
        for (filename, line_number, function, line) in traceback.traceback:
            print('File {0}, line {1}, in {2}'.format(filename, line_number, function))
            print(line)
        print('{0}: {1}'.format(str(traceback.error.__class__.__name__), traceback.error))


def install_deps(d):
    templar.install_deps.install_deps(d)


def git_config(d):
    templar.git.git_config(d)
