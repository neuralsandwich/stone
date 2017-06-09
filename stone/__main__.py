"""Entry point for Stone"""

from __future__ import print_function
import argparse
import os

from .stone import generate_site, init_site, new_page


def main(args=None):
    """Entry point function for Stone"""
    parser = argparse.ArgumentParser(
        prog='stone', description='Static website generator')

    # Add general arguments after subparsers so the order makes sense
    parser.add_argument("site_root", help='website root directory')

    subparsers = parser.add_subparsers(title='commands', help='commands')

    # stone build <path>
    build_parser = subparsers.add_parser(
        'generate', aliases=['gen'], help=('generate site'))
    build_parser.set_defaults(func=generate_site)

    # stone init <path>
    init_parser = subparsers.add_parser(
        'init', help=('create a template site.json'))
    init_parser.add_argument(
        "--type", default="blog", type=str, help='type of site to generate')
    init_parser.add_argument(
        "--site-name",
        type=str,
        help='name of the site: example.com',
        required=True)
    init_parser.set_defaults(func=init_site)

    # stone newpage <path>
    newpage_parser = subparsers.add_parser(
        'newpage', help=('add a new page to  site.json and an emtpy file'))
    newpage_parser.add_argument(
        "--page-type",
        default="post",
        type=str,
        help='type of page to generate')
    newpage_parser.set_defaults(func=new_page)

    args = parser.parse_args()

    if not os.path.isdir(args.site_root):
        print("[ERROR] %s is not a directory" % args.site_root)
        parser.print_help()
        return 1

    args.func(args)


if __name__ == '__main__':
    main()
