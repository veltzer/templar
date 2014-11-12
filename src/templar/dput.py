'''
Module that knows how to run dput(1)
'''

import templar.subprocess # for check_call
import os.path # for join

def run(d):
	templar.subprocess.check_call([
		'dput',
		d.launchpad_ppa,
		os.path.join(d.deb_out_folder, '{0}_{1}_source.changes'.format(d.deb_pkgname, d.deb_version)),
	])
