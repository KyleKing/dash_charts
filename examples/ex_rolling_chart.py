"""Example Rolling Mean and Filled Standard Deviation Chart."""

import dash_html_components as html
import numpy as np
import pandas as pd
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.rolling_chart import RollingChart
from dash_charts.utils_app import init_app
from dash_charts.utils_fig import min_graph


class RollingDemo:
    """Demo Simple Rolling Mean Chart."""

    def __init__(self):
        """Initialize app."""
        self.app = init_app()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        # Initialize an example chart
        self.exRolling = RollingChart(
            title='Sample Timeseries Chart',
            x_label='Index',
            y_label='Measured Value',
        )

        # Create sample data and application layout
        self._generateData()
        self._createLayout()

        self.app.run_server(debug=debug, **kwargs)

    def _generateData(self):
        """Create self.dfDemo with sample data."""
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
        colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#7f7f7f', '#17becf', None,
        ]
        idxs = [20 + int(idx * count / len(colors)) for idx in range(len(colors))]
        self.annotations = [
            (self.dfDemo['x'][idxs[idx]], self.dfDemo['y'][idxs[idx]], 'Additional Information', color)
            for idx, color in enumerate(colors)
        ]

    def _createLayout(self):
        """Create application layout."""
        self.app.layout = html.Div(
            className='section',
            children=[
                html.Div([
                    min_graph(
                        id='rolling-chart',
                        figure=self.exRolling.create_figure(
                            df=self.dfDemo, dataLbl='Demo Data', rollingCount=4,
                            annotations=self.annotations,
                        ),
                    ),
                ]),
            ],
        )


if __name__ == '__main__':
    port = parse_cli_port()
    RollingDemo().run(port=port)
