"""Utility functions and classes for building applications."""

import copy
from itertools import count
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

ASSETS_DIR = Path(__file__).parent / 'assets'
"""Path to the static files directory."""

COUNTER = count(start=0, step=1)
"""Initialize iterator to provide set of unique integers when called with `next()`."""


def init_app(**kwargs):
    """Return new Dash app with `assets_folder` set to local assets.

    Args:
        kwargs: any kwargs to pass to the dash initializer other than `assets_folder`

    Returns:
        app `dash.Dash()` instance

    """
    return dash.Dash(__name__, assets_folder=str(ASSETS_DIR), **kwargs)


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

    def __init__(self, *, app=None):
        """Initialize app and initial data members. Should be inherited in child class and called with super().

        Args:
            app: Dash instance. If None, will create standalone app. Otherwise, will be part of existing app

        Raises:
            RuntimeError: if child class has not set a `self.name` data member

        """
        self.app = init_app() if app is None else app
        if self.name is None:
            raise RuntimeError('Child class must set `self.name` to a unique string for this app')

    def register_uniq_ids(self, base_ids):
        """Register all ids in the lookup dictionary.

        Args:
            base_ids: list of unique strings to register with the lookup dictionary

        """
        for base_id in base_ids:
            self.ids[base_id] = f'{self.name}-{base_id}'

    def run(self, **dash_kwargs):
        """Run the application passing any kwargs to Dash.

        Args:
            **dash_kwargs: keyword arguments for `Dash.run_server()`

        Raises:
            RuntimeError: if child class has not called `self.register_uniq_ids`

        """
        if not self.ids.keys():
            raise RuntimeError('Child class must first call `self.register_uniq_ids(__)` before self.run()')

        # Register the charts, the app layout, the callbacks, then start the Dash server
        self.register_charts()
        self.app.layout = self.return_layout()
        self.register_callbacks()
        self.app.run_server(**dash_kwargs)  # TODO: How does this work with multiple apps?

    def register_charts(self):
        """Register the initial charts.

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('register_charts is not implemented')

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(children=['Welcome to the BaseApp!'])

    def register_callbacks(self):
        """Register the chart callbacks.

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('register_callbacks is not implemented')


class AppWithTabs(AppBase):
    """Base class for building tabbed Dash Applications."""

    pass  # TODO: Implement


class AppMultiPage(AppBase):
    """Base class for building multi-page Dash Applications."""

    pass  # TODO: Implement


class TabBase:
    """Base class for each tab (page) of the application."""

    tab_name = None
    """Unique keyname used to identify the tab."""

    def __init__(self, app):
        """Initialize the tab and verify data members.

        app -- Dash application instance

        """
        if self.tab_name is None:
            raise RuntimeError('The tab must be assigned a unique tab_name')

        self.app = app

    def create_layout(self):
        """Return the Dash layout components."""
        raise NotImplementedError('self.create_layout has not been implemented for "{}"'.format(self.tab_name))

    def registerCallbacks(self):
        """Register all callbacks necessary for this tab."""
        raise NotImplementedError('self.registerCallbacks has not been implemented for "{}"'.format(self.tab_name))


class TabbedDashApp:
    """Base Dash Application with tabs in a left side bar."""

    app = None
    """Main Dash application."""

    # TODO: Convert tab_list_tbd to list so that tab_lookup is created by define_tabs
    tab_list_tbd = None
    """List of tabs (to be combined with app_tabs)."""

    app_tabs = None
    """Dictionary of tabs created by `self.define_tabs()`."""

    # FIXME: DOCUMENT
    tab_map_tbd = None
    """Not sure?"""

    source_data = None
    """Source data used throughout app. Treat as `read-only` updating only as new data is available."""

    def __init__(self):
        """Initialize app."""
        self.app = init_app()

    def define_tabs(self):
        """Define the list of tabs used to create the navigation and each page."""
        raise NotImplementedError('This class must be overridden to return a list of TabBase elements.')

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        # Suppress callback verification as tab content is rendered later
        self.app.config['suppress_callback_exceptions'] = True

        self.tab_list_tbd = self.define_tabs()
        self.app_tabs = {_tab.tab_name: _tab for _tab in self.tab_list_tbd}
        self.tab_map_tbd = {tab.tab_name: tab.create_layout() for tab in self.tab_list_tbd}

        # Create application layout and navigation callback
        self._createLayout()
        self.register_navigation_callback()
        # Register callbacks from each tab
        for _tab in self.tab_list_tbd:
            _tab.registerCallbacks()

        self.app.run_server(debug=debug, **kwargs)

    def _createLayout(self):
        """Create application layout."""
        self.app.layout = html.Div(children=[
            self.__sideMenu(),
            html.Div(style={'margin-left': '10%', 'width': '90%'}, children=[
                self.__content()
            ]),
        ])

    def __sideMenu(self):
        """Return the HTML elements for the tab side-menu."""
        tab_style = {'padding': '10px 20px 10px 20px'}
        tab_select = copy.copy(tab_style)
        tab_select['border-left'] = '3px solid #119DFF'
        return html.Div(children=[
            dcc.Tabs(
                id='tabs-select', value=self.tab_list_tbd[0].tab_name, vertical=True,
                children=[
                    dcc.Tab(label=_tab.tab_name, value=_tab.tab_name, style=tab_style, selected_style=tab_select)
                    for _tab in self.tab_list_tbd
                ],
                style={'width': '100%'},
                parent_style={'width': '100%'},
            ),
        ], style={
            'background-color': '#F9F9F9',
            'bottom': '0',
            'left': '0',
            'padding': '15px 0 0 5px',
            'position': 'fixed',
            'top': '0',
            'width': '9%',
        })

    def __content(self):
        """Return HTML elements for the main content."""
        return html.Div(className='section', children=[
            html.Div(id='tabs-content'),
        ])

    def register_navigation_callback(self):
        """Register callback to handle tab rendering/navigation."""
        @self.app.callback(
            Output('tabs-content', 'children'),
            [Input('tabs-select', 'value')],
        )
        def render_tabs(name):
            """Render tabs when switched."""
            return self.tab_map_tbd[name]
