"""Config

Stone's representation for site.json
"""
import errno
import json
import os

from stone.site import Site


class Config(object):

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
            for site_data in json_data["sites"]:
                configs.append(Site(path, site_data))
        except KeyError:
            configs.append(Site(path, site_data))

        return configs
