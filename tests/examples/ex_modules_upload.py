"""Example of the Upload Module."""

import dash_bootstrap_components as dbc
from dash import html
from implements import implements

from dash_charts.components import format_email_pass_id, login_form
from dash_charts.modules_upload import UploadModule
from dash_charts.utils_app import AppBase, AppInterface
from dash_charts.utils_callbacks import map_args, map_outputs
from dash_charts.utils_helpers import parse_dash_cli_args


@implements(AppInterface)  # noqa: H601
class UploadModuleDemo(AppBase):
    """Example using the Upload Module."""

    name = 'Example Use of the Upload Module'
    """Application name"""

    user_info = 'user-info'
    """ID used for showing the currently logged in username."""

    submit_id = 'submit-login'
    """ID used for the submit button element."""

    external_stylesheets = [dbc.themes.FLATLY]  # DARKLY, FLATLY, etc. (https://bootswatch.com/)
    """List of external stylesheets. Default is minimal Dash CSS. Only applies if app argument not provided."""

    data_raw = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    mod_upload = None
    """Main table (DataTable)."""

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.email_id, self.pass_id = format_email_pass_id(self.submit_id)
        self.register_uniq_ids([self.user_info, self.submit_id, self.email_id, self.pass_id])

        # Register modules
        self.mod_upload = UploadModule('filtered_table')
        self.modules = [
            self.mod_upload,
        ]

    def create_elements(self) -> None:
        """Initialize charts and tables."""
        ...

    def _show_current_user(self, username):

        return f'(Currently logged in as: {username})' if username else '(Not Logged In)'

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return dbc.Container([   # noqa: ECE001
            dbc.Col([
                html.H1(self.name),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        login_form(self._il[self.submit_id]),
                    ]),
                    dbc.Col([
                        html.Div([self._show_current_user(None)], id=self._il[self.user_info]),
                    ]),
                ]),
                html.Hr(),
                self.mod_upload.return_layout(self._il),
            ]),
        ])

    def create_callbacks(self) -> None:
        """Create Dash callbacks."""
        outputs = [(self.user_info, 'children'), (self.mod_upload.get(self.mod_upload.id_username_cache), 'data')]
        inputs = [(self.submit_id, 'n_clicks')]
        states = [(self.email_id, 'value'), (self.pass_id, 'value')]

        @self.callback(outputs, inputs, states, pic=False)
        def login_handler(*raw_args):
            a_in, a_state = map_args(raw_args, inputs, states)
            email = a_state[self.email_id]['value']
            # password = a_state[self.pass_id]['value']  # noqa: E800
            print("WARN: The password isn't authenticated. This is just a placeholder")  # noqa: T001

            return map_outputs(
                outputs, [
                    (self.user_info, 'children', self._show_current_user(email)),
                    (self.mod_upload.get(self.mod_upload.id_username_cache), 'data', email),
                ],
            )


instance = UploadModuleDemo
app = instance()
app.create()
if __name__ == '__main__':
    app.run(**parse_dash_cli_args())
else:
    FLASK_HANDLE = app.get_server()
