"""Utility functions and classes for building applications."""

import copy
from itertools import count
from pathlib import Path

import dash
import dash_html_components as html

from .utils_fig import format_app_callback

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
    """Return new Dash app.

    If not overridden in kwargs, will set path to assets folder, add dash stylesheets, and default meta tags.

    Args:
        app_kwargs: any kwargs to pass to the dash initializer

    Returns:
        dict: `dash.Dash()` instance (`app`)

    """
    if 'assets_folder' not in app_kwargs:
        app_kwargs['assets_folder'] = str(ASSETS_DIR)
    if 'external_stylesheets' not in app_kwargs:
        app_kwargs['external_stylesheets'] = [STATIC_URLS['dash']]
    if 'meta_tags' not in app_kwargs:
        app_kwargs['meta_tags'] = [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
    return dash.Dash(__name__, **app_kwargs)


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

    external_stylesheets = [STATIC_URLS['dash']]
    """List of external stylesheets. Default is minimal Dash CSS. Only applies if app argument not provided."""

    # In child class, declare the rest of the static data members here

    def __init__(self, app=None):
        """Initialize app and initial data members. Should be inherited in child class and called with super().

        Args:
            app: Dash instance. If None, will create standalone app. Otherwise, will be part of existing app

        """
        self.app = init_app(external_stylesheets=self.external_stylesheets) if app is None else app

    def create(self):
        """Create the ids, app charts, layout, and callbacks. Called in `__init__`.

        Raises:
            NotImplementedError: if child class has not set a `self.name` data member

        """
        if self.name is None:
            raise NotImplementedError('Child class must set `self.name` to a unique string for this app')

        self.initialization()
        self.create_charts()
        self.app.layout = self.return_layout()
        self.create_callbacks()
        self.verify_app_initialization()

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        pass

    def register_uniq_ids(self, app_ids):
        """Register the `app_ids` to the corresponding global_id in the `self.ids` lookup dictionary.

        The app_ids must be unique within this App so that a layout can be created. This method registers `self.ids`
          which are a list of globally unique ids (incorporating this App's unique `self.name`) allowing for the child
          class of this base App to be resused multiple times within a tabbed or multi-page application without
          id-collision

        Args:
            app_ids: list of strings that are unique within this App

        """
        self.ids = copy.deepcopy(self.ids)
        for app_id in app_ids:
            self.ids[app_id] = f'{self.name}-{app_id}'.replace(' ', '-')

    def verify_app_initialization(self):
        """Check that the app was properly initialized.

        Raises:
            RuntimeError: if child class has not called `self.register_uniq_ids`

        """
        if not self.ids.keys():
            raise RuntimeError('Child class must first call `self.register_uniq_ids(__)` before self.run()')

    def create_charts(self):
        """Register the initial charts.

        Does not return a result. All charts should be initialized in this method (ex `self.chart_main = ParetoChart()`)

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('create_charts must be implemented by child class')

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

    def create_callbacks(self):
        """Register the chart callbacks.

        Does not return a result. May `pass` as long as no callbacks are needed for application

        Raises:
            NotImplementedError: Child class must implement this method

        """
        raise NotImplementedError('create_callbacks must be implemented by child class')

    def run(self, **dash_kwargs):
        """Launch the Dash server instance.

        Args:
            **dash_kwargs: keyword arguments for `Dash.run_server()`

        """
        self.app.run_server(**dash_kwargs)

    def get_server(self):
        """Retrieve server from app instance for production hosting with green unicorn, waitress, IIS, etc.

        Returns:
            obj: the Flask `server` component of the Dash app

        """
        return self.app.server
