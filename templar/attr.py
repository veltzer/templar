'''
Attributes for this project
'''

import datetime # for datetime
import subprocess # for check_output, DEVNULL
import os.path # for join, expanduser, basename
import os # for getcwd
import glob # for glob
import socket # for gethostname
import configparser # for ConfigParser

class Attr(object):

	@classmethod
	def read_full_ini(cls, filename):
		ini_file=os.path.expanduser(filename)
		if os.path.isfile(ini_file):
			ini_config=configparser.ConfigParser()
			ini_config.read(ini_file)
			for section in ini_config.sections():
				for k,v in ini_config.items(section):
					setattr(cls, '{0}_{1}'.format(section, k), v)

	@classmethod
	def read_ini(cls, filename, sections):
		ini_file=os.path.expanduser(filename)
		if os.path.isfile(ini_file):
			ini_config=configparser.ConfigParser()
			ini_config.read(ini_file)
			for section in sections:
				for k,v in ini_config.items(section):
					setattr(cls, '{0}_{1}'.format(section, k), v)


	@classmethod
	def init(cls):
		# general # TODO: get homedir in python
		cls.general_current_year=datetime.datetime.now().year
		cls.general_homedir='/home/mark'
		#cls.general_hostname=subprocess.check_output(['hostname']).decode().rstrip()
		cls.general_hostname=socket.gethostname()
		cls.general_domainname=subprocess.check_output(['hostname','--domain']).decode().rstrip()

		# messages
		cls.messages_dne='THIS FILE IS AUTO GENERATED. DO NOT EDIT!!!'

		# ini files
		cls.read_full_ini('~/.details.ini')

		# project
		if os.path.isfile('project.ini'):
			cls.read_full_ini('project.ini')
		if 'project_year_started' in cls.__dict__:
			cls.project_copyright_years=', '.join(map(str,range(int(cls.project_year_started), datetime.datetime.now().year+1)))
			if str(cls.general_current_year)==cls.project_year_started:
				cls.project_copyright_years=cls.general_current_year
			else:
				cls.project_copyright_years='{0}-{1}'.format(cls.project_year_started, cls.general_current_year)
		cls.project_name=os.path.basename(os.getcwd())

		if 'project_google_analytics_tracking_id' in cls.__dict__:
			cls.project_google_analytics_snipplet='''<script>
(function(i,s,o,g,r,a,m){{i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){{
(i[r].q=i[r].q||[]).push(arguments)}},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
}})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', '{0}', 'auto');
ga('send', 'pageview');

</script>'''.format(cls.project_google_analytics_tracking_id)

		# git
		try:
			cls.git_describe=subprocess.check_output(['git', 'describe'], stderr=subprocess.DEVNULL).decode().rstrip()
		except:
			cls.git_describe='no git repository'

		# this is wrong for the tag since they may not be alphabetically ordered...
		#tag=subprocess.check_output(['git', 'tag']).decode().rstrip();
		#if tag!='':
		#	cls.git_lasttag=tag.split()[-1].rstrip()
		#else:
		#	cls.git_lasttag='no git tag yet'

		# this is right
		try:
			cls.git_lasttag=subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags'], stderr=subprocess.DEVNULL).decode().rstrip()
		except:
			cls.git_lasttag='no git tag yet'

		# deb
		cls.deb_pkgname=os.path.basename(os.getcwd())
		cls.deb_date='Fri, 21 Jun 2013 09:14:32 +0300'

		# apt
		cls.apt_protocol='https'
		cls.apt_codename=subprocess.check_output(['lsb_release','--codename', '--short']).decode().rstrip()
		cls.apt_arch=subprocess.check_output('dpkg-architecture | grep -e ^DEB_BUILD_ARCH= | cut -d = -f 2', shell=True).decode().rstrip()
		cls.apt_archs='i386 {0} source'.format(cls.apt_arch)
		cls.apt_component='main'
		cls.apt_folder='apt'
		cls.apt_service_dir=os.path.join(cls.general_homedir, 'public_html/public', cls.apt_folder)
		cls.apt_except='50{0}'.format(cls.personal_slug)
		cls.apt_pack_list=glob.glob(os.path.join(cls.general_homedir, 'packages', '*.deb'))
		cls.apt_packlist=' '.join(cls.apt_pack_list)
		cls.apt_id=subprocess.check_output(['lsb_release','--id', '--short']).decode().rstrip()
		cls.apt_keyfile='public_key.gpg'
		cls.apt_apache_site_file='{0}.apt'.format(cls.personal_slug)

	@classmethod
	def getdeps(cls):
		deps=[
			os.path.expanduser('~/.details.ini'),
			'/etc/hostname',
		]
		if os.path.isfile('templardefs/attr.py'):
			deps.append('templardefs/attr.py')
		if os.path.isfile('project.ini'):
			deps.append('project.ini')
		return ' '.join(deps)
