"""Test the file examples/ex_gantt_chart.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_gantt_chart


@pytest.mark.INTERACTIVE
def test_smoke_test_ex_gantt_chart(dash_duo):
    """Test ex_gantt_chart."""
    dash_duo.start_server(ex_gantt_chart.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
