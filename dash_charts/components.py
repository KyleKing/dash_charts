"""Application components built on Dash Bootstrap Components."""

import dash_bootstrap_components as dbc
from dash import dcc


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
        Row: dbc row with label and dropdown

    """
    if form_style is None:
        form_style = {}
    return dbc.Row(
        [
            dbc.Label(name),
            dcc.Dropdown(id=_id, options=options, **dropdown_kwargs),
        ], style=form_style,
    )


def format_email_pass_id(submit_id):
    """Return tuple of the formatted email and password IDs based on the base submit_id value.

    Args:
        submit_id: id used to create unique element IDs

    Returns:
        tuple: formatted IDs: `(email_id, pass_id)`

    """
    return [f'{submit_id}-{key}' for key in ['email', 'password']]


def login_form(submit_id):
    """Return dbcForm with email and password inputs and submit button.

    Based on: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/

    Args:
        submit_id: id used to create unique element IDs

    Returns:
        form: dbc.Form with email and password inputs and submit button

    """
    email_id, pass_id = format_email_pass_id(submit_id)
    return dbc.Form(
        dbc.Row(
            [
                dbc.Label('Email', width='auto'),
                dbc.Col(
                    dbc.Input(type='email', placeholder='Enter email', id=email_id),
                    className='me-3',
                ),
                dbc.Label('Password', width='auto'),
                dbc.Col(
                    dbc.Input(type='password', placeholder='Enter password', id=pass_id),
                    className='me-3',
                ),
                dbc.Col(dbc.Button('Submit', color='primary', id=submit_id), width='auto'),
            ],
            className='g-2',
        ),
    )
