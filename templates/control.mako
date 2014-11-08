Source: ${tdefs.deb_pkgname}
Maintainer: ${tdefs.personal_origin}
Section: ${tdefs.deb_section}
Priority: ${tdefs.deb_priority}
Build-Depends: ${tdefs.deb_builddepends}
Standards-Version: ${tdefs.deb_standards_version}
# the next line is what makes the package only compile to 3.4 on installation or building
X-Python-Version: >= ${tdefs.deb_x_python_version}
X-Python3-Version: >= ${tdefs.deb_x_python3_version}
Vcs-Git: ${tdefs.project_website_git}
Vcs-Browser: ${tdefs.project_website_source}

Package: ${tdefs.deb_pkgname}
Architecture: ${tdefs.deb_architecture} 
Depends: ${tdefs.deb_depends}
Description: ${tdefs.project_short_description}
 ${tdefs.project_description}
