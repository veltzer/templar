"""
Module that knows how to run dpkg(1)

TODO:
- use a python package to interface dpkg here.
"""

import templar.subprocess
import os.path


def install(d):
    templar.subprocess.check_call([
        'sudo',
        'dpkg',
        '--install',
        os.path.join(d.deb_out_folder, '{0}_{1}_{2}.deb'.format(
            d.deb_pkgname,
            d.deb_version,
            d.deb_architecture,
        )),
    ])
