"""Example Pareto Chart."""

import dash_html_components as html
import pandas as pd
from dash_charts import helpers
from dash_charts.pareto_chart import ParetoChart


class ParetoDemo:
    """Demo Simple Pareto Chart."""

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

    def __init__(self):
        """Initialize app."""
        self.app = helpers.initApp()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        # Initialize an example chart
        self.exPareto = ParetoChart(
            title='Sample Pareto Chart',
            xLbl='Category Title',
            yLbl='Measured Downtime (hours)',
            colors=('#87C9A3', '#BA3D4D'),
            limitCat=7,
        )

        # Create application layout
        self._createLayout()

        self.app.run_server(debug=debug, **kwargs)

    def _createLayout(self):
        """Create application layout."""
        self.app.layout = html.Div(
            className='section',
            children=[
                html.H4(children='Example Pareto Chart'),
                html.Div([
                    helpers.MinGraph(
                        id='pareto-chart',
                        figure=self.exPareto.createFigure(df=self.dfDemo),
                    ),
                ]),
            ],
        )


if __name__ == '__main__':
    ParetoDemo().run()
