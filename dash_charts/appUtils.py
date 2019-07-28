"""App/GUI utility classes."""

import copy

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_charts.helpers import initApp


class TabBase:
    """Base class for each tab (page) of the application."""

    NAME = None

    def __init__(self, app):
        """Initialize the tab and verify data members.

        app -- Dash application instance

        """
        assert self.NAME is not None, 'The tab must be assigned a unique NAME'

        self.app = app

    def createLayout(self):
        """Return the Dash layout components."""
        raise NotImplementedError('self.createLayout has not been implemented for "{}"'.format(self.NAME))

    def registerCallbacks(self):
        """Register all callbacks necessary for this tab."""
        raise NotImplementedError('self.registerCallbacks has not been implemented for "{}"'.format(self.NAME))


class TabbedDashApp:
    """Base Dash Application with tabs in a left side bar."""

    def __init__(self):
        """Initialize app."""
        self.app = initApp()

    def defineTABS(self):
        """Define the list of tabs used to create the navigation and each page."""
        raise NotImplementedError('This class must be overridden to return a list of TabBase elements.')

    def run(self, *, debug=True, **kwargs):
        """Run the application passing any kwargs to dash."""
        # Suppress callback verification as tab content is rendered later
        self.app.config['suppress_callback_exceptions'] = True

        self.TABS = self.defineTABS()
        self.TAB_LOOKUP = {_tab.NAME: _tab for _tab in self.TABS}
        self.TAB_MAP = {tab.NAME: tab.createLayout() for tab in self.TABS}

        # Create application layout and navigation callback
        self._createLayout()
        self._registerNaviCallback()
        # Register callbacks from each tab
        for _tab in self.TABS:
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
        tabStyle = {'padding': '10px 20px 10px 20px'}
        tabSelect = copy.copy(tabStyle)
        tabSelect['border-left'] = '3px solid #119DFF'
        return html.Div(children=[
            dcc.Tabs(
                id='tabs-select', value=self.TABS[0].NAME, vertical=True,
                children=[
                    dcc.Tab(label=_tab.NAME, value=_tab.NAME, style=tabStyle, selected_style=tabSelect)
                    for _tab in self.TABS
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

    def _registerNaviCallback(self):
        """Register callback to handle tab rendering/navigation."""
        @self.app.callback(
            Output('tabs-content', 'children'),
            [Input('tabs-select', 'value')],
        )
        def renderTabs(name):
            """Render tabs when switched."""
            return self.TAB_MAP[name]
