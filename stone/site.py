"""Site

Stone's representation of a website
"""
from collections import UserDict
import os

from stone.page import Page
from stone.resource import Resource


class Site(UserDict):
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
