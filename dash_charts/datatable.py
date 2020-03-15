"""DataTable Base Classes."""

import dash_table


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

    style_table = {
        'overflowX': 'scroll',
    }
    """DataTable.style_table dictionary. Default enables overflowX scroll."""

    css = [
        {'selector': '.row', 'rule': 'margin: 0'},
    ]
    """DataTable.css list. Use the style_* properties first.

    Default sets row margin to zero to fix a negative margin issue when using dash_table and Bootstrap
    See: https://github.com/facultyai/dash-bootstrap-components/issues/334

    """

    style_cell = {}
    """DataTable.style_cell dictionary. Default is empty dictionary."""

    style_cell_conditional = []
    """DataTable.style_cell_conditional list. Default is empty list."""

    style_data = {}
    """DataTable.style_data dictionary. Default is empty dictionary."""

    style_data_conditional = [
        {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
    ]
    """DataTable.style_data_conditional list. Default is for odd rows to have an off-white background (zebra stripe)."""

    style_header = {
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold',
    }
    """DataTable.style_header dictionary. Default is bold and off-white background."""

    style_header_conditional = []
    """DataTable.style_header_conditional list. Default is empty list."""

    style_filter = {}
    """DataTable.style_filter dictionary. Default is empty dictionary."""

    style_filter_conditional = []
    """DataTable.style_filter_conditional list. Default is empty list."""

    column_selectable = 'single'
    """DataTable.column_selectable. Default is `'single'`."""

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

    sort_mode = 'multi'
    """DataTable.sort_mode. Default is `'multi'`."""

    def __init__(self):
        """Initialize class."""
        pass

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

    def _create_datatable(self, df_raw, columns):
        """Return dictionary of keyword arguments for datatable.

        Args:
            df_raw: data to pass to datatable
            columns: list of column names to display

        Returns:
            dict: keys include `(columns, data)` and all data members

        """
        return {
            # Preserve order of columns from original dataframe
            'columns': [{'name': column, 'id': column} for column in df_raw.columns if column in columns],
            'data': df_raw.loc[:, columns].to_dict('records'),

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
