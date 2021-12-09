"""Coordinate chart.

Creates a grid of tiles with consistently spaced x/y positions. Provided data is plotted as a marker at each position
unless None. This can be used to create all sorts of visualizations that have spatially related data, such as calendars

"""

import calendar
import cmath
import math
from itertools import chain

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from .utils_fig import CustomChart, check_raw_data

# PLANNED: subplots for multiple years of calendar charts (Subplot title is year)


def calculate_grid(grid_dims, corners, width, height):
    """Calculate the grid x and y coordinates.

    Args:
        grid_dims: tuple of the number of tiles in grid. In format `(row, column)`
        corners: dictionary with keys `(x, y)` containing lists of the four exterior corner coordinates
        width: float width in pixels
        height: float height in pixels

    Returns:
        dict: with keys `(x, y)` with lists of lists containing float values

    """
    grid = {'x': [], 'y': []}
    for r_idx in range(grid_dims[0]):
        y_offset = height * (grid_dims[0] - r_idx)
        y_grid = [y_offset - _y for _y in corners['y']]
        for c_idx in range(grid_dims[1]):
            x_offset = width * c_idx
            grid['x'].extend([x_offset + _x for _x in corners['x']])
            grid['y'].extend(y_grid)
    return grid


def calculate_border(grid_dims, width, height):
    """Calculate each line in all borders.

    Args:
        grid_dims: tuple of the number of tiles in grid. In format `(row, column)`
        width: float width in pixels
        height: float height in pixels

    Returns:
        list: containing dictionaries keys `(x, y)` and values for the two points for each line in grid

    """
    return [
        {
            'x': [c_idx * width] * 2,
            'y': [0, height * grid_dims[0]],
        } for c_idx in range(grid_dims[1] + 1)
    ] + [
        {
            'x': [0, width * grid_dims[1]],
            'y': [r_idx * height] * 2,
        } for r_idx in range(grid_dims[0] + 1)
    ]


