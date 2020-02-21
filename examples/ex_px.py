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
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.utils_app import STATIC_URLS, AppBase, AppWithTabs, init_app, opts_dd
from dash_charts.utils_fig import map_args, map_outputs, min_graph

# FIXME: Implement ability for user to select JSON or CSV data and graph interactively!

# All Chart - TODO: Make sure all these charts are in example
# scatter([data_frame, x, y, color, symbol, …])
#    In a scatter plot, each row of data_frame is represented by a symbol
# scatter_3d([data_frame, x, y, z, color, …])
#    In a 3D scatter plot, each row of data_frame is represented by a
# scatter_polar([data_frame, r, theta, color, …])
#    In a polar scatter plot, each row of data_frame is represented by a
# scatter_ternary([data_frame, a, b, c, …])
#    In a ternary scatter plot, each row of data_frame is represented by a
# scatter_mapbox([data_frame, lat, lon, …])
#    In a Mapbox scatter plot, each row of data_frame is represented by a
# scatter_geo([data_frame, lat, lon, …])
#    In a geographic scatter plot, each row of data_frame is represented
#
# line([data_frame, x, y, line_group, color, …])
#    In a 2D line plot, each row of data_frame is represented as vertex of
# line_3d([data_frame, x, y, z, color, …])
#    In a 3D line plot, each row of data_frame is represented as vertex of
# line_polar([data_frame, r, theta, color, …])
#    In a polar line plot, each row of data_frame is represented as vertex
# line_ternary([data_frame, a, b, c, color, …])
#    In a ternary line plot, each row of data_frame is represented as
# line_mapbox([data_frame, lat, lon, color, …])
#    In a Mapbox line plot, each row of data_frame is represented as
# line_geo([data_frame, lat, lon, locations, …])
#    In a geographic line plot, each row of data_frame is represented as
#
# area([data_frame, x, y, line_group, color, …])
#    In a stacked area plot, each row of data_frame is represented as
#
# bar([data_frame, x, y, color, facet_row, …])
#    In a bar plot, each row of data_frame is represented as a rectangular
# bar_polar([data_frame, r, theta, color, …])
#    In a polar bar plot, each row of data_frame is represented as a wedge
#
# violin([data_frame, x, y, color, facet_row, …])
#    In a violin plot, rows of data_frame are grouped together into a
# box([data_frame, x, y, color, facet_row, …])
#    In a box plot, rows of data_frame are grouped together into a
# strip([data_frame, x, y, color, facet_row, …])
#    In a strip plot each row of data_frame is represented as a jittered
# histogram([data_frame, x, y, color, …])
#    In a histogram, rows of data_frame are grouped together into a
# pie([data_frame, names, values, color, …])
#    In a pie plot, each row of data_frame is represented as a sector of a
# treemap([data_frame, names, values, …])
#    A treemap plot represents hierarchial data as nested rectangular
# sunburst([data_frame, names, values, …])
#    A sunburst plot represents hierarchial data as sectors laid out over
# funnel([data_frame, x, y, color, facet_row, …])
#    In a funnel plot, each row of data_frame is represented as a
# funnel_area([data_frame, names, values, …])
#    In a funnel area plot, each row of data_frame is represented as a
# scatter_matrix([data_frame, dimensions, …])
#    In a scatter plot matrix (or SPLOM), each row of data_frame is
#
# parallel_coordinates([data_frame, …])
#    In a parallel coordinates plot, each row of data_frame is represented
# parallel_categories([data_frame, …])
#    In a parallel categories (or parallel sets) plot, each row of
#
# choropleth([data_frame, lat, lon, …])
#    In a choropleth map, each row of data_frame is represented by a
# choropleth_mapbox([data_frame, geojson, …])
#    In a Mapbox choropleth map, each row of data_frame is represented by a
#
# density_contour([data_frame, x, y, z, …])
#    In a density contour plot, rows of data_frame are grouped together
# density_heatmap([data_frame, x, y, z, …])
#    In a density heatmap, rows of data_frame are grouped together into
# density_mapbox([data_frame, lat, lon, z, …])
#    In a Mapbox density map, each row of data_frame contributes to the intensity of
#
# imshow(img[, zmin, zmax, origin, …])
#    Display an image, i.e.


