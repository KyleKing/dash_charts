"""Example DataTable."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash_charts.components import dropdown_group
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.datatable import BaseDataTable
from dash_charts.utils_app import AppBase, opts_dd
from dash_charts.utils_fig import map_args, map_outputs


class DataTableDemo(AppBase):
    """Example creating a DataTable."""

    name = 'Example DataTable'
    """Application name"""

    external_stylesheets = [dbc.themes.FLATLY]  # DARKLY, FLATLY, etc. (https://bootswatch.com/)
    """List of external stylesheets. Default is minimal Dash CSS. Only applies if app argument not provided."""

    data_raw = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    table_main = None
    """Main table (DataTable)."""

    id_table = 'datatable'
    """Unique name for the main table."""

    id_column_select = 'main-dropdown'
    """Unique name for the dropdown."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_table, self.id_column_select])
        # Load sample plotly express data to populate the datatable
        self.data_raw = px.data.gapminder()

    def create_elements(self):
        """Initialize charts and tables."""
        self.table_main = BaseDataTable()
        # Extend DataTable Parameters as needed
        self.table_main.style_data_conditional.extend([
            {'if': {'row_index': 2}, 'backgroundColor': '#3D9970', 'color': 'white'},
            {'if': {'column_id': 'pop'}, 'backgroundColor': '#3D9970', 'color': 'white'},
            {
                'if': {
                    'column_id': 'year',
                    'filter_query': '{year} le "1975"',
                },
                'backgroundColor': '#3D4999',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': 'gdpPerCap',
                    'row_index': 5,
                },
                'backgroundColor': '#3D4999',
                'color': 'white',
            },
        ])

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        options = [opts_dd(column, column) for column in self.data_raw.columns]
        return dbc.Container([
            dbc.Col([
                dcc.Markdown(self.table_main.filter_summary),
                html.Br(),
                dropdown_group('Select DataFrame Columns', self.ids[self.id_column_select],
                               options, multi=True, persistence=True, value=self.data_raw.columns),
                html.Div([], id=self.ids[self.id_table]),
            ]),
        ])

    def create_callbacks(self):
        """Create Dash callbacks."""
        outputs = [(self.id_table, 'children')]
        inputs = [(self.id_column_select, 'value')]
        states = []

        @self.callback(outputs, inputs, states)
        def update_table(*args):
            a_in, a_states = map_args(args, inputs, states)
            columns = a_in[self.id_column_select]['value']
            if len(columns) == 0:
                raise PreventUpdate
            datatable = self.table_main.create_table(self.data_raw, columns)
            return map_outputs(outputs, [(self.id_table, 'children', datatable)])


instance = DataTableDemo
if __name__ == '__main__':
    port = parse_cli_port()
    app = instance()
    app.create()
    app.run(port=port, debug=True)
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