class CoordinateChart(CustomChart):  # noqa: H601
    """Coordinate Chart."""

    border_opacity: float = 0.2
    """Border opacity for grid. Value must be in [0-1] where 0 is none. Default is 0.2."""

    border_line = None
    """Dictionary passed to plotly `line`. Used to set thickness, color, dash style, etc. Default is None."""

    marker_kwargs = None
    """Marker keyword arguments used in `create_marker()`. Default is None."""

    # Private states for managing coordinate chart dimensions
    _grid: dict
    _borders: list

    def __init__(self, *, title, grid_dims, corners, titles=None, layout_overrides=()):
        """Initialize Coordinate Chart and store parameters as data members.

        Args:
            title: String title for chart (can be an empty string for blank)
            grid_dims: tuple of the number of tiles in grid. In format `(row, column)`
            corners: dictionary with keys `(x, y)` containing lists of the four corner coordinates
            titles: list of strings that will appear in each tile. Default is None for no titles
            layout_overrides: Custom parameters in format [ParentKey, SubKey, Value] to customize 'go.layout'

        """
        # Initialize base method. Sets xlabel and ylabel to empty strings because coordinate chart use the x/y
        #   axis for arranging points. Data is displayed by color or size
        super().__init__(title=title, xlabel='', ylabel='', layout_overrides=layout_overrides)

        # Initialize chart parameters
        self.calculate_layout(grid_dims, corners, titles)

    def calculate_layout(self, grid_dims, corners, titles):
        """Calculate coordinate chart layout. Called by __init__, but can be called later to update the chart.

        Args:
            grid_dims: tuple of the number of tiles in grid. In format `(row, column)`
            corners: dictionary with keys `(x, y)` containing lists of the four corner coordinates
            titles: list of strings that will appear in each tile. Default is None for no titles

        """
        # Calculate exterior height and width of grid
        width = float(np.max(corners['x']) + np.min(corners['x']))
        height = float(np.max(corners['y']) + np.min(corners['y']))

        # Set grid and border coordinates for traces
        self._grid = calculate_grid(grid_dims, corners, width, height)
        self._borders = calculate_border(grid_dims, width, height)

        # Add titles to annotations if provided
        if titles is None:
            self.annotations = []
        else:
            v_offset = np.min(corners['y']) * 0.4
            self.annotations = [
                go.layout.Annotation(
                    ax=0, ay=0,
                    x=(idx % grid_dims[1] + 0.5) * width,  # noqa: S001
                    y=(grid_dims[0] - int(idx / grid_dims[1]) % grid_dims[0]) * height - v_offset,
                    text=title,
                )
                for idx, title in enumerate(titles) if title is not None
            ]

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with at minimum the column `values: str`

        Returns:
            list: Dash chart traces

        """
        # Check that the raw data frame is properly formatted
        check_raw_data(df_raw, min_keys=['values'])

        # Merge x/y grid data with values. Temporarily extend values with None, then drop those rows
        values = df_raw['values'].to_list()
        values.extend([None] * (len(self._grid['x']) - len(values)))
        df_grid = pd.DataFrame(
            data={
                'values': values,
                'x': self._grid['x'],
                'y': self._grid['y'],
            },
        ).dropna()

        return [
            go.Scatter(
                hoverinfo='none',
                line=self.border_line or {'color': 'black'},
                mode='lines',
                opacity=self.border_opacity,
                showlegend=False,
                x=border['x'],
                y=border['y'],
            ) for border in self._borders
        ] + [
            go.Scatter(
                hoverinfo='text',
                mode='markers',
                showlegend=False,
                text=df_grid['values'],
                x=df_grid['x'],
                y=df_grid['y'],
                marker=self.create_marker(df_grid, **(self.marker_kwargs or {})),
            ),
        ]

    def create_marker(self, df_grid, colorscale='Viridis', size=16, symbol='circle'):
        """Return a dictionary for the scatter plot.

        See: https://plot.ly/python/colorscales/ (Named colorscales: Reds, Bluered, Jet, Viridis, Cividis, etc.)

        Args:
            df_grid: pandas dataframe with at minimum the column `values: str`, `x: float`, `y: float`
            colorscale: plotly colorscale, see doc link above. Default is 'Viridis'
            size: integer marker size
            symbol: marker symbol (square, circle, circle-open, x, etc.)

        Returns:
            dict: the chart marker shape, symbol, color, etc.

        """
        return {
            'color': df_grid['values'],
            'colorscale': colorscale,
            'showscale': True,
            'size': size,
            'symbol': symbol,
        }

    def create_layout(self):
        """Extend the standard layout.

        Returns:
            dict: layout for Dash figure

        """
        layout = super().create_layout()
        for axis in ['xaxis', 'yaxis']:
            layout[axis]['showgrid'] = False
            layout[axis]['showticklabels'] = False
            layout[axis]['zeroline'] = False
        layout['yaxis']['scaleanchor'] = 'x'
        layout['yaxis']['scaleratio'] = 1
        return layout


# ==============================================================================
# Standard Coordinate Grids


class GridClass:
    """Base class for specifying a grid for the Coordinate chart."""

    marker_kwargs = None
    """Marker keyword arguments. Default is None."""

    def __init__(self, grid_dims, titles):
        """Initialize the coordinates.

        Args:
            grid_dims: tuple of the number of tiles in grid. In format `(row, column)`
            titles: list of titles to place in each grid element

        """
        self.grid_dims = grid_dims
        self.titles = titles


class CircleGrid(GridClass):  # noqa: H601
    """Grid of circular coordinates."""

    marker_kwargs = {'size': 10}
    """Marker keyword arguments. Default is `{'size': 10}`"""

    def __init__(self, grid_dims, titles=None):
        """Initialize the coordinates.

        Args:
            grid_dims: tuple of the number of tiles in grid. In format `(row, column)`
            titles: list of titles to place in each grid element. Default is None

        """
        if titles is None:
            titles = []
            for idx in range(grid_dims[0] * grid_dims[1]):
                x_coord = int(idx / grid_dims[1]) + 1
                y_coord = idx % (grid_dims[0] + 1) + 1  # noqa: S001
                titles.append(f'Subtitle for ({x_coord}, {y_coord})')

        super().__init__(grid_dims=grid_dims, titles=titles)

        # Calculate four corners
        opp = 0.5 * math.cos(cmath.pi / 4)
        adj = 0.5 * math.sin(cmath.pi / 4)
        self.corners = {
            'x': [0.5, 1 - adj, 1.0, 1 + adj, 1.5, 1 + adj, 1.0, 1 - adj],
            'y': [1.0, 1 - opp, 0.5, 1 - opp, 1.0, 1 + opp, 1.5, 1 + opp],
        }


def calculate_calendar_grid_corners(margin, days_in_week=7, max_weeks_in_month=6):
    """Calculate the four exterior corner coordinates of a calendar coordinate grid.

    Args:
        margin: float spacing between tiles
        days_in_week: number of days in week. Default is 7
        max_weeks_in_month: max number of weeks in a month. Default is 6

    Returns:
        list: dictionary with keys `(x, y)` containing lists of the four exterior corner coordinates

    """
    y_indices = [[idx] * days_in_week for idx in range(max_weeks_in_month)]
    return {
        'x': np.add([*range(days_in_week)] * max_weeks_in_month, margin),
        'y': np.add([*chain.from_iterable(y_indices)], margin),
    }


class YearGrid(GridClass):  # noqa: H601
    """Coordinates of days within a grid of months in one year."""

    marker_kwargs = {'size': 10, 'symbol': 'square'}
    """Marker keyword arguments. Default is `{'size': 10, 'symbol': 'square'}`"""

    def __init__(self, grid_dims=(4, 3), titles=None):
        """Initialize the coordinates.

        Args:
            grid_dims: tuple of the number of tiles in grid. In format `(row, column)`. Default is (4, 3)
            titles: list of titles to place in each grid element. Default is None

        Raises:
            RuntimeError: if error in the grid dimensions

        """
        if grid_dims[0] * grid_dims[1] != 12:  # pragma: no cover
            raise RuntimeError('Calendar must show all 12 months Expected (12,1), (6,2), (4,3), (1,12), etc.')
        if titles is None:
            titles = calendar.month_name[1:]

        super().__init__(grid_dims=grid_dims, titles=titles)

        # Calculate four corners
        self.corners = calculate_calendar_grid_corners(margin=2)

    def format_data(self, month_lists, year):
        """Return the formatted list that can be passed to a coordinate chart.

        Args:
            month_lists: list of daily values where each sublist is one month starting with January
            year: year expressed in 4 decimal places (i.e. 2019)

        Returns:
            list: of values with additional None values to align with grid

        """
        values = []
        for idx_month, daily_list in enumerate(month_lists):
            idx_first_day, count_days = calendar.monthrange(year, idx_month + 1)
            idx_first_day += 1  # Increment to start on Sunday -- PLANNED: make this configureable
            values.extend([None] * idx_first_day)
            values.extend(daily_list)
            values.extend([None] * (len(self.corners['x']) - idx_first_day - count_days))
        return values


class MonthGrid(GridClass):  # noqa: H601
    """Coordinates of days within a single month."""

    marker_kwargs = {'size': 35, 'symbol': 'square'}
    """Marker keyword arguments. Default is `{'size': 35, 'symbol': 'square'}`"""

    def __init__(self, grid_dims=(1, 1), titles=None):
        """Initialize the coordinates.

        Args:
            grid_dims: tuple of the number of tiles in grid. In format `(row, column)`. Default is (1, 1)
            titles: list of titles to place in each grid element. Default is None

        Raises:
            RuntimeError: if error in the grid dimensions or titles

        """
        if grid_dims != (1, 1):  # pragma: no cover
            raise RuntimeError('Day grid can only show one month, expected (1, 1)')
        if titles is not None and len(titles) != 1:  # pragma: no cover
            raise RuntimeError(f'Only one title is allowed for the MonthGrid. Received: {titles}')

        super().__init__(grid_dims=grid_dims, titles=titles)

        # Calculate four corners
        self.corners = calculate_calendar_grid_corners(margin=1.25)

    def format_data(self, daily_values, year, month):
        """Return the formatted list that can be passed to a coordinate chart.

        Args:
            daily_values: list of values for each day of month
            year: year expressed in 4 digits (2019, 2020, etc.)
            month: month index in [1, 12]

        Returns:
            list: of values with additional None values to align with grid

        """
        idx_first_day = calendar.monthrange(year, month)[0]
        values = [None] * idx_first_day
        values.extend(daily_values)
        return values
