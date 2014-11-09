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
import templar.make # for make
import templar.fileops # for touch_exists
import templar.debug # for debug

##############
# parameters #
##############
# do you want to check if everything is commited ? Answer True to this
# unless you are doing development on this script...
opt_check=True

#############
# functions #
#############
env_var='TEMPLAR_OVERRIDE'
def create_override_env(series):
	os.environ[env_var]='apt_codename={0}'.format(series)

def remove_override_env():
	del os.environ[env_var]

override_file_name='/tmp/templar_override.ini'
def create_override_file(series):
	with open(override_file_name, 'w') as f:
		print('[apt]', file=f)
		print('codename={0}'.format(series), file=f)

def remove_override_file():
	os.unlink(override_file_name)

old_val=None
def create_override(d, series):
	old_val=d.apt_codename
	d.apt_codename=series
	create_override_env(series)

def remove_override(d):
	d.apt_codename=old_val
	remove_override_env()

def run(d):
	# check that everything is committed
	templar.git.check_allcommit()

	# tag the new version
	tag=str(int(d.git_lasttag)+1)
	templar.git.tag(tag)
	# very hard clean
	templar.git.clean()
	# touch the Makefile so that everything gets regenerated
	# (esp templar stuff which may think they are up to date, they are not!
	# since the tag has changed)
	templar.fileops.touch_exists('Makefile')
	# build everything
	templar.make.make('templar')
	# commit the files which have been changed (FIXME: only do this if there were changes, currently there are)
	templar.git.commit_all(tag)
	# push new version
	templar.git.push()

	for series in d.deb_series.split():
		templar.debug.debug('starting to build for series [{0}]'.format(series))
		create_override(d, series)
		templar.debuild.run(d)
		remove_override(d)
