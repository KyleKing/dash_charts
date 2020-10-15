"""Add a nested Table of Contents to any HTML file with BeautifulSoup and dominate."""

from bs4 import BeautifulSoup
from dominate import tags

TOC_KEYWORD = '{{toc}}'
"""Default string to replace in the specified file with the nested table of contents. Default is `{{toc}}`."""


def add_nested_list_item(l_index, l_string, level=1):
    """Add nested list items recursively.

    Args:
        l_index: numeric index of the list depth (note: 1-indexed)
        l_string: string to show in the list element
        level: current list depth. Optional and default is 1

    """
    with tags.ul():
        if l_index != level:
            add_nested_list_item(l_index, l_string, level + 1)
        else:
            tags.li(f'H{l_index}: {l_string}')


def create_toc(html_text, header_depth=3):
    """Return the HTML for a nested table of contents based on the HTML file path.

    Args:
        html_text: HTML text
        header_depth: depth of headers to show. Default is 3 (H1-H3)

    Returns:
        string: table of contents

    """
    soup = BeautifulSoup(html_text, features='lxml')
    h_lookup = {f'h{idx}': idx for idx in range(1, header_depth + 1)}
    toc = tags.div()
    for header in soup.findAll([*h_lookup.keys()]):
        with toc:
            add_nested_list_item(h_lookup[header.name], header.string)
            # FIXME: Figure out how to make the header links work (i.e. when clicked in TOC go to the respective header)
            # > `tags.a(header.string, f'#{header.string}')`?
    return str(toc)


def write_toc(html_path, header_depth=3, toc_key=TOC_KEYWORD):
    """Write the nested table of contents to the specified file.

    Args:
        html_path: path to the HTML file
        header_depth: depth of headers to show. Default is 3 (H1-H3)
        toc_key: string to replace with the nested table of contents. Default is `TOC_KEYWORD`

    Raises:
        RuntimeError: if the key was not found in the file

    """
    text = html_path.read_text()
    if toc_key not in text:
        raise RuntimeError(f'HTML file does not have the table of contents key ({toc_key}): {html_path}')
    toc = create_toc(text, header_depth=header_depth)
    html_path.write_text(text.replace('{{toc}}', toc))
