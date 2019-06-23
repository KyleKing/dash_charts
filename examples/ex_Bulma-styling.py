"""Example Bulma layout.

See documentation on Bulma layouts: https://bulma.io/documentation/layout/tiles/

"""

import dash_html_components as html
import numpy as np
import pandas as pd
import plotly_express as px
from dash_charts.helpers import MinGraph, initApp
from dash_charts.rolling_chart import RollingChart

app = initApp()

# ------------------
# Start Boilerplate from `ex_rolling_chart.py`

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
# Initialize an example chart
exRolling = RollingChart(
    title='Sample Timeseries Chart',
    xLbl='Index',
    yLbl='Measured Value',
)

# End Boilerplate
# ------------------

# ------------------
# Demo laying out a 3 column grid with Bulma where
#   - the first column has three tiles
#   - the middle column is half the full screen width
#   - the tiles will wrap on smaller screens

# Initialize the dashboard layout
app.layout = html.Div(className='section', children=[
    html.Div(className='tile is-ancestor', children=[
        html.Div(className='tile is-parent is-vertical is-3', children=[
            html.Article(className='tile is-child notification', children=[
                html.P(className='title', children='Top Vertical Tile'),
                html.P(
                    className='subtitle',
                    children='Uses notification class for grey background and internal padding',
                ),
                html.P(className='subtitle', children='Could also add is-info, is-warning, etc.'),
            ]),
            html.Article(className='tile is-child', children=[
                html.P(className='title', children='Vertical...'),
                html.P(className='subtitle', children='(Top tile)'),
                MinGraph(
                    figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=200),
                ),
            ]),
            html.Article(className='tile is-child', children=[
                html.P(className='title', children='...tiles'),
                html.P(className='subtitle', children='(Bottom tile)'),
                MinGraph(
                    figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=200),
                ),
            ]),
        ]),
        MinGraph(
            className='tile is-child is-6 is-block-desktop',
            figure=exRolling.createFigure(df=dfDemo, dataLbl='Demo Data', rollingCount=4),
        ),
        html.Article(className='tile is-child is-3 is-block-desktop', children=[
            html.P(className='title', children='A Small Chart'),
            MinGraph(
                figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=350),
            ),
            html.P(className='subtitle', children='An Image'),
            html.Img(src='https://media.giphy.com/media/JGQe5mxayVF04/giphy.gif')
        ]),
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True)
