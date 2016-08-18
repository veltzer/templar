'''
run any command line, emit its output and error but always return an OK (0) return code
'''

import subprocess # for call

def run(args):
    subprocess.call(args)
