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
    """Return dcc.Graph element with Plotly overlay removed."""
    return dcc.Graph(config={'displayModeBar': False}, **kwargs)


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
    dimsDict = OrderedDict([])

    def __init__(self):
        """Resolve higher-order data members."""
        self.colOpts = tuple([ddOpts(_c, _c) for _c in self.data.columns])
        self.funcOpts = tuple([ddOpts(lbl, lbl) for idx, lbl in enumerate(self.funcMap.keys())])


class Tab1(TabBase):
    """Tab1 properties."""
    title = 'Tip Data'
    data = px.data.tips()
    funcMap = OrderedDict([
        ('scatter', px.scatter),
        ('density_contour', px.density_contour),
    ])
    dims = ('x', 'y', 'color', 'facet_row', 'facet_col')
    dimsDict = OrderedDict([
        ('marginal_x', ('histogram', 'rag', 'violin', 'box')),
        ('marginal_y', ('histogram', 'rag', 'violin', 'box')),
        ('trendline', ('ols', 'lowess')),
        # Consider: 'log_y'/'log_x' > daq.BooleanSwitch(id='{}-bool', on=False)
        # Won't work: error_x..., animation_frame/animation_group, category_orders, labels, etc.
    ])


class Tab2(TabBase):
    """Tab2 properties."""
    title = 'Iris Data'
    data = px.data.iris()
    funcMap = OrderedDict([
        ('scatter', px.scatter),
        ('histogram', px.histogram),
        ('density_contour', px.density_contour),
        ('strip', px.strip),
        ('box', px.box),
        ('violin', px.violin),
        ('scatter', px.scatter),
    ])
    dims = ('x', 'y', 'color', 'facet_col', 'facet_row')


class Tab3(TabBase):
    """Tab3 properties."""
    title = 'Gapminder Data'
    data = px.data.gapminder()
    funcMap = OrderedDict([
        ('line', px.line),
        ('area', px.area),
    ])
    dims = ('x', 'y', 'color', 'line_group', 'facet_row', 'facet_col')


class Tab4(TabBase):
    """Tab4 properties."""
    title = 'Ternary'
    data = px.data.election()
    funcMap = OrderedDict([
        ('scatter_ternary', px.scatter_ternary),
        ('line_ternary', px.line_ternary),
    ])
    dims = ('a', 'b', 'c', 'color', 'size')


class Tab5(TabBase):
    """Tab5 properties."""
    title = 'Polar'
    data = px.data.wind()
    funcMap = OrderedDict([
        ('scatter_polar', px.scatter_polar),
        ('line_polar', px.line_polar),  # (line_close=True)
    ])
    dims = ('r', 'theta', 'color')


class Tab6(TabBase):
    """Tab6 properties."""
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


TABS = [Tab1(), Tab2(), Tab3(), Tab4(), Tab5(), Tab6()]
TAB_LOOKUP = {_tab.title: _tab for _tab in TABS}

# ======================================================================================================================
# Declare the layout and callbacks
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Suppress callback verification because the tab content won't be rendered to check the graph callbacks
app.config['suppress_callback_exceptions'] = True

# Create layout, then individual tabs
app.layout = html.Div([
    html.H1('Dash/Plotly Express Data Exploration Demo'),
    dcc.Tabs(id='tabs-select', value=TABS[0].title, children=[
        dcc.Tab(label=_tab.title, value=_tab.title) for _tab in TABS
    ], style={'margin-bottom': '15px'}),
    html.Div(id='tabs-content'),
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
            ]) for _d in _tab.dims
        ] + [
            html.P([
                _d + ':', dcc.Dropdown(id='{}-{}'.format(_tab.title, _d), options=[ddOpts(_l, _l) for _l in _list])
            ]) for _d, _list in _tab.dimsDict.items()
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
    inputs.extend([Input('{}-{}'.format(_tab.title, _k), 'value') for _k in _tab.dimsDict.keys()])

    @app.callback(
        Output('{}-graph'.format(_tab.title), 'figure'),
        inputs,
    )
    def renderFigure(tabName, nameFunc, *args):
        """Create the figure."""
        # Check if the trigger event is a tab change. If so, return an empty chart
        triggeredIDs = [_t['prop_id'] for _t in dash.callback_context.triggered]
        ic(triggeredIDs)
        if 'tabs-select.value' in triggeredIDs:
            return {}
        # Otherwise, parse the arguments to generate a new plot
        tab = TAB_LOOKUP[tabName]
        if tab.takesArgs:
            keys = list(tab.dims) + list(tab.dimsDict.keys())
            kwargs = OrderedDict(zip(keys, args))
            ic(kwargs)
            ic(tab.data.head(2))
            return tab.funcMap[nameFunc](tab.data, height=650, **kwargs)
        return tab.funcMap[nameFunc]()


if __name__ == '__main__':
    app.run_server(debug=True)
