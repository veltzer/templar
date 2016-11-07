'''
packging definitions
'''

def populate(d):
    d.entry_points={
        'console_scripts': [
            'templar_cmd=templar.templar_cmd:cli',
            'make_helper=templar.make_helper:cli',
        ],
    }

def getdeps():
    return [
        __file__, # myself
    ]
