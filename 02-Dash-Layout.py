# -*- coding: utf-8 -*-
"""02, Dash Layout.

Based on: https://dash.plot.ly/getting-started.

For reference see:

[Core Dash Components](https://dash.plot.ly/dash-core-components)
[HTML Components](https://dash.plot.ly/dash-html-components)

"""

import random

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from random_word import RandomWords

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # {'src': 'file:///Users/kyleking/Developer/Werk/__LocalProjects/Dash-HelloWorld/assets/styles.css'},
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # , assets_url_path='../')

colors = {
    'background': '#FFF',
    'text': '#26335C'
}

# =====================================================================================================================
# Barchart

# Create data for Bar Chart
rWords = RandomWords()
try:
    x = rWords.get_random_words(limit=20)
except Exception:  # Known API Error, see: https://github.com/vaibhavsingh97/random-word/issues/13
    x = ['Test123', 'Test234']


def randY():
    """Generate Random Y Coordinates."""
    return [random.randint(1, 50) for __ in x]


# =====================================================================================================================
# Table

agricDF = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


def generate_table(dataframe, max_rows=10, max_cols=10):
    """Reusable Pandas HTML data table component."""
    return html.Table(
        [
            html.Tr([html.Th(col) for cIdx, col in enumerate(dataframe.columns) if cIdx < max_cols])
        ] + [
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for cIdx, col in enumerate(dataframe.columns) if cIdx < max_cols
            ]) for i in range(min(len(dataframe), max_rows))
        ]
    )


# =====================================================================================================================
# Configure Scatter Plot

lifeExpDF = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/'
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

# =====================================================================================================================
# Layout the application

app.layout = html.Div([
    html.Div(
        className="app-content",
        children=[
            html.H1(
                children='Dash: Hello Barchart',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            html.Div(children='When Random Words meet Random Numbers', style={
                'textAlign': 'center',
                'color': colors['text']
            }),
            dcc.Graph(
                id='example-graph-2',
                figure={
                    'data': [
                        {'x': x, 'y': randY(), 'type': 'bar', 'name': 'Montréal'},
                        {'x': x, 'y': randY(), 'type': 'bar', 'name': 'Baltimore'},
                        {'x': x, 'y': randY(), 'type': 'bar', 'name': 'Washington DC'},
                    ],
                    'layout': {
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text']
                        }
                    }
                }
            ),

            html.H4(children='US Agriculture Exports (2011)'),
            generate_table(agricDF),

            dcc.Markdown(children="""
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
            """),

            dcc.Graph(
                id='life-exp-vs-gdp',
                figure={
                    'data': [
                        go.Scatter(
                            x=lifeExpDF[lifeExpDF['continent'] == i]['gdp per capita'],
                            y=lifeExpDF[lifeExpDF['continent'] == i]['life expectancy'],
                            text=lifeExpDF[lifeExpDF['continent'] == i]['country'],
                            mode='markers',
                            opacity=0.7,
                            marker={
                                'size': 15,
                                'line': {'width': 0.5, 'color': 'white'}
                            },
                            name=i
                        ) for i in lifeExpDF.continent.unique()
                    ],
                    'layout': go.Layout(
                        xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                        yaxis={'title': 'Life Expectancy'},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            ),

            html.H4(children='(Some of) Dash HTML Elements'),

            html.Label('Dropdown'),
            dcc.Dropdown(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                value='MTL'
            ),

            html.Label('Multi-Select Dropdown'),
            dcc.Dropdown(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                value=['MTL', 'SF'],
                multi=True
            ),

            html.Label('Radio Items'),
            dcc.RadioItems(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                value='MTL'
            ),

            html.Label('Checkboxes'),
            dcc.Checklist(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                values=['MTL', 'SF']
            ),

            html.Label('Text Input'),
            dcc.Input(value='MTL', type='text'),

            html.Label('Slider'),
            dcc.Slider(
                min=0,
                max=9,
                marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                value=5,
            ),
        ]
    )
])
# ], style={'columnCount': 2})


if __name__ == '__main__':
    app.run_server(debug=True)
