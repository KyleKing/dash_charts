"""Equations used in scipy fit calculations."""

import numpy as np


def linear(x_values, factor_a, factor_b):
    """Return result(s) of linear equation with factors of a and b.

    `y = a * x + b`

    Args:
        x_values: single number of list of numbers
        factor_a: number, slope
        factor_b: number, intercept

    Returns:
        y_values: as list or single digit

    """
    return np.add(
        np.multiply(factor_a, x_values),
        factor_b,
    )


def quadratic(x_values, factor_a, factor_b, factor_c):
    """Return result(s) of quadratic equation with factors of a, b, and c.

    `y = a * x^2 + b * x + c`

    Args:
        x_values: single number of list of numbers
        factor_a: number
        factor_b: number
        factor_c: number

    Returns:
        y_values: as list or single digit

    """
    return np.add(
        np.multiply(
            factor_a,
            np.power(x_values, 2),
        ),
        np.add(
            np.multiply(factor_b, x_values),
            factor_c,
        ),
    )


def power(x_values, factor_a, factor_b):
    """Return result(s) of quadratic equation with factors of a and b.

    `y = a * x^b`

    Args:
        x_values: single number of list of numbers
        factor_a: number
        factor_b: number

    Returns:
        y_values: as list or single digit

    """
    return np.multiply(
        factor_a,
        np.power(
            np.array(x_values).astype(float),
            factor_b,
        ),
    )


def exponential(x_values, factor_a, factor_b):
    """Return result(s) of exponential equation with factors of a and b.

    `y = a * e^(b * x)`

    Args:
        x_values: single number of list of numbers
        factor_a: number
        factor_b: number

    Returns:
        y_values: as list or single digit

    """
    return np.multiply(
        factor_a,
        np.exp(
            np.multiply(factor_b, x_values),
        ),
    )


def double_exponential(x_values, factor_a, factor_b, factor_c, factor_d):
    """Return result(s) of a double exponential equation with factors of a, b, c, and d.

    `y = a * e^(b * x) - c * e^(d * x)`

    Args:
        x_values: single number of list of numbers
        factor_a: number
        factor_b: number
        factor_c: number
        factor_d: number

    Returns:
        y_values: as list or single digit

    """
    return np.subtract(
        np.multiply(
            factor_a,
            np.exp(
                np.multiply(factor_b, x_values),
            ),
        ),
        np.multiply(
            factor_c,
            np.exp(
                np.multiply(factor_d, x_values),
            ),
        ),
    )
