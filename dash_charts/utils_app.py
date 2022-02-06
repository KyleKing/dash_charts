"""Utility functions and classes for building applications."""

from copy import deepcopy
from itertools import count
from pathlib import Path
from pprint import pprint
from typing import List, Optional

import dash
from box import Box
from dash import html
from implements import Interface

from .utils_callbacks import format_app_callback

ASSETS_DIR = Path(__file__).parent / 'assets'
"""Path to the static files directory."""

COUNTER = count(start=0, step=1)
"""Initialize iterator to provide set of unique integers when called with `next(...)`."""

STATIC_URLS = {
    'dash': {
        'href': 'https://codepen.io/chriddyp/pen/bWLwgP.css',
        'rel': 'stylesheet',
        'crossorigin': 'anonymous',
    },
    'bulma': {
        'href': 'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.5/css/bulma.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-H5O3U+oUYwd/bFECZMaQ1XJlueV5e1gB4b7Xt0M06fPbgz48WH33qxUyQNPeZVou',  # pragma: allowlist secret
        'crossorigin': 'anonymous',
    },
    'bulmaswatch-flatly': {
        'href': 'https://jenil.github.io/bulmaswatch/flatly/bulmaswatch.min.css',
        'rel': 'stylesheet',
    },
    'normalize': {
        'href': 'https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-9Z9AuAj0Xi0z7WFOSgjjow8EnNY9wPNp925TVLlAyWhvZPsf5Ks23Ex0mxIrWJzJ',  # pragma: allowlist secret
        'crossorigin': 'anonymous',
    },
}
"""Dictionary of stylesheet names and URL to minimized CSS asset.

Hashes generated from: https://www.srihash.org/

"""


