"""Example Alignment Chart."""

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from dash_charts import helpers
from dash_charts.alignment_chart import AlignChart


class AlignmentDemo:
    """Demo Simple Rolling Mean Chart."""

    def __init__(self):
        """Initialize app."""
        self.app = helpers.initApp()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        self.exAlign = AlignChart(
            title='Positioning Error Analysis',
            xLbl='X-Axis Measurements (µm)',
            yLbl='Y-Axis Measurements (µm)',
            customLayoutParams=(
                ('height', None, 650),
                ('width', None, 750),
            ),
            measLbl='Positioning Error',
            idealLbl='Expected Position',
            pad=0.75,
        )

        # Create sample data and application layout
        self._generateData()
        self._createLayout()

        self._registerCallbacks()

        self.app.run_server(debug=debug, **kwargs)

    def _generateData(self):
        """Create self.dfDemo with sample data."""
        # Generate a grid of initial points
        dim = 5
        count = pow(dim, 2)
        grid = np.meshgrid(*([np.linspace(1, dim, dim)] * 2))

        # Combine into a dataframe
        self.dfDemo = pd.DataFrame(data={
            'x': grid[0].flatten(),
            'y': grid[1].flatten(),
            'xDelta': np.random.randn(count) / 12,
            'yDelta': np.random.randn(count) / 8,
            'label': ['Point {}'.format(idx) for idx in range(count)],
        })

    def _createLayout(self):
        """Create application layout."""
        self.app.layout = html.Div(className='section', style={
            'max-width': '800px',
            'margin-right': 'auto',
            'margin-left': 'auto',
        }, children=[
            html.Div([helpers.MinGraph(id='alignment-chart')]),
            html.Div(style={
                'max-width': '400px',
                'margin-right': 'auto',
                'margin-left': 'auto',
            }, children=[
                html.Div(id='slider-output-container'),
                dcc.Slider(id='stretch-input', min=0, max=20, step=0.1, value=5),
                html.Button('Reset to 1', id='reset-button', className='button is-primary'),
            ]),
        ])

    def _registerCallbacks(self):
        """Register callbacks to handle user interaction."""
        @self.app.callback(
            Output('alignment-chart', 'figure'),
            [Input('stretch-input', 'value')])
        def updateAlignChart(stretch):
            """Create/update the alignment chart with the user-configurable stretch input."""
            return self.exAlign.createFigure(df=self.dfDemo, stretch=stretch)

        @self.app.callback(
            Output('slider-output-container', 'children'),
            [Input('stretch-input', 'value')])
        def indicateSliderPos(stretch):
            """Add text describing the current slider value."""
            return 'Selected stretch factor: `{}`'.format(stretch)

        @self.app.callback(
            Output('stretch-input', 'value'),
            [Input('reset-button', 'n_clicks')])
        def resetstretch(n_clicks):
            """Button to reset the stretch factor."""
            return 1


if __name__ == '__main__':
    AlignmentDemo().run()
