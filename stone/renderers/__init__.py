"""Stone Renderers"""
import sys
from pathlib import Path

from stone.plugins import import_plugin
from stone.renderers.jinja2 import Renderer as Jinja2Renderer
from stone.renderers.markdown import Renderer as MarkdownRenderer

_BUILTIN_RENDERERS = (
    'jinja2',
    'markdown',
)


def import_renderer(module_name):
    if module_name in _BUILTIN_RENDERERS:
        return 'stone.renderers.' + module_name

    filename = module_name + '.py'
    module_path = Path.home().joinpath('.stone', 'renderers', filename)
    module_name = 'stone.ext.renderers' + module_name
    return import_plugin(module_name, module_path)


def load_renderers(renderers=[], templates=[]):
    if not renderers:
        renderers = ['markdown', 'jinja2']

    previous_renderer = None
    for r in renderers[::-1]:
        module_name = import_renderer(r)
        renderer = sys.modules[module_name].Renderer(
            templates=templates, _next=previous_renderer)
        previous_renderer = renderer
    return previous_renderer
