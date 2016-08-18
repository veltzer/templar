'''
A module which wraps subprocess

Why do we need this?
This is a single place where activation of processes takes place and so we could
centrally debug everything that is going on.

TODO:
- in the case where debug is not needed so output to the screen should be
minimized aggregate the output of the commands
and output them in case of error or debug.
'''

import subprocess # for check_call, DEVNULL
import templar.debug # for process

# do we want to see stdout and stderr?
opt_debug=False

'''check_call wrapper'''
def check_call(l):
    templar.debug.process(l, 'check_call')
    if opt_debug:
        subprocess.check_call(l)
    else:
        subprocess.check_call(l, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

'''check_output wrapper'''
def check_output(l):
    templar.debug.process(l, 'check_output')
    if opt_debug:
        return subprocess.check_output(l)
    else:
        return subprocess.check_output(l, stderr=subprocess.DEVNULL)
