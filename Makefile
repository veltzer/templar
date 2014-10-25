##############
# parameters #
##############
# do you want to show the commands executed ?
# Since we are using ?= for assignment it means that you can just
# set this from the command line and avoid changing the makefile...
DO_MKDBG?=0
# version
VER:=$(shell git describe)
# tag
TAG:=$(shell git tag | tail -1)
# name of this package
NAME:=templar
# where to put the package?
REPO:=~/packages
# where to build full packages?
BUILD.ALL:=build.full
# where to build source packages?
BUILD.SOURCE:=build.source
# where to build source packages?
BUILD.GBP:=build.gbp
# my ppa
PPA:=ppa:mark-veltzer/ppa

########
# code #
########
# silent stuff
ifeq ($(DO_MKDBG),1)
Q:=
# we are not silent in this branch
else # DO_MKDBG
Q:=@
#.SILENT:
endif # DO_MKDBG

PKG_TIGHT:=$(NAME)_$(TAG)
PKG_BASE:=$(PKG_TIGHT)_all
PKG:=$(PKG_BASE).deb
PKG_FULL:=$(REPO)/$(PKG)
PKG_CHANGES:=$(PKG_TIGHT)_source.changes

#########
# rules #
#########
.PHONY: all
all:
	$(info tell me what you want to do)

# source

.PHONY: source-debug
source-debug:
	$(info doing [$@])
	$(info VER is $(VER))
	$(info TAG is $(TAG))
	$(info NAME is $(NAME))
	$(info PKG_TIGHT is $(PKG_TIGHT))
	$(info PKG_BASE is $(PKG_BASE))
	$(info PKG is $(PKG))
	$(info PKG_FULL is $(PKG_FULL))
	$(info PKG_CHANGES is $(PKG_CHANGES))
	$(info REPO is $(REPO))

.PHONY: source-build
source-build:
	$(info doing [$@])
	$(Q)setup.py build

.PHONY: source-install
source-install:
	$(info doing [$@])
	$(Q)setup.py install

.PHONY: source-clean
source-clean:
	$(info doing [$@])
	$(Q)git clean -xdf

.PHONY: source-sdist
source-sdist:
	$(info doing [$@])
	$(Q)setup.py sdist

# deb

.PHONY: deb-build-all
deb-build-all: deb-build-gbp deb-build-debuild-all deb-build-debuild-source

.PHONY: deb-build-gbp
deb-build-gbp:
	$(info doing [$@])
	$(Q)rm -f ../$(NAME)_*
	$(Q)git clean -xdf > /dev/null
	$(Q)-mkdir $(BUILD.GBP)
	$(Q)git-buildpackage > /tmp/git-buildpackage.log
	$(Q)mv ../$(NAME)_* $(BUILD.GBP)
	$(Q)chmod 444 $(BUILD.GBP)/$(NAME)_*

.PHONY: deb-build-debuild-all
deb-build-debuild-all:
	$(info doing [$@])
	$(Q)rm -f ../$(NAME)_*
	$(Q)git clean -xdf > /dev/null
	$(Q)-mkdir $(BUILD.ALL)
	$(Q)debuild -S > /tmp/debuild_s.log
	$(Q)mv ../$(NAME)_* $(BUILD.ALL)
	$(Q)chmod 444 $(BUILD.ALL)/$(NAME)_*

.PHONY: deb-build-debuild-source
deb-build-debuild-source:
	$(info doing [$@])
	$(Q)rm -f ../$(NAME)_*
	$(Q)git clean -xdf > /dev/null
	$(Q)-mkdir $(BUILD.SOURCE)
	$(Q)debuild -S > /tmp/debuild.log
	$(Q)mv ../$(NAME)_* $(BUILD.SOURCE)
	$(Q)chmod 444 $(BUILD.SOURCE)/$(NAME)_*

.PHONY: deb-dput
deb-dput:
	$(info doing [$@])
	$(Q)dput $(PPA) $(BUILD.SOURCE)/$(PKG_CHANGES)

.PHONY: deb-install
deb-install:
	$(info doing [$@])
	$(Q)sudo dpkg --install $(PKG_FULL)

.PHONY: deb-contents
deb-contents:
	$(info doing [$@])
	$(Q)dpkg --contents $(PKG_FULL)

.PHONY: deb-info
deb-info:
	$(info doing [$@])
	$(Q)dpkg --info $(PKG_FULL)

.PHONY: deb-all
deb-all: deb-contents deb-info

# installed

.PHONY: installed-listfiles
installed-listfiles:
	$(info doing [$@])
	$(Q)dpkg --listfiles $(NAME)

.PHONY: installed-purge
installed-purge:
	$(info doing [$@])
	$(Q)sudo dpkg --purge $(NAME)

#################
# python checks #
#################
.PHONY: check_main
check_main:
	$(info doing [$@])
	$(Q)-git grep __main -- "*.py"
.PHONY: check_semicol
check_semicol:
	$(info doing [$@])
	$(Q)-git grep ";$$" -- "*.py"

.PHONY: check_all
check_all: check_main check_semicol
	$(info doing [$@])
