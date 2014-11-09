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
import subprocess # for check_call, DEVNULL
import sys # for stderr
import os # for environ, unlink
import glob # for glob
import templar.git # for check_allcommit, clean
import templar.make # for make

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

def remove_override(d):
	d.apt_codename=old_val

def run(d):
	# check that everything is committed
	templar.git.check_allcommit()

	# tag the new version
	tag=str(int(d.git_lasttag)+1)
	templar.git.tag(tag)
	# build and commit for templating files that have the version in them
	templar.git.clean()
	templar.make.make('templar')
	templar.git.commit_all(tag)
	templar.git.push()

	for series in d.deb_series.split():
		print('starting to build for series [{0}]'.format(series), file=sys.stderr)
		create_override(d, series)
		templar.debuild.run(d)
		print('results are {0}'.format(glob.glob('build.source/*'), file=sys.stderr)
		remove_override()
