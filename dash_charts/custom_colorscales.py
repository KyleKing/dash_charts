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


def makecolorbar(colorscale=((1,), (10,), (100,))):
    """Format a colorbar.

    colorscale -- colorscale lists of lists where the value is the first index

    """
    # Set tickvalues array
    vals = [_c[0] for _c in colorscale]
    min_val = np.min([val for val in vals if val != 0])
    return {
        'tick0': 0,
        'tickmode': 'array',
        'tickvals': np.divide(vals, min_val),
    }


logFire = [
    # 313695, FEE090, D73027 (33 steps, 14 steps)
    [0, '#000000'],
    [1. / pow(10, 9), '#0C0D25'],
    [1. / pow(10, 8), '#181B4A'],
    [1. / pow(10, 7), '#24286F'],
    [1. / pow(10, 6), '#313695'],
    [1. / pow(10, 5), '#363A94'],
    [1. / pow(10, 4), '#393C94'],
    [1. / pow(10, 3), '#3C3F94'],
    # [1. / pow(10, 2.9), '#414394'],
    # [1. / pow(10, 2.8), '#474894'],
    # [1. / pow(10, 2.7), '#4C4C94'],
    # [1. / pow(10, 2.6), '#525194'],
    # [1. / pow(10, 2.5), '#575694'],
    # [1. / pow(10, 2.4), '#5D5A93'],
    # [1. / pow(10, 2.3), '#625F93'],
    # [1. / pow(10, 2.2), '#686393'],
    # [1. / pow(10, 2.1), '#6D6893'],
    [1. / pow(10, 2.00), '#736D93'],
    # [1. / pow(10, 1.95), '#797193'],
    # [1. / pow(10, 1.90), '#7E7693'],
    # [1. / pow(10, 1.85), '#847A92'],
    # [1. / pow(10, 1.80), '#897F92'],
    # [1. / pow(10, 1.75), '#8F8492'],
    # [1. / pow(10, 1.70), '#948892'],
    # [1. / pow(10, 1.65), '#9A8D92'],
    # [1. / pow(10, 1.60), '#9F9192'],
    # [1. / pow(10, 1.55), '#A59692'],
    # [1. / pow(10, 1.50), '#AA9B92'],
    # [1. / pow(10, 1.45), '#B09F91'],
    # [1. / pow(10, 1.40), '#B5A491'],
    # [1. / pow(10, 1.35), '#BBA891'],
    # [1. / pow(10, 1.30), '#C1AD91'],
    # [1. / pow(10, 1.25), '#C6B291'],
    # [1. / pow(10, 1.20), '#CCB691'],
    # [1. / pow(10, 1.15), '#D1BB91'],
    # [1. / pow(10, 1.10), '#D7BF90'],
    # [1. / pow(10, 1.05), '#DCC490'],
    [1. / pow(10, 1.00), '#E2C990'],
    # [1. / pow(10, 0.95), '#E7CD90'],
    # [1. / pow(10, 0.90), '#EDD290'],
    # [1. / pow(10, 0.85), '#F2D690'],
    # [1. / pow(10, 0.80), '#F8DB90'],
    # [1. / pow(10, 0.75), '#FEE090'],
    # [1. / pow(10, 0.70), '#FACE85'],
    # [1. / pow(10, 0.65), '#F6BC7B'],
    # [1. / pow(10, 0.60), '#F2AB70'],
    # [1. / pow(10, 0.55), '#EE9966'],
    # [1. / pow(10, 0.50), '#EA885B'],
    # [1. / pow(10, 0.45), '#E67651'],
    # [1. / pow(10, 0.40), '#E26446'],
    # [1. / pow(10, 0.35), '#DE533C'],
    [1. / pow(10, 0.30), '#DA4131'],
    [1. / pow(10, 0.25), '#D73027'],
    [1., '#A50026'],
]