# ======================================================================================================================
# Create classes to manage tabs state. Easy to scale up or down
# >> Demo uses sample data. User could replace with data loaded from a static CSV file, TinyDB, SQLite, etc.


class TabBase(AppBase):
    """Base tab class with helper methods."""

    id_chart = 'chart'
    id_func = 'func'
    id_template = 'template'  # TODO: turn off template for the color swatch example

    takes_args: bool = True
    templates = ['ggplot2', 'seaborn', 'simple_white', 'plotly',
                 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
                 'ygridoff', 'gridon', 'none']  # import plotly.io as pio; pio.templates

    # Must override in child class
    name: str = None
    data: pd.DataFrame = None
    func_map: OrderedDict = None
    dims: tuple = ()  # FIXME: should be able to be None
    dims_dict: OrderedDict = OrderedDict([])  # FIXME: should be able to be None

    def __init__(self, *dash_args, **dash_kwargs):
        """Resolve higher-order data members."""
        super().__init__(*dash_args, **dash_kwargs)

        self.col_opts = [] if self.data is None else tuple(opts_dd(_c, _c) for _c in self.data.columns)
        self.func_opts = tuple(opts_dd(lbl, lbl) for lbl in self.func_map.keys())
        self.t_opts = tuple(opts_dd(template, template) for template in self.templates)

        self.input_ids = [self.id_func, self.id_template] + list(self.dims) + list(self.dims_dict.keys())
        self.register_uniq_ids([self.id_chart] + self.input_ids)

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        assert isinstance(self.name, str)
        assert isinstance(self.dims, tuple)
        assert isinstance(self.dims_dict, OrderedDict)
        return html.Div([
            html.Div([
                html.P([
                    'Plot Type:',
                    dcc.Dropdown(id=self.ids[self.id_func], options=self.func_opts, value=self.func_opts[0]['label']),
                ]),
            ] + [
                html.P([
                    'Template:',
                    dcc.Dropdown(id=self.ids[self.id_template], options=self.t_opts, value=self.t_opts[0]['label']),
                ]),
            ] + [
                html.P([dim + ':', dcc.Dropdown(id=self.ids[dim], options=self.col_opts)])
                for dim in self.dims
            ] + [
                html.P([dim + ':', dcc.Dropdown(id=self.ids[dim], options=[opts_dd(item, item) for item in items])])
                for dim, items in self.dims_dict.items()
            ], style={'width': '25%', 'float': 'left'}),
            min_graph(id=self.ids[self.id_chart], style={'width': '75%', 'display': 'inline-block'}),
        ], style={'padding': '15px'})

    def register_charts(self):
        """Register the initial charts."""
        pass

    def register_callbacks(self):
        """Register callbacks necessary for this tab."""
        assert isinstance(self.takes_args, bool)
        assert isinstance(self.data, pd.DataFrame) or self.data is None, 'Data can be None...'
        assert isinstance(self.func_map, OrderedDict)

        outputs = ((self.id_chart, 'figure'), )
        inputs = [(_id, 'value') for _id in self.input_ids]
        states = ()
        @self.callback(outputs, inputs, states)
        def update_chart(*args):
            a_in, _a_states = map_args(args, inputs, states)
            name_func = a_in[self.id_func]['value']

            properties = [trigger['prop_id'] for trigger in dash.callback_context.triggered]
            new_chart = {}
            # If event is not a tab change, return the updated chart
            if 'tabs-select.value' not in properties:  # FIXME: replace tabs-select with actual keyname
                if self.takes_args:
                    # Parse the arguments to generate a new plot
                    kwargs = {key: a_in[key]['value'] for key in self.input_ids[1:]}
                    new_chart = self.func_map[name_func](self.data, height=650, **kwargs)
                else:
                    new_chart = self.func_map[name_func]()
            # Example Mapping Output. Alternatively, just: `return [new_chart]`
            return map_outputs(outputs, [(self.id_chart, 'figure', new_chart)])


