"""Alignment chart."""
import math

import numpy as np
import plotly.graph_objects as go

from . import helpers


class AlignChart(helpers.MarginalChart):
    """Alignment/Distortion/Positioning Error Chart.

    Example Use: analyze inspection data for trends in misalignment, such as in molded parts

    """

    def __init__(self, title='', xLbl='', yLbl='', customLayoutParams=(), measLbl='Meas', idealLbl='Ideal', pad=0):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        xLbl/yLbl -- optional, X and Y Axis axis titles. Defaults to blank
        customLayoutParams -- Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'
        measLbl/idealLbl -- optional, legend names for the respective values
        pad -- optional, internal padding within the chart. Defaults to 0

        """
        super().__init__(title, xLbl, yLbl, customLayoutParams)
        # Store the additional kwargs as data members
        self.measLbl = measLbl
        self.idealLbl = idealLbl
        self.pad = pad

    def listifyData(self, df, stretch):
        """Convert the dataframe into a list for plotting.

        df -- Pandas dataframe with columns names: ['x', 'y', 'xDelta', 'yDelta', 'label']
        stretch -- optional, float value to change the spacing between ideal and measured coordinates

        """
        measLabels = []
        data = {
            'x': {self.idealLbl: [], self.measLbl: []},
            'y': {self.idealLbl: [], self.measLbl: []},
        }
        for row in df.itertuples():
            measLabels.append(row.label)
            data['x'][self.idealLbl].append(row.x)
            data['y'][self.idealLbl].append(row.y)
            data['x'][self.measLbl].append(row.x + stretch * row.xDelta)
            data['y'][self.measLbl].append(row.y + stretch * row.yDelta)

        # Calculate the chart range
        self.range = {}
        for axis in ['x', 'y']:
            vals = data[axis][self.idealLbl] + data[axis][self.measLbl]
            self.range[axis] = math.floor(min(vals) - self.pad), math.ceil(max(vals) + self.pad)
        return (measLabels, data)

    def createTraces(self, df, stretch=1):
        """Return traces for plotly chart.

        df -- Pandas dataframe with columns names: ['x', 'y', 'xDelta', 'yDelta', 'label']
        stretch -- optional, float value to change the spacing between ideal and measured coordinates

        ```py
        # Example dataframe
        df = pd.DataFrame(data={
            'x': [1, 2, 1, 2],
            'y': [1, 2, 2, 1],
            'xDelta': [0.01, 0.02, 0.005, -0.04],
            'yDelta': [0.01, -0.05, 0.005, 0.005],
            'label': ['A', 'B', 'C', 'D'],
        })
        ```

        """
        # FIXME: Handle multiple data sets/missing points? - use greyscale for ideal?

        measLabels, data = self.listifyData(df, stretch)
        # Plot the ideal and measured scatter points
        chartData = [
            go.Scatter(
                legendgroup='Points',
                mode='markers',
                name=lbl,
                opacity=1 if lbl == self.measLbl else 0.2,
                text=measLabels if lbl == self.measLbl else lbl,
                x=data['x'][lbl],
                y=data['y'][lbl],
            ) for lbl in [self.idealLbl, self.measLbl]
        ]
        # Plot a semi-transparent connecting line between related points
        chartData.extend([
            go.Scatter(
                line={'color': '#D93D40', 'dash': 'solid'},
                mode='lines',
                opacity=0.15,
                showlegend=False,
                x=[data['x'][self.idealLbl][idx], data['x'][self.measLbl][idx]],
                y=[data['y'][self.idealLbl][idx], data['y'][self.measLbl][idx]],
            ) for idx in range(len(measLabels))
        ])
        return chartData

    def createMargTop(self, df, stretch=1):
        """Return traces for the top marginal chart.

        df -- Pandas dataframe with columns names: ['x', 'y', 'xDelta', 'yDelta', 'label']
        stretch -- optional, float value to change the spacing between ideal and measured coordinates

        """
        return [
            go.Box(
                marker_color='royalblue',
                name=xVal,
                showlegend=False,
                x=df['x'][df['x'] == xVal] + df['xDelta'][df['x'] == xVal] * stretch
            )
            for xVal in np.sort(df['x'].unique())
        ]

    def createMargRight(self, df, stretch=1):
        """Return traces for the right marginal chart.

        df -- Pandas dataframe with columns names: ['x', 'y', 'xDelta', 'yDelta', 'label']
        stretch -- optional, float value to change the spacing between ideal and measured coordinates

        """
        df['yNew'] = df['y'] + df['yDelta'] * stretch
        return [
            go.Box(
                marker_color='royalblue',
                name=yVal,
                showlegend=False,
                x=[idx] * len(df['y'] == yVal),
                y=df['yNew'][df['y'] == yVal],
            )
            for idx, yVal in enumerate(np.sort(df['y'].unique()))
        ]

    def createLayout(self):
        """Override the default layout and add additional settings."""
        layout = super().createLayout()
        for axis in ['yaxis', 'xaxis']:
            layout[axis]['zeroline'] = False
        layout['yaxis']['scaleanchor'] = 'x'
        layout['yaxis']['scaleratio'] = 1
        layout['legend'] = {}  # Reset legend to default position on top right
        return layout
