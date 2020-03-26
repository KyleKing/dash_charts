"""Test the file examples/ex_utils_static.py."""

import tempfile
from pathlib import Path

from .examples import ex_utils_static


def test_smoke_test_write_plotly_html():
    """Smoke test WritePlotlyHTML static."""
    with tempfile.TemporaryDirectory() as dir_name:  # act
        filename = Path(dir_name) / 'tmp.html'
        ex_utils_static.write_sample_html(filename)
        content = filename.read_text()

    assert len(content.split('\n')) == 99659
