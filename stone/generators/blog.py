"""Stone Blog"""

from stone.generators.abc import SiteGenerator


class Generator(SiteGenerator):
    """Stones interpretation of a blog"""
    site_type = "blog"

    def __init__(self):
        pass

    def __eq__(self, other):
        return tuple(self) == tuple(self)

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __str__(self):
        return str(tuple(self))

    def generate(self, renderer, site):
        rendered_pages = []
        index = None

        for page in site.pages:
            if page.get('page_type') == 'index':
                index = page
                continue

            rendered_page = renderer.render(page)
            rendered_pages.append(rendered_page)

        index['posts'] = [post for post in site.pages if post is not index]
        index['posts'].reverse()
        rendered_pages.append(renderer.render(index))

        return rendered_pages
