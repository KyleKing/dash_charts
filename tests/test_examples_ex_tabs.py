"""Test the file examples/ex_tabs.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_tabs


@pytest.mark.INTERACTIVE()
def test_smoke_test_ex_tabs(dash_duo):
    """Test ex_tabs."""
    dash_duo.start_server(ex_tabs.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
