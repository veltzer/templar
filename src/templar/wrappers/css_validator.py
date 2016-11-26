"""
this is a specific wrapper written for the css validator

css validator does NOT return a good error code (0 always).
"""

import sys
import subprocess


def run(args):
    # run the command
    # noinspection PyBroadException
    try:
        out = subprocess.check_output(args).decode()
    except:
        sys.exit(7)
    do_print = False
    error = False
    for line in out.split('\n'):
        if line.startswith('Sorry'):
            do_print = True
            error = True
        if line.startswith('Valid'):
            do_print = False
        if do_print:
            print(line)
    if error:
        sys.exit(1)
