"""Demonstrate realtime updates from a SQLite db.

Example Python/SQLite: https://www.dataquest.io/blog/python-pandas-databases/
    https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

TODO: https://plot.ly/python/big-data-analytics-with-pandas-and-sqlite/

"""

import sqlite3
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

dbFile = Path.cwd() / 'pages/assets/sqlite-demo.sqlite'

app = dash.Dash(__name__, assets_folder=str(Path.cwd() / 'pages/assets'))
app.layout = html.Div([
    html.Div(
        className='app-content',
        children=[
            html.H1(
                children='SQLite/Dash Testing',
            ),
            dcc.Graph(id='sqlite-scatter', animate=True),
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
    # cursor = conn.cursor()
    # cursor.execute("SELECT id, name, marks from SCHOOL").fetchall()
    df = pd.read_sql_query('SELECT id, name, age from SCHOOL', conn)

    conn.close()

    fit = np.poly1d(np.polyfit(df['ID'], df['AGE'], 5))

    return {
        'data': [
            go.Scatter(
                mode='markers',
                text=df['NAME'],
                x=df['ID'],
                y=df['AGE'],
            ),
            go.Scatter(
                # line={'color': '#D93D40', 'dash': 'solid'},
                mode='lines',
                x=df['ID'],
                y=fit(df['ID']),
                # opacity=0.4,
            ),
        ],
        'layout': go.Layout(
            title=go.layout.Title(text='Live-Updating Plot'),
            xaxis={
                'automargin': True,
                # 'autorange': True,  # FIXME: forces full page refresh on range change?
                'range': [0, 1000],
                'showgrid': True,
                'title': 'Index',
            },
            yaxis={
                'automargin': True,
                'zeroline': True,
                # 'autorange': True,  # FIXME: Doesn't work
                'range': [-150, 150],
                'showgrid': True,
                'title': 'Age',
            },
            hovermode='closest',
        ),
    }


if __name__ == '__main__':
    app.run_server(debug=True)
