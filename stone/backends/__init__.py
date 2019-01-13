"""Stone Backends"""
import sys
from pathlib import Path

from stone.plugins import import_plugin
import stone.backends.file
import stone.backends.s3

_BUILTIN_BACKENDS = (
    'file',
    's3'
)


def import_backend(module_name):
    if module_name in _BUILTIN_BACKENDS:
        return 'stone.backends.' + module_name

    filename = module_name + '.py'
    module_path = Path.home().joinpath('.stone', 'backends', filename)
    module_name = 'stone.ext.backends.' + module_name
    return import_plugin(module_name, module_path)


def load_backends(backends=[], *args, **kwargs):
    if not backends:
        backends = [{'type': 'file'}]

    results = []
    for b in backends:
        module_name = import_backend(b['type'])
        results.append(sys.modules[module_name].Backend(*args, **b, **kwargs))

    return results
