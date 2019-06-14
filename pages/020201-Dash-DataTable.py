# -*- coding: utf-8 -*-
"""02-0201, Basic Dash DataTable Styling.

Based on: https://dash.plot.ly/datatable

> https://github.com/plotly/dash-table

"""

from pathlib import Path

import dash
import dash_html_components as html
import dash_table
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/26k-consumer-complaints.csv')
df = df[:45]

app = dash.Dash(__name__, assets_folder=str(Path.cwd() / 'pages/assets'))

# =====================================================================================================================
# Layout the application

app.layout = html.Div([
    html.Div(
        className='app-content',
        children=[
            html.H2(children='Example DataTable'),
            dash_table.DataTable(
                id='table',
                columns=[{'name': i, 'id': i} for i in df.columns],
                data=df.to_dict('rows'),
                # # > Setting a fixed row can cause the header row to have the wrong horizontal spacing as the data
                # n_fixed_rows=1,
                style_table={
                    'maxHeight': '600',
                    'overflowX': 'scroll',
                    'overflowY': 'scroll',
                },
                style_cell={
                    'maxWidth': '300px',
                },
                style_cell_conditional=[
                    {'if': {'row_index': 'odd'},
                     'backgroundColor': 'rgb(248, 248, 248)',
                     },
                ] + [
                    {'if': {'column_id': c},
                     'textAlign': 'center',
                     'width': '80px',
                     } for c in ['Unnamed: 0', 'Product']
                ],
                css=[{
                    'selector': '.dash-cell div.dash-cell-value',
                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;',
                }],
                merge_duplicate_headers=True,
                # style_as_list_view=True,  # Remove vertical lines for short tables
            ),
        ],
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
