#!/usr/bin/python3

'''
this script will install all the required packages that you need on
ubuntu to compile and work with this package.
'''

import subprocess # for check_call, DEVNULL
import yaml # for load
import os.path # for isfile

APT_FILE='apt.yaml'
def install_apt():
	# if the file is not there it is NOT an error
	if not os.path.isfile(APT_FILE):
		return
	print('installing from {0}...'.format(APT_FILE))
	with open(APT_FILE, 'r') as stream:
		o=yaml.load(stream)
	packs=[ x['name'] for x in o['packages'] ]
	args=[
		'sudo',
		'apt-get',
		'install',
		'--assume-yes'
	]
	args.extend(packs)
	subprocess.check_call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

NODE_FILE='package.json'
def install_node():
	# if the file is not there it is NOT an error
	if not os.path.isfile(NODE_FILE):
		return
	print('installing from {0}...'.format(NODE_FILE))
	subprocess.check_call([
		'npm',
		'install',
	], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

install_apt()
install_node()
