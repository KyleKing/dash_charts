"""Example DataTable."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash_charts.components import dropdown_group
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.datatable import BaseDataTable
from dash_charts.utils_app import AppBase, opts_dd
from dash_charts.utils_app_modules import ModuleBase
from dash_charts.utils_fig import map_args, map_outputs
from icecream import ic


class ModuleDataTable(ModuleBase):
    """Modular Dash data table."""

    id_table_parent = 'datatable-module-parent'
    id_table = 'datatable-module'

    table = None

    all_ids = [id_table_parent, id_table]

    def create_elements(self, ids):
        """Register the callback for creating the main chart.

        Args:
            ids: `self.ids` from base application

        """
        self.table = BaseDataTable()

    def return_layout(self, ids):
        """Return Dash application layout.

        Args:
            ids: `self.ids` from base application

        Returns:
            dict: Dash HTML object. Default is simple HTML text

        """
        placeholder = pd.DataFrame.from_records([['body']], columns=['header'])
        return html.Div([
            self.table.create_table(placeholder, None, id=ids[self.get(self.id_table)]),
        ], id=ids[self.get(self.id_table_parent)])

    def return_table_map(self, ids, df_table, columns=None):
        """Return list of tuples for `map_outputs` that includes the new datatable.

        Args:
            ids: `self.ids` from base application
            df_table: dataframe to show in table
            columns: list of columns to show. Default is None, which will show all columns

        Returns:
            list: list of tuples for `map_outputs`

        """
        datatable = self.table.create_table(df_table, columns, id=ids[self.get(self.id_table)])
        return [(self.get(self.id_table_parent), 'children', datatable)]

    def create_callbacks(self, parent):
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        """
        self.register_highlight_sort_column(parent)

    def register_highlight_sort_column(self, parent):
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        """
        outputs = [(self.get(self.id_table), 'style_data_conditional')]
        inputs = [(self.get(self.id_table), 'sort_by')]
        states = []

        @parent.callback(outputs, inputs, states)
        def highlight_sort_column(*args):
            a_in, a_states = map_args(args, inputs, states)
            sort_by = a_in[self.get(self.id_table)]['sort_by']
            if sort_by is None:
                raise PreventUpdate

            sorted_columns_style = []
            for sort in sort_by:
                sorted_columns_style.extend([
                    {'if': {'column_id': sort['column_id'], 'row_index': 'odd'},
                     'color': self.table.text_color, 'background-color': self.table.zebra_color},
                    {'if': {'column_id': sort['column_id'], 'row_index': 'even'},
                     'color': self.table.text_color, 'background-color': self.table.selected_cell_color},
                ])

            style_data_conditional = [*self.table.style_data_conditional, *sorted_columns_style]
            return map_outputs(outputs, [(self.get(self.id_table), 'style_data_conditional', style_data_conditional)])

        # # Experiment with different table properties
        # table_keys = ['is_focused', 'selected_cells', 'selected_rows',
        #               'selected_columns', 'selected_row_ids', 'sort_action', 'sort_mode', 'sort_by']
        # inputs = [(self.get(self.id_table), key) for key in table_keys]

        #     for key in table_keys:
        #         key_padded = ''.join((key + ' ' * 20)[:20])
        #         value = f'{key_padded}:{a_in[self.get(self.id_table)][key]}'
        #         ic(value)
        #     ic('\n' * 5)


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
