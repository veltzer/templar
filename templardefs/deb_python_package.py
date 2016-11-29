"""
packaging definitions
"""


def populate(d):
    d.entry_points = {
        'console_scripts': [
            'templar=templar.cmdline:main',
            'make_helper=templar.make_helper:main',
        ],
    }


def get_deps():
    return [
        __file__,  # myself
    ]
