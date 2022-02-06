"""Generic Plotly Express Data Analysis App(s).

Examples: https://www.plotly.express/

Docs: https://www.plotly.express/plotly_express/

# (Currently) Unsupported plotly express types

```py
px.parallel_coordinates(px.data.iris(), color="species_id",
                        dimensions=['sepal_width', 'sepal_length', 'petal_width', 'petal_length'])
px.treemap(px.data.tips(), path=['day', 'time', 'sex'], values='total_bill')
px.sunburst(px.data.tips(), path=['day', 'time', 'sex'], values='total_bill)
```

Other charts that could be useful (but won't work with simple dropdowns)

- scatter_matrix([data_frame, dimensions, …])
    - In a scatter plot matrix (or SPLOM), each row of data_frame is
    - https://plotly.com/python/splom/
- parallel_coordinates([data_frame, …])
    - In a parallel coordinates plot, each row of data_frame is represented
    - https://plotly.com/python-api-reference/generated/plotly.express.parallel_coordinates.html
- parallel_categories([data_frame, …])
    - In a parallel categories (or parallel sets) plot, each row of
    - https://plotly.com/python-api-reference/generated/plotly.express.parallel_categories.html
- density_heatmap([data_frame, x, y, z, …])
    - In a density heatmap, rows of data_frame are grouped together into
    - https://plotly.com/python-api-reference/generated/plotly.express.density_heatmap.html
- imshow(img[, zmin, zmax, origin, …])
    - Display an image, i.e.
    - https://plotly.com/python/imshow/

"""

from collections import OrderedDict

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html
from implements import implements

from .components import dropdown_group, opts_dd
from .utils_app import AppBase, AppInterface
from .utils_app_with_navigation import FullScreenAppWithTabs
from .utils_callbacks import map_args, map_outputs
from .utils_fig import min_graph

# ======================================================================================================================
# Create classes to manage tabs state. Easy to scale up or down
# >> Demo uses sample data. User could replace with data loaded from a static CSV file, TinyDB, SQLite, etc.


