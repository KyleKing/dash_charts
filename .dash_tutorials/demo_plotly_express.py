"""Example using Plotly Express.

Examples: https://www.plotly.express/
Docs: https://www.plotly.express/plotly_express/

"""

import dash_core_components as dcc
import dash_html_components as html
import plotly_express as px
from _config import app
from dash.dependencies import Input, Output
from dash_charts.helpers import MinGraph
from icecream import ic

tips = px.data.tips()
colOpts = [dict(label=x, value=x) for x in tips.columns]

fnMap = {
    'histogram()': px.histogram,
    'scatter()': px.scatter,
    'line()': px.line,
    'area()': px.area,
    'density_contour()': px.density_contour,
    'strip()': px.strip,
    'box()': px.box,
    'violin()': px.violin,

    # # Other plots, but which need a different source data set
    # 'density_heatmap()': px.density_heatmap,
    # 'bar()': px.bar,
    # 'scatter_ternary()': px.scatter_ternary,  # < Cool!
    # 'line_ternary()': px.line_ternary,  # < Cool!
    # 'scatter_polar()': px.scatter_polar,
    # 'scatter_line()': px.scatter_line,
    # 'scatter_bar()': px.scatter_bar,
    # 'scatter_matrix()': px.scatter_matrix,
    # 'parallel_coordinates()': px.parallel_coordinates,
}
funcOpts = [dict(label=_x, value=_x) for _x in fnMap.keys()]

dimensions = ['x', 'y', 'color', 'size', 'facet_col', 'facet_row']

app.layout = html.Div([
    html.H1('Demo: Plotly Express in Dash with Tips Dataset'),
    html.Div(
        [
            html.P(['Plot Type:', dcc.Dropdown(id='func', options=funcOpts, value=funcOpts[0]['value'])]),
        ] + [
            html.P(
                [_d + ':', dcc.Dropdown(id=_d, options=colOpts)]
            ) for idx, _d in enumerate(dimensions)
        ],
        style={'width': '25%', 'float': 'left'},
    ),
    MinGraph(id='graph', style={'width': '75%', 'display': 'inline-block'}),
])


@app.callback(
    Output('graph', 'figure'),
    [Input('func', 'value')] + [Input(d, 'value') for d in dimensions])
def make_figure(fnName, x, y, color, size, facet_col, facet_row):
    """Create the px figure."""
    ic(fnName, x, y)
    # Ensure that the minimum parameters exist
    if fnName is None:
        fnName = funcOpts[0]['value']
    if x is None:
        x = colOpts[0]['value']
    if y is None:
        y = colOpts[1]['value']
    # Return the figure from plotly express
    return fnMap[fnName](
        tips,
        x=x,
        y=y,
        # color=color,
        # size=size,
        # facet_col=facet_col,
        # facet_row=facet_row,
        height=700,
        # marginal_x="histogram",
        # marginal_y="histogram",
        # # Alt: histogram, rug, box, violin
    )

    # # Plotting color swatches
    # return px.colors.diverging.swatches()


if __name__ == '__main__':
    app.run_server(debug=True)
