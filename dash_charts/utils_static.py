"""Utilities for generating static HTML reports."""

import io
from base64 import b64encode

import dash_bootstrap_components as dbc
import dominate
import markdown
import pandas as pd
import plotly.io
from bs4 import BeautifulSoup
from dominate import tags, util


def write_div(figure, path_or_file_object, is_div=True, **html_kwargs):
    """Write Plotly figure as HTML to specified file.

    Args:
        figure: Plotly figure (can be from `create_figure` for custom charts)
        path_or_file_object: *string* path or file object
        is_div: if True (default) will override html_kwargs to only write the minimum HTML needed
        html_kwargs: additional keyword arguments passed to `plotly.io.write_html()`

    """
    for key in ['include_plotlyjs', 'full_html']:
        if key not in html_kwargs and is_div:
            html_kwargs[key] = False

    plotly.io.write_html(fig=figure, file=path_or_file_object, **html_kwargs)


def make_div(figure, **html_kwargs):
    """Write Plotly figure as HTML to specified file.

    Args:
        figure: Plotly figure (can be from `create_figure` for custom charts)
        html_kwargs: additional keyword arguments passed to `plotly.io.write_html()`

    Returns:
        str: HTML div

    """
    with io.StringIO() as output:
        write_div(figure, output, is_div=True, **html_kwargs)
        return output.getvalue()


def add_image(image_path, alt_text=None):
    """Write base64 image to HTML.

    Args:
        image_path: Path to image file and format will be read from file suffix.
        alt_text: alternate text. If None, will show the image filename

    Returns:
        str: HTML

    """
    with open(image_path, 'rb') as image_file:
        encoded_image = b64encode(image_file.read()).decode()
    image_uri = f'data:image/{image_path.suffix[1:]};base64,{encoded_image}'
    return f'<img src="{image_uri}" alt="{alt_text or image_path.name}"/>'


def add_video(video_path, alt_text=None):
    """Write base64 video to HTML.

    Video formats can easily be converted with ffmpeg: `ffmpeg -i video_filename.mov video_filename.webm`

    Args:
        video_path: Path to video file and format will be read from file suffix. Video should be in webm format
        alt_text: alternate text. If None, will show the video filename

    Returns:
        str: HTML video tag

    """
    with open(video_path, 'rb') as video_file:
        encoded_video = b64encode(video_file.read()).decode()
    video_uri = f'data:video/{video_path.suffix[1:]};base64,{encoded_video}'
    return f'<video src="{video_uri}" controls>{alt_text or video_path.name}</video>'


def write_image_file(figure, path_or_file_object, image_format, **img_kwargs):
    """Write Plotly figure as an image to specified file.

    Args:
        figure: Plotly figure (can be from `create_figure` for custom charts)
        path_or_file_object: *string* path or file object
        image_format: one of `(png, jpg, jpeg, webp, svg, pdf)`
        img_kwargs: additional keyword arguments passed to `plotly.io.write_image()`

    """
    plotly.io.write_image(fig=figure, file=str(path_or_file_object), format=image_format, **img_kwargs)


def capture_plotly_body():
    """Return HTML body that includes necessary scripts for Plotly and MathJax.

    Returns:
        tuple: of the top and the bottom HTML content

    """
    # Capture necessary Plotly boilerplate HTML
    with io.StringIO() as output:
        write_div({}, output, is_div=False, include_mathjax='.js', validate=False)
        blank_plotly = BeautifulSoup(output.getvalue(), features='lxml')
    # Remove the empty figure div and corresponding script
    plot_div = blank_plotly.find('div', attrs={'class': 'plotly-graph-div'})
    for script in blank_plotly.find_all('script')[::-1]:
        # Use the ID from the plot to identify which script needs to be removed
        if plot_div.attrs['id'] in script.prettify():
            script.decompose()
            break
    plot_div.decompose()
    return blank_plotly.body.prettify()


def format_plotly_boilerplate(**doc_kwargs):
    """Initialize a boilerplate dominate document for creating static Plotly HTML files.

    See dominate documentation: https://pypi.org/project/dominate/

    Args:
        doc_kwargs: keyword arguments for `dominate.document()`

    Returns:
        dict: dominate document instance

    """
    doc = dominate.document(**doc_kwargs)
    with doc:
        util.raw(capture_plotly_body())
    return doc


