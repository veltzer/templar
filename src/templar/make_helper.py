#!/usr/bin/python3

'''
Make is really bad at doing text processing. So the idea is to help make out
by supplying a python script which do the heavy lifting and keep the make code
clean and simple.
'''

###########
# imports #
###########
import os.path # splitext
import os # for sep
import argparse # for ArgumentParser, ArgumentDefaultsHelpFormatter, REMAINDER
import templar.api # for load_and_populate
import templar.debuild # for run
import templar.release # for run
import templar.dpkg # for install
import templar.wrappers.css_validator # for run
import templar.wrappers.debuild # for run
import templar.wrappers.noerr # for run
import templar.wrappers.ok # for run
import templar.wrappers.silent # for run
import templar.fileops # for touch_mkdir_many

########
# code #
########
def main():
    parser=argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers=parser.add_subparsers(
            title='subcommands',
            dest='subcommand',
    )

    subparser_rmfdas=subparsers.add_parser(
            'rmfdas',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser_rmfdas.add_argument('filenames', nargs=argparse.REMAINDER, action='store')

    subparser_rmfd=subparsers.add_parser(
            'rmfd',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser_rmfd.add_argument('filenames', nargs=argparse.REMAINDER, action='store')

    subparser_debuild=subparsers.add_parser(
            'debuild',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser_debuild.add_argument('--source', help='create only source packages', default=False, action='store_true')
    subparser_debuild.add_argument('--gbp', help='use git build package', default=False, action='store_true')

    subparser_debuild_install=subparsers.add_parser(
            'debuild-install',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparser_release=subparsers.add_parser(
            'release',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparser_wrapper_css_validator=subparsers.add_parser(
            'wrapper-css-validator',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser_wrapper_css_validator.add_argument('args', nargs=argparse.REMAINDER, action='store')

    subparser_wrapper_debuild=subparsers.add_parser(
            'wrapper-debuild',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser_wrapper_debuild.add_argument('args', nargs=argparse.REMAINDER, action='store')

    subparser_wrapper_noerr=subparsers.add_parser(
            'wrapper-noerr',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser_wrapper_noerr.add_argument('args', nargs=argparse.REMAINDER, action='store')

    subparser_wrapper_ok=subparsers.add_parser(
            'wrapper-ok',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser_wrapper_ok.add_argument('args', nargs=argparse.REMAINDER, action='store')

    subparser_wrapper_silent=subparsers.add_parser(
            'wrapper-silent',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser_wrapper_silent.add_argument('args', nargs=argparse.REMAINDER, action='store')

    subparser_touch_mkdir=subparsers.add_parser(
            'touch-mkdir',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser_touch_mkdir.add_argument('files', nargs=argparse.REMAINDER, action='store')

    args=parser.parse_args()

    if args.subcommand=='rmfdas':
            result=[]
            for f in args.filenames:
                    r=os.path.splitext(os.sep.join(f.split(os.sep)[1:]))[0]
                    result.append(r)
            print(' '.join(result), end='')
    if args.subcommand=='rmfd':
            result=[]
            for f in args.filenames:
                    r=os.sep.join(f.split(os.sep)[1:])
                    result.append(r)
            print(' '.join(result), end='')
    if args.subcommand=='debuild':
            d=templar.api.load_and_populate()
            templar.debuild.run(d, args.source, args.gbp)
    if args.subcommand=='debuild-install':
            d=templar.api.load_and_populate()
            templar.debuild.run(d, False, False)
            templar.dpkg.install(d)
    if args.subcommand=='release':
            templar.release.run(templar.api.load_and_populate())
    if args.subcommand=='wrapper-css-validator':
            templar.wrappers.css_validator.run(args.args)
    if args.subcommand=='wrapper-debuild':
            templar.wrappers.debuild.run(args.args)
    if args.subcommand=='wrapper-noerr':
            templar.wrappers.noerr.run(args.args)
    if args.subcommand=='wrapper-ok':
            templar.wrappers.ok.run(args.args)
    if args.subcommand=='wrapper-silent':
            templar.wrappers.silent.run(args.args)
    if args.subcommand=='touch-mkdir':
            templar.fileops.touch_mkdir_many(args.files)


if __name__ == '__main__':
    main()
