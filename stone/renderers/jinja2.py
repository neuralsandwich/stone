"""Stone Site Generator"""

from jinja2 import select_autoescape, Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound


class Renderer:
    """Renders Jinja2 templated input"""

    def __init__(self, _next=None, *args, **kwargs):
        self._next = _next
        try:
            self.templates = kwargs['templates']
        except KeyError:
            self.templates = []

    def __eq__(self, other):
        return tuple(self) == tuple(self)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, *self)

    def __str__(self):
        return str(tuple(self))

    def render(self, page):
        """Render using Jinja2 templates"""
        environment = Environment(
            loader=FileSystemLoader(self.templates),
            autoescape=select_autoescape(["html", "xml"]))

        try:
            page['content'] = environment.get_template(
                page['template']).render(page.data)
        except (TemplateNotFound, KeyError) as template_error:
            page['content'] = environment.from_string(page['content']).render(
                page.data)

        if self._next:
            return self._next.render(page)

        return page
