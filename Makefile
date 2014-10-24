##############
# parameters #
##############
# do you want to show the commands executed ?
# Since we are using ?= for assignment it means that you can just
# set this from the command line and avoid changing the makefile...
DO_MKDBG?=0
# version
VER:=$(shell git describe)
# name of this package
NAME:=templar

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

#########
# rules #
#########

.PHONY: all
all: deb

.PHONY: debug
debug:
	$(info doing [$@])
	$(info VER is $(VER))
	$(info NAME is $(NAME))

.PHONY: build
build:
	$(info doing [$@])
	$(Q)setup.py build

.PHONY: install
install:
	$(info doing [$@])
	$(Q)setup.py install

.PHONY: clean
clean:
	$(info doing [$@])
	$(Q)git clean -xdf

.PHONY: sdist
sdist:
	$(info doing [$@])
	$(Q)setup.py sdist

.PHONY: deb
deb:
	$(info doing [$@])
	$(Q)rm -f ../$(NAME)-* ../$(NAME)_*
	$(Q)git clean -xdf
	$(Q)#git-buildpackage --git-ignore-new
	$(Q)git-buildpackage
	$(Q)mv ../$(NAME)_* ~/packages/

.PHONY: install-deb
install-deb:
	$(info doing [$@])
	$(Q)sudo dpkg --install deb_dist/$(NAME)_$(VER)_all.deb

.PHONY: installed-listfiles
installed-listfiles:
	$(info doing [$@])
	$(Q)dpkg --listfiles $(NAME)

.PHONY: installed-purge
installed-purge:
	$(info doing [$@])
	$(Q)sudo dpkg --purge $(NAME)

.PHONY: deb-contents
deb-contents:
	$(info doing [$@])
	$(Q)dpkg --contents ~/packages/$(NAME)_$(VER)_all.deb

.PHONY: deb-info
deb-info:
	$(info doing [$@])
	$(Q)dpkg --info ~/packages/$(NAME)_$(VER)_all.deb

.PHONY: deb-all
deb-all: deb-contents deb-info

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
