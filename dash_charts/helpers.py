"""Main Helper Functions and Base Classes.

Charts: Functions and base classes to create templates for Dash figures
BaseApp: Base template for building an application

"""

import argparse
from itertools import count
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

ASSETS_DIR = Path(__file__).parent / 'assets'
"""Path to the static files directory."""

COUNTER = count(start=0, step=1)
"""Initialize iterator to provide set of unique integers when called with `next()`."""


def parse_cli_args():
    """Configure the CLI options for Dash applications.

    Returns:
        port number

    """
    parser = argparse.ArgumentParser(description='Process Dash Parameters.')
    parser.add_argument('--port', type=int, default=8050,
                        help='Pass port number to Dash server. Default is 8050')
    args = parser.parse_args()
    return args.port


# Charts


def min_graph(**kwargs):
    """Return dcc.Graph element with Plotly overlay removed.

    See: https://community.plot.ly/t/is-it-possible-to-hide-the-floating-toolbar/4911/7

    Args:
        kwargs: any kwargs to pass to the dash initializer other than `assets_folder`

    Returns:
        Dash `dcc.Graph` object

    """
    return dcc.Graph(config={'displayModeBar': False}, **kwargs)


def format_callback(lookup, outputs, inputs, states):
    """Format list of [Output, Input, State] for `@app.callback()`.

    Args:
        lookup: dict with generic key that maps to unique string
        outputs: list of tuples with id and key
        inputs: list of tuples with id and key
        states: list of tuples with id and key

    Returns:
        list of lists for `@app.callback()`

    """
    return ([Output(lookup[_id], key) for _id, key in outputs],
            [Input(lookup[_id], key) for _id, key in inputs],
            [State(lookup[_id], key) for _id, key in states])


def map_args(raw_args, inputs, states):
    """Map the function arguments into a dictionary with keys for the unique input and state names.

    Args:
        raw_args: list of arguments passed to callback
        inputs: list of unique input element ids
        states: list of unique state element ids

    Returns:
        Returns dictionary with arguments mapped to the unique ids

    """
    input_args = raw_args[:len(inputs)]
    state_args = raw_args[len(inputs):]

    results = {}
    for keys, args in ((inputs, input_args), (states, state_args)):
        for arg_idx, uniq_id, key in enumerate(keys):
            results[uniq_id].update([key, args[arg_idx]])
    return results


class CustomChart:
    """Base Class for Custom Charts."""

    axis_range = {}  # If None or empty dict, will enable autorange. Add X/Y keys to set range

    def __init__(self, title, x_label, y_label, cust_layout_params=()):
        """Initialize Custom Dash Chart and store parameters as data members.

        Args:
            title: String title for chart  (can be an empty string for blank)
            x_label: XAxis string label (can be an empty string for blank)
            y_label: YAxis string label (can be an empty string for blank)
            cust_layout_params: Custom parameters in format [ParentKey, SubKey, Value] to customize 'go.layout'

        """
        self.title = title
        self.labels = {'x': x_label, 'y': y_label}
        self.cust_layout_params = cust_layout_params

    def create_figure(self, raw_df, **kwargs_data):
        """Create the figure dictionary.

        Args:
            raw_df: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Returns:
            Dictionary with keys `data` and `layout` for Dash

        """
        return {
            'data': self.create_traces(raw_df, **kwargs_data),
            'layout': go.Layout(self.apply_cust_layout(self.create_layout())),
        }

    def create_traces(self, raw_df, **kwargs_data):
        """Return traces for plotly chart.

        Args:
            raw_df: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Raises:
            NotImplementedError: Must be overridden by child class

        """
        raise NotImplementedError('create_traces must be implemented by child class')

    def create_layout(self):
        """Return the standard layout. Can be overridden and modified when inherited.

        Returns:
            layout dictionary for Dash figure

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

    def apply_cust_layout(self, layout):
        """Extend and/or override layout with custom settings.

        Args:
            layout: base layout dictionary. Typically from self.create_layout()

        Returns:
            layout dictionary for Dash figure

        """
        for parent_key, sub_key, value in self.cust_layout_params:
            if sub_key is not None:
                layout[parent_key][sub_key] = value
            else:
                layout[parent_key] = value

        return layout


class MarginalChart(CustomChart):
    """Base Class for Custom Charts with Marginal X and Marginal Y Plots."""

    def create_figure(self, raw_df, **kwargs_data):
        """Create the figure dictionary.

        Args:
            raw_df: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Returns:
            Dash figure object

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
        for (trace_func, row, col) in traces:
            for trace in trace_func(raw_df, **kwargs_data):
                fig.add_trace(trace, row, col)
        # Apply axis labels
        fig.update_xaxes(title_text=self.labels['x'], row=2, col=1)
        fig.update_yaxes(title_text=self.labels['y'], row=2, col=1)
        # Replace the default blue/white grid introduced in Plotly v4
        fig.update_xaxes(showgrid=True, gridcolor='white')
        fig.update_yaxes(showgrid=True, gridcolor='white')
        fig['layout'].update(self.apply_cust_layout(self.create_layout()))
        return fig

    def create_traces(self, raw_df, **kwargs_data):
        """Return traces for the main plotly chart.

        Args:
            raw_df: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Returns:
            Empty list. Should be overridden by child class. Will otherwise be empty

        """
        return []

    def create_marg_top(self, raw_df, **kwargs_data):
        """Return traces for the top marginal chart.

        Args:
            raw_df: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Returns:
            Empty list. Should be overridden by child class. Will otherwise be empty

        """
        return []

    def create_marg_right(self, raw_df, **kwargs_data):
        """Return traces for the right marginal chart.

        Args:
            raw_df: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Returns:
            Empty list. Should be overridden by child class. Will otherwise be empty

        """
        return []

    def create_layout(self):
        """Remove axis lables from base layout as they would be applied to (row=1,col=1).

        Returns:
            Updated layout dictionary for Dash figure

        """
        layout = super().create_layout()
        layout['xaxis']['title'] = ''
        layout['yaxis']['title'] = ''
        layout['plot_bgcolor'] = '#F0F0F0'
        return layout


