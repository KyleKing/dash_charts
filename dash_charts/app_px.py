"""Generic Plotly Express Data Analysis App(s).

Examples: https://www.plotly.express/
Docs: https://www.plotly.express/plotly_express/

"""

from collections import OrderedDict

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.express as px

from .components import dropdown_group, opts_dd
from .utils_app import AppBase
from .utils_app_with_navigation import AppWithTabs
from .utils_callbacks import map_args, map_outputs
from .utils_fig import min_graph

# FIXME: Implement ability for user to select JSON or CSV data and graph interactively!
#   Require user to submit "Tidy" data with non-value headers

# # TODO: Show all data in code output
# px.data.election_geojson()  # Dict
# px.data.carshare().head()
# px.data.election().head()
# px.data.gapminder().head()
# px.data.iris().head()
# px.data.tips().head()
# px.data.wind().head()

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

    external_stylesheets = [dbc.themes.FLATLY]

    id_chart: str = 'chart'
    id_func: str = 'func'
    id_template: str = 'template'  # TODO: turn off template for the color swatch example

    takes_args: bool = True
    # TODO: Document
    templates: list = ['ggplot2', 'seaborn', 'simple_white', 'plotly',
                       'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
                       'ygridoff', 'gridon', 'none']
    """List of templates from: `import plotly.io as pio; pio.templates`"""

    # Must override in child class
    name: str = None
    # TODO: Document
    data: pd.DataFrame = None
    # TODO: Document
    func_map: OrderedDict = None
    # TODO: Document
    dims: tuple = ()  # FIXME: should be able to be None
    # TODO: Document
    dims_dict: OrderedDict = OrderedDict([])  # FIXME: should be able to be None
    # TODO: Document

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.input_ids = [self.id_func, self.id_template] + list(self.dims) + list(self.dims_dict.keys())
        self.register_uniq_ids([self.id_chart] + self.input_ids)

        self.col_opts = [] if self.data is None else tuple(opts_dd(_c, _c) for _c in self.data.columns)
        self.func_opts = tuple(opts_dd(lbl, lbl) for lbl in self.func_map.keys())
        self.t_opts = tuple(opts_dd(template, template) for template in self.templates)

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements."""
        pass

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        Raises:
            RuntimeError: if any class data member is not the expected type

        """
        errors = []
        if not isinstance(self.name, str):
            errors.append(f'Expected self.name="{self.name}" to be str')
        if not isinstance(self.dims, tuple):
            errors.append(f'Expected self.dims="{self.dims}" to be tuple')
        if not isinstance(self.dims_dict, OrderedDict):
            errors.append(f'Expected self.dims_dict="{self.dims_dict}" to be OrderedDict')
        if len(errors):
            formatted_errors = '\n' + '\n'.join(errors)
            raise RuntimeError(f'Found errors in data members:{formatted_errors}')

        return html.Div([
            html.Div([
                dropdown_group('Plot Type:', self.ids[self.id_func], self.func_opts, value=self.func_opts[0]['label']),
                dropdown_group('Template:', self.ids[self.id_template], self.t_opts, value=self.t_opts[0]['label']),
            ] + [
                dropdown_group(f'{dim}:', self.ids[dim], self.col_opts)
                for dim in self.dims
            ] + [
                dropdown_group(f'{dim}:', self.ids[dim], [opts_dd(item, item) for item in items])
                for dim, items in self.dims_dict.items()
            ], style={'width': '25%', 'float': 'left'}),
            min_graph(id=self.ids[self.id_chart], style={'width': '75%', 'display': 'inline-block'}),
        ], style={'padding': '15px'})

    def create_callbacks(self):
        """Register callbacks necessary for this tab."""
        errors = []
        if not isinstance(self.takes_args, bool):
            errors.append(f'Expected self.takes_args="{self.takes_args}" to be bool')
        if not (isinstance(self.data, pd.DataFrame) or self.data is None):
            errors.append(f'Expected self.data="{self.data}" to be pd.DataFrame or None')
        if not isinstance(self.func_map, OrderedDict):
            errors.append(f'Expected self.func_map="{self.func_map}" to be OrderedDict')
        if len(errors):
            formatted_errors = '\n' + '\n'.join(errors)
            raise RuntimeError(f'Found errors in data members:{formatted_errors}')

        outputs = [(self.id_chart, 'figure')]
        inputs = [(_id, 'value') for _id in self.input_ids]
        states = ()
        @self.callback(outputs, inputs, states)
        def update_chart(*raw_args):
            a_in, _a_states = map_args(raw_args, inputs, states)
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


class InteractivePXApp(AppWithTabs):
    """Plotly Express Demo application."""

    name = 'TabAppDemo'

    tabs_location = 'right'
    """Tab orientation setting. One of `(left, top, bottom, right)`."""

    tabs_margin = '175px'
    """Adjust this setting based on the width or height of the tabs to prevent the content from overlapping the tabs."""

    tabs_compact = False
    """Boolean setting to toggle between a padded tab layout if False and a minimal compact version if True."""

    def define_nav_elements(self):
        """Return list of initialized tabs.

        Returns:
            list: each item is an initialized tab (ex `[AppBase(self.app)]` in the order each tab is rendered

        """
        return [
            TabTip(app=self.app),
            TabIris(app=self.app),
            TabGapminder(app=self.app),
            TabTernary(app=self.app),
            TabPolar(app=self.app),
            TabColor(app=self.app),
        ]

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div([
            html.H1('Dash/Plotly Express Data Exploration Demo', style={'padding': '15px 0 0 15px'}),
            super().return_layout(),
        ])
