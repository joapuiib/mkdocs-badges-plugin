import json
import os
import re

import yaml
from mkdocs.config import base
from mkdocs.config import config_options as c
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files, File
from mkdocs.structure.pages import Page
from re import Match


log = get_plugin_logger(__name__)

BADGE_PATTERN = r"(?<!\\)\[badge(?::([\w\-\_]+))?([^\]]*?)\]"

class BadgesPluginConfig(base.Config):
    classes = c.Type(str, default='mdx-badge')
    types = c.Type(dict, default={})


class BadgesPlugin(BasePlugin[BadgesPluginConfig]):
    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files
    ):
        # Find and replace all external asset URLs in current page
        return self.replace_badges(markdown)

    def replace_badges(self, markdown: str):
        return re.sub(
            BADGE_PATTERN,
            self.replace, markdown, flags = re.I | re.M
        )

    def replace(self, match: Match):
        _type = match.group(1)
        badge_config = self.config['types'].get(_type, {})

        _text = [badge_config['text']] if 'text' in badge_config else []
        if match.group(2):
            _text += match.group(2).strip().split("|")

        _icon = badge_config.get('icon', None)
        _title = badge_config.get('title', None)
        _icon_href = badge_config.get('icon_href', None)

        _reference = badge_config.get('reference', None)
        _href = badge_config.get('href', None)
        _href = self._resolve_path(_reference, page, files) if _reference else _href

        _class = self.config['classes']

        return self._badge(**{
            'type': _type,
            'icon': _icon,
            'icon_href': _icon_href,
            'title': _title,
            'text': _text,
            'href': _href,
            '_class': _class
        })

    # Create badge
    def _badge(self, type: str = "", icon: str = "", icon_href: str = "", title: str = "", text: list = [], href: str = "", _class: str = ""):
        classes = f"{_class} {_class}--{type}" if type else _class
        icon_element = ""
        if icon:
            icon = f':{icon}:' if icon else ""
            if title:
                icon_element = f"<span class=\"{_class}__icon\" title=\"{title}\">{icon}</span>"
            else:
                icon_element = f"<span class=\"{_class}__icon\">{icon}</span>"

        return "".join([
            f"<span class=\"{classes}\">",
            *([f"<a href=\"{icon_href}\" class=\"{_class}__link\">"] if icon_href else []),
            *([icon_element] if icon_element else []),
            *(["</a>"] if icon_href else []),
            *([f"<a href=\"{href}\" class=\"{_class}__link\">"] if href else []),
            *[f"<span class=\"{_class}__text\">{t}</span>" for t in text],
            *(["</a>"] if href else []),
            f"</span>",
        ])


    # Create a linkable option
    def option(self, type: str):
        _, *_, name = re.split(r"[.:]", type)
        return f"[`{name}`](#+{type}){{ #+{type} }}\n\n"

    # Create a linkable setting - @todo append them to the bottom of the page
    def setting(self, type: str):
        _, *_, name = re.split(r"[.*]", type)
        return f"`{name}` {{ #{type} }}\n\n[{type}]: #{type}\n\n"

    # -----------------------------------------------------------------------------

    # Resolve path of file relative to given page - the posixpath always includes
    # one additional level of `..` which we need to remove
    def _resolve_path(self, path: str, page: Page, files: Files):
        path, anchor, *_ = f"{path}#".split("#")
        path = _resolve(files.get_file_from_path(path), page)
        return "#".join([path, anchor]) if anchor else path

    # Resolve path of file relative to given page - the posixpath always includes
    # one additional level of `..` which we need to remove
    def _resolve(self, file: File, page: Page):
        path = posixpath.relpath(file.src_uri, page.file.src_uri)
        return posixpath.sep.join(path.split(posixpath.sep)[1:])
