"""App/GUI utility classes."""

import copy

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_charts.helpers import init_app


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
