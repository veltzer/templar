'''
this is a specific wrapper written for the css validator

css validator does NOT return a good error code (0 always).
'''

import sys # for exit
import subprocess # for check_output

def run(args):
    # run the command
    try:
        out=subprocess.check_output(args)
    except:
        sys.exit(7)
    doPrint=False
    error=False
    for line in out.split('\n'):
        line=line.decode()
        if line.startswith('Sorry'):
            doPrint=True
            error=True
        if line.startswith('Valid'):
            doPrint=False
        if doPrint:
            print(line)
    if error:
        sys.exit(1)
