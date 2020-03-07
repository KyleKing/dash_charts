"""Example Alignment Chart."""

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.exceptions import PreventUpdate
from dash_charts.alignment_chart import AlignChart
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import min_graph

# TODO: Create fake CSV data that has an actual shape for measurement


class AlignmentDemo(AppBase):
    """Example creating an alignment chart."""

    name = 'Example Alignment Chart'
    """Application name"""

    data_raw = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    chart_main = None
    """Main chart (Alignment)."""

    id_chart = 'alignment'
    """Unique name for the main chart."""

    id_slider = 'slider-input'
    id_status = 'slider-status'
    id_button = 'button-reset'

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        self.register_uniq_ids([self.id_chart, self.id_slider, self.id_status, self.id_button])

        self._generate_data()

    def create_charts(self):
        """Initialize charts."""
        self.chart_main = AlignChart(
            title='Positioning Error Analysis',
            xlabel='X-Axis Measurements (µm)',
            ylabel='Y-Axis Measurements (µm)',
            layout_overrides=(
                ('height', None, 600),
                ('width', None, 800),
            ),
            meas_lbl='Positioning Error',
            ideal_lbl='Expected Position',
            pad=0.75,
        )

    def _generate_data(self):
        """Create self.data_raw with sample data."""
        # Generate a grid of initial points
        dim = 5
        count = pow(dim, 2)
        grid = np.meshgrid(np.linspace(1, dim, dim), np.linspace(1, dim, dim))

        # Combine into a dataframe
        self.data_raw = pd.DataFrame(data={
            'x': grid[0].flatten(),
            'y': grid[1].flatten(),
            'x_delta': np.random.randn(count) / 12,
            'y_delta': np.random.randn(count) / 8,
            'label': [f'Point {idx}' for idx in range(count)],
        })

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        s_ticks = range(0, 20 + 1, 2)  # TODO: no magic numbers
        return html.Div(
            style={
                'max-width': '850px',
                'margin-right': 'auto',
                'margin-left': 'auto',
            }, children=[
                html.H4(children=self.name),
                html.Div([min_graph(id=self.ids[self.id_chart], figure={})]),
                html.Div(id=self.ids[self.id_status]),
                dcc.Slider(
                    id=self.ids[self.id_slider], step=0.1,  # vertical=True,
                    min=min(s_ticks), max=max(s_ticks), marks={idx: f'{idx}' for idx in s_ticks},
                ),
                html.Button('Reset to 1', id=self.ids[self.id_button]),
            ],
        )

    def create_callbacks(self):
        """Register callbacks to handle user interaction."""
        @self.callback([(self.id_chart, 'figure')], [(self.id_slider, 'value')], [])
        def update_alignment_chart(stretch):
            # Create/update the alignment chart with the user-configurable stretch input
            if stretch is None:
                raise PreventUpdate
            return [self.chart_main.create_figure(df_raw=self.data_raw, stretch=stretch)]

        @self.callback([(self.id_status, 'children')], [(self.id_slider, 'value')], [])
        def indicate_slider_position(stretch):
            # Add text describing the current slider value
            return [f'Selected stretch factor: `{stretch}`']

        @self.callback([(self.id_slider, 'value')], [(self.id_button, 'n_clicks')], [])
        def reset_stretch(n_clicks):
            return [1]  # Button to reset the stretch factor


if __name__ == '__main__':
    port = parse_cli_port()
    AlignmentDemo().run(port=port, debug=True)
else:
    instance = AlignmentDemo()
    FLASK_HANDLE = instance.get_server()
