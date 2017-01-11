#!/usr/bin/env python3

import errno
import os
import sys

from jinja2 import Environment, DictLoader, select_autoescape
import json
import markdown


class Page(object):
    def __init__(self, site_root, source, target, redirects=None):
        self.source = os.path.join(site_root, source)
        self.target = os.path.join(site_root, target)

    def __repr__(self):
        return "Page(%r, %r)" % (self.source, self.target)

    def __str__(self):
        return open(self.source, "r").read()


class SiteConfig(object):

    site_config_file = "site.json"

    def __init__(self, root, data):
        self.root = root
        self.pages = []
        self.template = []
        self.data = data
        self._parse(data)

    def __repr__(self):
        return "SiteConfig(%r, %r)" % (self.root, self.data)

    def _parse(self, data):
        """Load pages to be generated"""
        try:
            self.pages = [Page(self.root, **page)
                          for page in data["pages"]]
            self.templates = [os.path.join(self.root, template)
                              for template in data["templates"]]
        except KeyError as ke:
            if ke is 'templates':
                print("No temaplates found for %s" %(data["site"]))


def main(args):
    if len(args) <= 1:
        print("Error: No path to site root")
        return 1

    site_root = args[1] if os.path.isdir(args[1]) else None

    site_configs = {}
    try:
        json_data = json.loads(
            open(os.path.join(site_root, SiteConfig.site_config_file), "r")
            .read())
    except FileNotFoundError as fnf:
        if fnf.errno != errno.ENOENT:
            raise
        else:
            print("Error: No path to site config")
            return 1

    try:
        for site_data in json_data["sites"]:
            site_configs[site_data["site"]] = SiteConfig(site_root, site_data)
    except KeyError:
        site_configs[site_data["site"]] = SiteConfig(site_root, site_data)

    for site in site_configs.values():
        for page in site.pages:
            html = markdown.markdown(str(page))
            try:
                target_file = open(page.target, "w")
                target_file.write(html)
                target_file.close()
            except FileNotFoundError as fnf:
                if fnf.errno != errno.ENOENT:
                    raise
                else:
                    target_path = os.path.split(page.target)[0]
                    if os.path.isdir(target_path) is False:
                        os.mkdir(target_path)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
