"""Test utils_helpers."""

from dash_charts import utils_helpers


def test_graph_return():
    """Test the graph return function."""
    raw_resp = {'A': 1, 'B': 2, 'C': None}
    exp_resp = [2, 1]

    result = utils_helpers.graph_return(raw_resp, keys=('B', 'A'))

    assert result == exp_resp
