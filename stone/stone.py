"""Stone library functions?"""
# -*- coding: utf-8 -*-

import os

from jinja2 import select_autoescape, Environment, FileSystemLoader

from stone.config import Config
from stone.page import Page
from stone.site import Site


def generate_site(args):
    """Generate site"""
    sites = Config().read(args.site_root)

    for site in sites:
        env = Environment(
            loader=FileSystemLoader(site.templates),
            autoescape=select_autoescape(["html", "xml"]))
        site.render(env)


def new_page(args):
    """Add new page to the site"""
    sites = Config().read(args.site_root)
    if not hasattr(args, 'site'):
        print('What site would you like to add a new page to?')
        count = 0
        for site in sites:
            print("%i - %s" % (count, site['site']))
            count += 1

        choice = input()
        if not int(choice) < len(sites):
            print("[ERROR] %s is not a valid selection" % choice)

    site = sites[int(choice)]
    if site:
        create_add_page(site, args.source, args.target,
                        data={'page_type': args.page_type})
        Config().write(args.site_root, sites)


def create_add_page(site: Site, source: str, target: str, data=None,
                    content=None):
    """Create a Page() and file on disk"""
    init_content = '# Hello, World!'
    if content is None and not isinstance(content, str):
        content = init_content

    try:
        os.mkdir(os.path.join('{}/{}'.format(site.root, site['source'])))
    except FileExistsError:
        pass

    file_path = '{}/{}/{}'.format(site.root, site['source'], source)
    file = open(file_path, 'w')
    file.write(content)
    file.close()

    if target is None:
        # Attempt to sanitize the filename from source for our output.html
        from unidecode import unidecode
        target = unidecode(source)
        target = target.lower().replace(r' ', '-')
        target = '{}.html'.format(target.split('.')[0])

    site.add_page(Page(site, source, target, data))


def init_site(args):
    """Creata a new site from template"""
    index_content = '''
{% for post in posts %}
    <ul>
        <li><a href="{{ post.href }}">{{ post.title }}</a></li>
    </ul>
{% endfor %}
'''
    init_content = 'title: Hello, World!\n\n# Hello, World!'

    site = Site(args.site_root, {'site': args.site_name, 'source': 'source',
                                 'target': 'target'})
    if args.type == 'blog':
        create_add_page(site, 'index.md', 'index.html',
                        content=index_content, data={'page_type': 'index'})
        create_add_page(site, 'example.md', 'example.html',
                        content=init_content, data={'page_type': 'post'})
    else:
        create_add_page(site, 'index.md', 'index.html', content=init_content)

    Config().write(args.site_root, [site])
