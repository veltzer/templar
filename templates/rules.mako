#!/usr/bin/make -f

# release the next line to get verbose behaviour
#export DH_VERBOSE=1
#export PYBUILD_NAME=${tdefs.deb_pkgname}

#%%:
#	dh $@ --with python3 --buildsystem=pybuild

clean:
build:
	$(info doing [$@])
	./setup.py build
binary:
	$(info doing [$@])
	./setup.py install --install-layout=deb --root=debian/${tdefs.deb_pkgname}
	dh_installchangelogs
	dh_installdocs
	dh_installexamples
	dh_compress -X.py
	dh_python3
	dh_fixperms
	dh_installdeb
	dh_gencontrol
	dh_builddeb
binary-arch:
build-arch:
binary-indep:
build-indep:
