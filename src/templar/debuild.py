'''
This module knows how to build debian packages using the debuild(1) command.
'''

import subprocess # for call
import templar.wrappers.debuid # for run
import os # for unlink
import glob # for glob
import templar.api # for load_and_populate
import templar.git # for clean
import templar.make # for make

def run():
	d=templar.api.load_and_populate()
	templar.git.clean()
	templar.make.make('templar')
	for f in glob.glob('../{0}_*'.format(d.deb_pkgname)):
		os.unlink(f)
	templar.wrappers.debuid(['debuild','-S'])
	os.mkdir(d.deb_build_source)
	'''
	$(Q)mv ../$(tdefs.deb_pkgname)_* $(tdefs.deb_build_source)
	$(Q)chmod 444 $(tdefs.deb_build_source)/$(tdefs.deb_pkgname)_*
	'''
