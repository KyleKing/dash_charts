"""Alignment chart."""

import math

import plotly.graph_objs as go

from . import helpers


class AlignChart(helpers.CustomChart):
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

    def formatData(self, df, stretch=1):
        """Format and return the data for the chart.

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
        # TODO: Handle multiple data sets/missing points? - use greyscale for ideal?

        # Re-format the data into list format for plotting
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

    def createLayout(self):
        """Override the default layout and add additional settings."""
        layout = super().createLayout()
        for axis in ['yaxis', 'xaxis']:
            layout[axis]['zeroline'] = False
        layout['yaxis']['scaleanchor'] = 'x'
        layout['yaxis']['scaleratio'] = 1
        return layout