def create_dbc_doc(theme=dbc.themes.BOOTSTRAP, custom_styles='', **doc_kwargs):
    """Create boilerplate dominate document with Bootstrap and Plotly for static HTML.

    Based on: https://github.com/facultyai/dash-bootstrap-components/tree/master/docs/templates/partials

    See dominate documentation: https://pypi.org/project/dominate/

    Args:
        theme: string URL to CSS for theming Bootstrap. Default is `dbc.themes.BOOTSTRAP`
        custom_styles: optional custom CSS to add to file. Default is blank (`''`)
        doc_kwargs: keyword arguments for `dominate.document()`

    Returns:
        dict: dominate document instance

    """
    stylesheets = [
        {'href': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.13.1/build/styles/a11y-light.min.css'},
        {'href': theme},
    ]
    scripts = [
        {'src': 'https://code.jquery.com/jquery-3.4.1.slim.min.js'},
        {'src': 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js'},
        {'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'},
        {'src': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.13.1/build/highlight.min.js'},
    ]

    doc = format_plotly_boilerplate(**doc_kwargs)
    with doc.head:
        tags.meta(charset='utf-8')
        tags.meta(name='viewport', content='width=device-width, initial-scale=1')
        for sheet_kwargs in stylesheets:
            tags.link(rel='stylesheet', **sheet_kwargs)
        util.raw(f'<style>{custom_styles}</style>')
        for script_kwargs in scripts:
            tags.script(**script_kwargs)
        util.raw('<script>hljs.initHighlightingOnLoad();</script>')

    return doc


def tag_code(text, language=''):
    """Format HTML for a `pre.code` block with specified `hljs` language.

    Args:
        text: string to show in code block
        language: `hljs` language (ex: `'language-json'`). Default is `''`.

    """
    tags.pre().add(tags.code(text, _class=f'{language} hljs'))


def tag_markdown(text, **markdown_kwargs):
    """Format markdown text as HTML.

    Args:
        text: markdown string
        markdown_kwargs: additional keyword arguments for `markdown.markdown`, such as `extensions`

    """
    util.raw(markdown.markdown(text, **markdown_kwargs))


def tag_table(df_table, table_class=None):
    """Format HTML for a responsive Bootstrap table.

    See Bootstrap documentation at: https://getbootstrap.com/docs/4.4/content/tables/#tables

    Args:
        df_table: pandas dataframe to show in table
        table_class: string classes to add to table. If None, will use default string

    Raises:
        RuntimeError: if `df_table` is not a DataFrame object

    """
    if table_class is None:
        table_class = 'table table-bordered table-striped table-hover'
    if not isinstance(df_table, pd.core.frame.DataFrame):
        raise RuntimeError(f'df_table is not a DataFrame ({type(df_table)}):\n{df_table}')

    df_table = df_table.reset_index()

    with tags.div(_class='table-responsive').add(tags.table(_class=table_class)):
        # Create header row
        with tags.thead().add(tags.tr()):
            for col in df_table.columns:
                tags.th(col)
        # Create body rows
        with tags.tbody():
            for row in df_table.itertuples(index=False):
                with tags.tr():
                    for value in row:
                        tags.td(str(value))


def write_lookup(key, function_lookup):
    """Determine the lookup result and add to the file.

    Args:
        key: string key for function lookup
        function_lookup: dictionary with either the string result or equation and arguments

    Raises:
        RuntimeError: if error in lookup dictionary

    """
    try:
        match = function_lookup[key]
    except KeyError:
        raise RuntimeError(f'Could not find "{key}" in {function_lookup}')

    if isinstance(match, str):
        util.raw(match)
    elif len(match) == 2:
        fun, args = match
        result = fun(*args)
        if isinstance(result, str):
            util.raw(result)
    else:
        raise RuntimeError(f'Match failed for "{key}". Returned: {match} from {function_lookup}')


def markdown_machine(lines, function_lookup):  # noqa: CCR001
    """Convert markdown text file into Plotly-HTML and write to doc context.

    Note: you will need a document with necessary boilerplate and call this within a `with doc:` dominate context
    Multiple Markdown files can then be put into a single HTML output file by calling this function with new lines
    and function lookup arguments

    Args:
        lines: list of text file lines
        function_lookup: dictionary with either the string result or equation and arguments
            Will be inserted into file where `>>lookup:function_name` assuming key of `function_name`

    """
    markdown_lines = []
    for line in lines:
        if line.startswith('>>lookup:'):
            # Write stored markdown and clear list. Then write the matched lookup
            tag_markdown('\n'.join(markdown_lines))
            markdown_lines = []
            write_lookup(line.split('>>lookup:')[1], function_lookup)
        else:
            markdown_lines.append(line)
    if markdown_lines:
        tag_markdown('\n'.join(markdown_lines))


def write_from_markdown(filename, function_lookup, **dbc_kwargs):
    """Wrap markdown_machine to convert markdown to Bootstrap HTML.

    Args:
        filename: path to markdown file
        function_lookup: dictionary with either the string result or equation and arguments
            Will be inserted into file where `>>lookup:function_name` assuming key of `function_name`
        dbc_kwargs: keyword arguments to pass to `create_dbc_doc`

    Returns:
        Path: created HTML filename

    """
    lines = filename.read_text().split('\n')
    html_filename = filename.parent / f'{filename.stem}.html'
    doc = create_dbc_doc(**dbc_kwargs)
    with doc:
        with tags.div(_class='container').add(tags.div(_class='col')):
            markdown_machine(lines, function_lookup)

    html_filename.write_text(str(doc))
    return html_filename
