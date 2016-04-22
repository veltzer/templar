#!/usr/bin/python3

'''
this script will install all the required packages that you need on
ubuntu to compile and work with this package.
'''

import subprocess # for check_call

packs=[
	# for scripts
	'python3', # for the python scripts
	'python3-all', # for the python scripts
	'dh-python', # for packaging helpers

	# for installation:
	'python-setuptools-doc', # for packaging
	'python3-setuptools', # for packaging
	'python-setuptools', # for packaging
	'python3-setuptools-git', # for packaging
	'python-setuptools-git', # for packaging

	# mako templating (current templating)
	'python3-mako', # mako for python 3 (we are not really using it)
	'python-mako-doc', # documentation for the template preprocessor
	
	# debian tools
	'devscripts', # for debuild(1)
]

args=[
	'sudo',
	'apt-get',
	'install',
	'--assume-yes'
]
args.extend(packs)
subprocess.check_call(args)
