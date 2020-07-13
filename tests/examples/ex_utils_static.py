"""Example Static HTML file output."""

import json
import webbrowser
from pathlib import Path

import dash_bootstrap_components as dbc
import jsonpickle
import pandas as pd
import plotly.express as px
from dash_charts import equations
from dash_charts.dash_helpers import json_dumps_compact
from dash_charts.scatter_line_charts import FittedChart
from dash_charts.utils_static import (add_image, create_dbc_doc, make_div, tag_code, tag_markdown, tag_table,
                                      write_from_markdown, write_image_file)
from dominate import tags, util

# TODO: Add tests for: utils_static.add_video and utils_static.write_lookup


def test_write_image_file(image_path, figure):
    """Test writing an image file."""
    if image_path.is_file():
        image_path.unlink()
    write_image_file(figure, image_path, image_path.suffix[1:])
    assert image_path.is_file()


def create_sample_custom_chart_figure():
    """Return figure dictionary using CustomChart classes.

    Returns:
        dict: chart figure

    """
    chart_main = FittedChart(
        title='Sample Fitted Scatter Data',
        xlabel='Index',
        ylabel='Measured Value',
    )
    chart_main.fit_eqs = [('linear', equations.linear)]
    # Create dataframe based on px sample dataset
    iris = px.data.iris()
    data_raw = pd.DataFrame(data={
        'name': iris['species'],
        'x': iris['petal_width'],
        'y': iris['petal_length'],
        'label': None,
    })
    return chart_main.create_figure(df_raw=data_raw)


def write_sample_html(filename):
    """Write static HTML.

    Args:
        filename: path to write the HTML file

    """
    image_path = Path(__file__).parent / 'test_write_image_file.png'
    figure = px.scatter(x=range(10), y=range(10))
    test_write_image_file(image_path, figure)

    # Configure dark theme
    custom_styles = 'pre {max-height: 400px;}'
    doc = create_dbc_doc(dbc.themes.DARKLY, custom_styles, title='Example Static File')
    with doc.head:
        tags.link(rel='stylesheet', href=('https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.13.1/build/styles/'
                                          'tomorrow-night-eighties.min.css'))

    figure = create_sample_custom_chart_figure()
    px_figure = px.scatter(x=[*range(10)][::-1], y=range(10), template='plotly_dark')
    px_figure_json = jsonpickle.encode(px_figure['layout'], unpicklable=False)
    with doc:
        with tags.div(_class='container').add(tags.div(_class='col')):
            tags.h1('Example Creating Static HTML')
            tags.p('Charts still have hover and zoom features, but there is no way to use callbacks in static HTML')
            util.raw(make_div(figure))
            tags.hr()

            tags.h1('Example Table')
            tag_table(px.data.iris().head(5))

            tags.hr()
            tags.h1('Example Code')
            tag_code((Path(__file__).parent / 'readme.py').read_text(), language='language-py')

            tags.hr()
            tags.h1('Markdown Examples')
            md_string = '# Hello Markdown!\n\n[HLJS Demo](https://highlightjs.org/static/demo/)'
            tags.p('Shown as raw code below')
            tag_code(md_string, language='language-md')
            tags.p('Shown as formatted HTML')
            tag_markdown(md_string)

            tags.hr()
            tags.h1('Example image')
            util.raw(add_image(image_path))
            # util.raw(add_video(video_path))

            tags.hr()
            tags.h1('Another Chart For Good Measure')
            util.raw(make_div(px_figure))
            tags.br()
            tags.p('JSON representation of the px_figure layout')
            tag_code(json_dumps_compact(json.loads(px_figure_json)), language='language-json')

    filename.write_text(str(doc))


def example_write_from_markdown():
    """Demonstrate the write_from_markdown function.

    Returns:
        Path: path to created HTMl file

    """
    filename = Path(__file__).parent / 'example_write_from_markdown.md'
    figure_px = px.scatter(x=range(10), y=range(10))
    function_lookup = {
        'make_div(figure_px)': (make_div, [figure_px]),
        'table(iris_data)': (tag_table, [px.data.iris().head(10)]),
    }
    return write_from_markdown(filename, function_lookup)


if __name__ == '__main__':
    # Create all HTML content in Python
    filename = Path(__file__).parent / 'tmp.html'
    write_sample_html(filename)
    webbrowser.open(filename.resolve().as_uri())

    # Alternatively, read from a Markdown file (note: both methods can be combined)
    filename_from_md = example_write_from_markdown()
    webbrowser.open(filename_from_md.resolve().as_uri())
