"""Dash Modules for Data Tables."""

import json

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.exceptions import PreventUpdate

from .components import dropdown_group, opts_dd
from .datatable import BaseDataTable
from .utils_app_modules import ModuleBase
from .utils_callbacks import map_args, map_outputs


class ModuleDataTable(ModuleBase):
    """Modular Dash data table."""

    id_table_parent = 'datatable-module-parent'
    """Table Parent ID."""

    id_table = 'datatable-module'
    """Table ID."""

    table = None
    """Dash Data Table."""

    all_ids = [id_table_parent, id_table]
    """List of ids to register for this module."""

    def create_elements(self, ids):
        """Register the callback for creating the main chart.

        Args:
            ids: `self._il` from base application

        """
        self.table = BaseDataTable()

    def return_layout(self, ids):
        """Return Dash application layout.

        Args:
            ids: `self._il` from base application

        Returns:
            dict: Dash HTML object

        """
        placeholder = pd.DataFrame.from_records([['body']], columns=['header'])
        return html.Div(
            [
                self.table.create_table(placeholder, None, id=ids[self.get(self.id_table)]),
            ], id=ids[self.get(self.id_table_parent)],
        )

    def return_table_map(self, ids, df_table, columns=None):
        """Return list of tuples for `map_outputs` that includes the new datatable.

        Args:
            ids: `self._il` from base application
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

        Raises:
            PreventUpdate: if no columns found in the table

        """
        outputs = [(self.get(self.id_table), 'style_data_conditional')]
        inputs = [(self.get(self.id_table), 'sort_by')]
        states = []

        @parent.callback(outputs, inputs, states)
        def highlight_sort_column(*raw_args):
            a_in, a_states = map_args(raw_args, inputs, states)
            sort_by = a_in[self.get(self.id_table)]['sort_by']
            if sort_by is None:
                raise PreventUpdate

            sorted_columns_style = []
            for sort in sort_by:
                sorted_columns_style.extend([
                    {
                        'if': {'column_id': sort['column_id'], 'row_index': 'odd'},
                        'color': self.table.text_color, 'background-color': self.table.zebra_color,
                    },
                    {
                        'if': {'column_id': sort['column_id'], 'row_index': 'even'},
                        'color': self.table.text_color, 'background-color': self.table.selected_cell_color,
                    },
                ])

            style_data_conditional = [*self.table.style_data_conditional, *sorted_columns_style]
            return map_outputs(outputs, [(self.get(self.id_table), 'style_data_conditional', style_data_conditional)])


class ModuleFilteredTable(ModuleDataTable):
    """Modular Dash data table with column selection and filter."""

    id_column_select = 'column-select'
    """Column select ID."""

    id_filter_button = 'filter-button'
    """Apply filter button ID."""

    id_filter_input = 'filter-query-input'
    """Filter query input ID."""

    id_filter_output = 'filter-query-output'
    """Filter query output ID."""

    id_filter_structure = 'filter-query-structure'
    """Filter query structure ID."""

    all_ids = ModuleDataTable.all_ids + [
        id_column_select, id_filter_button, id_filter_input, id_filter_output,
        id_filter_structure,
    ]
    """List of ids to register for this module."""

    show_filter = True
    """If True (default), will show an input for entering a global filter."""

    mod_df = None
    """Data frame shown in table. Passed to `return_layout` and used when creating the table."""

    def return_layout(self, ids, mod_df):
        """Return Dash application layout.

        Args:
            ids: `self._il` from base application
            mod_df: dataframe for

        Returns:
            dict: Dash HTML object

        """
        self.mod_df = mod_df
        options = [opts_dd(column, column) for column in self.mod_df.columns]
        if self.show_filter:
            filter_elements = dbc.Row([
                dbc.Col(
                    [
                        dbc.Form([
                            dcc.Input(
                                id=ids[self.get(self.id_filter_input)], placeholder='Enter filter query',
                                style={'width': '100%'},
                            ),
                            dbc.Button(
                                'Apply', color='secondary', id=ids[self.get(self.id_filter_button)],
                                style={'paddingTop': '5px'},
                            ),
                        ]),
                    ], width=4,
                ),
                dbc.Col(
                    [
                        html.Div([], id=ids[self.get(self.id_filter_output)]),
                    ], width=4,
                ),
                dbc.Col(
                    [
                        html.Div(id=ids[self.get(self.id_filter_structure)], style={'whitespace': 'pre'}),
                    ], width=4,
                ),
            ])
        else:
            filter_elements = html.Div()

        return dbc.Col([
            dropdown_group(
                'Select DataFrame Columns', ids[self.get(self.id_column_select)],
                options, multi=True, persistence=True, value=self.mod_df.columns,
            ),
            filter_elements,
            html.Br(),
            super().return_layout(ids),
        ])

    def create_callbacks(self, parent):
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        """
        super().create_callbacks(parent)
        self.register_create_table(parent)
        if self.show_filter:
            self.register_filter_interface(parent)
            self.register_show_query(parent)

    def register_create_table(self, parent):
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        Raises:
            PreventUpdate: if no columns found in the table

        """
        outputs = [(self.get(self.id_table_parent), 'children')]
        inputs = [(self.get(self.id_column_select), 'value')]
        states = []

        @parent.callback(outputs, inputs, states)
        def create_table(*raw_args):
            a_in, a_states = map_args(raw_args, inputs, states)
            columns = a_in[self.get(self.id_column_select)]['value']
            if not columns:
                raise PreventUpdate
            return map_outputs(outputs, self.return_table_map(parent.ids, self.mod_df, columns))

    def register_filter_interface(self, parent):
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        """
        outputs = [(self.get(self.id_table), 'filter_query')]
        inputs = [(self.get(self.id_filter_button), 'n_clicks')]
        states = [(self.get(self.id_filter_input), 'value')]

        @parent.callback(outputs, inputs, states)
        def show_query(*raw_args):
            a_in, a_states = map_args(raw_args, inputs, states)
            query = a_states[self.get(self.id_filter_input)]['value']
            if query is None:
                query = ''
            return map_outputs(outputs, [(self.get(self.id_table), 'filter_query', query)])

    def register_show_query(self, parent):   # noqa: CCR001
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        """
        outputs = [(self.get(self.id_filter_output), 'children'), (self.get(self.id_filter_structure), 'children')]
        inputs = [
            (self.get(self.id_table), 'filter_query'),
            (self.get(self.id_table), 'derived_filter_query_structure'),
        ]
        states = []

        @parent.callback(outputs, inputs, states)
        def show_query(*raw_args):
            a_in, a_states = map_args(raw_args, inputs, states)
            filter_query = a_in[self.get(self.id_table)]['filter_query']
            derived_query = a_in[self.get(self.id_table)]['derived_filter_query_structure']

            if filter_query is None or len(filter_query.strip()) == 0:
                filter_element = ['No filter query']
                derived_element = ['']
            else:
                filter_element = [dcc.Markdown(f'```\n\nfilter_query:\n\n{filter_query}\n\n```')]
                if derived_query is None:
                    derived_element = ['Error in query. Check formatting']
                else:
                    derived_element = [
                        html.Details([
                            html.Summary('Derived filter query structure'),
                            html.Div(dcc.Markdown(f'```json\n\n{json.dumps(derived_query, indent=4)}\n\n```')),
                        ]),
                    ]
            return map_outputs(
                outputs, [
                    (self.get(self.id_filter_output), 'children', filter_element),
                    (self.get(self.id_filter_structure), 'children', derived_element),
                ],
            )
