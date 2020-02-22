"""Example Pareto Chart."""

from io import StringIO

import dash_html_components as html
import pandas as pd
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.pareto_chart import ParetoChart
from dash_charts.utils_app import STATIC_URLS, AppBase, init_app
from dash_charts.utils_fig import min_graph

CSV_DATA = """category,events
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
        """Initialize app with custom stylesheets.

        Args:
            kwargs: keyword arguments passed to __init__

        """
        app = init_app(external_stylesheets=[STATIC_URLS[key] for key in ['dash']])
        super().__init__(app=app, **kwargs)
        self.raw_data = (pd.read_csv(StringIO(CSV_DATA))
                         .rename(columns={'events': 'value'}))
        self.register_uniq_ids([self.id_chart])

    def register_charts(self):
        """Initialize charts."""
        self.main_chart = ParetoChart(
            title='Made Up Categories vs. Made Up Counts',
            xlabel='Categories',
            ylabel='Count',
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
        # Override ParetoParameters as needed
        self.main_chart.show_count = True
        self.main_chart.pareto_colors = {'bar': '#A5AFC8', 'line': '#391D2F'}

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
                    figure=self.main_chart.create_figure(raw_df=self.raw_data),
                )]),
            ],
        )

    def register_callbacks(self):
        """Register the chart callbacks.."""
        pass  # No callbacks necessary for this simple example


if __name__ == '__main__':
    port = parse_cli_port()
    ParetoDemo().run(port=port, debug=True)
