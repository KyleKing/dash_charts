"""Utilities for better Dash callbacks."""

import re

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


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
    return (
        [Output(component_id=lookup[_id], component_property=prop) for _id, prop in outputs],
        [Input(component_id=lookup[_id], component_property=prop) for _id, prop in inputs],
        [State(component_id=lookup[_id], component_property=prop) for _id, prop in states],
    )


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
    for app_id in lookup:
        lookup[app_id] = dict(lookup[app_id])

    return [lookup[app_id][prop] for app_id, prop in outputs]


def get_triggered_id():
    """Use Dash context to get the id of the input element that triggered the callback.

    See advanced callbacks: https://dash.plotly.com/advanced-callbacks

    Returns:
        str: id of the input that triggered the callback

    Raises:
        PreventUpdate: if callback was fired without an input

    """
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    prop_id = ctx.triggered[0]['prop_id']  # in format: `id.key` where we only want the `id`
    return re.search(r'(^.+)\.[^\.]+$', prop_id)[1]
