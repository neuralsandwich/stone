"""Markdown to HTML Renderer"""

import mistune
import mistune_contrib.meta as m_meta


class Renderer:
    """Renders Markdown into HTML"""

    def __init__(self, _next=None, *args, **kwargs):
        self._next = _next

    def __eq__(self, other):
        return tuple(self) == tuple(self)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, *self)

    def __str__(self):
        return str(tuple(self))

    def render(self, page):
        """Renders a page content from Markdown to HTML"""
        meta, page['content'] = m_meta.parse(page['content'])
        page['content'] = mistune.markdown(page['content'])

        for key, value in meta.items():
            page[key] = value

        if self._next:
            return self._next.render(page)

        return page
