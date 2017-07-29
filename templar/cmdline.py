"""
This script is a wrapper for the mako templating system to be used from the command line,
build system or whatever.

It has command line parsing and ability to import your own variable definitions.
- It can process a single file, in the future this may change.
- It work in utf.
- It chmods the output file to be read only (to avoid accidentally editing it).
- On any exception no output file is produced.
- You can specify encodings from the command line.
TODO:
- make this module create the folder for the output file if that folder does not exist.
"""

import sys
import argparse
import templar.api


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        title='sub_commands',
        dest='sub_command',
    )

    sub_parser_process = subparsers.add_parser(
        'process',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_process.add_argument('--input', help='input file')
    sub_parser_process.add_argument('--input_encoding', help='specify input encoding', default=sys.getdefaultencoding())
    sub_parser_process.add_argument('--output', help='output file')
    sub_parser_process.add_argument('--output_encoding', help='specify output encoding',
                                    default=sys.getdefaultencoding())
    sub_parser_process.add_argument('--no_chmod', help='don\'t chmod the output to readonly', default=False,
                                    action='store_true')

    sub_parser_print = subparsers.add_parser(
        'print_make',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser_print.add_argument('--no_sec', help="don't do security", default=False, action='store_true')

    for x in ['print_all', 'get_deps', 'install_deps', 'git_config']:
        subparsers.add_parser(
            x,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    args = parser.parse_args()

    if args.sub_command == 'process':
        d = templar.api.load_and_populate()
        try:
            templar.api.process(
                d,
                args.input,
                args.output,
                args.input_encoding,
                args.output_encoding,
                args.no_chmod,
            )
        except Exception as e:
            templar.api.print_exception(e, args.input)
            sys.exit(1)

    if args.sub_command == 'print_make':
        d = templar.api.load_and_populate()
        for k in sorted(d.keys()):
            v = d[k]
            if type(v) != str:
                continue
            if v.find('\n') != -1:
                continue
            if not args.no_sec and (k.find('password') != -1 or k.find('secret') != -1):
                continue
            print('{0}.{1}:={2}'.format('tdefs', k, v))

    if args.sub_command == 'print_all':
        d = templar.api.load_and_populate()
        for k in sorted(d.keys()):
            v = d[k]
            print('{0}.{1}={2}'.format('tdefs', k, v))

    if args.sub_command == 'install_deps':
        d = templar.api.load_and_populate()
        templar.api.install_deps(d)

    if args.sub_command == 'git_config':
        d = templar.api.load_and_populate()
        templar.api.git_config(d)

    if args.sub_command == 'get_deps':
        print(' '.join(templar.api.get_all_deps()))


if __name__ == '__main__':
    main()
