"""Example Bootstrap layout.

See documentation: https://dash-bootstrap-components.opensource.faculty.ai/l/components

"""

import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
from implements import implements

from dash_charts.utils_app import AppBase, AppInterface
from dash_charts.utils_fig import min_graph
from dash_charts.utils_helpers import parse_dash_cli_args


@implements(AppInterface)
class BootstrapStylingDemo(AppBase):
    """Demo laying out a 3 column grid with Bootstrap where.

    - the first column has three tiles
    - the middle column is half the full screen width
    - the tiles will wrap on smaller screens

    """

    name = 'Example Bootstrap Styling Demo'
    """Application name"""

    external_stylesheets = [dbc.themes.FLATLY]  # DARKLY, FLATLY, etc. (https://bootswatch.com/)
    """List of external stylesheets. Default is minimal Dash CSS. Only applies if app argument not provided."""

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids(['placeholder'])

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements."""
        pass

    def return_navbar(self):
        """Return Dash navbar layout."""
        return dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink('Link', href='#')),
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label='Menu',
                    children=[
                        dbc.DropdownMenuItem('Entry 1'),
                        dbc.DropdownMenuItem('Entry 2'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Entry 3'),
                    ],
                ),
            ],
            brand='Demo',
            brand_href='#',
            sticky='top',
        )

    def return_body(self):
        """Return Dash body layout."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H2('Heading'),
                    html.P('Done id edit non mi sorta gravid at get meets.\n' * 10),
                    dbc.Button('View details', color='secondary'),
                ], md=4),
                dbc.Col([
                    html.H2('Graph'),
                    min_graph(figure={'data': [{'x': [1, 2, 3], 'y': [1, 4, 9]}]}),
                ]),
            ]),
        ], className='mt-4')

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(children=[
            # Code based on DBC example
            self.return_navbar(),
            self.return_body(),
            # Re-implementation of the code from Bulma example in bootstrap
            # TODO: Decide which styles from Bulma should be compared here
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Article(children=[
                            html.P(children='Top Vertical Tile'),
                            html.P(children='Notification class for grey background'),
                            html.P(children='Could also add is-info, is-warning, etc.'),
                        ]),
                        html.Article(children=[
                            html.P(children='Vertical...'),
                            html.P(children='(Top tile)'),
                            min_graph(
                                figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=200),
                            ),
                        ]),
                        html.Article(children=[
                            html.P(children='...tiles'),
                            html.P(children='(Bottom tile)'),
                            min_graph(
                                figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=200),
                            ),
                        ]),
                    ], sm=12, md=3),
                    dbc.Col([
                        min_graph(
                            className='',
                            figure={},
                        ),
                    ], sm=12, md=6),
                    dbc.Col([
                        html.Article(children=[
                            html.P(children='A Small Chart'),
                            min_graph(figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=350)),
                            html.P(children='An Image'),
                            html.Img(
                                src='https://media.giphy.com/media/JGQe5mxayVF04/giphy.gif',
                                style={'maxWidth': '100%'},
                            ),
                        ]),
                    ], sm=12, md=3),
                ]),
            ], className='mt-5'),  # Shorthand `mt-#` for margin top
        ])

    def create_callbacks(self) -> None:
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


instance = BootstrapStylingDemo
app = instance()
app.create()
if __name__ == '__main__':
    app.run(**parse_dash_cli_args())
else:
    FLASK_HANDLE = app.get_server()
