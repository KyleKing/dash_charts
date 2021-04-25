"""Example Pareto Chart."""

from io import StringIO

import dash_html_components as html
import pandas as pd
from implements import implements

from dash_charts.pareto_chart import ParetoChart
from dash_charts.utils_app import AppBase, AppInterface
from dash_charts.utils_fig import min_graph
from dash_charts.utils_helpers import parse_dash_cli_args

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


@implements(AppInterface)
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

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart])
        # Format sample CSV data for the Pareto
        self.data_raw = (pd.read_csv(StringIO(CSV_DATA))
                         .rename(columns={'events': 'value'}))

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = ParetoChart(
            title='Made Up Categories vs. Made Up Counts',
            xlabel='Categories',
            ylabel='Count',
            layout_overrides=(
                ('height', None, 500),
                ('width', None, 750),
                ('showlegend', None, True),
                ('legend', None, {'x': 0.6, 'y': 0.8, 'bgcolor': 'rgba(240, 240, 240, 0.49)'}),
            ),
        )
        # Override Pareto Parameters as needed
        self.chart_main.show_count = True
        self.chart_main.pareto_colors = {'bar': '#A5AFC8', 'line': '#391D2F'}

    def return_layout(self) -> dict:
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
                    id=self._il[self.id_chart],
                    figure=self.chart_main.create_figure(df_raw=self.data_raw),
                )]),
            ],
        )

    def create_callbacks(self) -> None:
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


instance = ParetoDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
