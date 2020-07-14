"""Test custom_colorscales."""

from dash_charts import custom_colorscales


def test_colorscales():
    """Test the length of the colorscales variables."""
    result = 10

    assert len(custom_colorscales.DEFAULT_PLOTLY_COLORS) == result
    assert len(custom_colorscales.DEFAULT_PLOTLY_COLORS_RGB) == result
