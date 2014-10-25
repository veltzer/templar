#!/usr/bin/python3

'''
This is the installation tool. use minimal packages here.
dont use setuptools, dont use subprocess.

We really this file to be generated.
'''

import distutils.core # for setup

distutils.core.setup(
	name='templar',
	description='Templating engine for python',
	long_description='Templating engine for python (long description)',
	author='Mark Veltzer',
	author_email='mark@veltzer.net',
	maintainer='Mark Veltzer',
	maintainer_email='mark@veltzer.net',
	keywords=[
		'mako',
		'templating',
		'python',
	],
	url='https://www.veltzer.net/templar',
	license='LGPL',
	platforms=[
		'ALL',
	],
	packages=['templar'],
	version='0.3',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: LGPL',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Building',
		'Topic :: Software Development :: Libraries',
		'Topic :: Utilities',
	],
	data_files=[
		('/usr/share/templar', ['make/Makefile.prep']),
	],
)
