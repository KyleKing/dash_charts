"""Example Coordinate Chart."""

import dash_html_components as html
import numpy as np
import pandas as pd
from dash_charts import coordinate_chart, helpers  # custom_colorscales


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
            titles=self.grid.titles,
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

        # Remove a known number of random values from the data set (for the circle Demo)
        removeCount = 5
        for idx in list(set(np.random.randint(len(vals), size=removeCount * 2)))[:removeCount]:
            self.dfDemo['values'][idx] = None

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
                                # 'colorscale': custom_colorscales.logFire,
                                'size': 10, 'symbol': 'square',
                            },
                        ),
                    ),
                ]),
            ],
        )


if __name__ == '__main__':
    CoordinateDemo().run()
