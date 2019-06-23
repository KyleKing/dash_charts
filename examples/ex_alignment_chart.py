"""Example Alignment Chart."""

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from dash_charts import helpers
from dash_charts.alignment_chart import AlignChart
from dash_charts.helpers import initApp

app = initApp()

# ------------------
# Sample Data

# Generate a grid of initial points
dim = 5
count = pow(dim, 2)
grid = np.meshgrid(*([np.linspace(1, dim, dim)] * 2))

# Combine into a dataframe
dfDemo = pd.DataFrame(data={
    'x': grid[0].flatten(),
    'y': grid[1].flatten(),
    'xDelta': np.random.randn(count) / 12,
    'yDelta': np.random.randn(count) / 8,
    'label': ['Point {}'.format(idx) for idx in range(count)],
})

# ------------------
# Layout

# Initialize an example chart
exAlign = AlignChart(
    title='Positioning Error Analysis',
    xLbl='X-Axis Measurements (µm)',
    yLbl='Y-Axis Measurements (µm)',
    measLbl='Positioning Error',
    idealLbl='Expected Position',
    pad=0.75,
)

# Initialize the dashboard layout
app.layout = html.Div(className='section', children=html.Div(
    className='something',
    children=[
        html.H4(children='Example Alignment Chart'),
        html.Div([
            helpers.MinGraph(id='alignment-chart'),
        ]),
        dcc.Slider(id='stretch-input', min=0, max=20, step=0.1, value=5),
        html.Div(id='slider-output-container'),
        html.Button('Reset to 1', id='reset-button', className='button is-primary'),
    ],
))

# ------------------
# Callbacks


@app.callback(
    Output('alignment-chart', 'figure'),
    [Input('stretch-input', 'value')])
def updateAlignChart(stretch):
    """Create/update the alignment chart with the user-configurable stretch input."""
    return exAlign.createFigure(df=dfDemo, stretch=stretch)


@app.callback(
    Output('slider-output-container', 'children'),
    [Input('stretch-input', 'value')])
def indicateSliderPos(stretch):
    """Add text describing the current slider value."""
    return 'Selected stretch factor: `{}`'.format(stretch)


@app.callback(
    Output('stretch-input', 'value'),
    [Input('reset-button', 'n_clicks')])
def resetstretch(_n_clicks):
    """Button to reset the stretch factor."""
    return 1


if __name__ == '__main__':
    app.run_server(debug=True)
