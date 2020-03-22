"""Example Scatter Data with Fitted Line."""

import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash_charts import equations
from dash_charts.dash_helpers import parse_dash_cli_args
from dash_charts.fitted_chart import FittedChart
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import min_graph


class FittedDemo(AppBase):
    """Example creating a Fitted chart."""

    name = 'Example Fitted Chart'
    """Application name"""

    data_raw = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    chart_main = None
    """Main chart (Fitted)."""

    id_chart = 'fitted'
    """Unique name for the main chart."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart])

        self._generate_data()

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = FittedChart(
            title='Sample Fitted Scatter Data',
            xlabel='Index',
            ylabel='Measured Value',
        )
        # Set fit equations
        self.chart_main.fit_eqs = [('quadratic', equations.quadratic)]

    def _generate_data(self):
        """Create self.data_raw with sample data."""
        # Create dataframe based on px sample dataset
        iris = px.data.iris()
        self.data_raw = pd.DataFrame(data={
            'name': iris['species'],
            'x': iris['petal_width'],
            'y': iris['petal_length'],
            'label': None,
        })

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


instance = FittedDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