def init_app(**app_kwargs: dict) -> dash.Dash:
    """Return new Dash app.

    If not overridden in kwargs, will set path to assets folder, add dash stylesheets, and default meta tags.

    Args:
        app_kwargs: any kwargs to pass to the dash initializer

    Returns:
        dash.Dash: instance (`app`)

    """
    if 'assets_folder' not in app_kwargs:
        app_kwargs['assets_folder'] = str(ASSETS_DIR)
    if 'external_stylesheets' not in app_kwargs:
        app_kwargs['external_stylesheets'] = [STATIC_URLS['dash']]
    if 'meta_tags' not in app_kwargs:
        app_kwargs['meta_tags'] = [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
    return dash.Dash(__name__, **app_kwargs)


class AppInterface(Interface):  # noqa: H601
    """Base Dash Application Interface."""

    name = None
    _il = {}
    external_stylesheets = []
    modules: list = []
    validation_layout = None
    init_app_kwargs = {}

    def __init__(self, app: Optional[dash.Dash] = None) -> None:  # noqa: D102, D107
        ...

    def create(self, assign_layout: bool = True) -> None:  # noqa: D102
        ...

    def override_module_defaults(self) -> None:  # noqa: D102
        ...

    def initialization(self) -> None:  # noqa: D102
        ...

    def generate_data(self) -> None:  # noqa: D102
        ...

    def register_uniq_ids(self, app_ids: List[str]) -> None:  # noqa: D102
        ...

    def verify_app_initialization(self) -> None:  # noqa: D102
        ...

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements.

        Does not return a result. All charts should be initialized in this method (ex `self.chart_main = ParetoChart()`)

        """
        ...

    def return_layout(self) -> dict:  # noqa: D102
        ...

    def callback(self, outputs, inputs, states, pic: bool = False, **kwargs: dict):  # noqa: D102
        ...

    def create_callbacks(self) -> None:
        """Register the chart callbacks.

        Does not return a result. May `pass` as long as no callbacks are needed for application

        """
        ...

    def run(self, **dash_kwargs: dict) -> None:  # noqa: D102
        ...

    def get_server(self):  # noqa: D102
        ...


class AppBase:  # noqa: H601
    """Base class for building Dash Applications."""

    name = None
    """Child class must specify a name for the application.

    Set in `self.__init__()`

    """

    nsi = Box({})
    """Box dictionary of Non-Specific IDs (NSI). In `self.initialization()` automatically registered.

    Set in `self.__init__()`

    """

    _il = {}
    """Specific ID lookup (IL) used to track each element in UI that requires a callback."""

    _id = {}
    """Dotted-dict to store ID's relevant for a given chart (replaces storing each id as a data member).

    FIXME: Need to decide if there is a better approach. Reading this code is confusing...

    """

    external_stylesheets = [STATIC_URLS['dash']]
    """List of external stylesheets. Default is minimal Dash CSS. Only applies if app argument not provided."""

    modules: list = []
    """Initialized modules for GUI set in `self.initialization()`. Leave as an empty list if no modules are needed.

    If list contains modules, in self.create(), each module's `*.create_elements` / `*.create_callbacks` will be called

    Child class must call `*.return_layout(ids)` to render each module's layout in `self.return_layout()` method

    """

    validation_layout = None
    """Validation layout used for callback validation. If None, will use the default layout for callback exceptions."""

    init_app_kwargs = {}
    """Additional keyword arguments passed to `init_app()`."""

    # In child class, declare the rest of the static data members here

    def __init__(self, app: Optional[dash.Dash] = None) -> None:
        """Initialize app and initial data members. Should be inherited in child class and called with super().

        Args:
            app: Dash instance. If None, will create standalone app. Otherwise, will be part of existing app

        """
        default = {'title': self.name, 'external_stylesheets': self.external_stylesheets}
        self.init_app_kwargs = {**default, **self.init_app_kwargs}
        self.app = app or init_app(**self.init_app_kwargs)

    def create(self, assign_layout: bool = True) -> None:  # noqa: CCR001
        """Create the ids, app charts, layout, callbacks, and optional modules.

        Args:
            assign_layout: if True, will assign `self.app.layout`. If False, must call `self.return_layout` separately.
                Default is True

        Raises:
            NotImplementedError: if child class has not set the `self.name` data member

        """
        if self.name is None:  # pragma: no cover
            raise NotImplementedError('Child class must set `self.name` to a unique string for this app')

        # Initialize app and each module
        self.initialization()
        for mod in self.modules:
            self.register_uniq_ids(mod.all_ids)
        self.override_module_defaults()  # Call optional override method

        # Create charts for app and each module
        self.create_elements()
        for mod in self.modules:
            mod.create_elements(self._il)

        # Create app layout. User must call the return_layout method from each module within own return_layout method
        if assign_layout:
            self.app.layout = self.return_layout()
        if assign_layout and self.validation_layout:
            self.app.validation_layout = [deepcopy(self.app.layout)] + self.validation_layout
            pprint('\n\nValidationLayout?')
            pprint(self.app.validation_layout)

        # Create callbacks for app and each module
        self.create_callbacks()
        for mod in self.modules:
            mod.create_callbacks(self)

        self.verify_app_initialization()

    def override_module_defaults(self) -> None:
        """Override default values from modules."""
        ...

    def initialization(self) -> None:
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        self.register_uniq_ids([*self._id.values()])
        self.generate_data()

    def generate_data(self) -> None:
        """Recommended method for generating data stored in memory. Called in initialization."""
        ...

    def register_uniq_ids(self, app_ids: List[str]) -> None:
        """Register the `app_ids` to the corresponding global_id in the `self._il` lookup dictionary.

        The app_ids must be unique within this App so that a layout can be created. This method registers `self._il`
          which are a list of globally unique ids (incorporating this App's unique `self.name`) allowing for the child
          class of this base App to be resused multiple times within a tabbed or multi-page application without
          id-collision

        Args:
            app_ids: list of strings that are unique within this App

        """
        self._il = deepcopy(self._il)
        for app_id in app_ids:
            self._il[app_id] = f'{self.name}-{app_id}'.replace(' ', '-')

    def verify_app_initialization(self) -> None:
        """Check that the app was properly initialized.

        Raises:
            RuntimeError: if child class has not called `self.register_uniq_ids`

        """
        if not self._il.keys():  # pragma: no cover
            raise RuntimeError('Child class must first call `self.register_uniq_ids(__)` before self.run()')

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object. Default is simple HTML text

        """
        return html.Div(['Welcome to the BaseApp! Override return_layout() in child class.'])  # pragma: no cover

    def callback(self, outputs, inputs, states, pic: bool = False, **kwargs: dict):
        """Return app callback decorator based on provided components.

        Args:
            outputs: list of tuples with app_id and property name
            inputs: list of tuples with app_id and property name
            states: list of tuples with app_id and property name
            pic: If True, prevent call on page load (`prevent_initial_call`). Default is False
            **kwargs: any additional keyword arguments for `self.app.callback`

        Returns:
            dict: result of `self.app.callback()`

        """
        return self.app.callback(
            *format_app_callback(self._il, outputs, inputs, states),
            prevent_initial_call=pic,
            **kwargs,
        )

    def run(self, **dash_kwargs: dict) -> None:
        """Launch the Dash server instance.

        Args:
            **dash_kwargs: keyword arguments for `Dash.run_server()`

        """
        self.app.run_server(**dash_kwargs)  # pragma: no cover

    def get_server(self):
        """Retrieve server from app instance for production hosting with green unicorn, waitress, IIS, etc.

        Returns:
            dict: the Flask `server` component of the Dash app

        """
        return self.app.server
