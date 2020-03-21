"""Dash Modules."""

import dash_html_components as html
import pandas as pd
from dash.exceptions import PreventUpdate

from .datatable import BaseDataTable
from .utils_app_modules import ModuleBase
from .utils_fig import map_args, map_outputs


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
