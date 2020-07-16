"""Example Time Vis Chart."""

import dash_html_components as html
import pandas as pd
from dash_charts.dash_helpers import parse_dash_cli_args
from dash_charts.time_vis_chart import TimeVisChart
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import min_graph


class TimeVisDemo(AppBase):  # noqa: H601
    """Example creating a TimeVis chart."""

    name = 'Example TimeVis Chart'
    """Application name"""

    chart_main = None
    """Main chart (TimeVis)."""

    id_chart = 'TimeVis'
    """Unique name for the main chart."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart])

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = TimeVisChart(
            title='Pool Schedule (Sample TimeVis Chart)',
            xlabel=None,
            ylabel=None,
        )
        self.chart_main.fillcolor = '#A9DDDF'

    def generate_data(self):
        """Create self.data_raw with sample data."""
        # Note: Plotly-supported time formats https://plotly.com/chart-studio-help/date-format-and-time-series/
        # TODO: "All Category" (vertical background shape with no category, but label)
        # TODO: Event (no end date, so vertical line to YAxis)
        data = [
            {'category': 'Restricted Swim Hours', 'label': 'Adult Swim',
             'start': '2020-07-01 16:00:00', 'end': '2020-07-01 19:30:00'},
            {'category': 'Restricted Swim Hours', 'label': 'Adult Swim',
             'start': '2020-07-02 16:00:00', 'end': '2020-07-02 19:30:00'},
            {'category': 'Restricted Swim Hours', 'label': 'Adult Swim',
             'start': '2020-07-03 16:00:00', 'end': '2020-07-03 19:30:00'},
            {'category': 'Open Swim', 'label': 'Open',
             'start': '2020-07-01 09:00:00', 'end': '2020-07-01 15:50:00'},
            {'category': 'Open Swim', 'label': 'Open',
             'start': '2020-07-02 09:00:00', 'end': '2020-07-02 15:50:00'},
            {'category': 'Open Swim', 'label': 'Open',
             'start': '2020-07-03 09:00:00', 'end': '2020-07-03 15:50:00'},
            {'category': 'Restricted Swim Hours', 'label': 'Lap',
             'start': '2020-07-01 07:00:00', 'end': '2020-07-01 08:30:00'},
            {'category': 'Restricted Swim Hours', 'label': 'Lap',
             'start': '2020-07-02 07:00:00', 'end': '2020-07-02 08:30:00'},
            {'category': 'Restricted Swim Hours', 'label': 'Lap',
             'start': '2020-07-03 07:00:00', 'end': '2020-07-03 08:30:00'},
            {'category': 'Swim Team', 'label': 'P-A',
             'start': '2020-07-01 08:00:00', 'end': '2020-07-01 09:00:00'},
            {'category': 'Swim Team', 'label': 'P-A',
             'start': '2020-07-02 08:00:00', 'end': '2020-07-02 09:00:00'},
            {'category': 'Swim Team', 'label': 'P-A',
             'start': '2020-07-03 08:00:00', 'end': '2020-07-03 09:00:00'},
            {'category': 'Swim Team', 'label': 'P-B',
             'start': '2020-07-01 14:00:00', 'end': '2020-07-01 15:00:00'},
            {'category': 'Swim Team', 'label': 'P-B',
             'start': '2020-07-02 14:00:00', 'end': '2020-07-02 15:00:00'},
            {'category': 'Swim Team', 'label': 'P-B',
             'start': '2020-07-03 14:00:00', 'end': '2020-07-03 15:00:00'},
            {'category': 'Open Swim', 'label': 'Weekend Open Swim',
             'start': '2020-07-04 08:00:00', 'end': '2020-07-04 20:00:00'},
            {'category': 'Open Swim', 'label': 'Weekend Open Swim',
             'start': '2020-07-05 08:00:00', 'end': '2020-07-05 20:00:00'},
        ]
        self.data_raw = pd.DataFrame.from_dict(data)

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


instance = TimeVisDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
