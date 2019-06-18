"""Pareto Chart."""

import plotly.graph_objs as go

from . import helpers


class ParetoChart(helpers.CustomChart):
    """Pareto Chart.

    Example Use: Ticketing System

    """

    def __init__(self, title='', xLbl='', yLbl='', colors=('#62A4D1', '#C5676B')):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        xLbl/yLbl -- optional, X and Y Axis axis titles. Defaults to blank
        colors -- optional color scheme. 1st value is for the bar color. 2nd is for cum percentage

        """
        super().__init__(title, xLbl, yLbl)
        self.colors = colors

    def formatData(self, df):
        """Format and return the data for the chart.

        df -- Pandas dataframe with keys (value, percent)

        """
        # TODO: Add additional arguments for modification

        # Verify data format
        expecK = ['value', 'label']
        foundK = df.keys()
        assert all([_k in foundK for _k in expecK]), 'df must have keys {}'.format(expecK)

        # Sort and calculate percentage
        df = df.sort_values(by=['value'], ascending=False)
        df['cumPer'] = df['value'].divide(df['value'].sum()).cumsum().fillna(1)

        chartData = [
            go.Bar(
                marker={'color': self.colors[0]},
                name='Raw Value',
                x=df['label'],
                y=df['value'],
            ),
        ] + [
            go.Scatter(
                line={'color': self.colors[1], 'dash': 'solid'},
                mode='lines',
                name='Cumulative Percentage',
                x=df['label'],
                y=df['cumPer'],
                yaxis='y2',
            ),
        ]
        return chartData

    def createLayout(self):
        """Override the default layout and add additional settings."""
        layout = super().createLayout()
        layout['legend'] = {}
        layout['showlegend'] = False

        # See multiple axis: https://plot.ly/python/multiple-axes/
        layout['yaxis2'] = {
            'overlaying': 'y',
            'range': [0, 1],
            'side': 'right',
            'tickfont': {'color': self.colors[1]},
            'tickformat': '%',
            'title': 'Cumulative Percentage',
            'titlefont': {'color': self.colors[1]},
        }
        return layout
