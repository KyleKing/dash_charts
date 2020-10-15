"""Test utils_static_toc.py."""

import dominate
from dominate import tags, util

from dash_charts.utils_static_toc import TOC_KEYWORD, write_toc

from .configuration import TEST_DATA_DIR


def write_test_html(html_path):
    """Create a test HTML file for the specified HTML path."""
    doc = dominate.document()
    with doc.head:
        tags.meta(charset='utf-8')
        tags.meta(name='viewport', content='width=device-width, initial-scale=1')
    with doc:
        with tags.div(_class='container').add(tags.div(_class='col')):
            tags.h1('Example Header 1')
            util.raw(TOC_KEYWORD)
            tags.h2('Example Header 2')
            tags.h2('Example Header 2')
            tags.h3('Example Header 3')
            tags.h4('Example Header 4')
            tags.h5('Example Header 5')
            tags.h6('Example Header 6')
    html_path.write_text(str(doc))


def test_utils_static_toc():
    """Test utils_static_toc."""
    html_expected = TEST_DATA_DIR / 'test_utils_static_toc-expected.html'  # in VCS
    html_path = html_expected.parent / 'test_utils_static_toc-test.html'
    write_test_html(html_path)
    write_toc(html_path)

    result = html_path.read_text().strip()

    assert html_expected.read_text().strip() == result
    html_path.unlink()
