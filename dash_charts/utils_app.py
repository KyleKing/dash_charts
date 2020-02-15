"""Utility functions and classes for building applications."""

import copy
from collections import OrderedDict
from itertools import count
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html

from .utils_fig import format_app_callback

ASSETS_DIR = Path(__file__).parent / 'assets'
"""Path to the static files directory."""

COUNTER = count(start=0, step=1)
"""Initialize iterator to provide set of unique integers when called with `next()`."""

STATIC_URLS = {
    'dash': {
        'href': 'https://codepen.io/chriddyp/pen/bWLwgP.css',
        'rel': 'stylesheet',
        'crossorigin': 'anonymous',
    },
    'bulma': {
        'href': 'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.5/css/bulma.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-H5O3U+oUYwd/bFECZMaQ1XJlueV5e1gB4b7Xt0M06fPbgz48WH33qxUyQNPeZVou',
        'crossorigin': 'anonymous',
    },
    'bulmaswatch-flatly': {
        'href': 'https://jenil.github.io/bulmaswatch/flatly/bulmaswatch.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-grOdOgbiGLquXGKNXkKpsnbx1eEGLCSnYloh9JKQdX31HHHQiQFf3uz8hhuIzUy8',
        'crossorigin': 'anonymous',
    },
    'normalize': {
        'href': 'https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-9Z9AuAj0Xi0z7WFOSgjjow8EnNY9wPNp925TVLlAyWhvZPsf5Ks23Ex0mxIrWJzJ',
        'crossorigin': 'anonymous',
    },
}
"""Dictionary of stylesheet names and URL to minimized CSS asset.

Hashes generated from: https://www.srihash.org/

"""


def init_app(**app_kwargs):
    """Return new Dash app with `assets_folder` set to local assets.

    Args:
        app_kwargs: any kwargs to pass to the dash initializer other than `assets_folder`

    Returns:
        dict: `dash.Dash()` instance (`app`)

    """
    return dash.Dash(__name__, assets_folder=str(ASSETS_DIR), **app_kwargs)


def opts_dd(lbl, value):
    """Format an individual item in a Dash dcc dropdown list.

    Args:
        lbl: Dropdown label
        value: Dropdown value

    Returns:
        dict: keys `label` and `value` for dcc.dropdown()

    """
    return {'label': str(lbl), 'value': value}


class AppBase:
    """Base class for building Dash Applications."""

    name = None
    """Child class must specify a name for the application"""

    ids = {}
    """Lookup dictionary used to track each element in UI that requires a callback"""

    # In child class, declare the rest of the static data members here

    def __init__(self, app=None):
        """Initialize app and initial data members. Should be inherited in child class and called with super().

        Args:
            app: Dash instance. If None, will create standalone app. Otherwise, will be part of existing app

        Raises:
            RuntimeError: if child class has not set a `self.name` data member

        """
        if self.name is None:
            raise RuntimeError('Child class must set `self.name` to a unique string for this app')

        self.app = init_app() if app is None else app

    def register_uniq_ids(self, app_ids):
        """Register the `app_ids` to the corresponding global_id in the `self.ids` lookup dictionary.

        The app_ids must be unique within this App so that a layout can be created. This method registers `self.ids`
          which are a list of globally unique ids (incorporating this App's unique `self.name`) allowing for the child
          class of this base App to be resused multiple times within a tabbed or multi-page application without
          id-collision

        Args:
            app_ids: list of strings that are unique within this App

        """
        for app_id in app_ids:
            self.ids[app_id] = f'{self.name}-{app_id}'

    def verify_app_initialization(self):
        """Check that the app was properly initialized.

        Raises:
            RuntimeError: if child class has not called `self.register_uniq_ids`

        """
        if not self.ids.keys():
            raise RuntimeError('Child class must first call `self.register_uniq_ids(__)` before self.run()')

    def run(self, **dash_kwargs):
        """Configure the app and start the Dash server instance.

        Args:
            **dash_kwargs: keyword arguments for `Dash.run_server()`

        """
        self.verify_app_initialization()
        # Register the charts, the app layout, then the callbacks
        self.register_charts()
        self.app.layout = self.return_layout()
        self.register_callbacks()
        # Launch the server
        self.app.run_server(**dash_kwargs)

    def register_charts(self):
        """Register the initial charts.

        Does not return a result. All charts should be initialized in this method (ex `self.main_chart = ParetoChart()`)

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('register_charts must be implemented by child class')

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(children=['Welcome to the BaseApp! Override return_layout() in child class.'])

    def callback(self, outputs, inputs, states):
        """Return app callback decorator based on provided components.

        Args:
            outputs: list of tuples with app_id and property name
            inputs: list of tuples with app_id and property name
            states: list of tuples with app_id and property name

        Returns:
            dict: result of `self.app.callback()`

        """
        return self.app.callback(*format_app_callback(self.ids, outputs, inputs, states))

    def register_callbacks(self):
        """Register the chart callbacks.

        Does not return a result. May `pass` as long as no callbacks are needed for application

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('register_callbacks must be implemented by child class')


