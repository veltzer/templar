"""
this is a specific wrapper written for debuild since it does not have "warnings as errors"
and produces copious amounts of junk as output.
"""
import sys
import templar.capture_all


warning_patterns_to_ignore = {
    'binary-without-manpage',
    'extra-license-file',
    'package-needs-versioned-debhelper-build-depends',
}
error_patterns_to_ignore = {
    'source-contains-unsafe-symlink',
    'missing-dep-for-interpreter',
}


def run(args):
    seen_error = False
    do_errors = True
    lines = [line for line in templar.capture_all.capture_all(args)]
    for line in lines:
        if line.find('warning') != -1:
            seen_error = True
        if line.find('error') != -1:
            seen_error = True
        if line.startswith('E: '):
            for pat in error_patterns_to_ignore:
                if line.find(pat) != -1:
                    break
            else:
                seen_error = True
        if line.startswith('W: '):
            for pat in warning_patterns_to_ignore:
                if line.find(pat) != -1:
                    break
            else:
                seen_error = True
    if seen_error:
        for line in lines:
            print(line, end='')
    if seen_error and do_errors:
        sys.exit(1)