@implements(AppInterface)  # noqa: H601
class TabBase(AppBase):
    """Base tab class with helper methods."""

    external_stylesheets = [dbc.themes.FLATLY]

    # ID Elements for UI
    id_chart: str = 'chart'
    id_func: str = 'func'
    id_template: str = 'template'  # PLANNED: template should be able to be None

    takes_args: bool = True
    """If True, will pass arguments from UI to function."""

    templates: list = [
        'ggplot2', 'seaborn', 'simple_white', 'plotly',
        'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
        'ygridoff', 'gridon', 'none',
    ]
    """List of templates from: `import plotly.io as pio; pio.templates`"""

    # Must override in child class
    name: str = None
    """Unique tab component name. Must be overridden in child class."""
    data: pd.DataFrame = None
    """Dataframe. Must be overridden in child class."""
    func_map: OrderedDict = None
    """Map of functions to keywords. Must be overridden in child class."""

    # PLANNED: below items should be able to be None
    dims: tuple = ()
    """Keyword from function for dropdowns with column names as options. Must be overridden in child class."""
    dims_dict: OrderedDict = OrderedDict([])
    """OrderedDict of keyword from function to allowed values. Must be overridden in child class."""
    default_dim_name = {}
    """Lookup for dim:column name to use as default in dropdown."""

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()

        # Register the the unique element IDs
        self.input_ids = [self.id_func, self.id_template] + [*self.dims] + [*self.dims_dict.keys()]
        self.register_uniq_ids([self.id_chart] + self.input_ids)

        # Configure the options for the various dropdowns
        self.col_opts = [] if self.data is None else tuple(opts_dd(_c, _c) for _c in self.data.columns)
        self.func_opts = tuple(opts_dd(lbl, lbl) for lbl in self.func_map.keys())
        self.t_opts = tuple(opts_dd(template, template) for template in self.templates)

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements."""
        ...

    def verify_types_for_layout(self):
        """Verify data types of data members necessary for the layout of this tab.

        Raises:
            RuntimeError: if any relevant data members are of the wrong type

        """
        errors = []
        if not isinstance(self.name, str):
            errors.append(f'Expected self.name="{self.name}" to be str')
        if not isinstance(self.dims, tuple):
            errors.append(f'Expected self.dims="{self.dims}" to be tuple')
        if not isinstance(self.dims_dict, OrderedDict):
            errors.append(f'Expected self.dims_dict="{self.dims_dict}" to be OrderedDict')
        if errors:
            formatted_errors = '\n' + '\n'.join(errors)
            raise RuntimeError(f'Found errors in data members:{formatted_errors}')

    def verify_types_for_callbacks(self):
        """Verify data types of data members necessary for the callbacks of this tab.

        Raises:
            RuntimeError: if any relevant data members are of the wrong type

        """
        errors = []
        if not isinstance(self.takes_args, bool):
            errors.append(f'Expected self.takes_args="{self.takes_args}" to be bool')
        if not (isinstance(self.data, pd.DataFrame) or self.data is None):
            errors.append(f'Expected self.data="{self.data}" to be pd.DataFrame or None')
        if not isinstance(self.func_map, OrderedDict):
            errors.append(f'Expected self.func_map="{self.func_map}" to be OrderedDict')
        if errors:
            formatted_errors = '\n' + '\n'.join(errors)
            raise RuntimeError(f'Found errors in data members:{formatted_errors}')

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        self.verify_types_for_layout()

        return html.Div(
            [  # noqa: ECE001
                html.Div(
                    [
                        dropdown_group(
                            'Plot Type:', self._il[self.id_func],
                            self.func_opts, value=self.func_opts[0]['label'],
                        ),
                        dropdown_group(
                            'Template:', self._il[self.id_template],
                            self.t_opts, value=self.t_opts[0]['label'],
                        ),
                    ] + [
                        dropdown_group(
                            f'{dim}:', self._il[dim], self.col_opts,
                            value=self.default_dim_name.get(dim, None),
                        )
                        for dim in self.dims
                    ] + [
                        dropdown_group(f'{dim}:', self._il[dim], [opts_dd(item, item) for item in items])
                        for dim, items in self.dims_dict.items()
                    ], style={'width': '25%', 'float': 'left'},
                ),
                min_graph(id=self._il[self.id_chart], style={'width': '75%', 'display': 'inline-block'}),
            ], style={'padding': '15px'},
        )

    def create_callbacks(self) -> None:
        """Register callbacks necessary for this tab."""
        self.verify_types_for_callbacks()

        self.register_update_chart()

    def register_update_chart(self):   # noqa: CCR001
        """Register the update_chart callback."""
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
            if 'tabs-select.value' not in properties:  # FIXME: replace tabs-select with actual keyname (?)
                if self.takes_args:
                    # Parse the arguments to generate a new plot
                    kwargs = {key: a_in[key]['value'] for key in self.input_ids[1:]}
                    new_chart = self.func_map[name_func](self.data, height=650, **kwargs)
                else:
                    new_chart = self.func_map[name_func]()
            # Example Mapping Output. Alternatively, just: `return [new_chart]`
            return map_outputs(outputs, [(self.id_chart, 'figure', new_chart)])


@implements(AppInterface)  # noqa: H601
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
    ])
    default_dim_name = {
        'x': 'total_bill',
        'y': 'tip',
        'color': 'smoker',
    }


@implements(AppInterface)  # noqa: H601
class TabIris(TabBase):
    """TabIris properties."""

    name = 'Iris Data'
    data = px.data.iris()
    func_map = OrderedDict([
        ('histogram', px.histogram),
        ('bar', px.bar),
        ('strip', px.strip),
        ('box', px.box),
        ('violin', px.violin),
    ])
    dims = ('x', 'y', 'color', 'facet_row', 'facet_col')
    default_dim_name = {
        'x': 'sepal_width',
        'color': 'species',
    }


@implements(AppInterface)  # noqa: H601
class TabGapminder(TabBase):
    """TabGapminder properties."""

    name = 'Gapminder Data'
    data = px.data.gapminder()
    func_map = OrderedDict([
        ('area', px.area),
        ('line', px.line),
    ])
    dims = ('x', 'y', 'color', 'line_group', 'facet_row', 'facet_col')
    default_dim_name = {
        'x': 'year',
        'y': 'pop',
        'color': 'continent',
        'line_group': 'country',
    }


@implements(AppInterface)  # noqa: H601
class TabTernary(TabBase):
    """TabTernary properties."""

    name = 'Ternary'
    data = px.data.election()
    func_map = OrderedDict([
        ('scatter_ternary', px.scatter_ternary),
        ('line_ternary', px.line_ternary),
    ])
    dims = ('a', 'b', 'c', 'color', 'hover_name')  # size - only for scatter
    default_dim_name = {
        'a': 'Joly',
        'b': 'Coderre',
        'c': 'Bergeron',
        'color': 'winner',
        'hover_name': 'district',
    }


@implements(AppInterface)  # noqa: H601
class TabWind(TabBase):
    """TabWind properties."""

    name = 'Wind'
    data = px.data.wind()
    func_map = OrderedDict([
        ('scatter_polar', px.scatter_polar),
        ('line_polar', px.line_polar),  # (line_close=True)
        ('bar_polar', px.bar_polar),
    ])
    dims = ('r', 'theta', 'color')
    default_dim_name = {
        'r': 'frequency',
        'theta': 'direction',
        'color': 'strength',
        'symbol': 'strength',
    }


@implements(AppInterface)  # noqa: H601
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
    default_dim_name = {
        'x': 'sepal_width',
        'y': 'sepal_length',
    }

# ======================================================================================================================
# Create class for application to control manage variable scopes


class InteractivePXApp(FullScreenAppWithTabs):  # noqa: H601
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
            TabWind(app=self.app),
            TabColor(app=self.app),
        ]

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div([
            html.H1('Dash/Plotly Express Data Exploration Demo', style={'padding': '15px 0 0 15px'}),
            super().return_layout(),
        ])
