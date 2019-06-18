"""Main Helper Functions."""

import plotly.graph_objs as go


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

    def __init__(self, title='', xLbl='', yLbl=''):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        xLbl/yLbl -- optional, X- and Y-Axis axis labels. Defaults to blank

        """
        # Store kwargs as data members
        self.title = title
        self.labels = {'x': xLbl, 'y': yLbl}

        self.range = {}

    def createFigure(self, data, **kwargsData):
        """Create the figure dictionary.

        data -- data to pass to formatter method
        kwargsData -- keyword arguments to pass to the data formatter method

        """
        return{
            'data': self.formatData(data, **kwargsData),
            'layout': go.Layout(self.createLayout()),
        }

    def createLayout(self):
        """Return the standard layout. Can be overridden and modified when inherited."""
        layout = dict(
            title=go.layout.Title(text=self.title),
            xaxis={
                'title': self.labels['x'],
            },
            yaxis={
                'title': self.labels['y'],
            },
            legend=dict(orientation='h'),
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
