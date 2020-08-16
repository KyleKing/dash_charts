"""Test the file examples/ex_coordinate_chart.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_coordinate_chart


@pytest.mark.CHROME
def test_smoke_test_ex_coordinate_chart(dash_duo):
    """Test ex_coordinate_chart."""
    dash_duo.start_server(ex_coordinate_chart.app.app)

    time.sleep(1)

    assert no_log_errors(dash_duo)
