"""Example using Plotly Express.

Examples: https://www.plotly.express/
Docs: https://www.plotly.express/plotly_express/

"""

import dash_core_components as dcc
import dash_html_components as html
import plotly_express as px
from dash.dependencies import Input, Output
from dash_charts.utils_app import init_app
from dash_charts.utils_fig import min_graph
from icecream import ic

app = init_app()

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
}
funcOpts = [dict(label=_x, value=_x) for _x in fnMap.keys()]

dimensions = ['x', 'y', 'color', 'facet_col', 'facet_row']

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
    min_graph(id='graph', style={'width': '75%', 'display': 'inline-block'}),
])


@app.callback(
    Output('graph', 'figure'),
    [Input('func', 'value')] + [Input(d, 'value') for d in dimensions])
def make_figure(fnName, x, y, color, facet_col, facet_row):
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
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=700,
    )


if __name__ == '__main__':
    app.run_server(debug=True)
