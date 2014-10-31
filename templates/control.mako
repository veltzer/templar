Source: ${attr.deb_pkgname}
Maintainer: ${attr.personal_origin}
Section: python
Priority: optional
Build-Depends: python3-all, python3-setuptools, python-all, python-setuptools, debhelper, dh-python, python-support
Standards-Version: 3.9.4
X-Python3-Version: >= 3.4

Package: ${attr.deb_pkgname}
Architecture: all
Depends: ${"${misc:Depends}"}, ${"${python3:Depends}"}
Description: ${attr.project_short_description}
 ${attr.project_description}
