"""Pareto Chart."""

import pandas as pd
import plotly.graph_objects as go

from . import helpers


class ParetoChart(helpers.CustomChart):
    """Pareto Chart.

    Example Use: Tracking ticket occurrences in a ticketing system or associated downtime

    """

    def __init__(self, title='', x_label='', y_label='', cust_layout_params=(), colors=('#4682b4', '#b44646'), limitCat=20):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        x_label/y_label -- optional, X and Y Axis axis titles. Defaults to blank
        cust_layout_params -- Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'
        colors -- optional color scheme. 1st value is for the bar color. 2nd is for cum percentage
        limitCat -- set the maximum number of categories. Defaults to 20

        """
        super().__init__(title, x_label, y_label, cust_layout_params)
        self.colors = colors
        self.limitCat = limitCat

    def create_traces(self, df, showCount=True):
        """Return traces for plotly chart.

        df -- Pandas dataframe with keys (categories, percent)

        """
        # Verify data format
        expecK = ['value', 'categories']
        foundK = df.keys()
        assert all([_k in foundK for _k in expecK]), 'df must have keys {}'.format(expecK)
        # Compress dataframe to only the unique values
        dfP = None
        for cat in df['categories'].unique():
            data = {'value': [df.loc[df['categories'] == cat]['value'].sum()], 'label': [cat]}
            if showCount:
                data['counts'] = df['categories'].value_counts()[cat]
            dfRow = pd.DataFrame(data=data)
            dfP = dfRow if dfP is None else dfP.append(dfRow)
        # Sort and calculate percentage
        dfP = dfP.sort_values(by=['value'], ascending=False).head(self.limitCat)
        dfP = dfP[dfP['value'] != 0]
        dfP['cumPer'] = dfP['value'].divide(dfP['value'].sum()).cumsum()
        # Add auto-generated count to each bar
        textKwargs = {'text': dfP['counts'], 'textposition': 'auto'} if showCount else {}

        chartData = [
            go.Bar(
                hoverinfo='y',
                marker={'color': self.colors[0]},
                name='Raw Value',
                x=dfP['label'],
                y=dfP['value'],
                yaxis='y1',
                **textKwargs,
            ),
        ] + [
            go.Scatter(
                hoverinfo='y',
                line={'color': self.colors[1]},
                mode='lines',
                name='Cumulative Percentage',
                x=dfP['label'],
                y=dfP['cumPer'],
                yaxis='y2',
            ),
        ]
        return chartData

    def create_layout(self):
        """Override the default layout and add additional settings."""
        layout = super().create_layout()
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
