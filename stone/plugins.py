"""Stone Plugin Functions"""

import importlib
import sys

def import_plugin(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    if module is None:
        raise ImportError

    spec.loader.exec_module(module)
    sys.modules[module_name] = module
    return module_name


