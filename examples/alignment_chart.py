"""Example Alignment Chart."""

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from dash_charts.alignment_chart import AlignChart
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.utils_app import init_app
from dash_charts.utils_fig import min_graph


class AlignmentDemo:
    """Demo Simple Rolling Mean Chart."""

    def __init__(self):
        """Initialize app."""
        self.app = init_app()

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        self.exAlign = AlignChart(
            title='Positioning Error Analysis',
            x_label='X-Axis Measurements (µm)',
            y_label='Y-Axis Measurements (µm)',
            cust_layout_params=(
                ('height', None, 800),
                ('width', None, 1000),
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
        sTicks = range(0, 20 + 1, 2)
        # Create centered, 2-column layout
        self.app.layout = html.Div(className='columns', children=[
            html.Div(className='column', children=[
                html.Div([min_graph(id='alignment-chart')]),
            ]),
            html.Div(className='column', children=[
                html.Div(style={
                    'padding-top': '200px',
                    'max-width': '250px',
                }, children=[
                    html.Div(style={
                        'height': '400px',
                        'margin': '25px 0 25px 50px',
                    }, children=[
                        dcc.Slider(
                            id='stretch-input', step=0.1, vertical=True,
                            min=min(sTicks), max=max(sTicks), marks={idx: '{}'.format(idx) for idx in sTicks},
                        ),
                    ]),
                    html.Div(id='slider-output-container'),
                    html.Button('Reset to 1', id='reset-button', className='button is-primary'),
                ]),
            ]),
        ])

    def _registerCallbacks(self):
        """Register callbacks to handle user interaction."""
        @self.app.callback(
            Output('alignment-chart', 'figure'),
            [Input('stretch-input', 'value')])
        def updateAlignChart(stretch):
            """Create/update the alignment chart with the user-configurable stretch input."""
            return self.exAlign.create_figure(df=self.dfDemo, stretch=stretch)

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
    port = parse_cli_port()
    AlignmentDemo().run(port=port)
