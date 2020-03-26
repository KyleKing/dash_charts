"""Example Static HTML file output."""

import json
import webbrowser
from pathlib import Path

import dash_bootstrap_components as dbc
import jsonpickle
import pandas as pd
import plotly.express as px
from dash_charts import equations
from dash_charts.fitted_chart import FittedChart
from dash_charts.utils_static import create_dbc_doc, make_div, tag_code, tag_table
from dominate import tags, util


def create_sample_custom_chart_figure():
    """Return figure dictionary using CustomChart classes.

    Returns:
        TODO

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
            tag_code('# Hello Markdown!\n\n[HLJS Demo](https://highlightjs.org/static/demo/)', language='language-md')
            tag_code((Path(__file__).parent / 'readme.py').read_text(), language='language-py')

            tags.hr()
            tags.h1('Another Chart For Good Measure')
            util.raw(make_div(px_figure))
            tag_code(json.dumps(json.loads(px_figure_json), indent=4), language='language-json')

    filename.write_text(str(doc))


if __name__ == '__main__':
    filename = Path(__file__).parent / 'tmp.html'
    write_sample_html(filename)
    webbrowser.open(filename.resolve().as_uri())
