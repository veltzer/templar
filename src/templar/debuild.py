'''
This module knows how to build debian packages using the debuild(1) command.
'''

import templar.git # for clean
import glob # for glob
import templar.wrappers.debuild # for run
import templar.fileops # for unlink, move, chmod, mkdir, chmod_pw
import templar.api # for process, print_exception
import templar.utils # for pkg_get_real_filename
import os.path # for isdir

def run(d, source, gbp):
	templar.git.clean()
	# debian folder should not exist
	assert not os.path.isdir('debian')
	# first arg is relative to current package
	templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/changelog.mako'), 'debian/changelog')
	templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/compat.mako'), 'debian/compat')
	templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/control.mako'), 'debian/control')
	templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/copyright.mako'), 'debian/copyright')
	#templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/files.mako'), 'debian/files')
	templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/format.mako'), 'debian/source/format')
	templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/rules.mako'), 'debian/rules')
	templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/setup.py.mako'), 'setup.py')
	for f in glob.glob('../{0}_*'.format(d.deb_pkgname)):
		templar.fileops.unlink(f)
	if not source or gbp:
		templar.fileops.chmod_pw('debian/control')
	if gbp:
		args=['git-buildpackage']
	else:
		args=['debuild']
	if source:
		args.append('-S')
	templar.wrappers.debuild.run(args)
	templar.fileops.mkdir(d.deb_out_folder)
	for f in glob.glob('../{0}_*'.format(d.deb_pkgname)):
		res=templar.fileops.move(f, d.deb_out_folder)
		templar.fileops.chmod(res, 0o0444)
