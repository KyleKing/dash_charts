"""Test the file examples/ex_pareto_chart.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_pareto_chart


@pytest.mark.CHROME
def test_smoke_test_ex_pareto_chart(dash_duo):
    """Test ex_pareto_chart."""
    dash_duo.start_server(ex_pareto_chart.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
