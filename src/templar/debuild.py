'''
This module knows how to build debian packages using the debuild(1) command.
'''

import templar.git # for clean
import templar.make # for make
import glob # for glob
import templar.wrappers.debuild # for run
import templar.fileops # for unlink, move, chmod, mkdir, chmod_pw

def run(d, source):
	templar.git.clean()
	templar.make.make('templar')
	for f in glob.glob('../{0}_*'.format(d.deb_pkgname)):
		templar.fileops.unlink(f)
	templar.fileops.chmod_pw('debian/control')
	args=['debuild']
	if source:
		args.append('-S')
	templar.wrappers.debuild.run(args)
	templar.fileops.mkdir(d.deb_out_folder)
	for f in glob.glob('../{0}_*'.format(d.deb_pkgname)):
		res=templar.fileops.move(f, d.deb_out_folder)
		templar.fileops.chmod(res, 0o0444)
