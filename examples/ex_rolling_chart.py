"""Example Rolling Mean and Filled Standard Deviation Chart."""

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from _config import app
from dash_charts.rolling_chart import RollingChart

# ------------------
# Sample Data

# Generate random data points
count = 1000
mu, sigma = (15, 10)  # mean and standard deviation
samples = np.random.normal(mu, sigma, count)
# Add a break at the mid-point
midCount = count / 2
yVals = [samples[_i] + (-1 if _i > midCount else 1) * _i / 10.0 for _i in range(count)]

# Combine into a dataframe
dfDemo = pd.DataFrame(data={
    'x': range(count),
    'y': yVals,
    'label': ['Point {}'.format(idx) for idx in range(count)],
})

# ------------------
# Layout

# Initialize an example chart
exampleRollingChart = RollingChart(
    title='Sample Timeseries Chart',
    xLbl='Index',
    yLbl='Measured Value',
)

# Initialize the dashboard layout
app.layout = html.Div(
    className='app-content',
    children=[
        html.H4(children='Example Rolling  Chart'),
        html.Div([
            dcc.Graph(id='rolling-chart', figure=exampleRollingChart.createFigure(df=dfDemo)),
        ]),
    ],
)

if __name__ == '__main__':
    app.run_server(debug=True)
