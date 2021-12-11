"""Example Scatter Data with Fitted Line."""

import dash_html_components as html
import pandas as pd
import plotly.express as px
from implements import implements

from dash_charts import equations
from dash_charts.scatter_line_charts import FittedChart
from dash_charts.utils_app import AppBase, AppInterface
from dash_charts.utils_fig import min_graph
from dash_charts.utils_helpers import parse_dash_cli_args


@implements(AppInterface)  # noqa: H601
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

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart])

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = FittedChart(
            title='Sample Fitted Scatter Data',
            xlabel='Index',
            ylabel='Measured Value',
        )
        # Set fit equations
        self.chart_main.fit_eqs = [('quadratic', equations.quadratic)]

    def generate_data(self) -> None:
        """Create self.data_raw with sample data."""
        # Create dataframe based on px sample dataset
        iris = px.data.iris()
        self.data_raw = pd.DataFrame(
            data={
                'name': iris['species'],
                'x': iris['petal_width'],
                'y': iris['petal_length'],
                'label': None,
            },
        )
        # Alternatively, use `[random.expovariate(0.2) for _i in range(count)]`

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


instance = FittedDemo
app = instance()
app.create()
if __name__ == '__main__':
    app.run(**parse_dash_cli_args())
else:
    FLASK_HANDLE = app.get_server()
