"""Example Coordinate Chart."""

import calendar

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash import html
from implements import implements

from dash_charts import coordinate_chart
from dash_charts.coordinate_chart import CoordinateChart
from dash_charts.utils_app import AppBase, AppInterface
from dash_charts.utils_fig import min_graph
from dash_charts.utils_helpers import parse_dash_cli_args

# TODO: Also set marker size based on value?
# TODO: Re-align alignment charts into line and update screenshot
# TODO: Maybe green heat map like Github? For one year?


@implements(AppInterface)  # noqa: H601
class CoordinateDemo(AppBase):
    """Example creating basic Coordinate Charts."""

    name = 'Example Coordinate Charts'
    """Application name"""

    external_stylesheets = [dbc.themes.FLATLY]

    data_raw_years = None
    data_raw_months = None
    data_raw_circle = None
    """In-memory data referenced by callbacks. If modified, will impact all viewers (Years/Months/Circle)."""

    chart_years = None
    chart_months = None
    chart_circle = None
    """Main charts (Coordinate Year/Month/Circle)."""

    id_chart_years = 'years-chart'
    id_chart_months = 'months-chart'
    id_chart_circle = 'circle-chart'
    """Unique name for each chart (Year/Month/Circle)."""

    grid_years = coordinate_chart.YearGrid()
    grid_months = coordinate_chart.MonthGrid(titles=[calendar.month_name[2]])  # uses Feb
    grid_circle = coordinate_chart.CircleGrid(grid_dims=(5, 4))  # set grid to arbitrary 5x4
    """Coordinate chart grids (Year/Month/Circle)."""

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart_years, self.id_chart_months, self.id_chart_circle])

        day, month, year = (20, 11, 2020)  # Alteratively use `now = datetime.datetime.now()`` and `now.day` etc.

        # Data for the Year Chart
        month_list = [
            np.random.randint(1e2, size=calendar.monthrange(year, month_idx)[1])
            for month_idx in range(1, month + 1)
        ]
        # Remove all future data for the current month
        month_list[month - 1] = month_list[month - 1][:(day - 1)]
        self.data_raw_years = pd.DataFrame(data={'values': self.grid_years.format_data(month_list, year)})

        # Data for the Month Chart
        month_list = np.random.randint(1e4, size=calendar.monthrange(year, month)[1])
        self.data_raw_months = pd.DataFrame(data={'values': self.grid_months.format_data(month_list, year, month)})

        # Generated data for the Circle Chart
        len_points = np.multiply(*self.grid_circle.grid_dims) * len(self.grid_circle.corners['x'])
        values = np.random.randint(1e9, size=len_points)
        self.data_raw_circle = pd.DataFrame(data={'values': values})
        # Remove a known number of random values from the data set (for the circle Demo)
        remove_count = 5
        for idx in list(set(np.random.randint(len(values), size=remove_count * 2)))[:remove_count]:
            self.data_raw_circle['values'][idx] = None

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_years = CoordinateChart(
            title='Example Year Grid',
            grid_dims=self.grid_years.grid_dims,
            corners=self.grid_years.corners,
            titles=self.grid_years.titles,
            layout_overrides=(
                ('height', None, 700),
                ('width', None, 500),
            ),
        )
        # Override Coordinate Parameters as needed
        self.chart_years.marker_kwargs = self.grid_years.marker_kwargs
        self.chart_years.border_opacity = 0

        self.chart_months = CoordinateChart(
            title='Example Month Grid',
            grid_dims=self.grid_months.grid_dims,
            corners=self.grid_months.corners,
            titles=self.grid_months.titles,
            layout_overrides=(
                ('height', None, 400),
                ('width', None, 400),
            ),
        )
        # Override Coordinate Parameters as needed
        self.chart_months.marker_kwargs = self.grid_months.marker_kwargs
        self.chart_months.marker_kwargs['colorscale'] = 'Bluered'

        self.chart_circle = CoordinateChart(
            title='Example Circle Grid',
            grid_dims=self.grid_circle.grid_dims,
            corners=self.grid_circle.corners,
            titles=self.grid_circle.titles,
            layout_overrides=(
                ('height', None, 750),
                ('width', None, 650),
            ),
        )
        # Override Coordinate Parameters as needed
        self.chart_circle.marker_kwargs = self.grid_circle.marker_kwargs
        self.chart_circle.marker_kwargs['colorscale'] = 'Cividis'

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return dbc.Container([
            dbc.Row([
                html.H4(children=self.name),
            ]),
            dbc.Row([
                dbc.Col(
                    [
                        min_graph(
                            id=self._il[self.id_chart_months],
                            figure=self.chart_months.create_figure(df_raw=self.data_raw_months),
                        ),
                    ], width=4,
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    [
                        min_graph(
                            id=self._il[self.id_chart_years],
                            figure=self.chart_years.create_figure(df_raw=self.data_raw_years),
                        ),
                    ], width=5,
                ),
                dbc.Col(
                    [
                        min_graph(
                            id=self._il[self.id_chart_circle],
                            figure=self.chart_circle.create_figure(df_raw=self.data_raw_circle),
                        ),
                    ], width=5,
                ),
            ]),
        ])

    def create_callbacks(self) -> None:
        """Create Dash callbacks."""
        ...  # No callbacks necessary for this simple example


instance = CoordinateDemo
app = instance()
app.create()
if __name__ == '__main__':
    app.run(**parse_dash_cli_args())
else:
    FLASK_HANDLE = app.get_server()
