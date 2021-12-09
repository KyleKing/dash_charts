"""Example Time Vis Chart."""

import dash_html_components as html
import pandas as pd
from implements import implements

from dash_charts.time_vis_chart import TimeVisChart
from dash_charts.utils_app import AppBase, AppInterface
from dash_charts.utils_fig import min_graph
from dash_charts.utils_helpers import parse_dash_cli_args


@implements(AppInterface)  # noqa: H601
class TimeVisDemo(AppBase):
    """Example creating a TimeVis chart."""

    name = 'Example TimeVis Chart'
    """Application name"""

    chart_main = None
    """Main chart (TimeVis)."""

    id_chart = 'TimeVis'
    """Unique name for the main chart."""

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart])

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = TimeVisChart(
            title='Pool Schedule (Sample TimeVis Chart)',
            xlabel=None,
            ylabel=None,
        )
        self.chart_main.fillcolor = '#A9DDDF'

    def generate_data(self) -> None:
        """Create self.data_raw with sample data."""
        data = [
            {
                'category': '', 'label': 'Closed',
                'start': '2020-07-01 19:30:00', 'end': '2020-07-02 07:00:00',
            },
            {
                'category': '', 'label': 'Closed',
                'start': '2020-07-02 19:30:00', 'end': '2020-07-03 07:00:00',
            },
            {
                'category': '', 'label': 'Closed',
                'start': '2020-07-03 19:30:00', 'end': '2020-07-04 08:00:00',
            },
            {
                'category': '', 'label': 'Closed',
                'start': '2020-07-04 20:00:00', 'end': '2020-07-05 08:00:00',
            },
        ]
        for day in [1, 2, 3]:
            data.extend([
                {
                    'category': 'Events', 'label': 'Pool Opens to Public',
                    'start': f'2020-07-0{day} 07:00:00', 'end': None,
                },
                {
                    'category': 'Events', 'label': 'Closes',
                    'start': f'2020-07-0{day} 19:30:00', 'end': None,
                },
                {
                    'category': 'Restricted Swim Hours', 'label': 'Adult Swim',
                    'start': f'2020-07-0{day} 16:00:00', 'end': f'2020-07-0{day} 19:30:00',
                },
                {
                    'category': 'Open Swim', 'label': 'Open',
                    'start': f'2020-07-0{day} 09:00:00', 'end': f'2020-07-0{day} 15:50:00',
                },
                {
                    'category': 'Restricted Swim Hours', 'label': 'Lap',
                    'start': f'2020-07-0{day} 07:00:00', 'end': f'2020-07-0{day} 08:30:00',
                },
                {
                    'category': 'Swim Team', 'label': 'P-A',
                    'start': f'2020-07-0{day} 08:00:00', 'end': f'2020-07-0{day} 09:00:00',
                },
                {
                    'category': 'Swim Team', 'label': 'P-B',
                    'start': f'2020-07-0{day} 14:00:00', 'end': f'2020-07-0{day} 15:00:00',
                },
            ])
        for weekend in [4, 5]:
            data.extend([
                {
                    'category': 'Events', 'label': 'Pool Opens to Public',
                    'start': f'2020-07-0{weekend} 08:00:00', 'end': None,
                },
                {
                    'category': 'Events', 'label': 'Closes',
                    'start': f'2020-07-0{weekend} 20:00:00', 'end': None,
                },
                {
                    'category': 'Open Swim', 'label': 'Weekend Open Swim',
                    'start': f'2020-07-0{weekend} 08:00:00', 'end': f'2020-07-0{weekend} 20:00:00',
                },
            ])
        self.data_raw = pd.DataFrame.from_dict(data)

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
                html.Div([
                    min_graph(
                        id=self._il[self.id_chart],
                        figure=self.chart_main.create_figure(df_raw=self.data_raw),
                    ),
                ]),
            ],
        )

    def create_callbacks(self) -> None:
        """Create Dash callbacks."""
        ...  # No callbacks necessary for this simple example


instance = TimeVisDemo
app = instance()
app.create()
if __name__ == '__main__':
    app.run(**parse_dash_cli_args())
else:
    FLASK_HANDLE = app.get_server()
