"""Stone library functions?"""

import os

from jinja2 import (Environment, FileSystemLoader, select_autoescape)
import markdown

from stone.configloader import ConfigLoader


def generate_site(args):
    """Generate site"""
    sites = ConfigLoader().load(args.site_root)

    markdown_renderer = markdown.Markdown(
        extensions=['markdown.extensions.meta', 'markdown.extensions.tables',
                    'markdown.extensions.footnotes'])
    for site in sites:
        env = Environment(
            loader=FileSystemLoader(site.templates),
            autoescape=select_autoescape(["html", "xml"]))
        site.render(markdown_renderer, env)


def new_page(args):
    """Add new page to the site"""
    sites = ConfigLoader().load(args.site_root)
    if not hasattr(args, 'site'):
        print('What site would you like to add a new page to?')
        count = 0
        for site in sites:
            print("%i - %s" % (count, site.data['site']))
            count += 1

        choice = input()
        if not int(choice) < len(sites):
            print("[ERROR] %s is not a valid selection" % choice)
            return 1


def init_site(args):
    template_sites = '{{"sites":[{!s}]}}'
    template_site = '{{"site":"{!s}","pages":[{!s}],"type":"{!s}","templates":"[{!s}]"}}'
    template_page = '{{"page_type":"{!s}","source":"{!s}","target":"{!s}","redirects":"{!s}"}}'
    init_content = '# Hello, World!'
    init_index = template_page.format('page', 'source/index.md',
                                      'target/index.html', '')
    init_site = template_site.format(args.site_name, init_index, 'page', '')
    init_sites = template_sites.format(init_site)

    f = open('{}/site.json'.format(args.site_root), 'w')
    f.write(init_sites)
    f.close()

    try:
        os.mkdir(os.path.join('{}/source'.format(args.site_root)))
    except FileExistsError as fef:
        pass

    f = open('{}/source/index.md'.format(args.site_root), 'w')
    f.write(init_content)
    f.close()
