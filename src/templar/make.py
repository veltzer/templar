"""
Module that will run make tasks for you
"""

import templar.subprocess


def make(target):
    """ make [foo] """
    templar.subprocess.check_call(['make', target])
