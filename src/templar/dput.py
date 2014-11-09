'''
Module that knows how to run dput(1)
'''

import templar.subprocess # for check_call
import os.path # for join

def run(d):
	templar.subprocess.check_call([
		'dput',
		d.launchpad_ppa,
		os.path.join(d.deb_build_source, '{0}_{1}~{2}_source.changes'.format(d.deb_pkgname, d.git_lasttag, d.apt_codename)),
	])
