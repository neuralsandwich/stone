"""Entry point for Stone"""

from __future__ import print_function
import argparse
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown
from .stone import ConfigLoader, add_page


def main(args=None):
    """Entry point function for Stone"""
    parser = argparse.ArgumentParser(description='Static website generator')
    parser.add_argument("site_root", help='website root directory')

    subparsers = parser.add_subparsers(help='sub-command help')
    newpage = subparsers.add_parser(
        'newpage', help=('add a new page to  site.json and an emtpy file'))
    newpage.add_argument(
        "--page-type",
        default="post",
        type=str,
        help='type of page to generate')

    args = parser.parse_args()
    sites = ConfigLoader().load(args.site_root)

    if hasattr(args, 'page_type'):
        return add_page(args, sites)
    else:
        if not os.path.isdir(args.site_root):
            print("[ERROR] %s is not a directory" % args.site_root)
            parser.print_help()
            return 1

        markdown_renderer = markdown.Markdown(
            extensions=['markdown.extensions.meta'])
        for site in sites:
            env = Environment(
                loader=FileSystemLoader(site.templates),
                autoescape=select_autoescape(["html", "xml"]))

            site.render(markdown_renderer, env)

        return 0


if __name__ == '__main__':
    main()
