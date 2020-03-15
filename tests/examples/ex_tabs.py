"""Example Tabbed Applet."""

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.utils_app import AppBase
from dash_charts.utils_app_with_navigation import AppWithTabs
from dash_charts.utils_fig import min_graph


class StaticTab(AppBase):
    """Simple App without charts or callbacks."""

    basic_style = {
        'marginLeft': 'auto',
        'marginRight': 'auto',
        'maxWidth': '1000px',
        'paddingTop': '10px',
    }

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids(['N/A'])

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements.."""
        pass

    def create_callbacks(self):
        """Register callbacks necessary for this tab."""
        pass


# ----------------------------------------------------------------------------------------------------------------------


class TabZero(StaticTab):
    """Tab Zero."""

    name = 'Tab Name for Tab Zero'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

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
            obj: Dash HTML object. Default is simple HTML text

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
            obj: Dash HTML object. Default is simple HTML text

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
            obj: Dash HTML object. Default is simple HTML text

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


class TabAppDemo(AppWithTabs):
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


instance = TabAppDemo
if __name__ == '__main__':
    port = parse_cli_port()
    app = instance()
    app.create()
    app.run(port=port, debug=True)
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
