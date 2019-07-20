"""Example Rolling Mean and Filled Standard Deviation Chart."""

import dash_html_components as html
import numpy as np
import pandas as pd
from dash_charts import helpers
from dash_charts.rolling_chart import RollingChart


class RollingDemo:
    """Demo Simple Rolling Mean Chart."""

    def __init__(self):
        """Initialize app."""
        self.app = helpers.initApp()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        # Initialize an example chart
        self.exRolling = RollingChart(
            title='Sample Timeseries Chart',
            xLbl='Index',
            yLbl='Measured Value',
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

    def _createLayout(self):
        """Create application layout."""
        self.app.layout = html.Div(
            className='section',
            children=[
                html.H4(children='Example Rolling  Chart'),
                html.Div([
                    helpers.MinGraph(
                        id='rolling-chart',
                        figure=self.exRolling.createFigure(
                            df=self.dfDemo, dataLbl='Demo Data', rollingCount=4,
                        ),
                    ),
                ]),
            ],
        )


if __name__ == '__main__':
    RollingDemo().run()
