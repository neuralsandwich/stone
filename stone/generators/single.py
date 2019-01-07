"""Stone Static Content"""

from stone.generators.abc import SiteGenerator


class Generator(SiteGenerator):
    """Stones interpretation of a single page"""
    site_type = "single"

    def __init__(self):
        pass

    def __eq__(self, other):
        return tuple(self) == tuple(self)

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __str__(self):
        return str(tuple(self))

    def generate(self, renderer, site):
        return [renderer.render(page) for page in site.pages]
