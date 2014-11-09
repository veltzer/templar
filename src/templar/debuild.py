'''
This module knows how to build debian packages using the debuild(1) command.
'''

import templar.git # for clean
import templar.make # for make
import glob # for glob
import templar.wrappers.debuild # for run
import templar.fileops # for unlink, move, chmod, mkdir

def run(d):
	templar.git.clean()
	templar.make.make('templar')
	for f in glob.glob('../{0}_*'.format(d.deb_pkgname)):
		templar.fileops.unlink(f)
	templar.wrappers.debuild.run(['debuild','-S'])
	templar.fileops.mkdir(d.deb_build_source)
	for f in glob.glob('../{0}_*'.format(d.deb_pkgname)):
		res=templar.fileops.move(f, d.deb_build_source)
		templar.fileops.chmod(res, 0o0444)
