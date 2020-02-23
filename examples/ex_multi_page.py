"""Example Multi Page Applet."""

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.utils_app import STATIC_URLS, AppBase, AppMultiPage, init_app
from dash_charts.utils_fig import min_graph


class StaticPage(AppBase):
    """Simple App without charts or callbacks."""

    basic_style = {
        'margin-left': 'auto',
        'margin-right': 'auto',
        'max-width': '1000px',
        'padding-top': '10px',
    }

    def __init__(self, **kwargs):
        """Resolve higher-order data members.

        Args:
            kwargs: keyword arguments passed to __init__

        """
        super().__init__(**kwargs)
        self.register_uniq_ids(['N/A'])

    def register_charts(self):
        """Register the initial charts."""
        pass

    def register_callbacks(self):
        """Register callbacks necessary for this tab."""
        pass


# ----------------------------------------------------------------------------------------------------------------------


class PageText(StaticPage):
    """Text page."""

    name = 'Text Page'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(style=self.basic_style, children=(
            [html.H1(children=f'{self.name} Scrollable Content')]
            + [html.P(children=[str(count) + '-word' * 10]) for count in range(100)]
        ))


class PageChart(StaticPage):
    """Chart page."""

    name = 'Chart Page'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(style=self.basic_style, children=[
            html.H1(children=self.name),
            dcc.Loading(
                type='circle',
                children=[
                    min_graph(figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=500)),
                ],
            ),
        ])


class Page404(StaticPage):
    """404 page."""

    name = 'Page 404'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(style=self.basic_style, children=[
            html.H1(children=f'404: Path not found'),
            html.Img(src='https://upload.wikimedia.org/wikipedia/commons/2/26/NL_Route_404.svg'),
        ])


# ----------------------------------------------------------------------------------------------------------------------


class MultiPageDemo(AppMultiPage):
    """Demo application."""

    name = 'MultiPageDemo'

    def __init__(self, **kwargs):
        """Initialize app with custom stylesheets.

        Args:
            kwargs: keyword arguments passed to __init__

        """
        app = init_app(external_stylesheets=[STATIC_URLS['dash']])
        super().__init__(app=app, **kwargs)

    def define_nav_elements(self):
        """Return list of initialized tabs.

        Returns:
            list: each item is an initialized tab (ex `[AppBase(self.app)]` in the order each tab is rendered

        """
        return [
            PageText(app=self.app),
            PageChart(app=self.app),
            Page404(app=self.app),
        ]

    def nav_bar(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(children=['TODO...'])  # FIXME: Make navbar

    def select_page_name(self, pathname):
        """Return the page name determined based on the pathname.

        Should return obj: Dash HTML object

        Args:
            pathname: relative pathname from URL

        Raises:
            NotImplementedError: Child class must implement this method

        """
        if pathname == '/':
            return PageText.name
        elif 'chart' in pathname:
            return PageChart.name
        else:
            return Page404.name


if __name__ == '__main__':
    port = parse_cli_port()
    MultiPageDemo().run(port=port, debug=True)
