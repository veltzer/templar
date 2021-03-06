"""
run any command line and do not emit it's standard
error or output unless there is an error, in which case
emit them and exit with the original commands exit code.

This wrapper is DIFFERENT than the noerr.py wrapper
since this one actually exits with error codes.
"""

import sys
import subprocess


def run(args):
    assert type(args) == list
    pr = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out_out, out_err) = pr.communicate()
    status = pr.returncode
    if status:
        print(out_out.decode(), end='')
        print(out_err.decode(), end='')
        sys.exit(status)
