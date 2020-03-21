"""Example DataTable."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash_charts.components import dropdown_group
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.modules import ModuleDataTable
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

    mod_table = None
    """Main table (DataTable)."""

    id_column_select = 'main-dropdown'
    """Unique name for the dropdown."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_column_select])

        # Load sample plotly express data to populate the datatable
        self.data_raw = px.data.gapminder()

        # Register modules
        self.mod_table = ModuleDataTable('main_table')
        self.modules = [
            self.mod_table,
        ]

    def create_elements(self):
        """Initialize charts and tables."""
        pass

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        options = [opts_dd(column, column) for column in self.data_raw.columns]
        return dbc.Container([
            dbc.Col([
                dcc.Markdown(self.mod_table.table.filter_summary),
                html.Br(),
                html.H1(self.name),
                dropdown_group('Select DataFrame Columns', self.ids[self.id_column_select],
                               options, multi=True, persistence=True, value=self.data_raw.columns),
                self.mod_table.return_layout(self.ids),
            ]),
        ])

    def create_callbacks(self):
        """Create Dash callbacks."""
        outputs = [(self.mod_table.get(self.mod_table.id_table_parent), 'children')]
        inputs = [(self.id_column_select, 'value')]
        states = []

        @self.callback(outputs, inputs, states)
        def update_table(*args):
            a_in, a_states = map_args(args, inputs, states)
            columns = a_in[self.id_column_select]['value']
            if len(columns) == 0:
                raise PreventUpdate
            return map_outputs(outputs, self.mod_table.return_table_map(self.ids, self.data_raw, columns))


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
