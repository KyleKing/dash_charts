"""Test pareto_chart."""

import pytest

from dash_charts import pareto_chart


class TestChart(pareto_chart.ParetoChart):  # noqa: H601
    """Custom chart for testing."""

    __test__ = False


def test_pareto_colors_property():
    """Test setting the pareto_colors property on the ParetoChart class."""
    test_chart = TestChart(title='', xlabel='', ylabel='')
    pass_colors_1 = {'bar': '#B2FFD6', 'line': '#AA78A6'}
    pass_colors_2 = {'bar': 'rgba(37, 87, 100, 1.00)', 'line': 'hsla(356, 55%, 44%)'}
    fail_colors_1 = {'line': '#B2FFD6'}
    fail_message_1 = "Validation of self.pareto_colors failed: {'bar': ['required field']}"

    with pytest.raises(RuntimeError) as fail_error_1:
        test_chart.pareto_colors = fail_colors_1

    assert str(fail_error_1.value) == fail_message_1
    test_chart.pareto_colors = pass_colors_1
    assert test_chart.pareto_colors == pass_colors_1
    test_chart.pareto_colors = pass_colors_2
    assert test_chart.pareto_colors == pass_colors_2
