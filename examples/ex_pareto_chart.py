"""Example Pareto Chart."""

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from _config import app
from dash_charts.pareto_chart import ParetoChart

# ------------------
# Sample Data

dfDemo = pd.DataFrame(data={
    'value': [76, 131, None, 41, 42, 92],
    'label': [
        'Every Cloud Has a Silver Lining',
        'Back To the Drawing Board',
        'Lickety Split',
        'Mountain Out of a Molehill',
        'Everything But The Kitchen Sink',
        'Happy as a Clam',
    ],
})

# ------------------
# Layout

# Initialize an example chart
exampleParetoChart = ParetoChart(
    title='Sample Pareto Chart',
    xLbl='Category Title',
    yLbl='Measured Downtime (hours)',
    colors=('#87C9A3', '#BA3D4D'),
)

# Initialize the dashboard layout
app.layout = html.Div(
    className='app-content',
    children=[
        html.H4(children='Example Pareto Chart'),
        html.Div([
            dcc.Graph(
                id='pareto-chart',
                figure=exampleParetoChart.createFigure(df=dfDemo),
            ),
        ]),
    ],
)

if __name__ == '__main__':
    app.run_server(debug=True)
