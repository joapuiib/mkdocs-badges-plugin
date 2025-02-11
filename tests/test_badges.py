import textwrap

from mkdocs_badges_plugin.plugin import BadgesPlugin

def _test(markdown_text, expected_html, config={}):
    plugin = BadgesPlugin()
    plugin.load_config(config)

    expected_html = "".join(textwrap.dedent(expected_html).strip().split("\n"))

    html = plugin.replace_badges(markdown_text)
    assert html == expected_html


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