class AppWithTabs(AppBase):
    """Base class for building Dash Application with tabs. Tabs will be in specified `self.tabs_location`."""

    app = None
    """Main Dash application to pass to all child tabs."""

    tabs_location = 'left'
    """Tab orientation setting. One of `(left, top, bottom, right)`."""

    tab_lookup = None
    """OrderedDict of tabs based on the list of tuples from `self.define_tabs()`."""

    tab_layouts = None
    """Dictionary with tab_names as keys and corresponding layout as value."""

    # App ids
    id_tabs_content = 'tabs-wrapper'
    id_tabs_select = 'tabs-content'

    app_ids = [id_tabs_content, id_tabs_select]
    """List of all ids for this app view. Will be mapped to `self.ids` for globally unique ids."""

    def define_tabs(self):
        """Return list of initialized tabs.

        Should return, list: each item is an initialized tab (ex `[AppBase(self.app)]` in the order each tab is rendered

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('define_tabs must be implemented by child class')

    def verify_app_initialization(self):
        """Check that the app was properly initialized.

        Raises:
            RuntimeError: if child class has not called `self.register_uniq_ids`

        """
        super().verify_app_initialization()
        allowed_locations = ('left', 'top', 'bottom', 'right')
        if self.tabs_location not in allowed_locations:
            raise RuntimeError(f'`self.tabs_location = {self.tabs_location}` is not in {allowed_locations}')

    def run(self, **dash_kwargs):
        """Override base class. Configure the parent app and all tabs. Starts the Dash server instance.

        Args:
            **dash_kwargs: keyword arguments for `Dash.run_server()`

        """
        # Suppress callback verification as tab content is rendered later
        self.app.config['suppress_callback_exceptions'] = True
        # Register all unique elements id
        self.register_uniq_ids(self.app_ids)
        # Initialize the lookup for each tab then configure each tab
        self.tab_lookup = OrderedDict([(tab.name, tab) for tab in self.define_tabs()])
        self.verify_app_initialization()
        self.tab_layouts = {}
        for tab_name, tab in self.tab_lookup.items():
            tab.verify_app_initialization()
            tab.register_charts()
            self.tab_layouts[tab_name] = tab.return_layout()
            tab.register_callbacks()
        # Create parent application layout and navigation
        self.app.layout = self.return_layout()
        self.register_callbacks()
        # Launch the server
        self.app.run_server(**dash_kwargs)

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        # Determine style for containing div of the tab content
        div_style = {f'margin-{self.tabs_location}': '10%'}
        if self.tabs_location in ['left', 'right']:
            div_style['width'] = '90%'
        else:
            div_style['height'] = '90%'
        # Configure the tab menu and tab content div
        return html.Div(children=[
            self.tab_menu(),
            html.Div(style=div_style, children=[
                html.Div(id=self.ids[self.id_tabs_content]),
            ]),
        ])

    def tab_menu(self):
        """Return the HTML elements for the tab menu.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        # Unselected tab style
        tab_style = {
            'padding': '10px 20px 10px 20px',
        }
        # Extend tab style for selected case
        selected_style = copy.deepcopy(tab_style)
        if self.tabs_location in ['left', 'right']:
            # Configure for vertical case
            selected_style['border-left'] = '3px solid #119DFF'
            tabs_kwargs = {
                'vertical': True,
                'style': {'width': '100%'},
                'parent_style': {'width': '100%'},
            }
            tabs_style = {
                'background-color': '#F9F9F9',
                'padding': '15px 0 0 5px',
                'position': 'fixed',
                'top': '0', 'bottom': '0', self.tabs_location: '0',  # left/right
                'width': '9%',
            }
        else:
            # Configure for horizontal case
            selected_style['border-top'] = '3px solid #119DFF'
            tabs_kwargs = {}
            tabs_style = {
                'background-color': '#F9F9F9',
                'height': '9%',
                'padding': '15px 0 0 5px',
                'position': 'fixed',
                'right': '0', 'left': '0', self.tabs_location: '0',  # top/bottom
            }
        # Create the tab menu
        tab_kwargs = {'style': tab_style, 'selected_style': selected_style}
        tabs = [dcc.Tab(label=name, value=name, **tab_kwargs) for name, tab in self.tab_lookup.items()]
        return html.Div(children=[
            dcc.Tabs(
                id=self.ids[self.id_tabs_select], value=list(self.tab_lookup.keys())[0],
                children=tabs, **tabs_kwargs,
            ),
        ], style=tabs_style)

    def register_callbacks(self):
        """Register the navigation callback."""
        outputs = [(self.id_tabs_content, 'children')]
        inputs = [(self.id_tabs_select, 'value')]

        @self.callback(outputs, inputs, [])
        def render_tab(tab_name):
            return [self.tab_layouts[tab_name]]


class AppMultiPage(AppBase):
    """Base class for building multi-page Dash Applications."""

    pass  # FIXME: Implement
