"""Pareto Chart."""

import plotly.graph_objs as go

from . import helpers


class ParetoChart(helpers.CustomChart):
    """Pareto Chart.

    Example Use: Tracking ticket occurrences in a ticketing system or associated downtime

    """

    def __init__(self, title='', xLbl='', yLbl='', customLayoutParams=(), colors=('#4682b4', '#b44646'), limitCat=20):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        xLbl/yLbl -- optional, X and Y Axis axis titles. Defaults to blank
        customLayoutParams -- Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'
        colors -- optional color scheme. 1st value is for the bar color. 2nd is for cum percentage
        limitCat -- set the maximum number of categories. Defaults to 20

        """
        super().__init__(title, xLbl, yLbl, customLayoutParams)
        self.colors = colors
        self.limitCat = limitCat

    def formatData(self, df):
        """Format and return the data for the chart.

        df -- Pandas dataframe with keys (value, percent)

        """
        # Verify data format
        expecK = ['value', 'label']
        foundK = df.keys()
        assert all([_k in foundK for _k in expecK]), 'df must have keys {}'.format(expecK)

        # Sort and calculate percentage
        df = df.sort_values(by=['value'], ascending=False).head(self.limitCat)
        df = df[df['value'] != 0]
        df['cumPer'] = df['value'].divide(df['value'].sum()).cumsum()

        chartData = [
            go.Bar(
                hoverinfo='y',
                marker={'color': self.colors[0]},
                name='Raw Value',
                x=df['label'],
                y=df['value'],
                yaxis='y1',
            ),
        ] + [
            go.Scatter(
                hoverinfo='y',
                line={'color': self.colors[1]},
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

        # Update YAxis configuration
        layout['yaxis']['mirror'] = 'ticks'
        layout['yaxis']['showline'] = True
        layout['yaxis']['tickformat'] = '.1f'

        # See multiple axis: https://plot.ly/python/multiple-axes/
        layout['yaxis2'] = {
            'dtick': 0.1,
            'overlaying': 'y',
            'range': [0, 1.01],
            'showgrid': False,
            'side': 'right',
            'tickformat': '.0%',
            'tickmode': 'linear',
            'title': 'Cumulative Percentage',
        }

        return layout
