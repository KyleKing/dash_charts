"""Test the file dash_charts/utils_static.py."""

from pathlib import Path

from dash_charts.utils_static import WritePlotlyHTML


def test_smoke_test_write_plotly_html():
    """Smoke test WritePlotlyHTML static."""
    filename = Path(__file__).parent / 'tmp.html'
    filename.write_text('')

    with WritePlotlyHTML(filename) as output:  # act
        output.write('')

    assert len(filename.read_text().split('\n')) == 26
