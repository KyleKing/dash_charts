"""Example Dash Application."""

from typing import Optional

import dash
import dash_html_components as html
import plotly.express as px
from box import Box
from implements import implements

from dash_charts.pareto_chart import ParetoChart
from dash_charts.utils_app import AppBase, AppInterface
from dash_charts.utils_fig import min_graph

_ID = Box({
    'chart': 'pareto',
})
"""Default App IDs."""


@implements(AppInterface)
class ParetoDemo(AppBase):
    """Example creating a simple Pareto chart."""

    def __init__(self, app: Optional[dash.Dash] = None) -> None:
        """Initialize app and initial data members. Should be inherited in child class and called with super().

        Args:
            app: Dash instance. If None, will create standalone app. Otherwise, will be part of existing app

        """
        self.name = 'Car Share Pareto Demo'
        self.data_raw = None
        self.chart_main = None
        self._id = _ID

        super().__init__(app=app)

    def generate_data(self) -> None:
        """Format the car share data from plotly express for the Pareto. Called by parent class."""
        self.data_raw = (
            px.data.carshare()
            .rename(columns={'peak_hour': 'category', 'car_hours': 'value'})
        )
        self.data_raw['category'] = [f'H:{cat:02}' for cat in self.data_raw['category']]

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = ParetoChart(title='Car Share Pareto', xlabel='Peak Hours', ylabel='Car Hours')

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div([
            html.Div([
                min_graph(
                    id=self._il[self._id.chart],
                    figure=self.chart_main.create_figure(df_raw=self.data_raw),
                ),
            ]),
        ])

    def create_callbacks(self) -> None:
        """Register the callbacks."""
        pass  # Override base class. Not necessary for this example


if __name__ == '__main__':
    app = ParetoDemo()
    app.create()
    app.run(debug=True)
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
