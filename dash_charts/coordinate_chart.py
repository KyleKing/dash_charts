"""Coordinate chart."""

import calendar
import cmath
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import custom_colorscales, helpers


class CoordinateChart(helpers.CustomChart):
    """Coordinate Chart.

    Example Use: visualizing a discrete dataset

    """

    def __init__(self, title='', xLbl='', yLbl='', customLayoutParams=(), gridDims=None, coord=None, titles=None):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        xLbl/yLbl -- optional, X and Y Axis axis titles. Defaults to blank
        customLayoutParams -- Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'
        gridDims -- tuple of two values with the rectangular grid size
        coord -- lists of the x/y coordinates from the top left corner of a single grid rectangle

        """
        super().__init__(title, xLbl, yLbl, customLayoutParams)
        # Calculate each point in the grid
        self.width = float(np.max(coord['x']) + np.min(coord['x']))
        self.height = float(np.max(coord['y']) + np.min(coord['y']))
        self.grid = {'x': [], 'y': []}
        for rIdx in range(gridDims[0]):
            yOffset = self.height * (gridDims[0] - rIdx)
            yGrid = [yOffset - _y for _y in coord['y']]
            for cIdx in range(gridDims[1]):
                xOffset = self.width * cIdx
                self.grid['x'].extend([xOffset + _x for _x in coord['x']])
                self.grid['y'].extend(yGrid)
        # Store points used to create the grid borders
        self.borders = [{
            'x': [cIdx * self.width] * 2,
            'y': [0, self.height * gridDims[0]],
        } for cIdx in range(gridDims[1] + 1)] + [{
            'x': [0, self.width * gridDims[1]],
            'y': [rIdx * self.height] * 2,
        } for rIdx in range(gridDims[0] + 1)]
        # Create annotations
        vOffset = np.min(coord['y']) * 0.4
        self.annotations = [
            go.layout.Annotation(
                ax=0, ay=0,
                x=(idx % gridDims[1] + 0.5) * self.width,
                y=(gridDims[0] - int(idx / gridDims[1]) % gridDims[0]) * self.height - vOffset,
                text=title,
            )
            for idx, title in enumerate(titles) if title is not None
        ] if titles is not None else []

    def createTraces(self, dfRaw, borderOp=0.2, borderLine={'color': 'black'}, markerKwargs={}):
        """Return traces for plotly chart.

        dfRaw -- Pandas dataframe with columns names: ['values']
        borderOp - border opacity in [0-1] where 0 is none
        borderLine -- dictionary passed to plotly `line`. Used to set thickness, color, dash style, etc.
        markerKwargs -- optional keyword arguments to pass to scatterMarker()

        """
        # Ensure that the provides values are the same length as the total number of grid points
        vals = list(dfRaw['values'])
        vals.extend([None] * (len(self.grid['x']) - len(vals)))
        # Remove 'None' values from grid
        df = pd.DataFrame(data={
            'values': vals,
            'x': self.grid['x'],
            'y': self.grid['y'],
        }).dropna()

        chartData = [
            go.Scatter(
                hoverinfo='none',
                line=borderLine,
                mode='lines',
                opacity=borderOp,
                showlegend=False,
                x=border['x'],
                y=border['y'],
            ) for border in self.borders
        ] + [
            go.Scatter(
                hoverinfo='text',
                mode='markers',
                showlegend=False,
                text=df['values'],
                x=df['x'],
                y=df['y'],
                marker=self.scatterMarker(df, **markerKwargs),
            ),
        ]
        return chartData

    def scatterMarker(self, df, colorscale='Viridis', size=16, symbol='circle'):
        """Return a dictionary for the scatter plot.

        df -- Pandas dataframe
        colorscale -- list of values or plotly colorscale name (Reds, Bluered, Jet, Viridis, Cividis, etc.)
        size -- marker size
        symbol -- marker symbol (square, circle, circle-open, x, etc.)

        See: https://plot.ly/python/colorscales/

        """
        marker = {
            'color': df['values'],
            'colorscale': colorscale,
            'showscale': True,
            'size': size,
            'symbol': symbol,
        }
        if type(colorscale) is list:
            marker['colorbar'] = custom_colorscales.makecolorbar(colorscale)
        return marker

    def createLayout(self):
        """Override the default layout and add additional settings."""
        layout = super().createLayout()
        layout['annotations'] = self.annotations
        for axis in ['xaxis', 'yaxis']:
            layout[axis]['showgrid'] = False
            layout[axis]['showticklabels'] = False
            layout[axis]['zeroline'] = False
        layout['yaxis']['scaleanchor'] = 'x'
        layout['yaxis']['scaleratio'] = 1
        return layout


# Standard Coordinate Grids


class CircleGrid:
    """Grid of circular coordinates."""

    markerKwargs = {'size': 10}

    def __init__(self, dims=(4, 5), titles=None):
        """Initialize the coordinates.

        dims -- tuple of iterations in the x/y axis respectively
        titles -- list of titles to place in each grid element

        """
        self.dims = dims
        self.titles = titles if titles is not None else [
            'Subtitle for ({}, {})'.format(
                int(idx / dims[1]) + 1,
                idx % (dims[0] + 1) + 1,
            )
            for idx in range(dims[0] * dims[1])
        ]
        opp = 0.5 * math.cos(cmath.pi / 4)
        adj = 0.5 * math.sin(cmath.pi / 4)
        self.coord = {
            'x': [0.5, 1 - adj, 1.0, 1 + adj, 1.5, 1 + adj, 1.0, 1 - adj],
            'y': [1.0, 1 - opp, 0.5, 1 - opp, 1.0, 1 + opp, 1.5, 1 + opp],
        }


class YearGrid:
    """Coordinates of days within a grid of months over one year."""

    markerKwargs = {'size': 10, 'symbol': 'square'}

    def __init__(self, dims=(4, 3), titles=None):
        """Initialize the coordinates.

        dims -- tuple of iterations in the x/y axis respectively
        titles -- list of titles to place in each grid element

        """
        self.dims = dims
        assert dims[0] * dims[1] == 12, 'Calendar must show all 12 months Expected (12,1), (6,2), (4,3), (1,12), etc.'
        self.titles = titles if titles is not None else calendar.month_name[1:]
        margin = 2
        self.coord = {
            'x': np.add(list(range(7)) * 6, margin),
            'y': np.add([0] * 7 + [1] * 7 + [2] * 7 + [3] * 7 + [4] * 7 + [5] * 7, margin),
        }

    def formatData(self, monthLists, year):
        """Return the formatted list that can be passed to a coordinate chart.

        monthLists -- list of lists where each sub-list is a month and contains the daily value
        year -- year expressed in 4 decimal places (i.e. 2019)

        """
        vals = []
        for idx, monthList in enumerate(monthLists):
            idxFirstDay, countDays = calendar.monthrange(year, idx + 1)
            idxFirstDay += 1  # Increment to start on Sunday
            vals.extend([None] * idxFirstDay)
            vals.extend(monthList)
            vals.extend([None] * (len(self.coord['x']) - idxFirstDay - countDays))
        return vals


class MonthGrid:
    """Coordinates of days within a single month."""

    markerKwargs = {'size': 35, 'symbol': 'square'}

    def __init__(self, dims=(1, 1), titles=None):
        """Initialize the coordinates.

        dims -- tuple of iterations in the x/y axis respectively
        titles -- list of titles to place in each grid element

        """
        self.dims = dims
        assert dims == (1, 1), 'Day grid can only show one month, expected (1, 1)'
        self.titles = titles
        margin = 1.25
        self.coord = {
            'x': np.add(list(range(7)) * 6, margin),
            'y': np.add([0] * 7 + [1] * 7 + [2] * 7 + [3] * 7 + [4] * 7 + [5] * 7, margin),
        }

    def formatData(self, monthList, year, month):
        """Return the formatted list that can be passed to a coordinate chart.

        monthList -- list of daily values
        year -- year expressed in 4 decimal places (i.e. 2019)
        month -- month in 1-12

        """
        idxFirstDay = calendar.monthrange(year, month)[0]
        vals = [None] * idxFirstDay
        vals.extend(monthList)
        return vals
