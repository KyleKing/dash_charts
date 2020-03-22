"""Utilities for custom Dash figures."""

import dash_core_components as dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .dash_helpers import validate

# TODO: Methods for making charts/callbacks that update when data changes in a SQL database?


def min_graph(**kwargs):
    """Return dcc.Graph element with Plotly overlay removed.

    See: https://community.plot.ly/t/is-it-possible-to-hide-the-floating-toolbar/4911/7

    Args:
        kwargs: any kwargs to pass to the dash initializer other than `assets_folder`

    Returns:
        dict: Dash `dcc.Graph` object

    """
    return dcc.Graph(config={'displayModeBar': False}, **kwargs)


def check_raw_data(df_raw, min_keys):
    """Verify that dataframe contains the minimum columns.

    Args:
        df_raw: data to pass to formatter method
        min_keys: list of string column names expected in dataframe

    Raises:
        RuntimeError: if any columns are missing from dataframe

    """
    all_keys = df_raw.keys()
    if len([_k for _k in min_keys if _k in all_keys]) != len(min_keys):
        raise RuntimeError(f'`df_raw` must have keys {min_keys}. Found: {all_keys}')


class CustomChart:
    """Base Class for Custom Charts."""

    _axis_range = {}
    _axis_range_schema = {
        'x': {
            'items': [{'type': ['integer', 'float']}, {'type': ['integer', 'float']}],
            'required': False,
            'type': 'list',
        },
        'y': {
            'items': [{'type': ['integer', 'float']}, {'type': ['integer', 'float']}],
            'required': False,
            'type': 'list',
        },
    }

    @property
    def axis_range(self):
        """Specify x/y axis range or leave as empty dictionary for autorange.

        Returns:
            dict: dictionary potentially with keys `(x, y)`

        """
        return self._axis_range

    @axis_range.setter
    def axis_range(self, axis_range):
        errors = validate(axis_range, self._axis_range_schema)
        if errors:
            raise RuntimeError(f'Validation of self.axis_range failed: {errors}')
        # Assign new axis_range
        self._axis_range = axis_range

    def __init__(self, *, title, xlabel, ylabel, layout_overrides=()):
        """Initialize Custom Dash Chart and store parameters as data members.

        Args:
            title: String title for chart (can be an empty string for blank)
            xlabel: XAxis string label (can be an empty string for blank)
            ylabel: YAxis string label (can be an empty string for blank)
            layout_overrides: Custom parameters in format [ParentKey, SubKey, Value] to customize 'go.layout'

        """
        self.title = title
        self.labels = {'x': xlabel, 'y': ylabel}
        self.layout_overrides = layout_overrides
        self.initialize_mutables()

    def initialize_mutables(self):
        """Initialize the mutable data members to prevent modifying one attribute and impacting all instances."""
        pass

    def create_figure(self, df_raw, **kwargs_data):
        """Create the figure dictionary.

        Args:
            df_raw: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Returns:
            dict: keys `data` and `layout` for Dash

        """
        return {
            'data': self.create_traces(df_raw, **kwargs_data),
            'layout': go.Layout(self.apply_custom_layout(self.create_layout())),
        }

    def create_traces(self, df_raw, **kwargs_data):
        """Return traces for plotly chart.

        Should return, list: trace data points. List may be empty

        Args:
            df_raw: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Raises:
            NotImplementedError: Must be overridden by child class

        """
        raise NotImplementedError('create_traces must be implemented by child class')  # pragma: no cover

    def create_layout(self):
        """Return the standard layout. Can be overridden and modified when inherited.

        Returns:
            dict: layout for Dash figure

        """
        layout = {
            'title': go.layout.Title(text=self.title),
            'xaxis': {
                'automargin': True,
                'title': self.labels['x'],
            },
            'yaxis': {
                'automargin': True,
                'title': self.labels['y'],
                'zeroline': True,
            },
            'legend': {'orientation': 'h'},
            'hovermode': 'closest',
        }

        # Optionally apply the specified range
        for axis in ['x', 'y']:
            axis_name = f'{axis}axis'
            if axis in self.axis_range:
                layout[axis_name]['range'] = self.axis_range[axis]
            else:
                layout[axis_name]['autorange'] = True

        return layout

    def apply_custom_layout(self, layout):
        """Extend and/or override layout with custom settings.

        Args:
            layout: base layout dictionary. Typically from self.create_layout()

        Returns:
            dict: layout for Dash figure

        """
        for parent_key, sub_key, value in self.layout_overrides:
            if sub_key is not None:
                layout[parent_key][sub_key] = value
            else:
                layout[parent_key] = value

        return layout


class MarginalChart(CustomChart):
    """Base Class for Custom Charts with Marginal X and Marginal Y Plots."""

    def create_figure(self, df_raw, **kwargs_data):
        """Create the figure dictionary.

        Args:
            df_raw: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Returns:
            dict: Dash figure object

        """
        # Initialize figure with subplots
        fig = make_subplots(
            rows=2, cols=2,
            shared_xaxes=True, shared_yaxes=True,
            vertical_spacing=0.02, horizontal_spacing=0.02,
            row_width=[0.8, 0.2], column_width=[0.8, 0.2],
        )
        # Populate the traces of each subplot
        traces = [
            (self.create_traces, 2, 1),
            (self.create_marg_top, 1, 1),
            (self.create_marg_right, 2, 2),
        ]
        for trace_func, row, col in traces:
            for trace in trace_func(df_raw, **kwargs_data):
                fig.add_trace(trace, row, col)
        # Apply axis labels
        fig.update_xaxes(title_text=self.labels['x'], row=2, col=1)
        fig.update_yaxes(title_text=self.labels['y'], row=2, col=1)
        # Replace the default blue/white grid introduced in Plotly v4
        fig.update_xaxes(showgrid=True, gridcolor='white')
        fig.update_yaxes(showgrid=True, gridcolor='white')
        fig['layout'].update(self.apply_custom_layout(self.create_layout()))
        return fig

    def create_traces(self, df_raw, **kwargs_data):
        """Return traces for the main plotly chart.

        Should return, list: trace data points. List may be empty

        Args:
            df_raw: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Raises:
            NotImplementedError: Must be overridden by child class

        """
        raise NotImplementedError('create_traces must be implemented by child class')  # pragma: no cover

    def create_marg_top(self, df_raw, **kwargs_data):
        """Return traces for the top marginal chart.

        Should return, list: trace data points. List may be empty

        Args:
            df_raw: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Raises:
            NotImplementedError: Must be overridden by child class

        """
        raise NotImplementedError('create_marg_top must be implemented by child class')  # pragma: no cover

    def create_marg_right(self, df_raw, **kwargs_data):
        """Return traces for the right marginal chart.

        Should return, list: trace data points. List may be empty

        Args:
            df_raw: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Raises:
            NotImplementedError: Must be overridden by child class

        """
        raise NotImplementedError('create_marg_right must be implemented by child class')  # pragma: no cover

    def create_layout(self, *, bg_color='#F0F0F0'):
        """Remove axis lables from base layout as they would be applied to (row=1,col=1).

        Args:
            bg_color: Background color for the chart. Default is white for light themes

        Returns:
            dict: updated layout for Dash figure

        """
        layout = super().create_layout()
        layout['xaxis']['title'] = ''
        layout['yaxis']['title'] = ''
        layout['plot_bgcolor'] = bg_color
        return layout
