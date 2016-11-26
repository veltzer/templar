TEMPLAR_TEMPLAR_SCRIPT:=PYTHONPATH=src; python3 -m templar.templar_cmd
TEMPLAR_MAKEHELPER_SCRIPT:=PYTHONPATH=src; python3 -m templar.make_helper
include make/Makefile.debug
include make/Makefile.templar
include make/Makefile.package_build
include make/Makefile.top_level
include make/Makefile.check_py
