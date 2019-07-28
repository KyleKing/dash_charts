"""Main Helper Functions."""

from pathlib import Path

import dash
import dash_core_components as dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ASSETS_DIR = Path(__file__).parent / 'assets'


def initApp(**kwargs):
    """Return new Dash app with `assets_folder` set to local assets.

    kwargs -- any kwargs to pass to the dash initializer

    """
    return dash.Dash(__name__, assets_folder=str(ASSETS_DIR), **kwargs)


def MinGraph(**kwargs):
    """Return dcc.Graph element with Plotly overlay removed.

    See: https://community.plot.ly/t/is-it-possible-to-hide-the-floating-toolbar/4911/7

    """
    return dcc.Graph(
        config={
            'displayModeBar': False,
            # 'modeBarButtonsToRemove': ['sendDataToCloud'],
        },
        **kwargs,
    )


def ddOpts(lbl, val):
    """Format an individual item in a dropdown list. Return the dictionary.

    lbl -- Dropdown label
    val -- Dropdown value (will be converted to JSON)

    """
    return {'label': str(lbl), 'value': val}


class ChartState:
    """Configurable Chart."""

    def __init__(self, chartFunc, **kwargsDef):
        """Store parameters.

        chartFunc -- callback to create the figure object
        kwargsDef -- default keyword arguments passed to chart function

        """
        self.kwargsDef = kwargsDef
        self.chartFunc = chartFunc

    def figure(self, **kwargsNew):
        """Return the Dash figure dictionary.

        kwargsNew -- new keyword arguments to pass to the chart function

        """
        return self.chartFunc(**kwargsNew, **self.kwargsDef)


class CustomChart:
    """Base Class for Custom Charts."""

    def __init__(self, title='', xLbl='', yLbl='', customLayoutParams=()):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        xLbl/yLbl -- optional, X- and Y-Axis axis labels. Defaults to blank
        customLayoutParams -- Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'

        """
        # Store kwargs as data members
        self.title = title
        self.labels = {'x': xLbl, 'y': yLbl}
        self.customLayoutParams = customLayoutParams
        self.annotations = None

        self.range = {}

    def createFigure(self, df, **kwargsData):
        """Create the figure dictionary.

        df -- data to pass to formatter method
        kwargsData -- keyword arguments to pass to the data formatter method

        """
        return {
            'data': self.createTraces(df, **kwargsData),
            'layout': go.Layout(self.applyCustomlayoutParams(self.createLayout())),
        }

    def createTraces(self, df, **kwargsData):
        """Return traces for plotly chart."""
        raise NotImplementedError('createTraces must be implemented by child class')

    def createLayout(self):
        """Return the standard layout. Can be overridden and modified when inherited."""
        layout = dict(
            title=go.layout.Title(text=self.title),
            xaxis={
                'automargin': True,
                'title': self.labels['x'],
            },
            yaxis={
                'automargin': True,
                'title': self.labels['y'],
                'zeroline': True,
            },
            legend={'orientation': 'h'},
            hovermode='closest',
        )

        # Optionally apply the specified range
        for axis in ['x', 'y']:
            axisName = '{}axis'.format(axis)
            if axis in self.range:
                layout[axisName]['range'] = self.range[axis]
            else:
                layout[axisName]['autorange'] = True

        return layout

    def applyCustomlayoutParams(self, layout):
        """Apply/override layout with custom layout parameters.

        layout -- layout dictionary from self.createLayout()

        """
        for parentKey, subKey, val in self.customLayoutParams:
            if subKey is not None:
                layout[parentKey][subKey] = val
            else:
                layout[parentKey] = val

        return layout


class MarginalChart(CustomChart):
    """Base Class for Custom Charts with Marginal X and Marginal Y Plots."""

    def createFigure(self, df, **kwargsData):
        """Create the figure dictionary.

        data -- data to pass to formatter method
        kwargsData -- keyword arguments to pass to the data formatter method

        """
        fig = make_subplots(
            rows=2, cols=2,
            shared_xaxes=True, shared_yaxes=True,
            vertical_spacing=0.02, horizontal_spacing=0.02,
            row_width=[0.8, 0.2], column_width=[0.8, 0.2],
        )
        traces = [
            (self.createTraces, 2, 1), (self.createMargTop, 1, 1), (self.createMargRight, 2, 2),
        ]
        for traceFunc, row, col in traces:
            for trace in traceFunc(df, **kwargsData):
                fig.add_trace(trace, row, col)
        # Apply axis labels
        fig.update_xaxes(title_text=self.labels['x'], row=2, col=1)
        fig.update_yaxes(title_text=self.labels['y'], row=2, col=1)
        # Replace the default blue/white grid introduced in Plotly v4
        fig.update_xaxes(showgrid=True, gridcolor='white')
        fig.update_yaxes(showgrid=True, gridcolor='white')
        fig['layout'].update(self.applyCustomlayoutParams(self.createLayout()))
        return fig

    def createTraces(self, df, **kwargsData):
        """Return traces for plotly chart."""
        return []

    def createMargTop(self, df, **kwargsData):
        """Return traces for the top marginal chart."""
        return []

    def createMargRight(self, df, **kwargsData):
        """Return traces for the right marginal chart."""
        return []

    def createLayout(self):
        """Override the default layout and add additional settings."""
        layout = super().createLayout()
        # Remove axis lables from layout as they would be applied to row=1,col=1
        layout['xaxis']['title'] = ''
        layout['yaxis']['title'] = ''
        layout['plot_bgcolor'] = '#F0F0F0'
        return layout
