"""Example Tabbed Applet."""

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from dash_charts.utils_app_with_navigation import AppWithTabs, StaticTab
from dash_charts.utils_fig import min_graph
from dash_charts.utils_helpers import parse_dash_cli_args


class TabZero(StaticTab):
    """Tab Zero."""

    name = 'Tab Name for Tab Zero'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(style=self.basic_style, children=(
            [html.H1(children=f'{self.name} Scrollable Content')]
            + [html.P(children=[str(count) + '-word' * 10]) for count in range(100)]
        ))


class TabOne(StaticTab):
    """Tab One."""

    name = 'Tab Name for Tab One'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(style=self.basic_style, children=[
            html.H1(children=f'Image from {self.name}'),
            html.Img(src='https://media.giphy.com/media/JGQe5mxayVF04/giphy.gif'),
        ])


class TabTwo(StaticTab):
    """Tab Two."""

    name = 'Tab Name for Tab Two'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(style=self.basic_style, children=[
            html.H1(children=f'{self.name} Chart'),
            dcc.Loading(
                type='circle',
                children=[
                    min_graph(figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=500)),
                ],
            ),
        ])


class TabThree(StaticTab):
    """Tab Three."""

    name = 'Tab Name for Tab Three'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(style=self.basic_style, children=[
            html.H1(children=f'{self.name} Chart'),
            dcc.Loading(
                type='cube',
                children=[
                    min_graph(figure=px.scatter(
                        px.data.iris(), x='sepal_width', y='sepal_length', color='species',
                        marginal_y='rug', marginal_x='histogram', height=500,
                    )),
                ],
            ),
        ])


# ----------------------------------------------------------------------------------------------------------------------


class TabAppDemo(AppWithTabs):  # noqa: H601
    """Demo application."""

    name = 'TabAppDemo'

    tabs_location = 'right'
    """Tab orientation setting. One of `(left, top, bottom, right)`."""

    def define_nav_elements(self):
        """Return list of initialized tabs.

        Returns:
            list: each item is an initialized tab (ex `[AppBase(self.app)]` in the order each tab is rendered

        """
        return [
            TabZero(app=self.app),
            TabOne(app=self.app),
            TabTwo(app=self.app),
            TabThree(app=self.app),
        ]

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        side_padding = {'padding': '10px 0 0 10px'}
        return html.Div([
            html.H3('Application with Tabbed Content Demo', style=side_padding),
            html.P('AppWithTabs is rendered inline, while FullScreenAppWithTabs has a navigation element fixed to the'
                   'viewport. See the px app for an example with full screen and below for an example with'
                   'AppWithTabs.', style=side_padding),
            html.Hr(),
            super().return_layout(),
            html.Hr(),
            html.P('Additional content, like tables, upload module, etc. could go here', style=side_padding),
        ])


instance = TabAppDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
