# -*- coding: utf-8 -*-
"""Distortion chart.

dash ref: https://dash.plot.ly/
plotly ref: https://plot.ly/python/reference/

"""

import math
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

assets_dir = Path.cwd() / 'assets/styles.css'
app = dash.Dash(__name__, assets_url_path=str(assets_dir))

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


def createDistortion(df, factor):
    """TODO."""
    measLabels = []
    xData = {'Ideal': [], 'Meas': []}
    yData = {'Ideal': [], 'Meas': []}
    for row in df.itertuples():
        measLabels.append(row.label)
        xData['Ideal'].append(row.x)
        yData['Ideal'].append(row.y)
        xData['Meas'].append(row.x + factor * row.xDelta)
        yData['Meas'].append(row.y + factor * row.yDelta)

    return {
        'data': [
            go.Scatter(
                mode='markers',
                name=lbl,
                text=measLabels if lbl == 'Meas' else lbl,
                x=xData[lbl],
                y=yData[lbl],
                marker={'size': 5 if lbl == 'Meas' else 7},
            ) for lbl in ['Ideal', 'Meas']
        ] + [
            go.Scatter(
                line={'color': '#D93D40', 'dash': 'solid'},
                mode='lines',
                opacity=0.4,
                legendgroup='Connection',
                showlegend=False,
                x=[xData['Ideal'][idx], xData['Meas'][idx]],
                y=[yData['Ideal'][idx], yData['Meas'][idx]],
            ) for idx in range(len(measLabels))
        ],
        'layout': go.Layout(
            title=go.layout.Title(text='Demo Plot'),
            xaxis={
                'range': [0, math.ceil(max(xData['Ideal'] + xData['Meas']))],
                'showgrid': True,
                'title': 'XAxisLabel',
            },
            yaxis={
                'range': [0, math.ceil(max(yData['Ideal'] + yData['Meas']))],
                'showgrid': True,
                'title': 'YAxisLabel',
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
