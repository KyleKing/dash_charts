"""Example DataTable.

TODO: See todo list at bottom!!

"""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from implements import implements

from dash_charts.modules_datatable import ModuleFilteredTable
from dash_charts.utils_app import AppBase, AppInterface
from dash_charts.utils_helpers import parse_dash_cli_args


@implements(AppInterface)  # noqa: H601
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

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        # Load sample plotly express data to populate the datatable
        self.data_raw = px.data.gapminder()

        # Register modules
        self.mod_table = ModuleFilteredTable('filtered_table')
        self.modules = [
            self.mod_table,
        ]

    def create_elements(self) -> None:
        """Initialize charts and tables."""
        pass

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return dbc.Container([
            dbc.Col([
                dcc.Markdown(self.mod_table.table.filter_summary),
                html.Br(),
                html.H1(self.name),
                self.mod_table.return_layout(self._il, self.data_raw),
            ]),
        ])

    def create_callbacks(self) -> None:
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


instance = DataTableDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()

# TODO: CLICKABLE POPUPS
# - Datatable
# 	- Have click able icon in first column of table that triggers a dbc modal with additional information
# 		- Would have layout determined in callback. Could be used to show a timeline, full traceback, or other long
#           form data that can't be displayed in condensed table format
# 		- dbc modal:  https://dash-bootstrap-components.opensource.faculty.ai/l/components/modal
# 		- Would require pattern matching callback: https://dash.plotly.com/pattern-matching-callbacks

# # TODO: See: https://dash.plot.ly/datatable/interactivity
# > ('datatable-id...', 'derived_virtual_row_ids'),
# > ('datatable-id...', 'selected_row_ids'),
# > ('datatable-id...', 'active_cell'),


# TODO: Formatting (Typing): https://dash.plot.ly/datatable/typing
