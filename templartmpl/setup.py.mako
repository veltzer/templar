#!/usr/bin/python3

'''
This is the installation tool. use minimal packages here.
dont use setuptools, dont use subprocess.
'''

import distutils.core # for setup

distutils.core.setup(
	name='${tdefs.project_name}',
	version='${tdefs.git_lasttag}~${tdefs.apt_codename}',
	description='${tdefs.project_description}',
	long_description='${tdefs.project_long_description}',
	author='${tdefs.personal_fullname}',
	author_email='${tdefs.personal_email}',
	maintainer='${tdefs.personal_fullname}',
	maintainer_email='${tdefs.personal_email}',
	keywords=${tdefs.hlp_project_keywords()},
	url='${tdefs.project_website}',
	license='${tdefs.project_license}',
	platforms=${tdefs.hlp_project_platforms()},
	${tdefs.hlp_source_under('src') | tdefs.make_hlp_wrap(1) },
	classifiers=${tdefs.hlp_project_classifiers()},
	data_files=[
		('/usr/share/templar', ['make/Makefile']),
		${tdefs.hlp_files_under('templates/*.mako', '/usr/share/templar/templates')},
		${tdefs.hlp_files_under('src/*', '/usr/bin')},
	],
)
