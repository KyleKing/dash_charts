"""Main Helper Functions."""

import dash
from pathlib import Path
import dash_core_components as dcc
import plotly.graph_objs as go

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

        self.range = {}

    def createFigure(self, df, **kwargsData):
        """Create the figure dictionary.

        data -- data to pass to formatter method
        kwargsData -- keyword arguments to pass to the data formatter method

        """
        return {
            'data': self.formatData(df, **kwargsData),
            'layout': go.Layout(self.applyCustomlayoutParams(self.createLayout())),
        }

    def formatData(self, df, **kwargsData):
        """Return formatted data for data key of figure."""
        raise NotImplementedError('formatData must be implemented by child class')

    def createLayout(self):
        """Return the standard layout. Can be overridden and modified when inherited."""
        layout = dict(
            title=go.layout.Title(text=self.title),
            xaxis={
                'automargin': True,
                'showgrid': True,
                'title': self.labels['x'],
            },
            yaxis={
                'automargin': True,
                'showgrid': True,
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
