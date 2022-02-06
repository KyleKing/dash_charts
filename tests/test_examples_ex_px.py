"""Test the file examples/ex_app_px.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_app_px


@pytest.mark.INTERACTIVE
def test_smoke_test_ex_app_px(dash_duo):
    """Test ex_app_px."""
    dash_duo.start_server(ex_app_px.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
