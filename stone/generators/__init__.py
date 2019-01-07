"""Stone Sites"""

import sys
from pathlib import Path

from stone.plugins import import_plugin

from stone.generators.blog import Generator
from stone.generators.single import Generator

_BUILTIN_GENERATORS = (
    'stone.generators.blog',
    'stone.generators.single',
)


def import_generators(module_name):
    if module_name in _BUILTIN_GENERATORS:
        return module_name

    filename = module_name + '.py'
    module_path = Path.home().joinpath('.stone', 'generators', filename)
    module_name = 'stone.ext.generators.' + module_name
    result = import_plugin(module_name, module_path)
    return result


def load_generator(name, *args, **kwargs):
    module_name = import_generators(name)
    return sys.modules[name].Generator(*args, **kwargs)


def get_module_name(name):
    builtin_name = 'stone.generators.' + name
    if builtin_name in _BUILTIN_GENERATORS:
        return builtin_name

    return 'stone.ext.generators.' + name
