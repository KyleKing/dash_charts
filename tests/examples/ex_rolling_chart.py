"""Example Rolling Mean and Filled Standard Deviation Chart."""

import dash_html_components as html
import numpy as np
import pandas as pd
from dash_charts.dash_helpers import parse_dash_cli_args
from dash_charts.rolling_chart import RollingChart
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import min_graph


class RollingDemo(AppBase):
    """Example creating a rolling mean chart."""

    name = 'Example Rolling Chart'
    """Application name"""

    data_raw = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    chart_main = None
    """Main chart (Rolling)."""

    id_chart = 'rolling'
    """Unique name for the main chart."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart])

        self._generate_data()

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = RollingChart(
            title='Sample Timeseries Chart with Rolling Calculations',
            xlabel='Index',
            ylabel='Measured Value',
        )

    def _generate_data(self):
        """Create self.data_raw with sample data."""
        # Generate random data points
        count = 1000
        mu, sigma = (15, 10)  # mean and standard deviation
        samples = np.random.normal(mu, sigma, count)
        # Add a break at the mid-point
        mid_count = count / 2
        y_vals = [samples[_i] + (-1 if _i > mid_count else 1) * _i / 10.0 for _i in range(count)]

        # Combine into a dataframe
        self.data_raw = pd.DataFrame(data={
            'x': range(count),
            'y': y_vals,
            'label': [f'Point {idx}' for idx in range(count)],
        })
        colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#7f7f7f', '#17becf', None,
        ]
        indices = [20 + int(idx * count / len(colors)) for idx in range(len(colors))]
        self.annotations = [
            (self.data_raw['x'][indices[idx]], self.data_raw['y'][indices[idx]], 'Additional Information', color)
            for idx, color in enumerate(colors)
        ]

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(
            style={
                'maxWidth': '1000px',
                'marginRight': 'auto',
                'marginLeft': 'auto',
            }, children=[
                html.H4(children=self.name),
                html.Div([min_graph(
                    id=self.ids[self.id_chart],
                    figure=self.chart_main.create_figure(
                        df_raw=self.data_raw,
                        # annotations=self.annotations,  # FIXME: Implement annotations
                    ),
                )]),
            ],
        )

    def create_callbacks(self):
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


instance = RollingDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
