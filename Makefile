TEMPLAR_TEMPLAR_SCRIPT:=./src/templar_cmd
TEMPLAR_MAKEHELPER_SCRIPT:=./src/make_helper
include make/Makefile.templar
include make/Makefile.package_build
include make/Makefile.toplevel
include make/Makefile.check_py
include make/Makefile.debug
