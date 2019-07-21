"""Example Coordinate Chart."""

import dash_html_components as html
import numpy as np
import pandas as pd
from dash_charts import coordinate_chart, custom_colorscales, helpers


class CoordinateDemo:
    """Demo Simple Rolling Mean Chart."""

    def __init__(self):
        """Initialize app."""
        self.app = helpers.initApp()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        # Select the grid system
        # self.grid = monthGrid()
        self.grid = coordinate_chart.circleGrid()

        self.exCoord = coordinate_chart.CoordinateChart(
            title='Example Coordinate Chart',
            customLayoutParams=(
                ('height', None, 650),
                ('width', None, 750),
            ),
            gridDims=self.grid.dims,
            coord=self.grid.coord,
        )

        # Create sample data and application layout
        self._generateData()
        self._createLayout()

        self.app.run_server(debug=debug, **kwargs)

    def _generateData(self):
        """Create self.dfDemo with sample data."""
        # Generate a list of random values for the chart
        lenPoints = (self.grid.dims[0] * self.grid.dims[1] * len(self.grid.coord['x']))
        vals = np.random.randint(10000, size=lenPoints)
        self.dfDemo = pd.DataFrame(data={'values': vals})

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
                            markerKwargs={
                                'colorscale': custom_colorscales.logFire,
                                'size': 10, 'symbol': 'square',
                            },
                        ),
                    ),
                ]),
            ],
        )


if __name__ == '__main__':
    CoordinateDemo().run()
