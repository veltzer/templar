'''
This module knows how to build debian packages using the debuild(1) command.
'''

import templar.api # for load_and_populate
import templar.git # for clean
import templar.make # for make
import glob # for glob
import os # for unlink, mkdir
import templar.wrappers.debuild # for run
import shutil # for move

def run():
	d=templar.api.load_and_populate()
	templar.git.clean()
	templar.make.make('templar')
	for f in glob.glob('../{0}_*'.format(d.deb_pkgname)):
		os.unlink(f)
	templar.wrappers.debuild.run(['debuild','-S'])
	os.mkdir(d.deb_build_source)
	for f in glob.glob('../{0}_*'.format(d.deb_pkgname)):
		res=shutil.move(f, d.deb_build_source)
		os.chmod(res, 0o0444)