# Base App


def init_app(**kwargs):
    """Return new Dash app with `assets_folder` set to local assets.

    Args:
        kwargs: any kwargs to pass to the dash initializer other than `assets_folder`

    Returns:
        app `dash.Dash()` instance

    """
    return dash.Dash(__name__, assets_folder=str(ASSETS_DIR), **kwargs)


def opts_dd(lbl, value):
    """Format an individual item in a Dash dcc dropdown list.

    Args:
        lbl: Dropdown label
        value: Dropdown value

    Returns:
        dict with keys `label` and `value`

    """
    return {'label': str(lbl), 'value': value}


class BaseApp:
    """Base class for building Dash Applications."""

    name = None
    """Child class must specify a name for the application"""

    uniq_ids = {}
    """Lookup dictionary used to track each element in UI that requires a callback"""

    # In child class, declare the rest of the static data members here

    def __init__(self, app=None):
        """Initialize app and initial data members. Should be inherited in child class and called with super().

        Args:
            app: Dash instance. If None, will create standalone app. Otherwise, will be part of existing app

        Raises:
            RuntimeError: if child class has not set a `self.name` data member

        """
        self.app = init_app() if app is None else app
        if self.name is None:
            raise RuntimeError('Child class must set `self.name` to a unique string for this app')

    def register_uniq_ids(self, base_ids):
        """Register all ids in the lookup dictionary.

        Args:
            base_ids: list of unique strings to register with the lookup dictionary

        """
        for base_id in base_ids:
            self.uniq_ids[base_id] = f'{self.name}-{base_id}'

    def run(self, **dash_kwargs):
        """Run the application passing any kwargs to Dash.

        Args:
            **dash_kwargs: keyword arguments for `Dash.run_server()`

        Raises:
            RuntimeError: if child class has not called `self.register_uniq_ids`

        """
        if not self.uniq_ids.keys():
            raise RuntimeError('Child class must first call `self.register_uniq_ids(__)` before self.run()')

        # Register the charts, the app layout, the callbacks, then start the Dash server
        self.register_charts()
        self.app.layout = self.return_layout()
        self.register_callbacks()
        self.app.run_server(**dash_kwargs)  # TODO: How does this work with multiple apps?

    def register_charts(self):
        """Register the initial charts.

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('register_charts is not implemented')

    def returnLayout(self):
        """Return Dash application layout.

        Returns:
            Dash application layout. Default is simple HTML text

        """
        return html.Div(children=['Welcome to the BaseApp!'])

    def register_callbacks(self):
        """Register the chart callbacks.

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('register_callbacks is not implemented')
