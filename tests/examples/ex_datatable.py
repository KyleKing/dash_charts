"""Example DataTable."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.modules_datatable import ModuleFilteredTable
from dash_charts.utils_app import AppBase


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

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        # Load sample plotly express data to populate the datatable
        self.data_raw = px.data.gapminder()

        # Register modules
        self.mod_table = ModuleFilteredTable('filtered_table')
        self.modules = [
            self.mod_table,
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
                dcc.Markdown(self.mod_table.table.filter_summary),
                html.Br(),
                html.H1(self.name),
                self.mod_table.return_layout(self.ids, self.data_raw),
            ]),
        ])

    def create_callbacks(self):
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


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

# TODO: CLICKABLE POPUPS
# - Datatable
# 	- Have click able icon in first column of table that triggers a dbc modal with additional information
# 		- Would have layout determined in callback. Could be used to show a timeline, full traceback, or other long
#           form data that can't be displayed in condensed table format
# 		- dbc modal:  https://dash-bootstrap-components.opensource.faculty.ai/l/components/modal
# 		- Would require wildcard props for each row: https://github.com/plotly/dash/issues/475

# # TODO: See: https://dash.plot.ly/datatable/interactivity
# ('datatable-id...', 'derived_virtual_row_ids'),
# ('datatable-id...', 'selected_row_ids'),
# ('datatable-id...', 'active_cell'),


# TODO: Formatting (Typing): https://dash.plot.ly/datatable/typing

# # TODO: Upload data recipe (https://dash.plot.ly/datatable/editable)
# app.layout = html.Div([
#     dcc.Upload(
#         id='datatable-upload',
#         children=html.Div([
#             'Drag and Drop or ',
#             html.A('Select Files')
#         ]),
#         style={
#             'width': '100%', 'height': '60px', 'lineHeight': '60px',
#             'borderWidth': '1px', 'borderStyle': 'dashed',
#             'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
#         },
#     ),
#     dash_table.DataTable(id='datatable-upload-container'),
#     dcc.Graph(id='datatable-upload-graph')
# ])
#
# def parse_contents(contents, filename):
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     if 'csv' in filename:
#         # Assume that the user uploaded a CSV file
#         return pd.read_csv(
#             io.StringIO(decoded.decode('utf-8')))
#     elif 'xls' in filename:
#         # Assume that the user uploaded an excel file
#         return pd.read_excel(io.BytesIO(decoded))
#
# @app.callback([Output('datatable-upload-container', 'data'),
#                Output('datatable-upload-container', 'columns')],
#               [Input('datatable-upload', 'contents')],
#               [State('datatable-upload', 'filename')])
# def update_output(contents, filename):
#     if contents is None:
#         return [{}], []
#     df = parse_contents(contents, filename)
#     return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]
#
# @app.callback(Output('datatable-upload-graph', 'figure'),
#               [Input('datatable-upload-container', 'data')])
# def display_graph(rows):
#     df = pd.DataFrame(rows)
#
#     if (df.empty or len(df.columns) < 1):
#         return {
#             'data': [{
#                 'x': [],
#                 'y': [],
#                 'type': 'bar'
#             }]
#         }
#     return {
#         'data': [{
#             'x': df[df.columns[0]],
#             'y': df[df.columns[1]],
#             'type': 'bar'
#         }]
#     }
