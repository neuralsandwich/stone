"""Stone library functions?"""
import collections
import errno
import json
import os

from jinja2.exceptions import TemplateNotFound

class Page(dict):
    """Representation of a Page"""
    def __init__(self,
                 site_root,
                 source,
                 target,
                 page_type=None,
                 redirects=None):
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

    def __contains__(self, key):
        return str(key) in self.data

    def __missing__(self, key):
        if str(key) in self.data:
            return self.data
        else:
            raise KeyError(key)

    def __repr__(self):
        return "Page(%r, %r)" % (self.data['source'], self.data['target'])

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
        print("Rendering: %s to %s" % (self.data['source_path'],
                                       self.data['target_path']))
        try:
            with open(self.data['target_path'], "w") as target_file:
                target_file.write(
                        environment.get_template(self['template']).render(
                            self))
        except TemplateNotFound as tnf:
            print(tnf)
        except KeyError as ke:
            if str(ke) == '\'template\'':
                print('Missing template, rendering markdown only')
                environment.from_string(self['content']).render(self)
            else:
                raise
        except FileNotFoundError as fnf:
            if fnf.errno == errno.ENOENT:
                os.makedirs(
                    os.path.split(self.data['target_path'])[0], exist_ok=True)
                self.render_html(environment)
            else:
                raise


class Resource(dict):
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
                target_file.write(css_minify(self.data["content"]))
        except FileNotFoundError as fnf:
            if fnf.errno == errno.ENOENT:
                os.makedirs(
                    os.path.split(self.data['target_path'])[0], exist_ok=True)
                self.render()
            else:
                raise


class Site(object):
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
            if page['page_type'] == "index":
                """
                Pass all blog posts to the index page, do not pass other indexes
                or page types to the index.
                """
                page['posts'] = [post for post in self.pages
                                 if post is not page]
                page['posts'].reverse()
            page.render_html(environment)

        for resource in self.resources:
            resource.render()


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
                print("[ERROR] No path to site config")
                return 1

        try:
            for site_data in json_data["sites"]:
                configs.append(Site(path, site_data))
        except KeyError:
            configs.append(Site(path, site_data))

        return configs


def add_page(args, sites):
    if not hasattr(args, 'site'):
        print('Why site would you like to add a new page to?')
        count = 0
        for site in sites:
            print("%i - %s" % (count, site.data['site']))
            count += 1

        choice = input()
        if not int(choice) < len(sites):
            print("[ERROR] %s is not a valid selection" % choice)
            return 1
