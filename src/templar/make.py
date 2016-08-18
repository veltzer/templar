'''
Module that will run make tasks for you
'''

import templar.subprocess # for check_call

''' make [foo] '''
def make(target):
    templar.subprocess.check_call(['make', target])
