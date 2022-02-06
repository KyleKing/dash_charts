"""Classes for more complex applications that have tabbed or paged navigation."""

from collections import OrderedDict
from copy import deepcopy

import dash_bootstrap_components as dbc
from dash import dcc, html
from implements import implements

from .utils_app import AppBase, AppInterface

TODO_CLIENT_CALLBACK = '''
TODO: Create clientside callbacks dynamically to update the title on navigation
See: http://dash.plotly.com/external-resources
```py
app.clientside_callback(
    """
    function(tab_value) {
        if (tab_value === 'tab-1') {
            document.title = 'Tab 1'
        } else if (tab_value === 'tab-2') {
            document.title = 'Tab 2'
        }
    }
    """,
    Output('blank-output', 'children'),
    [Input('tabs-example', 'value')]
)
```
'''


# TODO: Try to see if I can resolve the interface differences or if I need make a subclass interface
# @implements(AppInterface)  # noqa: H601
class AppWithNavigation(AppBase):
    """Base class for building Dash Application with tabs or URL routing."""

    app = None
    """Main Dash application to pass to all child tabs."""

    nav_lookup = None
    """OrderedDict based on the list of tuples from `self.define_nav_elements()`."""

    nav_layouts = None
    """Dictionary with nav_names as keys and corresponding layout as value."""

    def define_nav_elements(self):
        """Return list of initialized pages or tabs accordingly.

        Should return, list: each item is an initialized app (ex `[AppBase(self.app)]` in the order each tab is rendered

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('define_nav_elements must be implemented by child class')  # pragma: no cover

    def create(self, **kwargs):
        """Create each navigation componet, storing the layout. Then parent class to create application.

        Args:
            kwargs: keyword arguments passed to `self.create`

        """
        # Initialize the lookup for each tab then configure each tab
        self.nav_lookup = OrderedDict([(tab.name, tab) for tab in self.define_nav_elements()])
        self.nav_layouts = {}
        for nav_name, nav in self.nav_lookup.items():
            nav.create(assign_layout=False)
            self.nav_layouts[nav_name] = nav.return_layout()

        # Store validation_layout that is later used for callback verification in base class
        self.validation_layout = [*map(deepcopy, self.nav_layouts.values())]

        # Initialize parent application that handles navigation
        super().create(**kwargs)

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids(self.app_ids)

    def create_elements(self) -> None:
        """Override method as not needed at navigation-level."""
        ...  # pragma: no cover

    def create_callbacks(self) -> None:
        """Override method as not needed at navigation-level."""
        ...  # pragma: no cover


@implements(AppInterface)  # noqa: H601
class StaticTab(AppBase):
    """Simple App without charts or callbacks."""

    basic_style = {
        'marginLeft': 'auto',
        'marginRight': 'auto',
        'maxWidth': '1000px',
        'paddingTop': '10px',
    }

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids(['N/A'])

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements.."""
        ...

    def create_callbacks(self) -> None:
        """Register callbacks necessary for this tab."""
        ...


class AppWithTabs(AppWithNavigation):
    """Base class for building Dash Application with tabs."""

    # App ids
    id_tabs_content = 'tabs-wrapper'
    id_tabs_select = 'tabs-content'

    app_ids = [id_tabs_content, id_tabs_select]
    """List of all ids for the top-level tab view. Will be mapped to `self._il` for globally unique ids."""

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        tabs = [dcc.Tab(label=name, value=name) for name, tab in self.nav_lookup.items()]
        return html.Div(
            children=[
                dcc.Tabs(
                    id=self._il[self.id_tabs_select], value=list(self.nav_lookup.keys())[0],
                    children=tabs,
                ),
                html.Div(id=self._il[self.id_tabs_content]),
            ],
        )

    def create_callbacks(self) -> None:
        """Register the navigation callback."""
        outputs = [(self.id_tabs_content, 'children')]
        inputs = [(self.id_tabs_select, 'value')]

        @self.callback(outputs, inputs, [])
        def render_tab(tab_name):
            return [self.nav_layouts[tab_name]]


