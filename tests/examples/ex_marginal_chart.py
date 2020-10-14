"""Example Marginal-Chart."""

import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import MarginalChart, check_raw_data, min_graph
from dash_charts.utils_helpers import parse_dash_cli_args


class SampleMarginalChart(MarginalChart):
    """Sample implementing a custom MarginalChart."""

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns `name: str`, `x: float`, `y: float` and `label: str`

        Returns:
            list: Dash chart traces

        """
        check_raw_data(df_raw, min_keys=['name', 'x', 'y', 'label'])

        return [
            go.Scatter(
                mode='markers',
                # name=df_raw['name'],
                text=df_raw['label'],
                x=df_raw['x'],
                y=df_raw['y'],
            ),
        ]

    def create_marg_top(self, df_raw):
        """Return traces for the top marginal chart.

        Args:
            df_raw: same pandas dataframe as self.create_traces()

        """
        return [
            go.Bar(
                marker_color='royalblue',
                # name='TODO,
                showlegend=False,
                x=df_raw['x'],
                y=df_raw['y'],
            ),
        ]

    def create_marg_right(self, df_raw):
        """Return traces for the top marginal chart.

        Args:
            df_raw: same pandas dataframe as self.create_traces()

        """
        key = 'name'
        return [
            go.Violin(
                marker_color='royalblue',
                name=str(name),
                showlegend=False,
                x=df_raw[key][df_raw[key] == name],
                y=df_raw['y'][df_raw[key] == name],
            )
            for idx, name in enumerate(np.sort(df_raw[key].unique()))
        ]

    def create_layout(self):
        """Extend the standard layout.

        Returns:
            dict: layout for Dash figure

        """
        layout = super().create_layout()
        layout['legend'] = {}  # Reset legend to default position on top right
        layout['showlegend'] = False
        return layout


class SampleMarginalChartDemo(AppBase):
    """Example creating a Marginal chart."""

    name = 'Example Marginal Chart'
    """Application name"""

    data_raw = None
    """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

    chart_main = None
    """Main chart (Marginal)."""

    id_chart = 'marginal'
    """Unique name for the main chart."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart])

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = SampleMarginalChart(
            title='Sample User-Implemented Marginal Chart with Iris dataset',
            xlabel='Petal Width',
            ylabel='Petal Length',
        )

    def generate_data(self):
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
                    figure=self.chart_main.create_figure(
                        df_raw=self.data_raw,
                    ),
                )]),
            ],
        )

    def create_callbacks(self):
        """Create Dash callbacks."""
        pass  # No callbacks necessary for this simple example


instance = SampleMarginalChartDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
