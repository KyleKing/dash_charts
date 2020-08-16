"""Test the file examples/ex_time_vis_chart.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_time_vis_chart


@pytest.mark.CHROME
def test_smoke_test_ex_time_vis_chart(dash_duo):
    """Test ex_time_vis_chart."""
    dash_duo.start_server(ex_time_vis_chart.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
