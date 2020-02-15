"""Example Tabbed Applet."""

import dash_html_components as html
import plotly_express as px
from dash_charts.dash_helpers import parse_cli_port
from dash_charts.utils_app import AppBase, AppWithTabs
from dash_charts.utils_fig import min_graph


class StaticTab(AppBase):
    """Simple App without charts or callbacks."""

    def register_charts(self):
        """Register the initial charts."""
        pass

    def register_callbacks(self):
        """Register callbacks necessary for this tab."""
        pass


class TabOne(StaticTab):
    """Tab One."""

    name = 'Tab One'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(className='columns', children=[
            html.Div(className='column', children=[
                html.P(className='title', children='First Chart'),
                min_graph(
                    figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=300),
                ),
                html.P(className='title', children='Another Chart'),
                min_graph(
                    figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=300),
                ),
            ]),
            html.Div(className='column', children=[
                html.P(className='title', children='A Small Chart'),
                min_graph(
                    figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length', height=300),
                ),
                html.P(className='subtitle', children='An Image'),
                html.Img(src='https://media.giphy.com/media/JGQe5mxayVF04/giphy.gif'),
            ]),
        ])


class TabTwo(StaticTab):
    """Tab Two."""

    name = 'Tab Two'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(className='section', children=[
            html.P(className='title', children=f'{self.name} Chart'),
            min_graph(figure=px.scatter(px.data.iris(), x='sepal_width', y='sepal_length')),
        ])


class TabThree(StaticTab):
    """Tab Three."""

    name = 'Tab Three'

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return html.Div(className='section', children=[
            html.P(className='title', children=f'{self.name} Chart'),
            min_graph(figure=px.scatter(
                px.data.iris(), x='sepal_width', y='sepal_length', color='species',
                marginal_y='rug', marginal_x='histogram',
            )),
        ])


class TabAppDemo(AppWithTabs):
    """Demo application."""

    name = 'TabAppDemo'

    tabs_location = 'right'
    """Tab orientation setting. One of `(left, top, bottom, right)`."""

    def define_tabs(self):
        """Return list of initialized tabs.

        Returns:
            list: each item is an initialized tab (ex `[AppBase(self.app)]` in the order each tab is rendered

        """
        return [
            TabOne(self.app),
            TabTwo(self.app),
            TabThree(self.app),
        ]


if __name__ == '__main__':
    port = parse_cli_port()
    TabAppDemo().run(port=port, debug=True)
