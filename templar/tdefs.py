'''
Attributes for this project
'''

import datetime # for datetime
import subprocess # for check_output, DEVNULL
import os.path # for join, expanduser, basename, isfile
import os # for getcwd
import glob # for glob
import socket # for gethostname
import templar.utils # for read_full_ini_dict

override_file_name='templar_override.ini'

def populate(d):
	# general # TODO: get homedir in python
	d.general_current_year=datetime.datetime.now().year
	d.general_homedir='/home/mark'
	#d.general_hostname=subprocess.check_output(['hostname']).decode().rstrip()
	d.general_hostname=socket.gethostname()
	d.general_domainname=subprocess.check_output(['hostname','--domain']).decode().rstrip()

	# messages
	d.messages_dne='THIS FILE IS AUTO GENERATED. DO NOT EDIT!!!'

	# details.ini
	ini_file=os.path.expanduser('~/.details.ini')
	if os.path.isfile(ini_file):
		templar.utils.read_full_ini_dict(d, ini_file)

	# project
	if os.path.isfile('project.ini'):
		templar.utils.read_full_ini_dict(d, 'project.ini')

	if 'project_year_started' in d:
		d.project_copyright_years=', '.join(map(str,range(int(d.project_year_started), datetime.datetime.now().year+1)))
		if str(d.general_current_year)==d.project_year_started:
			d.project_copyright_years=d.general_current_year
		else:
			d.project_copyright_years='{0}-{1}'.format(d.project_year_started, d.general_current_year)
	d.current_folder=os.path.basename(os.getcwd())

	if 'project_google_analytics_tracking_id' in d:
		d.project_google_analytics_snipplet='''<script type="text/javascript">
(function(i,s,o,g,r,a,m){{i['GoogleAnalyticsObject=r;i[r]=i[r]||function(){{
(i[r].q=i[r].q||[]).push(arguments)}},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
}})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', '{0}', 'auto');
ga('send', 'pageview');

</script>'''.format(d.project_google_analytics_tracking_id)

	if 'project_paypal_donate_button_id' in d:
		d.project_paypal_donate_button_snipplet='''<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="{0}">
<input type="image" src="https://www.paypalobjects.com/en_US/IL/i/btn/btn_donateCC_LG.gif" name="submit" alt="PayPal - The safer, easier way to pay online!">
<img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
</form>'''.format(d.project_paypal_donate_button_id)

	# git
	try:
		d.git_describe=subprocess.check_output(['git', 'describe'], stderr=subprocess.DEVNULL).decode().rstrip()
	except:
		d.git_describe='no git repository'

	# this is wrong for the tag since they may not be alphabetically ordered...
	#tag=subprocess.check_output(['git', 'tag']).decode().rstrip();
	#if tag!='':
	#	d.git_lasttag=tag.split()[-1].rstrip()
	#else:
	#	d.git_lasttag='no git tag yet'

	# this is right
	try:
		d.git_lasttag=subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags'], stderr=subprocess.DEVNULL).decode().rstrip()
	except:
		d.git_lasttag='no git tag yet'

	# deb
	d.deb_pkgname=os.path.basename(os.getcwd())
	d.deb_date='Fri, 21 Jun 2013 09:14:32 +0300'

	# apt
	d.apt_protocol='https'
	d.apt_codename=subprocess.check_output(['lsb_release','--codename', '--short']).decode().rstrip()
	d.apt_arch=subprocess.check_output('dpkg-architecture | grep -e ^DEB_BUILD_ARCH= | cut -d = -f 2', shell=True).decode().rstrip()
	d.apt_archs='i386 {0} source'.format(d.apt_arch)
	d.apt_component='main'
	d.apt_folder='apt'
	d.apt_service_dir=os.path.join(d.general_homedir, 'public_html/public', d.apt_folder)
	d.apt_except='50{0}'.format(d.personal_slug)
	d.apt_pack_list=glob.glob(os.path.join(d.general_homedir, 'packages', '*.deb'))
	d.apt_packlist=' '.join(d.apt_pack_list)
	d.apt_id=subprocess.check_output(['lsb_release','--id', '--short']).decode().rstrip()
	d.apt_keyfile='public_key.gpg'
	d.apt_apache_site_file='{0}.apt'.format(d.personal_slug)

	if os.path.isfile(override_file_name):
		templar.utils.read_full_ini_dict(d, override_file_name)

def getdeps():
	deps=[
		__file__, # myself
		'/etc/hostname', # for hostname and stuff
	]
	details_file=os.path.expanduser('~/.details.ini')
	if os.path.isfile(details_file):
		deps.append(details_file)
	if os.path.isfile('project.ini'):
		deps.append('project.ini')
	if os.path.isfile(override_file_name):
		deps.append(override_file_name)
	return deps
