"""Example using Dash DAQ to toggle the dark mode.

Source: https://dash.plot.ly/dash-daq

"""

import dash_daq as daq
from dash import html
from dash.dependencies import Input, Output

from dash_charts.utils_app import init_app

app = init_app()

THEME = {
    'dark': False,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

app.layout = html.Div(
    id='full-window',
    children=[
        html.Br(),
        daq.ToggleSwitch(
            id='theme-toggle',
            label=['Light', 'Dark'],
            style={'width': '250px', 'margin': 'auto'},
            value=True,
        ),
        html.Div(
            id='dial-component',
            children=[],
            style={'display': 'block', 'marginLeft': 'calc(50% - 110px)'},
        ),
    ],
)


@app.callback(
    Output('dial-component', 'children'),
    [Input('theme-toggle', 'value')],
)
def activate_dark_theme(dark_enabled):
    """Update the daw theme provider based on the toggle setting."""
    THEME.update(dark=bool(dark_enabled))  # noqa: DAR101, DAR201
    # Return a cool-looking dial, but could be a graph, etc.
    return daq.DarkThemeProvider(theme=THEME, children=daq.Knob(value=6))


@app.callback(
    Output('full-window', 'style'),  # NOTE: Overwrites style prop for this div
    [Input('theme-toggle', 'value')],
)
def set_background(dark_enabled):
    """Set the background styles."""
    if dark_enabled:  # noqa: DAR101, DAR201
        return {'background-color': '#303030', 'color': 'white', 'height': '100vh'}
    return {'background-color': 'white', 'color': 'black', 'height': '100vh'}


if __name__ == '__main__':
    app.run_server(debug=True)
