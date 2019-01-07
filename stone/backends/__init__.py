"""Stone Backends"""
import sys
from pathlib import Path

from stone.plugins import import_plugin
from stone.backends.file import Backend

_BUILTIN_BACKENDS = ('file')


def import_backend(module_name):
    if module_name in _BUILTIN_BACKENDS:
        return 'stone.backends.' + module_name

    filename = module_name + '.py'
    module_path = Path.home().joinpath('.stone', 'backends', filename)
    module_name = 'stone.ext.backends.' + module_name
    return import_plugin(module_name, module_path)


def load_backends(backends=[], *args, **kwargs):
    if not backends:
        backends = ['file']

    results = []
    for b in backends:
        module_name = import_backend(b)
        results.append(sys.modules[module_name].Backend(*args, **kwargs))

    return results
