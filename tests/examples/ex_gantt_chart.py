"""Example Gantt Chart."""

from pathlib import Path

import dash_html_components as html
import pandas as pd
from dash_charts.gantt_chart import GanttChart
from dash_charts.utils_app import AppBase
from dash_charts.utils_helpers import parse_dash_cli_args
from dash_charts.utils_fig import min_graph
from palettable.wesanderson import FantasticFox2_5


class GanttDemo(AppBase):  # noqa: H601
    """Example creating a Gantt chart."""

    name = 'Example Gantt Chart'
    """Application name"""

    chart_main = None
    """Main chart (Gantt)."""

    id_chart = 'Gantt'
    """Unique name for the main chart."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart])

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = GanttChart(
            title='Sample Gantt Chart',
            xlabel=None,
            ylabel=None,
        )
        self.chart_main.pallette = FantasticFox2_5.hex_colors

    def generate_data(self):
        """Create self.data_raw with sample data."""
        csv_filename = Path(__file__).parent / 'ex_gantt_data.csv'
        self.data_raw = pd.read_csv(csv_filename)

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
                    figure=self.chart_main.create_figure(df_raw=self.data_raw),
                )]),
            ],
        )

    def create_callbacks(self):
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


instance = GanttDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
