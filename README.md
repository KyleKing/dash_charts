# Dash-Charts

Helpful functions for Plotly Dash apps: https://dash.plot.ly/

## Quick Start

1. Install Poetry: https://github.com/sdispater/poetry
1. Not on PyPi and can't use `pip install ...`. Instead, install from Github with Poetry: `poetry add dash-charts --git `
1. Then use in python:

    ```py
    import pandas as pd
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
        dcc.Graph(figure=exPareto.createFigure(df=dfDemo)),
    ])
    ```

1. See the full examples in [`examples/`](./examples)
1. The chart classes are a good starting point and can be overridden for further personalization

## Local Development

```sh
git clone https://github.com/KyleKing/Dash-HelloWorld.git
cd Dash-HelloWorld
poetry install
poetry shell
python examples/01_hello_world.py
```

## Example Charts and Documentation

List and images of example charts below. Full package documentation at: [TODO](./TODO/)

TODO: export documentation as pdoc3 then make available as gh-pages or PDF?

### Pareto Chart

Create a Pareto chart in Dash. Handles ordering the categories, calculating the cumulative percentage, and configuring both YAxis.

![ex_pareto_chart.png](.images/ex_pareto_chart.png)

### Alignment Chart

Useful for visualizing misalignment between measured values and expected values. Accepts a `stretch` argument to visually increase the spacing between the measured and expected value.

![ex_alignment_chart.png](.images/ex_alignment_chart.png)

### Rolling Mean/STD Chart

Easily chart the rolling mean and standard deviation for a given scatter data set.

![ex_rolling_chart.png](.images/ex_rolling_chart.png)

## TODO Tasks (README)

- Rename and publish as PyPi package
- Add tests/configure application
- Checkout the v2 Table Filtering in Dash 0.43
- Check FAQs: https://dash.plot.ly/faqs
- Checkout example charts: https://plot.ly/python/statistical-charts/
  - More examples:
    - https://gist.github.com/chriddyp/9b2b3e8a6c67697279d3724dce5dab3c
    - https://github.com/plotly/dash-recession-report-demo
    - https://github.com/plotly/dash-opioid-epidemic-demo
    - https://github.com/plotly/dash-web-trader
- Test routing: https://dash.plot.ly/urls
- Experiment with sharing state: https://dash.plot.ly/sharing-data-between-callbacks
