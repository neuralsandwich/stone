"""Config

Stone's representation for site.json
"""

from collections import UserDict
import json
import os

from stone.site import SiteEncoder

CONFIG_VERSION = 1
SITE_CONFIG_FILE = "site.json"


class SiteConfig(UserDict):
    """SiteConfig

    A UserDict which requires a path
    """
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.data = {k: v for k, v in kwargs.items()}

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({!r})".format(class_name, self.path)

    def __missing__(self, key):
        return self[key]

    def __contains__(self, key):
        return key in self.data[key]

    def __setitem__(self, key, item):
        self.data[key] = item


def read(path):
    """Load site configuration"""
    configs = []
    json_data = json.loads(
        open(os.path.join(path, SITE_CONFIG_FILE), "r").read())

    try:
        if json_data["version"] != 1:
            raise ValueError('Version not supported. Supported version {}'.
                             format(CONFIG_VERSION))
        for site_data in json_data["sites"]:
            configs.append(SiteConfig(path, **site_data))
    except KeyError:
        configs.append(SiteConfig(path, **site_data))

    return configs


def write(path, sites):
    """Serialize a site to JSON"""
    config = {'version': CONFIG_VERSION}
    config['sites'] = sites

    with open(os.path.join(path, self.site_config_file), "w") as cfg_file:
        cfg_file.write(json.dumps(config, cls=SiteEncoder, indent=4))
