#!/usr/bin/python3

'''
This is the installation tool. use minimal packages here.
dont use setuptools, dont use subprocess.
'''

import distutils.core # for setup

distutils.core.setup(
	name='${tdefs.project_name}',
	#version='tdefs.git_lasttag~tdefs.apt_codename',
	description='${tdefs.project_description}',
	long_description='${tdefs.project_long_description}',
	author='${tdefs.personal_fullname}',
	author_email='${tdefs.personal_email}',
	maintainer='${tdefs.personal_fullname}',
	maintainer_email='${tdefs.personal_email}',
	keywords=[ ${tdefs.project_keywords} ],
	url='${tdefs.project_website}',
	license='${tdefs.project_license}',
	platforms=[
		'ALL',
	],
	packages=['src/templar'],
	classifiers=[ ${tdefs.project_classifiers} ],
	data_files=[
		('/usr/share/templar', ['make/Makefile']),
		('/usr/share/templar/templates', ['templates/README.md.mako']),
		('/usr/share/templar/templates', ['templates/changelog.mako']),
		('/usr/bin', ['src/templar_cmd']),
		('/usr/bin', ['src/make_helper']),
		('/usr/bin', ['src/release_helper']),
	],
)
