# Dash_Charts

Boilerplate chart classes for [Plotly/Dash](https://dash.plot.ly/) apps. See the `examples/` directory and Example Charts below

<!-- TOC -->

- [Dash_Charts](#dash_charts)
    - [Quick Start](#quick-start)
    - [Local Development](#local-development)
    - [Example Charts and Documentation](#example-charts-and-documentation)
        - [Pareto Chart](#pareto-chart)
        - [Rolling Mean/STD Chart](#rolling-meanstd-chart)
        - [Coordinate Chart](#coordinate-chart)
        - [Alignment Chart](#alignment-chart)
        - [Tabbed Application](#tabbed-application)
    - [External Links](#external-links)
    - [TODO](#todo)

<!-- /TOC -->

## Quick Start

1. Install Poetry: https://github.com/sdispater/poetry
1. Not on PyPi sp can't use `pip install dash_charts`. Instead, install from Github with Poetry: `poetry add dash_charts --git https://github.com/KyleKing/dash_charts.git`
1. Then use in python:

    ```py
    import pandas as pd
    from dash_charts.helpers import MinGraph
    from dash_charts.pareto_chart import ParetoChart

    # Create the data (could be CSV, database, etc.)
    dfDemo = pd.DataFrame(data={})

    # Initialize the chart
    exPareto = ParetoChart(
        title='Sample Pareto Chart',
        xLbl='Category Title',
        yLbl='Measured Downtime (hours)',
    )

    # Create the figure dictionary and add to the layout
    app.layout = html.Div([
        MinGraph(figure=exPareto.createFigure(df=dfDemo)),
    ])
    ```

1. See the full examples in [`examples/`](./examples)

## Local Development

```sh
git clone https://github.com/KyleKing/dash_charts.git
cd dash_charts
poetry install
poetry shell
python examples/01_hello_world.py
```

## Example Charts and Documentation

Full documentation is available at: [https://kyleking.me/dash_charts/](https://kyleking.me/dash_charts/). Below headers highlight some of the examples and included chart functionality

### Pareto Chart

Create a Pareto chart in Dash. Handles ordering the categories, calculating the cumulative percentage, and configuring both YAxis.

![ex_pareto_chart.png](.images/ex_pareto_chart.png)

### Rolling Mean/STD Chart

Easily chart the rolling mean and standard deviation for a given scatter data set.

![ex_rolling_chart-annotated.png](.images/ex_rolling_chart-annotated.png)

### Coordinate Chart

Chart a discrete data set on a 2D plane with color for intensity. Below examples show how to use the CircleGrid() and MonthGrid() classes

![ex_coordinate_chart-circle.png](.images/ex_coordinate_chart-circle.png)
![ex_coordinate_chart-year.png](.images/ex_coordinate_chart-year.png)
![ex_coordinate_chart-month.png](.images/ex_coordinate_chart-month.png)

### Alignment Chart

Useful for visualizing misalignment between measured values and expected values. Accepts a `stretch` argument to visually increase the spacing between the measured and expected value.

![ex_alignment_chart.png](.images/ex_alignment_chart.png)

### Tabbed Application

Useful for putting together a multi-page complex application.

![ex_app.png](.images/ex_app.png)

## External Links

Useful Dash reference links

- [Official Dash Docs](https://dash.plot.ly)
    - Using [URLs in Dash](https://dash.plot.ly/urls)
- [Official Plotly Docs](https://plot.ly/python/) (Searchable)
- Example Apps
    - Pretty annotations from [Market Ahead](https://www.marketahead.com/p/FOX) commercial Dash app
    - Pleasant dark app from Dash-Bio, [Circos](https://github.com/plotly/dash-bio/blob/master/tests/dashbio_demos/app_circos.py)
    - All [Dash Sample Apps](https://github.com/plotly/dash-sample-apps/tree/master/apps)
- Cool Callback Chain debugger [dash_callback_chain](https://github.com/nicolaskruchten/dash_callback_chain)
- [Awesome CSS Frameworks](https://github.com/troxler/awesome-css-frameworks)
    - Bulma Themes
        - [Bulma Flatly Theme preview](https://jenil.github.io/bulmaswatch/flatly/)
        - [Bulma Customizer](https://bulma-customizer.bstash.io/)
        - [Admin Template](https://bulmatemplates.github.io/bulma-templates/)

## TODO

- Add data table
    - Checkout the v2 Table Filtering in Dash 0.43 / https://dash.plot.ly/datatable
    - [Filtering Syntax](https://dash.plot.ly/datatable/filtering)
- TODO: Add the 3D version of the Coordinate chart
    - [Ribbon](https://plot.ly/python/v3/ribbon-plots/)
    - [Surface](https://plot.ly/python/3d-surface-plots/)
- TODO: Enable stacked subplots for multiple years of calendar charts (Subplot title is year)
- Add a tree map
- Review [Grammar of Graphics](https://towardsdatascience.com/a-comprehensive-guide-to-the-grammar-of-graphics-for-effective-visualization-of-multi-dimensional-1f92b4ed4149)
- Add tests?
