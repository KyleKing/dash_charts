"""Test the file examples/ex_marginal_chart.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_marginal_chart


@pytest.mark.INTERACTIVE
def test_smoke_test_ex_marginal_chart(dash_duo):
    """Test ex_marginal_chart."""
    dash_duo.start_server(ex_marginal_chart.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
