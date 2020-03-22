"""Application components built on Dash Bootstrap Components."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc


def opts_dd(lbl, value):
    """Format an individual item in a Dash dcc dropdown list.

    Args:
        lbl: Dropdown label
        value: Dropdown value

    Returns:
        dict: keys `label` and `value` for dcc.dropdown()

    """
    return {'label': str(lbl), 'value': value}


def dropdown_group(name, _id, options, form_style=None, **dropdown_kwargs):
    """Return a Form Group with label and dropdown.

    Dropdown documentation: https://dash.plot.ly/dash-core-components/dropdown

    Args:
        name: label name of dropdown
        _id: element id
        options: list of dicts with keys `(value, label)`
        form_style: style keyword argument for dbc.FormGroup(). Default is None
        dropdown_kwargs: key word arguments for dropdown. Could be: `(persistence, multi, searchable, etc.)`

    Returns:
        FormGroup: dbc form group of label and dropdown

    """
    if form_style is None:
        form_style = {}
    return dbc.FormGroup([
        dbc.Label(name),
        dcc.Dropdown(id=_id, options=options, **dropdown_kwargs),
    ], style=form_style)
