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
TEMPLAR_TEMPLAR_SCRIPT:=scripts/templar_cmd.py
# quiet or not?
TEMPLAR_Q=@
# folder where templar files are
TEMPLAR_TEMPLAR_FOLDER:=templar

########
# code #
########
TEMPLAR_TMPL_FILE_DEPS:=$(shell $(TEMPLAR_TEMPLAR_SCRIPT) getdeps)
# the - (minus) at the begining of the next line is so that users wont see
# an error coming out of make when the file needs to be rebuilt...
-include $(TEMPLAR_TMPL_FILE)

# prep sources and targets
TEMPLAR_ALL_MAKO_SRC:=$(shell find $(TEMPLAR_TEMPLAR_FOLDER) -type f -and -name "*.mako" 2> /dev/null)
TEMPLAR_ALL_MAKO_TGT:=$(shell scripts/remove_first_dir_and_suffix.py $(TEMPLAR_ALL_MAKO_SRC))

TEMPLAR_ALL_DEP:=$(MAKEFILE_LIST)
#TEMPLAR_ALL_DEP:=$(TEMPLAR_TMPL_FILE) $(TEMPLAR_MAKEFILE)
TEMPLAR_ALL:=$(TEMPLAR_ALL_MAKO_TGT)

###########
# targets #
###########
.PHONY: debug_prep
debug_prep:
	$(info TEMPLAR_MAKEFILE is $(TEMPLAR_MAKEFILE))
	$(info TEMPLAR_TMPL_FILE is $(TEMPLAR_TMPL_FILE))
	$(info TEMPLAR_TMPL_FILE_DEPS is $(TEMPLAR_TMPL_FILE_DEPS))
	$(info TEMPLAR_ALL_MAKO_SRC is $(TEMPLAR_ALL_MAKO_SRC))
	$(info TEMPLAR_ALL_MAKO_TGT is $(TEMPLAR_ALL_MAKO_TGT))
	$(info TEMPLAR_ALL is $(TEMPLAR_ALL))

# rule about creating the template file
# it should not depend on ALL_DEP_PREP since ALL_DEP_PREP includes it and this will create circular dependency
$(TEMPLAR_TMPL_FILE): $(TEMPLAR_TEMPLAR_SCRIPT) $(TEMPLAR_TMPL_FILE_DEPS)
	$(info doing [$@])
	$(TEMPLAR_Q)$(TEMPLAR_TEMPLAR_SCRIPT) printmake > $@

.PHONY: prep
prep: $(TEMPLAR_ALL_MAKO_TGT)

#################
# pattern rules #
#################
$(TEMPLAR_ALL_MAKO_TGT): %: $(TEMPLAR_TEMPLAR_FOLDER)/%.mako $(TEMPLAR_TMPL_FILE_DEPS) $(ALL_DEP_PREP)
	$(info doing [$@])
	$(TEMPLAR_Q)$(TEMPLAR_TEMPLAR_SCRIPT) process --input $< --output $@
