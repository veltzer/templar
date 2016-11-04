'''
dependencies for this project
'''

def populate(d):
    d.packs=[
        # for the python scripts
        'python3',
        # for the python scripts
        'python3-all',
        # for packaging helpers
        'dh-python',
        # for packaging
        'python-setuptools-doc',
        # for packaging
        'python3-setuptools',
        # for packaging
        'python-setuptools',
        # for packaging
        'python3-setuptools-git',
        # for packaging
        'python-setuptools-git',
        # mako for python 3 (we are not really using it)
        'python3-mako',
        # documentation for the template preprocessor
        'python-mako-doc',
        # for debuild(1)
        'devscripts',
    ]

def getdeps():
    return [
        __file__, # myself
    ]
