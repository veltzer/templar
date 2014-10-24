#!/usr/bin/python3

import distutils.core # for setup
import setuptools # for find_packages
import subprocess # for check_output

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
	packages=setuptools.find_packages(),
	version=subprocess.check_output(['git','describe']).decode().rstrip(),
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
	# scripts cannot specify target directory by data_files can...:)
	data_files=[
		('/usr/bin', ['templar.py']),
	],
	#scripts=['templar.py'],
)
