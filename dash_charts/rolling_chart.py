"""Rolling Mean and Filled Standard Deviation Chart."""

import bottleneck
import numpy as np
import plotly.graph_objects as go

from . import helpers


class RollingChart(helpers.CustomChart):
    """Rolling Mean and Filled Standard Deviation Chart.

    Example Use: Timeseries data

    """

    def __init__(self, title='', xLbl='', yLbl='', customLayoutParams=()):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        xLbl/yLbl -- optional, X and Y Axis axis titles. Defaults to blank
        customLayoutParams -- Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'

        """
        super().__init__(title, xLbl, yLbl, customLayoutParams)

    def createTraces(self, df, dataLbl='Data', rollingCount=5, stdCount=2):
        """Return traces for plotly chart.

        df -- Pandas dataframe with columns names: ['x', 'y', 'label']
        dataLbl --
        rollingCount -- count of items to use for rolling calculations. Default 5
        stdCount -- count of STD deviations to display. Default 2

        """
        chartData = [
            go.Scatter(
                mode='markers',
                name=dataLbl,
                opacity=0.5,
                text=df['label'],
                x=df['x'],
                y=df['y'],
            ),
        ]
        # Only add the rolling calculations if there are a sufficient number of points
        if len(df['x']) >= rollingCount:
            rollingMean = bottleneck.move_mean(df['y'], rollingCount)
            rollingSTD = bottleneck.move_std(df['y'], rollingCount)
            chartData.extend([
                go.Scatter(
                    fill='toself',
                    hoverinfo='skip',
                    name='{}x STD Range'.format(stdCount),
                    opacity=0.5,
                    x=list(df['x']) + list(df['x'])[::-1],
                    y=list(np.add(rollingMean, np.multiply(stdCount, rollingSTD))) + list(
                        np.subtract(rollingMean, np.multiply(stdCount, rollingSTD)))[::-1],
                ),
                go.Scatter(
                    hoverinfo='skip',
                    mode='lines',
                    name='Rolling Mean',
                    opacity=0.9,
                    x=df['x'],
                    y=rollingMean,
                ),
            ])

        return chartData
