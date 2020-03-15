"""Test equations."""

import math

import numpy as np
from dash_charts import equations


def test_linear():
    """Test the linear equation."""
    factor_a, factor_b = 0.5, 100
    x_values = [-1, 0, 1, 10, 100]
    y_expected = [99.5, 100, 100.5, 105, 150]
    x_single = -5
    y_expected_single = 97.5

    y_values = equations.linear(x_values, factor_a, factor_b)
    y_single = equations.linear(x_single, factor_a, factor_b)

    assert np.allclose(y_values, y_expected)
    assert y_single == y_expected_single


def test_quadratic():
    """Test the quadratic equation."""
    factor_a, factor_b, factor_c = 0.4, 2.1, 30
    x_values = [-1, 0, 1, 10, 100]
    y_expected = np.array([28.3, 30, 32.5, 91, 4240])
    x_single = -5
    y_expected_single = 29.5

    y_values = equations.quadratic(x_values, factor_a, factor_b, factor_c)
    y_single = equations.quadratic(x_single, factor_a, factor_b, factor_c)

    assert np.allclose(y_values, y_expected)
    assert y_single == y_expected_single


def test_power():
    """Test the power equation."""
    factor_a, factor_b = 5, 3
    x_values = [-5, -1, 0, 1, 10]
    y_expected = [-625, -5, 0, 5, 5000]
    x_single = -2
    y_expected_single = -40

    y_values = equations.power(x_values, factor_a, factor_b)
    y_single = equations.power(x_single, factor_a, factor_b)

    assert np.allclose(y_values, y_expected)
    assert y_single == y_expected_single


def test_exponential():
    """Test the exponential equation."""
    factor_a, factor_b = 5, 3
    x_values = [-1, 0, 10]
    y_expected = [5 * math.exp(-3), 5, 5 * math.exp(30)]
    x_single = math.log(2)
    y_expected_single = 39.99999999999999

    y_values = equations.exponential(x_values, factor_a, factor_b)
    y_single = equations.exponential(x_single, factor_a, factor_b)

    assert np.allclose(y_values, y_expected)
    assert y_single == y_expected_single


def test_double_exponential():
    """Test the double_exponential equation."""
    factor_a, factor_b, factor_c, factor_d = 2, 5, 0.5, 1
    x_values = [-1, 0, 1, math.log(3)]
    y_expected = [-0.170464, 1.5, 295.467, 484.5]
    x_single = -2
    y_expected_single = -0.06757684175878138

    y_values = equations.double_exponential(x_values, factor_a, factor_b, factor_c, factor_d)
    y_single = equations.double_exponential(x_single, factor_a, factor_b, factor_c, factor_d)

    assert np.allclose(y_values, y_expected)
    assert y_single == y_expected_single
