'''
Module that knows how to run dpkg(1)
'''

import templar.subprocess # for check_call
import os.path # for join

def install(d):
	templar.subprocess.check_call([
		'sudo',
		'dpkg',
		'--install',
		os.path.join(d.deb_out_folder, '{0}_{1}~{2}_{3}.deb'.format(
			d.deb_pkgname,
			d.git_lasttag,
			d.apt_codename,
			d.deb_architecture,
		)),
	])
