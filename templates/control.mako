Source: ${attr.deb_pkgname}
Maintainer: ${attr.personal_origin}
Section: python
Priority: optional
Build-Depends: python3, debhelper
Standards-Version: 3.9.4
X-Python3-Version: >= 3.4

Package: ${attr.deb_pkgname}
Architecture: all
Depends: ${"${misc:Depends}"}, ${"${python:Depends}"}
Description: ${attr.project_short_description}
 ${attr.project_description}
