"""Test utils_fig."""

import pytest

from dash_charts.utils_fig import CustomChart


class TestChart(CustomChart):  # noqa: H601
    """Custom chart for testing."""

    __test__ = False


def test_axis_range_property():
    """Test setting the axis_range property on the CustomChart base class."""
    test_chart = TestChart(title='', xlabel='', ylabel='')
    pass_range_1 = {'x': [15, 25]}
    pass_range_2 = {'x': [15, 25]}
    fail_range_1 = {'x': [1, 2, 3]}
    fail_message_1 = "Validation of self.axis_range failed: {'x': ['length of list should be 2, it is 3']}"

    with pytest.raises(RuntimeError) as fail_error_1:
        test_chart.axis_range = fail_range_1

    assert str(fail_error_1.value) == fail_message_1
    test_chart.axis_range = pass_range_1
    assert test_chart.axis_range == pass_range_1
    test_chart.axis_range = pass_range_2
    assert test_chart.axis_range == pass_range_2
