"""Page

Stone's representation of a page
"""
from collections import UserDict
import errno
import os

from jinja2.exceptions import TemplateNotFound


class Page(UserDict):
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
