"""Write strings to a file"""

import os
import errno


class Backend:
    """Stone backend for writing to file"""

    def __init__(self, *args, **kwargs):
        try:
            self._root = kwargs['root']
        except KeyError:
            self._root = None

    def __eq__(self, other):
        return tuple(self) == tuple(self)

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __str__(self):
        return str(tuple(self))

    def _write(self, _path, content):
        path = os.path.join(self._root, _path)
        with open(path, 'w') as output:
            output.write(content)

    def commit(self, page):
        """Commit page to a file"""

        try:
            self._write(page['target_path'], page['content'])
        except FileNotFoundError as fnf:
            if fnf.errno == errno.ENOENT:
                os.makedirs(
                    os.path.split(page.data['target_path'])[0], exist_ok=True)
                self._write(page['target_path'], page['content'])
            else:
                raise
