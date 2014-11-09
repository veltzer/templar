#!/usr/bin/python3

'''
This is the installation tool. use minimal packages here.
dont use setuptools, dont use subprocess.
'''

import distutils.core # for setup

distutils.core.setup(
	name='templar',
	version='40~utopic',
	description='Easy templating tool long description (TBD)',
	long_description='Templating solution for programmers',
	author='Mark Veltzer',
	author_email='mark.veltzer@gmail.com',
	maintainer='Mark Veltzer',
	maintainer_email='mark.veltzer@gmail.com',
	keywords=[ 'mako',
'templating',
'python' ],
	url='https://veltzer.github.io/templar',
	license='LGPL',
	platforms=[
		'ALL',
	],
	packages=[
		'templar',
		'templar/wrappers',
	],
	package_dir = {
		'templar':'src/templar',
		'templar/wrappers':'src/templar/wrappers',
	},
	classifiers=[ 'Development Status :: 4 - Beta',
'Environment :: Console',
'Intended Audience :: Developers',
'License :: OSI Approved :: LGPL',
'Operating System :: OS Independent',
'Programming Language :: Python',
'Programming Language :: Python :: 3',
'Topic :: Software Development :: Building',
'Topic :: Software Development :: Libraries',
'Topic :: Utilities' ],
	data_files=[
		('/usr/share/templar', ['make/Makefile']),
		('/usr/share/templar/templates', ['templates/README.md.mako']),
		('/usr/share/templar/templates', ['templates/changelog.mako']),
		('/usr/bin', ['src/templar_cmd']),
		('/usr/bin', ['src/make_helper']),
	],
)
