"""Example using Plotly Express with tabbed interface.

Examples: https://www.plotly.express/
Docs: https://www.plotly.express/plotly_express/

"""

from collections import OrderedDict

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly_express as px
from dash.dependencies import Input, Output
from icecream import ic  # noqa: F401

# ======================================================================================================================
# (Helper Functions)


def ddOpts(lbl, val):
    """Return the formatted dictionary for a dcc.Dropdown element."""
    return {'label': str(lbl), 'value': str(val)}


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


# ======================================================================================================================
# Create classes to manage tabs state. Easy to scale up or down
# >> Demo uses sample data. User should replace with data loaded from a static CSV file, TinyDB, SQLite, etc.


class TabBase:
    """Base tab class with helper methods."""

    title = ''
    takesArgs = True
    data = pd.DataFrame()
    funcMap = OrderedDict([])
    dims = tuple()

    def __init__(self):
        """Resolve higher-order data members."""
        self.colOpts = tuple([ddOpts(_c, _c) for _c in self.data.columns])
        self.funcOpts = tuple([ddOpts(lbl, lbl) for idx, lbl in enumerate(self.funcMap.keys())])


class Tab1(TabBase):
    """Tab1 properties."""
    title = 'Scatter-Style'
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
    title = 'Color Swatches'
    takesArgs = False
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
TAB_LOOKUP = {_tab.title: _tab for _tab in TABS}

# ======================================================================================================================
# Declare the layout and callbacks
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Suppress callback verification because the tab content won't be rendered to check the graph callbacks
app.config['suppress_callback_exceptions'] = True

# Declare layout and each tab content
app.layout = html.Div([
    html.H1('Dash/Plotly Express Data Exploration Demo'),
    dcc.Tabs(id='tabs-select', value=TABS[0].title, children=[
        dcc.Tab(label=_tab.title, value=_tab.title) for _tab in TABS
    ], style={'margin-bottom': '15px'}),
    html.Div(id='tabs-content')
])
TAB_MAP = {
    _tab.title: html.Div([
        html.Div([
            html.P([
                'Plot Type:',
                dcc.Dropdown(
                    id='{}-func'.format(_tab.title), options=_tab.funcOpts, value=_tab.funcOpts[0]['label']
                ),
            ])
        ] + [
            html.P([
                _d + ':', dcc.Dropdown(id='{}-{}'.format(_tab.title, _d), options=_tab.colOpts)
            ]) for idx, _d in enumerate(_tab.dims)
        ], style={'width': '25%', 'float': 'left'},
        ),
        MinGraph(id='{}-graph'.format(_tab.title), style={'width': '75%', 'display': 'inline-block'}),
    ])
    for _tab in TABS
}


@app.callback(Output('tabs-content', 'children'), [Input('tabs-select', 'value')])
def renderTabs(tabName):
    """Render tabs when switched."""
    return TAB_MAP[tabName]


# Register callbacks for each tab
for _tab in TABS:
    inputs = [Input('tabs-select', 'value'), Input('{}-func'.format(_tab.title), 'value')]
    inputs.extend([Input('{}-{}'.format(_tab.title, _d), 'value') for _d in _tab.dims])

    @app.callback(Output('{}-graph'.format(_tab.title), 'figure'), inputs)
    def renderFigure(tabName, nameFunc, *args):
        """Create the express figure."""
        tab = TAB_LOOKUP[tabName]  # Read tab class from input
        # Suppress errors when switching tabs
        if nameFunc is None or nameFunc not in tab.funcMap:
            return {}
        # Return the figure based on the tab settings
        if tab.takesArgs:
            kwargs = dict(zip(tab.dims, args))
            return tab.funcMap[nameFunc](tab.data, height=650, **kwargs)
        return tab.funcMap[nameFunc]()


if __name__ == '__main__':
    app.run_server(debug=True)
