"""Distortion chart."""

import math
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__, assets_folder=str(Path.cwd() / 'examples/assets'))

app.layout = html.Div(
    className='app-content',
    children=[
        html.H4(children='Project'),
        html.Div([dcc.Graph(id='distortion-chart')]),
        dcc.Slider(id='factor-input', min=0, max=20, step=0.1, value=5),
        html.Div(id='slider-output-container'),
        html.Button('Reset Factor to 1', id='reset-button'),
    ],
)


def createDistortion(df, title='', measLbl='Meas', idealLbl='Ideal', xLbl='', yLbl='', pad=0, stretch=1):
    """Create an alignment chart to pot an ideal location and the measured location. User can change the stretch.

    TODO: Plot multiple alignments on the same chart

    ```py
    # Example dataframe
    dfDemo = pd.DataFrame(data={
        'x': [1, 2, 1, 2],
        'y': [1, 2, 2, 1],
        'xDelta': [0.01, 0.02, 0.005, -0.04],
        'yDelta': [0.01, -0.05, 0.005, 0.005],
        'label': ['A', 'B', 'C', 'D'],
    })
    ```

    df -- Pandas dataframe with columns names: ['x', 'y', 'xDelta', 'yDelta', 'label']
    title -- optional, string title for chart. Defaults to blank
    measLbl/idealLbl -- optional, legend names for the respective values
    xLbl/yLbl -- optional, X and Y Axis axis titles. Defaults to blank
    pad -- optional, padding around the points within the chart. Defaults to 0
    stretch -- optional, float factor value to change the spacing between ideal and measured coordinates

    """
    # Format data into lists
    measLabels = []
    data = {
        'x': {idealLbl: [], measLbl: []},
        'y': {idealLbl: [], measLbl: []},
    }
    for row in df.itertuples():
        measLabels.append(row.label)
        data['x'][idealLbl].append(row.x)
        data['y'][idealLbl].append(row.y)
        data['x'][measLbl].append(row.x + stretch * row.xDelta)
        data['y'][measLbl].append(row.y + stretch * row.yDelta)

    return {
        'data': [
            go.Scatter(
                mode='markers',
                name=lbl,
                text=measLabels if lbl == measLbl else lbl,
                opacity=1 if lbl == measLbl else 0.25,
                x=data['x'][lbl],
                y=data['y'][lbl],
            ) for lbl in [idealLbl, measLbl]
        ] + [
            go.Scatter(
                line={'color': '#D93D40', 'dash': 'solid'},
                mode='lines',
                opacity=0.15,
                legendgroup='Visual-Guides',
                showlegend=False,
                x=[data['x'][idealLbl][idx], data['x'][measLbl][idx]],
                y=[data['y'][idealLbl][idx], data['y'][measLbl][idx]],
            ) for idx in range(len(measLabels))
        ],
        'layout': go.Layout(
            title=go.layout.Title(text=title),
            xaxis={
                'range': [0, math.ceil(max(data['x'][idealLbl] + data['x'][measLbl]) + pad)],
                'showgrid': True,
                'title': xLbl,
            },
            yaxis={
                'range': [0, math.ceil(max(data['y'][idealLbl] + data['y'][measLbl]) + pad)],
                'showgrid': True,
                'title': yLbl,
            },
            legend=dict(orientation='h'),
            hovermode='closest',
        ),
    }


dfDemo = pd.DataFrame(data={
    'x': [1, 2, 1, 2],
    'y': [1, 2, 2, 1],
    'xDelta': [0.01, 0.02, 0.005, -0.04],
    'yDelta': [0.01, -0.05, 0.005, 0.005],
    'label': ['A', 'B', 'C', 'D'],
})


@app.callback(
    Output('distortion-chart', 'figure'),
    [Input('factor-input', 'value')])
def updateDistChart(factor):
    """TODO."""
    return createDistortion(dfDemo, factor)


@app.callback(
    Output('slider-output-container', 'children'),
    [Input('factor-input', 'value')])
def indicateSliderPos(factor):
    """TODO."""
    return 'Selected factor: `{}`'.format(factor)


@app.callback(
    Output('factor-input', 'value'),
    [Input('reset-button', 'n_clicks')])
def resetFactor(_n_clicks):
    """TODO."""
    return 1


if __name__ == '__main__':
    app.run_server(debug=True)
