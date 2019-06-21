"""Example using Plotly Express with tabbed interface.

Examples: https://www.plotly.express/
Docs: https://www.plotly.express/plotly_express/

"""

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly_express as px
from _config import app
from dash.dependencies import Input, Output
from dash_charts.helpers import MinGraph
from icecream import ic
from collections import OrderedDict

# ======================================================================================================================
# Demo uses sample data. User should replace with data loaded from a static CSV file, TinyDB, SQLite, etc.

# Create classes to manage tabs state. Easy to scale up or down


def ddOpts(lbl, val):
    """Return the formatted dictionary for a dcc.Dropdown element."""
    return {'label': lbl, 'value': val}


class TabBase:
    """Base tab class with helper methods."""

    name = ''
    data = pd.DataFrame()
    funcMap = OrderedDict([])
    dims = tuple()

    def __init__(self):
        """Resolve higher-order data members."""
        self.colOpts = tuple([ddOpts(_c, _c) for _c in self.data.columns])
        self.funcOpts = tuple([ddOpts(lbl, lbl) for idx, lbl in enumerate(self.funcMap.keys())])


class Tab1(TabBase):
    """Tab1 properties."""
    name = 'Scatter-Style'
    data = px.data.tips()
    funcMap = OrderedDict([
        ('scatter', px.scatter),
        ('histogram', px.histogram),
        ('line', px.line),
        ('area', px.area),
        ('density_contour', px.density_contour),
        ('strip', px.strip),
        ('box', px.box),
        ('violin', px.violin),
    ])
    dims = ('x', 'y', 'color', 'size', 'facet_col', 'facet_row')


class Tab2(TabBase):
    """Tab2 properties."""
    name = 'Color Swatches'
    funcMap = OrderedDict([
        ('colors.qualitative', px.colors.qualitative.swatches),
        ('colors.sequential', px.colors.sequential.swatches),
        ('colors.diverging', px.colors.diverging.swatches),
        ('colors.cyclical', px.colors.cyclical.swatches),
        ('colors.colorbrewer', px.colors.colorbrewer.swatches),
        ('colors.cmocean', px.colors.cmocean.swatches),
        ('colors.carto', px.colors.carto.swatches),
    ])


TABS = [Tab1(), Tab2()]

# ======================================================================================================================
# Declare the layout and callbacks

# FIXME: Add tabs!
tab = TABS[0]
app.layout = html.Div([
    html.H1('Dash/Plotly Express Data Exploration Demo'),
    html.Div(
        [html.P([
            'Plot Type:',
            dcc.Dropdown(id='{}-func'.format(tab.name), options=tab.funcOpts, value=tab.funcOpts[0]['label']),
        ])] + [html.P([
            _d + ':', dcc.Dropdown(id='{}-{}'.format(tab.name, _d), options=tab.colOpts)
        ]) for idx, _d in enumerate(tab.dims)],
        style={'width': '25%', 'float': 'left'},
    ),
    MinGraph(id='{}-graph'.format(tab.name), style={'width': '75%', 'display': 'inline-block'}),
])

# Register callbacks for each tab
for tab in [TABS[0]]:
    inputs = [Input('{}-func'.format(tab.name), 'value')]
    inputs.extend([Input('{}-{}'.format(tab.name, _d), 'value') for _d in tab.dims])

    @app.callback(Output('{}-graph'.format(tab.name), 'figure'), inputs)
    def make_figure(func, *args):
        """Create the express figure."""
        # Return the figure from plotly express
        kwargs = dict(zip(tab.dims, args))
        return tab.funcMap[func](tab.data, height=700, **kwargs)


if __name__ == '__main__':
    app.run_server(debug=True)