# > PLANNED: Make the tabs and chart compact as well when the compact argument is set to True
class FullScreenAppWithTabs(AppWithTabs):  # noqa: H601
    """Base class for building Dash Application with tabs that uses the full window."""

    tabs_location = 'left'
    """Tab orientation setting. One of `(left, top, bottom, right)`."""

    tabs_margin = '10%'
    """Adjust this setting based on the width or height of the tabs to prevent the content from overlapping the tabs."""

    tabs_compact = False
    """Boolean setting to toggle between a padded tab layout if False and a minimal compact version if True."""

    def verify_app_initialization(self):
        """Check that the app was properly initialized.

        Raises:
            RuntimeError: if child class has not called `self.register_uniq_ids`

        """
        super().verify_app_initialization()
        allowed_locations = ('left', 'top', 'bottom', 'right')
        if self.tabs_location not in allowed_locations:  # pragma: no cover
            raise RuntimeError(f'`self.tabs_location = {self.tabs_location}` is not in {allowed_locations}')

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(
            children=[
                self.tab_menu(),
                html.Div(
                    style={f'margin-{self.tabs_location}': self.tabs_margin},
                    children=[html.Div(id=self._il[self.id_tabs_content])],
                ),
            ],
        )

    def generate_tab_kwargs(self):
        """Create the tab keyword arguments. Intended to be modified through inheritance.

        Returns:
            tuple: keyword arguments and styling for the dcc.Tab elements

                - tab_kwargs: with at minimum keys `(style, selected_style)` for dcc.Tab
                - tabs_kwargs: to be passed to dcc.Tabs
                - tabs_style: style for the dcc.Tabs HTML element

        """
        # Unselected tab style
        if self.tabs_compact:
            tab_style = {'padding': '2px 4px 2px 4px'}
            tabs_padding = '6px 0 0 2px'
        else:
            tab_style = {'padding': '10px 20px 10px 20px'}
            tabs_padding = '15px 0 0 5px'
        # Extend tab style for selected case
        selected_style = deepcopy(tab_style)
        opposite_lookup = {'top': 'bottom', 'bottom': 'top', 'left': 'right', 'right': 'left'}
        tabs_style = {   # noqa: ECE001
            'backgroundColor': '#F9F9F9',
            'padding': tabs_padding,
            'position': 'fixed',
            'zIndex': '999',
            f'border{opposite_lookup[self.tabs_location].title()}': '1px solid #d6d6d6',
            self.tabs_location: '0',
        }
        if self.tabs_location in ['left', 'right']:
            # Configure for vertical case
            selected_style['border-left'] = '3px solid #119DFF'
            tabs_kwargs = {
                'vertical': True,
                'style': {'width': '100%'},
                'parent_style': {'width': '100%'},
            }
            tabs_style['top'] = '0'
            tabs_style['bottom'] = '0'
            tabs_style['width'] = 'auto'
        else:
            # Configure for horizontal case
            selected_style['border-top'] = '3px solid #119DFF'
            tabs_kwargs = {}
            tabs_style['height'] = 'auto'
            tabs_style['right'] = '0'
            tabs_style['left'] = '0'

        tab_kwargs = {'style': tab_style, 'selected_style': selected_style}
        return (tab_kwargs, tabs_kwargs, tabs_style)

    def tab_menu(self):
        """Return the HTML elements for the tab menu.

        Returns:
            dict: Dash HTML object

        """
        tab_kwargs, tabs_kwargs, tabs_style = self.generate_tab_kwargs()
        tabs = [dcc.Tab(label=name, value=name, **tab_kwargs) for name, tab in self.nav_lookup.items()]
        return html.Div(
            children=[
                dcc.Tabs(
                    id=self._il[self.id_tabs_select], value=list(self.nav_lookup.keys())[0],
                    children=tabs, **tabs_kwargs,
                ),
            ], style=tabs_style,
        )


class AppMultiPage(AppWithNavigation):  # noqa: H601
    """Base class for building Dash Application with multiple pages."""

    navbar_links = None
    """Base class must create list of tuples `[('Link Name', '/link'), ]` to use default `self.nav_bar()`."""

    dropdown_links = None
    """Base class must create list of tuples `[('Link Name', '/link'), ]` to use default `self.nav_bar()`."""

    logo = None
    """Optional path to logo. If None, no logo will be shown in navbar."""

    # App ids
    id_url = 'pages-url'
    id_pages_content = 'pages-wrapper'
    id_toggler = 'nav-toggle'
    id_collapse = 'nav-collapse'

    app_ids = [id_url, id_pages_content, id_toggler, id_collapse]
    """List of all ids for the top-level pages view. Will be mapped to `self._il` for globally unique ids."""

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(
            children=[
                dcc.Location(id=self._il[self.id_url], refresh=False),
                self.nav_bar(),
                html.Div(id=self._il[self.id_pages_content]),
            ],
        )

    def nav_bar(self):
        """Return the HTML elements for the navigation menu.

        Returns:
            dict: Dash HTML object

        """
        # Create brand icon and name where icon in optional
        brand = []
        if self.logo:
            brand.append(dbc.Col(html.Img(src=self.logo, height='25px')))
        brand.append(dbc.Col(dbc.NavbarBrand(self.name, className='ml-2')))
        # Create links in navbar and dropdown. Both are optional
        links = []
        if self.navbar_links:
            links.append(
                dbc.Nav(
                    children=[dbc.NavItem(dbc.NavLink(name, href=link)) for name, link in self.navbar_links],
                    fill=True,
                    navbar=True,
                ),
            )
        if self.dropdown_links:
            links.append(
                dbc.Nav(
                    dbc.DropdownMenu(
                        children=[dbc.DropdownMenuItem(name, href=link) for name, link in self.dropdown_links],
                        in_navbar=True,
                        label='Links',
                        nav=True,
                    ),
                    navbar=True,
                ),
            )
        # Layout default navbar
        return dbc.Navbar(
            children=[
                dbc.NavLink(
                    [
                        dbc.Row(
                            children=brand,
                            align='center g-0',
                        ),
                    ], href='/',
                ),
                dbc.NavbarToggler(id=self._il[self.id_toggler]),
                dbc.Collapse(
                    dbc.Row(
                        children=links,
                        className='flex-nowrap mt-3 mt-md-0 g-0',
                        align='center',
                    ),
                    id=self._il[self.id_collapse],
                    navbar=True,
                ),
            ],
            sticky='top',
            color='dark',
            dark=True,
        )

    def create_callbacks(self) -> None:
        """Register the navigation callback."""
        outputs = [(self.id_pages_content, 'children')]
        inputs = [(self.id_url, 'pathname')]

        @self.callback(outputs, inputs, [])
        def render_page(pathname):
            try:
                # TODO: Demo how pages could use parameters from pathname
                return [self.nav_layouts[self.select_page_name(pathname)]]
            except Exception as err:
                return [html.Div(children=[f'Error rendering "{pathname}":\n{err}'])]

        @self.callback(
            [(self.id_collapse, 'is_open')],
            [(self.id_toggler, 'n_clicks')],
            [(self.id_collapse, 'is_open')],
        )
        def toggle_navbar_collapse(n_clicks, is_open):
            return [not is_open if n_clicks else is_open]

    def select_page_name(self, pathname):
        """Return the page name determined based on the pathname.

        Should return str: page name

        Args:
            pathname: relative pathname from URL

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('nav_bar must be implemented by child class')  # pragma: no cover
