"""Example of the Upload Module."""

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_charts.dash_helpers import parse_dash_cli_args
from dash_charts.modules_upload import UploadModule
from dash_charts.utils_app import AppBase


class UploadModuleDemo(AppBase):
    """Example using the Upload Module."""

    name = 'Example Use of the Upload Module'
    """Application name"""

    external_stylesheets = [dbc.themes.FLATLY]  # DARKLY, FLATLY, etc. (https://bootswatch.com/)
    """List of external stylesheets. Default is minimal Dash CSS. Only applies if app argument not provided."""

    data_raw = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    mod_upload = None
    """Main table (DataTable)."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()

        # Register modules
        self.mod_upload = UploadModule('filtered_table')
        self.modules = [
            self.mod_upload,
        ]

    def create_elements(self):
        """Initialize charts and tables."""
        pass

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return dbc.Container([
            dbc.Col([
                html.H1(self.name),
                html.H2('(`self.mod_upload.return_drop_to_upload()` below)'),
                self.mod_upload.return_drop_to_upload(self.ids),
                html.H2('(`self.mod_upload.return_uploaded_table_view()` below)'),
                self.mod_upload.return_uploaded_table_view(self.ids),
            ]),
        ])

    def create_callbacks(self):
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


instance = UploadModuleDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
