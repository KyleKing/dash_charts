# Developer Notes

## Local Development

```sh
git clone https://github.com/kyleking/dash_charts.git
cd dash_charts
poetry install

# See the available tasks
poetry run doit list

# Run the default task list (lint, auto-format, test coverage, etc.)
poetry run doit --continue

# Make code changes and run specific tasks as needed:
poetry run doit run test
```

## Publishing

For testing, create an account on [TestPyPi](https://test.pypi.org/legacy/). Replace `...` with the API token generated on TestPyPi|PyPi respectively

```sh
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi ...

poetry run doit run publish_test_pypi
# If you didn't configure a token, you will need to provide your username and password to publish
```

To publish to the real PyPi

```sh
poetry config pypi-token.pypi ...
poetry run doit run publish

# For a full release, triple check the default tasks, increment the version, rebuild documentation, and publish!
poetry run doit run --continue
poetry run doit run cl_bump lock document deploy_docs publish

# For pre-releases use cl_bump_pre
poetry run doit run cl_bump_pre -p rc
poetry run doit run lock document deploy_docs publish
```

## Current Status

<!-- {cts} COVERAGE -->
| File                                       |   Statements |   Missing |   Excluded | Coverage   |
|:-------------------------------------------|-------------:|----------:|-----------:|:-----------|
| `dash_charts/__init__.py`                  |            4 |         0 |          0 | 100.0%     |
| `dash_charts/app_px.py`                    |          130 |        11 |          0 | 91.5%      |
| `dash_charts/components.py`                |           13 |         0 |          0 | 100.0%     |
| `dash_charts/coordinate_chart.py`          |          102 |         1 |          6 | 99.0%      |
| `dash_charts/custom_colorscales.py`        |            3 |         0 |          0 | 100.0%     |
| `dash_charts/datatable.py`                 |           79 |        25 |          0 | 68.4%      |
| `dash_charts/equations.py`                 |           11 |         0 |          0 | 100.0%     |
| `dash_charts/gantt_chart.py`               |           54 |         0 |          0 | 100.0%     |
| `dash_charts/modules_datatable.py`         |          100 |        33 |          0 | 67.0%      |
| `dash_charts/modules_upload.py`            |          130 |        60 |          0 | 53.8%      |
| `dash_charts/pareto_chart.py`              |           42 |         0 |          2 | 100.0%     |
| `dash_charts/scatter_line_charts.py`       |           45 |         0 |          3 | 100.0%     |
| `dash_charts/time_vis_chart.py`            |           61 |         0 |          0 | 100.0%     |
| `dash_charts/utils_app.py`                 |          103 |        14 |          6 | 86.4%      |
| `dash_charts/utils_app_modules.py`         |           26 |         3 |          4 | 88.5%      |
| `dash_charts/utils_app_with_navigation.py` |          118 |         9 |          6 | 92.4%      |
| `dash_charts/utils_callbacks.py`           |           31 |         6 |          0 | 80.6%      |
| `dash_charts/utils_data.py`                |           63 |         1 |          0 | 98.4%      |
| `dash_charts/utils_dataset.py`             |           76 |        43 |          0 | 43.4%      |
| `dash_charts/utils_fig.py`                 |           74 |         3 |          4 | 95.9%      |
| `dash_charts/utils_helpers.py`             |           19 |         8 |          7 | 57.9%      |
| `dash_charts/utils_json_cache.py`          |           51 |        10 |          0 | 80.4%      |
| `dash_charts/utils_static.py`              |          111 |         5 |          0 | 95.5%      |
| `dash_charts/utils_static_toc.py`          |           22 |         1 |          0 | 95.5%      |
| **Totals**                                 |         1468 |       233 |         38 | 84.1%      |

Generated on: 2022-08-04T20:47:35.216758
<!-- {cte} -->
