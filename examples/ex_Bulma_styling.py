"""Example Bulma layout.

See documentation on Bulma layouts: https://bulma.io/documentation/layout/tiles/

"""

import dash_html_components as html
import numpy as np
import pandas as pd
import plotly_express as px
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.rolling_chart import RollingChart
from dash_charts.utils_app import init_app
from dash_charts.utils_fig import min_graph


class BulmaStylingDemo:
    """Demo laying out a 3 column grid with Bulma where.

    - the first column has three tiles
    - the middle column is half the full screen width
    - the tiles will wrap on smaller screens

    """

    def __init__(self):
        """Initialize app."""
        self.app = init_app()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        # ----------------------------------------------------------------------
        # > Sample data from `ex_rolling_chart.py`
        # Generate random data points
        count = 1000
        mu, sigma = (15, 10)  # mean and standard deviation
        samples = np.random.normal(mu, sigma, count)
        # Add a break at the mid-point
        midCount = count / 2
        yVals = [samples[_i] + (-1 if _i > midCount else 1) * _i / 10.0 for _i in range(count)]
        # Combine into a dataframe
        self.dfDemo = pd.DataFrame(data={
            'x': range(count),
            'y': yVals,
            'label': ['Point {}'.format(idx) for idx in range(count)],
        })
        # > End sample data
        # ----------------------------------------------------------------------

        # Initialize an example chart
        self.exRolling = RollingChart(
            title='Sample Timeseries Chart',
            x_label='Index',
            y_label='Measured Value',
        )

        # Create application layout
        self._createLayout()

        self.app.run_server(debug=debug, **kwargs)

    def _createLayout(self):
        """Create application layout."""
        # Initialize the dashboard layout
        self.app.layout = html.Div(className='section', children=[
            html.Div(className='tile is-ancestor', children=[
                html.Div(className='tile is-parent is-vertical is-3', children=[
                    html.Article(className='tile is-child notification', children=[
                        html.P(className='title', children='Top Vertical Tile'),
                        html.P(
                            className='subtitle',
                            children='Uses notification class for grey background and internal padding',
                        ),
                        html.P(className='subtitle', children='Could also add is-info, is-warning, etc.'),
                    ]),
                    html.Article(className='tile is-child', children=[
                        html.P(className='title', children='Vertical...'),
                        html.P(className='subtitle', children='(Top tile)'),
                        min_graph(
                            figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=200),
                        ),
                    ]),
                    html.Article(className='tile is-child', children=[
                        html.P(className='title', children='...tiles'),
                        html.P(className='subtitle', children='(Bottom tile)'),
                        min_graph(
                            figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=200),
                        ),
                    ]),
                ]),
                min_graph(
                    className='tile is-child is-6 is-block-desktop',
                    figure=self.exRolling.create_figure(df=self.dfDemo, dataLbl='Demo Data', rollingCount=4),
                ),
                html.Article(className='tile is-child is-3 is-block-desktop', children=[
                    html.P(className='title', children='A Small Chart'),
                    min_graph(
                        figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=350),
                    ),
                    html.P(className='subtitle', children='An Image'),
                    html.Img(src='https://media.giphy.com/media/JGQe5mxayVF04/giphy.gif')
                ]),
            ]),
        ])


if __name__ == '__main__':
    port = parse_cli_port()
    BulmaStylingDemo().run(port=port)
