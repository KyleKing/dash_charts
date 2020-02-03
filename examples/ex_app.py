"""Example Tabbed Applet."""

import dash_html_components as html
import plotly_express as px
from dash_charts import utils_app
from dash_charts.helpers import min_graph


class TabOne(utils_app.TabBase):
    """Tab One."""

    tab_name = 'Tab One'

    def create_layout(self):
        """Return the Dash layout components."""
        return html.Div(className='columns', children=[
            html.Div(className='column', children=[
                html.P(className='title', children='First Chart'),
                min_graph(
                    figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=300),
                ),
                html.P(className='title', children='Another Chart'),
                min_graph(
                    figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=300),
                ),
            ]),
            html.Div(className='column', children=[
                html.P(className='title', children='A Small Chart'),
                min_graph(
                    figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=300),
                ),
                html.P(className='subtitle', children='An Image'),
                html.Img(src='https://media.giphy.com/media/JGQe5mxayVF04/giphy.gif')
            ]),
        ])

    def registerCallbacks(self):
        """Register callbacks necessary for this tab."""
        pass


class TabTwo(utils_app.TabBase):
    """Tab Two."""

    tab_name = 'Tab Two'

    def create_layout(self):
        """Return the Dash layout components."""
        return html.Div(className='section', children=[
            html.P(className='title', children='Tab Two Chart'),
            min_graph(figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length")),
        ])

    def registerCallbacks(self):
        """Register callbacks necessary for this tab."""
        pass


class TabThree(utils_app.TabBase):
    """Tab Three."""

    tab_name = 'Tab Three'

    def create_layout(self):
        """Return the Dash layout components."""
        return html.Div(className='section', children=[
            html.P(className='title', children='Tab Three Chart'),
            min_graph(figure=px.scatter(
                px.data.iris(), x="sepal_width", y="sepal_length", color="species",
                marginal_y="rug", marginal_x="histogram",
            )),
        ])

    def registerCallbacks(self):
        """Register callbacks necessary for this tab."""
        pass


class DemoApp(utils_app.TabbedDashApp):
    """Demo application."""

    def define_tabs(self):
        """Define the tabs."""
        return [
            TabOne(self.app),
            TabTwo(self.app),
            TabThree(self.app),
        ]


if __name__ == '__main__':
    DemoApp().run()
