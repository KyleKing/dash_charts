"""Utilities for custom Dash figures."""

import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
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


def format_app_callback(lookup, outputs, inputs, states):
    """Format list of [Output, Input, State] for `@app.callback()`.

    Args:
        lookup: dict with app_id keys that map to a globally unique component id
        outputs: list of tuples with app_id and property name
        inputs: list of tuples with app_id and property name
        states: list of tuples with app_id and property name

    Returns:
        list: list[lists] in order `(Outputs, Inputs, States)` for `@app.callback()`. Some sublists may be empty

    """
    return ([Output(component_id=lookup[_id], component_property=prop) for _id, prop in outputs],
            [Input(component_id=lookup[_id], component_property=prop) for _id, prop in inputs],
            [State(component_id=lookup[_id], component_property=prop) for _id, prop in states])


def map_args(raw_args, inputs, states):
    """Map the function arguments into a dictionary with keys for the input and state names.

    For situations where the order of inputs and states may change, use this function to verbosely define the inputs:

    ```python
    a_in, a_state = map_args(raw_args, inputs, states)
    click_data = a_in[self.id_main_figure]['clickData']
    n_clicks = a_in[self.id_randomize_button]['n_clicks']
    data_cache = a_state[self.id_store]['data']
    ```

    Alternatively, for use cases that are unlikely to change the order of Inputs/State, unwrap positionally with:

    ```python
    click_data, n_clicks = args[:len(inputs)]
    data_cache = args[len(inputs):]
    ```

    Args:
        raw_args: list of arguments passed to callback
        inputs: list of input components. May be empty list
        states: list of state components. May be empty list

    Returns:
        dict: with keys of the app_id, property, and arg value (`a_in[key][arg_type]`)

    """
    # Split args into groups of inputs/states
    a_in = raw_args[:len(inputs)]
    a_state = raw_args[len(inputs):]

    # Map args into dictionaries
    arg_map = [{app_id: [] for app_id in {items[0] for items in group}} for group in [inputs, states]]
    for group_idx, (groups, args) in enumerate([(inputs, a_in), (states, a_state)]):
        # Assign the arg to the appropriate dictionary in arg_map
        for arg_idx, (app_id, prop) in enumerate(groups):
            arg_map[group_idx][app_id].append((prop, args[arg_idx]))
        for app_id in arg_map[group_idx].keys():
            arg_map[group_idx][app_id] = dict(arg_map[group_idx][app_id])
    return arg_map


def map_outputs(outputs, element_info):
    """Return properly ordered list of new Dash elements based on the order of outputs.

    Alternatively, for simple cases of 1-2 outputs, just return the list with:

    ```python
    return [new_element_1, new_element_2]
    ```

    Args:
        outputs: list of output components
        element_info: list of tuples with keys `(app_id, prop, element)`

    Returns:
        list: ordered list to match the order of outputs

    Raises:
        RuntimeError: Check that the number of outputs and the number of element_info match

    """
    if len(outputs) != len(element_info):
        raise RuntimeError(f'Expected same number of items between:\noutputs:{outputs}\nelement_info:{element_info}')

    # Create a dictionary of the elements
    lookup = {app_id: [] for app_id in {info[0] for info in element_info}}
    for app_id, prop, element in element_info:
        lookup[app_id].append((prop, element))
    for app_id in lookup.keys():
        lookup[app_id] = dict(lookup[app_id])

    # Create the returned list in the order of the outputs
    results = []
    for app_id, prop in outputs:
        results.append(lookup[app_id][prop])
    return results


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
            (self._create_marg_top, 1, 1),
            (self._create_marg_right, 2, 2),
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

    def _create_marg_top(self, df_raw, **kwargs_data):
        """Return traces for the top marginal chart.

        Should return, list: trace data points. List may be empty

        Args:
            df_raw: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Raises:
            NotImplementedError: Must be overridden by child class

        """
        raise NotImplementedError('_create_marg_top must be implemented by child class')  # pragma: no cover

    def _create_marg_right(self, df_raw, **kwargs_data):
        """Return traces for the right marginal chart.

        Should return, list: trace data points. List may be empty

        Args:
            df_raw: data to pass to formatter method
            kwargs_data: keyword arguments to pass to the data formatter method

        Raises:
            NotImplementedError: Must be overridden by child class

        """
        raise NotImplementedError('_create_marg_right must be implemented by child class')  # pragma: no cover

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