class TabTip(TabBase):
    """TabTip properties."""

    name = 'Tip Data'
    data = px.data.tips()
    func_map = OrderedDict([
        ('scatter', px.scatter),
        ('density_contour', px.density_contour),
    ])
    dims = ('x', 'y', 'color', 'facet_row', 'facet_col')
    dims_dict = OrderedDict([
        ('marginal_x', ('histogram', 'rag', 'violin', 'box')),
        ('marginal_y', ('histogram', 'rag', 'violin', 'box')),
        ('trendline', ('ols', 'lowess')),
        # Consider: 'log_y'/'log_x' > daq.BooleanSwitch(id='{}-bool', on=False)
        # Won't work: error_x..., animation_frame/animation_group, category_orders, labels, etc.
    ])


class TabIris(TabBase):
    """TabIris properties."""

    name = 'Iris Data'
    data = px.data.iris()
    func_map = OrderedDict([
        ('histogram', px.histogram),
        ('density_contour', px.density_contour),
        ('strip', px.strip),
        ('box', px.box),
        ('violin', px.violin),
        ('scatter', px.scatter),
    ])
    dims = ('x', 'y', 'color', 'facet_col', 'facet_row')


class TabGapminder(TabBase):
    """TabGapminder properties."""

    name = 'Gapminder Data'
    data = px.data.gapminder()
    func_map = OrderedDict([
        ('area', px.area),
    ])
    dims = ('x', 'y', 'color', 'line_group', 'facet_row', 'facet_col')


class TabTernary(TabBase):
    """TabTernary properties."""

    name = 'Ternary'
    data = px.data.election()
    func_map = OrderedDict([
        ('scatter_ternary', px.scatter_ternary),
        ('line_ternary', px.line_ternary),
    ])
    dims = ('a', 'b', 'c', 'color', 'size')


class TabPolar(TabBase):
    """TabPolar properties."""

    name = 'Polar'
    data = px.data.wind()
    func_map = OrderedDict([
        ('scatter_polar', px.scatter_polar),
        ('line_polar', px.line_polar),  # (line_close=True)
    ])
    dims = ('r', 'theta', 'color')


class TabColor(TabBase):
    """TabColor properties."""

    name = 'Color Swatches'
    takes_args = False
    func_map = OrderedDict([
        ('colors.qualitative', px.colors.qualitative.swatches),
        ('colors.sequential', px.colors.sequential.swatches),
        ('colors.diverging', px.colors.diverging.swatches),
        ('colors.cyclical', px.colors.cyclical.swatches),
        ('colors.colorbrewer', px.colors.colorbrewer.swatches),
        ('colors.cmocean', px.colors.cmocean.swatches),
        ('colors.carto', px.colors.carto.swatches),
    ])

# ======================================================================================================================
# Create class for application to control manage variable scopes


class PXDemoApp(AppWithTabs):
    """Plotly Express Demo application."""

    name = 'TabAppDemo'

    tabs_location = 'right'
    """Tab orientation setting. One of `(left, top, bottom, right)`."""

    tabs_margin = '175px'
    """Adjust this setting based on the width or height of the tabs to prevent the content from overlapping the tabs."""

    tabs_compact = False
    """Boolean setting to toggle between a padded tab layout if False and a minimal compact version if True."""

    def __init__(self, **dash_kwargs):
        """Initialize app with custom stylesheets."""
        app = init_app(external_stylesheets=[STATIC_URLS[key] for key in ['dash']], **dash_kwargs)
        super().__init__(app=app)

    def define_tabs(self):
        """Return list of initialized tabs.

        Returns:
            list: each item is an initialized tab (ex `[AppBase(self.app)]` in the order each tab is rendered

        """
        return [
            TabTip(self.app),
            TabIris(self.app),
            TabGapminder(self.app),
            TabTernary(self.app),
            TabPolar(self.app),
            TabColor(self.app),
        ]

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div([
            html.H1('Dash/Plotly Express Data Exploration Demo', style={'padding': '15px 0 0 15px'}),
            super().return_layout()
        ])


if __name__ == '__main__':
    port = parse_cli_port()
    PXDemoApp().run(port=port, debug=True)
