"""Main Helper Functions."""

from pathlib import Path

import dash
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

ASSETS_DIR = Path(__file__).parent / 'assets'


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
        dcc.Graph object

    """
    return dcc.Graph(
        config={
            'displayModeBar': False,
            # 'modeBarButtonsToRemove': ['sendDataToCloud'],
        },
        **kwargs,
    )


def opts_dd(lbl, value):
    """Format an individual item in a dropdown list. Return the dictionary.

    Args:
        lbl: Dropdown label
        value: Dropdown value (will be converted to JSON)

    Returns:
        dict with keys label and value

    """
    return {'label': str(lbl), 'value': value}


def format_callback(lookup, outputs, inputs, states):
    """Return list of Output, Input, and State lists for `@app.callback()`.

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


def unwrap_args(raw_args, inputs, states):
    """TODO.

    Args:
        raw_args: TODO
        inputs: TODO
        states: TODO

    Returns:
        TODO

    """
    input_args = raw_args[:len(inputs)]
    state_args = raw_args[-len(states):]

    results = [{}, {}]
    for result_idx, keys, args in enumerate(((inputs, input_args), (states, state_args))):
        for arg_idx, uniq_id, key in enumerate(keys):
            results[result_idx][uniq_id].update([key, args[arg_idx]])
    return results


# Charts


class CustomChart:
    """Base Class for Custom Charts."""

    def __init__(self, title, x_label, y_label, cust_layout_params=()):
        """Create basic instance of a custom Dash chart.

        Args:
            title: optional, string title for chart. Defaults to blank
            x_label: optional, X- and Y-Axis axis labels. Defaults to an empty string (blank)
            y_label: TODO
            cust_layout_params: Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'

        """
        # Store kwargs as data members
        self.title = title
        self.labels = {'x': x_label, 'y': y_label}
        self.cust_layout_params = cust_layout_params

    def create_figure(self, df, **kwargs_data):
        """Create the figure dictionary.

        Args:
            df: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Return:
            TODO

        """
        return {
            'data': self.create_traces(df, **kwargs_data),
            'layout': go.Layout(self.apply_cust_layout(self.create_layout())),
        }

    def create_traces(self, df, **kwargs_data):
        """Return traces for plotly chart."""
        raise NotImplementedError('create_traces must be implemented by child class')

    def create_layout(self):
        """Return the standard layout. Can be overridden and modified when inherited."""
        layout = dict(
            title=go.layout.Title(text=self.title),
            xaxis={
                'automargin': True,
                'title': self.labels['x'],
            },
            yaxis={
                'automargin': True,
                'title': self.labels['y'],
                'zeroline': True,
            },
            legend={'orientation': 'h'},
            hovermode='closest',
        )

        # Optionally apply the specified range
        for axis in ['x', 'y']:
            axis_name = '{}axis'.format(axis)
            if axis in self.range:
                layout[axis_name]['range'] = self.range[axis]
            else:
                layout[axis_name]['autorange'] = True

        return layout

    def apply_cust_layout(self, layout):
        """Apply/override layout with custom layout parameters.

        Args:
            layout: layout dictionary from self.create_layout()

        Return:
            TODO

        """
        for parent_key, sub_key, val in self.cust_layout_params:
            if sub_key is not None:
                layout[parent_key][sub_key] = val
            else:
                layout[parent_key] = val

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
