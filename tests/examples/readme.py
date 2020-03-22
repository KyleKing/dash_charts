import dash_html_components as html
import plotly.express as px
from dash_charts.pareto_chart import ParetoChart
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import min_graph


class ParetoDemo(AppBase):
    """Example creating a simple Pareto chart."""

    name = 'Car Share Pareto Demo'
    """Application name"""

    data_raw = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    chart_main = None
    """Main chart (Pareto)."""

    id_chart = 'pareto'
    """Unique name for the main chart."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and application data."""
        super().initialization()
        self.register_uniq_ids([self.id_chart])
        # Format the car share data from plotly express for the Pareto
        self.data_raw = (px.data.carshare()
                         .rename(columns={'peak_hour': 'category', 'car_hours': 'value'}))
        self.data_raw['category'] = [f'H:{cat:02}' for cat in self.data_raw['category']]

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = ParetoChart(title='Car Share Pareto', xlabel='Peak Hours', ylabel='Car Hours')

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div([
            html.Div([min_graph(
                id=self.ids[self.id_chart],
                figure=self.chart_main.create_figure(df_raw=self.data_raw),
            )]),
        ])

    def create_callbacks(self):
        """Register the callbacks."""
        pass  # Override base class. Not necessary for this example


if __name__ == '__main__':
    app = ParetoDemo()
    app.create()
    app.run(debug=True)
