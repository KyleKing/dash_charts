"""Example Coordinate Chart."""

import calendar

import dash_html_components as html
import numpy as np
import pandas as pd
from dash_charts import coordinate_chart
from dash_charts.coordinate_chart import CoordinateChart
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import min_graph


class CoordinateDemo(AppBase):
    """Example creating basic Coordinate Charts."""

    name = 'Example Coordinate Charts'
    """Application name"""

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
    grid_circle = coordinate_chart.CircleGrid()
    """Coordinate chart grids (Year/Month/Circle)."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        self.register_uniq_ids([self.id_chart_years, self.id_chart_months, self.id_chart_circle])

        day, month, year = (20, 11, 2020)  # Alteratively use `now = datetime.datetime.now()`` and `now.day` etc.

        # Data for the Year Chart
        month_list = [
            np.random.randint(10000, size=calendar.monthrange(year, month_idx)[1])
            for month_idx in range(1, month + 1)
        ]
        # Remove all future data for the current month
        month_list[month - 1] = month_list[month - 1][:(day - 1)]
        self.data_raw_years = pd.DataFrame(data={'values': self.grid_years.format_data(month_list, year)})

        # Data for the Month Chart
        month_list = np.random.randint(10000, size=calendar.monthrange(year, month)[1])
        self.data_raw_months = pd.DataFrame(data={'values': self.grid_months.format_data(month_list, year, month)})

        # Generated data for the Circle Chart
        len_points = (self.grid_circle.dims[0] * self.grid_circle.dims[1] * len(self.grid_circle.coord['x']))
        values = np.random.randint(10000, size=len_points)
        self.data_raw_circle = pd.DataFrame(data={'values': values})
        # Remove a known number of random values from the data set (for the circle Demo)
        remove_count = 5
        for idx in list(set(np.random.randint(len(values), size=remove_count * 2)))[:remove_count]:
            self.data_raw_circle['values'][idx] = None

    def create_charts(self):
        """Initialize charts."""
        self.chart_years = CoordinateChart(
            title='Example Year Grid',
            grid_dims=self.grid_years.dims,
            coord=self.grid_years.coord,
            titles=self.grid_years.titles,
            layout_overrides=(
                ('height', None, 700),
                ('width', None, 550),
            ),
        )
        # Override Coordinate Parameters as needed
        self.chart_years.marker_kwargs = self.grid_years.marker_kwargs
        self.chart_years.border_opacity = 0

        self.chart_months = CoordinateChart(
            title='Example Month Grid',
            grid_dims=self.grid_months.dims,
            coord=self.grid_months.coord,
            titles=self.grid_months.titles,
            layout_overrides=(
                ('height', None, 600),
                ('width', None, 600),
            ),
        )
        # Override Coordinate Parameters as needed
        self.chart_months.marker_kwargs = self.grid_months.marker_kwargs

        self.chart_circle = CoordinateChart(
            title='Example Circle Grid',
            grid_dims=self.grid_circle.dims,
            coord=self.grid_circle.coord,
            titles=self.grid_circle.titles,
            layout_overrides=(
                ('height', None, 650),
                ('width', None, 750),
            ),
        )
        # Override Coordinate Parameters as needed
        self.chart_circle.marker_kwargs = self.grid_circle.marker_kwargs
        # # NOTE: Uncomment for logarithmic colorscale
        # self.chart_circle.marker_kwargs['colorscale'] = custom_colorscales.logFire

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(
            style={
                'max-width': '1000px',
                'margin-right': 'auto',
                'margin-left': 'auto',
            }, children=[
                html.H4(children=self.name),
                html.Div([min_graph(
                    id=self.ids[self.id_chart_years],
                    figure=self.chart_years.create_figure(df_raw=self.data_raw_years),
                )]),
                html.Div([min_graph(
                    id=self.ids[self.id_chart_months],
                    figure=self.chart_months.create_figure(df_raw=self.data_raw_months),
                )]),
                html.Div([min_graph(
                    id=self.ids[self.id_chart_circle],
                    figure=self.chart_circle.create_figure(df_raw=self.data_raw_circle),
                )]),
            ],
        )

    def create_callbacks(self):
        """Register the chart callbacks.."""
        pass  # No callbacks necessary for this simple example


if __name__ == '__main__':
    port = parse_cli_port()
    CoordinateDemo().run(port=port, debug=True)
else:
    instance = CoordinateDemo()
    FLASK_HANDLE = instance.get_server()
