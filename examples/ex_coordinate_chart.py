"""Example Coordinate Chart."""

import cmath
import math

import dash_html_components as html
import numpy as np
import pandas as pd
from dash_charts import helpers
from dash_charts.coordinate_chart import CoordinateChart


class CoordinateDemo:
    """Demo Simple Rolling Mean Chart."""

    def __init__(self):
        """Initialize app."""
        self.app = helpers.initApp()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        self.gridDims = (3, 2)
        opp = 0.5 * math.cos(cmath.pi / 4)
        adj = 0.5 * math.sin(cmath.pi / 4)
        self.coord = {
            'x': [0.5, 1 - adj, 1.0, 1 + adj, 1.5, 1 + adj, 1.0, 1 - adj],
            'y': [1.0, 1 - opp, 0.5, 1 - opp, 1.0, 1 + opp, 1.5, 1 + opp],
        }
        self.exCoord = CoordinateChart(
            title='Example Coordinate Chart',
            customLayoutParams=(
                ('height', None, 650),
                ('width', None, 750),
            ),
            gridDims=self.gridDims,
            coord=self.coord,
        )

        # Create sample data and application layout
        self._generateData()
        self._createLayout()

        self.app.run_server(debug=debug, **kwargs)

    def _generateData(self):
        """Create self.dfDemo with sample data."""
        # Generate a list of random values for the chart
        self.dfDemo = pd.DataFrame(data={
            'values': np.random.randint(500, size=(self.gridDims[0] * self.gridDims[1] * len(self.coord['x']))),
        })

    def _createLayout(self):
        """Create application layout."""
        self.app.layout = html.Div(
            className='section',
            children=[
                html.Div([
                    helpers.MinGraph(
                        id='coordinate-chart',
                        figure=self.exCoord.createFigure(
                            df=self.dfDemo,
                            markerKwargs={'colorscale':'Viridis', 'size': 16, 'symbol': 'square'},
                        ),
                    ),
                ]),
            ],
        )


if __name__ == '__main__':
    CoordinateDemo().run()
