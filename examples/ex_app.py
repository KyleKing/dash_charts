"""Example Tabbed Applet."""

import dash_html_components as html
import plotly_express as px
from dash_charts import appUtils
from dash_charts.helpers import MinGraph


class TabOne(appUtils.TabBase):
    """Tab One."""

    NAME = 'Tab One'

    def createLayout(self):
        """Return the Dash layout components."""
        return html.Div(className='columns', children=[
            html.Div(className='column', children=[
                html.P(className='title', children='First Chart'),
                MinGraph(
                    figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=300),
                ),
                html.P(className='title', children='Another Chart'),
                MinGraph(
                    figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=300),
                ),
            ]),
            html.Div(className='column', children=[
                html.P(className='title', children='A Small Chart'),
                MinGraph(
                    figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", height=300),
                ),
                html.P(className='subtitle', children='An Image'),
                html.Img(src='https://media.giphy.com/media/JGQe5mxayVF04/giphy.gif')
            ]),
        ])

    def registerCallbacks(self):
        """Register callbacks necessary for this tab."""
        pass


class TabTwo(appUtils.TabBase):
    """Tab Two."""

    NAME = 'Tab Two'

    def createLayout(self):
        """Return the Dash layout components."""
        return html.Div(className='section', children=[
            html.P(className='title', children='Tab Two Chart'),
            MinGraph(figure=px.scatter(px.data.iris(), x="sepal_width", y="sepal_length")),
        ])

    def registerCallbacks(self):
        """Register callbacks necessary for this tab."""
        pass


class TabThree(appUtils.TabBase):
    """Tab Three."""

    NAME = 'Tab Three'

    def createLayout(self):
        """Return the Dash layout components."""
        return html.Div(className='section', children=[
            html.P(className='title', children='Tab Three Chart'),
            MinGraph(figure=px.scatter(
                px.data.iris(), x="sepal_width", y="sepal_length", color="species",
                marginal_y="rug", marginal_x="histogram",
            )),
        ])

    def registerCallbacks(self):
        """Register callbacks necessary for this tab."""
        pass


class DemoApp(appUtils.TabbedDashApp):
    """Demo application."""

    def defineTABS(self):
        """Define the tabs."""
        return [
            TabOne(self.app),
            TabTwo(self.app),
            TabThree(self.app),
        ]


if __name__ == '__main__':
    DemoApp().run()
