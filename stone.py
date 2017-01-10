#!/usr/bin/env python3

import errno
import os
import sys

import json
import markdown

class Page(object):

    def __init__(self, site_root, source, target):
        self.source = os.path.join(site_root, source)
        self.target = os.path.join(site_root, target)

    def __repr__(self):
        return "Page(%r, %r)" % (self.source, self.target)

    def __str__(self):
        return open(self.source, "r").read()


class SiteConfig(object):

    site_config_file = "site.json"

    def __init__(self, path):
        self.root = path
        self.path = os.path.join(path, self.site_config_file)
        self.pages = []
        self._parse(self.path)

    def __repr__(self):
        return "SiteConfig(%r)" % (self.path)

    def _parse(self, config_path):
        json_data = json.loads(open(config_path, "r").read())
        self.pages = [Page(self.root, **page) for page in json_data["pages"]]


def main(args):
    if len(args) <= 1:
        print("Error: No path to site root")
        return 1

    site_root = args[1] if os.path.isdir(args[1]) else None
    config = SiteConfig(site_root)

    for page in config.pages:
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
