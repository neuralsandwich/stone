"""Abstract base class for SiteGenerators"""

from abc import (
    ABC,
    abstractmethod,
)


class SiteGenerator(ABC):
    pass

    @abstractmethod
    def generate(self, renderer, site):
        pass
