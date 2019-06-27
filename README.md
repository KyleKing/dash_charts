# Dash_Charts

Boilerplate chart classes for [Plotly/Dash](https://dash.plot.ly/) apps. See the `examples/` directory and Example Charts below

<!-- TOC -->

- [Dash_Charts](#dash_charts)
    - [Quick Start](#quick-start)
    - [Local Development](#local-development)
    - [Example Charts and Documentation](#example-charts-and-documentation)
        - [Pareto Chart](#pareto-chart)
        - [Alignment Chart](#alignment-chart)
        - [Rolling Mean/STD Chart](#rolling-meanstd-chart)
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

### Alignment Chart

Useful for visualizing misalignment between measured values and expected values. Accepts a `stretch` argument to visually increase the spacing between the measured and expected value.

![ex_alignment_chart.png](.images/ex_alignment_chart.png)

### Rolling Mean/STD Chart

Easily chart the rolling mean and standard deviation for a given scatter data set.

![ex_rolling_chart.png](.images/ex_rolling_chart.png)

## External Links

Useful Dash reference links

- [Official Dash Docs](https://dash.plot.ly)
- [Official Plotly Docs](https://plot.ly/python/)
- Pretty annotations from [Market Ahead](https://www.marketahead.com/p/FOX) commercial Dash app
- Really Pretty dark app from Dash-Bio [Circos](https://github.com/plotly/dash-bio/blob/master/tests/dashbio_demos/app_circos.py)
- General [Dash Sample Apps](https://github.com/plotly/dash-sample-apps/tree/master/apps)
- Cool Callback Chain debugger [dash_callback_chain](https://github.com/nicolaskruchten/dash_callback_chain)
- [Awesome CSS Frameworks](https://github.com/troxler/awesome-css-frameworks)
    - Deciding between [Bulma](https://bulma.io) and [Materialize](https://materializecss.com/showcase.html)
    - [Bulma Flatly Theme preview](https://jenil.github.io/bulmaswatch/flatly/)
    - [Bulma Customizer](https://bulma-customizer.bstash.io/)
    - See the [Admin Template here](https://bulmatemplates.github.io/bulma-templates/)

## TODO

- Checkout the v2 Table Filtering in Dash 0.43 / https://dash.plot.ly/datatable
    - [Filtering Syntax](https://dash.plot.ly/datatable/filtering)
- Review [Grammar of Graphics](https://towardsdatascience.com/a-comprehensive-guide-to-the-grammar-of-graphics-for-effective-visualization-of-multi-dimensional-1f92b4ed4149)
- Implement multi-page apps:
    - See ["SlapDash" Multi-Page Cookie Cutter App](https://github.com/ned2/slapdash)
    - Official Docs: https://dash.plot.ly/urls
- See annotations
    - [Text & Annotations](https://plot.ly/python/text-and-annotations/)
    - [Shapes in Plotly](https://plot.ly/python/shapes/)
    - (Want annotations like: [Market Ahead](https://www.marketahead.com/p/FOX) commercial Dash app)
- Add tests
