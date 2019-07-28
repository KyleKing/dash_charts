"""Example Pareto Chart."""

from pathlib import Path

import dash_html_components as html
import pandas as pd
from dash_charts import helpers
from dash_charts.pareto_chart import ParetoChart
from icecream import ic


class ParetoDemo:
    """Demo Simple Pareto Chart."""

    def __init__(self):
        """Initialize app."""
        self.app = helpers.initApp()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        # Initialize an example chart
        legend = dict(
            x=0.6,
            y=0.8,
            bgcolor='rgba(240, 240, 240, 0.49)',
        )
        self.exPareto = ParetoChart(
            title='Sample Pareto Chart',
            xLbl='Category Title',
            yLbl='Measured Downtime (hours)',
            customLayoutParams=(
                ('yaxis', 'dtick', 10),
                ('yaxis', 'tickformat', '.0f'),
                ('margin', None, {'l': 75, 'b': 100, 't': 50, 'r': 125}),
                ('height', None, 500),
                ('width', None, 750),
                ('showlegend', None, True),
                ('legend', None, legend),
            ),
        )

        # Create application layout
        self._generateData()
        self._createLayout()

        self.app.run_server(debug=debug, **kwargs)

    def _generateData(self):
        """Create self.dfPareto with sample data."""
        self.dfPareto = pd.read_csv(Path(__file__).parent / 'DowntimeData.csv')
        self.dfPareto = self.dfPareto.rename(columns={'downtime': 'value'})
        ic(self.dfPareto)

    def _createLayout(self):
        """Create application layout."""
        self.app.layout = html.Div(
            className='section', style={
                'max-width': '1000px',
                'margin-right': 'auto',
                'margin-left': 'auto',
            }, children=[
                html.H4(children='Example Pareto Chart'),
                html.Div([
                    helpers.MinGraph(
                        id='pareto-chart',
                        figure=self.exPareto.createFigure(df=self.dfPareto, showCount=True),
                    ),
                ]),
            ],
        )


if __name__ == '__main__':
    ParetoDemo().run()
