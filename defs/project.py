'''
project definitions for templar
'''

import templar.utils # for hlp_files_under

def populate(d):
    # project section
    d.project_github_username='veltzer'
    d.project_name='templar'
    d.project_website='https://{project_github_username}.github.io/{project_name}'.format(**d)
    d.project_website_source='https://github.com/{project_github_username}/{project_name}'.format(**d)
    d.project_website_git='git://github.com/{project_github_username}/{project_name}.git'.format(**d)
    d.project_website_download='https://launchpad.net/~mark-veltzer/+archive/ubuntu/ppa'
    d.project_paypal_donate_button_id='YSQSL83L4GK4Q'
    d.project_google_analytics_tracking_id='UA-81412152-1'

    d.project_short_description='Easy templating tool'
    d.project_description='Easy templating tool long description (TBD)'
    d.project_long_description='Templating solution for programmers'
    d.project_year_started='2014'
    d.project_keywords=[
        'mako',
        'templating',
        'python',
    ]
    d.project_platforms=[
        'ALL',
    ]
    d.project_license='LGPL'
    d.project_classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: LGPL',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Building',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ]
    d.project_data_files=[]
    d.project_data_files.append(templar.utils.hlp_files_under('/usr/share/templar/make', 'make/*'))
    #d.project_data_files.append(templar.utils.hlp_files_under('/usr/share/templar/templartmpl', 'templates/*.mako'))
    d.project_data_files.append(templar.utils.hlp_files_under('/usr/share/templar/templardefs', 'defs/*.py'))
    d.project_data_files.append(templar.utils.hlp_files_under('/usr/bin', 'src/*'))
    d.project_data_files.append(templar.utils.hlp_files_under('/usr/lib/python3/dist-packages/templar/templates', 'src/templar/templates/*.mako'))

    # deb section
    d.deb_package=True
    d.deb_section='python'
    d.deb_priority='optional'
    d.deb_architecture='all'
    d.deb_pkgname='templar'
    # to which series to publish the package?
    d.deb_series=[
        'xenial',
        'wily',
        'vivid',
        # end of life
        #'utopic',
        'trusty',
        # does not accept new uploads
        #'saucy',
        # does not accept new uploads
        #'raring',
    ]
    # these are dependencies for runtime
    d.deb_depends='${misc:Depends}, ${python3:Depends}, python3-mako'
    # these are dependencies for buildtime at launchpad ppa
    d.deb_builddepends='python3-all, python3-setuptools, python3-setuptools, debhelper, dh-python'
    d.deb_standards_version='3.9.6'
    #d.deb_standards_version='3.9.5'
    d.deb_x_python_version='>= 3.4'
    d.deb_x_python3_version='>= 3.4'
    d.deb_urgency='low'

def getdeps():
    return [
        __file__, # myself
    ]
