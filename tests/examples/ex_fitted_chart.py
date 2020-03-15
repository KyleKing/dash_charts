"""Example Scatter Data with Fitted Line."""

import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash_charts import equations
from dash_charts.dash_helpers import parse_cli_port
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
        """Create self.df_demo with sample data."""
        # Create dataframe based on px sample dataset
        iris = px.data.iris()
        # count = len(iris['petal_width'])
        self.data_raw = pd.DataFrame(data={
            'name': iris['species'],
            'x': iris['petal_width'],
            'y': iris['petal_length'],
            'label': None,
        })

        # colors = [
        #     '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#7f7f7f', '#17becf', None,
        # ]
        # indices = [20 + int(idx * count / len(colors)) for idx in range(len(colors))]
        # self.annotations = [
        #     (self.data_raw['x'][indices[idx]], self.data_raw['y'][indices[idx]], 'Additional Information', color)
        #     for idx, color in enumerate(colors)
        # ]

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

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
                    figure=self.chart_main.create_figure(
                        df_raw=self.data_raw,
                        # annotations=self.annotations,  # FIXME: Implement annotations
                    ),
                )]),
            ],
        )

    def create_callbacks(self):
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


instance = FittedDemo
if __name__ == '__main__':
    port = parse_cli_port()
    app = instance()
    app.create()
    app.run(port=port, debug=True)
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
