"""Example Rolling Mean and Filled Standard Deviation Chart."""

import dash_html_components as html
import numpy as np
import pandas as pd
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.rolling_chart import RollingChart
from dash_charts.utils_app import STATIC_URLS, AppBase, init_app
from dash_charts.utils_fig import min_graph


class RollingDemo(AppBase):
    """Example creating a the rolling mean chart."""

    name = 'Example Rolling Chart'
    """Application name"""

    raw_data = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    main_chart = None
    """Main chart (Rolling)."""

    id_chart = 'rolling'
    """Unique name for the main chart."""

    def __init__(self):
        """Initialize app with custom stylesheets."""
        app = init_app(external_stylesheets=[STATIC_URLS[key] for key in ['dash']])
        super().__init__(app=app)

        self._generate_data()

        self.register_uniq_ids([self.id_chart])

    def register_charts(self):
        """Initialize charts."""
        self.main_chart = RollingChart(
            title='Sample Timeseries Chart with Rolling Calculations',
            xlabel='Index',
            ylabel='Measured Value',
        )

    def _generate_data(self):
        """Create self.df_demo with sample data."""
        # Generate random data points
        count = 1000
        mu, sigma = (15, 10)  # mean and standard deviation
        samples = np.random.normal(mu, sigma, count)
        # Add a break at the mid-point
        mid_count = count / 2
        y_vals = [samples[_i] + (-1 if _i > mid_count else 1) * _i / 10.0 for _i in range(count)]

        # Combine into a dataframe
        self.raw_data = pd.DataFrame(data={
            'x': range(count),
            'y': y_vals,
            'label': [f'Point {idx}' for idx in range(count)],
        })
        colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#7f7f7f', '#17becf', None,
        ]
        indices = [20 + int(idx * count / len(colors)) for idx in range(len(colors))]
        self.annotations = [
            (self.raw_data['x'][indices[idx]], self.raw_data['y'][indices[idx]], 'Additional Information', color)
            for idx, color in enumerate(colors)
        ]

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
                    id=self.ids[self.id_chart],
                    figure=self.main_chart.create_figure(
                        raw_df=self.raw_data,
                        # annotations=self.annotations,
                    ),
                )]),
            ],
        )

    def register_callbacks(self):
        """Register the chart callbacks.."""
        pass  # No callbacks necessary for this simple example

        # # TODO: Implement SQL parser to load data in real time!
        # from dash_charts.utils_fig import map_args, map_outputs, min_graph  # noqa: E800
        # outputs = ((self.id_chart, 'figure'), )  # noqa: E800
        # inputs = ((self.id_chart, 'clickData'), )  # noqa: E800
        # states = ()  # noqa: E800
        # @self.callback(outputs, inputs, states)  # noqa: E800
        # def update_chart(*args):  # noqa: E800
        #     # Example handling input arguments  # noqa: E800
        #     a_in, a_states = map_args(args, inputs, states)  # noqa: E800
        #     ic(a_in[self.id_chart]['clickData'])  # noqa: E800
        #     # Example mapping output results  # noqa: E800
        #     new_figure = self.main_chart.create_figure(raw_df=self.raw_data, show_count=True)  # noqa: E800
        #     return map_outputs(outputs, [(self.id_chart, 'figure', new_figure)])  # noqa: E800


if __name__ == '__main__':
    port = parse_cli_port()
    RollingDemo().run(port=port, debug=True)
