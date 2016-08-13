#!/usr/bin/python3

'''
this script will install all the required packages that you need on
ubuntu to compile and work with this package.
'''

import tools # for install_apt, install_node

tools.install_apt()
tools.install_node()
