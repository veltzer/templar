"""
Make is really bad at doing text processing. So the idea is to help make out
by supplying a python script which does the heavy lifting and keep the make code
clean and simple.
"""

import os.path
import os
import argparse
import templar.api
import templar.debuild
import templar.release
import templar.dpkg
import templar.wrappers.css_validator
import templar.wrappers.debuild
import templar.wrappers.noerr
import templar.wrappers.ok
import templar.wrappers.silent
import templar.wrappers.shell_noerr
import templar.fileops


def main():
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(
            title='sub_commands',
            dest='sub_command',
    )

    sub_parser_remove_folders = subparsers.add_parser(
            'remove-folders',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_remove_folders.add_argument('filenames', nargs=argparse.REMAINDER, action='store')

    sub_parser_remove_folder = subparsers.add_parser(
            'remove-folder',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_remove_folder.add_argument('filenames', nargs=argparse.REMAINDER, action='store')

    sub_parser_debuild = subparsers.add_parser(
            'debuild',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_debuild.add_argument('--source', help='create only source packages', default=False, action='store_true')
    sub_parser_debuild.add_argument('--gbp', help='use git build package', default=False, action='store_true')

    subparsers.add_parser(
            'debuild-install',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers.add_parser(
            'release',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    sub_parser_wrapper_css_validator = subparsers.add_parser(
            'wrapper-css-validator',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_wrapper_css_validator.add_argument('args', nargs=argparse.REMAINDER, action='store')

    sub_parser_wrapper_debuild = subparsers.add_parser(
            'wrapper-debuild',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_wrapper_debuild.add_argument('args', nargs=argparse.REMAINDER, action='store')

    sub_parser_wrapper_noerr = subparsers.add_parser(
            'wrapper-noerr',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_wrapper_noerr.add_argument('args', nargs=argparse.REMAINDER, action='store')

    sub_parser_wrapper_ok = subparsers.add_parser(
            'wrapper-ok',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_wrapper_ok.add_argument('args', nargs=argparse.REMAINDER, action='store')

    sub_parser_wrapper_silent = subparsers.add_parser(
            'wrapper-silent',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_wrapper_silent.add_argument('args', nargs=argparse.REMAINDER, action='store')
    
    sub_parser_wrapper_silent = subparsers.add_parser(
            'wrapper-shell-noerr',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_wrapper_silent.add_argument('arg', nargs=1, action='store')

    sub_parser_touch_mkdir = subparsers.add_parser(
            'touch-mkdir',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_touch_mkdir.add_argument('files', nargs=argparse.REMAINDER, action='store')

    args = parser.parse_args()

    if args.sub_command == 'remove-folders':
            result = []
            for f in args.filenames:
                    r = os.path.splitext(os.sep.join(f.split(os.sep)[1:]))[0]
                    result.append(r)
            print(' '.join(result), end='')
    if args.sub_command == 'remove-folder':
            result = []
            for f in args.filenames:
                    r = os.sep.join(f.split(os.sep)[1:])
                    result.append(r)
            print(' '.join(result), end='')
    if args.sub_command == 'debuild':
            d = templar.api.load_and_populate()
            templar.debuild.run(d, args.source, args.gbp)
    if args.sub_command == 'debuild-install':
            d = templar.api.load_and_populate()
            templar.debuild.run(d, False, False)
            templar.dpkg.install(d)
    if args.sub_command == 'release':
            templar.release.run(templar.api.load_and_populate())
    if args.sub_command == 'wrapper-css-validator':
            templar.wrappers.css_validator.run(args.args)
    if args.sub_command == 'wrapper-debuild':
            templar.wrappers.debuild.run(args.args)
    if args.sub_command == 'wrapper-noerr':
            templar.wrappers.noerr.run(args.args)
    if args.sub_command == 'wrapper-ok':
            templar.wrappers.ok.run(args.args)
    if args.sub_command == 'wrapper-silent':
            templar.wrappers.silent.run(args.args)
    if args.sub_command == 'wrapper-shell-noerr':
            templar.wrappers.shell_noerr.run(args.arg[0])
    if args.sub_command == 'touch-mkdir':
            templar.fileops.touch_mkdir_many(args.files)


if __name__ == '__main__':
    main()
