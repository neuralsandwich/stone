#!/usr/bin/env python3

import collections
import errno
import os
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound
import json
import markdown


class Page(collections.UserDict):
    def __init__(self,
                 site_root,
                 source,
                 target,
                 page_type=None,
                 redirects=None):
        self.data = {}
        self.data['page_type'] = page_type
        self.data['redirects'] = redirects
        self.source_path = os.path.join(site_root, source)
        self.target_path = os.path.join(site_root, target)
        self.source = source
        self.target = target
        self.href = self.target.split('/')[1]
        self.data['content'] = open(self.source_path, "r").read()

    def __contains__(self, key):
        return str(key) in self.data

    def __missing__(self, key):
        if str(key) in self.data:
            return self.data
        else:
            raise KeyError(key)

    def __repr__(self):
        return "Page(%r, %r)" % (self.source, self.target)

    def __setitem__(self, key, item):
        self.data[str(key)] = item

    def convert_to_template_html(self, md_renderer):
        self.renderer = md_renderer
        self['content'] = self.renderer.convert(self['content'])
        for key, value in self.renderer.Meta.items():
            if isinstance(value, list) and len(value) == 1:
                self.data[key] = value[0]
            else:
                self.data[key] = value

    def render_html(self, environment):
        print("Rendering: %s to %s" % (self.source_path, self.target_path))
        try:
            with open(self.target_path, "w") as target_file:
                target_file.write(
                    environment.get_template(self['template']).render(self))
        except TemplateNotFound as tnf:
            print(tnf)
        except KeyError as ke:
            if str(ke) == '\'template\'':
                print('Missing template, rendering markdown only')
                environment.from_string(self['content']).render(self)
            else:
                raise
        except FileNotFoundError as fnf:
            if fnf.errno != errno.ENOENT:
                raise
            else:
                os.makedirs(os.path.split(self.target_path)[0])
                self.render_html(environment)


class Site(object):
    def __init__(self, root, data):
        self.pages = []
        self.index = []
        self.root = root
        self.templates = []
        self.template = []
        self.data = data
        self._parse(data)

    def __repr__(self):
        return "SiteConfig(%r, %r)" % (self.root, self.data)

    def _parse(self, data):
        """Load pages to be generated"""
        try:
            self.pages = [Page(self.root, **page) for page in data["pages"]]
            self.templates = [os.path.join(self.root, template)
                              for template in data["templates"]]
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
            if page['page_type'] == "index":
                page['posts'] = [post for post in self.pages
                                 if post is not page]
            page.render_html(environment)


class ConfigLoader(object):

    site_config_file = "site.json"

    def __init__(self):
        pass

    def load(self, path):
        configs = []
        try:
            json_data = json.loads(
                open(os.path.join(path, self.site_config_file), "r").read())
        except FileNotFoundError as fnf:
            if fnf.errno != errno.ENOENT:
                raise
            else:
                print("Error: No path to site config")
                return 1

        try:
            for site_data in json_data["sites"]:
                configs.append(Site(path, site_data))
        except KeyError:
            configs.append(Site(path, site_data))

        return configs


def main(args):
    if len(args) <= 1:
        print("Error: No path to site root")
        return 1

    site_root = args[1] if os.path.isdir(args[1]) else None

    cfg_loader = ConfigLoader()
    sites = cfg_loader.load(site_root)
    markdown_renderer = markdown.Markdown(
        extensions=['markdown.extensions.meta'])
    for site in sites:
        env = Environment(
            loader=FileSystemLoader(site.templates),
            autoescape=select_autoescape(["html", "xml"]))

        site.render(markdown_renderer, env)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
