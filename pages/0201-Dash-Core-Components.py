# -*- coding: utf-8 -*-
"""02-01, Dash Core Components.

Based on: https://dash.plot.ly/dash-core-components.

Other Examples:

- Store for user data: https://dash.plot.ly/dash-core-components/store
- Confirm Dialog: https://dash.plot.ly/dash-core-components/confirm
- Upload Component: https://dash.plot.ly/dash-core-components/upload

"""

from datetime import datetime as dt
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash(__name__, assets_folder=str(Path.cwd() / 'pages/assets'))

# =====================================================================================================================
# Layout the application

app.layout = html.Div([
    html.Div(
        className='app-content',
        children=[
            html.H4(children='(Most of) Dash HTML Elements'),

            # ==========
            # Dropdowns
            # ==========

            html.Label('Dropdown'),
            dcc.Dropdown(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'},
                ],
                value='MTL',
            ),

            html.Label('Multi-Select Dropdown'),
            dcc.Dropdown(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': u'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'},
                ],
                value=['MTL', 'SF'],
                multi=True,
            ),

            # ==========
            # Sliders
            # ==========

            html.Label('Basic Slider'),
            dcc.Slider(
                id='example-id',
                min=0,
                max=10,
                step=0.1,
                value=3.3,
                updatemode='drag',  # Faster updates
            ),
            html.Label('Labeled Slider'),
            dcc.Slider(
                min=0,
                max=10,
                marks={i: chr(ord('A') + i) for i in range(10)},
                value=5,
                dots=False,
            ),

            html.Label('Range Slider With Nice Labels (No Inclusion)'),
            dcc.RangeSlider(
                min=0,
                max=100,
                value=[10, 65],
                marks={
                    0: {'label': '0°C', 'style': {'color': '#77b0b1'}},
                    26: {'label': '26°C'},
                    37: {'label': '37°C'},
                    100: {'label': '100°C', 'style': {'color': '#f50'}},
                },
                included=False,
            ),
            html.Label('Pushable Multi-Range Slider'),
            dcc.RangeSlider(
                min=-5,
                max=30,
                value=[1, 3, 4, 5, 12, 17],
                pushable=2,
            ),

            # ==========
            # Inputs
            # ==========

            html.Label('Input and Text Area'),
            dcc.Input(
                placeholder='Enter a value...',
                type='text',
                value='MTL',
            ),
            dcc.Textarea(
                placeholder='Enter a value...\n' * 10,
                value='This is a TextArea component',
                style={'width': '100%'},
            ),

            # ==========
            # Select (Radio/Checkbox)
            # ==========

            html.Label('Radio Items'),
            dcc.RadioItems(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': 'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'},
                ],
                value='MTL',
                # labelStyle={'display': 'inline-block'},
            ),
            html.Label('Checkboxes'),
            dcc.Checklist(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': 'Montréal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'},
                ],
                values=['MTL', 'SF'],
            ),

            # ==========
            # Button and Callback
            # ==========

            html.Label('Example Button with Callback'),
            html.Div(dcc.Input(id='input-box', type='text')),
            html.Button('Submit', id='button'),
            html.Div(
                id='output-container-button',
                children='Enter a value and press submit',
            ),

            # ==========
            # Datepicker
            # ==========

            html.Label('Single Date Picker'),
            dcc.DatePickerSingle(
                id='date-picker-single',
                date=dt(2020, 4, 1),
            ),
            html.Label('Ranged Date Picker'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=dt(1997, 5, 3),
                end_date_placeholder_text='Select a date!',
            ),
            html.H6('^ fyi: need padding below for dropdown element'),

            # ==========
            # Graphs - of course
            # ==========

            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                            y=[219, 99, 97, 112, 127, 180, 236, 207, 236, 263, 350, 430, 474, 526, 488, 537, 500, 439],
                            name='Rest of world',
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)',
                            ),
                        ),
                        go.Bar(
                            x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                            y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270, 299, 340, 403, 549, 499],
                            name='China',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)',
                            ),
                        ),
                    ],
                    layout=go.Layout(
                        title='US Export of Plastic Scrap',
                        showlegend=True,
                        legend=go.layout.Legend(
                            x=0,
                            y=1.0,
                        ),
                        margin=go.layout.Margin(l=40, r=0, t=40, b=30),  # noqa: E741
                    ),
                ),
                style={'height': 300},
                id='my-graph',
            ),

        ],
    ),
])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    """Indicate button-click event."""
    return 'The input value was "{}" and the button has been clicked {} times'.format(value, n_clicks)


if __name__ == '__main__':
    app.run_server(debug=True)
