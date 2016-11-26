"""
Module that will run git tasks for you

TODO:
- implement this better with GitPython (a python module to interact with git for you).
"""

import sys
import templar.subprocess


def clean():
    """ git clean -xdf > /dev/null """
    templar.subprocess.check_call(['git', 'clean', '-xdf'])


def is_allcommit():
    """ function that reports if all is comitted """
    out = templar.subprocess.check_output(['git', 'status', '-s']).decode()
    return out == ''


def check_allcommit():
    """ function that checks that all is committed """
    if not is_allcommit():
        print('first commit everything, then call me...', file=sys.stderr)
        sys.exit(1)


def commit_all(msg):
    templar.subprocess.check_call(['git', 'commit', '--all', '-m', msg])


def push(tags):
    args = ['git', 'push', ]
    if tags:
        args.append('--follow-tags')
        # args.append('--tags')
    templar.subprocess.check_call(args)


def tag(tag_name):
    templar.subprocess.check_call(['git', 'tag', '--annotate', '--sign', '-m', tag_name, tag_name])


def git_config(d):
    print('config is ', d['personal_key'])
    print('config is ', d['core_editor'])
    print('config is ', d['personal_fullname'])
    print('config is ', d['personal_email'])
