"""Coordinate chart."""

import calendar
import cmath
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import custom_colorscales
from .utils_fig import CustomChart



class CoordinateChart(CustomChart):
    """Coordinate Chart.

    Example Use: visualizing a discrete dataset

    """

    def __init__(self, title='', xlabel='', ylabel='', custom_layout_params=(), grid_dims=None, coord=None, titles=None):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        xlabel/ylabel -- optional, X and Y Axis axis titles. Defaults to blank
        layout_overrides -- Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'
        grid_dims -- tuple of two values with the rectangular grid size
        coord -- lists of the x/y coordinates from the top left corner of a single grid rectangle

        """
        super().__init__(title, xlabel, ylabel, layout_overrides)
        # Calculate each point in the grid
        self.width = float(np.max(coord['x']) + np.min(coord['x']))
        self.height = float(np.max(coord['y']) + np.min(coord['y']))
        self.grid = {'x': [], 'y': []}
        for r_idx in range(grid_dims[0]):
            y_offset = self.height * (grid_dims[0] - r_idx)
            y_grid = [y_offset - _y for _y in coord['y']]
            for c_idx in range(grid_dims[1]):
                x_offset = self.width * c_idx
                self.grid['x'].extend([x_offset + _x for _x in coord['x']])
                self.grid['y'].extend(y_grid)
        # Store points used to create the grid borders
        self.borders = [{
            'x': [c_idx * self.width] * 2,
            'y': [0, self.height * grid_dims[0]],
        } for c_idx in range(grid_dims[1] + 1)] + [{
            'x': [0, self.width * grid_dims[1]],
            'y': [r_idx * self.height] * 2,
        } for r_idx in range(grid_dims[0] + 1)]
        # Create annotations
        v_offset = np.min(coord['y']) * 0.4
        self.annotations = [
            go.layout.Annotation(
                ax=0, ay=0,
                x=(idx % grid_dims[1] + 0.5) * self.width,
                y=(grid_dims[0] - int(idx / grid_dims[1]) % grid_dims[0]) * self.height - v_offset,
                text=title,
            )
            for idx, title in enumerate(titles) if title is not None
        ] if titles is not None else []

    def create_traces(self, df_raw, border_opacity=0.2, border_line=None, marker_kwargs=None):
        """Return traces for plotly chart.

        df_raw -- Pandas dataframe with columns names: ['values']
        border_opacity - border opacity in [0-1] where 0 is none
        border_line -- dictionary passed to plotly `line`. Used to set thickness, color, dash style, etc.
        marker_kwargs -- optional keyword arguments to pass to scatter_marker()

        """
        # Ensure that the provides values are the same length as the total number of grid points
        vals = list(df_raw['values'])
        vals.extend([None] * (len(self.grid['x']) - len(vals)))
        # Remove 'None' values from grid
        df = pd.DataFrame(data={
            'values': vals,
            'x': self.grid['x'],
            'y': self.grid['y'],
        }).dropna()

        chart_data = [
            go.Scatter(
                hoverinfo='none',
                line={'color': 'black'} if border_line is None else border_line,
                mode='lines',
                opacity=border_opacity,
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
                marker=self.scatter_marker(df, **({} if marker_kwargs is None else marker_kwargs)),
            ),
        ]
        return chart_data

    def scatter_marker(self, df, colorscale='Viridis', size=16, symbol='circle'):
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

    def create_layout(self):
        """Override the default layout and add additional settings."""
        layout = super().create_layout()
        layout['annotations'] = self.annotations
        for axis in ['xaxis', 'yaxis']:
            layout[axis]['showgrid'] = False
            layout[axis]['showticklabels'] = False
            layout[axis]['zeroline'] = False
        layout['yaxis']['scaleanchor'] = 'x'
        layout['yaxis']['scaleratio'] = 1
        return layout


# ==============================================================================
# Standard Coordinate Grids


class CircleGrid:
    """Grid of circular coordinates."""

    marker_kwargs = {'size': 10}

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

    marker_kwargs = {'size': 10, 'symbol': 'square'}

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

    def format_data(self, month_lists, year):
        """Return the formatted list that can be passed to a coordinate chart.

        month_lists -- list of lists where each sub-list is a month and contains the daily value
        year -- year expressed in 4 decimal places (i.e. 2019)

        """
        vals = []
        for idx, month_list in enumerate(month_lists):
            idx_first_day, countDays = calendar.monthrange(year, idx + 1)
            idx_first_day += 1  # Increment to start on Sunday
            vals.extend([None] * idx_first_day)
            vals.extend(month_list)
            vals.extend([None] * (len(self.coord['x']) - idx_first_day - countDays))
        return vals


class MonthGrid:
    """Coordinates of days within a single month."""

    marker_kwargs = {'size': 35, 'symbol': 'square'}

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

    def format_data(self, month_list, year, month):
        """Return the formatted list that can be passed to a coordinate chart.

        month_list -- list of daily values
        year -- year expressed in 4 decimal places (i.e. 2019)
        month -- month in 1-12

        """
        idx_first_day = calendar.monthrange(year, month)[0]
        vals = [None] * idx_first_day
        vals.extend(month_list)
        return vals
