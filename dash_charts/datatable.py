"""DataTable Base Classes."""

import dash_table

# TODO: Create a simpler datatable?
# self..filter_action = 'none'
# self..row_selectable = False
# # self..style_as_list_view = True
# self.sort_action = 'none'


class BaseDataTable:
    """Base Class for Data Tables."""

    filter_summary = """Table Filter Syntax:

Full documentation at: [https://dash.plot.ly/datatable/filtering](https://dash.plot.ly/datatable/filtering)

- `eq`: exact match (applies to number columns and will try to convert string to number)
- `contains`: search for exact (case-sensitive) substring in each cell
- `datestartswith`: matches partial datetime. For example, datestartswith `2018-03-01` will match `2018-03-01 12:59`
but not `2018-03`
- `ne`, `gt`, `ge`, `lt`, `le`: comparison operators for not equal, greater than, greater or equal, less than, etc.
Applies to numbers and string columns (uses numbers, symbols, uppercase letter, lowercase letters)

Press enter of tab to apply the filter"""
    """Markdown text explaining dash_table.DataTable filtering rules with link to full documentation."""

    # dash_table.DataTable Parameters. Documentation: https://dash.plot.ly/datatable/reference

    style_table = None
    """DataTable.style_table dictionary. Default enables overflowX scroll. Set in `initialize_mutables`."""

    css = None
    """DataTable.css list. Use the style_* properties first.  Set in `initialize_mutables`.

    Default sets row margin to zero to fix a negative margin issue when using dash_table and Bootstrap
    See: https://github.com/facultyai/dash-bootstrap-components/issues/334

    Also sets other various style tweaks to highlight the filter icons on hover, etc.

    """

    style_cell = None
    """DataTable.style_cell dictionary. Default is empty dictionary. Set in `initialize_mutables`."""

    style_cell_conditional = None
    """DataTable.style_cell_conditional list. Default is empty list. Set in `initialize_mutables`."""

    style_data = None
    """DataTable.style_data dictionary. Default is empty dictionary. Set in `initialize_mutables`."""

    style_data_conditional = None
    """DataTable.style_data_conditional list. Default is for odd rows to have an off-white background (zebra stripe).

    Set in `initialize_mutables`

    """

    style_header = None
    """DataTable.style_header dictionary. Default is bold and off-white background. Set in `initialize_mutables`."""

    style_header_conditional = None
    """DataTable.style_header_conditional list. Default is empty list. Set in `initialize_mutables`."""

    style_filter = None
    """DataTable.style_filter dictionary. Default is empty dictionary. Set in `initialize_mutables`."""

    style_filter_conditional = None
    """DataTable.style_filter_conditional list. Default is empty list. Set in `initialize_mutables`."""

    column_selectable = 'single'
    """DataTable.column_selectable. Default is `'single'`."""

    column_kwarg_lookup = None
    """Lookup for keyword arguments for each column allowing deletable, selectable, etc. to be set per column."""

    export_format = 'none'
    """DataTable.export_format. Default is `'none'`. Could be one of `(csv, xlsx)`."""

    export_headers = 'names'
    """DataTable.export_headers. Default is `'names'`. See documentation."""

    filter_action = 'native'
    """DataTable.filter_action. Default is `'native'`."""

    page_size = 25
    """DataTable.page_size. Default is `'25'`."""

    row_selectable = 'single'
    """DataTable.row_selectable. Default is `'single'`."""

    style_as_list_view = False
    """DataTable.style_as_list_view. Default is False."""

    sort_action = 'native'
    """DataTable.sort_action. Default is `'native'`."""

    sort_mode = 'single'
    """DataTable.sort_mode. Default is `'single'`."""

    def __init__(self):
        """Initialize class."""
        self.initialize_mutables()

    def initialize_mutables(self):
        """Initialize the mutable data members to prevent modifying one attribute and impacting all instances."""
        self.style_table = {'overflowX': 'scroll'}
        self.css = [
            # Fix width when overflow is True and using dash_bootstrap_components
            {'selector': '.row', 'rule': 'margin: 0'},

            # Based on: https://community.plot.ly/t/dash-table-datatable-styling-examples/15594/
            # Highlight filter icons on hover anywhere in the header cell
            {'selector': 'tr:hover', 'rule': 'backgroundColor: pink'},
            # Align the select icon to the left and the sort icon to the right
            {'selector': 'th.dash-header div', 'rule': 'display:flex;'},
            {'selector': 'th.dash-header div span.column-header--select',
             'rule': 'order: 1; width: 100%; text-align: left'},
            {'selector': 'th.dash-header div span.column-header-name', 'rule': 'order: 2'},
            {'selector': 'th.dash-header div span.column-header--sort',
             'rule': 'order: 3; width: 100%; text-align: right'},
        ]
        self.style_cell = {}
        self.style_cell_conditional = []
        self.style_data = {}
        self.style_data_conditional = [
            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
        ]
        self.style_header = {
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
        }
        self.style_header_conditional = []
        self.style_filter = {}
        self.style_filter_conditional = []

        self.initialize_column_kwarg_lookup()  # Must be called last

    def initialize_column_kwarg_lookup(self):
        """Initialize the column lookup based on the other mutables.

        Documentation: https://dash.plot.ly/datatable/reference

        Additional kwargs not set in default lookup:
            - clearable, deletable, editable, hideable, renamable, format, presentation, on_change, sort_as_null,
                validation, type

        """
        self.column_kwarg_lookup = {
            'default_kwargs': {
                'selectable': (self.column_selectable is not None),
            },
        }

    def create_table(self, df_raw, columns=None, **kwargs_datatable):
        """Create the dash_table.DataTable.

        Args:
            df_raw: data to pass to datatable
            columns: list of column names to display. Default is None to use all columns from df_raw
            kwargs_datatable: keyword arguments to pass to the datatable

        Returns:
            DataTable: returns dash_table.DataTable object

        """
        if columns is None:
            columns = df_raw.columns
        return dash_table.DataTable(**self._create_datatable(df_raw, columns), **kwargs_datatable)

    def format_datatable_columns(self, df_raw, columns):
        """Return a list of column names formatted for a dash_table. Uses `self.self.column_name_kwarg_lookup`.

        Args:
            df_raw: data to pass to datatable
            columns: list of strings or None

        Returns:
            list: of dict with keys `(name, id, deleteable, selectable)` in order of df_raw columns

        """
        return [
            {'name': col, 'id': col, **self.column_kwarg_lookup.get(col, self.column_kwarg_lookup['default_kwargs'])}
            for col in df_raw.columns if (columns is None or col in columns)
        ]

    def _create_datatable(self, df_raw, columns, **table_kwargs):
        """Return dictionary of keyword arguments for datatable.

        Args:
            df_raw: data to pass to datatable
            columns: will auto format list of string column names to display or use list of dicts
            table_kwargs: additional keyword arguments to pass to datatable, such as id

        Returns:
            dict: keys include `(columns, data)` and all data members

        """
        return {
            'columns': self.format_datatable_columns(df_raw, columns) if isinstance(columns[0], str) else columns,
            'data': (df_raw.loc[:, columns] if columns is not None else df_raw).to_dict('records'),

            # Add all datamembers
            'css': self.css,
            'style_table': self.style_table,
            'style_cell': self.style_cell,
            'style_cell_conditional': self.style_cell_conditional,
            'style_data': self.style_data,
            'style_data_conditional': self.style_data_conditional,
            'style_header': self.style_header,
            'style_header_conditional': self.style_header_conditional,
            'style_filter': self.style_filter,
            'style_filter_conditional': self.style_filter_conditional,
            'column_selectable': self.column_selectable,
            'export_format': self.export_format,
            'export_headers': self.export_headers,
            'filter_action': self.filter_action,
            'page_size': self.page_size,
            'row_selectable': self.row_selectable,
            'style_as_list_view': self.style_as_list_view,
            'sort_action': self.sort_action,
            'sort_mode': self.sort_mode,
        }
