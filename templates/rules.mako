#!/usr/bin/make -f

export DH_VERBOSE=1
export PYBUILD_NAME=${tdefs.deb_pkgname}

%%:
	dh $@ --with python2,python3 --buildsystem=pybuild
