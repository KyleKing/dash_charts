"""Final test alphabetically (zz) to catch general integration cases."""

import toml
from dash_charts import __version__


def test_version():
    """Check that PyProject and __version__ are equivalent."""
    assert toml.load('pyproject.toml')['tool']['poetry']['version'] == __version__
