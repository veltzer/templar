#############
# Variables #
#############
# do you want to show the commands executed ?
# Since we are using ?= for assignment it means that you can just
# set this from the command line and avoid changing the makefile...
DO_MKDBG?=0
# version
VER:=$(shell git describe)
# name of this package
NAME:=templar

#########
# Logic #
#########
# silent stuff
ifeq ($(DO_MKDBG),1)
Q:=
# we are not silent in this branch
else # DO_MKDBG
Q:=@
#.SILENT:
endif # DO_MKDBG

#########
# Rules #
#########

.PHONY: all
all: deb

.PHONY: debug
debug:
	$(info VER is $(VER))

.PHONY: build
build:
	./setup.py build

.PHONY: install
install:
	./setup.py install

.PHONY: clean_old
clean_old:
	rm -rf `find . -name "*.pyc"` `find . -name "*.o"` `find . -name "*.elf"`
	rm -rf build dist deb_dist

.PHONY: clean
clean:
	git clean -xdf

.PHONY: sdist
sdist:
	./setup.py sdist

.PHONY: debianize
debianize:
	\rm -rf debian/source
	python2 ./setup.py --command-packages=stdeb.command debianize

.PHONY: deb2
deb2:
	$(error dont use this)
	rm -f ../$(NAME)-* ../$(NAME)_*
	git clean -xdf
	python setup.py sdist --dist-dir=../ --prune
#	python setup.py sdist --dist-dir=../
	dpkg-buildpackage -i -I -rfakeroot

.PHONY: deb
deb:
	rm -f ../$(NAME)-* ../$(NAME)_*
	git clean -xdf
	git-buildpackage --git-ignore-new
	mv ../$(NAME)_* ~/packages/

.PHONY: install-deb
install-deb:
	sudo dpkg --install deb_dist/$(NAME)_$(VER)_all.deb

.PHONY: listfiles
listfiles:
	dpkg --listfiles $(NAME)
.PHONY: purge
purge:
	sudo dpkg --purge $(NAME)
.PHONY: results
results:
	dpkg --contents ~/packages/$(NAME)_$(VER)_all.deb
	dpkg --info ~/packages/$(NAME)_$(VER)_all.deb

.PHONY: check_main
check_main:
	@-git grep __main -- "*.py"
.PHONY: check_semicol
check_semicol:
	@-git grep ";$$" -- "*.py"

.PHONY: check_all
check_all: check_main check_semicol
