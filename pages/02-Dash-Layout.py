# -*- coding: utf-8 -*-
"""02, Dash Layout.

Based on: https://dash.plot.ly/getting-started.

For reference see:

[Core Dash Components](https://dash.plot.ly/dash-core-components)
[HTML Components](https://dash.plot.ly/dash-html-components)

"""

import random
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

assets_dir = Path.cwd() / 'pages/assets'

app = dash.Dash(__name__, assets_folder=str(assets_dir))

colors = {
    'background': '#FFF',
    'text': '#26335C',
}

# =====================================================================================================================
# Barchart

# Create data for Bar Chart
x = [
    'aerial tramways', 'aircrafts', 'aircraft carriers', 'airplanes', 'balloons', 'barges', 'cabs', 'cable cars',
    'cabooses', 'delivery trucks', 'destroyers', 'diesel trucks', 'earth movers', 'eighteen-wheelers', 'electric cars',
    'elevated railroads', 'ferries', 'fireboats', 'galleons', 'garbage trucks', 'gliders', 'handcars', 'hang gliders',
]
random.shuffle(x)


def randY():
    """Generate Random Y Coordinates."""
    return [random.randint(1, 50) for __ in x]


# =====================================================================================================================
# Table

agricDF = pd.read_csv(assets_dir / 'usa-agricultural-exports-2011.csv')


def generate_table(dataframe, max_rows=10, max_cols=10):
    """Reusable Pandas HTML data table component."""
    return html.Table(
        [
            html.Tr([html.Th(col) for cIdx, col in enumerate(dataframe.columns) if cIdx > 0 and cIdx <= max_cols]),
        ] + [
            html.Tr([
                html.Td(
                    dataframe.iloc[i][col],
                ) for cIdx, col in enumerate(dataframe.columns) if cIdx > 0 and cIdx <= max_cols
            ]) for i in range(min(len(dataframe), max_rows))
        ],
    )


# =====================================================================================================================
# Configure Scatter Plot

lifeExpDF = pd.read_csv(assets_dir / 'gdp-life-exp-2007.csv')

# =====================================================================================================================
# Layout the application

app.layout = html.Div([
    html.Div(
        className='app-content',
        children=[
            html.H1(
                children='Dash: Hello Barchart',
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                },
            ),
            html.Div(children='When Random Words meet Random Numbers', style={
                'textAlign': 'center',
                'color': colors['text'],
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
                            'color': colors['text'],
                        },
                    },
                },
                style={'margin-top': '20px'},
            ),

            html.H4(children='US Agriculture Exports (2011)'),
            generate_table(agricDF),

            html.H4(children='Life Expectancy vs. GDP (2007)'),
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
                                'line': {'width': 0.5, 'color': 'white'},
                            },
                            name=i,
                        ) for i in lifeExpDF.continent.unique()
                    ],
                    'layout': go.Layout(
                        xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                        yaxis={'title': 'Life Expectancy'},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest',
                    ),
                },
                style={'margin-top': '20px'},
            ),

            dcc.Markdown(children="""
---

### Dash and Markdown

- Dash apps can be written in Markdown.
- Dash uses the [CommonMark](http://commonmark.org/) specification of Markdown.
- Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)

Code snippet:

```python
print('I am Code Block')
print('Syntax highlighting could work if Highlight.js is included')
```
---
"""),

            html.H4(children='(Some of) Dash HTML Elements'),

            html.Label('Dropdown', style={'margin-top': '20px'}),
            dcc.Dropdown(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'},
                ],
                value='MTL',
            ),

            html.Label('Multi-Select Dropdown', style={'margin-top': '20px'}),
            dcc.Dropdown(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'},
                ],
                value=['MTL', 'SF'],
                multi=True,
            ),

            html.Label('Radio Items', style={'margin-top': '20px'}),
            dcc.RadioItems(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'},
                ],
                value='MTL',
            ),

            html.Label('Checkboxes', style={'margin-top': '20px'}),
            dcc.Checklist(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'},
                ],
                values=['MTL', 'SF'],
            ),

            html.Label('Text Input', style={'margin-top': '20px'}),
            dcc.Input(value='MTL', type='text'),

            html.Label('Slider', style={'margin-top': '20px'}),
            dcc.Slider(
                min=0,
                max=9,
                marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                value=5,
            ),
        ],
    ),
])
# ], style={'columnCount': 2})


if __name__ == '__main__':
    app.run_server(debug=True)
