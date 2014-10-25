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
TAG:=$(shell git tag)
# name of this package
NAME:=templar
# where to put the package?
REPO:=~/packages

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

PKG:=$(NAME)_$(TAG)_all.deb
PKG_FULL:=$(REPO)/$(PKG)

#########
# rules #
#########
.PHONY: all
all: deb-build

# source

.PHONY: source-debug
source-debug:
	$(info doing [$@])
	$(info VER is $(VER))
	$(info TAG is $(TAG))
	$(info NAME is $(NAME))
	$(info PKG is $(PKG))
	$(info PKG_FULL is $(PKG_FULL))
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

.PHONY: deb-build
deb-build:
	$(info doing [$@])
	$(Q)rm -f ../$(NAME)_* $(REPO)/$(REPO)/$(NAME)_*
	$(Q)git clean -xdf > /dev/null
	$(Q)git-buildpackage > /tmp/git-buildpackage.log
	$(Q)mv ../$(NAME)_* $(REPO)
	$(Q)chmod 444 $(REPO)/$(NAME)_*

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
