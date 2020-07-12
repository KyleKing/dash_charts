"""Example Gantt Chart.

Based on D3 demo from: https://github.com/alampros/Gantt-Chart#creating-a-simple-gantt-chart

"""

import dash_html_components as html
from dash_charts.dash_helpers import parse_dash_cli_args
from dash_charts.gantt import GanttChart
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import min_graph


class GanttDemo(AppBase):
    """Example creating a Gantt chart."""

    name = 'Example Gantt Chart'
    """Application name"""

    data_raw = [
        {'category': 'Project A', 'label': 'task1', 'start': '2014-02-01', 'end': '01/05/2014', 'progress': 0.15},
        {'category': 'Project A', 'label': 'task1.1', 'start': '2014-03-01', 'end': '01/05/2014'},
        {'category': 'Project A', 'label': 'task2', 'start': '2014-04-01', 'end': '01/08/2014', 'progress': 0.35},
        {'category': 'Project A', 'label': 'deployment 1', 'start': '2014-07-01'},
        {'category': 'Project A', 'label': 'task2.1', 'start': '2014-07-01', 'end': '01/08/2014', 'progress': 0.75},
        {'category': 'Project B', 'label': 'task3', 'start': '2014-10-01', 'end': '01/12/2014', 'progress': 0.6},
        {'category': 'Project B', 'label': 'deployment 2', 'start': '2014-03-01'},
    ]
    """All in-memory tasks and milestones referenced by callbacks and plotted. If modified, will impact all viewers."""

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

    def generate_data(self):
        """Create self.data_raw with sample data."""
        pass

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
