import logging
import os
from errbot.plugin_info import PluginInfo
from jinja2 import Environment, FileSystemLoader
from bottle import TEMPLATE_PATH
from pathlib import Path

log = logging.getLogger(__name__)


def make_templates_path(root: Path):
    return root / 'templates'


system_templates_path = str(make_templates_path(Path(__file__).parent))
template_path = [system_templates_path]
TEMPLATE_PATH.insert(0, system_templates_path)  # for views
env = Environment(loader=FileSystemLoader(template_path),
                  trim_blocks=True,
                  keep_trailing_newline=False,
                  autoescape=True)


def tenv():
    return env


def make_templates_from_plugin_path(pluginfo_path: Path):
    return make_templates_path(pluginfo_path.parent)


def add_plugin_templates_path(plugin_info: PluginInfo):
    global env
    tmpl_path = make_templates_from_plugin_path(plugin_info.location)
    if tmpl_path.exists():
        log.debug("Templates directory found for this plugin [%s]" % tmpl_path)
        tmpl_path = str(tmpl_path)
        template_path.append(tmpl_path)  # for webhooks
        TEMPLATE_PATH.insert(0, tmpl_path)  # for webviews
        # Ditch and recreate a new templating environment
        env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
        return
    log.debug("No templates directory found for this plugin [Looking for %s]" % tmpl_path)


def remove_plugin_templates_path(plugin_info: PluginInfo):
    global env
    tmpl_path = make_templates_from_plugin_path(plugin_info.location)
    if tmpl_path in template_path:
        tmpl_path = str(tmpl_path)
        template_path.remove(tmpl_path)  # for webhooks
        TEMPLATE_PATH.remove(tmpl_path)  # for webviews
        # Ditch and recreate a new templating environment
        env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
