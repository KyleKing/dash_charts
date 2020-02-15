"""Example Coordinate Chart."""

import calendar
import datetime

import dash_html_components as html
import numpy as np
import pandas as pd
from dash_charts import coordinate_chart  # custom_colorscales
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.utils_app import init_app
from dash_charts.utils_fig import min_graph


class CoordinateDemo:
    """Demo Simple Rolling Mean Chart."""

    def __init__(self):
        """Initialize app."""
        self.app = init_app()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        # ----------------------------------------------------------------------
        # NOTE: Select the grid system. Toggle these lines to update the chart
        # self.grid = coordinate_chart.CircleGrid()
        # self.grid = coordinate_chart.YearGrid()
        self.grid = coordinate_chart.MonthGrid(titles=[calendar.month_name[2]])  # uses Feb
        # ----------------------------------------------------------------------

        self.exCoord = coordinate_chart.CoordinateChart(
            title='Example Coordinate Chart',
            layout_overrides=(
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
        if isinstance(self.grid, coordinate_chart.CircleGrid):
            # Generated data for the circleGrid demo
            # Generate a list of random values for the chart
            lenPoints = (self.grid.dims[0] * self.grid.dims[1] * len(self.grid.coord['x']))
            vals = np.random.randint(10000, size=lenPoints)
            self.dfDemo = pd.DataFrame(data={'values': vals})
            # Remove a known number of random values from the data set (for the circle Demo)
            removeCount = 5
            for idx in list(set(np.random.randint(len(vals), size=removeCount * 2)))[:removeCount]:
                self.dfDemo['values'][idx] = None

        elif isinstance(self.grid, coordinate_chart.YearGrid):
            # Data for the YearGrid demo
            now = datetime.datetime.now()
            monthList = [
                np.random.randint(10000, size=calendar.monthrange(now.year, monthIdx)[1])
                for monthIdx in range(1, now.month + 1)
            ]
            # Remove all future data for the current month
            monthList[now.month - 1] = monthList[now.month - 1][:(now.day - 1)]
            self.dfDemo = pd.DataFrame(data={'values': self.grid.formatData(monthList, now.year)})

        elif isinstance(self.grid, coordinate_chart.MonthGrid):
            # Data for the MonthGrid demo
            month, year = (2, 2016)  # Always plot for February 2016 (Leap Year)
            monthList = np.random.randint(10000, size=calendar.monthrange(year, month)[1])
            self.dfDemo = pd.DataFrame(data={'values': self.grid.formatData(monthList, year, month)})

        else:
            raise RuntimeError('Unknown Grid Type: {}'.format(self.grid))

    def _createLayout(self):
        """Create application layout."""
        markerKwargs = self.grid.markerKwargs
        # markerKwargs['colorscale'] = custom_colorscales.logFire  # NOTE: Uncomment for logarithmic colorscale

        self.app.layout = html.Div(
            className='section',
            children=[
                html.Div([
                    min_graph(
                        id='coordinate-chart',
                        figure=self.exCoord.create_figure(
                            df=self.dfDemo,
                            markerKwargs=markerKwargs,
                        ),
                    ),
                ]),
            ],
        )


if __name__ == '__main__':
    port = parse_cli_port()
    CoordinateDemo().run(port=port, debug=True)
