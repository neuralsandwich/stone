"""Resource

Stone's representation for resources like CSS
"""

from collections import UserDict
import errno
import os


class Resource(UserDict):
    """Resource: Stones representation for resources like CSS"""
    def __init__(self, site_root, source, target, resource_type=None):
        super().__init__()
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
                target_file.write(self.data["content"])
        except FileNotFoundError as fnf:
            if fnf.errno == errno.ENOENT:
                os.makedirs(
                    os.path.split(self.data['target_path'])[0], exist_ok=True)
                self.render()
            else:
                raise
