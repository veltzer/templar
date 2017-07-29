"""
This module will handle tasks related to python versions
for you
"""

import sys


def check_version_x_y(x, y):
    if sys.version_info[0:2] != (x, y):
        print('you must use python version {0}.{1}'.format(x, y), file=sys.stderr)
        sys.exit(1)


def check_version_tup(t):
    if sys.version_info[0:2] != t:
        print('you must use python version {0}.{1}'.format(t[0], t[1]), file=sys.stderr)
        sys.exit(1)


def check_version(t):
    if sys.version_info[0:2] != t:
        raise Exception('you must use python {0}'.format(t))
