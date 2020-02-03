"""Main Helper Functions."""

from pathlib import Path

import dash
import dash_core_components as dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ASSETS_DIR = Path(__file__).parent / 'assets'


def init_app(**kwargs):
    """Return new Dash app with `assets_folder` set to local assets.

    Args:
        kwargs: any kwargs to pass to the dash initializer other than `assets_folder`

    Returns:
        dash.Dash() instance (i.e. APP)

    """
    return dash.Dash(__name__, assets_folder=str(ASSETS_DIR), **kwargs)


def min_graph(**kwargs):
    """Return dcc.Graph element with Plotly overlay removed.

    See: https://community.plot.ly/t/is-it-possible-to-hide-the-floating-toolbar/4911/7

    Args:
        kwargs: any kwargs to pass to the dash initializer other than `assets_folder`

    Returns:
        dcc.Graph object

    """
    return dcc.Graph(
        config={
            'displayModeBar': False,
            # 'modeBarButtonsToRemove': ['sendDataToCloud'],
        },
        **kwargs,
    )


def opts_dd(lbl, val):
    """Format an individual item in a dropdown list. Return the dictionary.

    lbl -- Dropdown label
    val -- Dropdown value (will be converted to JSON)

    """
    return {'label': str(lbl), 'value': val}


# TODO: Unused - should re-examine if this could create problems with modified state
class ChartState:
    """Configurable Chart."""

    def __init__(self, chart_func, **kwargs_def):
        """Store parameters.

        chart_func -- callback to create the figure object
        kwargs_def -- default keyword arguments passed to chart function

        """
        self.kwargs_def = kwargs_def
        self.chart_func = chart_func

    def figure(self, **kwargsNew):
        """Return the Dash figure dictionary.

        kwargsNew -- new keyword arguments to pass to the chart function

        """
        return self.chart_func(**kwargsNew, **self.kwargs_def)


class CustomChart:
    """Base Class for Custom Charts."""

    def __init__(self, title='', x_label='', y_label='', cust_layout_params=()):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        x_label/y_label -- optional, X- and Y-Axis axis labels. Defaults to an empty string (blank)
        cust_layout_params -- Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'

        """
        # Store kwargs as data members
        self.title = title
        self.labels = {'x': x_label, 'y': y_label}
        self.cust_layout_params = cust_layout_params
        self.annotations = None

        self.range = {}

    def create_figure(self, df, **kwargs_data):
        """Create the figure dictionary.

        df -- data to pass to formatter method
        kwargs_data -- keyword arguments to pass to the data formatter method

        """
        return {
            'data': self.create_traces(df, **kwargs_data),
            'layout': go.Layout(self.apply_cust_layout(self.create_layout())),
        }

    def create_traces(self, df, **kwargs_data):
        """Return traces for plotly chart."""
        raise NotImplementedError('create_traces must be implemented by child class')

    def create_layout(self):
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
            axis_name = '{}axis'.format(axis)
            if axis in self.range:
                layout[axis_name]['range'] = self.range[axis]
            else:
                layout[axis_name]['autorange'] = True

        return layout

    def apply_cust_layout(self, layout):
        """Apply/override layout with custom layout parameters.

        layout -- layout dictionary from self.create_layout()

        """
        for parent_key, sub_key, val in self.cust_layout_params:
            if sub_key is not None:
                layout[parent_key][sub_key] = val
            else:
                layout[parent_key] = val

        return layout


class MarginalChart(CustomChart):
    """Base Class for Custom Charts with Marginal X and Marginal Y Plots."""

    def create_figure(self, df, **kwargs_data):
        """Create the figure dictionary.

        data -- data to pass to formatter method
        kwargs_data -- keyword arguments to pass to the data formatter method

        """
        fig = make_subplots(
            rows=2, cols=2,
            shared_xaxes=True, shared_yaxes=True,
            vertical_spacing=0.02, horizontal_spacing=0.02,
            row_width=[0.8, 0.2], column_width=[0.8, 0.2],
        )
        traces = [
            (self.create_traces, 2, 1), (self.create_marg_top, 1, 1), (self.create_marg_right, 2, 2),
        ]
        for trace_func, row, col in traces:
            for trace in trace_func(df, **kwargs_data):
                fig.add_trace(trace, row, col)
        # Apply axis labels
        fig.update_xaxes(title_text=self.labels['x'], row=2, col=1)
        fig.update_yaxes(title_text=self.labels['y'], row=2, col=1)
        # Replace the default blue/white grid introduced in Plotly v4
        fig.update_xaxes(showgrid=True, gridcolor='white')
        fig.update_yaxes(showgrid=True, gridcolor='white')
        fig['layout'].update(self.apply_cust_layout(self.create_layout()))
        return fig

    def create_traces(self, df, **kwargs_data):
        """Return traces for plotly chart."""
        return []

    def create_marg_top(self, df, **kwargs_data):
        """Return traces for the top marginal chart."""
        return []

    def create_marg_right(self, df, **kwargs_data):
        """Return traces for the right marginal chart."""
        return []

    def create_layout(self):
        """Override the default layout and add additional settings."""
        layout = super().create_layout()
        # Remove axis lables from layout as they would be applied to row=1,col=1
        layout['xaxis']['title'] = ''
        layout['yaxis']['title'] = ''
        layout['plot_bgcolor'] = '#F0F0F0'
        return layout
