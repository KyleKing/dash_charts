# dash_charts

Python package for [Plotly/Dash](https://dash.plot.ly/) apps with support for multi-page, modules, and new charts such as Pareto with an Object Orient Approach

Includes base classes for building a custom chart or application, new charts such as a Pareto, and base classes for tabbed or multi-page applications. See full documentation at [https://kyleking.me/dash_charts/](https://kyleking.me/dash_charts/). ( TODO: Currently not online )

<!-- TOC -->

- [dash_charts](#dash_charts)
    - [Nov2020-Mar2021 Updates](#nov2020-mar2021-updates)
    - [Quick Start](#quick-start)
        - [1. Install](#1-install)
        - [2. Example Code](#2-example-code)
        - [3. Resulting Pareto Chart](#3-resulting-pareto-chart)
        - [4. Additional Notes](#4-additional-notes)
    - [Design Principles](#design-principles)
    - [Local Development](#local-development)
    - [Example Charts and Tables](#example-charts-and-tables)
        - [Pareto Chart](#pareto-chart)
        - [Gantt Chart](#gantt-chart)
        - [Time Vis Chart](#time-vis-chart)
        - [Rolling Mean and STD Chart](#rolling-mean-and-std-chart)
        - [Fitted Chart](#fitted-chart)
        - [Real Time SQL Demo](#real-time-sql-demo)
        - [Coordinate Chart](#coordinate-chart)
        - [Marginal Chart](#marginal-chart)
        - [Data Table Module](#data-table-module)
        - [Upload Module](#upload-module)
    - [Applications](#applications)
        - [Tabbed Application](#tabbed-application)
        - [Multi-Page Application](#multi-page-application)
        - [PX Generic Application](#px-generic-application)
    - [Other](#other)
        - [Cache](#cache)
        - [Static HTML Generation](#static-html-generation)
    - [Coverage](#coverage)
    - [External Links](#external-links)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Roadmap](#roadmap)
    - [Contributing](#contributing)
    - [License](#license)

<!-- /TOC -->

## Nov2020-Mar2021 Updates

<!-- FIXME: Keep updates up to date! -->
I am in the process of implementing breaking changes for a `0.1` version. The major change will be to refactor the various chart constructors to match the plotly express initialization arguments

I plan on reaching >75% test coverage, adding type annotations, and improving the documentation as well

I considered using a builder pattern, but the plotly.express approach can be implemented through an attributes class that accepts unhandled keyword arguments to the plots

```py
@attr.s(auto..)
class ChartSettings(BaseSettings):

    x_label: str
    y_label: str
    etc: int


class SomeChart:
    def __init__(self, **kwargs):
        self.something = AttrClass(**kwargs)
```

~~Alternatively, the builder pattern might be useful to create new charts with slightly different views.~~ Would require serializing the class in order to copy rather than modify in memory

Currently blocked by pending changes to `calcipy` and `calcipy-template` to how doit tasks are configured

## Quick Start

### 1. Install

With Poetry install `dash_charts` with: `poetry add dash_charts --git https://github.com/KyleKing/dash_charts.git#main`

### 2. Example Code

<!-- CODE:tests/examples/readme.py -->

```py
"""Example Dash Application."""

from typing import Optional

import dash
from dash import html
import plotly.express as px
from box import Box
from implements import implements

from dash_charts.pareto_chart import ParetoChart
from dash_charts.utils_app import AppBase, AppInterface
from dash_charts.utils_fig import min_graph

# FIXME: the change to use Box/_ID needs to be implemented in the examples. This is causing failures in the test cases
#   Still pending if this is the preferred approach
_ID = Box({
    'chart': 'pareto',
})
"""Default App IDs."""


@implements(AppInterface)
class ParetoDemo(AppBase):
    """Example creating a simple Pareto chart."""

    def __init__(self, app: Optional[dash.Dash] = None) -> None:
        """Initialize app and initial data members. Should be inherited in child class and called with super().

        Args:
            app: Dash instance. If None, will create standalone app. Otherwise, will be part of existing app

        """
        self.name = 'Car Share Pareto Demo'
        self.data_raw = None
        self.chart_main = None
        self._id = _ID

        super().__init__(app=app)

    def generate_data(self) -> None:
        """Format the car share data from plotly express for the Pareto. Called by parent class."""
        self.data_raw = (px.data.carshare()
                         .rename(columns={'peak_hour': 'category', 'car_hours': 'value'}))
        self.data_raw['category'] = [f'H:{cat:02}' for cat in self.data_raw['category']]

    def create_elements(self) -> None:
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = ParetoChart(title='Car Share Pareto', xlabel='Peak Hours', ylabel='Car Hours')

    def return_layout(self) -> dict:
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div([
            html.Div([min_graph(
                id=self._il[self._id.chart],
                figure=self.chart_main.create_figure(df_raw=self.data_raw),
            )]),
        ])

    def create_callbacks(self) -> None:
        """Register the callbacks."""
        pass  # Override base class. Not necessary for this example


if __name__ == '__main__':
    app = ParetoDemo()
    app.create()
    app.run(debug=True)
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()

```

<!-- /CODE:tests/examples/readme.py -->

### 3. Resulting Pareto Chart

![MinimumExampleScreenCapture](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/pareto_readme.png)

### 4. Additional Notes

<!-- FIXME: Document use of the `calcipy_template` instead of manual configuration -->

TO get the most out of the tools, you may want to add `calcipy` and add the below snippets to your `pyproject.toml` file

```toml
[tool.poetry.dev-dependencies.dash]
extras = [ "testing",]
version = "*, ^1.19"

[tool.poetry.dependencies.calcipy]
git = "https://github.com/kyleking/calcipy.git"
branch = "dev/development"
rev = "01635ea"  # Always pin to a commit
develop = true  # Optional: will reinstall each time

[tool.poetry.dev-dependencies.calcipy]
git = "https://github.com/kyleking/calcipy.git"
branch = "dev/development"
extras = [ "dev", "lint", "test", "commitizen_legacy"]
```

You will also want at minimum the [dodo.py](https://raw.githubusercontent.com/KyleKing/dash_charts/blob/main/dodo.py) and folder structure from [dash_charts](https://github.com/KyleKing/dash_charts)

## Design Principles

I wanted to show that an object oriented programming approach to Dash projects could be really powerful for improving code reuse and improving readability in large projects. Below are a couple of design principles to keep that I try to keep in mind when implementing this package.

- Try to encapsulate all application logic (callbacks, ids, etc.) in application classes or modules
- For components that are reused between application, create a `module`. The layout, state, and callbacks can all be delegated to the module rather than cluttering the main application's class and allowing for better code reuse
- Move any methods that do not require state (`self`) into standalone functions
- If you can separate Dash (ids/layout/Callbacks) and Plotly (figures/tables) code, you can generate static HTML or PNGs more easily. Sometimes static output is useful when programmatically generating views rather than tweaking the interactive inputs each time.

Overall, I find that this package really improves my Dash code and I hope others find it useful. Please feel free to submit PRs or open issues if you have any input. See [./DESIGN.md](https://github.com/KyleKing/dash_charts/blob/main/DESIGN.md) for additional information on design decisions and package architecture

## Local Development

Initial commands to clone code from Github, create Python virtual environment, and run first example application

```sh
git clone https://github.com/KyleKing/dash_charts.git
cd dash_charts
poetry install
poetry shell
python tests/examples/ex_app_px.py
```

Other useful scripts for testing, documentation, and more:

```sh
poetry run ptw -- -m "not INTERACTIVE"
poetry run doit run test
poetry run doit
```

## Example Charts and Tables

Below are screenshots and links to the example code for each chart or table included in dash_charts

### Pareto Chart

Create Pareto charts in Dash. Handles ordering the category, calculating the cumulative percentage, and configuring both YAxis.

See sample code in [tests/examples/ex_pareto_chart.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_pareto_chart.py). Screenshot below:

![ex_pareto_chart.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_pareto_chart.png)

### Gantt Chart

Create simple Gantt charts in Dash. Doesn't support more advanced features such as dependencies and resource assignment, but effectively shows tasks, progress, and projects in a clear way. You can toggle the different projects on/off and use zoom like a normal Plotly chart.

See sample code in [tests/examples/ex_gantt_chart.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_gantt_chart.py). Screenshot below:

![ex_gantt_chart.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_gantt_chart.png)

### Time Vis Chart

Create a TimeVis chart to plot general time visualizations (based on [daattali/timevis](https://github.com/daattali/timevis) from R). This chart differs from a Gantt chart by showing events that repeat in the same row.

See sample code in [tests/examples/ex_time_vis_chart.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_time_vis_chart.py). Screenshot below:

![ex_time_vis_chart.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_time_vis_chart.png)

### Rolling Mean and STD Chart

Easily chart the rolling mean and standard deviation for a given scatter data set. Demonstrates using chart annotations.

See sample code in [tests/examples/ex_rolling_chart.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_rolling_chart.py). Screenshot below:

![ex_rolling_chart.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_rolling_chart.png)

### Fitted Chart

Fit arbitrary scatter data with a specified equation. On hover will show the rounded fit parameters. Useful for experimenting with new data.

See sample code in [tests/examples/ex_fitted_chart.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_fitted_chart.py). Screenshot below:

![ex_fitted_chart.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_fitted_chart.png)

### Real Time SQL Demo

Example using a Rolling Chart to show real time data from a SQLite database. For the demo, a background thread populates the database as the Dash app runs in a separate thread.

See sample code in [tests/examples/ex_sqlite_realtime.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_sqlite_realtime.py). Screenshot below:

![ex_sqlite_realtime.gif](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_sqlite_realtime.gif)

### Coordinate Chart

Chart a discrete data set on a 2D plane with color for intensity. Below examples show how to use the `YearGrid()`, `MonthGrid()`, and `CircleGrid()` classes

See sample code in [tests/examples/ex_coordinate_chart.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_coordinate_chart.py). Screenshot below:

![ex_coordinate_chart.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_coordinate_chart.png)

### Marginal Chart

Example creating a new chart from utils_fig.MarginalChart

See sample code in [tests/examples/ex_marginal_chart.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_marginal_chart.py). Screenshot below:

![ex_marginal_chart.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_marginal_chart.png)

### Data Table Module

Display Dash data table from dataframe

See sample code in [tests/examples/ex_datatable.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_datatable.py). Screenshot below:

![ex_datatable.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_datatable.png)

### Upload Module

Upload module for user-selected CSV, JSON, or SQLite files.

See sample code in [tests/examples/ex_upload.py](https://ra/www.gubusem/KyleKing/dash_charts/blob/main/tests/examples/ex_upload.py). Screenshot below:

![ex_upload.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_upload.png)

## Applications

Every app derives from `AppBase()` so that each tab or page can be run independently or part of a more complicated application

### Tabbed Application

Use the `AppWithTabs()` base class to quickly build applications with tabbed navigation. You can set tabs to the top/bottom/left/right, to be compact or not, etc.

See sample code in [tests/examples/ex_tabs.py](https://ra/www.gubusem/KyleKing/dash_charts/blob/main/tests/examples/ex_tabs.py). Screenshot below:

![ex_tabs.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_tabs.png)

### Multi-Page Application

Use the `AppMultiPage()` base class to quickly build applications with tabbed navigation. You can set tabs to the top/bottom/left/right, to be compact or not, etc.

See sample code in [tests/examples/ex_multi_page.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_multi_page.py). Screenshot below:

![ex_multi_page.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_multi_page.png)

### PX Generic Application

To facilitate general data analysis from a JSON, CSV, or SQLite file, dash_charts includes apps for each px plot type and a tabbed app to bring them all together.

See sample code in [tests/examples/ex_app_px.py](https://ra/www.gubusem/KyleKing/dash_charts/blob/main/tests/examples/ex_app_px.py). Screenshot below:

![ex_app_px.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_app_px.png)

## Other

Other notable components in `dash_charts`

### Cache

Utilities for utilizing a local cache file system for storing JSON data. Particularly useful if scraping or making many API calls to cache the responses locally.

See sample code in the relevant test file [tests/test_utils_json_cache.py](https:/raw./usercontentgithub.com/KyleKing/dash_charts/blob/main/tests/test_utils_json_cache.py)

### Static HTML Generation

utilities for creating static HTML output with all of the CustomCharts above or user-created. Also includes utilities for writing tables, code, markdown, and more to be added.

See sample code in [tests/examples/ex_utils_static.py](https://www.github.com/KyleKing/dash_charts/blob/main/tests/examples/ex_utils_static.py). Screenshot below:

![ex_utils_static.png](https://raw.githubusercontent.com/KyleKing/dash_charts/main/.images/ex_utils_static.png)

## Coverage

Latest coverage table

<!-- COVERAGE -->

| File | Statements | Missing | Excluded | Coverage |
| --: | --: | --: | --: | --: |
| `dash_charts/__init__.py` | 2 | 0 | 0 | 100.0% |
| `dash_charts/app_px.py` | 130 | 11 | 0 | 91.5% |
| `dash_charts/components.py` | 13 | 0 | 0 | 100.0% |
| `dash_charts/coordinate_chart.py` | 102 | 1 | 6 | 99.0% |
| `dash_charts/custom_colorscales.py` | 3 | 0 | 0 | 100.0% |
| `dash_charts/datatable.py` | 79 | 25 | 0 | 68.4% |
| `dash_charts/equations.py` | 11 | 0 | 0 | 100.0% |
| `dash_charts/gantt_chart.py` | 54 | 0 | 0 | 100.0% |
| `dash_charts/modules_datatable.py` | 101 | 11 | 0 | 89.1% |
| `dash_charts/modules_upload.py` | 132 | 60 | 0 | 54.5% |
| `dash_charts/pareto_chart.py` | 43 | 0 | 2 | 100.0% |
| `dash_charts/scatter_line_charts.py` | 45 | 0 | 3 | 100.0% |
| `dash_charts/time_vis_chart.py` | 61 | 0 | 0 | 100.0% |
| `dash_charts/utils_app.py` | 98 | 14 | 6 | 85.7% |
| `dash_charts/utils_app_modules.py` | 26 | 3 | 4 | 88.5% |
| `dash_charts/utils_app_with_navigation.py` | 119 | 9 | 6 | 92.4% |
| `dash_charts/utils_callbacks.py` | 34 | 6 | 0 | 82.4% |
| `dash_charts/utils_data.py` | 63 | 1 | 0 | 98.4% |
| `dash_charts/utils_dataset.py` | 76 | 43 | 0 | 43.4% |
| `dash_charts/utils_fig.py` | 77 | 2 | 4 | 97.4% |
| `dash_charts/utils_helpers.py` | 17 | 8 | 7 | 52.9% |
| `dash_charts/utils_json_cache.py` | 51 | 10 | 0 | 80.4% |
| `dash_charts/utils_static.py` | 111 | 5 | 0 | 95.5% |
| `dash_charts/utils_static_toc.py` | 22 | 1 | 0 | 95.5% |

Generated on: 2020-11-08T22:46:27.420973

<!-- /COVERAGE -->

## External Links

[![codebeat badge](https://codebeat.co/badges/9d2b9a53-9203-4467-8cde-68f24e930389)](https://codebeat.co/projects/github-com-kyleking-dash_charts-main) [![Documentation Site Online Status Badge](https://img.shields.io/website?label=Doc%20Site&up_message=up&url=https%3A%2F%2Fgithub.com%2FKyleKing%2Fdash_charts%2F)](https://kyleking.me/dash_charts/) ![Commits Since last Release](https://img.shields.io/github/commits-since/KyleKing/dash_charts/latest) ![Last Commit Badge](https://img.shields.io/github/last-commit/kyleking/dash_charts)

Useful Dash reference links

- Official [Dash Docs](https://dash.plot.ly) / [Plotly Docs](https://plot.ly/python/)
- Example Apps
    - Pretty annotations from [Market Ahead](https://www.marketahead.com/p/FOX), a commercial Dash app
    - Pleasant dark app from Dash-Bio, [Circos](https://github.com/plotly/dash-bio/blob/main/tests/dashbio_demos/app_circos.py)
    - All [Dash Sample Apps](https://github.com/plotly/dash-sample-apps/tree/main/apps)
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
    - [Pandas CheatSheet for Data Manipulation](https://github.com/pandas-dev/pandas/blob/main/doc/cheatsheet/Pandas_Cheat_Sheet.pdf)

<!-- TODO: See https://github.com/KyleKing/calcipy/issues/38 -->

## Installation

1. ...
2. ...

    ```sh
    echo Hello World!
    ```

3. ...

## Usage

<!-- TODO: Show an example (screenshots, terminal recording, etc.) -->

For more examples, see [Scripts](https://github.com/kyleking/dash_charts/scripts) or [Tests](https://github.com/kyleking/dash_charts/tests)

## Roadmap

See the `Open Issues` and `Milestones` for current status and [./docs/CODE_TAG_SUMMARY.md](./docs/CODE_TAG_SUMMARY.md) for annotations in the source code.

For release history, see the [./docs/CHANGELOG.md](./docs/CHANGELOG.md)

## Contributing

See the Developer Guide, Contribution Guidelines, etc

- [./docs/DEVELOPER_GUIDE.md](./docs/DEVELOPER_GUIDE.md)
- [./docs/STYLE_GUIDE.md](./docs/STYLE_GUIDE.md)
- [./docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md)
- [./docs/CODE_OF_CONDUCT.md](./docs/CODE_OF_CONDUCT.md)
- [./docs/SECURITY.md](./docs/SECURITY.md)

## License

[LICENSE](https://github.com/kyleking/dash_charts/LICENSE)
