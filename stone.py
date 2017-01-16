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
    def __init__(self, site_root, source, target, redirects=None):
        self.data = {}
        self.source = source
        self.target = target
        self.source_path = os.path.join(site_root, source)
        self.target_path = os.path.join(site_root, target)
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

    def __str__(self):
        return self.data['content']
        return
    def __setitem__(self, key, item):
        self.data[str(key)] = item

    def md_to_template_html(self, md_renderer):
        self.renderer = md_renderer
        self['content'] = self.renderer.convert(str(self))
        for key, value in self.renderer.Meta.items():
            if isinstance(value, list) and len(value) == 1:
                self.data[key] = value[0]
            else:
                self.data[key] = value


class SiteConfig(object):
    def __init__(self, root, data):
        self.pages = []
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
                configs.append(SiteConfig(path, site_data))
        except KeyError:
            configs.append(SiteConfig(path, site_data))

        return configs


def main(args):
    if len(args) <= 1:
        print("Error: No path to site root")
        return 1

    site_root = args[1] if os.path.isdir(args[1]) else None

    cfg_loader = ConfigLoader()
    site_configs = cfg_loader.load(site_root)
    markdown_renderer = markdown.Markdown(
        extensions=['markdown.extensions.meta'])
    for site in site_configs:
        env = Environment(
            loader=FileSystemLoader(site.templates),
            autoescape=select_autoescape(["html", "xml"]))

        for page in site.pages:
            page.md_to_template_html(markdown_renderer)
            print("Rendering: %s to %s" % (page.source, page.target))
            try:
                with open(page.target_path, "w") as target_file:
                    target_file.write(
                    env.get_template(page['template']).render(page))
            except TemplateNotFound as tnf:
                print(tnf)
            except KeyError as ke:
                if str(ke) == '\'template\'':
                    print('Missing template, rendering markdown only')
                    env.from_string(page.content).render(page)
                else:
                    raise
            except FileNotFoundError as fnf:
                if fnf.errno != errno.ENOENT:
                    raise
                else:
                    target_path = os.path.split(page.target)[0]
                    if os.path.isdir(target_path) is False:
                        os.makedirs(target_path)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
