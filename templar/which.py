"""
This is a module which helps in resolving paths for executing stuff.

It's main API is the which(1) function.

References:
http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python/
"""

import os.path
import os

'''
returns the absolute path of a program

if you pass an absolute path then it will check that the program is executable
and return it.

if you pass a relative path it will resolve it via the PATH environment variable
will check that it is executable and return it.

if the program cannot be found or is not executable an exception will be raised.
'''


def is_exe(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


def which(program):
    if os.path.isabs(program):
        assert is_exe(program)
        return program
    for path in os.environ['PATH'].split(os.pathsep):
        curr = os.path.join(path, program)
        if is_exe(curr):
            return curr
    raise ValueError('cannot find the program [{0}] in PATH'.format(program))
