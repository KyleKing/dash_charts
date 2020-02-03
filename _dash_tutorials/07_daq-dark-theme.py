"""Example using Dash DAQ.

Source: https://dash.plot.ly/dash-daq

"""

import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_charts.helpers import init_app

app = init_app()

THEME = {
    'dark': False,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E'
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
            style={'display': 'block', 'margin-left': 'calc(50% - 110px)'},
        ),
    ],
)


@app.callback(
    Output('dial-component', 'children'),
    [Input('theme-toggle', 'value')]
)
def activateDarkTheme(darkEnabled):
    """Update the daw theme provider based on the toggle setting."""
    THEME.update(dark=bool(darkEnabled))
    # Return a cool-looking dial, but could be a graph, etc.
    return daq.DarkThemeProvider(theme=THEME, children=daq.Knob(value=6))


@app.callback(
    Output('full-window', 'style'),  # FYI: Overwrites style prop for this div
    [Input('theme-toggle', 'value')]
)
def setBackground(darkEnabled):
    """Set the background styles."""
    if darkEnabled:
        return {'background-color': '#303030', 'color': 'white', 'height': '100vh'}
    return {'background-color': 'white', 'color': 'black', 'height': '100vh'}


if __name__ == '__main__':
    app.run_server(debug=True)
