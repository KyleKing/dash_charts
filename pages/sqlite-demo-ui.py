"""Demonstrate realtime updates from a SQLite db.

See: https://www.dataquest.io/blog/python-pandas-databases/

"""

import sqlite3
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
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
            dcc.Graph(id='sqlite-scatter'),
            html.Button('UPDATE', id='update-button'),
        ],
    ),
])


@app.callback(
    Output('sqlite-scatter', 'figure'),
    [Input('update-button', 'n_clicks')])
def updateScatter(_n_clicks):
    """Update the scatter plot with latest from db."""
    conn = sqlite3.connect(dbFile)
    # cursor = conn.cursor()
    # cursor.execute("SELECT id, name, marks from SCHOOL").fetchall()
    df = pd.read_sql_query('SELECT id, name, age from SCHOOL', conn)

    conn.close()

    return {
        'data': [
            go.Scatter(
                mode='markers',
                text=df['NAME'],
                x=df['ID'],
                y=df['AGE'],
            ),
        ],
        'layout': go.Layout(
            title=go.layout.Title(text='Live-Updating Plot'),
            xaxis={
                'showgrid': True,
                'title': 'Index',
            },
            yaxis={
                'showgrid': True,
                'title': 'Age',
            },
            hovermode='closest',
        ),
    }


if __name__ == '__main__':
    # FYI: For PyInstaller, debug must be False. Otherwise returns:
    #   "AttributeError: 'FrozenImporter' object has no attribute 'filename'"
    app.run_server(debug=False)
