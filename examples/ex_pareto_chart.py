"""Example Pareto Chart."""

from io import StringIO

import dash_html_components as html
import pandas as pd
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.pareto_chart import ParetoChart
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import min_graph

CSV_DATA = """categories,downtime
Every Cloud Has a Silver Lining,10
Every Cloud Has a Silver Lining,66
SHOULDN'T APPEAR BECAUSE NONE VALUE,
SHOULDN'T APPEAR BECAUSE 0 VALUE,0
SHOULDN'T APPEAR BECAUSE 0 VALUE,0
SHOULDN'T APPEAR BECAUSE 0 VALUE,0
Back To the Drawing Board,30
Back To the Drawing Board,30
Back To the Drawing Board,30
Back To the Drawing Board,30
Back To the Drawing Board,11
Lickety Split,1
Lickety Split,0
Mountain Out of a Molehill,41
Everything But The Kitchen Sink,42
Happy as a Clam,92"""


class ParetoDemo(AppBase):
    """Example creating a simple Pareto chart."""

    name = 'Example Pareto Chart'
    """Application name"""

    raw_data = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    main_chart = None
    """Main chart (Pareto)."""

    id_chart = 'pareto'
    """Unique name for the main chart."""

    def __init__(self, **kwargs):
        """Initialize raw dataset.

        Args:
            **kwargs: Any keyword arguments to pass to the base class

        """
        super().__init__(**kwargs)
        self.raw_data = (pd.read_csv(StringIO(CSV_DATA))
                         .rename(columns={'downtime': 'value'}))
        self.register_uniq_ids([self.id_chart])

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
                html.H4(children=self.name),
                html.Div([min_graph(
                    id=self.ids[self.id_chart],
                    figure=self.main_chart.create_figure(raw_df=self.raw_data, show_count=True),
                )]),
            ],
        )

    def register_callbacks(self):
        """Register the chart callbacks.."""
        pass  # No callbacks necessary for this simple example

        # # TODO: Remove this code - keep for now until I can make a more complex example that utilizes this
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
    ParetoDemo().run(debug=True, port=port)
