TEMPLAR_TEMPLAR_SCRIPT:=./src/templar_cmd
TEMPLAR_MAKEHELPER_SCRIPT:=./src/make_helper
include make/Makefile

ALL:=$(TEMPLAR_ALL)
ALL_DEP:=$(TEMPLAR_ALL_DEP)

##############
# parameters #
##############
# do you want to show the commands executed ?
DO_MKDBG:=0

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
.DEFAULT_GOAL=all
.PHONY: all
all: $(ALL)

.PHONY: clean
clean:
	$(info doing [$@])
	$(Q)git clean -xdf > /dev/null

.PHONY: deb-debug
deb-debug:
	$(info doing [$@])

# checks

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

# package building

.PHONY: deb-build-gbp
deb-build-gbp:
	$(info doing [$@])
	$(Q)./src/make_helper debuild --gbp

.PHONY: deb-build-debuild-all
deb-build-debuild-all:
	$(info doing [$@])
	$(Q)./src/make_helper debuild

.PHONY: deb-build-debuild-source
deb-build-debuild-source:
	$(info doing [$@])
	$(Q)./src/make_helper debuild --source

.PHONY: deb-release
deb-release:
	$(info doing [$@])
	$(Q)./src/make_helper release

.PHONY: deb-install
deb-install:
	$(info doing [$@])
	$(Q)./src/make_helper debuild-install
