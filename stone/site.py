"""Site

Stone's representation of a website
"""
# -*- coding: utf-8 -*-

from collections import UserDict
from json import JSONEncoder
import os
from typing import Dict, List

from stone.page import Page, PageEncoder
from stone.resource import Resource


class SiteEncoder(JSONEncoder):
    """JSON encoder for Site"""

    def default(self, o):
        if isinstance(o, Site):
            items = ['site', 'type', 'source', 'target', 'templates']
            result = {}
            for item in items:
                try:
                    result[item] = o[item]
                except KeyError:
                    pass
            result['pages'] = o.pages
            return result
        if isinstance(o, Page):
            return PageEncoder().default(o)

        # When not a page, call the JSONEncoder. It will call the correct fail.
        return JSONEncoder.default(self, o)


class Site(UserDict):  # pylint: disable=too-many-ancestors
    """Representation of a Site"""

    root: str
    pages: List[Page]
    templates: List[str]
    resources: List[str]
    data: Dict[str, str]

    def __init__(self, root: str, data: Dict) -> None:
        super().__init__()
        self.root = root
        self.data = data
        self.pages = []
        self.templates = []
        self.resources = []
        self._parse(data)

    def __contains__(self, key):
        return str(key) in self.data

    def __repr__(self):
        return "Site(%r, %r)" % (self.root, self.data)

    def __str__(self):
        """Return the stringified version of Site

        Return a selective dictionary of Site as a string
        """
        items = ['site', 'type', 'source', 'target', 'templates']
        result = {}
        for item in items:
            try:
                result[item] = self[item]
            except KeyError:
                pass
        result['pages'] = self.pages
        return str(result)

    def __setitem__(self, key, item):
        self.data[str(key)] = item

    def _parse(self, data):
        """Load pages to be generated"""
        for page_data in data['pages']:
            self.pages.append(
                Page(
                    self,
                    page_data.pop('source'),
                    page_data.pop('target'),
                    data=page_data))

        self.templates = [
            os.path.join(self.root, template)
            for template in data.get('templates', [])
        ]
        self.data['templates'] = self.templates
        self.resources = [
            Resource(self.root, **resource)
            for resource in data.get('resources', [])
        ]
        self.data['resources'] = self.resources
