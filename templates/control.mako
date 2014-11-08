Source: ${tdefs.deb_pkgname}
Maintainer: ${tdefs.personal_origin}
Section: ${tdefs.deb_section}
Priority: ${tdefs.deb_priority}
Build-Depends: python3-all, python3-setuptools, python-all, python-setuptools, debhelper, dh-python
Standards-Version: 3.9.4
# the next line is what makes the package only compile to 3.4 on installation or building
X-Python-Version: >= 3.4
X-Python3-Version: >= 3.4

Package: ${tdefs.deb_pkgname}
Architecture: ${tdefs.deb_architecture} 
Depends: ${"${misc:Depends}"}, ${"${python3:Depends}"}
Description: ${tdefs.project_short_description}
 ${tdefs.project_description}
