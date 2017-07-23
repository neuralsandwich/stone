"""Config

Stone's representation for site.json
"""
import errno
import json
import os
import sys

from stone.site import Site, SiteEncoder


class Config(object):
    """Loader site.json"""

    site_config_file = "site.json"

    def __init__(self):
        pass

    def read(self, path):
        """Load site configuration"""
        configs = []
        try:
            json_data = json.loads(
                open(os.path.join(path, self.site_config_file), "r").read())
        except FileNotFoundError as fnf:
            if fnf.errno != errno.ENOENT:
                raise
            else:
                print("[ERROR] No path to site config")
                return 1

        try:
            if json_data["version"] != 1:
                print(
                    "This is an older site.json and it doesn't checkout",
                    file=sys.stderr)
                exit(1)
            for site_data in json_data["sites"]:
                configs.append(Site(path, site_data))
        except KeyError:
            configs.append(Site(path, site_data))

        return configs

    def write(self, path, sites):
        """Serialize a site to JSON"""
        config = {'version': 1}
        config['sites'] = sites
        with open(os.path.join(path, self.site_config_file), "w") as cfg_file:
            cfg_file.write(json.dumps(config, cls=SiteEncoder, indent=4))
