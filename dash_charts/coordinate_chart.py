"""Coordinate chart."""

import calendar
import cmath
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import custom_colorscales
from .utils_fig import CustomChart

# TODO: subplots for multiple years of calendar charts (Subplot title is year)


class CoordinateChart(CustomChart):
    """Coordinate Chart."""

    border_opacity = 0.2
    """Border opacity for grid. Value must be in [0-1] where 0 is none. Default is 0.2."""

    border_line = None
    """Dictionary passed to plotly `line`. Used to set thickness, color, dash style, etc. Default is None."""

    marker_kwargs = None
    """optional keyword arguments to pass to `scatter_marker()`. Default is None."""

    # _pareto_colors: dict = {'bar': '#4682b4', 'line': '#b44646'}
    #
    # @property
    # def pareto_colors(self):
    #     """Colors for bar and line traces in Pareto chart.
    #
    #     Returns:
    #         dict: dictionary with keys `(bar, line)`
    #
    #     """
    #     return self._pareto_colors
    #
    # @pareto_colors.setter
    # def pareto_colors(self, pareto_colors):
    #     expected_keys = sorted(['bar', 'line'])
    #     if sorted(pareto_colors.keys()) != expected_keys:
    #         raise RuntimeError(f'Expected {pareto_colors} to have keys: {expected_keys}')
    #     self._pareto_colors = pareto_colors

    def __init__(self, title='', layout_overrides=(), grid_dims=None, coord=None, titles=None):
        """Initialize chart parameters.

        Args:
            title: optional, string title for chart. Defaults to blank
            xlabel/ylabel: optional, X and Y Axis axis titles. Defaults to blank
            layout_overrides: Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'
            grid_dims: tuple of two values with the rectangular grid size
            coord: lists of the x/y coordinates from the top left corner of a single grid rectangle

        """
        super().__init__(title=title, xlabel='', ylabel='', layout_overrides=layout_overrides)
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
                x=(idx % grid_dims[1] + 0.5) * self.width,  # noqa: S001
                y=(grid_dims[0] - int(idx / grid_dims[1]) % grid_dims[0]) * self.height - v_offset,
                text=title,
            )
            for idx, title in enumerate(titles) if title is not None
        ] if titles is not None else []

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with at minimum the column `values: str`

        Returns:
            list: Dash chart traces

        Raises:
            RuntimeError: if the `df_raw` is missing any necessary columns

        """
        # Ensure that the provides values are the same length as the total number of grid points
        values = list(df_raw['values'])
        values.extend([None] * (len(self.grid['x']) - len(values)))
        # Remove 'None' values from grid
        df_grid = pd.DataFrame(data={
            'values': values,
            'x': self.grid['x'],
            'y': self.grid['y'],
        }).dropna()

        return [
            go.Scatter(
                hoverinfo='none',
                line={'color': 'black'} if self.border_line is None else self.border_line,
                mode='lines',
                opacity=self.border_opacity,
                showlegend=False,
                x=border['x'],
                y=border['y'],
            ) for border in self.borders
        ] + [
            go.Scatter(
                hoverinfo='text',
                mode='markers',
                showlegend=False,
                text=df_grid['values'],
                x=df_grid['x'],
                y=df_grid['y'],
                marker=self.scatter_marker(df_grid, **({} if self.marker_kwargs is None else self.marker_kwargs)),
            ),
        ]

    def scatter_marker(self, df, colorscale='Viridis', size=16, symbol='circle'):
        """Return a dictionary for the scatter plot.

        See: https://plot.ly/python/colorscales/

        Args:
            df: Pandas dataframe
            colorscale: list of values or plotly colorscale name (Reds, Bluered, Jet, Viridis, Cividis, etc.)
            size: marker size
            symbol: marker symbol (square, circle, circle-open, x, etc.)

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

        Args:
            dims: tuple of iterations in the x/y axis respectively
            titles: list of titles to place in each grid element

        """
        self.dims = dims
        if titles is None:
            self.titles = []
            for idx in range(dims[0] * dims[1]):
                x_coord = int(idx / dims[1]) + 1
                y_coord = idx % (dims[0] + 1) + 1  # noqa: S001
                self.titles.append(f'Subtitle for ({x_coord}, {y_coord})')
        else:
            self.titles = titles

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

        Args:
            dims: tuple of iterations in the x/y axis respectively
            titles: list of titles to place in each grid element

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

        Args:
            month_lists: list of lists where each sub-list is a month and contains the daily value
            year: year expressed in 4 decimal places (i.e. 2019)

        """
        values = []
        for idx, month_list in enumerate(month_lists):
            idx_first_day, count_days = calendar.monthrange(year, idx + 1)
            idx_first_day += 1  # Increment to start on Sunday
            values.extend([None] * idx_first_day)
            values.extend(month_list)
            values.extend([None] * (len(self.coord['x']) - idx_first_day - count_days))
        return values


class MonthGrid:
    """Coordinates of days within a single month."""

    marker_kwargs = {'size': 35, 'symbol': 'square'}

    def __init__(self, dims=(1, 1), titles=None):
        """Initialize the coordinates.

        Args:
            dims: tuple of iterations in the x/y axis respectively
            titles: list of titles to place in each grid element

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

        Args:
            month_list: list of daily values
            year: year expressed in 4 decimal places (i.e. 2019)
            month: month in 1-12

        """
        idx_first_day = calendar.monthrange(year, month)[0]
        values = [None] * idx_first_day
        values.extend(month_list)
        return values
