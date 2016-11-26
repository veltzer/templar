"""
Module that knows how to run dput(1)

dput(1) uploads your package to debian/ubuntu.
The weird thing about dput(1) is that you just point it to the '.changes'
file of your generated package and it takes care of the rest.
"""

import templar.subprocess  # for check_call
import os.path  # for join

do_dput = True


def run(d):
    if do_dput:
        templar.subprocess.check_call([
            'dput',
            # '--debug',
            d.launchpad_ppa,
            os.path.join(d.deb_out_folder, '{0}_{1}_source.changes'.format(d.deb_pkgname, d.deb_version)),
        ])
