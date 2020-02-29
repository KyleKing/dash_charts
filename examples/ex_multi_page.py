"""Example Multi Page Applet."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.utils_app import AppBase, AppMultiPage
from dash_charts.utils_fig import min_graph


class StaticPage(AppBase):
    """Simple App without charts or callbacks."""

    basic_style = {
        'margin-left': 'auto',
        'margin-right': 'auto',
        'max-width': '1000px',
        'padding-top': '10px',
    }

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        self.register_uniq_ids(['N/A'])

    def create_charts(self):
        """Register the initial charts."""
        pass

    def create_callbacks(self):
        """Register callbacks necessary for this tab."""
        pass


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

    navbar_links = [('Home', '/'), ('Chart', '/is-chart'), ('404', '/404')]
    """Base class must create list of tuples `[('Link Name', '/link'), ]` to use default `self.nav_bar()`."""

    dropdown_links = [('DBC', 'https://dash-bootstrap-components.opensource.faculty.ai/l/components/nav')]
    """Base class must create list of tuples `[('Link Name', '/link'), ]` to use default `self.nav_bar()`."""

    logo = 'https://images.plot.ly/logo/new-branding/plotly-logomark.png'
    """Optional path to logo. If None, no logo will be shown in navbar."""

    external_stylesheets = [dbc.themes.FLATLY]  # DARKLY, FLATLY, etc. (https://bootswatch.com/)
    """List of external stylesheets. Default is minimal Dash CSS. Only applies if app argument not provided."""

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

    def select_page_name(self, pathname):
        """Return the page name determined based on the pathname.

        Args:
            pathname: relative pathname from URL

        Returns:
            str: page name

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
else:
    INSTANCE = MultiPageDemo()
    FLASK_HANDLE = INSTANCE.get_server()
