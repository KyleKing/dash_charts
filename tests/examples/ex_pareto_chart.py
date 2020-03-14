"""Example Pareto Chart."""

from io import StringIO

import dash_html_components as html
import pandas as pd
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.pareto_chart import ParetoChart
from dash_charts.utils_app import AppBase
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

    data_raw = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    chart_main = None
    """Main chart (Pareto)."""

    id_chart = 'pareto'
    """Unique name for the main chart."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        self.register_uniq_ids([self.id_chart])
        # Format sample CSV data for the Pareto
        self.data_raw = (pd.read_csv(StringIO(CSV_DATA))
                         .rename(columns={'events': 'value'}))

    def create_charts(self):
        """Initialize charts."""
        self.chart_main = ParetoChart(
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
        # Override Pareto Parameters as needed
        self.chart_main.show_count = True
        self.chart_main.pareto_colors = {'bar': '#A5AFC8', 'line': '#391D2F'}

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
                    figure=self.chart_main.create_figure(df_raw=self.data_raw),
                )]),
            ],
        )

    def create_callbacks(self):
        """Register the chart callbacks.."""
        pass  # No callbacks necessary for this simple example


instance = ParetoDemo
if __name__ == '__main__':
    port = parse_cli_port()
    app = instance()
    app.create()
    app.run(port=port, debug=True)
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
