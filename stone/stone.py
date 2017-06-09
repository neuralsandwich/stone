"""Stone library functions?"""

import collections
import errno
import json
import os

from jinja2 import (Environment, FileSystemLoader, select_autoescape)
from jinja2.exceptions import TemplateNotFound
import markdown


class ConfigLoader(object):

    site_config_file = "site.json"

    def __init__(self):
        pass

    def load(self, path):
        """Load site configuration"""
        configs = []
        try:
            json_data = json.loads(
                open(os.path.join(path, self.site_config_file), "r").read())
        except FileNotFoundError as fnf:
            if fnf.errno != errno.ENOENT:
                raise
            else:
                print("[ERROR] No path to site config")
                return 1

        try:
            for site_data in json_data["sites"]:
                configs.append(Site(path, site_data))
        except KeyError:
            configs.append(Site(path, site_data))

        return configs


class Page(collections.UserDict):
    """Representation of a Page"""

    def __init__(self,
                 site_root,
                 source,
                 target,
                 page_type=None,
                 redirects=None):

        self._site_root = site_root
        self.data = {
            "page_type": page_type,
            "redirects": redirects,
            "source": source,
            "source_path": os.path.abspath(os.path.join(site_root, source)),
            "target": target,
            "target_path": os.path.abspath(os.path.join(site_root, target))
        }
        try:
            self.data["href"] = target.split('/')[1]
        except IndexError:
            self.data["href"] = target
        self.data['content'] = open(self.data['source_path'], "r").read()
        self.renderer = None

    def __contains__(self, key):
        return str(key) in self.data

    def __missing__(self, key):
        if str(key) in self.data:
            return self.data
        else:
            raise KeyError(key)

    def __repr__(self):
        class_name = type(self).__name__
        return ('{}({!r}, {!r}, {!r}, page_type={!r}, redirects={!r})'
                .format(class_name, self._site_root, self.data['source'],
                        self.data['target'], self.data['page_type'],
                        self.data['redirects']))

    def __setitem__(self, key, item):
        self.data[str(key)] = item

    def convert_to_template_html(self, md_renderer):
        """Convert markdown to templated HTML"""
        self.renderer = md_renderer
        self.data['content'] = self.renderer.convert(self.data['content'])
        for key, value in self.renderer.Meta.items():
            self.data[key] = value[0]

    def render_html(self, environment):
        print("Rendering: %s to %s" % (self.data['source_path'],
                                       self.data['target_path']))
        try:
            with open(self.data['target_path'], "w") as target_file:
                target_file.write(
                    environment.get_template(self.data['template']).render(
                        self.data))
        except TemplateNotFound as tnf:
            print(tnf)
        except KeyError as ke:
            if str(ke) == '\'template\'':
                print('Missing template, rendering markdown only')
                with open(self.data['target_path'], "w") as target_file:
                    target_file.write(
                        environment.from_string(self.data['content']).render(
                            self))
            else:
                raise
        except FileNotFoundError as fnf:
            if fnf.errno == errno.ENOENT:
                os.makedirs(
                    os.path.split(self.data['target_path'])[0], exist_ok=True)
                self.render_html(environment)
            else:
                raise


class Resource(collections.UserDict):
    def __init__(self, site_root, source, target, resource_type=None):
        self.data = {
            "resource_type": resource_type,
            "source": source,
            "source_path": os.path.abspath(os.path.join(site_root, source)),
            "target": target,
            "target_path": os.path.abspath(os.path.join(site_root, target)),
            "href": target.split('/')[1]
        }
        with open(self.data["source_path"], "r") as source_file:
            self.data["content"] = source_file.read()

    def __contains__(self, key):
        return str(key) in self.data

    def __missing__(self, key):
        if str(key) in self.data:
            return self.data
        else:
            raise KeyError(key)

    def __repr__(self):
        return "Resource(%r, %r)" % (self.data['source'], self.data['target'])

    def __setitem__(self, key, item):
        self.data[str(key)] = item

    def render(self):
        print("Rendering: %s to %s" % (self.data['source_path'],
                                       self.data['target_path']))
        try:
            with open(self.data['target_path'], "w") as target_file:
                target_file.write(self.data["content"])
        except FileNotFoundError as fnf:
            if fnf.errno == errno.ENOENT:
                os.makedirs(
                    os.path.split(self.data['target_path'])[0], exist_ok=True)
                self.render()
            else:
                raise


class Site(collections.UserDict):
    def __init__(self, root, data):
        self.pages = []
        self.index = []
        self.root = root
        self.templates = []
        self.resources = []
        self.data = data
        self._parse(data)

    def __repr__(self):
        return "Site(%r, %r)" % (self.root, self.data)

    def _parse(self, data):
        """Load pages to be generated"""
        try:
            self.pages = [Page(self.root, **page) for page in data["pages"]]
            self.templates = [os.path.join(self.root, template)
                              for template in data["templates"]]
            self.resources = [Resource(self.root, **resource)
                              for resource in data["resources"]]
            print(self.resources)
        except KeyError as ke:
            if ke is 'templates':
                print("No temaplates found for %s" % (data["site"]))

    def is_blog(self):
        try:
            return self.data['type'] == 'blog'
        except KeyError as ke:
            return False

    def render(self, renderer, environment):
        """Render Markdown to HTML and extract YAML metadata"""
        for page in self.pages:
            page.convert_to_template_html(renderer)
            """
            Pages to know their titles, this comes from their YAML metadata
            """
        for page in self.pages:
            if page.data['page_type'] == "index":
                """
                Pass all blog posts to the index page, do not pass other indexes
                or page types to the index.
                """
                page.data['posts'] = [post for post in self.pages
                                      if post is not page]
                page.data['posts'].reverse()
            page.render_html(environment)

        for resource in self.resources:
            resource.render()


def generate_site(args):
    """Generate site"""
    sites = ConfigLoader().load(args.site_root)

    markdown_renderer = markdown.Markdown(
        extensions=['markdown.extensions.meta'])
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
