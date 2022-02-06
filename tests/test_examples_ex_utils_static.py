"""Test the file examples/ex_utils_static.py."""

import tempfile
from pathlib import Path

from .examples import ex_utils_static


def test_smoke_test_write_plotly_html():
    """Smoke test WritePlotlyHTML."""
    try:
        with tempfile.TemporaryDirectory() as dir_name:  # act
            filename = Path(dir_name) / 'tmp.html'

            ex_utils_static.write_sample_html(filename)  # act

            content = filename.read_text()
    except ValueError as exc:
        raise ValueError(
            'Likely no orca installation was found. Try'
            + ' "brew install orca" (and open to finish the installation)'
            + ' or "conda install -c plotly plotly-orca" for Windows',
        ) from exc
    assert len(content.split('\n')) >= 2500


def test_smoke_test_write_from_markdown():
    """Smoke test write_from_markdown."""
    ex_utils_static.example_write_from_markdown()  # act
