"""DataTable Base Classes."""

from dash import dash_table

# TODO: See pattern mathing callbacks for adding buttons (to show modal) to datatables
#   https://dash.plotly.com/pattern-matching-callbacks

# PLANNED: see conditional formatting: https://dash.plotly.com/datatable/conditional-formatting

# PLANNED: These methods may be replaced in a future version of Dash
# Currently, edge case when column is string, but filter could be a number
# See: https://dash.plot.ly/datatable/callbacks & https://github.com/plotly/dash-table/issues/441

OPERATORS = [
    ['ge ', '>='],
    ['le ', '<='],
    ['lt ', '<'],
    ['gt ', '>'],
    ['ne ', '!='],
    ['eq ', '='],
    ['contains '],
    ['datestartswith '],
]
"""List of lists containing each possible filter string."""


def split_filter_part(filter_part):  # noqa: CCR001
    """Split the filter into `(name, operator, value)` components.

    Based on `Backend Paging with Filtering`: https://dash.plot.ly/datatable/callbacks

    Args:
        filter_part: string filter query

    Returns:
        tuple: `(name, operator, value)` which could be all None if no match was found

    """
    for operator_type in OPERATORS:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace(f'\\{v0}', v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # Word operators need spaces after them in the filter string, but we don't want these later
                return (name, operator_type[0].strip(), value)

    return [None, None, None]


def apply_datatable_filters(df_table, filter_query):
    """Filter a dataframe based on Dash datatable filterquery.

    Based on `Backend Paging with Filtering`: https://dash.plot.ly/datatable/callbacks

    Args:
        df_table: pandas dataframe to filter
        filter_query: Dash datatable string filter query

    Returns:
        dataframe: filtered dataframe

    """
    filtering_expressions = filter_query.split(' && ')
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            df_table = df_table.loc[getattr(df_table[col_name], operator)(filter_value)]
        elif operator == 'contains':
            df_table = df_table.loc[df_table[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            df_table = df_table.loc[df_table[col_name].str.startswith(filter_value)]
    return df_table


# PLANNED: Maybe move parameters to attr.ib classes?
class BaseDataTable:  # noqa: H601
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

    column_selectable = None
    """DataTable.column_selectable. Default is `None`."""

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

    row_selectable = None
    """DataTable.row_selectable. Default is `None`."""

    style_as_list_view = False
    """DataTable.style_as_list_view. Default is False."""

    sort_action = 'native'
    """DataTable.sort_action. Default is `'native'`."""

    sort_mode = 'single'
    """DataTable.sort_mode. Default is `'single'`."""

    # CSS Variables

    text_color = '#333333'
    """Default text color."""

    background_color = '#ffffff'
    """Default background color."""

    zebra_color = '#f9f9f9'
    """Default background color for odd rows (zebra-stripe)."""

    selected_cell_color = '#eaeaea'
    """Default color for selected cells."""

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
            # Align the select icon to the left and the sort icon to the right
            {
                'selector': 'th.dash-header div',
                'rule': 'display: flex; align-items: center;',
            },
            {
                'selector': 'th.dash-header div span.column-header--select',
                'rule': 'order: 1; flex-shrink: 5; text-align: left;',
            },
            {
                'selector': 'th.dash-header div span.column-header-name',
                'rule': 'order: 2; flex-grow: 5; text-align: center;',
            },
            {
                'selector': 'th.dash-header div span.column-header--sort',
                'rule': 'order: 3; flex-shrink: 5; text-align: right;',
            },

            # Remove excess borders to better match JQuery DataTables styling
            # (Some border styles don't appear to work from `self.style_header`)
            {'selector': 'th.dash-filter', 'rule': 'border-bottom-color: rgb(17, 17, 17) !important;'},
        ]
        self.style_cell = {
            'backgroundColor': self.background_color,
            'borderStyle': f'1px solid {self.zebra_color}',
            'color': self.text_color,
        }
        self.style_cell_conditional = []
        self.style_data = {}
        self.style_data_conditional = [
            {'if': {'row_index': 'even'}, 'backgroundColor': self.zebra_color},
        ]
        self.style_header = {
            'borderLeft': 'none',
            'borderRight': 'none',
            'borderTop': 'none',
            'fontWeight': 'bold',
        }
        self.style_header_conditional = []
        self.style_filter = {
            'borderBottomColor': 'rgb(17, 17, 17)',
        }
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
                'selectable': True,
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
