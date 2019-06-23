"""Example Pareto Chart."""

import dash_html_components as html
import pandas as pd
from dash_charts import helpers
from dash_charts.helpers import initApp
from dash_charts.pareto_chart import ParetoChart

app = initApp()

# ------------------
# Sample Data

dfDemo = pd.DataFrame(data={
    'value': [76, None, 131, 1, 41, 42, 92, None],
    'label': [
        'Every Cloud Has a Silver Lining',
        'Should be #7',
        'Back To the Drawing Board',
        'Lickety Split',
        'Mountain Out of a Molehill',
        'Everything But The Kitchen Sink',
        'Happy as a Clam',
        'SHOULDN\'T APPEAR',
    ],
})

# ------------------
# Layout

# Initialize an example chart
exPareto = ParetoChart(
    title='Sample Pareto Chart',
    xLbl='Category Title',
    yLbl='Measured Downtime (hours)',
    colors=('#87C9A3', '#BA3D4D'),
    limitCat=7,
)

# Initialize the dashboard layout
app.layout = html.Div(
    className='section',
    children=[
        html.H4(children='Example Pareto Chart'),
        html.Div([
            helpers.MinGraph(
                id='pareto-chart',
                figure=exPareto.createFigure(df=dfDemo),
            ),
        ]),
    ],
)

if __name__ == '__main__':
    app.run_server(debug=True)
