"""Stone library functions?"""
# -*- coding: utf-8 -*-

import os

from jinja2 import select_autoescape, Environment, FileSystemLoader
from markdown import Markdown

from stone.config import Config
from stone.page import Page
from stone.site import Site


def generate_site(args):
    """Generate site"""
    sites = Config().read(args.site_root)

    markdown_renderer = Markdown(extensions=[
        'markdown.extensions.meta', 'markdown.extensions.tables',
        'markdown.extensions.footnotes'
    ])
    for site in sites:
        env = Environment(
            loader=FileSystemLoader(site.templates),
            autoescape=select_autoescape(["html", "xml"]))
        site.render(markdown_renderer, env)


def new_page(args):
    """Add new page to the site"""
    sites = Config().read(args.site_root)
    if not hasattr(args, 'site'):
        print('What site would you like to add a new page to?')
        count = 0
        for site in sites:
            print("%i - %s" % (count, site.data['site']))
            count += 1

        choice = input()
        if not int(choice) < len(sites):
            print("[ERROR] %s is not a valid selection" % choice)

    site = sites[int(choice)]
    if site:
        page = create_page(site, args.source, args.target)
        page['page_type'] = args.page_type
        site.add_page(page)
        Config().write(args.site_root, sites)


def create_page(site: Site, source: str, target: str) -> Page:
    """Create a Page() and file on disk"""
    init_content = '# Hello, World!'

    try:
        os.mkdir(os.path.join('{}/{}'.format(site.root, site['source'])))
    except FileExistsError:
        pass

    file_path = '{}/{}/{}'.format(site.root, site['source'], source)
    file = open(file_path, 'w')
    file.write(init_content)
    file.close()

    if target is None:
        # Attempt to sanitize the filename from source for our output.html
        from unidecode import unidecode
        target = unidecode(source)
        target = target.lower().replace(r' ', '-')
        target = '{}.html'.format(target.split('.')[0])

    page = Page(site, source, target)
    return page


def init_site(args):
    """Creata a new site from template"""
    template_sites = '{{"sites":[{!s}]}}'
    template_site = ('{{"site":"{!s}",'
                     '"pages":[{!s}],"type":"{!s}","templates":"[{!s}]"}}')
    template_page = ('{{"page_type":"{!s}","source":"{!s}","target":"{!s}",'
                     '"redirects":"{!s}"}}')
    init_content = '# Hello, World!'
    init_index = template_page.format('page', 'source/index.md',
                                      'target/index.html', '')
    site = template_site.format(args.site_name, init_index, 'page', '')
    sites = template_sites.format(site)

    file = open('{}/site.json'.format(args.site_root), 'w')
    file.write(sites)
    file.close()

    try:
        os.mkdir(os.path.join('{}/source'.format(args.site_root)))
    except FileExistsError:
        pass

    file = open('{}/source/index.md'.format(args.site_root), 'w')
    file.write(init_content)
    file.close()
