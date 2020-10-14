"""Test utils_fig."""

import math

import numpy as np
import pytest
from matplotlib import pyplot as plt

from dash_charts import utils_fig


def test_convert_matplolib():
    """Test convert_matplolib."""
    # Create figure with example code from plotly.py tests
    fig = plt.figure()
    x_values = [10, 20, 30]
    y_values = [100, 200, 300]
    plt.plot(x_values, y_values)

    result = utils_fig.convert_matplolib(fig)  # Convert to Plotly

    assert result


def test_convert_matplolib_docs():
    """Test convert_matplolib."""
    # Create Example Plot of a Sine Wave
    x_coords = np.arange(0, math.pi * 2, 0.05)
    plt.plot(x_coords, np.sin(x_coords))
    plt.xlabel('Angle')
    plt.ylabel('Sine')
    plt.title('Sine Wave')
    fig = plt.gcf()

    result = utils_fig.convert_matplolib(fig)  # Convert to Plotly

    assert result


class TestChart(utils_fig.CustomChart):  # noqa: H601
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
