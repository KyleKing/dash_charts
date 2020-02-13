"""Example Pareto Chart."""

from pathlib import Path

import dash_html_components as html
import pandas as pd
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.pareto_chart import ParetoChart
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import format_app_callback, map_args, min_graph
from icecream import ic


class ParetoDemo(AppBase):
    """Example creating a simple Pareto chart."""

    name = 'Pareto Demo'
    """Application name"""

    raw_data = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    main_chart = None
    """Main chart (Pareto)."""
    chart_id = 'pareto'
    """Unique name for the main chart."""

    def __init__(self, **kwargs):
        """Initialize raw dataset.

        Args:
            **kwargs: Any keyword arguments to pass to the base class

        """
        super().__init__(**kwargs)
        self.raw_data = (pd.read_csv(Path(__file__).parent / 'DowntimeData.csv')
                         .rename(columns={'downtime': 'value'}))
        self.register_uniq_ids([self.chart_id])

    def register_charts(self):
        """Register an empty Pareto chart."""
        # Initialize an example chart
        self.main_chart = ParetoChart(
            title='Example Pareto Chart',
            x_label='Category Title',
            y_label='Measured Downtime (hours)',
            layout_overrides=(
                ('yaxis', 'dtick', 10),
                ('yaxis', 'tickformat', '.0f'),
                ('margin', None, {'l': 75, 'b': 100, 't': 50, 'r': 125}),
                ('height', None, 500),
                ('width', None, 750),
                ('showlegend', None, True),
                ('legend', None, {'x': 0.6, 'y': 0.8, 'bgcolor': 'rgba(240, 240, 240, 0.49)'}),
            ),
        )

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(
            className='section', style={
                'max-width': '1000px',
                'margin-right': 'auto',
                'margin-left': 'auto',
            }, children=[
                html.H4(children='Example Pareto Chart'),
                html.Div([min_graph(id=self.ids[self.chart_id], figure={})]),
            ],
        )

    def register_callbacks(self):
        """Register the chart callbacks. Not implemented yet."""
        outputs = ((self.chart_id, 'figure'), )
        inputs = ((self.chart_id, 'clickData'), )
        states = ()

        # TODO: Make this simpler - maybe format_app_callback can be a decorator?
        @self.app.callback(*format_app_callback(self.ids, outputs, inputs, states))
        def update_chart(*args):
            a_in, a_states = map_args(self.ids, args, inputs, states)
            ic(a_in[self.ids[self.chart_id]])  # clickData
            return [self.main_chart.create_figure(raw_df=self.raw_data, show_count=True)]
            # # Better return outputs
            # new_figure = self.main_chart.create_figure(raw_df=self.raw_data, show_count=True)
            # return map_outputs({self.chart_id: new_figure})


if __name__ == '__main__':
    port = parse_cli_port()
    ParetoDemo().run(debug=True, port=port)
