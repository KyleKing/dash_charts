"""Test the file examples/ex_rolling_chart.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_rolling_chart


@pytest.mark.INTERACTIVE()
def test_smoke_test_ex_rolling_chart(dash_duo):
    """Test ex_rolling_chart."""
    dash_duo.start_server(ex_rolling_chart.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
