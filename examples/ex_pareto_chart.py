"""Example Pareto Chart."""

from pathlib import Path

from icecream import ic
import dash_html_components as html
import pandas as pd
from dash_charts import helpers
from dash_charts.pareto_chart import ParetoChart


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
        df = pd.read_csv(Path(__file__).parent / 'DowntimeData.csv')
        # Example looping raw data to create the data/label dataframe expected by ParetoChart()
        self.dfPareto = None
        for cat in df['categories'].unique():
            downtime = df.loc[df['categories'] == cat]['downtime'].sum()
            dfRow = pd.DataFrame(data={'value': [downtime], 'label': [cat]})
            self.dfPareto = dfRow if self.dfPareto is None else self.dfPareto.append(dfRow)
        ic(self.dfPareto)

    def _createLayout(self):
        """Create application layout."""
        self.app.layout = html.Div(
            className='section',
            children=[
                html.H4(children='Example Pareto Chart'),
                html.Div([
                    helpers.MinGraph(
                        id='pareto-chart',
                        figure=self.exPareto.createFigure(df=self.dfPareto),
                    ),
                ]),
            ],
        )


if __name__ == '__main__':
    ParetoDemo().run()
