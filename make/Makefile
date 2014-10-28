#########################
# must be done at start #
#########################
# this makefile's name. if you do this after including other stuff you will get
# the names of the stuff you include
TEMPLAR_MAKEFILE:=$(lastword $(MAKEFILE_LIST))
##############
# parameters #
##############
# the template file to be created
TEMPLAR_TMPL_FILE:=.attr.config
# what is the templar script?
TEMPLAR_TEMPLAR_SCRIPT?=/usr/bin/templar_cmd.py
# what is the make helper script?
TEMPLAR_MAKEHELPER_SCRIPT?=/usr/bin/make_helper.py
# quiet or not?
TEMPLAR_Q=@
# folder where templar files are
TEMPLAR_TEMPLAR_FOLDER:=templartmpl
# do we want security?
TEMPLAR_SEC?=1

########
# code #
########
TEMPLAR_TMPL_EXTRA_DEPS:=$(shell $(TEMPLAR_TEMPLAR_SCRIPT) getdeps)
# the - (minus) at the begining of the next line is so that users wont see
# an error coming out of make when the file needs to be rebuilt...
-include $(TEMPLAR_TMPL_FILE)

TEMPLAR_TEMPLAR_SCRIPT_ARGS:=
ifeq ($(TEMPLAR_SEC), 0)
TEMPLAR_TEMPLAR_SCRIPT_ARGS+=--nosec
endif

# templar sources and targets
TEMPLAR_ALL_MAKO_SRC:=$(shell find $(TEMPLAR_TEMPLAR_FOLDER) -type f -or -type l -and -name "*.mako" 2> /dev/null)
TEMPLAR_ALL_MAKO_TGT:=$(shell $(TEMPLAR_MAKEHELPER_SCRIPT) rmfdas $(TEMPLAR_ALL_MAKO_SRC))

# MAKEFILE_LIST includes included makefiles like TEMPLAR_TMPL_FILE above...
TEMPLAR_ALL_DEP:=$(MAKEFILE_LIST) $(TEMPLAR_TMPL_EXTRA_DEPS)
#TEMPLAR_ALL_DEP:=$(TEMPLAR_TMPL_FILE) $(TEMPLAR_MAKEFILE)
TEMPLAR_ALL:=$(TEMPLAR_ALL_MAKO_TGT)

###########
# targets #
###########
.PHONY: templar_debug
templar_debug:
	$(info TEMPLAR_MAKEFILE is $(TEMPLAR_MAKEFILE))
	$(info TEMPLAR_TMPL_FILE is $(TEMPLAR_TMPL_FILE))
	$(info TEMPLAR_TMPL_EXTRA_DEPS is $(TEMPLAR_TMPL_EXTRA_DEPS))
	$(info TEMPLAR_ALL_MAKO_SRC is $(TEMPLAR_ALL_MAKO_SRC))
	$(info TEMPLAR_ALL_MAKO_TGT is $(TEMPLAR_ALL_MAKO_TGT))
	$(info TEMPLAR_ALL is $(TEMPLAR_ALL))
	$(info TEMPLAR_ALL_DEP is $(TEMPLAR_ALL_DEP))
	$(info TEMPLAR_TEMPLAR_SCRIPT is $(TEMPLAR_TEMPLAR_SCRIPT))
	$(info TEMPLAR_MAKEHELPER_SCRIPT is $(TEMPLAR_MAKEHELPER_SCRIPT))
	$(info TEMPLAR_SEC is $(TEMPLAR_SEC))

# rule about creating the template file
# it should not depend on TEMPLAR_ALL_DEP since TEMPLAR_ALL_DEP includes it and this will create circular dependency
$(TEMPLAR_TMPL_FILE): $(TEMPLAR_TEMPLAR_SCRIPT) $(TEMPLAR_TMPL_EXTRA_DEPS)
	$(info doing [$@])
	$(TEMPLAR_Q)$(TEMPLAR_TEMPLAR_SCRIPT) printmake $(TEMPLAR_TEMPLAR_SCRIPT_ARGS) > $@

.PHONY: templar
templar: $(TEMPLAR_ALL_MAKO_TGT)

#################
# pattern rules #
#################
$(TEMPLAR_ALL_MAKO_TGT): %: $(TEMPLAR_TEMPLAR_FOLDER)/%.mako $(TEMPLAR_ALL_DEP)
	$(info doing [$@])
	$(TEMPLAR_Q)$(TEMPLAR_TEMPLAR_SCRIPT) process --input $< --output $@
