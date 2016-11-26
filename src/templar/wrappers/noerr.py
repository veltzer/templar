"""
run any command line and do not emit it's standard error or output unless there is an error
or there was an error.

Notice that we run the commands via a shell so that we will be able to do the following:
this_script.py 'ls -l 2> /dev/null'
In this case we will have on argument and we MUST run it to preserve the intention of the user.
if on the other hand we are run this way:
this_script.py ls -l
in which case we get many arguments, its ok to run them without a shell and save some resources.
"""

import subprocess


def run(args):
    assert type(args) == list
    subprocess.call(args)
