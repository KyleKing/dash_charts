"""Custom Plotly Colorscales.

Gradients genrated with: http://herethere.net/~samson/php/color_gradient/

"""

import numpy as np

DEFAULT_PLOTLY_COLORS = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf',  # blue-teal
]
"""List of default Plotly colors in Hex strings."""

DEFAULT_PLOTLY_COLORS_RGB = [
    'rgb(31,119,180)',   # 0
    'rgb(255,127,14)',   # 1
    'rgb(44,160,44)',    # 2
    'rgb(214,39,40)',    # 3
    'rgb(148,103,189)',  # 4
    'rgb(140,86,75)',    # 5
    'rgb(227,119,194)',  # 6
    'rgb(127,127,127)',  # 7
    'rgb(188,189,34)',   # 8
    'rgb(23,190,207)',   # 9
]
"""List of default Plotly colors in RGB strings."""


# PLANNED: DELETE
def make_colorbar(colorscale=((1,), (10,), (100,))):
    """Return dictionary for Plotly colorbar.

    Args:
        colorscale: colorscale lists of lists where the value is the first index

    Returns:
        dict: colorbar dictionary with keys `(tick0, tickmode, tickvals)`

    """
    values = [_c[0] for _c in colorscale]
    min_val = np.min([val for val in values if val != 0])
    return {
        'tick0': 0,
        'tickmode': 'array',
        'tickvals': np.divide(values, min_val),
    }
