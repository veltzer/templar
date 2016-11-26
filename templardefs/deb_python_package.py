"""
packaging definitions
"""


def populate(d):
    d.entry_points = {
        'console_scripts': [
            'templar_cmd=templar.templar_cmd:main',
            'make_helper=templar.make_helper:main',
        ],
    }


def get_deps():
    return [
        __file__,  # myself
    ]
