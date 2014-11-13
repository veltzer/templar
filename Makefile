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

# general

.DEFAULT_GOAL=all
.PHONY: all
all: $(ALL)
	$(info doing [$@])

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

.PHONY: debuild-gbp
debuild-gbp:
	$(info doing [$@])
	$(Q)$(TEMPLAR_MAKEHELPER_SCRIPT) debuild --gbp

.PHONY: debuild
debuild:
	$(info doing [$@])
	$(Q)$(TEMPLAR_MAKEHELPER_SCRIPT) debuild

.PHONY: debuild-source
debuild-source:
	$(info doing [$@])
	$(Q)$(TEMPLAR_MAKEHELPER_SCRIPT) debuild --source

.PHONY: release
release:
	$(info doing [$@])
	$(Q)$(TEMPLAR_MAKEHELPER_SCRIPT) release

.PHONY: debuild-install
debuild-install:
	$(info doing [$@])
	$(Q)$(TEMPLAR_MAKEHELPER_SCRIPT) debuild-install
