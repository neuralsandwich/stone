"""Entry point for Stone"""

from __future__ import print_function
import argparse
import os

from stone.stone import generate_site, init_site, new_page


def add_newpage(parser):
    """Add arguments for newpage command"""
    subparser = parser.add_parser(
        'newpage', help=('add a new page to  site.json and an emtpy file'))
    subparser.add_argument(
        "source",
        type=str,
        help='input filename')
    subparser.add_argument(
        "--target",
        type=str,
        help='output filename')
    subparser.add_argument(
        "--page-type",
        default="post",
        type=str,
        help='type of page to generate')
    subparser.set_defaults(func=new_page)


def add_init(parser):
    """Add arguments for init command"""
    subparser = parser.add_parser(
        'init', help=('create a template site.json'))
    subparser.add_argument(
        "--type", default="blog", type=str, help='type of site to generate')
    subparser.add_argument(
        "--site-name",
        type=str,
        help='name of the site: example.com',
        required=True)
    subparser.set_defaults(func=init_site)


def add_generate(parser):
    """Add arguments for generate command"""
    subparser = parser.add_parser(
        'generate', aliases=['gen', 'build'], help=('generate site'))
    subparser.set_defaults(func=generate_site)


def main(args=None):
    """Entry point function for Stone"""
    parser = argparse.ArgumentParser(
        prog='stone', description='Static website generator')

    # Add general arguments after subparsers so the order makes sense
    parser.add_argument("site_root", help='website root directory')

    subparsers = parser.add_subparsers(title='commands', help='commands')

    # stone build <path>
    add_generate(subparsers)

    # stone init <path>
    add_init(subparsers)

    # stone newpage <path>
    add_newpage(subparsers)
    args = parser.parse_args()

    if not os.path.isdir(args.site_root):
        print("[ERROR] %s is not a directory" % args.site_root)
        parser.print_help()
        return 1

    args.func(args)


if __name__ == '__main__':
    main()
