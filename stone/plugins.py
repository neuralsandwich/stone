"""Stone Plugin Functions"""

import importlib
import sys


def import_plugin(module_name, file_path):
    """Returns the name of the imported python module or raises ImportError"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    if module is None:
        raise ImportError("Could not find {}".format(module_name))

    spec.loader.exec_module(module)
    sys.modules[module_name] = module
    return module_name
