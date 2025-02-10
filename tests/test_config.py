from mkdocs.config.base import load_config

from mkdocs_badges_plugin.plugin import BadgesPlugin


def test_config_default_values():
    plugin = BadgesPlugin()
    plugin.load_config({})
    assert plugin.config.classes == 'mdx-badge'
    assert plugin.config.types == {}


def test_config_class():
    plugin = BadgesPlugin()
    plugin.load_config({'classes': 'custom-class'})
    assert plugin.config.classes == 'custom-class'


def test_config_types():
    plugin = BadgesPlugin()
    plugin.load_config({'types': {'type': {'text': 'text'}}})
    assert plugin.config.types == {'type': {'text': 'text'}}
