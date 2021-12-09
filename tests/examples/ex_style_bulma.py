"""Example Bulma layout.

See documentation on Bulma layouts: https://bulma.io/documentation/layout/tiles/

"""

import dash_html_components as html
import plotly.express as px
from implements import implements

from dash_charts.utils_app import STATIC_URLS, AppBase, AppInterface
from dash_charts.utils_fig import min_graph
from dash_charts.utils_helpers import parse_dash_cli_args


@implements(AppInterface)
class BulmaStylingDemo(AppBase):
    """Demo laying out a 3 column grid with Bulma where.

    - the first column has three tiles
    - the middle column is half the full screen width
    - the tiles will wrap on smaller screens

    """

    name = 'Example Bulma Styling Demo'
    """Application name"""

    external_stylesheets = [STATIC_URLS['bulmaswatch-flatly']]
    """List of external stylesheets. Default is minimal Dash CSS. Only applies if app argument not provided."""

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids(['---'])

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements."""
        pass

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(
            className='section', children=[
                html.Div(
                    className='tile is-ancestor', children=[
                        html.Div(
                            className='tile is-parent is-vertical is-3', children=[
                                html.Article(
                                    className='tile is-child notification', children=[
                                        html.P(className='title', children='Top Vertical Tile'),
                                        html.P(className='subtitle', children='Notification class for grey background'),
                                        html.P(className='subtitle', children='Could also add is-info, is-warning, etc.'),
                                    ],
                                ),
                                html.Article(
                                    className='tile is-child', children=[
                                        html.P(className='title', children='Vertical...'),
                                        html.P(className='subtitle', children='(Top tile)'),
                                        min_graph(
                                            figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=200),
                                        ),
                                    ],
                                ),
                                html.Article(
                                    className='tile is-child', children=[
                                        html.P(className='title', children='...tiles'),
                                        html.P(className='subtitle', children='(Bottom tile)'),
                                        min_graph(
                                            figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=200),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        min_graph(
                            className='tile is-child is-6 is-block-desktop',
                            figure={},
                        ),
                        html.Article(
                            className='tile is-child is-3 is-block-desktop', children=[
                                html.P(className='title', children='A Small Chart'),
                                min_graph(figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=350)),
                                html.P(className='subtitle', children='An Image'),
                                html.Img(src='https://media.giphy.com/media/JGQe5mxayVF04/giphy.gif'),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def create_callbacks(self) -> None:
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


instance = BulmaStylingDemo
app = instance()
app.create()
if __name__ == '__main__':
    app.run(**parse_dash_cli_args())
else:
    FLASK_HANDLE = app.get_server()
