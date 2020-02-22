"""Application components built on Dash Bootstrap Components."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc


def dropdown_group(name, _id, options, def_idx, persist=False):
    """Return a Form Group with label and dropdown.

    Args:
        name: label name of dropdown
        _id: element id
        options: list of dicts with keys `(value, label)`
        def_idx: index of initially selected option
        persist: if True, state of dropdown will be preserved on refresh. Defaults is False

    Returns:
        FormGroup: dbc form group of label and dropdown

    """
    return dbc.FormGroup([
        dbc.Label(name),
        dcc.Dropdown(id=_id, options=options, value=options[def_idx]['value'], persistence=persist),
    ])
