"""02-0203, Dash Interactive DataTable (With Python).

Based on: https://dash.plot.ly/datatable/filtering

"""

from pathlib import Path

import dash
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__, assets_folder=str(Path.cwd() / 'examples/assets'))

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')


app.layout = html.Div([
    html.Div(
        className='app-content',
        children=[
            dash_table.DataTable(
                id='table-filtering-be',
                columns=[
                    {'name': i, 'id': i} for i in sorted(df.columns)
                ],
                filtering='be',
                filter='',
            ),
        ],
    ),
])

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-filtering-be', 'data'),
    [Input('table-filtering-be', 'filter')])
def update_table(_filter):
    filtering_expressions = _filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
