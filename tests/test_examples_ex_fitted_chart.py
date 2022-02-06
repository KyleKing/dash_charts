"""Test the file examples/ex_fitted_chart.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_fitted_chart


@pytest.mark.INTERACTIVE()
def test_smoke_test_ex_fitted_chart(dash_duo):
    """Test ex_fitted_chart."""
    dash_duo.start_server(ex_fitted_chart.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
