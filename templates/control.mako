Source: templar
Maintainer: ${attr.personal_origin}
Section: python
Priority: optional
Build-Depends: python3, debhelper
Standards-Version: 3.9.4
X-Python3-Version: >= 3.4

Package: templar
Architecture: all
Depends: ${"${misc:Depends}"}, ${"${python3:Depends}"}
Description: Easy templating tool
 Easy templating tool long description
