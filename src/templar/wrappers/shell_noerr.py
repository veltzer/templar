"""
run a string via a shell and do not return its exit code.
"""

import subprocess


def run(arg):
    assert type(arg) == str
    subprocess.call(arg, shell=True)
