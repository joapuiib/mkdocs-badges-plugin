import re
import textwrap

from mkdocs_badges_plugin.plugin import BadgesPlugin

from mkdocs.commands.build import build
from mkdocs.config.base import load_config

def _dedent(text):
    return "".join(textwrap.dedent(text).strip().split("\n"))

def _test(markdown_text, expected_html, config={}, page=None, files=None):
    plugin = BadgesPlugin()
    plugin.load_config(config)

    expected_html = _dedent(expected_html)

    html = plugin.replace_badges(markdown_text, page, files)
    assert html == expected_html


def test_escaped_badge():
    markdown_text = '\\[badge Text]'
    expected = '\\[badge Text]'

    _test(markdown_text, expected)


def test_generic_untyped_badge_single_text():
    markdown_text = '[badge Text]'

    expected_html = R'''
    <span class="mdx-badge">
    <span class="mdx-badge__text">Text</span>
    </span>
    '''

    _test(markdown_text, expected_html)


def test_generic_untyped_badge_multiple_text():
    markdown_text = '[badge Text1 with spaces|Text2 with spaces]'

    expected_html = R'''
    <span class="mdx-badge">
    <span class="mdx-badge__text">Text1 with spaces</span>
    <span class="mdx-badge__text">Text2 with spaces</span>
    </span>
    '''

    _test(markdown_text, expected_html)


def test_generic_typed_badge():
    markdown_text = '[badge:type Text]'

    expected_html = R'''
    <span class="mdx-badge mdx-badge--type">
    <span class="mdx-badge__text">Text</span>
    </span>
    '''

    _test(markdown_text, expected_html)


def test_config_class_badge():
    config = {'classes': 'custom-badge'}
    markdown_text = '[badge:type Text]'

    expected_html = R'''
    <span class="custom-badge custom-badge--type">
    <span class="custom-badge__text">Text</span>
    </span>
    '''

    _test(markdown_text, expected_html, config)

def test_typed_badge():
    config = {
        'types': {
            'tag': {
                'title': 'Tag',
                'text': 'Tag',
                'icon': 'material-tag'
        }
    }}

    markdown_text = '[badge:tag]'

    expected_html = R'''
    <span class="mdx-badge mdx-badge--tag">
    <span class="mdx-badge__icon" title="Tag">:material-tag:</span>
    <span class="mdx-badge__text">Tag</span>
    </span>
    '''

    _test(markdown_text, expected_html, config)


def test_typed_badge_href():
    config = {
        'types': {
            'tag': {
                'title': 'Tag',
                'icon': 'material-tag',
                'href': 'https://example.com',
                'text': 'Tag',
        }
    }}

    markdown_text = '[badge:tag]'

    expected_html = R'''
    <span class="mdx-badge mdx-badge--tag">
    <span class="mdx-badge__icon" title="Tag">:material-tag:</span>
    <a href="https://example.com" class="mdx-badge__link">
    <span class="mdx-badge__text">Tag</span>
    </a>
    </span>
    '''

    _test(markdown_text, expected_html, config)


def test_typed_badge_icon_href():
    config = {
        'types': {
            'tag': {
                'title': 'Tag',
                'icon': 'material-tag',
                'icon_href': 'https://example.com',
                'text': 'Tag',
        }
    }}

    markdown_text = '[badge:tag]'

    expected_html = R'''
    <span class="mdx-badge mdx-badge--tag">
    <a href="https://example.com" class="mdx-badge__link">
    <span class="mdx-badge__icon" title="Tag">:material-tag:</span>
    </a>
    <span class="mdx-badge__text">Tag</span>
    </span>
    '''

    _test(markdown_text, expected_html, config)


def test_typed_badge_with_reference():
    badges_config = {
        'types': {
            'tag': {
                'reference': 'badges.md',
                'text': 'Tag',
        }
    }}
    mkdocs_config = load_config(
        "tests/mkdocs.yml",
        docs_dir="docs/",
        plugins={"badges": badges_config},
    )
    build(mkdocs_config)

    site_dir = mkdocs_config["site_dir"]

    # Works, but, is it what are we looking for?
    expected_html = R'''
    <span class="mdx-badge mdx-badge--tag">
    <a href="../badges.md" class="mdx-badge__link">
    <span class="mdx-badge__text">Tag</span>
    </a>
    </span>
    '''
    expected_html = _dedent(expected_html)

    with open(site_dir+'/tests/badge_reference/index.html') as f:
        badges = re.findall(r"(\w+): <strong>(.*?)</strong>", f.read())
        actual_html = next((badge[1] for badge in badges if badge[0] == 'tag'), None)

        assert expected_html == actual_html
