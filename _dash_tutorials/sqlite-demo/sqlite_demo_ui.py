"""Demonstrate realtime updates from a SQLite db.

Example Python/SQLite: https://www.dataquest.io/blog/python-pandas-databases/
    https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

TODO: https://plot.ly/python/big-data-analytics-with-pandas-and-sqlite/

"""

import sqlite3
from pathlib import Path

import bottleneck
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash_charts.utils_fig import min_graph

dbFile = Path.cwd() / 'sqlite-demo.sqlite'
points = 1000

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div(
        className='section',
        children=[
            html.H1(children='SQLite/Dash Testing'),
            min_graph(id='sqlite-scatter', animate=True),
            dcc.Interval(id='graph-update', interval=400, n_intervals=0),
        ],
    ),
])


@app.callback(
    Output('sqlite-scatter', 'figure'),
    [Input('graph-update', 'n_intervals')])
def updateScatter(n_intervals):
    """Update the scatter plot with latest from db."""
    conn = sqlite3.connect(dbFile)
    df = pd.read_sql_query('SELECT ID,LABEL,VALUE from EVENTS', conn)
    conn.close()
    # Demo fitting wth a polynomial (not that useful)
    fit = np.poly1d(np.polyfit(df['ID'], df['VALUE'], 5))
    # Demo using a moving mean/std
    rollingMean = bottleneck.move_mean(df['VALUE'], 5)
    rollingSTD = bottleneck.move_std(df['VALUE'], 5)
    return {
        'data': [
            go.Scatter(
                mode='markers',
                name='scatter',
                text=df['LABEL'],
                x=df['ID'],
                y=df['VALUE'],
                opacity=0.3,
            ),
            go.Scatter(
                name='2x STD',
                fill='toself',
                x=list(df['ID']) + list(df['ID'])[::-1],
                y=list(np.add(rollingMean, np.multiply(2, rollingSTD))) + \
                list(np.subtract(rollingMean, np.multiply(2, rollingSTD)))[::-1],
                opacity=0.5,
            ),
            go.Scatter(
                # line={'color': '#D93D40', 'dash': 'solid'},
                mode='lines',
                name='fit',
                x=df['ID'],
                y=fit(df['ID']),
                opacity=0.7,
            ),
            go.Scatter(
                mode='lines',
                name='move_mean',
                x=df['ID'],
                y=rollingMean,
                opacity=0.9,
            ),
        ],
        'layout': go.Layout(
            title=go.layout.Title(text='Live-Updating Plot'),
            xaxis={
                'automargin': True,
                # 'autorange': True,  # FYI: requires full page refresh
                'range': [0, points],
                'showgrid': True,
                'title': 'Index',
            },
            yaxis={
                'automargin': True,
                'zeroline': True,
                'autorange': True,
                'showgrid': True,
                'title': 'VALUE',
            },
            legend={'orientation': 'h'},
            hovermode='closest',
        ),
    }


if __name__ == '__main__':
    app.run_server(debug=True)
