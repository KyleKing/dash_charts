# Dash_Charts

Library for OOP implementation of [Plotly/Dash](https://dash.plot.ly/). Includes base classes for building a custom chart or application, new charts such as a Pareto, and base classes for tabbed or multi-page applications. See full documentation at [https://kyleking.me/dash_charts/](https://kyleking.me/dash_charts/).

<!-- TOC -->

- [Dash_Charts](#dash_charts)
  - [Quick Start](#quick-start)
  - [Local Development](#local-development)
  - [Example Charts and Tables](#example-charts-and-tables)
    - [Pareto Chart](#pareto-chart)
    - [Rolling Mean and STD Chart](#rolling-mean-and-std-chart)
    - [Coordinate Chart](#coordinate-chart)
    - [Marginal Chart](#marginal-chart)
    - [Data Table](#data-table)
  - [Applications](#applications)
    - [Tabbed Application](#tabbed-application)
    - [Multi-Page Application](#multi-page-application)
  - [Coverage](#coverage)
  - [External Links](#external-links)

<!-- /TOC -->

## Quick Start

1. Install `dash_charts` from Github with: `pip install git+https://github.com/KyleKing/dash_charts.git` (or in a Poetry project with `pip install dash_charts --git https://github.com/KyleKing/dash_charts.git`)
1. Minimum example:

    <!-- CODE:tests/examples/readme.py -->

    ```py
    import dash_html_components as html
    import plotly.express as px
    from dash_charts.pareto_chart import ParetoChart
    from dash_charts.utils_app import AppBase
    from dash_charts.utils_fig import min_graph


    class ParetoDemo(AppBase):
        """Example creating a simple Pareto chart."""

        name = 'Car Share Pareto Demo'
        """Application name"""

        data_raw = None
        """All in-memory data referenced by callbacks and plotted. If modified, will impact all viewers."""

        chart_main = None
        """Main chart (Pareto)."""

        id_chart = 'pareto'
        """Unique name for the main chart."""

        def initialization(self):
            """Initialize ids with `self.register_uniq_ids([...])` and application data."""
            super().initialization()
            self.register_uniq_ids([self.id_chart])
            # Format the car share data from plotly express for the Pareto
            self.data_raw = (px.data.carshare()
                             .rename(columns={'peak_hour': 'category', 'car_hours': 'value'}))
            self.data_raw['category'] = [f'H:{cat:02}' for cat in self.data_raw['category']]

        def create_elements(self):
            """Initialize the charts, tables, and other Dash elements."""
            self.chart_main = ParetoChart(title='Car Share Pareto', xlabel='Peak Hours', ylabel='Car Hours')

        def return_layout(self):
            """Return Dash application layout.

            Returns:
                obj: Dash HTML object. Default is simple HTML text

            """
            return html.Div([
                html.Div([min_graph(
                    id=self.ids[self.id_chart],
                    figure=self.chart_main.create_figure(df_raw=self.data_raw),
                )]),
            ])

        def create_callbacks(self):
            """Register the callbacks."""
            pass  # Override base class. Not necessary for this example


    if __name__ == '__main__':
        app = ParetoDemo()
        app.create()
        app.run(debug=True)

    ```

    <!-- /CODE:tests/examples/readme.py -->

1. Resulting Pareto Chart

    ![MinimumExampleScreenCapture](.images/pareto_readme.png)

## Local Development

```sh
git clone https://github.com/KyleKing/dash_charts.git
cd dash_charts
poetry install
poetry shell
python tests/examples/ex_px.py
```

## Example Charts and Tables

Below are screenshots and links to the example code for each chart or table included in dash_charts

### Pareto Chart

Create a Pareto chart in Dash. Handles ordering the category, calculating the cumulative percentage, and configuring both YAxis.

See sample code in [tests/examples/ex_pareto_chart.py](tests/examples/ex_pareto_chart.py). Screenshot below:

![ex_pareto_chart.png](.images/ex_pareto_chart.png)

### Rolling Mean and STD Chart

Easily chart the rolling mean and standard deviation for a given scatter data set.

See sample code in [tests/examples/ex_rolling_chart.py](tests/examples/ex_rolling_chart.py). Screenshot below:

![ex_rolling_chart-annotated.png](.images/ex_rolling_chart-annotated.png)

### Coordinate Chart

Chart a discrete data set on a 2D plane with color for intensity. Below examples show how to use the `YearGrid()`, `MonthGrid()`, and `CircleGrid()` classes

See sample code in [tests/examples/ex_coordinate_chart.py](tests/examples/ex_coordinate_chart.py). Screenshot below:

![ex_coordinate_chart.png](.images/ex_coordinate_chart.png)

### Marginal Chart

Example creating a new chart from utils_fig.MarginalChart

See sample code in [tests/examples/ex_marginal_chart.py](tests/examples/ex_marginal_chart.py). Screenshot below:

![ex_marginal_chart.png](.images/ex_marginal_chart.png)

### Data Table

Display Dash data table from dataframe

See sample code in [tests/examples/ex_datatable.py](tests/examples/ex_datatable.py). Screenshot below:

![ex_datatable.png](.images/ex_datatable.png)

## Applications

Every app derives from `AppBase()` so that each tab or page can be run independently or part of a more complicated application

### Tabbed Application

Use the `AppWithTabs()` base class to quickly build applications with tabbed navigation. You can set tabs to the top/bottom/left/right, to be compact or not, etc.

See sample code in [tests/examples/ex_tabs.py](tests/examples/ex_tabs.py). Screenshot below:

![ex_tabs.png](.images/ex_tabs.png)

### Multi-Page Application

Use the `AppMultiPage()` base class to quickly build applications with tabbed navigation. You can set tabs to the top/bottom/left/right, to be compact or not, etc.

See sample code in [tests/examples/ex_multi_page.py](tests/examples/ex_multi_page.py). Screenshot below:

![ex_multi_page.png](.images/ex_multi_page.png)

## Coverage

Latest coverage table

<!-- COVERAGE -->

| File | Statements | Missing | Excluded | Coverage |
| --: | --: | --: | --: | --: |
| __init__.py | 1 | 0 | 0 | 100.0 |
| components.py | 6 | 0 | 0 | 100.0 |
| coordinate_chart.py | 105 | 1 | 6 | 99.0 |
| custom_colorscales.py | 4 | 0 | 0 | 100.0 |
| dash_helpers.py | 6 | 0 | 6 | 100.0 |
| datatable.py | 30 | 1 | 0 | 96.7 |
| equations.py | 11 | 0 | 0 | 100.0 |
| fitted_chart.py | 37 | 1 | 5 | 97.3 |
| grouped_bar.py | 0 | 0 | 0 | 100.0 |
| pareto_chart.py | 39 | 0 | 2 | 100.0 |
| rolling_chart.py | 23 | 1 | 0 | 95.7 |
| time_vis.py | 0 | 0 | 0 | 100.0 |
| utils_app.py | 57 | 4 | 8 | 93.0 |
| utils_app_modules.py | 15 | 15 | 2 | 0.0 |
| utils_app_with_navigation.py | 97 | 9 | 6 | 90.7 |
| utils_fig.py | 88 | 3 | 4 | 96.6 |

Generated on: 2020-03-15T19:37:26.334293

<!-- /COVERAGE -->

## External Links

[![codebeat badge](https://codebeat.co/badges/9d2b9a53-9203-4467-8cde-68f24e930389)](https://codebeat.co/projects/github-com-kyleking-dash_charts-master) [![Documentation Site Online Status Badge](https://img.shields.io/website?label=Doc%20Site&up_message=up&url=https%3A%2F%2Fgithub.com%2FKyleKing%2Fdash_charts%2F)](https://kyleking.me/dash_charts/) ![Commits Since last Release](https://img.shields.io/github/commits-since/KyleKing/dash_charts/latest) ![Last Commit Badge](https://img.shields.io/github/last-commit/kyleking/dash_charts)

Useful Dash reference links

- Official [Dash Docs](https://dash.plot.ly) / [Plotly Docs](https://plot.ly/python/)
- Example Apps
  - Pretty annotations from [Market Ahead](https://www.marketahead.com/p/FOX), a commercial Dash app
  - Pleasant dark app from Dash-Bio, [Circos](https://github.com/plotly/dash-bio/blob/master/tests/dashbio_demos/app_circos.py)
  - All [Dash Sample Apps](https://github.com/plotly/dash-sample-apps/tree/master/apps)
- Code Conceptual inspiration
  - [On Tidy data](https://www.jeannicholashould.com/tidy-data-in-python.html)
  - [Using field for properties in a @DataClass](https://florimond.dev/blog/articles/2018/10/reconciling-dataclasses-and-properties-in-python/)
- Best Practices
  - IBM Design Language (note that v2 doesn't have documentation on visualization yet)
    - [Process](https://www.ibm.com/design/v1/language/experience/data-visualization/process/)
    - [Select Chart](https://www.ibm.com/design/v1/language/experience/data-visualization/chart-models/)
      - Alt [Chart Decision Diagram](https://www.tatvic.com/blog/7-visualizations-learn-r/)
    - [Principles (color conventions, etc.)](https://www.ibm.com/design/v1/language/experience/data-visualization/visualization/)
    - [Color Library and Data Vis Swatches](https://www.ibm.com/design/v1/language/resources/color-library/)
    - [Interaction](https://www.ibm.com/design/v1/language/experience/data-visualization/interaction/)
    - [Style](https://www.ibm.com/design/v1/language/experience/data-visualization/style/)
- Colors
  - [Friendly Guide to Colors](https://lisacharlotterost.de/2016/04/22/Colors-for-DataVis/)
  - [Viz-Palette Tool](https://projects.susielu.com/viz-palette)
  - [AI Color Palette](http://colormind.io/) / [Coolors](https://coolors.co/2b303a-92dce5-eee5e9-7c7c7c-d64933)
- Reference
  - [Pandas CheatSheet for Data Manipulation](https://github.com/pandas-dev/pandas/blob/master/doc/cheatsheet/Pandas_Cheat_Sheet.pdf)
