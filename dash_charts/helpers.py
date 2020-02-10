"""Main Helper Functions."""

import argparse
from pathlib import Path

import dash
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

ASSETS_DIR = Path(__file__).parent / 'assets'
"""Path to the static files directory."""


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


def init_app(**kwargs):
    """Return new Dash app with `assets_folder` set to local assets.

    Args:
        kwargs: any kwargs to pass to the dash initializer other than `assets_folder`

    Returns:
        app `dash.Dash()` instance

    """
    return dash.Dash(__name__, assets_folder=str(ASSETS_DIR), **kwargs)


def min_graph(**kwargs):
    """Return dcc.Graph element with Plotly overlay removed.

    See: https://community.plot.ly/t/is-it-possible-to-hide-the-floating-toolbar/4911/7

    Args:
        kwargs: any kwargs to pass to the dash initializer other than `assets_folder`

    Returns:
        Dash `dcc.Graph` object

    """
    return dcc.Graph(config={'displayModeBar': False}, **kwargs)


def opts_dd(lbl, value):
    """Format an individual item in a Dash dcc dropdown list.

    Args:
        lbl: Dropdown label
        value: Dropdown value

    Returns:
        dict with keys `label` and `value`

    """
    return {'label': str(lbl), 'value': value}


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
    """Map the function arguments into a dictionary with keys the unique input and state names.

    Args:
        raw_args: list of arguments passed to callback
        inputs: list of unique input element ids
        states: list of unique state element ids

    Returns:
        Returns dictionary with arguments mapped to the unique ids

    """
    input_args = raw_args[:len(inputs)]
    state_args = raw_args[-len(states):]

    results = {}
    for keys, args in ((inputs, input_args), (states, state_args)):
        for arg_idx, uniq_id, key in enumerate(keys):
            results[uniq_id].update([key, args[arg_idx]])
    return results


# Charts


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

    def create_figure(self, df, **kwargs_data):
        """Create the figure dictionary.

        Args:
            df: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Return:
            Dictionary with keys `data` and `layout` for Dash

        """
        return {
            'data': self.create_traces(df, **kwargs_data),
            'layout': go.Layout(self.apply_cust_layout(self.create_layout())),
        }

    def create_traces(self, df, **kwargs_data):
        """Return traces for plotly chart."""
        raise NotImplementedError('create_traces must be implemented by child class')

    def create_layout(self):
        """Return the standard layout. Can be overridden and modified when inherited.

        Return:
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
            axis_name = '{}axis'.format(axis)
            if axis in self.axis_range:
                layout[axis_name]['range'] = self.axis_range[axis]
            else:
                layout[axis_name]['autorange'] = True

        return layout

    def apply_cust_layout(self, layout):
        """Extend and/or override layout with custom settings.

        Args:
            layout: base layout dictionary. Typically from self.create_layout()

        Return:
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

    def create_figure(self, df, **kwargs_data):
        """Create the figure dictionary.

        Args:
            data: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Return:
            TODO

        """
        fig = make_subplots(
            rows=2, cols=2,
            shared_xaxes=True, shared_yaxes=True,
            vertical_spacing=0.02, horizontal_spacing=0.02,
            row_width=[0.8, 0.2], column_width=[0.8, 0.2],
        )
        traces = [
            (self.create_traces, 2, 1), (self.create_marg_top, 1, 1), (self.create_marg_right, 2, 2),
        ]
        for trace_func, row, col in traces:
            for trace in trace_func(df, **kwargs_data):
                fig.add_trace(trace, row, col)
        # Apply axis labels
        fig.update_xaxes(title_text=self.labels['x'], row=2, col=1)
        fig.update_yaxes(title_text=self.labels['y'], row=2, col=1)
        # Replace the default blue/white grid introduced in Plotly v4
        fig.update_xaxes(showgrid=True, gridcolor='white')
        fig.update_yaxes(showgrid=True, gridcolor='white')
        fig['layout'].update(self.apply_cust_layout(self.create_layout()))
        return fig

    def create_traces(self, df, **kwargs_data):
        """Return traces for plotly chart."""
        return []

    def create_marg_top(self, df, **kwargs_data):
        """Return traces for the top marginal chart."""
        return []

    def create_marg_right(self, df, **kwargs_data):
        """Return traces for the right marginal chart."""
        return []

    def create_layout(self):
        """Override the default layout and add additional settings."""
        layout = super().create_layout()
        # Remove axis lables from layout as they would be applied to row=1,col=1
        layout['xaxis']['title'] = ''
        layout['yaxis']['title'] = ''
        layout['plot_bgcolor'] = '#F0F0F0'
        return layout


# Component: May consist of one or more charts and/or user inputs
# Combines elements into module that can be integrated into larger app. May have callbacks


# TODO

# Base App: Base class for application that includes components, charts, and/or other Dash inputs
