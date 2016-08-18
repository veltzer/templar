'''
This module will handle tasks related to python versions
for you
'''

import sys # for version_info, exit, stderr

def checkversion(x,y):
    if sys.version_info[0:2] != (x,y):
        print('you must use python version {0}.{1}'.format(x,y), file=sys.stderr)
        sys.exit(1)
