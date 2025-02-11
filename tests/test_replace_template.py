import textwrap

from mkdocs.commands.build import build
from mkdocs.config.base import load_config

import re

def _dedent(text):
    return "".join(textwrap.dedent(text).strip().split("\n"))


def test_render_badge_document():
    mkdocs_config = load_config(
        "tests/mkdocs.yml",
        plugins={
            'badges': {
                'types': {
                    'tag': {
                        'title': 'Tag',
                        'icon': 'material-tag'
                    }
                }
            }
        },
    )

    build(mkdocs_config)
    site_dir = mkdocs_config["site_dir"]

    with open(site_dir+'/badges/index.html') as f:
        badges = re.findall(r"(\w+): <strong>(.*?)</strong>", f.read())

        expected_tag_badge = R'''
        <span class="mdx-badge mdx-badge--tag">
        <span class="mdx-badge__icon" title="Tag">:material-tag:</span>
        <span class="mdx-badge__text"><code>Example</code></span>
        </span>
        '''
        expected_tag_badge = _dedent(expected_tag_badge)

        actual_tag_badge = next((badge[1] for badge in badges if badge[0] == 'tag'), None)
        assert expected_tag_badge == actual_tag_badge

