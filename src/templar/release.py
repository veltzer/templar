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
def set_tag(d, tag):
	d.git_lasttag=tag
	d.git_version=d.git_lasttag
	d.deb_version='{0}~{1}'.format(d.git_version, d.apt_codename)

def set_codename(d, apt_codename):
	d.apt_codename=apt_codename
	set_tag(d, d.git_lasttag)

def set_codename_tag(d, apt_codename, tag):
	d.apt_codename=apt_codename
	set_tag(d, tag)

def run(d):
	# check that everything is committed
	templar.git.check_allcommit()

	# calculate the new tag and setup data
	tag=str(int(d.git_lasttag)+1)
	set_tag(d, tag)

	# build everything
	templar.api.process(d, templar.utils.pkg_get_real_filename(__file__, 'templates/README.md.mako'), 'README.md')

	# commit the README.md file which was just changed because it contains the version number.
	# this is a little ugly since I'm not really sure if the README.md was changed.
	# I should really check if there are changes and only then commit.
	templar.git.commit_all('release '+tag)

	# create the tag
	templar.git.tag(tag)

	# push new version
	templar.git.push(True)

	if not d.deb_package:
		return

	for series in d.deb_series:
		templar.debug.debug('starting to build for series [{0}]'.format(series))
		set_codename(d, series)
		templar.debuild.run(d, True, False)
		templar.dput.run(d)
