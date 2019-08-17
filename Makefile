TEMPLAR_TEMPLAR_SCRIPT:=python3 -m templar.cmdline
TEMPLAR_MAKEHELPER_SCRIPT:=python3 -m templar.make_helper
include make/Makefile.debug
include make/Makefile.templar
include make/Makefile.package_build
include make/Makefile.top_level
include make/Makefile.check_py
