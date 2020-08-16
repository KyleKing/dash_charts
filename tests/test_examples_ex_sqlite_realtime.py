"""Test the file examples/ex_sqlite_realtime.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_sqlite_realtime


@pytest.mark.CHROME
def test_smoke_test_ex_sqlite_realtime(dash_duo):
    """Test ex_sqlite_realtime."""
    dash_duo.start_server(ex_sqlite_realtime.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
