"""Page

Stone's representation of a page
"""
from collections import UserDict
import errno
from json import JSONEncoder
import os
import sys
from typing import Any, Dict

from jinja2.exceptions import TemplateNotFound


class PageEncoder(JSONEncoder):
    """JSON encoder for Page"""

    def default(self, o):
        if isinstance(o, Page):
            return o.to_entry()

        # When not a page, call the JSONEncoder. It will call the correct fail.
        return JSONEncoder.default(self, o)


class Page(UserDict):  # pylint: disable=too-many-ancestors
    """Representation of a Page"""

    _site = None
    data: Dict[str, str] = {}

    def __init__(self, site, source: str, target: str,
                 data: Dict=None) -> None:
        super().__init__()
        self.data = {}
        self._site = site

        def get(key, dic):
            """Get a dictionary key if it exists"""
            return dic[key] if key in dic else None

        try:
            for k in data.keys():
                self.data[k] = get(k, data)
        except AttributeError:
            pass

        self.data["source"] = source
        self.data["target"] = target
        self.data["source_path"] = os.path.abspath(
            os.path.join(self._site.root, site['source'], source))
        self.data["target"] = target
        self.data["target_path"] = os.path.abspath(
            os.path.join(self._site.root, site['target'], target))
        try:
            self.data["href"] = target.split('/')[1]
        except IndexError:
            self.data["href"] = target
        self.data['content'] = open(self.data['source_path'], "r").read()
        self.renderer = None

    def __contains__(self, key):
        return key in self.data

    def __delitem__(self, key):
        del self.data[key]

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        self.data.__iter__()

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({}, {})".format(class_name, self['source'], self['target'])

    def __str__(self):
        return str(self.to_entry())

    def __setitem__(self, key, item):
        self.data[key] = item

    def clear(self):
        self.data = {}

    def convert_to_template_html(self, md_renderer):
        """Convert markdown to templated HTML"""
        self.renderer = md_renderer
        self['content'] = self.renderer.convert(self['content'])
        for key, value in self.renderer.Meta.items():
            self[key] = value[0]

    def get(self, key, default=None):
        try:
            return self.data[key]
        except KeyError:
            return default

    def render_html(self, environment):
        """Render the page to html"""
        try:
            with open(self['target_path'], "w") as target_file:
                target_file.write(
                    environment.get_template(self['template']).render(
                        self.data))
        except TemplateNotFound:
            print('Missing template, rendering markdown only',
                  file=sys.stderr)
            with open(self['target_path'], "w") as target_file:
                target_file.write(
                    environment.from_string(self['content']).render(self.data))
        except KeyError as key_error:
            if str(key_error) == '\'template\'':
                print('Missing template, rendering markdown only',
                      file=sys.stderr)
                with open(self['target_path'], "w") as target_file:
                    target_file.write(
                        environment.from_string(
                            self['content']).render(self.data))
            else:
                raise
        except FileNotFoundError as fnf:
            if fnf.errno == errno.ENOENT:
                os.makedirs(
                    os.path.split(self.data['target_path'])[0], exist_ok=True)
                self.render_html(environment)
            else:
                raise

    def to_entry(self) -> Dict[str, Any]:
        """"Convert Page into serialised json for site.json"""

        def get(key):
            """return a dictionary item or None"""
            return self[key] if key in self else None

        items = ['source', 'target', 'page_type']
        entry = {}
        for item in items:
            if get(item) is not None:
                entry[item] = self[item]
        return entry
