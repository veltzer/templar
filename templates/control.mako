Source: ${tdefs.deb_pkgname}
Maintainer: ${tdefs.personal_origin}
Section: python
Priority: optional
Build-Depends: python3-all, python3-setuptools, python-all, python-setuptools, debhelper, dh-python
Standards-Version: 3.9.4
X-Python3-Version: >= 3.4

Package: ${tdefs.deb_pkgname}
Architecture: all
Depends: ${"${misc:Depends}"}, ${"${python3:Depends}"}
Description: ${tdefs.project_short_description}
 ${tdefs.project_description}
