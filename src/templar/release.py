'''
this is a release module.
it runs git status -s in order to see that everything is commited.
it then tags the current tree with one + the old tag.
it then cleans and then rebuilds everything and puts the results in the output.

TODO:
- iterate all series wanted by the developer and release for all of them.
- add integration with twitter and facebook to announce new versions.
- try to use a better git interface (there are native python git interfaces).
'''

###########
# imports #
###########
import os # for environ, unlink
import templar.git # for check_allcommit, clean
import templar.fileops # for touch_exists
import templar.debug # for debug
import templar.dput # for run
import templar.debuild # for run
import templar.api # for process
import templar.utils # for pkg_get_real_filename

##############
# parameters #
##############
# do you want to check if everything is commited ? Answer True to this
# unless you are doing development on this script...
opt_check=True

#############
# functions #
#############
override_file_name='/tmp/templar_override.ini'
def create_override_file(series):
	with open(override_file_name, 'w') as f:
		print('[apt]', file=f)
		print('codename={0}'.format(series), file=f)

def remove_override_file():
	os.unlink(override_file_name)

env_var='TEMPLAR_OVERRIDE'
def create_override_env(d):
	os.environ[env_var]='apt_codename={apt_codename};deb_version={deb_version}'.format(**d)

def remove_override_env():
	del os.environ[env_var]

def create_override(d, apt_codename, deb_version):
	d.old_apt_codename=d.apt_codename
	d.apt_codename=apt_codename
	d.old_deb_version=d.deb_version
	d.deb_version=deb_version
	#create_override_env(d)

def remove_override(d):
	d.apt_codename=d.old_apt_codename
	d.deb_version=d.old_deb_version
	#remove_override_env()

def run(d):
	# check that everything is committed
	templar.git.check_allcommit()

	# tag the new version
	tag=str(int(d.git_lasttag)+1)
	templar.git.tag(tag)
	d.git_lasttag=tag
	d.git_version=d.git_lasttag
	d.deb_version='{0}~{1}'.format(d.git_version, d.apt_codename)
	# very hard clean
	templar.git.clean()
	# touch the Makefile so that everything gets regenerated
	# (esp templar stuff which may think they are up to date, they are not!
	# since the tag has changed)
	templar.fileops.touch_exists('Makefile')
	# build everything
	templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/README.md.mako'), 'README.md')
	# commit the files which have been changed (FIXME: only do this if there were changes, currently there are)
	# the tag here is just a message, not a tag
	templar.git.commit_all(tag)
	# push new version
	templar.git.push(True)

	for series in d.deb_series:
		templar.debug.debug('starting to build for series [{0}]'.format(series))
		create_override(d, series, '{0}~{1}'.format(d.git_version, series))
		templar.debuild.run(d, True, False)
		templar.dput.run(d)
		remove_override(d)
	# wrap up - bring the folder back to regular business
	# very hard clean
	templar.git.clean()
	#templar.fileops.touch_exists('Makefile')
	#templar.make.make('templar')
